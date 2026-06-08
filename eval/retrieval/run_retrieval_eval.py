import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUERIES = ROOT / "eval" / "retrieval" / "queries.json"
EXPECTED = ROOT / "eval" / "retrieval" / "expected_context.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_semble(query: str, content: str) -> str:
    if not shutil.which("semble"):
        raise RuntimeError("Semble is not installed or is not on PATH.")
    result = subprocess.run(
        ["semble", "search", query, ".", "--content", content],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def score_output(output: str, expected_paths: list[str]) -> tuple[int, list[str]]:
    normalized = output.replace("\\", "/")
    found = [path for path in expected_paths if path in normalized]
    return len(found), found


def main() -> None:
    queries = load_json(QUERIES)
    expected = load_json(EXPECTED)
    failures = []

    for item in queries:
        query_id = item["id"]
        output = run_semble(item["query"], item.get("content", "code"))
        expected_paths = expected.get(query_id, [])
        score, found = score_output(output, expected_paths)
        print(f"{query_id}: found {score}/{len(expected_paths)}")
        for path in found:
            print(f"  ok {path}")
        missing = sorted(set(expected_paths) - set(found))
        for path in missing:
            print(f"  missing {path}")
        if missing:
            failures.append(query_id)

    if failures:
        print("Retrieval eval failures:")
        for query_id in failures:
            print(f"- {query_id}")
        raise SystemExit(1)

    print("Retrieval eval passed.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"Retrieval eval skipped: {exc}")
        raise SystemExit(2)
