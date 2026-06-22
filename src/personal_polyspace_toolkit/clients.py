"""Conservative, user-scoped client registration adapters."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomlkit

from .constants import PRODUCT_SKILLS
from .errors import OwnershipConflict, ToolkitError
from .state import atomic_write_text


@dataclass(frozen=True)
class ServerSpec:
    command: str
    args: tuple[str, ...]

    def as_json(self) -> dict[str, object]:
        return {"command": self.command, "args": list(self.args)}


def server_spec(binary: Path, polyspace_root: Path | None, telemetry: bool) -> ServerSpec:
    args: list[str] = []
    if polyspace_root is not None:
        args.append(f"--polyspace-root={polyspace_root}")
    if not telemetry:
        args.append("--disable-telemetry=true")
    return ServerSpec(str(binary.resolve()), tuple(args))


def codex_config_path(env: Mapping[str, str] | None = None) -> Path:
    environment = env or os.environ
    return Path(environment.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"


def desired_codex_entry(spec: ServerSpec, windows: bool) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "command": spec.command,
        "args": list(spec.args),
        "tool_timeout_sec": 600,
        "default_tools_approval_mode": "prompt",
    }
    if windows:
        entry["env_vars"] = ["WINDIR"]
    return entry


def register_codex(
    spec: ServerSpec,
    replace_existing: bool,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    path = codex_config_path(env)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    try:
        document = tomlkit.parse(text)
    except Exception as error:
        raise ToolkitError(f"Cannot parse Codex config {path}: {error}") from error
    servers = document.get("mcp_servers")
    if servers is None:
        servers = tomlkit.table()
        document["mcp_servers"] = servers
    assert servers is not None
    existing = servers.get("polyspace")
    previous = existing.unwrap() if existing is not None else None
    desired = desired_codex_entry(spec, os.name == "nt")
    if previous == desired:
        return {"path": str(path), "previous": previous, "installed": desired, "changed": False}
    if existing is not None and not replace_existing:
        raise OwnershipConflict(
            f"Codex already has a different polyspace MCP entry in {path}; use --replace-existing"
        )
    entry = tomlkit.table()
    for key, value in desired.items():
        entry[key] = value
    servers["polyspace"] = entry
    atomic_write_text(path, tomlkit.dumps(document))
    return {"path": str(path), "previous": previous, "installed": desired, "changed": True}


def unregister_codex(record: Mapping[str, Any]) -> None:
    path = Path(str(record["path"]))
    document = tomlkit.parse(path.read_text(encoding="utf-8"))
    servers = document.get("mcp_servers")
    if servers is None:
        raise OwnershipConflict(f"Codex polyspace entry is missing from {path}")
    current = servers.get("polyspace") if servers is not None else None
    current_value = current.unwrap() if current is not None else None
    if current_value != record.get("installed"):
        raise OwnershipConflict(
            f"Codex polyspace entry in {path} changed after setup; refusing removal"
        )
    previous = record.get("previous")
    if previous is None:
        del servers["polyspace"]
    else:
        restored = tomlkit.table()
        for key, value in previous.items():
            restored[key] = value
        servers["polyspace"] = restored
    atomic_write_text(path, tomlkit.dumps(document))


def verify_codex(record: Mapping[str, Any]) -> bool:
    path = Path(str(record.get("path", "")))
    if not path.is_file():
        return False
    try:
        document = tomlkit.parse(path.read_text(encoding="utf-8"))
        servers = document.get("mcp_servers")
        current = servers.get("polyspace") if servers is not None else None
        return current is not None and current.unwrap() == record.get("installed")
    except (OSError, ValueError):
        return False


def _run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def _claude_snapshot() -> dict[str, Any] | None:
    result = _run(("claude", "mcp", "get", "polyspace"))
    if result.returncode != 0:
        return None
    fields: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip().lower()] = value.strip()
    command = fields.get("command")
    if not command:
        return {"raw": result.stdout, "restorable": False}
    args = tuple(shlex.split(fields["args"], posix=os.name != "nt")) if fields.get("args") else ()
    return {"command": command, "args": list(args), "restorable": True}


def _marketplace_name_present(output: str) -> bool:
    return "personal-polyspace-toolkit" in output.lower()


def _register_claude_marketplace() -> bool:
    listed = _run(("claude", "plugin", "marketplace", "list"))
    if listed.returncode == 0 and _marketplace_name_present(listed.stdout):
        return False
    root = Path(__file__).resolve().parents[2]
    if not (root / ".claude-plugin" / "marketplace.json").is_file():
        raise ToolkitError(
            "Claude marketplace metadata is unavailable; run setup from a source checkout"
        )
    added = _run(("claude", "plugin", "marketplace", "add", str(root)))
    if added.returncode != 0:
        raise ToolkitError(added.stderr.strip() or "Failed to add the Claude plugin marketplace")
    return True


def register_claude(spec: ServerSpec, replace_existing: bool) -> dict[str, Any]:
    if shutil.which("claude") is None:
        raise ToolkitError("Claude Code CLI is not installed or not in PATH")
    previous = _claude_snapshot()
    if (
        previous is not None
        and previous.get("command") == spec.command
        and previous.get("args") == list(spec.args)
    ):
        marketplace_added = _register_claude_marketplace()
        return {
            "previous": previous,
            "installed": spec.as_json(),
            "changed": marketplace_added,
            "marketplaceAdded": marketplace_added,
        }
    if previous is not None and not replace_existing:
        raise OwnershipConflict("Claude already has a different polyspace MCP registration")
    if previous is not None and not previous.get("restorable"):
        raise OwnershipConflict("Claude's existing registration cannot be safely backed up")
    if previous is not None:
        removed = _run(("claude", "mcp", "remove", "polyspace", "-s", "user"))
        if removed.returncode != 0:
            raise ToolkitError(
                removed.stderr.strip() or "Failed to remove existing Claude registration"
            )
    payload = json.dumps(spec.as_json(), separators=(",", ":"))
    added = _run(("claude", "mcp", "add-json", "polyspace", payload, "-s", "user"))
    if added.returncode != 0:
        raise ToolkitError(added.stderr.strip() or "Failed to register Polyspace with Claude")
    try:
        marketplace_added = _register_claude_marketplace()
    except Exception:
        _run(("claude", "mcp", "remove", "polyspace", "-s", "user"))
        if previous:
            previous_payload = json.dumps(
                {"command": previous["command"], "args": previous.get("args", [])},
                separators=(",", ":"),
            )
            _run(
                (
                    "claude",
                    "mcp",
                    "add-json",
                    "polyspace",
                    previous_payload,
                    "-s",
                    "user",
                )
            )
        raise
    return {
        "previous": previous,
        "installed": spec.as_json(),
        "changed": True,
        "marketplaceAdded": marketplace_added,
    }


def unregister_claude(record: Mapping[str, Any]) -> None:
    if shutil.which("claude") is None:
        raise ToolkitError("Claude Code CLI is required to remove its MCP registration")
    current = _claude_snapshot()
    installed = record.get("installed")
    if not isinstance(installed, dict):
        raise ToolkitError("Claude ownership state is missing the installed server specification")
    if current is not None and (
        current.get("command") != installed.get("command")
        or current.get("args") != installed.get("args")
    ):
        raise OwnershipConflict(
            "Claude polyspace registration changed after setup; refusing removal"
        )
    removed = _run(("claude", "mcp", "remove", "polyspace", "-s", "user"))
    if current is not None and removed.returncode != 0:
        raise ToolkitError(removed.stderr.strip() or "Failed to remove Claude registration")
    previous = record.get("previous")
    if previous:
        payload = json.dumps(
            {"command": previous["command"], "args": previous.get("args", [])},
            separators=(",", ":"),
        )
        restored = _run(("claude", "mcp", "add-json", "polyspace", payload, "-s", "user"))
        if restored.returncode != 0:
            raise ToolkitError(restored.stderr.strip() or "Failed to restore Claude registration")
    if record.get("marketplaceAdded"):
        removed_marketplace = _run(
            ("claude", "plugin", "marketplace", "remove", "personal-polyspace-toolkit")
        )
        if removed_marketplace.returncode != 0:
            raise ToolkitError(
                removed_marketplace.stderr.strip() or "Failed to remove the Claude marketplace"
            )


def verify_claude(record: Mapping[str, Any]) -> bool:
    if shutil.which("claude") is None:
        return False
    current = _claude_snapshot()
    installed = record.get("installed")
    return bool(
        current
        and isinstance(installed, dict)
        and current.get("command") == installed.get("command")
        and current.get("args") == installed.get("args")
    )


def verify_qwen() -> bool:
    if shutil.which("qwen") is None:
        return False
    settings_path = Path.home() / ".qwen" / "settings.json"
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    servers = settings.get("mcpServers")
    providers = settings.get("modelProviders")
    polyspace = servers.get("polyspace") if isinstance(servers, dict) else None
    openai = providers.get("openai") if isinstance(providers, dict) else None
    if not isinstance(polyspace, dict) or not isinstance(openai, list) or not openai:
        return False
    serialized = json.dumps({"polyspace": polyspace, "openai": openai})
    skills_root = Path.home() / ".qwen" / "skills"
    skills_ok = all((skills_root / name / "SKILL.md").is_file() for name in PRODUCT_SKILLS)
    return "REPLACE_WITH_" not in serialized and skills_ok
