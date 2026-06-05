from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DISALLOWED_IMPORTS = {
    "src/models": ["src.api", "src.services"],
    "src/utils": ["src.api", "src.services", "src.models"],
    "src/services": ["src.api"],
}


def main() -> None:
    violations = []

    for folder, imports in DISALLOWED_IMPORTS.items():
        base = ROOT / folder
        if not base.exists():
            continue

        for path in base.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for import_name in imports:
                if f"import {import_name}" in text or f"from {import_name}" in text:
                    violations.append((path.relative_to(ROOT).as_posix(), import_name))

    if violations:
        for path, import_name in violations:
            print(f"Boundary violation: {path} imports {import_name}")
        raise SystemExit(1)

    print("No simple architecture boundary violations found.")


if __name__ == "__main__":
    main()
