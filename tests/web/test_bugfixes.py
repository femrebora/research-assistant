"""Regression tests for platform bugfixes (index, citekeys, wizard, SSE)."""
from __future__ import annotations

from unittest import mock

import pytest


@pytest.mark.unit
def test_citekey_markdown_renders_groups():
    """Session citekeys must render the matched key, not literal \\1 / \\2."""
    from research_assistant.web import app as app_module

    html = app_module._render_markdown_to_html("See [@smith2024] and @jones2023 for details.")
    assert "[@smith2024]" in html
    assert "@jones2023" in html
    assert "\\1" not in html
    assert "\\2" not in html


@pytest.mark.unit
def test_index_exists_false_for_empty_chroma(client, tmp_path, monkeypatch):
    """An empty chroma folder must not count as a usable index."""
    chroma = tmp_path / "chroma_db"
    chroma.mkdir()
    with (
        mock.patch("research_assistant.web.app.chroma_dir", return_value=chroma),
        mock.patch("research_assistant.web.app._get_collection", side_effect=RuntimeError("empty")),
    ):
        resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["exists"] is False


@pytest.mark.unit
def test_index_setup_includes_models(client):
    """Step 6 model dropdown needs models in the template context when an index exists."""
    fake_index = {
        "exists": True,
        "documents": 3,
        "chunks": 12,
        "embedding_model": "openai/text-embedding-3-small",
        "chunk_size": 800,
        "last_indexed": "2026-01-01",
    }
    with mock.patch("research_assistant.web.app._get_index_data", return_value=fake_index):
        resp = client.get("/index-setup?step=6")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'name="model"' in body
    assert "<option" in body
    assert "claude" in body


@pytest.mark.unit
def test_index_detect_zotero_endpoint(client):
    resp = client.get("/index/detect-zotero")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "suggested" in data
    assert "candidates" in data


@pytest.mark.unit
def test_index_clear_endpoint(client, tmp_path, monkeypatch):
    chroma = tmp_path / "chroma_db"
    chroma.mkdir()
    (chroma / "marker.txt").write_text("x", encoding="utf-8")
    with mock.patch("research_assistant.web.app.chroma_dir", return_value=chroma):
        resp = client.post("/index/clear")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "cleared"
    assert not chroma.exists()


@pytest.mark.unit
def test_settings_wizard_next_redirect(client, tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("THESIS_ROOT=/tmp/thesis\n", encoding="utf-8")
    monkeypatch.setenv("RA_ENV_FILE", str(env_file))
    monkeypatch.setenv("RA_HOST", "127.0.0.1")
    resp = client.post(
        "/settings",
        data={"THESIS_ROOT": str(tmp_path / "thesis"), "next": "/index-setup?step=2"},
        follow_redirects=False,
    )
    assert resp.status_code in (301, 302)
    assert "/index-setup?step=2" in resp.headers.get("Location", "")


@pytest.mark.unit
def test_paperforge_sse_does_not_double_slice():
    """get_events already slices; the SSE loop must iterate the returned list as-is."""
    import inspect

    from agentic import web_server

    src = inspect.getsource(web_server.paperforge_progress)
    assert "for evt in events:" in src
    assert "for evt in events[last_idx:]" not in src


@pytest.mark.unit
def test_library_search_uses_authors_field(client):
    fake = [{
        "title": "Example Paper",
        "authors": "Doe",
        "year": "2024",
        "citekey": "doe2024",
    }]
    with (
        mock.patch("research_assistant.workspace.library.search", return_value=fake),
        mock.patch("research_assistant.workspace.library.list_pdfs", return_value=[]),
    ):
        resp = client.get("/library-search?q=example&field=title")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Doe" in body
    assert "Example Paper" in body
