"""Validation for the public C-only project configuration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .constants import PROJECT_SCHEMA_VERSION, SUPPORTED_PROFILES
from .errors import ToolkitError

CPP_MARKERS = ("c++", "cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx")
STRING_PATH_FIELDS = (
    "checkersFile",
    "buildOptionsFile",
    "analysisOptionsFile",
    "justificationCatalog",
)
ALLOWED_FIELDS = frozenset(
    {
        "$schema",
        "schemaVersion",
        "language",
        "profiles",
        "checkersFile",
        "buildOptionsFile",
        "analysisOptionsFile",
        "justificationCatalog",
        "baseline",
        "include",
        "exclude",
    }
)


@dataclass(frozen=True)
class ProjectConfig:
    path: Path
    data: dict[str, Any]

    def resolved_path(self, field: str) -> Path | None:
        value = self.data.get(field)
        return (self.path.parent / value).resolve() if isinstance(value, str) else None


def _require_string(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ToolkitError(f"{field} must be a non-empty string")
    return value


def _reject_cpp(value: str, field: str) -> None:
    lowered = value.lower()
    if any(marker in lowered for marker in CPP_MARKERS):
        raise ToolkitError(f"{field} contains unsupported C++ content: {value}")


def load_project_config(path: Path) -> ProjectConfig:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ToolkitError(f"Cannot read project config {path}: {error}") from error
    if not isinstance(data, dict):
        raise ToolkitError("Project config must be a JSON object")
    unknown_fields = sorted(set(data) - ALLOWED_FIELDS)
    if unknown_fields:
        raise ToolkitError(f"Unknown project config fields: {', '.join(unknown_fields)}")
    if data.get("schemaVersion") != PROJECT_SCHEMA_VERSION:
        raise ToolkitError(f"schemaVersion must be {PROJECT_SCHEMA_VERSION}")
    if data.get("language") != "c":
        raise ToolkitError('language must be exactly "c"')

    profiles = data.get("profiles")
    if (
        not isinstance(profiles, list)
        or not profiles
        or not all(isinstance(x, str) for x in profiles)
    ):
        raise ToolkitError("profiles must be a non-empty array of strings")
    if len(profiles) != len(set(profiles)):
        raise ToolkitError("profiles must not contain duplicates")
    unknown = sorted(set(profiles) - SUPPORTED_PROFILES)
    if unknown:
        raise ToolkitError(f"Unsupported checker profiles: {', '.join(unknown)}")
    _require_string(data, "checkersFile")

    for field in STRING_PATH_FIELDS:
        value = data.get(field)
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                raise ToolkitError(f"{field} must be a non-empty string when provided")
            _reject_cpp(value, field)

    for field in ("include", "exclude"):
        values = data.get(field, [])
        if not isinstance(values, list) or not all(isinstance(x, str) and x for x in values):
            raise ToolkitError(f"{field} must be an array of non-empty strings")
        for value in values:
            _reject_cpp(value, field)
    include = data.get("include", ["**/*.c"])
    if any(not pattern.lower().endswith(".c") for pattern in include):
        raise ToolkitError("include patterns must select C translation units ending in .c")

    baseline = data.get("baseline")
    if baseline is not None:
        if not isinstance(baseline, dict) or set(baseline) - {"use", "store"}:
            raise ToolkitError("baseline may contain only use and store paths")
        for field, value in baseline.items():
            if not isinstance(value, str) or not value:
                raise ToolkitError(f"baseline.{field} must be a non-empty string")
            _reject_cpp(value, f"baseline.{field}")
    return ProjectConfig(path.resolve(), data)
