from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_LINES = 200
PATTERNS = [
    "AGENTS.md",
    "CLAUDE.md",
    "src/AGENTS.md",
    "src/CLAUDE.md",
    "tests/AGENTS.md",
    ".agents/skills/*/SKILL.md",
    ".claude/agents/*.md",
]


def main() -> None:
    failed = False
    for pattern in PATTERNS:
        for path in sorted(ROOT.glob(pattern)):
            if not path.is_file():
                continue
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            if line_count > MAX_LINES:
                print(f"{path.relative_to(ROOT).as_posix()}: {line_count} lines exceeds {MAX_LINES}.")
                failed = True
            else:
                print(f"{path.relative_to(ROOT).as_posix()}: {line_count} lines.")

    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
