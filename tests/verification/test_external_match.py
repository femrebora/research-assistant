"""Unit tests for verification.external_match: OpenAlex + Crossref clients."""
from __future__ import annotations

import pytest


@pytest.mark.unit
def test_cache_key_is_stable_and_source_aware():
    from research_assistant.verification.external_match import _cache_key

    k1 = _cache_key("openalex", "NUMT filtering")
    k2 = _cache_key("openalex", "NUMT filtering")
    k3 = _cache_key("crossref", "NUMT filtering")
    k4 = _cache_key("openalex", "Different query")

    assert k1 == k2, "Same source+query must produce the same key"
    assert k1 != k3, "Different source must produce a different key"
    assert k1 != k4, "Different query must produce a different key"
    assert isinstance(k1, str) and len(k1) == 64, "Cache key should be hex sha256"
