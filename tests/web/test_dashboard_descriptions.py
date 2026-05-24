"""Verify the dashboard tool catalog shows each tool's description."""
from __future__ import annotations

import re

import pytest

from research_assistant.web.tool_runner import TOOL_SPECS


def _first_sentence(text: str) -> str:
    """Extract the first sentence, handling abbreviations like .bib, e.g., etc."""
    # Split on period/exclamation/question followed by whitespace + capital
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return parts[0].strip().rstrip(".!?")


@pytest.mark.unit
def test_dashboard_shows_tool_descriptions(client):
    body = client.get("/").get_data(as_text=True)
    for spec in TOOL_SPECS:
        first_sentence = _first_sentence(spec.description)
        if not first_sentence:
            continue
        # Truncated to 100 chars matches the template-side truncation
        snippet = first_sentence[:100]
        assert snippet in body, (
            f"Description for {spec.name} not found in dashboard."
        )
