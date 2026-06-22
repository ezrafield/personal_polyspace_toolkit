import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOTS = [
    ROOT / "README.md",
    ROOT / "skills",
    ROOT / "docs" / "product",
    ROOT / "docs" / "setup",
    ROOT / "plugins" / "personal-polyspace-toolkit",
    ROOT / ".claude-plugin",
]
FORBIDDEN = ("github copilot", "cursor", "gemini", "sourcegraph amp", "c++")
REQUIRED_TOOLS = (
    "run_polyspace_as_you_code",
    "configure_build_options_for_polyspace",
    "configure_checkers_for_polyspace",
    "get_polyspace_documentation",
    "query_justification_catalog",
)


def product_files() -> list[Path]:
    files: list[Path] = []
    for root in PRODUCT_ROOTS:
        files.extend([root] if root.is_file() else list(root.rglob("*")))
    return sorted(path for path in files if path.is_file())


def main() -> None:
    problems: list[str] = []
    files = product_files()
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    lowered = text.lower()
    for term in FORBIDDEN:
        if term in lowered:
            problems.append(f"Active product surface contains forbidden term: {term}")

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(skill_files) != 11:
        problems.append(f"Expected 11 product skills, found {len(skill_files)}")
    for skill in skill_files:
        skill_text = skill.read_text(encoding="utf-8")
        if not skill_text.startswith("---\n"):
            problems.append(f"Missing frontmatter: {skill.relative_to(ROOT)}")
        for field in ("name:", "description:", "license:"):
            if field not in skill_text.split("---", 2)[1]:
                problems.append(f"Missing {field} in {skill.relative_to(ROOT)}")

    for tool in REQUIRED_TOOLS:
        if tool not in text:
            problems.append(f"Missing MCP compatibility tool in skills: {tool}")

    try:
        json.loads((ROOT / ".polyspace-toolkit.schema.json").read_text(encoding="utf-8"))
        json.loads((ROOT / "examples/polyspace-toolkit.json").read_text(encoding="utf-8"))
        json.loads((ROOT / "examples/qwen-settings.local.example.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        problems.append(f"Invalid JSON product artifact: {error}")

    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print("Product skills, client surfaces, compatibility names, and JSON artifacts are valid.")


if __name__ == "__main__":
    main()
