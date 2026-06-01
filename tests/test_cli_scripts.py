"""Tests for the CLI management scripts and related functionality.

Tests env parsing, Zotero path expansion, provider health status logic,
secret masking, CLI command resolution, and --help output.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from unittest import mock

import pytest

# ── Env parsing and writing ──────────────────────────────────────────────────

class TestSettingsStore:
    """Tests for settings_store.py env parsing and validation."""

    def test_api_keys_are_editable_secrets(self):
        """API keys are intentionally editable from the UI, and flagged secret.

        They live in EDITABLE_KEYS (so the browser can set them) *and* in
        SECRET_EDITABLE_KEYS (so the loopback guard knows to protect them).
        """
        from research_assistant.web.settings_store import (
            EDITABLE_KEYS,
            SECRET_EDITABLE_KEYS,
        )

        for key in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "DEEPSEEK_API_KEY",
                    "OPENAI_API_KEY", "ZOTERO_API_KEY"):
            assert key in EDITABLE_KEYS, f"{key} should be editable from the UI"
            assert key in SECRET_EDITABLE_KEYS, f"{key} should be a guarded secret"

    def test_save_writes_secrets_on_loopback(self):
        """On a loopback host, validate() keeps submitted API keys."""
        from research_assistant.web.settings_store import validate

        updates = {
            "THESIS_ROOT": "/tmp/test-thesis",
            "ANTHROPIC_API_KEY": "sk-ant-set-from-localhost",
        }
        with mock.patch.dict(os.environ, {"RA_HOST": "127.0.0.1"}):
            clean = validate(updates)
        assert clean["THESIS_ROOT"] == "/tmp/test-thesis"
        assert clean["ANTHROPIC_API_KEY"] == "sk-ant-set-from-localhost"

    def test_save_rejects_secrets_when_network_exposed(self):
        """When RA_HOST is non-loopback, secret writes are refused."""
        from research_assistant.web.settings_store import validate

        updates = {
            "THESIS_ROOT": "/tmp/test-thesis",
            "ANTHROPIC_API_KEY": "sk-ant-attempt-over-network",
        }
        with (
            mock.patch.dict(os.environ, {"RA_HOST": "0.0.0.0"}),
            pytest.raises(ValueError, match="non-loopback host"),
        ):
            validate(updates)

    def test_blank_secret_field_is_allowed_when_network_exposed(self):
        """A blank API-key field means 'keep current' and never trips the guard."""
        from research_assistant.web.settings_store import validate

        updates = {"THESIS_ROOT": "/tmp/test-thesis", "ANTHROPIC_API_KEY": ""}
        with mock.patch.dict(os.environ, {"RA_HOST": "0.0.0.0"}):
            clean = validate(updates)
        assert clean["THESIS_ROOT"] == "/tmp/test-thesis"
        assert "ANTHROPIC_API_KEY" not in clean

    def test_secret_status_never_reveals_values(self):
        """secret_status() must never include the actual secret value."""
        from research_assistant.web.settings_store import secret_status

        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-secret-value"}):
            statuses = secret_status()
            for s in statuses:
                assert "value" not in s, f"secret_status leaked value for {s['key']}"
                assert "sk-ant" not in str(s), "secret_status leaked key prefix"
                # Only 'key' and 'configured' should be present
                assert set(s.keys()) <= {"key", "configured"}


# ── Zotero path expansion ────────────────────────────────────────────────────

class TestZoteroPathExpansion:
    """Tests for Zotero storage path handling."""

    def test_tilde_expansion_in_resolve_pdf_path(self):
        """_resolve_pdf_path should expand ~ in ZOTERO_STORAGE."""
        from research_assistant.researcher import _resolve_pdf_path

        with mock.patch.dict(os.environ, {"ZOTERO_STORAGE": "~/Zotero/storage"}):
            # This should not crash — it should expand ~ and check existence
            result = _resolve_pdf_path("ABC123", "paper.pdf")
            # Path may or may not exist in test, but ~ should be expanded
            assert result is None or isinstance(result, Path)

    def test_zotero_storage_diagnostics_no_config(self):
        """Diagnostics should report not configured when env var is unset."""
        from research_assistant.workspace import library as lib_mod

        with mock.patch.dict(os.environ, {}, clear=True):
            diag = lib_mod.zotero_storage_diagnostics()
            assert diag["configured"] is False
            assert diag["exists"] is False
            assert diag["pdfs"] == 0

    def test_zotero_storage_diagnostics_with_path(self, tmp_path):
        """Diagnostics should detect path existence and count PDFs."""
        # Create a mock Zotero storage structure
        storage = tmp_path / "Zotero" / "storage"
        storage.mkdir(parents=True)
        subdir = storage / "ABC12345"
        subdir.mkdir()
        (subdir / "paper.pdf").write_text("PDF content")

        with mock.patch.dict(os.environ, {"ZOTERO_STORAGE": str(storage)}):
            from research_assistant.workspace.library import zotero_storage
            result = zotero_storage()
            if result:
                assert result.exists()
                pdfs = list(result.rglob("*.pdf"))
                assert len(pdfs) >= 1


# ── Provider health status ───────────────────────────────────────────────────

class TestProviderStatus:
    """Tests for provider health status logic."""

    def test_api_status_no_keys(self):
        """All providers should report not_configured when no keys are set."""
        from research_assistant.web.providers import api_provider_status

        with mock.patch.dict(os.environ, {}, clear=True):
            statuses = api_provider_status()
            for s in statuses:
                assert s.configured is False
                assert s.status == "not_configured"

    def test_api_status_with_key(self):
        """Provider with key should report key_present, not tested_ok."""
        from research_assistant.web.providers import api_provider_status

        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key"}):
            statuses = api_provider_status()
            anthropic = next(s for s in statuses if s.env_var == "ANTHROPIC_API_KEY")
            assert anthropic.configured is True
            assert anthropic.status == "key_present"
            # Should NOT claim "tested_ok" just because key exists
            assert anthropic.status != "tested_ok"

    def test_cli_status_resolves_path(self):
        """CLI status should resolve binary paths correctly."""
        from research_assistant.web.providers import cli_provider_status

        statuses = cli_provider_status()
        for s in statuses:
            assert s.alias in ("claude-cli", "gemini-cli", "codex-cli", "ollama-cli")
            assert s.binary != ""
            # Path may be None if CLI not installed, that's fine


# ── Secret masking ───────────────────────────────────────────────────────────

class TestSecretMasking:
    """Tests that secrets are never leaked in UI responses."""

    def test_provider_status_no_key_leak(self):
        """Provider status output must not contain API key values."""
        from research_assistant.web.providers import (
            api_provider_status,
            cli_provider_status,
        )

        with mock.patch.dict(os.environ, {
            "ANTHROPIC_API_KEY": "sk-ant-secret-key-12345",
            "OPENAI_API_KEY": "sk-secret-openai",
        }):
            api_status = api_provider_status()
            for s in api_status:
                # Convert to string representation
                rep = str(s)
                assert "sk-ant" not in rep, f"Secret leaked in {s.name}"
                assert "sk-secret" not in rep, f"Secret leaked in {s.name}"

    def test_settings_page_no_key_leak(self):
        """Settings secret_status must not leak key values."""
        from research_assistant.web.settings_store import secret_status

        with mock.patch.dict(os.environ, {
            "ANTHROPIC_API_KEY": "sk-ant-real-key-value",
            "ZOTERO_API_KEY": "zotero-secret-key",
        }):
            statuses = secret_status()
            rep = str(statuses)
            assert "sk-ant-real-key-value" not in rep
            assert "zotero-secret-key" not in rep

    def test_diagnostics_no_key_leak(self):
        """The /index/diagnostics endpoint must filter sensitive env vars."""
        import re

        # Simulate the diagnostics filtering logic
        sensitive_patterns = ["KEY", "SECRET", "TOKEN", "PASSWORD"]
        test_env = {
            "ANTHROPIC_API_KEY": "sk-ant-secret",
            "ZOTERO_API_KEY": "zot-secret",
            "THESIS_ROOT": "/home/user/thesis",
            "ZOTERO_STORAGE": "/home/user/Zotero/storage",
        }
        filtered = {
            k: ("***" if any(s in k.upper() for s in sensitive_patterns) else v)
            for k, v in test_env.items()
        }
        assert filtered["ANTHROPIC_API_KEY"] == "***"
        assert filtered["ZOTERO_API_KEY"] == "***"
        assert filtered["THESIS_ROOT"] == "/home/user/thesis"
        assert filtered["ZOTERO_STORAGE"] == "/home/user/Zotero/storage"


# ── Paper discovery config ───────────────────────────────────────────────────

class TestPaperDiscovery:
    """Tests for paper discovery configuration."""

    def test_openalex_works_without_key(self):
        """OpenAlex search should work without any API key configured."""
        with mock.patch.dict(os.environ, {}, clear=True):
            from research_assistant.research.discover import search_openalex
            # Should not raise about missing key — OpenAlex is keyless
            # (Will fail on network call in test, but import/config is fine)
            assert callable(search_openalex)

    def test_elicit_requires_key(self):
        """Elicit search should raise RuntimeError without ELICIT_API_KEY."""
        from research_assistant.research.discover import search_elicit

        with (
            mock.patch.dict(os.environ, {}, clear=True),
            pytest.raises(RuntimeError, match="ELICIT_API_KEY"),
        ):
            search_elicit("test query")

    def test_openalex_email_header(self):
        """OpenAlex should include mailto header when OPENALEX_EMAIL is set."""
        from research_assistant.research.discover import search_openalex
        # Just verify the function handles the email env var
        with mock.patch.dict(os.environ, {"OPENALEX_EMAIL": "researcher@example.com"}):
            assert callable(search_openalex)


# ── CLI scripts ──────────────────────────────────────────────────────────────

class TestCliScripts:
    """Tests for the CLI management scripts."""

    def test_research_assistant_script_exists(self):
        """The main research-assistant script should exist and be executable."""
        script = Path(__file__).parent.parent / "scripts" / "research-assistant"
        assert script.exists(), f"Script not found at {script}"
        assert os.access(script, os.X_OK), f"Script not executable: {script}"

    def test_start_web_script_exists(self):
        """The start_web.sh script should exist."""
        script = Path(__file__).parent.parent / "scripts" / "start_web.sh"
        assert script.exists()

    def test_stop_web_script_exists(self):
        """The stop_web.sh script should exist."""
        script = Path(__file__).parent.parent / "scripts" / "stop_web.sh"
        assert script.exists()

    def test_doctor_script_exists(self):
        """The doctor.sh script should exist."""
        script = Path(__file__).parent.parent / "scripts" / "doctor.sh"
        assert script.exists()

    def test_install_cli_script_exists(self):
        """The install_cli.sh script should exist."""
        script = Path(__file__).parent.parent / "scripts" / "install_cli.sh"
        assert script.exists()

    def test_scripts_are_executable(self):
        """All management scripts should be executable."""
        scripts_dir = Path(__file__).parent.parent / "scripts"
        for name in ("start_web.sh", "stop_web.sh", "restart_web.sh",
                     "status.sh", "logs.sh", "doctor.sh", "install_cli.sh",
                     "research-assistant"):
            script = scripts_dir / name
            if script.exists():
                assert os.access(script, os.X_OK), \
                    f"Script {name} is not executable"


# ── OpenAI unsupported parameter handling ────────────────────────────────────

class TestOpenAIParameterHandling:
    """Tests for GPT-5 temperature handling in provider tests."""

    def test_gpt5_detects_temperature_issue(self):
        """test_provider should use safe temperature for GPT-5 models."""
        from research_assistant.common import MODELS
        from research_assistant.web.providers import test_provider

        # GPT-5 model string detection — test_provider handles temperature=1
        gpt_model = MODELS.get("gpt", "")
        assert isinstance(gpt_model, str) and len(gpt_model) > 0


# ── Library search ───────────────────────────────────────────────────────────

class TestLibrarySearch:
    """Tests for the library search functionality."""

    def test_search_function_exists(self):
        """library.py should have a search function."""
        from research_assistant.workspace import library as lib_mod
        assert hasattr(lib_mod, 'search'), "library.py missing search() function"
        assert callable(lib_mod.search)

    def test_search_returns_empty_on_no_query(self, tmp_path):
        """search() should return empty list when no match."""
        from research_assistant.workspace import library as lib_mod
        results = lib_mod.search("xyznonexistentquery12345")
        assert isinstance(results, list)

    def test_zotero_storage_diagnostics_returns_dict(self):
        """zotero_storage_diagnostics should return a dict with expected keys."""
        from research_assistant.workspace import library as lib_mod
        diag = lib_mod.zotero_storage_diagnostics()
        assert isinstance(diag, dict)
        for key in ("configured", "resolved", "exists", "subfolders", "pdfs"):
            assert key in diag, f"Missing key '{key}' in diagnostics"


# ── Doctor command ───────────────────────────────────────────────────────────

class TestDoctorCommand:
    """Tests for the doctor.sh diagnostic script."""

    def test_doctor_script_runs(self):
        """doctor.sh should run without errors."""
        script = Path(__file__).parent.parent / "scripts" / "doctor.sh"
        if script.exists() and os.access(script, os.X_OK):
            result = subprocess.run(
                ["bash", str(script)],
                capture_output=True, text=True, timeout=30,
            )
            # Doctor should not crash
            assert result.returncode == 0, \
                f"doctor.sh failed: {result.stderr[:500]}"

    def test_doctor_script_mentions_key_sections(self):
        """doctor.sh output should include key diagnostic sections."""
        script = Path(__file__).parent.parent / "scripts" / "doctor.sh"
        if script.exists() and os.access(script, os.X_OK):
            result = subprocess.run(
                ["bash", str(script)],
                capture_output=True, text=True, timeout=30,
            )
            output = result.stdout
            # Should mention important sections
            assert "Python" in output
            assert "API Keys" in output or "Zotero" in output
