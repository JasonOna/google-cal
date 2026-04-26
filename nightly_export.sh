#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

OUT_DIR="$SCRIPT_DIR/outputs"
mkdir -p "$OUT_DIR"

# If outputs dir is empty, run from yesterday (1 day back)
if [ -z "$(ls -A "$OUT_DIR" 2>/dev/null)" ]; then
    DAYS_FROM_TODAY=1
else
    # Find the latest date file and calculate days since then
    LATEST_FILE=$(ls -t "$OUT_DIR"/*.txt 2>/dev/null | head -1)
    LATEST_DATE=$(basename "$LATEST_FILE" .txt)
    LATEST_EPOCH=$(date -j -f "%Y-%m-%d" "$LATEST_DATE" +%s)
    TODAY_EPOCH=$(date -j -f "%Y-%m-%d" "$(date +%Y-%m-%d)" +%s)
    DAYS_SINCE=$(( (TODAY_EPOCH - LATEST_EPOCH) / 86400 ))
    DAYS_FROM_TODAY=$((DAYS_SINCE + 1))
fi

# Run export for each day from latest file to yesterday
for ((i = DAYS_FROM_TODAY; i >= 1; i--)); do
    EXPORT_DATE=$(date -j -v-${i}d +%Y-%m-%d)
    OUT_FILE="$OUT_DIR/${EXPORT_DATE}.txt"
    if [ ! -f "$OUT_FILE" ]; then
        echo "Exporting events for $EXPORT_DATE..."
        ./run.sh calendar_export_runner.py "$i" > "$OUT_FILE" 2>&1
    fi
done
