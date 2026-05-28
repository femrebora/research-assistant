#!/usr/bin/env bash
# One-command setup for research-assistant.
# Run from inside the research-assistant directory.

set -e

VENV="${RA_VENV:-$HOME/.venvs/thesis}"

echo "→ Creating Python virtualenv at $VENV"
python3 -m venv "$VENV"

echo "→ Activating and installing the package in editable mode (with dev + desktop extras)"
# shellcheck disable=SC1090
source "$VENV/bin/activate"
pip install --upgrade pip
pip install -e ".[dev,desktop]"

if [ ! -f .env ]; then
    echo "→ Creating .env from template (you must edit it with your keys)"
    cp env.example .env
fi

echo ""
echo "Done. Next steps:"
echo "  1. Edit .env with your API keys and paths"
echo "  2. source $VENV/bin/activate"
echo "  3. Test CLI:     ra-ask 'hello' --model claude"
echo "  4. Index PDFs:   ra-researcher index"
echo "  5. Web UI:       ra-web              # browser at http://127.0.0.1:5050"
echo "  6. Desktop app:  ra-desktop          # native window"
echo ""
echo "Run 'ra-<TAB><TAB>' for the full list of installed commands."
