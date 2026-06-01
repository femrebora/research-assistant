"""Smoke-test every GET route, key POST paths, and HTMX partials.

All external calls (LiteLLM, Zotero, ChromaDB) are mocked so this suite
runs offline and deterministically.
"""

from __future__ import annotations

from unittest import mock

import pytest

# ── GET route smoke tests ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "route",
    [
        "/",
        "/ask-library",
        "/ask",
        "/compare",
        "/index",
        "/index-setup",
        "/index/diagnostics",
        "/library-search",
        "/orchestration",
        "/outline-recommender",
        "/paper-discovery",
        "/providers",
        "/prompts",
        "/sessions",
        "/settings",
        "/stats",
        "/writing-studio",
    ],
)
@pytest.mark.integration
def test_get_route_returns_200(client, route):
    """Every public GET route returns 200 or a redirect."""
    response = client.get(route)
    # Some routes may redirect (e.g. /workspace → /projects if no active project)
    assert response.status_code in (200, 302)


@pytest.mark.parametrize(
    "route, expected_text",
    [
        ("/", "Dashboard"),
        ("/ask-library", "Ask"),
        ("/index-setup", "Index"),
        ("/library-search", "Search"),
        ("/paper-discovery", "Discovery"),
        ("/providers", "Provider"),
        ("/settings", "Settings"),
        ("/writing-studio", "Writing"),
        ("/sessions", "Session"),
    ],
)
@pytest.mark.integration
def test_get_route_contains_key_text(client, route, expected_text):
    """Key pages render with their expected heading or label."""
    response = client.get(route)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert expected_text.lower() in body.lower(), f"Expected '{expected_text}' in {route}"


# ── Index setup page ─────────────────────────────────────────────────────────


@pytest.mark.integration
def test_index_page_shows_no_index_message(client):
    """When no index exists, the index page renders a friendly message."""
    with mock.patch("research_assistant.web.app.chroma_dir") as mock_chroma:
        mock_chroma.return_value.exists.return_value = False
        response = client.get("/index-setup")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # Should mention Zotero/storage setup or "Step 1" wizard
    assert "Zotero" in body or "Choose workspace" in body or "index" in body.lower()


# ── Settings POST ────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_settings_post_editable_field(client):
    """POST /settings with valid editable fields should redirect and flash."""
    with mock.patch(
        "research_assistant.web.settings_store.env_path",
        return_value=mock.MagicMock(),
    ), mock.patch("research_assistant.web.settings_store.save") as mock_save:
        mock_save.return_value = mock.MagicMock()
        response = client.post(
            "/settings",
            data={"THESIS_ROOT": "/tmp/test-thesis"},
            follow_redirects=True,
        )
    assert response.status_code == 200


