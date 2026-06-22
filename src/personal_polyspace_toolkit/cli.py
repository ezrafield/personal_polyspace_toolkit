"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from .constants import DEFAULT_MCP_VERSION
from .discovery import discover_polyspace, doctor_report
from .errors import ToolkitError
from .installer import setup, setup_plan, uninstall, verify
from .project_config import load_project_config


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="polyspace-toolkit")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser("doctor", help="Inspect prerequisites without changing files")
    doctor.add_argument("--json", action="store_true", dest="as_json")

    setup_parser = subcommands.add_parser("setup", help="Install and register the MCP server")
    setup_parser.add_argument(
        "--client", action="append", choices=("codex", "claude"), required=True
    )
    setup_parser.add_argument("--polyspace-root", type=Path)
    setup_parser.add_argument("--server-version", default=DEFAULT_MCP_VERSION)
    setup_parser.add_argument("--dry-run", action="store_true")
    setup_parser.add_argument("--yes", action="store_true")
    setup_parser.add_argument("--replace-existing", action="store_true")
    setup_parser.add_argument("--enable-telemetry", action="store_true")

    verify_parser = subcommands.add_parser("verify", help="Verify installed state")
    verify_parser.add_argument(
        "--client", choices=("codex", "claude", "qwen", "all"), default="all"
    )

    uninstall_parser = subcommands.add_parser("uninstall", help="Remove owned client configuration")
    uninstall_parser.add_argument(
        "--client", action="append", choices=("codex", "claude", "all"), required=True
    )

    config_parser = subcommands.add_parser("config", help="Validate project configuration")
    config_subcommands = config_parser.add_subparsers(dest="config_command", required=True)
    validate = config_subcommands.add_parser("validate")
    validate.add_argument("path", type=Path, nargs="?", default=Path(".polyspace-toolkit.json"))
    return parser


def _print(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, default=str))


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "doctor":
            report = doctor_report()
            if args.as_json:
                _print(report)
            else:
                polyspace = report["polyspace"]
                print(f"Platform: {report['platform']}")
                print(f"Polyspace: {polyspace or 'not found'}")
                print(f"Clients: {report['clients']}")
            return 0
        if args.command == "setup":
            installation = discover_polyspace(args.polyspace_root)
            selected_clients = list(dict.fromkeys(args.client))
            plan = setup_plan(
                selected_clients,
                installation,
                args.server_version,
                args.enable_telemetry,
                args.replace_existing,
            )
            _print(plan)
            if args.dry_run:
                return 0
            if not args.yes and input("Apply this setup plan? [y/N] ").strip().lower() != "y":
                print("Setup cancelled.")
                return 1
            _print(
                setup(
                    selected_clients,
                    installation,
                    args.server_version,
                    args.replace_existing,
                    args.enable_telemetry,
                )
            )
            return 0
        if args.command == "verify":
            report = verify(args.client)
            _print(report)
            return 0 if report["ready"] else 2
        if args.command == "uninstall":
            _print(uninstall(list(dict.fromkeys(args.client))))
            return 0
        if args.command == "config" and args.config_command == "validate":
            config = load_project_config(args.path)
            _print({"valid": True, "path": config.path, "profiles": config.data["profiles"]})
            return 0
    except ToolkitError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
