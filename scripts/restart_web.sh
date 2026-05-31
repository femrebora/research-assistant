#!/usr/bin/env bash
# Restart Research Assistant web server.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Stopping Research Assistant..."
bash "$SCRIPT_DIR/stop_web.sh"

sleep 1

echo "Starting Research Assistant..."
bash "$SCRIPT_DIR/start_web.sh"
