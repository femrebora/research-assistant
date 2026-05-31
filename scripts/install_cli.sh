#!/usr/bin/env bash
# Install (or update) the research-assistant command for the current user.
#
# What this does:
#   1. Copies a wrapper script to ~/.local/bin/research-assistant
#   2. Makes all helper scripts executable
#   3. Prints instructions for adding ~/.local/bin to PATH (manual)
#   4. Prints instructions for adding the `ra` alias (manual)
#
# This script NEVER modifies ~/.bashrc, ~/.zshrc, or any other shell config.
# You control your shell. Paste the one-liner only if you want the shortcut.
#
# Safe to run multiple times — will update the wrapper in place.
#
# To remove everything this script installed, run:
#   bash scripts/uninstall_cli.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN_DIR="$HOME/.local/bin"
TARGET="$BIN_DIR/research-assistant"

echo "Installing research-assistant CLI..."
echo "  Project: $PROJECT_DIR"
echo "  Target:  $TARGET"
echo ""

# ── Create ~/.local/bin ────────────────────────────────────────────────
mkdir -p "$BIN_DIR"

# ── Create the wrapper with PROJECT_DIR baked in ───────────────────────
# The wrapper detects at runtime whether the project directory still
# exists, so deleting the repo won't leave a broken command that
# produces cryptic "No such file" errors.
cat > "$TARGET" <<'SCRIPT_EOF'
#!/usr/bin/env bash
# research-assistant — start, stop, and manage Research Assistant.
#
# Daily usage:
#   research-assistant          Start or reopen Research Assistant
#   research-assistant stop     Stop Research Assistant
#
# Advanced:
#   research-assistant restart/status/logs/doctor/open/config
set -euo pipefail

PROJECT_DIR="__PROJECT_DIR__"

# ── Runtime guard: project directory deleted? ──────────────────────────
if [ ! -d "$PROJECT_DIR" ]; then
    cat >&2 <<EOF
research-assistant: project directory not found.

  The Research Assistant project was installed from:
    $PROJECT_DIR
  but that directory no longer exists.

  If you deleted the project intentionally, remove this command with:
    rm ~/.local/bin/research-assistant

  If you moved the project, re-run the installer from the new location:
    cd /path/to/research-assistant
    bash scripts/install_cli.sh

  To completely uninstall:
    bash scripts/uninstall_cli.sh   (if you still have the repo)
    …or follow the manual steps at the end of the README.
EOF
    exit 1
fi

usage() {
    cat <<EOF
Usage: research-assistant [COMMAND]

Daily commands:
  (no command)          Start or reopen Research Assistant
  stop                  Stop Research Assistant

Advanced commands:
  restart               Stop and start again
  status                Show server status
  logs [-n N] [-f]      View server logs (default: last 50 lines)
  doctor [--export]     Run system diagnostics
  open                  Open browser without starting server
  config                Show configuration paths

Alias (if you set it up): ra
EOF
    exit 0
}

case "${1:-}" in
    ""|start)
        exec bash "$PROJECT_DIR/scripts/start_web.sh"
        ;;
    stop)
        exec bash "$PROJECT_DIR/scripts/stop_web.sh"
        ;;
    restart)
        exec bash "$PROJECT_DIR/scripts/restart_web.sh"
        ;;
    status)
        exec bash "$PROJECT_DIR/scripts/status.sh"
        ;;
    logs)
        shift
        exec bash "$PROJECT_DIR/scripts/logs.sh" "$@"
        ;;
    doctor)
        shift
        exec bash "$PROJECT_DIR/scripts/doctor.sh" "$@"
        ;;
    open)
        BROWSER="${RA_BROWSER:-xdg-open}"
        HOST="${RA_HOST:-127.0.0.1}"
        PORT="${RA_PORT:-5050}"
        exec "$BROWSER" "http://${HOST}:${PORT}" 2>/dev/null || true
        ;;
    config)
        echo "Project directory: $PROJECT_DIR"
        DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"
        echo "Data directory:    $DATA_DIR"
        echo "Log file:          $DATA_DIR/research-assistant.log"
        echo "PID file:          $DATA_DIR/research-assistant.pid"
        echo "Web URL:           http://${RA_HOST:-127.0.0.1}:${RA_PORT:-5050}"
        if [ -f "$PROJECT_DIR/.env" ]; then
            echo "Env file:          $PROJECT_DIR/.env"
        else
            echo "Env file:          (not found)"
        fi
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        echo "Unknown command: $1"
        echo "Try: research-assistant --help"
        exit 1
        ;;
esac
SCRIPT_EOF

# Replace the placeholder with the actual project directory
sed -i "s|__PROJECT_DIR__|$PROJECT_DIR|" "$TARGET"

chmod +x "$TARGET"

# Make all helper scripts executable
for script in start_web.sh stop_web.sh restart_web.sh status.sh logs.sh doctor.sh; do
    if [ -f "$PROJECT_DIR/scripts/$script" ]; then
        chmod +x "$PROJECT_DIR/scripts/$script"
    fi
done

echo "✓ Installed: $TARGET"

# ── Check if ~/.local/bin is in PATH ───────────────────────────────────
IN_PATH=false
if echo "$PATH" | tr ':' '\n' | grep -q "^$HOME/.local/bin$"; then
    IN_PATH=true
fi

echo ""

if $IN_PATH; then
    echo "✓ ~/.local/bin is already in your PATH."
    echo ""
    echo "You can now use the command directly:"
    echo "  research-assistant"
    echo ""
else
    echo "~/.local/bin is NOT in your PATH yet."
    echo ""
    echo "To add it, paste this line into your shell config (~/.bashrc or ~/.zshrc):"
    echo ""
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then reload with:  source ~/.bashrc"
    echo ""
    echo "Or, run the command with its full path until you set up PATH:"
    echo "  ~/.local/bin/research-assistant"
    echo ""
fi

# ── Alias suggestion (never auto-adds) ─────────────────────────────────
echo "For the 'ra' shortcut, add this alias to your shell config:"
echo ""
echo "  alias ra=\"research-assistant\""
echo ""
echo "This is optional. You control when and how to set it up."
echo ""

echo "─── Quick reference ───────────────────────────────────────────"
echo "  research-assistant          Start or reopen Research Assistant"
echo "  research-assistant stop     Stop Research Assistant"
echo "  research-assistant doctor   Run system diagnostics"
echo "  research-assistant --help   Show all commands"
echo ""
echo "To uninstall later:  bash $PROJECT_DIR/scripts/uninstall_cli.sh"
