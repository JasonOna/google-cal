#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

OUT_DIR="$SCRIPT_DIR/outputs"
mkdir -p "$OUT_DIR"

OUT_FILE="$OUT_DIR/$(date +%F).txt"

./run.sh calendar_export.py > "$OUT_FILE" 2>&1
