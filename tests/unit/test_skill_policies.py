from pathlib import Path

from personal_polyspace_toolkit.constants import MCP_TOOL_NAMES

ROOT = Path(__file__).resolve().parents[2]


def test_every_product_skill_has_valid_frontmatter() -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    assert len(skill_files) == 11
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        frontmatter = text.split("---", 2)[1]
        assert "name:" in frontmatter
        assert "description:" in frontmatter
        assert "license:" in frontmatter


def test_mcp_compatibility_names_are_present_and_no_unknown_calls_exist() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "skills").rglob("*.md"))
    for name in MCP_TOOL_NAMES:
        assert name in text


def test_active_product_surfaces_exclude_removed_clients_and_unsupported_language_terms() -> None:
    roots = [
        ROOT / "README.md",
        ROOT / "skills",
        ROOT / "docs" / "product",
        ROOT / "docs" / "setup",
        ROOT / ".codex-plugin",
        ROOT / ".claude-plugin",
    ]
    files: list[Path] = []
    for root in roots:
        files.extend([root] if root.is_file() else list(root.rglob("*")))
    text = "\n".join(path.read_text(encoding="utf-8") for path in files if path.is_file()).lower()
    for forbidden in ("github copilot", "cursor", "gemini", "sourcegraph amp", "c++"):
        assert forbidden not in text


def test_high_risk_workflows_keep_approval_and_failure_gates() -> None:
    justify = (ROOT / "skills/justify-findings/SKILL.md").read_text(encoding="utf-8")
    generated_tests = (ROOT / "skills/generate-c-pstunit-tests/SKILL.md").read_text(
        encoding="utf-8"
    )
    analysis = (ROOT / "skills/run-analysis/SKILL.md").read_text(encoding="utf-8")
    assert "Wait for explicit approval" in justify
    assert "Wait for explicit approval" in generated_tests
    assert "If the MCP server is unavailable" in analysis
    assert "compilation" in analysis.lower()
