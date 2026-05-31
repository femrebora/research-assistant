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
# Search multiple locations in order of preference.  The first one that
# has both Python AND Flask installed wins.
PYTHON=""
PYTHON_SOURCE=""

# Candidate 1: project-local .venv
if [ -f "$PROJECT_DIR/.venv/bin/python" ]; then
    CANDIDATE="$PROJECT_DIR/.venv/bin/python"
    if "$CANDIDATE" -c "import flask" 2>/dev/null; then
        PYTHON="$CANDIDATE"
        PYTHON_SOURCE="$PROJECT_DIR/.venv"
    fi
fi

# Candidate 2: shared thesis venv
if [ -z "$PYTHON" ] && [ -f "$HOME/.venvs/thesis/bin/python" ]; then
    CANDIDATE="$HOME/.venvs/thesis/bin/python"
    if "$CANDIDATE" -c "import flask" 2>/dev/null; then
        PYTHON="$CANDIDATE"
        PYTHON_SOURCE="$HOME/.venvs/thesis"
    fi
fi

# Candidate 3: any other venv in common locations
if [ -z "$PYTHON" ]; then
    for venv_base in "$HOME/.venvs" "$HOME/.virtualenvs"; do
        if [ -d "$venv_base" ]; then
            for venv in "$venv_base"/*/; do
                CANDIDATE="${venv}bin/python"
                if [ -f "$CANDIDATE" ] && "$CANDIDATE" -c "import flask, research_assistant" 2>/dev/null; then
                    PYTHON="$CANDIDATE"
                    PYTHON_SOURCE="$venv"
                    break 2
                fi
            done
        fi
    done
fi

# Candidate 4: system python3
if [ -z "$PYTHON" ] && command -v python3 &>/dev/null; then
    CANDIDATE="python3"
    if "$CANDIDATE" -c "import flask, research_assistant" 2>/dev/null; then
        PYTHON="$CANDIDATE"
        PYTHON_SOURCE="system"
    fi
fi

# Nothing found — give clear instructions
if [ -z "$PYTHON" ]; then
    echo "Error: Could not find a Python environment with Flask and research_assistant installed."
    echo ""
    echo "Tried these locations:"
    echo "  • $PROJECT_DIR/.venv/bin/python"
    echo "  • $HOME/.venvs/thesis/bin/python"
    echo "  • Any venv under ~/.venvs/ or ~/.virtualenvs/"
    echo "  • system python3"
    echo ""
    echo "To set up the environment, run:"
    echo "  bash $PROJECT_DIR/scripts/setup.sh"
    exit 1
fi

echo "Using Python: $PYTHON ($PYTHON_SOURCE)"

# ── Verify the package can be imported ─────────────────────────────────
if ! "$PYTHON" -c "from research_assistant.web.app import app" 2>/dev/null; then
    echo "Error: research_assistant package is installed but its web module failed to import."
    echo ""
    echo "Try reinstalling:"
    echo "  cd $PROJECT_DIR"
    echo "  source ${PYTHON_SOURCE}/bin/activate 2>/dev/null || true"
    echo "  pip install -e ."
    exit 1
fi

# ── Start the server in background ─────────────────────────────────────
echo "Starting Research Assistant..."
cd "$PROJECT_DIR"

nohup "$PYTHON" -c "
import os
os.environ.setdefault('RA_HOST', '$HOST')
os.environ.setdefault('RA_PORT', '$PORT')
from research_assistant.web.app import app
app.run(host='$HOST', port=int('$PORT'), debug=False)
" >> "$LOG_FILE" 2>&1 &

SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"

# ── Wait until the server actually accepts connections ─────────────────
port_open() {
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
    echo "To stop it, run: research-assistant stop"
    echo ""
    "$BROWSER" "http://${HOST}:${PORT}" 2>/dev/null || true
else
    echo "Error: Server failed to start within the expected time. Recent log:"
    echo "  ----------------------------------------------------------------"
    tail -n 20 "$LOG_FILE" 2>/dev/null | sed 's/^/  /'
    echo "  ----------------------------------------------------------------"
    echo "  Full log: $LOG_FILE"
    echo ""
    echo "Run 'research-assistant doctor' for a full diagnostic."
    kill "$SERVER_PID" 2>/dev/null || true
    rm -f "$PID_FILE"
    exit 1
fi
