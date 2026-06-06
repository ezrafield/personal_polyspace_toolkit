from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEMAP = ROOT / "docs" / "agent" / "CODEMAP.md"

PURPOSES = {
    "api": "HTTP routes, request validation, response shaping, and transport boundaries.",
    "core": "Configuration, application setup, and cross-cutting primitives.",
    "models": "Domain models and persistence-facing data structures.",
    "services": "Business workflows and application logic.",
    "utils": "Small shared helpers with no business ownership.",
}

TEST_HINTS = {
    "api": ["tests/integration/test_api.py"],
    "models": ["tests/unit/test_models.py"],
    "services": ["tests/unit/test_services.py"],
}


def main() -> None:
    source_dirs = [path for path in (ROOT / "src").iterdir() if path.is_dir()]
    lines = [
        "# Code Map",
        "",
        "Generated from the current `src/` directory.",
        "",
    ]

    for directory in sorted(source_dirs):
        files = sorted(path.relative_to(ROOT).as_posix() for path in directory.rglob("*.py"))
        name = directory.name
        purpose = PURPOSES.get(name, "Project module. Replace this line with project-specific ownership notes.")
        lines.extend([f"## {directory.relative_to(ROOT).as_posix()}/", f"Purpose: {purpose}", "", "Entry points:"])
        if files:
            lines.extend(f"- `{file}`" for file in files)
        else:
            lines.append("- No Python entry points found yet.")
        tests = [path for path in TEST_HINTS.get(name, []) if (ROOT / path).exists()]
        if tests:
            lines.extend(["", "Tests:"])
            lines.extend(f"- `{path}`" for path in tests)
        lines.append("")

    CODEMAP.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Updated {CODEMAP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
