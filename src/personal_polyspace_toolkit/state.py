"""Ownership-tracked state with atomic persistence."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .constants import STATE_SCHEMA_VERSION
from .errors import ToolkitError


def state_dir(env: Mapping[str, str] | None = None) -> Path:
    environment = env or os.environ
    if os.name == "nt":
        base = Path(environment.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(environment.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return base / "personal-polyspace-toolkit"


def binary_path(os_name: str, env: Mapping[str, str] | None = None) -> Path:
    environment = env or os.environ
    if os_name == "windows":
        base = Path(environment.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "polyspace" / "polyspace-mcp-server.exe"
    return (
        Path(environment.get("HOME", str(Path.home()))) / ".local" / "bin" / "polyspace-mcp-server"
    )


def empty_state() -> dict[str, Any]:
    return {"schemaVersion": STATE_SCHEMA_VERSION, "binary": None, "clients": {}, "skills": {}}


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ToolkitError(f"Cannot read toolkit state {path}: {error}") from error
    if not isinstance(data, dict) or data.get("schemaVersion") != STATE_SCHEMA_VERSION:
        raise ToolkitError(f"Unsupported toolkit state in {path}")
    return data


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def save_state(path: Path, data: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for child in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(child.relative_to(path).as_posix().encode())
        digest.update(child.read_bytes())
    return digest.hexdigest()
