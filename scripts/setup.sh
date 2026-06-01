#!/usr/bin/env bash
# One command setup for research assistant.
# Run from inside the research assistant directory.

set -e
cd "$(dirname "$0")/.."

VENV="${RA_VENV:-$HOME/.venvs/thesis}"
THESIS_ROOT_DEFAULT="$HOME/thesis"
ZOTERO_STORAGE_DEFAULT="$HOME/Zotero/storage"

# ── Preflight: Python version ─────────────────────────────────────────────
PYTHON_CMD=""
for candidate in python3.12 python3.11 python3; do
    if command -v "$candidate" &>/dev/null; then
        PYTHON_CMD="$candidate"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Python 3.11 or newer is required but was not found."
    echo ""
    echo "Install Python 3.11+ and try again:"
    echo "  Ubuntu/Debian:  sudo apt install python3.12 python3.12-venv"
    echo "  Fedora:         sudo dnf install python3.12"
    echo "  macOS:          brew install python@3.12"
    echo ""
    exit 1
fi

PY_VERSION=$("$PYTHON_CMD" -c 'import sys; print(sys.version_info[:2])' 2>/dev/null)
PY_MAJOR=$(echo "$PY_VERSION" | sed 's/[^0-9]//g' | cut -c1)
PY_MINOR=$(echo "$PY_VERSION" | sed 's/[^0-9]//g' | cut -c2-)
if [ -z "$PY_MAJOR" ] || [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "${PY_MINOR:-0}" -lt 11 ]; }; then
    echo "ERROR: Python 3.11 or newer is required."
    echo "Found: $("$PYTHON_CMD" --version 2>/dev/null || echo "unknown version")"
    echo ""
    echo "Install Python 3.11+ and try again:"
    echo "  Ubuntu/Debian:  sudo apt install python3.12 python3.12-venv"
    echo "  Fedora:         sudo dnf install python3.12"
    echo "  macOS:          brew install python@3.12"
    echo ""
    exit 1
fi
echo "✓ $("$PYTHON_CMD" --version)"

# ── Preflight: pip ────────────────────────────────────────────────────────
if ! "$PYTHON_CMD" -m pip --version &>/dev/null; then
    echo "ERROR: pip is not available for $PYTHON_CMD."
    echo ""
    echo "Install pip and try again:"
    echo "  Ubuntu/Debian:  sudo apt install python3-pip"
    echo "  Fedora:         sudo dnf install python3-pip"
    echo "  macOS:          pip is bundled with python.org / Homebrew Python"
    echo ""
    exit 1
fi
echo "✓ pip available"

echo ""
echo "Creating Python virtualenv at $VENV"
"$PYTHON_CMD" -m venv "$VENV"

echo "Activating virtualenv and installing the package in editable mode"
# shellcheck disable=SC1090
source "$VENV/bin/activate"

python -m pip install --upgrade pip
python -m pip install -e ".[dev,desktop]"

if [ ! -f .env ]; then
    echo "Creating .env from env.example"
    cp env.example .env

    echo "Updating default local paths in .env"
    python - <<PY
from pathlib import Path

env_path = Path(".env")
text = env_path.read_text()

home = str(Path.home())

# Replace the generic /home/username/ placeholder with the actual home directory
text = text.replace("/home/username/", f"{home}/")
# Also handle legacy patterns for backward compatibility
text = text.replace("THESIS_ROOT=~/thesis", f"THESIS_ROOT={home}/thesis")
text = text.replace("ZOTERO_STORAGE=~/Zotero/storage", f"ZOTERO_STORAGE={home}/Zotero/storage")

env_path.write_text(text)
PY
fi

echo "Creating default research folders"
mkdir -p "$THESIS_ROOT_DEFAULT/logs"
mkdir -p "$ZOTERO_STORAGE_DEFAULT"

echo ""
echo "Done. Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. source $VENV/bin/activate"
echo "  3. Test CLI: ra-ask 'hello' --model claude"
echo "  4. Index PDFs: ra-researcher index"
echo "  5. Web UI: ra-web"
echo "  6. Desktop app: ra-desktop"
echo ""
echo "Open the Web UI at http://127.0.0.1:5050"
