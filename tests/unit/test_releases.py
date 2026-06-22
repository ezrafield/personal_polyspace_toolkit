import hashlib
import io
from pathlib import Path

import pytest

from personal_polyspace_toolkit.errors import ToolkitError
from personal_polyspace_toolkit.releases import download_verified, release_asset, release_url


def test_selects_official_tested_windows_asset() -> None:
    asset = release_asset("v1.1.1", "windows", "x86_64")
    assert asset.name == "polyspace-mcp-server-win64.exe"
    assert "mathworks/polyspace-agentic-toolkit" in release_url("v1.1.1", asset)


def test_rejects_unmanifested_version() -> None:
    with pytest.raises(ToolkitError, match="not in the tested release manifest"):
        release_asset("v99.0.0", "linux", "x86_64")


def test_verified_download_atomically_replaces_destination(tmp_path: Path) -> None:
    payload = b"verified binary"
    destination = tmp_path / "server"
    destination.write_bytes(b"old")

    digest = download_verified(
        "https://example.invalid/server",
        hashlib.sha256(payload).hexdigest(),
        destination,
        opener=lambda _: io.BytesIO(payload),
    )

    assert digest == hashlib.sha256(payload).hexdigest()
    assert destination.read_bytes() == payload


def test_digest_failure_preserves_existing_destination(tmp_path: Path) -> None:
    destination = tmp_path / "server"
    destination.write_bytes(b"old")

    with pytest.raises(ToolkitError, match="digest mismatch"):
        download_verified(
            "https://example.invalid/server",
            "0" * 64,
            destination,
            opener=lambda _: io.BytesIO(b"tampered"),
        )

    assert destination.read_bytes() == b"old"
