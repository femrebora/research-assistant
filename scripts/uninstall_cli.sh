#!/usr/bin/env bash
# Uninstall research-assistant — remove every trace the installer created.
#
# What this removes:
#   1. ~/.local/bin/research-assistant   (the CLI wrapper)
#   2. ~/.local/share/applications/research-assistant.desktop  (desktop launcher)
#   3. ~/.local/share/research-assistant/  (PID file, server logs, runtime data)
#
# What this does NOT remove (by design):
#   - Your thesis workspace (~/thesis by default) — that's YOUR work
#   - The Python virtual environment (~/.venvs/thesis by default)
#   - The ChromaDB vector index (~/thesis/chroma_db by default)
#   - The research-assistant project directory itself
#   - Your Zotero library
#
# After running this script, you may want to manually remove the two lines
# the old installer added to ~/.bashrc (if you ever ran the old installer).
# This script prints exact instructions for that.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REMOVED=()
SKIPPED=()

section() { echo ""; echo "== $1 =="; }
removed() { REMOVED+=("$1"); echo "  ✓ Removed: $1"; }
skip()    { SKIPPED+=("$1"); echo "  − Skipped (not found): $1"; }

echo "Research Assistant — Uninstall"
echo "==============================="
echo "Project directory: $PROJECT_DIR"
echo ""

# ── 1. CLI wrapper ─────────────────────────────────────────────────────
section "CLI wrapper"
if [ -f "$HOME/.local/bin/research-assistant" ]; then
    rm "$HOME/.local/bin/research-assistant"
    removed "~/.local/bin/research-assistant"
else
    skip "~/.local/bin/research-assistant"
fi

# ── 2. Desktop launcher ────────────────────────────────────────────────
section "Desktop launcher"
DESKTOP_FILE="$HOME/.local/share/applications/research-assistant.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    removed "~/.local/share/applications/research-assistant.desktop"
else
    skip "~/.local/share/applications/research-assistant.desktop"
fi

# ── 3. Runtime data (PID, logs) ────────────────────────────────────────
section "Runtime data"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"
if [ -d "$DATA_DIR" ]; then
    rm -rf "$DATA_DIR"
    removed "$DATA_DIR"
else
    skip "$DATA_DIR"
fi

# ── Summary ─────────────────────────────────────────────────────────────
section "Summary"
if [ ${#REMOVED[@]} -gt 0 ]; then
    echo "  Removed ${#REMOVED[@]} item(s):"
    for item in "${REMOVED[@]}"; do
        echo "    • $item"
    done
else
    echo "  Nothing was removed — research-assistant was not installed,"
    echo "  or had already been cleaned up."
fi

if [ ${#SKIPPED[@]} -gt 0 ]; then
    echo "  Skipped ${#SKIPPED[@]} item(s) (already gone):"
    for item in "${SKIPPED[@]}"; do
        echo "    • $item"
    done
fi

# ── Manual cleanup instructions ─────────────────────────────────────────
echo ""
echo "─── What to check manually ────────────────────────────────────"
echo ""
echo "1. Shell config (~/.bashrc or ~/.zshrc):"
echo ""
echo "   If you ran an older version of the installer, it may have"
echo "   added these lines to your ~/.bashrc.  Open the file and"
echo "   remove them if present:"
echo ""
echo "     # Added by research-assistant installer"
echo "     export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "     alias ra=\"research-assistant\""
echo ""
echo "   To check:  grep 'research-assistant\|alias ra=' ~/.bashrc"
echo "   To edit:   nano ~/.bashrc"
echo ""
echo "2. Workspace (NOT removed — this is your research data):"
echo "     ~/thesis/              Your thesis files, drafts, logs"
echo "     ~/thesis/chroma_db/    Vector index"
echo "     ~/.venvs/thesis/       Python virtual environment"
echo "     ~/Zotero/storage/      Your Zotero PDF library"
echo ""
echo "   To remove these:  rm -rf ~/thesis ~/.venvs/thesis ~/Zotero/storage"
echo "   Only do this if you're certain you no longer need them."
echo ""
echo "3. The project directory itself:"
echo "     $PROJECT_DIR"
echo ""
echo "   To remove:  rm -rf $PROJECT_DIR"
echo ""
echo "Uninstall complete."
