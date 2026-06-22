"""Safe setup, verification, skill installation, and uninstall orchestration."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .clients import (
    codex_config_path,
    register_claude,
    register_codex,
    server_spec,
    unregister_claude,
    unregister_codex,
    verify_claude,
    verify_codex,
    verify_qwen,
)
from .constants import DEFAULT_MCP_VERSION
from .discovery import PolyspaceInstallation, detect_platform
from .errors import OwnershipConflict, ToolkitError
from .releases import backup_file, download_verified, release_asset, release_url
from .state import binary_path, load_state, save_state, sha256_file, sha256_tree, state_dir


def _skills_root() -> Path:
    root = Path(__file__).resolve().parents[2] / "skills"
    if not root.is_dir():
        raise ToolkitError(
            "Product skills are unavailable; run setup from a permanent source checkout"
        )
    return root


def _skill_destination(client: str) -> Path:
    if client == "codex":
        return Path.home() / ".agents" / "skills"
    if client == "claude":
        return Path.home() / ".claude" / "skills"
    raise ToolkitError(f"Automated skill installation is unsupported for {client}")


def _install_skills(
    client: str,
    replace: bool,
    backup_root: Path,
    previous_records: Iterable[dict[str, Any]] = (),
) -> list[dict[str, Any]]:
    source_root = _skills_root()
    records: list[dict[str, Any]] = []
    previous_by_path = {record["path"]: record for record in previous_records}
    destination_root = _skill_destination(client)
    destination_root.mkdir(parents=True, exist_ok=True)
    sources = sorted(path for path in source_root.iterdir() if (path / "SKILL.md").is_file())

    # Detect every ownership conflict before copying the first skill. Otherwise a collision late in
    # the catalog can leave earlier skills installed even though setup reports failure.
    for source in sources:
        destination = destination_root / source.name
        if not destination.exists():
            continue
        previous_hash = sha256_tree(destination) if destination.is_dir() else None
        if previous_hash == sha256_tree(source):
            continue
        previous_record = previous_by_path.get(str(destination))
        previously_owned = bool(
            previous_record
            and previous_record.get("owned")
            and previous_hash == previous_record.get("installedHash")
        )
        if not replace and not previously_owned:
            raise OwnershipConflict(f"Skill destination already exists: {destination}")

    for source in sources:
        destination = destination_root / source.name
        previous_hash = sha256_tree(destination) if destination.is_dir() else None
        previous_record = previous_by_path.get(str(destination))
        backup: Path | None = None
        source_hash = sha256_tree(source)
        if previous_hash == source_hash:
            records.append(
                {
                    "path": str(destination),
                    "installedHash": source_hash,
                    "backup": (
                        previous_record.get("backup") if previous_record is not None else None
                    ),
                    "owned": bool(previous_record is not None and previous_record.get("owned")),
                }
            )
            continue
        if destination.exists():
            previously_owned = bool(
                previous_record
                and previous_record.get("owned")
                and previous_hash == previous_record.get("installedHash")
            )
            if not replace and not previously_owned:
                raise OwnershipConflict(f"Skill destination already exists: {destination}")
            if previously_owned:
                assert previous_record is not None
            if previously_owned and previous_record is not None and previous_record.get("backup"):
                backup = Path(previous_record["backup"])
            elif not previously_owned:
                backup = backup_root / "skills" / client / source.name
                if backup.exists():
                    shutil.rmtree(backup)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(destination, backup)
            shutil.rmtree(destination)
        temporary = destination.with_name(f".{destination.name}.installing")
        if temporary.exists():
            shutil.rmtree(temporary)
        shutil.copytree(source, temporary)
        os.replace(temporary, destination)
        records.append(
            {
                "path": str(destination),
                "installedHash": source_hash,
                "backup": str(backup) if backup else None,
                "owned": True,
            }
        )
    return records


def _remove_skills(records: Iterable[dict[str, Any]]) -> None:
    for record in records:
        if not record.get("owned"):
            continue
        destination = Path(record["path"])
        if destination.exists() and sha256_tree(destination) != record["installedHash"]:
            raise OwnershipConflict(f"Installed skill changed after setup: {destination}")
        if destination.exists():
            shutil.rmtree(destination)
        backup = record.get("backup")
        if backup and Path(backup).exists():
            shutil.copytree(Path(backup), destination)


def _probe_binary(path: Path) -> None:
    try:
        result = subprocess.run(
            (str(path), "--version"), capture_output=True, text=True, check=False, timeout=15
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ToolkitError(f"Installed MCP server did not execute: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise ToolkitError(f"Installed MCP server version check failed: {detail}")


def setup_plan(
    clients: list[str],
    installation: PolyspaceInstallation | None,
    version: str = DEFAULT_MCP_VERSION,
    telemetry: bool = False,
    replace_existing: bool = False,
) -> dict[str, Any]:
    host = detect_platform()
    asset = release_asset(version, host.os_name, host.architecture)
    client_details: dict[str, object] = {}
    for client in clients:
        if client == "codex":
            client_details[client] = {
                "mcpConfig": str(codex_config_path()),
                "skills": str(_skill_destination(client)),
            }
        elif client == "claude":
            client_details[client] = {
                "mcpScope": "user",
                "marketplace": str(Path(__file__).resolve().parents[2]),
                "skills": str(_skill_destination(client)),
            }
        else:
            raise ToolkitError(f"Unsupported automated client: {client}")
    return {
        "platform": {"os": host.os_name, "architecture": host.architecture},
        "polyspace": (
            {"root": str(installation.root), "release": installation.release}
            if installation
            else None
        ),
        "mcpServer": {
            "version": version,
            "asset": asset.name,
            "sha256": asset.sha256,
            "download": release_url(version, asset),
            "installPath": str(binary_path(host.os_name)),
        },
        "statePath": str(state_dir() / "state.json"),
        "clients": client_details,
        "telemetryEnabled": telemetry,
        "replaceExisting": replace_existing,
    }


def setup(
    clients: list[str],
    installation: PolyspaceInstallation | None,
    version: str = DEFAULT_MCP_VERSION,
    replace_existing: bool = False,
    telemetry: bool = False,
) -> dict[str, Any]:
    host = detect_platform()
    asset = release_asset(version, host.os_name, host.architecture)
    state_path = state_dir() / "state.json"
    state = load_state(state_path)
    target = binary_path(host.os_name)
    backup_root = state_dir() / "backups"
    prior_binary = state.get("binary")
    binary_backup: Path | None = None
    current_digest = sha256_file(target) if target.is_file() else None
    binary_changed = current_digest != asset.sha256
    if current_digest != asset.sha256:
        if target.exists():
            if prior_binary and prior_binary.get("owned") and prior_binary.get("backup"):
                binary_backup = Path(prior_binary["backup"])
            else:
                binary_backup = backup_root / "binary" / target.name
                backup_file(target, binary_backup)
        try:
            download_verified(release_url(version, asset), asset.sha256, target)
            _probe_binary(target)
        except Exception:
            target.unlink(missing_ok=True)
            if binary_backup and binary_backup.exists():
                backup_file(binary_backup, target)
            raise
    elif prior_binary and prior_binary.get("backup"):
        binary_backup = Path(prior_binary["backup"])
    state["binary"] = {
        "path": str(target),
        "version": version,
        "digest": asset.sha256,
        "backup": str(binary_backup) if binary_backup else None,
        "owned": bool(binary_changed or (prior_binary and prior_binary.get("owned"))),
    }

    spec = server_spec(target, installation.root if installation else None, telemetry)
    changed_registrations: list[tuple[str, dict[str, Any]]] = []
    changed_skills: list[list[dict[str, Any]]] = []
    try:
        for client in clients:
            prior_registration = state.get("clients", {}).get(client)
            skill_records = _install_skills(
                client,
                replace_existing,
                backup_root,
                state.get("skills", {}).get(client, []),
            )
            changed_skills.append(skill_records)
            if client == "codex":
                owned_and_unchanged = bool(
                    prior_registration
                    and prior_registration.get("owned")
                    and verify_codex(prior_registration)
                )
                registration = register_codex(spec, replace_existing or owned_and_unchanged)
            elif client == "claude":
                owned_and_unchanged = bool(
                    prior_registration
                    and prior_registration.get("owned")
                    and verify_claude(prior_registration)
                )
                registration = register_claude(spec, replace_existing or owned_and_unchanged)
            else:
                raise ToolkitError(f"Unsupported automated client: {client}")
            rollback_registration = dict(registration)
            registration_changed = bool(registration["changed"])
            if not registration["changed"] and prior_registration:
                registration = prior_registration
            else:
                registration["owned"] = bool(registration["changed"])
                if owned_and_unchanged and prior_registration:
                    registration["previous"] = prior_registration.get("previous")
                    registration["marketplaceAdded"] = bool(
                        registration.get("marketplaceAdded")
                        or prior_registration.get("marketplaceAdded")
                    )
            state["clients"][client] = registration
            state["skills"][client] = skill_records
            if registration.get("owned") and registration_changed:
                changed_registrations.append((client, rollback_registration))
    except Exception:
        for client, registration in reversed(changed_registrations):
            if client == "codex":
                unregister_codex(registration)
            elif client == "claude":
                unregister_claude(registration)
        for records in reversed(changed_skills):
            _remove_skills(records)
        if binary_changed:
            target.unlink(missing_ok=True)
            if binary_backup and binary_backup.exists():
                backup_file(binary_backup, target)
        raise
    state["polyspace"] = (
        {"root": str(installation.root), "release": installation.release} if installation else None
    )
    state["telemetryEnabled"] = telemetry
    save_state(state_path, state)
    return state


def verify(client: str) -> dict[str, object]:
    state = load_state(state_dir() / "state.json")
    binary = state.get("binary")
    binary_record = binary if isinstance(binary, dict) else None
    binary_ok = bool(binary_record and Path(binary_record["path"]).is_file())
    digest_ok = bool(
        binary_ok
        and binary_record
        and sha256_file(Path(binary_record["path"])) == binary_record["digest"]
    )
    if client == "all":
        client_state = state.get("clients", {})
        clients = {
            "codex": bool(client_state.get("codex") and verify_codex(client_state["codex"])),
            "claude": bool(client_state.get("claude") and verify_claude(client_state["claude"])),
            "qwen": verify_qwen(),
        }
    elif client == "qwen":
        clients = {"qwen": verify_qwen()}
    else:
        record = state.get("clients", {}).get(client)
        verifier = verify_codex if client == "codex" else verify_claude
        clients = {client: bool(record and verifier(record))}
    return {
        "binary": binary_ok,
        "digest": digest_ok,
        "polyspace": state.get("polyspace"),
        "clients": clients,
        "ready": binary_ok
        and digest_ok
        and state.get("polyspace") is not None
        and all(clients.values()),
    }


def uninstall(clients: list[str]) -> dict[str, Any]:
    state_path = state_dir() / "state.json"
    state = load_state(state_path)
    selected = list(state.get("clients", {})) if "all" in clients else clients
    for client in selected:
        record = state.get("clients", {}).get(client)
        if record is None:
            continue
        if record.get("owned"):
            if client == "codex":
                unregister_codex(record)
            elif client == "claude":
                unregister_claude(record)
        _remove_skills(state.get("skills", {}).get(client, []))
        state["clients"].pop(client, None)
        state["skills"].pop(client, None)
    if not state.get("clients") and state.get("binary"):
        binary = state["binary"]
        target = Path(binary["path"])
        if target.exists() and sha256_file(target) != binary["digest"]:
            raise OwnershipConflict(f"MCP binary changed after setup: {target}")
        if binary.get("owned"):
            target.unlink(missing_ok=True)
        backup = binary.get("backup")
        if backup and Path(backup).exists():
            backup_file(Path(backup), target)
        state["binary"] = None
    save_state(state_path, state)
    return state