@pytest.mark.integration
def test_settings_post_bad_timeout_rejected(client):
    """POST /settings with non-numeric CLI_TIMEOUT should show error."""
    response = client.post(
        "/settings",
        data={"CLI_TIMEOUT": "not-a-number"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "whole number" in body.lower()


# ── Provider test (mocked) ───────────────────────────────────────────────────


@pytest.mark.integration
def test_provider_test_with_key(client):
    """POST /providers/test returns a result when key is configured."""
    with mock.patch(
        "research_assistant.web.providers.ask_model",
        return_value={"text": "OK", "input_tokens": 5, "output_tokens": 2, "cost": 0.0},
    ), mock.patch.dict(
        "os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test-key"}
    ):
        response = client.post("/providers/test", data={"alias": "claude"})
    assert response.status_code == 200
    # HTMX fragment — should contain the alias or a result indicator
    body = response.get_data(as_text=True)
    assert body  # non-empty fragment returned


@pytest.mark.integration
def test_provider_test_no_key(client):
    """POST /providers/test returns an error when no key is configured."""
    with mock.patch.dict("os.environ", {}, clear=True):
        response = client.post("/providers/test", data={"alias": "claude"})
    assert response.status_code in (200, 400, 500)
    body = response.get_data(as_text=True)
    # Should indicate an error or missing config
    assert body


# ── HTMX partial endpoints ───────────────────────────────────────────────────


@pytest.mark.integration
def test_htmx_panel_status(client):
    """GET /panel/status returns a valid HTML fragment."""
    response = client.get("/panel/status")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # Should contain status-related content
    assert body


@pytest.mark.integration
def test_htmx_panel_settings(client):
    """GET /panel/settings returns editable fields fragment."""
    response = client.get("/panel/settings")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # Should contain form elements for editable settings
    assert body


@pytest.mark.integration
def test_htmx_panel_providers(client):
    """GET /panel/providers returns provider status fragment."""
    response = client.get("/panel/providers")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert body


@pytest.mark.integration
def test_htmx_panel_settings_save(client):
    """POST /panel/settings/save updates a setting via HTMX."""
    with mock.patch(
        "research_assistant.web.settings_store.env_path",
        return_value=mock.MagicMock(),
    ), mock.patch("research_assistant.web.settings_store.save") as mock_save:
        mock_save.return_value = mock.MagicMock()
        response = client.post(
            "/panel/settings/save",
            data={"THESIS_ROOT": "/tmp/test"},
        )
    assert response.status_code == 200


# ── Error paths ──────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_tool_page_unknown_tool_returns_404(client):
    """GET /tools/<unknown> returns 404."""
    response = client.get("/tools/nonexistent-tool-xyz")
    assert response.status_code == 404


@pytest.mark.integration
def test_session_view_nonexistent_returns_200_or_404(client):
    """GET /sessions/<nonexistent> handles gracefully."""
    response = client.get("/sessions/__nonexistent_session_xyz__")
    # Should not crash (200 with message or 404)
    assert response.status_code in (200, 404)


@pytest.mark.integration
def test_project_view_invalid_slug_handles_gracefully(client):
    """GET /projects/<bad-slug> should not 500."""
    with mock.patch(
        "research_assistant.workspace.projects.list_projects",
        return_value=[],
    ), mock.patch(
        "research_assistant.workspace.projects.get_project",
        return_value=None,
    ):
        response = client.get("/projects/nonexistent-slug-123")
    assert response.status_code in (200, 302, 404)


@pytest.mark.integration
def test_compare_post_no_question_shows_form(client):
    """POST /compare with empty question just re-renders the form."""
    response = client.post("/compare", data={"question": "", "models": "claude"})
    assert response.status_code == 200


# ── Project CRUD (mocked) ───────────────────────────────────────────────────


@pytest.mark.integration
def test_projects_page_with_no_projects(client):
    """GET /projects shows empty state when no projects exist."""
    with mock.patch(
        "research_assistant.workspace.projects.list_projects",
        return_value=[],
    ):
        response = client.get("/projects")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "project" in body.lower()


@pytest.mark.integration
def test_projects_new_form_renders(client):
    """GET /projects/new renders the create-project form."""
    response = client.get("/projects/new")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "form" in body.lower() or "project" in body.lower()


# ── Index status JSON ───────────────────────────────────────────────────────


@pytest.mark.integration
def test_index_status_json(client):
    """GET /index/status returns JSON with expected keys."""
    response = client.get("/index/status")
    assert response.status_code == 200
    data = response.get_json()
    assert "running" in data
    assert isinstance(data["running"], bool)


# ── Stats page ──────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_stats_page_renders(client):
    """GET /stats renders without crashing."""
    response = client.get("/stats")
    assert response.status_code == 200


# ── Nested project paths ────────────────────────────────────────────────────


@pytest.mark.integration
def test_project_detail_redirects_or_renders(client):
    """GET /projects/<slug> returns a page or redirect."""
    with mock.patch(
        "research_assistant.workspace.projects.get_project",
        return_value=None,
    ):
        response = client.get("/projects/test-slug")
    assert response.status_code in (200, 302, 404)
