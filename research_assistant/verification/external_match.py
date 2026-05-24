"""HTTP clients for OpenAlex and Crossref with a shelve-based response cache.

Used by the Originality check tool to compare draft paragraphs against
published academic abstracts.  The clients are intentionally simple: paginated
JSON requests, polite rate-limit, 24-hour cached responses.
"""
from __future__ import annotations

import hashlib
import os
import re
import shelve
import time
from pathlib import Path
from typing import Any

import httpx

OPENALEX_BASE_URL = "https://api.openalex.org/works"
CROSSREF_BASE_URL = "https://api.crossref.org/works"
HTTP_TIMEOUT = 20.0

CACHE_PATH: Path = Path.home() / ".cache" / "research-assistant" / "external_match.shelf"
CACHE_TTL_SECONDS: int = 24 * 60 * 60  # 24 hours


def _cache_key(source: str, query: str) -> str:
    """Stable cache key for a (source, query) pair. Hex sha256."""
    h = hashlib.sha256()
    h.update(source.encode("utf-8"))
    h.update(b"\x00")
    h.update(query.encode("utf-8"))
    return h.hexdigest()


def _polite_pool_params() -> dict[str, str]:
    email = os.getenv("OPENALEX_EMAIL") or os.getenv("CONTACT_EMAIL")
    return {"mailto": email} if email else {}


def _reconstruct_abstract(inverted: dict[str, list[int]] | None) -> str:
    """OpenAlex returns abstracts as `{word: [positions]}` — flatten back to text."""
    if not inverted:
        return ""
    positions: dict[int, str] = {}
    for word, idxs in inverted.items():
        for i in idxs:
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions))


def _strip_doi_prefix(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("https://doi.org/", "")


def _first_author(authorships: list[dict[str, Any]]) -> str | None:
    if not authorships:
        return None
    name = authorships[0].get("author", {}).get("display_name")
    return name or None


def search_openalex(query: str, *, limit: int = 5) -> list[dict[str, Any]]:
    """Search OpenAlex /works. Returns a list of dicts with title/abstract/year/doi/authors/url.

    Network errors and non-2xx responses are caught and yield an empty list — the
    caller (originality.py) is tolerant of this.
    """
    params = {"search": query, "per-page": str(limit), **_polite_pool_params()}
    try:
        response = httpx.get(OPENALEX_BASE_URL, params=params, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return []

    out: list[dict[str, Any]] = []
    for work in payload.get("results", []):
        out.append(
            {
                "title": work.get("title", "") or "",
                "abstract": _reconstruct_abstract(work.get("abstract_inverted_index")),
                "year": work.get("publication_year"),
                "doi": _strip_doi_prefix(work.get("doi")),
                "authors": _first_author(work.get("authorships", [])),
                "url": work.get("id"),
            }
        )
    return out


def _strip_jats(html: str | None) -> str:
    """Crossref abstracts are wrapped in JATS XML tags. Strip them for cosine matching."""
    if not html:
        return ""
    return re.sub(r"<[^>]+>", "", html).strip()


def _crossref_authors(author_list: list[dict[str, Any]] | None) -> str | None:
    if not author_list:
        return None
    a = author_list[0]
    family = a.get("family", "")
    given = a.get("given", "")
    if family and given:
        return f"{family}, {given}"
    return family or given or None


def _crossref_year(issued: dict[str, Any] | None) -> int | None:
    if not issued:
        return None
    parts = issued.get("date-parts") or [[None]]
    if not parts or not parts[0]:
        return None
    year = parts[0][0]
    return int(year) if isinstance(year, int) else None


def search_crossref(query: str, *, limit: int = 5) -> list[dict[str, Any]]:
    """Search Crossref /works. Same return shape as search_openalex."""
    params = {
        "query.bibliographic": query,
        "rows": str(limit),
        "select": "DOI,title,abstract,issued,author,URL",
    }
    try:
        response = httpx.get(CROSSREF_BASE_URL, params=params, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return []

    out: list[dict[str, Any]] = []
    for item in payload.get("message", {}).get("items", []):
        title_list = item.get("title") or []
        out.append(
            {
                "title": title_list[0] if title_list else "",
                "abstract": _strip_jats(item.get("abstract")),
                "year": _crossref_year(item.get("issued")),
                "doi": item.get("DOI"),
                "authors": _crossref_authors(item.get("author")),
                "url": item.get("URL"),
            }
        )
    return out


_SEARCHERS = {
    "openalex": search_openalex,
    "crossref": search_crossref,
}


def cached_search(source: str, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
    """Run `_SEARCHERS[source](query, limit=limit)` with on-disk caching.

    Cache entries are pickled `{ts, results}` dicts. Entries older than
    CACHE_TTL_SECONDS are refetched. Cache failures are non-fatal — we fall
    back to a live request.
    """
    if source not in _SEARCHERS:
        raise ValueError(f"Unknown source '{source}'. Available: {list(_SEARCHERS)}")

    key = _cache_key(source, f"{query}::{limit}")
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with shelve.open(str(CACHE_PATH)) as cache:
            entry = cache.get(key)
            if entry and (time.time() - entry["ts"] < CACHE_TTL_SECONDS):
                return entry["results"]
    except Exception:
        pass  # cache miss / corruption — fall through to live fetch

    results = _SEARCHERS[source](query, limit=limit)

    try:
        with shelve.open(str(CACHE_PATH)) as cache:
            cache[key] = {"ts": time.time(), "results": results}
    except Exception:
        pass  # write failure is non-fatal

    return results
