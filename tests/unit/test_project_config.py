import json
from pathlib import Path

import pytest

from personal_polyspace_toolkit.errors import ToolkitError
from personal_polyspace_toolkit.project_config import load_project_config


def write_config(tmp_path: Path, **changes: object) -> Path:
    data: dict[str, object] = {
        "schemaVersion": 1,
        "language": "c",
        "profiles": ["misra-c-2012", "polyspace-defects"],
        "checkersFile": ".polyspace/checkers.xml",
        "include": ["src/**/*.c"],
    }
    data.update(changes)
    path = tmp_path / ".polyspace-toolkit.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_loads_valid_config_and_resolves_paths(tmp_path: Path) -> None:
    config = load_project_config(write_config(tmp_path))
    assert config.data["profiles"] == ["misra-c-2012", "polyspace-defects"]
    assert config.resolved_path("checkersFile") == (tmp_path / ".polyspace/checkers.xml").resolve()


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"profiles": []}, "non-empty"),
        ({"profiles": ["cert-c", "cert-c"]}, "duplicates"),
        ({"profiles": ["unknown"]}, "Unsupported checker"),
        ({"language": "other"}, 'exactly "c"'),
        ({"include": ["src/**/*.hpp"]}, "unsupported"),
        ({"include": ["include/**/*.h"]}, "ending in .c"),
        ({"checkersFile": "config/rules.cpp.xml"}, "unsupported"),
        ({"unexpected": True}, "Unknown project config fields"),
    ],
)
def test_rejects_invalid_or_non_c_config(
    tmp_path: Path, changes: dict[str, object], message: str
) -> None:
    with pytest.raises(ToolkitError, match=message):
        load_project_config(write_config(tmp_path, **changes))
