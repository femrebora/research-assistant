#!/usr/bin/env bash
# research-assistant doctor — safe system diagnostics (no secrets).
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/research-assistant"

EXPORT=false
if [ "${1:-}" = "--export" ]; then
    EXPORT=true
fi

header() { echo ""; echo "== $1 =="; }
ok()    { echo "  ✓ $1"; }
warn()  { echo "  ⚠ $1"; }
err()   { echo "  ✗ $1"; }
info()  { echo "  ℹ $1"; }

echo "Research Assistant Doctor"
echo "========================="
echo "Date: $(date)"

# ── Python ─────────────────────────────────────────────────────────────
header "Python"
PYTHON_VERSION=$(python3 --version 2>/dev/null || echo "")
if [ -n "$PYTHON_VERSION" ]; then
    ok "$PYTHON_VERSION ($(which python3))"
else
    err "Python 3 not found"
fi

# ── Virtual environment ────────────────────────────────────────────────
header "Virtual Environment"
VENV_FOUND=false
for venv_path in "$PROJECT_DIR/.venv" "$HOME/.venvs/thesis"; do
    if [ -f "$venv_path/bin/python" ]; then
        ok "Found: $venv_path"
        VENV_FOUND=true
        VENV_PYTHON="$venv_path/bin/python"
        VENV_VERSION=$("$VENV_PYTHON" --version 2>/dev/null || echo "unknown")
        info "  Version: $VENV_VERSION"
        break
    fi
done
if ! $VENV_FOUND; then
    warn "No virtual environment found at .venv or ~/.venvs/thesis"
    info "Run: bash $PROJECT_DIR/scripts/setup.sh"
fi

# ── Required packages ──────────────────────────────────────────────────
header "Required Packages"
if $VENV_FOUND; then
    for pkg in flask litellm chromadb pdfplumber pyzotero click rich httpx; do
        if "$VENV_PYTHON" -c "import ${pkg//-/_}" 2>/dev/null; then
            ok "$pkg"
        else
            err "$pkg — not installed"
        fi
    done
fi

# ── Environment file ───────────────────────────────────────────────────
header "Environment (.env)"
if [ -f "$PROJECT_DIR/.env" ]; then
    ok ".env found at $PROJECT_DIR/.env"
else
    err ".env not found at $PROJECT_DIR/.env"
    info "Copy from: cp $PROJECT_DIR/env.example $PROJECT_DIR/.env"
fi

# ── API keys (present/absent only — never show values) ─────────────────
header "API Keys"
check_key() {
    local key_name="$1"
    local value="${!key_name:-}"
    if [ -n "${value:-}" ]; then
        ok "$key_name: configured"
    else
        warn "$key_name: not configured"
    fi
}
# Source .env if available (for doctor checks only)
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a; source "$PROJECT_DIR/.env" 2>/dev/null || true; set +a
fi
for key in ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN GEMINI_API_KEY DEEPSEEK_API_KEY OPENAI_API_KEY ZOTERO_API_KEY SEMANTIC_SCHOLAR_API_KEY ELICIT_API_KEY BRAVE_API_KEY SERPAPI_API_KEY FLASK_SECRET_KEY; do
    check_key "$key"
done
# OPENALEX_EMAIL is a semi-secret (not an API key, but used for rate-limit pools)
OPENALEX_EMAIL="${OPENALEX_EMAIL:-}"
if [ -n "$OPENALEX_EMAIL" ]; then
    ok "OPENALEX_EMAIL: configured ($OPENALEX_EMAIL)"
else
    warn "OPENALEX_EMAIL: not configured"
fi

