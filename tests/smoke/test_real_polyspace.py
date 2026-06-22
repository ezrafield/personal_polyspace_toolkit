import os
import subprocess
from pathlib import Path

import pytest

from personal_polyspace_toolkit.discovery import discover_polyspace, release_key

pytestmark = pytest.mark.polyspace
HAS_POLYSPACE = bool(os.environ.get("POLYSPACE_ROOT"))
HAS_CHECKERS = bool(os.environ.get("POLYSPACE_SMOKE_CHECKERS_FILE"))


def analysis_binary(root: Path, release: str) -> Path:
    name = (
        "polyspace-as-you-code"
        if release_key(release) >= (2026, 0)
        else "polyspace-bug-finder-access"
    )
    if os.name == "nt":
        name += ".exe"
    return root / "polyspace" / "bin" / name


@pytest.mark.skipif(not HAS_POLYSPACE, reason="POLYSPACE_ROOT is not configured")
def test_real_polyspace_binary_responds() -> None:
    installation = discover_polyspace()
    assert installation is not None
    binary = analysis_binary(installation.root, installation.release)

    result = subprocess.run(
        (str(binary), "-help"), capture_output=True, text=True, check=False, timeout=60
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert "polyspace" in (result.stdout + result.stderr).lower()


@pytest.mark.skipif(
    not (HAS_POLYSPACE and HAS_CHECKERS),
    reason="POLYSPACE_ROOT and POLYSPACE_SMOKE_CHECKERS_FILE are required",
)
def test_real_polyspace_analyzes_standalone_c_file(tmp_path: Path) -> None:
    installation = discover_polyspace()
    assert installation is not None
    binary = analysis_binary(installation.root, installation.release)
    source = tmp_path / "known_finding.c"
    source.write_text(
        "int divide(int value, int divisor) { return value / divisor; }\n",
        encoding="utf-8",
    )
    results = tmp_path / "results"

    result = subprocess.run(
        (
            str(binary),
            "-sources",
            str(source),
            "-checkers-selection-file",
            os.environ["POLYSPACE_SMOKE_CHECKERS_FILE"],
            "-results-dir",
            str(results),
        ),
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert results.is_dir() and any(results.iterdir())
