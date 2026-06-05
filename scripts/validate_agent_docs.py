from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "docs/agent/INDEX.md",
    "docs/agent/CODEMAP.md",
    "docs/agent/AGENTS_AND_SKILLS.md",
    "docs/agent/TOOLS.md",
    "docs/agent/MCPS.md",
    "docs/agent/SOURCE_UNDERSTANDING.md",
    "docs/agent/TASK_LOG_TEMPLATE.md",
    ".mcp/README.md",
    ".understand-anything/README.md",
    ".understand-anything/.understandignore",
]

REQUIRED_SKILLS = [
    "repo-navigator",
    "safe-implementation",
    "test-debug-loop",
    "code-review",
    "docs-sync",
    "architecture-decision",
    "task-handoff",
    "source-understanding",
    "knowledge-graph-search",
    "understand-refresh",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]

    for skill in REQUIRED_SKILLS:
        path = ROOT / ".agents" / "skills" / skill / "SKILL.md"
        if not path.exists():
            missing.append(path.relative_to(ROOT).as_posix())

    if missing:
        for path in missing:
            print(f"Missing: {path}")
        raise SystemExit(1)

    print("Agent docs, skills, and MCP notes look complete.")


if __name__ == "__main__":
    main()
