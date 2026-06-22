import json
from pathlib import Path

from personal_polyspace_toolkit.cli import main


def test_config_validate_command(tmp_path: Path, capsys: object) -> None:
    config = tmp_path / ".polyspace-toolkit.json"
    config.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "language": "c",
                "profiles": ["cert-c"],
                "checkersFile": ".polyspace/checkers.xml",
            }
        ),
        encoding="utf-8",
    )
    assert main(("config", "validate", str(config))) == 0


def test_dry_run_does_not_require_polyspace_or_mutate(capsys: object) -> None:
    assert main(("setup", "--client", "codex", "--dry-run")) == 0
    output = capsys.readouterr().out
    assert '"sha256"' in output
    assert '"installPath"' in output
    assert '"telemetryEnabled": false' in output
