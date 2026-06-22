"""Verified acquisition of tested Polyspace MCP server releases."""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import IO, cast

from .constants import GITHUB_REPOSITORY, TESTED_RELEASES, ReleaseAsset
from .errors import ToolkitError

OpenUrl = Callable[[str], IO[bytes]]


def release_asset(version: str, os_name: str, architecture: str) -> ReleaseAsset:
    release = TESTED_RELEASES.get(version)
    if release is None:
        raise ToolkitError(f"MCP server {version} is not in the tested release manifest")
    asset = release.get((os_name, architecture))
    if asset is None:
        raise ToolkitError(f"MCP server {version} has no asset for {os_name}/{architecture}")
    return asset


def release_url(version: str, asset: ReleaseAsset) -> str:
    return f"https://github.com/{GITHUB_REPOSITORY}/releases/download/{version}/{asset.name}"


def _default_open(url: str) -> IO[bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "personal-polyspace-toolkit"})
    return cast(IO[bytes], urllib.request.urlopen(request, timeout=60))


def download_verified(
    url: str,
    expected_sha256: str,
    destination: Path,
    opener: OpenUrl = _default_open,
) -> str:
    """Download, hash, and atomically replace a binary."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    temporary_path = Path(temporary)
    digest = hashlib.sha256()
    try:
        with os.fdopen(descriptor, "wb") as output, opener(url) as response:
            while block := response.read(1024 * 1024):
                digest.update(block)
                output.write(block)
            output.flush()
            os.fsync(output.fileno())
        actual = digest.hexdigest()
        if actual != expected_sha256:
            raise ToolkitError(
                f"MCP server digest mismatch: expected {expected_sha256}, received {actual}"
            )
        if os.name != "nt":
            temporary_path.chmod(0o755)
        os.replace(temporary_path, destination)
        return actual
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def backup_file(source: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, backup)
