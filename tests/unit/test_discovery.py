from pathlib import Path

import pytest

from personal_polyspace_toolkit.discovery import (
    detect_platform,
    discover_polyspace,
    read_polyspace_release,
    validate_supported_release,
)
from personal_polyspace_toolkit.errors import ToolkitError


@pytest.mark.parametrize(
    ("system", "machine", "expected"),
    [
        ("Windows", "AMD64", ("windows", "x86_64")),
        ("Linux", "x86_64", ("linux", "x86_64")),
        ("Darwin", "arm64", ("macos", "arm64")),
        ("Darwin", "x86_64", ("macos", "x86_64")),
    ],
)
def test_supported_platforms(system: str, machine: str, expected: tuple[str, str]) -> None:
    host = detect_platform(system, machine)
    assert (host.os_name, host.architecture) == expected


def test_rejects_unsupported_host() -> None:
    with pytest.raises(ToolkitError, match="Unsupported platform"):
        detect_platform("Linux", "arm64")


@pytest.mark.parametrize("release", ["R2024b", "R2025a", "R2026a"])
def test_supported_polyspace_releases(release: str) -> None:
    validate_supported_release(release)


def test_rejects_old_polyspace_release() -> None:
    with pytest.raises(ToolkitError, match="R2024b or later"):
        validate_supported_release("R2024a")


def test_discovers_explicit_root_and_version(tmp_path: Path) -> None:
    version = tmp_path / "polyspace" / "VersionInfo.xml"
    version.parent.mkdir()
    version.write_text("<release>R2026a</release>", encoding="utf-8")

    installation = discover_polyspace(tmp_path, env={})

    assert installation is not None
    assert installation.root == tmp_path.resolve()
    assert installation.release == "R2026a"
    assert installation.source == "argument"


def test_invalid_explicit_root_is_actionable(tmp_path: Path) -> None:
    with pytest.raises(ToolkitError, match="VersionInfo"):
        read_polyspace_release(tmp_path)
