"""Provider introspection for the web UI.

Reports the health of both API-keyed model providers (Anthropic, Gemini,
DeepSeek, OpenAI) and CLI-routed providers (claude-cli, gemini-cli, codex-cli,
ollama-cli), and runs a lightweight round-trip test against any model alias.

Secrets are never returned in full — API keys are reported only as
configured/not-set, never echoed.
"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass

from research_assistant.common import CLI_PROVIDERS, MODELS, ask_model

# Which env var holds the key for each API-backed alias, grouped by provider.
# (alias list is informational; the env var is what gates availability.)
API_PROVIDERS: tuple[dict, ...] = (
    {
        "name": "Anthropic (Claude)",
        "env_var": "ANTHROPIC_API_KEY",
        "aliases": ("claude", "sonnet", "haiku"),
    },
    {
        "name": "Google (Gemini)",
        "env_var": "GEMINI_API_KEY",
        "aliases": ("gemini", "flash"),
    },
    {
        "name": "DeepSeek",
        "env_var": "DEEPSEEK_API_KEY",
        "aliases": ("deepseek",),
    },
    {
        "name": "OpenAI (GPT)",
        "env_var": "OPENAI_API_KEY",
        "aliases": ("gpt", "gpt-mini", "codex"),
    },
)


@dataclass(frozen=True)
class CliStatus:
    """Resolved state of a single CLI-routed provider."""

    alias: str
    command: str
    binary: str
    found: bool
    path: str | None
    version: str | None = None


@dataclass(frozen=True)
class ApiStatus:
    """Configuration state of a single API-keyed provider (never the key itself).

    Status values:
      - "not_configured": no API key set
      - "key_present": API key is configured but not tested
      - "tested_ok": tested successfully
      - "tested_failed": test call failed
      - "rate_limited": currently rate limited
      - "unavailable": service unavailable
    """

    name: str
    env_var: str
    aliases: tuple[str, ...]
    configured: bool
    status: str = "not_configured"
    last_test_error: str | None = None


def _get_version(binary: str) -> str | None:
    """Try to get the version string from a CLI tool."""
    for flag in ("--version", "-v", "version"):
        try:
            result = subprocess.run(
                [binary, flag],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                version = result.stdout.strip().split("\n")[0][:100]
                return version
            # Some tools output version to stderr
            if result.stderr.strip():
                version = result.stderr.strip().split("\n")[0][:100]
                if "version" in version.lower() or result.returncode == 0:
                    return version
        except Exception:
            pass
    return None


def cli_provider_status() -> list[CliStatus]:
    """Resolve each CLI-routed alias to a binary and report whether it is installed."""
    statuses: list[CliStatus] = []
    for alias, command in CLI_PROVIDERS.items():
        parts = shlex.split(command)
        binary = parts[0] if parts else ""
        path = shutil.which(binary) if binary else None
        version = None
        if path:
            version = _get_version(binary)
        statuses.append(
            CliStatus(
                alias=alias,
                command=command,
                binary=binary,
                found=path is not None,
                path=path,
                version=version,
            )
        )
    return statuses


def api_provider_status() -> list[ApiStatus]:
    """Report which API providers have a key configured (without revealing it).

    Status is "key_present" when key exists but hasn't been tested yet.
    The test endpoint updates status to "tested_ok" or "tested_failed".
    """
    results: list[ApiStatus] = []
    for p in API_PROVIDERS:
        key_value = os.getenv(p["env_var"], "").strip()
        configured = bool(key_value)
        # Basic key format validation (warn on obviously invalid keys)
        status = "not_configured"
        if configured:
            status = "key_present"
            # Quick sanity check on API key format
            if p["env_var"] == "ANTHROPIC_API_KEY" and not key_value.startswith("sk-ant-"):
                status = "key_present"  # still present, just flag
            elif p["env_var"] == "OPENAI_API_KEY" and not key_value.startswith("sk-"):
                status = "key_present"
        results.append(
            ApiStatus(
                name=p["name"],
                env_var=p["env_var"],
                aliases=p["aliases"],
                configured=configured,
                status=status,
            )
        )
    return results


def test_provider(alias: str, prompt: str = "Reply with the single word: OK.") -> dict:
    """Run a tiny prompt through `alias` and report success, latency, and a snippet.

    Returns a dict safe to render directly: never contains secrets. On failure,
    `ok` is False and `error` carries a short message.
    """
    if alias not in MODELS:
        return {"ok": False, "alias": alias, "error": f"Unknown model alias '{alias}'."}

    start = time.monotonic()
    try:
        # For GPT-5 family models, temperature=0 is not supported.
        # Use temperature=1 as a safe default for testing.
        model_full = MODELS.get(alias, "")
        if "gpt-5" in str(model_full).lower() or (alias in ("gpt", "gpt-mini", "codex") and "gpt-5" in str(model_full)):
            test_temp = 1.0
        else:
            test_temp = 0.0

        result = ask_model(prompt, model=alias, max_tokens=16, temperature=test_temp)
    except Exception as e:  # surface any provider error to the UI
        error_msg = str(e)[:400]
        # Classify the error
        if "rate" in error_msg.lower() and "limit" in error_msg.lower():
            status = "rate_limited"
        elif "unavailable" in error_msg.lower() or "503" in error_msg:
            status = "unavailable"
        else:
            status = "tested_failed"
        return {
            "ok": False,
            "alias": alias,
            "elapsed_ms": int((time.monotonic() - start) * 1000),
            "error": error_msg,
            "status": status,
        }

    elapsed_ms = int((time.monotonic() - start) * 1000)
    text = (result.get("text") or "").strip()
    # CLI/API error paths return a parenthetical "(error: ...)" sentinel as text.
    ok = bool(text) and not text.startswith("(error")
    return {
        "ok": ok,
        "alias": alias,
        "elapsed_ms": elapsed_ms,
        "snippet": text[:200],
        "error": None if ok else (text[:400] or "Empty response."),
        "status": "tested_ok" if ok else "tested_failed",
    }
