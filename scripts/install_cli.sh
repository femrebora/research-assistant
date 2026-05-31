#!/usr/bin/env bash
# Install or update the research-assistant command for the current user.
#
# What this does:
#   1. Copies scripts/research-assistant → ~/.local/bin/research-assistant
#   2. Ensures ~/.local/bin is in PATH (adds to ~/.bashrc if needed)
#   3. Adds `alias ra="research-assistant"` to ~/.bashrc if not present
#
# Safe to run multiple times — will not duplicate PATH or alias lines.
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

# ── Create the installed script with PROJECT_DIR baked in ──────────────
cat > "$TARGET" <<SCRIPT_EOF
#!/usr/bin/env bash
# research-assistant — start, stop, and manage Research Assistant.
#
# Daily usage:
#   ra                      Start or reopen Research Assistant
#   ra stop                 Stop Research Assistant
#
# Advanced:
#   research-assistant restart/status/logs/doctor/open/config
set -euo pipefail

PROJECT_DIR="$PROJECT_DIR"

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

Alias: ra
EOF
    exit 0
}

case "\${1:-}" in
    ""|start)
        exec bash "\$PROJECT_DIR/scripts/start_web.sh"
        ;;
    stop)
        exec bash "\$PROJECT_DIR/scripts/stop_web.sh"
        ;;
    restart)
        exec bash "\$PROJECT_DIR/scripts/restart_web.sh"
        ;;
    status)
        exec bash "\$PROJECT_DIR/scripts/status.sh"
        ;;
    logs)
        shift
        exec bash "\$PROJECT_DIR/scripts/logs.sh" "\$@"
        ;;
    doctor)
        shift
        exec bash "\$PROJECT_DIR/scripts/doctor.sh" "\$@"
        ;;
    open)
        BROWSER="\${RA_BROWSER:-xdg-open}"
        HOST="\${RA_HOST:-127.0.0.1}"
        PORT="\${RA_PORT:-5050}"
        exec "\$BROWSER" "http://\${HOST}:\${PORT}" 2>/dev/null || true
        ;;
    config)
        echo "Project directory: \$PROJECT_DIR"
        DATA_DIR="\${XDG_DATA_HOME:-\$HOME/.local/share}/research-assistant"
        echo "Data directory:    \$DATA_DIR"
        echo "Log file:          \$DATA_DIR/research-assistant.log"
        echo "PID file:          \$DATA_DIR/research-assistant.pid"
        echo "Web URL:           http://\${RA_HOST:-127.0.0.1}:\${RA_PORT:-5050}"
        if [ -f "\$PROJECT_DIR/.env" ]; then
            echo "Env file:          \$PROJECT_DIR/.env"
        else
            echo "Env file:          (not found)"
        fi
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        echo "Unknown command: \$1"
        echo "Try: research-assistant --help"
        exit 1
        ;;
esac
SCRIPT_EOF

chmod +x "$TARGET"

# Make all helper scripts executable
for script in start_web.sh stop_web.sh restart_web.sh status.sh logs.sh doctor.sh; do
    if [ -f "$PROJECT_DIR/scripts/$script" ]; then
        chmod +x "$PROJECT_DIR/scripts/$script"
    fi
done

echo "✓ Installed: $TARGET"

# ── Ensure ~/.local/bin is in PATH ─────────────────────────────────────
if ! echo "$PATH" | tr ':' '\n' | grep -q "$HOME/.local/bin"; then
    if [ -f "$HOME/.bashrc" ]; then
        if ! grep -q 'HOME/.local/bin.*PATH' "$HOME/.bashrc" 2>/dev/null; then
            echo "" >> "$HOME/.bashrc"
            echo "# Added by research-assistant installer" >> "$HOME/.bashrc"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            echo "✓ Added ~/.local/bin to PATH in ~/.bashrc"
        else
            echo "✓ PATH already configured in ~/.bashrc"
        fi
    elif [ -f "$HOME/.profile" ]; then
        if ! grep -q 'HOME/.local/bin.*PATH' "$HOME/.profile" 2>/dev/null; then
            echo "" >> "$HOME/.profile"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
            echo "✓ Added ~/.local/bin to PATH in ~/.profile"
        fi
    fi
else
    echo "✓ ~/.local/bin already in PATH"
fi

# ── Add bash alias ─────────────────────────────────────────────────────
if [ -f "$HOME/.bashrc" ]; then
    if grep -q 'alias ra=' "$HOME/.bashrc" 2>/dev/null; then
        echo "✓ Alias 'ra' already configured in ~/.bashrc"
    else
        echo 'alias ra="research-assistant"' >> "$HOME/.bashrc"
        echo "✓ Added 'ra' alias to ~/.bashrc"
    fi
elif [ -f "$HOME/.bash_aliases" ]; then
    if grep -q 'alias ra=' "$HOME/.bash_aliases" 2>/dev/null; then
        echo "✓ Alias 'ra' already configured in ~/.bash_aliases"
    else
        echo 'alias ra="research-assistant"' >> "$HOME/.bash_aliases"
        echo "✓ Added 'ra' alias to ~/.bash_aliases"
    fi
fi

echo ""
echo "Installation complete!"
echo ""
echo "To start using it now, run:"
echo "  source ~/.bashrc"
echo "  ra"
echo ""
echo "Or open a new terminal and type:"
echo "  ra"
echo ""
echo "Daily workflow:"
echo "  ra          Start or reopen Research Assistant"
echo "  ra stop     Stop Research Assistant"
