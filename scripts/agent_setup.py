import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def detect_stack() -> list[str]:
    stack = []
    if exists("pyproject.toml") or exists("requirements.txt"):
        stack.append("python")
    if exists("package.json"):
        stack.append("node")
    if exists("go.mod"):
        stack.append("go")
    if exists("Cargo.toml"):
        stack.append("rust")
    return stack or ["unknown"]


def package_scripts() -> dict[str, str]:
    path = ROOT / "package.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("scripts", {})


def detect_commands() -> dict[str, str]:
    scripts = package_scripts()
    commands = {}
    for name in ["test", "lint", "typecheck", "dev"]:
        if name in scripts:
            commands[name] = f"npm run {name}"

    makefile = ROOT / "Makefile"
    if makefile.exists():
        make_text = makefile.read_text(encoding="utf-8")
        for name in ["test", "test-unit", "test-integration", "lint", "typecheck", "dev"]:
            if f"{name}:" in make_text:
                commands[name] = f"make {name}"

    if exists("pyproject.toml") and "test" not in commands:
        commands["test"] = "pytest"
    return commands


def write_commands(commands: dict[str, str]) -> None:
    lines = ["# Commands", "", "Detected project commands.", ""]
    for name, command in sorted(commands.items()):
        lines.append(f"- {name}: `{command}`")
    if not commands:
        lines.append("- TODO: add install, test, lint, typecheck, and dev commands.")
    (ROOT / "docs" / "agent" / "COMMANDS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_task_readme() -> None:
    path = ROOT / ".agent" / "tasks" / "README.md"
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Task Logs\n\n"
        "Use one markdown file per multi-step task. Include the goal, docs read, files inspected, "
        "commands run, verification, and follow-up risk.\n",
        encoding="utf-8",
    )


def ensure_agent_entrypoints(stack: list[str], commands: dict[str, str]) -> None:
    summary = ", ".join(stack)
    command_lines = "\n".join(f"- {name}: `{command}`" for name, command in sorted(commands.items()))
    if not command_lines:
        command_lines = "- TODO: confirm project commands."

    for filename in ["AGENTS.md", "CLAUDE.md"]:
        path = ROOT / filename
        if path.exists():
            continue
        path.write_text(
            f"# {filename}\n\n"
            f"Project stack: {summary}.\n\n"
            "Start by reading `docs/agent/INDEX.md`, then only the relevant module card.\n\n"
            "## Commands\n"
            f"{command_lines}\n",
            encoding="utf-8",
        )


def run_script(relative: str) -> int:
    result = subprocess.run([sys.executable, relative], cwd=ROOT, check=False)
    return result.returncode


def main() -> None:
    stack = detect_stack()
    commands = detect_commands()
    write_commands(commands)
    ensure_task_readme()
    ensure_agent_entrypoints(stack, commands)

    failures = []
    for script in [
        "scripts/generate_codemap.py",
        "scripts/update_module_cards.py",
        "scripts/validate_agent_docs.py",
    ]:
        if run_script(script) != 0:
            failures.append(script)

    print(f"Detected stack: {', '.join(stack)}")
    print(f"Detected commands: {', '.join(sorted(commands)) or 'none'}")
    if failures:
        print("Validation failures:")
        for script in failures:
            print(f"- {script}")
        raise SystemExit(1)
    print("Agent setup complete.")


if __name__ == "__main__":
    main()
