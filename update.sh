#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET_DIR=${1:-.}

PYTHON_BIN=${PYTHON:-}
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  else
    PYTHON_BIN=python
  fi
fi

"$PYTHON_BIN" "$SCRIPT_DIR/scripts/agentkit_installer.py" update \
  --source "$SCRIPT_DIR" \
  --target "$TARGET_DIR"
