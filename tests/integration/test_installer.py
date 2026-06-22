import hashlib
from pathlib import Path

import pytest
import tomlkit

from personal_polyspace_toolkit import clients, installer
from personal_polyspace_toolkit.constants import ReleaseAsset
from personal_polyspace_toolkit.discovery import HostPlatform, PolyspaceInstallation
from personal_polyspace_toolkit.errors import OwnershipConflict


def configure_fake_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    state_root = tmp_path / "state"
    binary = tmp_path / "bin" / "polyspace-server"
    skills = tmp_path / "codex-skills"
    codex_config = tmp_path / "codex" / "config.toml"
    payload = b"fake tested server"
    digest = hashlib.sha256(payload).hexdigest()

    monkeypatch.setattr(installer, "state_dir", lambda: state_root)
    monkeypatch.setattr(installer, "binary_path", lambda os_name: binary)
    monkeypatch.setattr(installer, "detect_platform", lambda: HostPlatform("linux", "x86_64"))
    monkeypatch.setattr(
        installer,
        "release_asset",
        lambda version, os_name, architecture: ReleaseAsset("fake-server", digest),
    )
    monkeypatch.setattr(installer, "release_url", lambda version, asset: "https://example.invalid")

    def fake_download(url: str, expected: str, destination: Path) -> str:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        return expected

    monkeypatch.setattr(installer, "download_verified", fake_download)
    monkeypatch.setattr(installer, "_probe_binary", lambda path: None)
    monkeypatch.setattr(installer, "_skill_destination", lambda client: skills)
    monkeypatch.setattr(clients, "codex_config_path", lambda env=None: codex_config)
    return state_root, binary


def test_setup_rerun_and_uninstall_are_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_root, binary = configure_fake_environment(tmp_path, monkeypatch)
    polyspace = PolyspaceInstallation(tmp_path / "R2026a", "R2026a", "test")

    first = installer.setup(["codex"], polyspace)
    second = installer.setup(["codex"], polyspace)

    assert first["binary"]["digest"] == second["binary"]["digest"]
    assert binary.is_file()
    assert len(second["skills"]["codex"]) == 11
    installer.uninstall(["codex"])
    assert not binary.exists()
    assert not (state_root / "state.json").read_text(encoding="utf-8").count('"codex"')


def test_skill_collision_rolls_back_binary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _, binary = configure_fake_environment(tmp_path, monkeypatch)
    binary.parent.mkdir(parents=True)
    binary.write_bytes(b"user binary")
    collision = tmp_path / "codex-skills" / "run-analysis"
    collision.mkdir(parents=True)
    (collision / "SKILL.md").write_text("user-owned", encoding="utf-8")

    with pytest.raises(OwnershipConflict, match="Skill destination"):
        installer.setup(["codex"], None)

    assert binary.read_bytes() == b"user binary"
    assert [path.name for path in (tmp_path / "codex-skills").iterdir()] == ["run-analysis"]
    assert (collision / "SKILL.md").read_text(encoding="utf-8") == "user-owned"


def test_failed_binary_probe_restores_previous_binary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, binary = configure_fake_environment(tmp_path, monkeypatch)
    binary.parent.mkdir(parents=True)
    binary.write_bytes(b"user binary")

    def failed_probe(path: Path) -> None:
        raise installer.ToolkitError("probe failed")

    monkeypatch.setattr(installer, "_probe_binary", failed_probe)

    with pytest.raises(installer.ToolkitError, match="probe failed"):
        installer.setup(["codex"], None)

    assert binary.read_bytes() == b"user binary"


def test_owned_rerun_updates_without_replace_and_restores_original_registration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configure_fake_environment(tmp_path, monkeypatch)
    config_path = tmp_path / "codex" / "config.toml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        '[mcp_servers.polyspace]\ncommand = "user-server"\nargs = ["--user"]\n',
        encoding="utf-8",
    )

    installer.setup(["codex"], None, replace_existing=True, telemetry=False)
    installer.setup(["codex"], None, replace_existing=False, telemetry=True)
    installer.uninstall(["codex"])

    document = tomlkit.parse(config_path.read_text(encoding="utf-8"))
    assert document["mcp_servers"]["polyspace"]["command"] == "user-server"
    assert document["mcp_servers"]["polyspace"]["args"] == ["--user"]
