"""Enforce that every Field in TOOL_SPECS has a non-empty help string.

Rationale: helpful tooltips are an explicit UX requirement (spec §12).
A failing test here means a Field was added or modified without a help text.
"""
from __future__ import annotations

import pytest

from research_assistant.web.tool_runner import TOOL_SPECS


@pytest.mark.unit
def test_every_field_has_help_text():
    missing: list[str] = []
    for spec in TOOL_SPECS:
        for fld in spec.fields:
            if not (fld.help or "").strip():
                missing.append(f"{spec.name}.{fld.name}")
    assert not missing, (
        "Fields missing help text:\n  " + "\n  ".join(missing)
    )
