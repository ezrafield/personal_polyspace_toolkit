from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "docs/agent/INDEX.md",
    "docs/agent/CODEMAP.md",
    "docs/agent/CODE_SEARCH.md",
    "docs/agent/CONTEXT_ROUTER.md",
    "docs/agent/COMMAND_OUTPUT_POLICY.md",
    "docs/agent/AGENTS_AND_SKILLS.md",
    "docs/agent/TOOLS.md",
    "docs/agent/MCPS.md",
    "docs/agent/MEMORY_POLICY.md",
    "docs/agent/MEMORY_RETRIEVAL.md",
    "docs/agent/MEMORY_PROMOTION_RULES.md",
    "docs/agent/SOURCE_UNDERSTANDING.md",
    "docs/agent/TASK_LOG_TEMPLATE.md",
    ".agent/tasks/README.md",
    ".agent/memory/README.md",
    ".agent/memory/index.json",
    ".agent/memory/semantic/project-facts.md",
    ".agent/memory/semantic/conventions.md",
    ".agent/memory/semantic/decisions.md",
    ".agent/memory/procedural/debugging-playbooks.md",
    ".agent/memory/procedural/testing-playbooks.md",
    ".agent/memory/procedural/refactor-playbooks.md",
    ".agent/memory/candidates/README.md",
    ".agent/plans/template.md",
    ".mcp/README.md",
    ".mcp/rtk.md",
    ".mcp/semble.md",
    ".mcp/serena.md",
    ".sembleignore",
    ".understand-anything/README.md",
    ".understand-anything/.understandignore",
    "scripts/extract_task_memory.py",
    "scripts/validate_memory_links.py",
    "scripts/audit_memory_staleness.py",
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
    "agent-setup",
    "code-search",
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

    print("Agent docs, memory scaffold, skills, and MCP notes look complete.")


if __name__ == "__main__":
    main()
