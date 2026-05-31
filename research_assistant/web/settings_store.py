"""Read/write helper for the in-browser Settings page.

Two classes of configuration:

* **Secrets** (API keys, Zotero key, Flask secret) — reported only as
  configured / not-set. Never echoed to the browser, never written from it.
* **Editable** (paths, CLI commands, timeouts) — surfaced with their current
  value and written back to the ``.env`` file on save.

Writes are surgical: only allow-listed editable keys are touched, existing
lines (comments, blanks, and every secret) are preserved in place.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import find_dotenv

# Reported as configured/not-set only — never editable or echoed.
SECRET_KEYS: tuple[str, ...] = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
    "OPENAI_API_KEY",
    "ZOTERO_API_KEY",
    "SEMANTIC_SCHOLAR_API_KEY",
    "ELICIT_API_KEY",
    "BRAVE_API_KEY",
    "SERPAPI_API_KEY",
    "FLASK_SECRET_KEY",
)

# Non-secret keys that are still sensitive enough that we only report
# configured/not-set (never echo their values in the UI).
SEMI_SECRET_KEYS: tuple[str, ...] = (
    "OPENALEX_EMAIL",
    "ZOTERO_USER_ID",
    "CONTACT_EMAIL",
)


@dataclass(frozen=True)
class EditableField:
    """A config key the user may edit from the browser."""

    key: str
    label: str
    group: str
    default: str = ""
    kind: str = "text"  # "text" | "number" | "password"
    help: str = ""


# Order here is the order rendered on the page.
EDITABLE_FIELDS: tuple[EditableField, ...] = (
    # ── Paths ────────────────────────────────────────────────────────────────
    EditableField("THESIS_ROOT", "Thesis root", "Paths", str(Path.home() / "thesis"),
                  help="Where logs, sessions, drafts, exports, and the index live."),
    EditableField("ZOTERO_STORAGE", "Zotero storage", "Paths", "",
                  help="Path to your Zotero/storage folder (PDF attachments)."),
    EditableField("THESIS_DOCS", "Additional PDFs folder", "Paths", "",
                  help="Extra folder of PDFs to include in library searches. Falls back to THESIS_ROOT if empty."),
    # ── Web UI ───────────────────────────────────────────────────────────────
    EditableField("RA_HOST", "Web UI host", "Web UI", "127.0.0.1",
                  help="Host the Flask app listens on. Change to 0.0.0.0 to expose on the network."),
    EditableField("RA_PORT", "Web UI port", "Web UI", "5050", kind="number",
                  help="Port the Flask app listens on."),
    EditableField("RA_BROWSER", "Browser command", "Web UI", "xdg-open",
                  help="Command used by `ra open`. macOS: open, Windows: start."),
    EditableField("FLASK_DEBUG", "Debug mode", "Web UI", "0", kind="number",
                  help="Set to 1 for hot reload and detailed error pages. Do not use in production."),
    # ── Model API keys ───────────────────────────────────────────────────────
    EditableField("ANTHROPIC_API_KEY", "Anthropic API key", "API keys", "",
                  kind="password",
                  help="Required for claude, sonnet, haiku model aliases."),
    EditableField("OPENAI_API_KEY", "OpenAI API key", "API keys", "",
                  kind="password",
                  help="Required for gpt, gpt-mini, codex model aliases and default embeddings."),
    EditableField("GEMINI_API_KEY", "Gemini API key", "API keys", "",
                  kind="password",
                  help="Required for gemini, flash model aliases."),
    EditableField("DEEPSEEK_API_KEY", "DeepSeek API key", "API keys", "",
                  kind="password",
                  help="Required for deepseek model alias."),
    # ── Zotero ───────────────────────────────────────────────────────────────
    EditableField("ZOTERO_USER_ID", "Zotero user ID", "Zotero", "",
                  help="Numeric user ID from zotero.org/settings/keys."),
    EditableField("ZOTERO_API_KEY", "Zotero API key", "Zotero", "",
                  kind="password",
                  help="API key with read access to your Zotero library. Create at zotero.org/settings/keys."),
    # ── Paper Discovery ──────────────────────────────────────────────────────
    EditableField("OPENALEX_EMAIL", "OpenAlex email (optional)", "Paper Discovery", "",
                  help="Email for OpenAlex polite pool — improves rate limits."),
    EditableField("SEMANTIC_SCHOLAR_API_KEY", "Semantic Scholar API key (optional)", "Paper Discovery", "",
                  kind="password",
                  help="Increases rate limit for Semantic Scholar searches. Leave blank to use without key."),
    EditableField("ELICIT_API_KEY", "Elicit API key (optional)", "Paper Discovery", "",
                  kind="password",
                  help="Required for Elicit searches. Requires a paid plan."),
    EditableField("BRAVE_API_KEY", "Brave Search API key (optional)", "Paper Discovery", "",
                  kind="password",
                  help="Web search via Brave Search API. Free tier: 2,000 queries/month."),
    # ── Vector Index ─────────────────────────────────────────────────────────
    EditableField("EMBEDDING_MODEL", "Embedding model", "Vector Index", "openai/text-embedding-3-small",
                  help="LiteLLM model string for embeddings. Default uses OpenAI; use ollama/nomic-embed-text for local."),
    # ── CLI providers ────────────────────────────────────────────────────────
    EditableField("CLAUDE_CLI_CMD", "Claude CLI command", "CLI providers", "claude -p"),
    EditableField("GEMINI_CLI_CMD", "Gemini CLI command", "CLI providers", "gemini -p"),
    EditableField("CODEX_CLI_CMD", "Codex CLI command", "CLI providers", "codex exec"),
    EditableField("OLLAMA_CLI_CMD", "Ollama CLI command", "CLI providers", "ollama run llama3.3"),
    EditableField("OLLAMA_MODEL", "Ollama model (API)", "CLI providers", "ollama/llama3.3",
                  help="Model string used by the LiteLLM-managed `local` alias."),
    EditableField("CLI_TIMEOUT", "CLI timeout (seconds)", "CLI providers", "600", kind="number"),
    # ── Misc ─────────────────────────────────────────────────────────────────
    EditableField("EDITOR", "Editor", "Misc", "",
                  help="Used by interactive review loops (paraphrase/critic). Falls back to VISUAL, then nano."),
    EditableField("CONTACT_EMAIL", "Contact email", "Misc", "",
                  help="Used by external verification tools. Falls back to OPENALEX_EMAIL."),
)

EDITABLE_KEYS: frozenset[str] = frozenset(f.key for f in EDITABLE_FIELDS)


def env_path() -> Path:
    """Resolve the .env file to read/write.

    Override with ``RA_ENV_FILE``; otherwise use the nearest existing .env;
    otherwise fall back to ``.env`` in the current working directory
    (creating it if needed).
    """
    override = os.getenv("RA_ENV_FILE", "").strip()
    if override:
        return Path(override)
    found = find_dotenv(usecwd=True)
    if found:
        return Path(found)
    return Path.cwd() / ".env"


def secret_status() -> list[dict]:
    """Report which secret keys are configured, without revealing any value.

    Only covers keys that are NOT already editable — keys in EDITABLE_FIELDS
    are shown with masked password inputs instead.
    """
    result: list[dict] = []
    for key in SECRET_KEYS:
        if key in EDITABLE_KEYS:
            continue  # shown as editable password field instead
        result.append(
            {"key": key, "configured": bool(os.getenv(key, "").strip())}
        )
    for key in SEMI_SECRET_KEYS:
        if key in EDITABLE_KEYS:
            continue
        result.append(
            {"key": key, "configured": bool(os.getenv(key, "").strip())}
        )
    return result


def editable_values() -> list[dict]:
    """Current value (or default) for each editable field, grouped for display.

    Password fields never echo their real value — they show a placeholder
    when configured and an empty field otherwise.
    """
    out: list[dict] = []
    for f in EDITABLE_FIELDS:
        raw = os.getenv(f.key, "") or ""
        if f.kind == "password":
            display_value = "••••••••" if raw else ""
            placeholder = "•••••••• (already set)" if raw else f.default
        else:
            display_value = raw
            placeholder = f.default
        out.append(
            {
                "key": f.key,
                "label": f.label,
                "group": f.group,
                "kind": f.kind,
                "help": f.help,
                "value": display_value,
                "placeholder": placeholder,
            }
        )
    return out


def _format_value(value: str) -> str:
    """Quote a .env value when it contains characters that need protection."""
    if value == "" or all(c not in value for c in ' \t#"\''):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def validate(updates: dict[str, str]) -> dict[str, str]:
    """Validate + normalise editable updates. Returns the clean subset to write.

    Rejects any non-editable key (defends against secret writes), skips
    masked password placeholders, and validates numeric fields.
    Raises ValueError on bad input.
    """
    numeric_keys = {f.key for f in EDITABLE_FIELDS if f.kind == "number"}
    password_keys = {f.key for f in EDITABLE_FIELDS if f.kind == "password"}
    masked_sentinels = {"••••••••", "********", ""}

    clean: dict[str, str] = {}
    for key, raw in updates.items():
        if key not in EDITABLE_KEYS:
            continue  # silently ignore anything not allow-listed
        value = (raw or "").strip()
        # Skip masked password placeholders — user didn't change the key
        if key in password_keys and value in masked_sentinels:
            continue
        if key in numeric_keys and value and not value.isdigit():
            raise ValueError(f"{key} must be a whole number.")
        clean[key] = value
    return clean


def save(updates: dict[str, str]) -> Path:
    """Write validated editable updates back to .env, preserving all other lines.

    Updates the value of existing allow-listed keys in place; appends new keys
    at the end. Secret lines and comments are never altered. Also reflects the
    change into the current process environment so the UI shows it immediately.
    """
    clean = validate(updates)
    path = env_path()

    lines: list[str] = []
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()

    seen: set[str] = set()
    new_lines: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            existing_key = stripped.split("=", 1)[0].strip()
            if existing_key in clean:
                new_lines.append(f"{existing_key}={_format_value(clean[existing_key])}")
                seen.add(existing_key)
                continue
        new_lines.append(line)

    appended = [k for k in clean if k not in seen]
    if appended:
        if new_lines and new_lines[-1].strip():
            new_lines.append("")
        for key in appended:
            new_lines.append(f"{key}={_format_value(clean[key])}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # Reflect immediately so the page re-renders with the saved values.
    for key, value in clean.items():
        os.environ[key] = value

    return path
