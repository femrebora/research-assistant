"""Verify the tools.html template renders Field.help for every field kind.

Rationale: tools.html currently only renders fld.help for checkbox fields
(see line 29 at HEAD). Help on textarea / select / number / text / file_or_text
is silently dropped. This test pins the correct behavior.
"""
from __future__ import annotations

import html

import pytest

from research_assistant.web.app import app
from research_assistant.web.tool_runner import TOOL_SPECS


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.mark.unit
def test_help_renders_for_every_field_kind(client):
    """Every Field.help string appears in the rendered /tools/<name> page."""
    for spec in TOOL_SPECS:
        response = client.get(f"/tools/{spec.name}")
        assert response.status_code == 200, f"{spec.name} 404"
        body = response.get_data(as_text=True)
        # Unescape HTML entities for comparison
        unescaped_body = html.unescape(body)
        for fld in spec.fields:
            help_text = (fld.help or "").strip()
            if not help_text:
                continue
            assert help_text in unescaped_body, (
                f"Help text for {spec.name}.{fld.name} ({fld.kind}) "
                f"not rendered in /tools/{spec.name} page."
            )
