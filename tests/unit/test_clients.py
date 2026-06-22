import json
from pathlib import Path
from subprocess import CompletedProcess

import pytest
import tomlkit

from personal_polyspace_toolkit import clients
from personal_polyspace_toolkit.clients import (
    ServerSpec,
    register_claude,
    register_codex,
    server_spec,
    unregister_codex,
    verify_qwen,
)
from personal_polyspace_toolkit.constants import PRODUCT_SKILLS
from personal_polyspace_toolkit.errors import OwnershipConflict


def test_server_spec_disables_telemetry_and_uses_root(tmp_path: Path) -> None:
    spec = server_spec(tmp_path / "server", tmp_path / "R2026a", telemetry=False)
    assert f"--polyspace-root={tmp_path / 'R2026a'}" in spec.args
    assert "--disable-telemetry=true" in spec.args


def test_codex_registration_preserves_unrelated_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "config.toml"
    path.write_text('model = "example"\n', encoding="utf-8")
    monkeypatch.setattr(clients, "codex_config_path", lambda env=None: path)
    spec = ServerSpec(str(tmp_path / "server"), ("--disable-telemetry=true",))

    record = register_codex(spec, replace_existing=False)
    document = tomlkit.parse(path.read_text(encoding="utf-8"))

    assert document["model"] == "example"
    assert document["mcp_servers"]["polyspace"]["tool_timeout_sec"] == 600
    assert document["mcp_servers"]["polyspace"]["default_tools_approval_mode"] == "prompt"
    unregister_codex(record)
    restored = tomlkit.parse(path.read_text(encoding="utf-8"))
    assert restored["model"] == "example"
    assert restored.get("mcp_servers") is None or "polyspace" not in restored["mcp_servers"]


def test_codex_refuses_unknown_existing_entry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "config.toml"
    path.write_text('[mcp_servers.polyspace]\ncommand = "other"\n', encoding="utf-8")
    monkeypatch.setattr(clients, "codex_config_path", lambda env=None: path)

    with pytest.raises(OwnershipConflict, match="replace-existing"):
        register_codex(ServerSpec("new", ()), replace_existing=False)


def test_codex_uninstall_refuses_drift(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "config.toml"
    monkeypatch.setattr(clients, "codex_config_path", lambda env=None: path)
    record = register_codex(ServerSpec("server", ()), replace_existing=False)
    path.write_text('[mcp_servers.polyspace]\ncommand = "changed"\n', encoding="utf-8")

    with pytest.raises(OwnershipConflict, match="changed after setup"):
        unregister_codex(record)


def test_claude_registration_adds_user_mcp_and_marketplace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    commands: list[tuple[str, ...]] = []

    def fake_run(command: tuple[str, ...]) -> CompletedProcess[str]:
        commands.append(command)
        if command[:4] == ("claude", "mcp", "get", "polyspace"):
            return CompletedProcess(command, 1, "", "not found")
        return CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(clients.shutil, "which", lambda name: str(tmp_path / name))
    monkeypatch.setattr(clients, "_run", fake_run)

    record = register_claude(ServerSpec(str(tmp_path / "server"), ()), False)

    assert record["marketplaceAdded"] is True
    assert any(command[:3] == ("claude", "mcp", "add-json") for command in commands)
    assert any(command[:4] == ("claude", "plugin", "marketplace", "add") for command in commands)


def test_qwen_verification_is_read_only_and_rejects_placeholders(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings_dir = tmp_path / ".qwen"
    settings_dir.mkdir()
    monkeypatch.setattr(clients.shutil, "which", lambda name: str(tmp_path / name))
    monkeypatch.setattr(clients.Path, "home", classmethod(lambda cls: tmp_path))
    settings = {
        "modelProviders": {"openai": [{"id": "local", "baseUrl": "http://localhost/v1"}]},
        "mcpServers": {"polyspace": {"command": "REPLACE_WITH_PATH"}},
    }
    (settings_dir / "settings.json").write_text(json.dumps(settings), encoding="utf-8")
    assert verify_qwen() is False

    settings["mcpServers"]["polyspace"]["command"] = str(tmp_path / "server")
    (settings_dir / "settings.json").write_text(json.dumps(settings), encoding="utf-8")
    for name in PRODUCT_SKILLS:
        skill = settings_dir / "skills" / name / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text("valid", encoding="utf-8")
    assert verify_qwen() is True
