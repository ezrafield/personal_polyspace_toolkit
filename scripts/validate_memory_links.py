import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".agent" / "memory" / "index.json"
VALID_TYPES = {"semantic", "procedural"}
VALID_CONFIDENCE = {"high", "medium", "low"}
REQUIRED_ENTRY_FIELDS = {
    "id",
    "type",
    "scope",
    "path",
    "summary",
    "keywords",
    "confidence",
    "last_verified",
    "source_task",
}
REQUIRED_CARD_FIELDS = {
    "Type",
    "Scope",
    "Confidence",
    "Last verified",
    "Source task",
}
REQUIRED_HEADINGS = {"When to use", "Related files", "Staleness triggers"}


def load_index() -> dict[str, Any]:
    if not INDEX.exists():
        raise SystemExit(f"Missing memory index: {INDEX.relative_to(ROOT).as_posix()}")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def as_path(relative: str) -> Path:
    return ROOT / relative


def parse_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        match = re.match(r"^([A-Za-z ]+):\s*(.+)$", line.strip())
        if match:
            metadata[match.group(1)] = match.group(2).strip()
    return metadata


def headings(text: str) -> set[str]:
    return {
        match.group(1).strip() for match in re.finditer(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    }


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


def validate_date(value: str, label: str, problems: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        problems.append(f"{label} must be YYYY-MM-DD: {value}")


def validate_card(entry: dict[str, Any], problems: list[str]) -> None:
    card_path = as_path(entry["path"])
    if not card_path.exists():
        problems.append(f"{entry['id']}: missing card {entry['path']}")
        return

    text = card_path.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    missing_metadata = sorted(REQUIRED_CARD_FIELDS - set(metadata))
    for field in missing_metadata:
        problems.append(f"{entry['path']}: missing metadata field {field}")

    card_headings = headings(text)
    for heading in sorted(REQUIRED_HEADINGS - card_headings):
        problems.append(f"{entry['path']}: missing heading ## {heading}")
    if "Content" not in card_headings and "Procedure" not in card_headings:
        problems.append(f"{entry['path']}: missing ## Content or ## Procedure")

    if metadata.get("Type") and metadata["Type"] != entry["type"]:
        problems.append(f"{entry['path']}: Type does not match index entry")
    if metadata.get("Scope") and metadata["Scope"] != entry["scope"]:
        problems.append(f"{entry['path']}: Scope does not match index entry")
    if metadata.get("Confidence") and metadata["Confidence"] != entry["confidence"]:
        problems.append(f"{entry['path']}: Confidence does not match index entry")
    if metadata.get("Last verified"):
        validate_date(metadata["Last verified"], f"{entry['path']} Last verified", problems)
    if metadata.get("Source task") and not as_path(metadata["Source task"]).exists():
        problems.append(f"{entry['path']}: Source task does not exist: {metadata['Source task']}")

    for related in related_files(text):
        if not as_path(related).exists():
            problems.append(f"{entry['path']}: related file does not exist: {related}")


def main() -> None:
    problems: list[str] = []
    data = load_index()
    if data.get("version") != 1:
        problems.append("index version must be 1")
    memories = data.get("memories")
    if not isinstance(memories, list):
        problems.append("index memories must be a list")
        memories = []

    seen_ids: set[str] = set()
    for entry in memories:
        if not isinstance(entry, dict):
            problems.append("memory entry must be an object")
            continue
        missing = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        entry_id = entry.get("id", "<missing id>")
        for field in missing:
            problems.append(f"{entry_id}: missing index field {field}")
        if missing:
            continue

        if entry["id"] in seen_ids:
            problems.append(f"{entry['id']}: duplicate memory id")
        seen_ids.add(entry["id"])
        if entry["type"] not in VALID_TYPES:
            problems.append(f"{entry['id']}: invalid type {entry['type']}")
        if entry["confidence"] not in VALID_CONFIDENCE:
            problems.append(f"{entry['id']}: invalid confidence {entry['confidence']}")
        if not isinstance(entry["keywords"], list) or not all(
            isinstance(item, str) for item in entry["keywords"]
        ):
            problems.append(f"{entry['id']}: keywords must be a list of strings")
        validate_date(entry["last_verified"], f"{entry['id']} last_verified", problems)
        if not as_path(entry["source_task"]).exists():
            problems.append(f"{entry['id']}: source_task does not exist: {entry['source_task']}")
        validate_card(entry, problems)

    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)

    print(f"Memory index and {len(memories)} promoted memory cards look valid.")


if __name__ == "__main__":
    main()
