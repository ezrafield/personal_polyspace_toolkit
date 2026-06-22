import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
TARGET = ROOT / "plugins" / "personal-polyspace-toolkit" / "skills"


def files_below(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source_files = files_below(SOURCE)
    target_files = files_below(TARGET)
    if args.check:
        if source_files != target_files:
            print("Codex plugin skills are stale; run python scripts/sync_codex_plugin.py")
            raise SystemExit(1)
        print("Codex plugin skills match the canonical catalog.")
        return
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET)
    print(f"Synchronized {len(source_files)} files into {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
