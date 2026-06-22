"""Cross-platform discovery for Polyspace and supported coding clients."""

from __future__ import annotations

import os
import platform
import re
import shutil
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path

from .errors import ToolkitError

RELEASE_RE = re.compile(r"R(?P<year>\d{4})(?P<half>[ab])", re.IGNORECASE)


@dataclass(frozen=True)
class HostPlatform:
    os_name: str
    architecture: str


@dataclass(frozen=True)
class PolyspaceInstallation:
    root: Path
    release: str
    source: str


def detect_platform(system: str | None = None, machine: str | None = None) -> HostPlatform:
    """Return the normalized supported platform or raise a clear error."""

    system_name = (system or platform.system()).lower()
    machine_name = (machine or platform.machine()).lower()
    os_map = {"windows": "windows", "linux": "linux", "darwin": "macos"}
    arch_map = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }
    os_name = os_map.get(system_name)
    architecture = arch_map.get(machine_name)
    if os_name is None or architecture is None:
        raise ToolkitError(f"Unsupported platform: {system_name}/{machine_name}")
    if os_name in {"windows", "linux"} and architecture != "x86_64":
        raise ToolkitError(f"Unsupported platform: {os_name}/{architecture}")
    return HostPlatform(os_name, architecture)


def release_key(release: str) -> tuple[int, int]:
    match = RELEASE_RE.search(release)
    if match is None:
        raise ToolkitError(f"Cannot determine Polyspace release from {release!r}")
    return int(match.group("year")), 0 if match.group("half").lower() == "a" else 1


def validate_supported_release(release: str) -> None:
    if release_key(release) < (2024, 1):
        raise ToolkitError(f"Polyspace {release} is unsupported; R2024b or later is required")


def read_polyspace_release(root: Path) -> str:
    candidates = (root / "polyspace" / "VersionInfo.xml", root / "VersionInfo.xml")
    for candidate in candidates:
        if not candidate.is_file():
            continue
        text = candidate.read_text(encoding="utf-8", errors="replace")
        match = RELEASE_RE.search(text)
        if match:
            release = match.group(0).upper().replace("A", "a").replace("B", "b")
            validate_supported_release(release)
            return release
    raise ToolkitError(f"No supported Polyspace VersionInfo.xml found below {root}")


def _root_from_binary(binary: str) -> Path | None:
    resolved = shutil.which(binary)
    if not resolved:
        return None
    path = Path(resolved).resolve()
    return path.parents[2] if len(path.parents) >= 3 else None


def _registry_candidates(env: Mapping[str, str]) -> list[Path]:
    home = Path(env.get("HOME") or Path.home())
    candidates: list[Path] = []
    for variable in ("APPDATA", "PROGRAMDATA", "LOCALAPPDATA"):
        if env.get(variable):
            candidates.append(
                Path(env[variable]) / "MathWorks" / "MATLAB" / "polyspace_products.prf"
            )
            candidates.append(Path(env[variable]) / "MathWorks" / "polyspace_products.prf")
    candidates.extend(sorted((home / ".matlab").glob("R*/polyspace_products.prf")))
    return candidates


def _roots_from_registry(path: Path) -> list[Path]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    values = re.findall(r"(?:[A-Za-z]:[\\/][^\r\n\"']+|/(?:[^\s\"']+/)+[^\s\"']+)", text)
    roots: list[Path] = []
    for value in values:
        candidate = Path(value.strip().rstrip(";,"))
        if candidate.exists():
            roots.append(candidate)
    return roots


def discover_polyspace(
    explicit_root: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> PolyspaceInstallation | None:
    """Discover Polyspace without broad filesystem searches."""

    environment = env or os.environ
    candidates: list[tuple[Path, str]] = []
    if explicit_root is not None:
        candidates.append((explicit_root.expanduser(), "argument"))
    if environment.get("POLYSPACE_ROOT"):
        candidates.append((Path(environment["POLYSPACE_ROOT"]).expanduser(), "POLYSPACE_ROOT"))
    for binary in ("polyspace-as-you-code", "polyspace-bug-finder-access"):
        root = _root_from_binary(binary)
        if root is not None:
            candidates.append((root, "PATH"))
    for registry in _registry_candidates(environment):
        candidates.extend((root, str(registry)) for root in _roots_from_registry(registry))

    errors: list[str] = []
    seen: set[Path] = set()
    for root, source in candidates:
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        try:
            return PolyspaceInstallation(resolved, read_polyspace_release(resolved), source)
        except ToolkitError as error:
            errors.append(str(error))
            if source == "argument":
                raise
    if explicit_root is not None and errors:
        raise ToolkitError(errors[0])
    return None


def doctor_report() -> dict[str, object]:
    host = detect_platform()
    installation = discover_polyspace()
    return {
        "platform": asdict(host),
        "polyspace": (
            {
                "root": str(installation.root),
                "release": installation.release,
                "source": installation.source,
            }
            if installation
            else None
        ),
        "clients": {name: shutil.which(name) for name in ("codex", "claude", "qwen")},
    }
