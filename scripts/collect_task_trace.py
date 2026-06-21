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
        "| Command | RTK Used | Raw Rerun | Reason |",
        "| --- | --- | --- | --- |",
        "| TODO | no | no | TODO |",
        "",
        "## Token / Context Notes",
        "- Large command outputs compressed where possible.",
        "- Raw output used only for failure verification.",
        "- Remaining context risk: TODO",
        "",
        "## Verification",
        "TODO",
        "",
        "## Memory Extraction",
        "- Candidate generated: no",
        "- Promotion needed: TODO",
        "- Notes: TODO",
        "",
        "## Follow-Up",
        "- TODO",
        "",
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
