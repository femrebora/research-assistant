#!/usr/bin/env bash
# Install a .desktop launcher for Research Assistant.
# Creates a menu entry that opens the Web UI at http://127.0.0.1:5050
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
APPS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
DESKTOP_FILE="$APPS_DIR/research-assistant.desktop"

# Find the CLI command
if [ -x "$HOME/.local/bin/research-assistant" ]; then
    RA_CMD="$HOME/.local/bin/research-assistant"
elif [ -x "$PROJECT_DIR/scripts/research-assistant" ]; then
    RA_CMD="$PROJECT_DIR/scripts/research-assistant"
else
    echo "Error: research-assistant command not found."
    echo "Run install_cli.sh first:"
    echo "  bash $PROJECT_DIR/scripts/install_cli.sh"
    exit 1
fi

mkdir -p "$APPS_DIR"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Research Assistant
Comment=Local thesis and literature review toolkit
Icon=applications-science
Exec=$RA_CMD
Terminal=false
Categories=Science;Education;Office;
StartupNotify=false
EOF

echo "✓ Desktop launcher installed: $DESKTOP_FILE"
echo ""
echo "Find 'Research Assistant' in your application menu, or run:"
echo "  xdg-open $DESKTOP_FILE"
echo ""
echo "Tip: The launcher will start the server and open your browser."
