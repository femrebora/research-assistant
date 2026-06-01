"""Tests for the /settings page: render, save, and secret-write defense.

The settings page is a hybrid surface: secrets that are also in the
editable allow-list (model API keys, Zotero credentials) can be set from
the browser only when the server is on a loopback host; non-loopback hosts
reject secret writes.  Plain editable keys (paths, CLI commands, timeouts)
can always be changed and written back to .env.  This test suite uses a
temporary .env so the real user config is never touched.
"""
from __future__ import annotations

import contextlib
import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from research_assistant.web.settings_store import (
    EDITABLE_FIELDS,
    SECRET_KEYS,
    editable_values,
    env_path,
    save,
    secret_status,
    validate,
)

# ---------------------------------------------------------------------------
# Unit tests (no Flask client needed)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_secret_keys_are_well_known():
    """Every critical secret key is in the denylist."""
    assert "ANTHROPIC_API_KEY" in SECRET_KEYS
    assert "GEMINI_API_KEY" in SECRET_KEYS
    assert "OPENAI_API_KEY" in SECRET_KEYS
    assert "DEEPSEEK_API_KEY" in SECRET_KEYS
    assert "FLASK_SECRET_KEY" in SECRET_KEYS
    assert "ZOTERO_API_KEY" in SECRET_KEYS


@pytest.mark.unit
def test_editable_fields_are_well_known():
    """Every intended editable field is in the allow-list."""
    keys = {f.key for f in EDITABLE_FIELDS}
    assert "THESIS_ROOT" in keys
    assert "CLI_TIMEOUT" in keys
    # At least one CLI_CMD should be editable
    assert any(k.endswith("_CLI_CMD") for k in keys)


@pytest.mark.unit
def test_validate_drops_non_editable_secrets():
    """validate() silently removes any key not in the editable allow-list.

    SERPAPI_API_KEY is a known secret that is NOT user-editable from the
    browser, so it must always be stripped by validate().
    """
    assert "SERPAPI_API_KEY" not in {f.key for f in EDITABLE_FIELDS}
    payload = {"THESIS_ROOT": "/tmp/test", "SERPAPI_API_KEY": "sk-injected"}
    cleaned = validate(payload)
    assert "THESIS_ROOT" in cleaned
    assert "SERPAPI_API_KEY" not in cleaned


@pytest.mark.unit
def test_validate_rejects_non_numeric_timeout():
    """CLI_TIMEOUT must be a whole number."""
    with pytest.raises(ValueError, match="whole number"):
        validate({"CLI_TIMEOUT": "not-a-number"})


# ---------------------------------------------------------------------------
# Integration tests (temp .env round-trip)
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_dotenv():
    """Create a temporary .env file, patch env_path() to return it, clean up."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("ANTHROPIC_API_KEY=sk-test-secret-123\n")
        f.write("# a comment line\n")
        f.write("THESIS_ROOT=/tmp/thesis\n")
        f.write("\n")
        f.write("GEMINI_API_KEY=gk-other-secret\n")
        tmp_path = f.name

    with mock.patch(
        "research_assistant.web.settings_store.env_path", return_value=Path(tmp_path)
    ), mock.patch(
        "research_assistant.web.app.settings_store.env_path", return_value=Path(tmp_path)
    ):
        yield tmp_path

    # Cleanup
    with contextlib.suppress(OSError):
        os.unlink(tmp_path)


@pytest.mark.integration
def test_settings_page_renders(client):
    """GET /settings returns 200 with secret status and editable form."""
    response = client.get("/settings")
    assert response.status_code == 200
    body = response.get_data(as_text=True)

    assert "Settings" in body or "settings" in body.lower()

    # Form should be present for editing
    assert "<form" in body.lower() or 'method="post"' in body.lower()


@pytest.mark.integration
def test_settings_post_saves_editable_and_secret_on_loopback(temp_dotenv):
    """On localhost, POST /settings saves editable paths AND API keys.

    Editing API keys in-browser is an intentional feature; it is only allowed
    when the server is bound to a loopback host (the default).
    """
    client = _make_client()

    with mock.patch.dict(os.environ, {"RA_HOST": "127.0.0.1"}):
        response = client.post(
            "/settings",
            data={
                "THESIS_ROOT": "/tmp/new-thesis-path",
                "ANTHROPIC_API_KEY": "sk-ant-set-from-localhost",
            },
            follow_redirects=True,
        )
    assert response.status_code == 200

    saved = Path(temp_dotenv).read_text()

    # Editable path was updated
    assert "THESIS_ROOT=/tmp/new-thesis-path" in saved
    # The API key the user typed was written in place
    assert "ANTHROPIC_API_KEY=sk-ant-set-from-localhost" in saved
    assert "ANTHROPIC_API_KEY=sk-test-secret-123" not in saved
    # An untouched secret is preserved verbatim
    assert "GEMINI_API_KEY=gk-other-secret" in saved


@pytest.mark.integration
def test_settings_post_blank_secret_preserves_existing(temp_dotenv):
    """A blank API-key field means 'keep current' — the existing value stays."""
    client = _make_client()

    with mock.patch.dict(os.environ, {"RA_HOST": "127.0.0.1"}):
        response = client.post(
            "/settings",
            data={"THESIS_ROOT": "/tmp/new-thesis-path", "ANTHROPIC_API_KEY": ""},
            follow_redirects=True,
        )
    assert response.status_code == 200

    saved = Path(temp_dotenv).read_text()
    assert "THESIS_ROOT=/tmp/new-thesis-path" in saved
    # Untouched secret preserved verbatim
    assert "ANTHROPIC_API_KEY=sk-test-secret-123" in saved


@pytest.mark.integration
def test_settings_post_rejects_secret_when_network_exposed(temp_dotenv):
    """When RA_HOST is non-loopback, a secret write is refused and shown as error."""
    client = _make_client()

    with mock.patch.dict(os.environ, {"RA_HOST": "0.0.0.0"}):
        response = client.post(
            "/settings",
            data={
                "THESIS_ROOT": "/tmp/new-thesis-path",
                "ANTHROPIC_API_KEY": "sk-ant-attempt-over-network",
            },
            follow_redirects=True,
        )
    assert response.status_code == 200

    saved = Path(temp_dotenv).read_text()
    # Nothing was written — validate() raised before the file was touched
    assert "sk-ant-attempt-over-network" not in saved
    assert "ANTHROPIC_API_KEY=sk-test-secret-123" in saved
    assert "THESIS_ROOT=/tmp/new-thesis-path" not in saved


@pytest.mark.integration
def test_settings_never_echoes_secrets(temp_dotenv):
    """GET /settings renders secret status pills, never the actual values."""
    client = _make_client()
    response = client.get("/settings")
    assert response.status_code == 200
    body = response.get_data(as_text=True)

    # The secret value itself must NOT appear in the HTML
    assert "sk-test-secret-123" not in body
    assert "gk-other-secret" not in body

    # But the secret key name may appear as a label
    assert "ANTHROPIC_API_KEY" in body or "Anthropic" in body


@pytest.mark.integration
def test_settings_nav_link_exists(client):
    """The settings link appears in base.html nav."""
    response = client.get("/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'href="/settings"' in body


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_client():
    """Return a Flask test client with TESTING mode on."""
    from research_assistant.web.app import app

    app.config["TESTING"] = True
    return app.test_client()
