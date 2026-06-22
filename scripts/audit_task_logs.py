from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / ".agent" / "tasks"
REQUIRED_HEADINGS = [
    "## Goal",
    "## Commands Run",
    "## Token / Context Notes",
    "## Verification",
    "## Memory Extraction",
    "## Follow-Up",
]


def main() -> None:
    problems = []
    if not TASKS.exists():
        print(".agent/tasks does not exist.")
        return

    for path in sorted(TASKS.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                problems.append(f"{path.relative_to(ROOT).as_posix()} missing {heading}")

    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)

    print("Task logs include the required audit headings.")


if __name__ == "__main__":
    main()