# ── Zotero storage ─────────────────────────────────────────────────────
header "Zotero Storage"
ZOTERO_STORAGE="${ZOTERO_STORAGE:-}"
if [ -n "$ZOTERO_STORAGE" ]; then
    RESOLVED=$(eval echo "$ZOTERO_STORAGE" 2>/dev/null || echo "$ZOTERO_STORAGE")
    info "Configured: $ZOTERO_STORAGE"
    info "Resolved:   $RESOLVED"
    if [ -d "$RESOLVED" ]; then
        ok "Path exists"
        SUBFOLDERS=$(find "$RESOLVED" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
        PDFS=$(find "$RESOLVED" -name "*.pdf" 2>/dev/null | wc -l)
        info "Subfolders: $SUBFOLDERS"
        info "PDFs found: $PDFS"
    else
        err "Path does not exist: $RESOLVED"
    fi
else
    warn "ZOTERO_STORAGE not configured"
    info "Set in: $PROJECT_DIR/.env or http://127.0.0.1:5050/settings"
fi

# ── Zotero API ─────────────────────────────────────────────────────────
header "Zotero API"
ZOTERO_USER_ID="${ZOTERO_USER_ID:-}"
if [ -n "$ZOTERO_USER_ID" ]; then
    ok "ZOTERO_USER_ID: $ZOTERO_USER_ID"
else
    warn "ZOTERO_USER_ID not configured"
fi

# ── Index ──────────────────────────────────────────────────────────────
header "Vector Index"
THESIS_ROOT="${THESIS_ROOT:-$HOME/thesis}"
THESIS_ROOT_EXPANDED=$(eval echo "$THESIS_ROOT" 2>/dev/null || echo "$THESIS_ROOT")
CHROMA_DIR="$THESIS_ROOT_EXPANDED/chroma_db"
if [ -d "$CHROMA_DIR" ]; then
    ok "Index exists: $CHROMA_DIR"
    if $VENV_FOUND; then
        CHUNKS=$("$VENV_PYTHON" -c "
import sys; sys.path.insert(0, '$PROJECT_DIR')
from research_assistant.researcher import _get_chroma_client, _get_collection
try:
    c = _get_collection()
    print(c.count())
except Exception as e:
    print('error: ' + str(e))
" 2>/dev/null || echo "unknown")
        info "Chunks: $CHUNKS"
    fi
else
    warn "Index not found: $CHROMA_DIR"
    info "Index from: http://127.0.0.1:5050/index-setup"
fi

# ── CLI tools ──────────────────────────────────────────────────────────
header "CLI Tools"
for tool in claude gemini codex ollama; do
    TOOL_PATH=$(which "$tool" 2>/dev/null || echo "")
    if [ -n "$TOOL_PATH" ]; then
        VERSION=$("$tool" --version 2>/dev/null | head -1 || echo "?")
        ok "$tool: $TOOL_PATH ($VERSION)"
    else
        warn "$tool: not found in PATH"
    fi
done

# ── Port ───────────────────────────────────────────────────────────────
header "Port (${RA_PORT:-5050})"
PORT="${RA_PORT:-5050}"
if command -v ss &>/dev/null; then
    if ss -tlnp 2>/dev/null | grep -q ":${PORT} "; then
        ok "Port $PORT is in use (server running)"
    else
        info "Port $PORT is available"
    fi
elif command -v lsof &>/dev/null; then
    if lsof -i ":${PORT}" -sTCP:LISTEN &>/dev/null; then
        ok "Port $PORT is in use (server running)"
    else
        info "Port $PORT is available"
    fi
else
    info "Cannot check port status (ss/lsof not found)"
fi

# ── PaperForge Port ────────────────────────────────────────────────────
header "PaperForge Port (${PF_PORT:-5055})"
PF_PORT_VAL="${PF_PORT:-5055}"
if command -v ss &>/dev/null; then
    if ss -tlnp 2>/dev/null | grep -q ":${PF_PORT_VAL} "; then
        ok "Port $PF_PORT_VAL is in use (PaperForge server running)"
    else
        info "Port $PF_PORT_VAL is available"
    fi
elif command -v lsof &>/dev/null; then
    if lsof -i ":${PF_PORT_VAL}" -sTCP:LISTEN &>/dev/null; then
        ok "Port $PF_PORT_VAL is in use (PaperForge server running)"
    else
        info "Port $PF_PORT_VAL is available"
    fi
else
    info "Cannot check PaperForge port status (ss/lsof not found)"
fi

# ── Background process ─────────────────────────────────────────────────
header "Background Process"
if [ -f "$DATA_DIR/research-assistant.pid" ]; then
    PID=$(cat "$DATA_DIR/research-assistant.pid" 2>/dev/null || echo "")
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        ok "Running (PID $PID)"
    else
        warn "Stale PID file (PID $PID not running)"
    fi
else
    info "No PID file (not started via research-assistant command)"
fi

# ── Data paths ─────────────────────────────────────────────────────────
header "Data Paths"
info "Project dir:  $PROJECT_DIR"
info "Data dir:     $DATA_DIR"
info "Log file:     $DATA_DIR/research-assistant.log"
info "PID file:     $DATA_DIR/research-assistant.pid"
info "Thesis root:  $THESIS_ROOT_EXPANDED"
info "Chroma DB:    $CHROMA_DIR"

echo ""
echo "Doctor check complete."
if [ "${1:-}" = "--export" ] || $EXPORT; then
    echo "(Export requested — no secrets included in this output.)"
fi
