import argparse
import fnmatch
import json
import shutil
from datetime import datetime
from pathlib import Path


MANIFEST = "agentkit-manifest.json"
BEGIN = "<!-- agentkit:begin -->"
END = "<!-- agentkit:end -->"


def load_manifest(source: Path) -> dict:
    return json.loads((source / MANIFEST).read_text(encoding="utf-8"))


def iter_manifest_paths(source: Path, entries: list[str]) -> list[Path]:
    paths: list[Path] = []
    for entry in entries:
        full = source / entry
        if entry.endswith("/") and full.exists():
            paths.extend(path for path in full.rglob("*") if path.is_file())
        elif full.exists():
            paths.append(full)
    return sorted(set(paths))


def is_excluded(relative: str, patterns: list[str]) -> bool:
    normalized = relative.replace("\\", "/")
    for pattern in patterns:
        if pattern.endswith("/") and normalized.startswith(pattern):
            return True
        if fnmatch.fnmatch(normalized, pattern):
            return True
    return False


def backup_existing(target_root: Path, relative: Path, backup_root: Path) -> None:
    target = target_root / relative
    if not target.exists():
        return

    backup = backup_root / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    if target.is_dir():
        shutil.copytree(target, backup, dirs_exist_ok=True)
    else:
        shutil.copy2(target, backup)


def copy_file(source_root: Path, target_root: Path, source_file: Path, backup_root: Path) -> str:
    relative = source_file.relative_to(source_root)
    target = target_root / relative
    backup_existing(target_root, relative, backup_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, target)
    return relative.as_posix()


def copy_if_missing(source_root: Path, target_root: Path, relative_name: str) -> str | None:
    source = source_root / relative_name
    target = target_root / relative_name
    if target.exists() or not source.exists():
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return Path(relative_name).as_posix()


def merge_file(source_root: Path, target_root: Path, relative_name: str, backup_root: Path) -> str:
    source = source_root / relative_name
    target = target_root / relative_name
    source_text = source.read_text(encoding="utf-8").strip()

    if target.exists():
        target_text = target.read_text(encoding="utf-8")
        if BEGIN in target_text and END in target_text:
            before = target_text.split(BEGIN, 1)[0].rstrip()
            after = target_text.split(END, 1)[1].lstrip()
            merged = f"{before}\n\n{BEGIN}\n{source_text}\n{END}\n"
            if after:
                merged += f"\n{after}"
        else:
            merged = f"{target_text.rstrip()}\n\n{BEGIN}\n{source_text}\n{END}\n"
        backup_existing(target_root, Path(relative_name), backup_root)
    else:
        merged = f"{BEGIN}\n{source_text}\n{END}\n"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(merged, encoding="utf-8")
    return Path(relative_name).as_posix()


def create_symlink(source_root: Path, target_root: Path, item: dict, backup_root: Path) -> str:
    link = Path(item["link"])
    target_name = Path(item["target"])
    link_path = target_root / link
    source_target = source_root / target_name
    backup_existing(target_root, link, backup_root)
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.exists() or link_path.is_symlink():
        if link_path.is_dir() and not link_path.is_symlink():
            shutil.rmtree(link_path)
        else:
            link_path.unlink()
    link_path.symlink_to(source_target, target_is_directory=source_target.is_dir())
    return link.as_posix()


def install(mode: str, source: Path, target: Path) -> None:
    manifest = load_manifest(source)
    backup_root = target / ".agentkit" / "backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
    installed: list[str] = []
    excluded = manifest.get("excluded_files", []) + manifest.get("project_local_files", [])

    for source_file in iter_manifest_paths(source, manifest.get("included_harness_files", [])):
        relative = source_file.relative_to(source).as_posix()
        if is_excluded(relative, excluded):
            continue
        installed.append(copy_file(source, target, source_file, backup_root))

    for relative_name in manifest.get("merge_files", []):
        if (source / relative_name).exists():
            installed.append(merge_file(source, target, relative_name, backup_root))

    for relative_name in manifest.get("copy_if_missing_files", []):
        copied = copy_if_missing(source, target, relative_name)
        if copied:
            installed.append(copied)

    for item in manifest.get("symlinks", []):
        installed.append(create_symlink(source, target, item, backup_root))

    version = manifest.get("version", "0.0.0")
    (target / ".agentkit-version").write_text(f"{version}\n", encoding="utf-8")
    (target / ".agentkit-installed-files").write_text(
        "\n".join(sorted(set(installed))) + "\n",
        encoding="utf-8",
    )

    print(f"Agent kit {mode} complete: {len(set(installed))} files recorded.")
    if backup_root.exists():
        print(f"Backups written to {backup_root.relative_to(target)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install or update the agent kit in a target project.")
    parser.add_argument("mode", choices=["install", "update"])
    parser.add_argument("--source", default=".", help="Agent kit source directory.")
    parser.add_argument("--target", default=".", help="Project directory to install into.")
    args = parser.parse_args()

    install(args.mode, Path(args.source).resolve(), Path(args.target).resolve())


if __name__ == "__main__":
    main()
