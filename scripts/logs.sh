#!/usr/bin/env bash
# View Research Assistant logs.
set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"
LOG_FILE="$DATA_DIR/research-assistant.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "No log file found at $LOG_FILE"
    exit 0
fi

# Default to last 50 lines; accept -n flag
if [ "${1:-}" = "-n" ] && [ -n "${2:-}" ]; then
    tail -n "$2" "$LOG_FILE"
elif [ "${1:-}" = "-f" ] || [ "${1:-}" = "--follow" ]; then
    tail -f "$LOG_FILE"
else
    tail -n 50 "$LOG_FILE"
fi
