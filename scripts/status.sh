#!/usr/bin/env bash
# Show Research Assistant status.
set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"
PID_FILE="$DATA_DIR/research-assistant.pid"
LOG_FILE="$DATA_DIR/research-assistant.log"
PORT="${RA_PORT:-5050}"
HOST="${RA_HOST:-127.0.0.1}"

running=false
pid=""

# ── Check PID file ─────────────────────────────────────────────────────
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE" 2>/dev/null || true)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        running=true
    fi
fi

# ── Check port ─────────────────────────────────────────────────────────
port_in_use=false
if command -v ss &>/dev/null; then
    ss -tlnp 2>/dev/null | grep -q ":${PORT} " && port_in_use=true
elif command -v lsof &>/dev/null; then
    lsof -i ":${PORT}" -sTCP:LISTEN &>/dev/null && port_in_use=true
fi

echo "Research Assistant Status"
echo "========================="
if $running; then
    echo "Server:   RUNNING (PID $pid)"
elif $port_in_use; then
    echo "Server:   RUNNING (port ${PORT} in use, PID file missing)"
else
    echo "Server:   STOPPED"
fi
echo "URL:      http://${HOST}:${PORT}"
echo "PID file: $PID_FILE"
echo "Log file: $LOG_FILE"

if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(wc -c < "$LOG_FILE" 2>/dev/null || echo "0")
    echo "Log size: ${LOG_SIZE} bytes"
fi

if [ -f "$PID_FILE" ]; then
    PID_AGE=$(($(date +%s) - $(stat -c %Y "$PID_FILE" 2>/dev/null || date +%s)))
    echo "Uptime:   ~${PID_AGE}s (since PID file)"
fi
