import subprocess


def main() -> None:
    result = subprocess.run(
        ["git", "status", "--short"],
        check=False,
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip() or "No changed files.")


if __name__ == "__main__":
    main()
