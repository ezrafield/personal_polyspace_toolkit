import json
import re
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".agent" / "memory" / "index.json"
MAX_AGE_DAYS = 180


def load_index() -> dict[str, Any]:
    if not INDEX.exists():
        raise SystemExit(f"Missing memory index: {INDEX.relative_to(ROOT).as_posix()}")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def as_path(relative: str) -> Path:
    return ROOT / relative


def related_files(text: str) -> list[str]:
    match = re.search(r"^## Related files\s*$", text, flags=re.MULTILINE)
    if not match:
        return []
    start = match.end()
    next_match = re.search(r"^## .+$", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    section = text[start:end]
    paths = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip().strip("`")
        if value and not value.startswith("TODO"):
            paths.append(value)
    return paths


def main() -> None:
    today = date.today()
    warnings: list[str] = []
    data = load_index()
    memories = data.get("memories", [])
    if not isinstance(memories, list):
        raise SystemExit("index memories must be a list")

    for entry in memories:
        if not isinstance(entry, dict):
            warnings.append("memory entry is not an object")
            continue
        entry_id = entry.get("id", "<missing id>")
        last_verified = entry.get("last_verified")
        try:
            verified_date = date.fromisoformat(last_verified)
        except (TypeError, ValueError):
            warnings.append(f"{entry_id}: invalid last_verified date: {last_verified}")
            continue
        age_days = (today - verified_date).days
        if age_days > MAX_AGE_DAYS:
            warnings.append(f"{entry_id}: last verified {age_days} days ago")

        path_value = entry.get("path")
        if not isinstance(path_value, str):
            warnings.append(f"{entry_id}: missing card path")
            continue
        card_path = as_path(path_value)
        if not card_path.exists():
            warnings.append(f"{entry_id}: missing card {path_value}")
            continue
        text = card_path.read_text(encoding="utf-8")
        for related in related_files(text):
            if not as_path(related).exists():
                warnings.append(f"{entry_id}: related file no longer exists: {related}")

    if warnings:
        for warning in warnings:
            print(warning)
        raise SystemExit(1)

    print("Promoted memory cards are not stale and related files still exist.")


if __name__ == "__main__":
    main()
