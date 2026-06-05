from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEMAP = ROOT / "docs" / "agent" / "CODEMAP.md"


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
        lines.extend(
            [
                f"## {directory.relative_to(ROOT).as_posix()}/",
                "Purpose: TODO - describe this module.",
                "",
                "Entry points:",
            ]
        )
        if files:
            lines.extend(f"- `{file}`" for file in files)
        else:
            lines.append("- TODO")
        lines.append("")

    CODEMAP.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Updated {CODEMAP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
