#!/usr/bin/env bash
# Start Research Assistant web server in the background.
# Safe to run multiple times — will not start a duplicate.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"
PID_FILE="$DATA_DIR/research-assistant.pid"
LOG_FILE="$DATA_DIR/research-assistant.log"
PORT="${RA_PORT:-5050}"
HOST="${RA_HOST:-127.0.0.1}"
BROWSER="${RA_BROWSER:-xdg-open}"

mkdir -p "$DATA_DIR"

# ── Check if already running ───────────────────────────────────────────
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Research Assistant is already running (PID $OLD_PID)."
        echo "Opening browser at http://${HOST}:${PORT}"
        "$BROWSER" "http://${HOST}:${PORT}" 2>/dev/null || true
        exit 0
    else
        # Stale PID file — clean up
        rm -f "$PID_FILE"
    fi
fi

# ── Check if port is already in use ────────────────────────────────────
if command -v ss &>/dev/null; then
    if ss -tlnp 2>/dev/null | grep -q ":${PORT} "; then
        echo "Port ${PORT} is already in use. Research Assistant may already be running."
        echo "To force restart: research-assistant restart"
        echo "Opening browser at http://${HOST}:${PORT}"
        "$BROWSER" "http://${HOST}:${PORT}" 2>/dev/null || true
        exit 0
    fi
elif command -v lsof &>/dev/null; then
    if lsof -i ":${PORT}" -sTCP:LISTEN &>/dev/null; then
        echo "Port ${PORT} is already in use. Research Assistant may already be running."
        echo "To force restart: research-assistant restart"
        echo "Opening browser at http://${HOST}:${PORT}"
        "$BROWSER" "http://${HOST}:${PORT}" 2>/dev/null || true
        exit 0
    fi
fi

# ── Find Python environment ────────────────────────────────────────────
# Try common virtualenv locations in order of preference
PYTHON=""
if [ -f "$PROJECT_DIR/.venv/bin/python" ]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
elif [ -f "$HOME/.venvs/thesis/bin/python" ]; then
    PYTHON="$HOME/.venvs/thesis/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "Error: Python not found. Please set up a virtual environment first:"
    echo "  bash $PROJECT_DIR/scripts/setup.sh"
    exit 1
fi

# Verify Flask is available
if ! "$PYTHON" -c "import flask" 2>/dev/null; then
    echo "Error: Flask not found in Python environment ($PYTHON)."
    echo "Run: bash $PROJECT_DIR/scripts/setup.sh"
    exit 1
fi

# ── Start the server in background ─────────────────────────────────────
echo "Starting Research Assistant..."
cd "$PROJECT_DIR"

nohup "$PYTHON" -c "
import os, sys
sys.path.insert(0, '$PROJECT_DIR')
os.environ.setdefault('RA_HOST', '$HOST')
os.environ.setdefault('RA_PORT', '$PORT')
from research_assistant.web.app import app, _cli
app.run(host='$HOST', port=int('$PORT'), debug=False)
" >> "$LOG_FILE" 2>&1 &

SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"

# ── Wait until the server actually accepts connections ─────────────────
# Poll the port instead of guessing with a fixed sleep — Flask can take
# several seconds to bind, and opening the browser too early lands the
# user on a "connection refused" page.
port_open() {
    # Prefer a real TCP connect; fall back to ss/lsof if /dev/tcp is unavailable.
    if (exec 3<>"/dev/tcp/${HOST}/${PORT}") 2>/dev/null; then
        exec 3>&- 3<&- 2>/dev/null || true
        return 0
    fi
    return 1
}

READY=false
for _ in $(seq 1 30); do
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        break  # process died — stop waiting, report the failure below
    fi
    if port_open; then
        READY=true
        break
    fi
    sleep 0.5
done

if $READY; then
    echo ""
    echo "Research Assistant is running at http://${HOST}:${PORT}"
    echo "To stop it, run: ra stop"
    echo ""
    # Open browser only once the server is actually responding.
    "$BROWSER" "http://${HOST}:${PORT}" 2>/dev/null || true
else
    echo "Error: Server failed to start within the expected time. Recent log:"
    echo "  ----------------------------------------------------------------"
    tail -n 20 "$LOG_FILE" 2>/dev/null | sed 's/^/  /'
    echo "  ----------------------------------------------------------------"
    echo "  Full log: $LOG_FILE"
    kill "$SERVER_PID" 2>/dev/null || true
    rm -f "$PID_FILE"
    exit 1
fi
