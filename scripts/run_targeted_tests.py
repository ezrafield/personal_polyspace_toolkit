import subprocess
import sys

DEFAULT_COMMAND = ["python", "-m", "pytest", "tests/unit", "-q"]


def main() -> None:
    command = sys.argv[1:] or DEFAULT_COMMAND
    print(f"Running: {' '.join(command)}")
    raise SystemExit(subprocess.run(command, check=False).returncode)


if __name__ == "__main__":
    main()
