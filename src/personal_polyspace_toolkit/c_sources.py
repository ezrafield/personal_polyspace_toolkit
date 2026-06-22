"""Deterministic C translation-unit selection helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ToolkitError


def c_translation_units_from_database(path: Path) -> tuple[list[Path], list[Path]]:
    """Return C units and ignored non-C files from a compilation database."""

    try:
        entries: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ToolkitError(f"Cannot read compilation database {path}: {error}") from error
    if not isinstance(entries, list):
        raise ToolkitError("Compilation database must contain a JSON array")
    c_units: list[Path] = []
    ignored: list[Path] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            raise ToolkitError("Every compilation database entry must contain a file string")
        directory = Path(entry.get("directory", path.parent))
        source = Path(entry["file"])
        resolved = (directory / source).resolve() if not source.is_absolute() else source.resolve()
        (c_units if resolved.suffix.lower() == ".c" else ignored).append(resolved)
    return sorted(set(c_units)), sorted(set(ignored))


def translation_units_for_header(header: Path, units: list[Path]) -> list[Path]:
    """Find C units with a direct quoted include of the requested header."""

    matches: list[Path] = []
    header_name = header.name
    for unit in units:
        try:
            text = unit.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#include") and f'"{header_name}"' in stripped:
                matches.append(unit)
                break
    return matches
