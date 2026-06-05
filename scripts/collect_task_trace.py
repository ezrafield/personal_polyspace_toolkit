from datetime import date
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / ".agent" / "tasks"


def changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ["Git repository not initialized or git status unavailable."]
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    TASKS.mkdir(parents=True, exist_ok=True)
    path = TASKS / f"{date.today().isoformat()}-task-trace.md"
    files = changed_files()
    body = [
        "# Task: Task Trace",
        "",
        "## Goal",
        "TODO",
        "",
        "## Changed Files",
        *(f"- {line}" for line in files),
        "",
        "## Commands Run",
        "```bash",
        "# TODO",
        "```",
        "",
        "## Risks",
        "- TODO",
        "",
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
