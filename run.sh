#!/bin/bash
# Create/activate virtual environment and run the script.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
PYTHON_BIN="$VENV_DIR/bin/python3"

if [ ! -d "$VENV_DIR" ]; then
	python3 -m venv "$VENV_DIR"
fi

if [ -f "requirements.txt" ]; then
	"$PYTHON_BIN" -m pip install -r requirements.txt
fi

"$PYTHON_BIN" "$@"
