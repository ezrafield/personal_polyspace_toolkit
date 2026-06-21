import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / ".agent" / "tasks"
CANDIDATES = ROOT / ".agent" / "memory" / "candidates"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "memory-candidate"


def latest_task_log() -> Path:
    logs = [path for path in TASKS.glob("*.md") if path.name != "README.md"]
    if not logs:
        raise SystemExit("No task logs found. Pass a task log path explicitly.")
    return max(logs, key=lambda path: path.stat().st_mtime)


def read_task(path_arg: str | None) -> Path:
    if not path_arg:
        return latest_task_log()
    path = Path(path_arg)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise SystemExit(f"Task log not found: {path}")
    if not path.is_file():
        raise SystemExit(f"Task log is not a file: {path}")
    return path


def heading_text(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^## .+$", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def list_items(section: str) -> list[str]:
    items = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def path_like_items(items: list[str]) -> list[str]:
    paths = []
    for item in items:
        value = item.strip().strip("`")
        if not value:
            continue
        parts = value.split(maxsplit=1)
        if len(parts) == 2 and parts[0] in {"A", "M", "D", "R", "??"}:
            value = parts[1].strip().strip("`")
        if any(separator in value for separator in ["/", "\\"]) or "." in Path(value).name:
            paths.append(value)
    return paths


def first_nonempty(section: str, fallback: str) -> str:
    for line in section.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("|") and stripped != "TODO":
            return stripped
    return fallback


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def candidate_body(task_path: Path, text: str) -> str:
    title = text.splitlines()[0].lstrip("# ").strip() if text.splitlines() else task_path.stem
    goal = first_nonempty(heading_text(text, "Goal"), "TODO: summarize the reusable lesson.")
    files = path_like_items(
        list_items(heading_text(text, "Files Inspected"))
        + list_items(heading_text(text, "Changed Files"))
    )
    files = [item for item in files if item and "TODO" not in item]
    source = relative(task_path)
    today = date.today().isoformat()

    related_files = files or [
        "TODO: add current source, test, or doc paths that verify this memory."
    ]

    return "\n".join(
        [
            f"# Memory Candidate: {title}",
            "",
            "Type: TODO: semantic or procedural",
            "Scope: TODO: project area or workflow",
            "Confidence: low",
            f"Last verified: {today}",
            f"Source task: {source}",
            "",
            "## When to use",
            "",
            "TODO: describe the future task or situation where this memory helps.",
            "",
            "## Semantic facts learned",
            "",
            f"- TODO: extract durable facts from the task. Starting point: {goal}",
            "",
            "## Procedural lessons learned",
            "",
            "- TODO: extract reusable workflow steps, checks, or pitfalls.",
            "",
            "## Related files",
            "",
            *(f"- {item}" for item in related_files),
            "",
            "## Staleness triggers",
            "",
            "- TODO: list code, docs, tools, or workflow changes that should re-check this memory.",
            "",
            "## Promotion checklist",
            "",
            "- [ ] Contains no secrets, credentials, or private data.",
            "- [ ] Is more reusable than the raw task log.",
            "- [ ] Was verified against current files before promotion.",
            "- [ ] Was moved into semantic or procedural memory.",
            "- [ ] `.agent/memory/index.json` was updated.",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a memory candidate from a task log.")
    parser.add_argument("task_log", nargs="?", help="Path to a .agent/tasks/*.md task log.")
    args = parser.parse_args()

    task_path = read_task(args.task_log)
    text = task_path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip() if text.splitlines() else task_path.stem
    output = CANDIDATES / f"{date.today().isoformat()}-{slugify(title)}.md"
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    output.write_text(candidate_body(task_path, text), encoding="utf-8")
    print(f"Wrote {relative(output)}")
    print("Review this candidate manually before promoting it to long-term memory.")


if __name__ == "__main__":
    main()
