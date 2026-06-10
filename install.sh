#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET_DIR=${1:-.}

normalize_path() {
  case "$1" in
    [A-Za-z]:\\* | *\\*)
      if command -v cygpath >/dev/null 2>&1; then
        cygpath -u "$1"
      else
        printf '%s\n' "$1"
      fi
      ;;
    *)
      printf '%s\n' "$1"
      ;;
  esac
}

TARGET_DIR=$(normalize_path "$TARGET_DIR")

PYTHON_BIN=${PYTHON:-}
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  else
    PYTHON_BIN=python
  fi
fi

"$PYTHON_BIN" "$SCRIPT_DIR/scripts/agentkit_installer.py" install \
  --source "$SCRIPT_DIR" \
  --target "$TARGET_DIR"
