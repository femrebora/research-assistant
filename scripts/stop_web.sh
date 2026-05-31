#!/usr/bin/env bash
# Stop the Research Assistant web server gracefully.
set -euo pipefail

DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"
PID_FILE="$DATA_DIR/research-assistant.pid"
PORT="${RA_PORT:-5050}"

stopped=false

# ── Try stopping by PID file ───────────────────────────────────────────
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE" 2>/dev/null || true)
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null || true
        # Wait up to 5 seconds for graceful shutdown
        for i in $(seq 1 10); do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 0.5
        done
        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID" 2>/dev/null || true
        fi
        stopped=true
    fi
    rm -f "$PID_FILE"
fi

# ── Fallback: find by port ─────────────────────────────────────────────
if command -v ss &>/dev/null; then
    PORT_PIDS=$(ss -tlnp 2>/dev/null | grep ":${PORT} " | sed -n 's/.*pid=\([0-9]*\).*/\1/p' || true)
elif command -v lsof &>/dev/null; then
    PORT_PIDS=$(lsof -ti ":${PORT}" -sTCP:LISTEN 2>/dev/null || true)
else
    PORT_PIDS=""
fi

if [ -n "$PORT_PIDS" ]; then
    for pid in $PORT_PIDS; do
        kill "$pid" 2>/dev/null || true
        stopped=true
    done
fi

if $stopped; then
    echo "Research Assistant stopped."
else
    echo "Research Assistant was not running."
fi
