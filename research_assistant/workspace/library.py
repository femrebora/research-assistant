"""Local PDF library — list, search, and excerpt PDFs from Zotero storage
and plain folders.

The workspace can pull source context from two places:

* Zotero (via API for metadata, local storage for PDFs)
* a plain local folder of PDFs, configurable via ``THESIS_DOCS``
  (default ``~/thesis``)

This module deliberately keeps things minimal: no indexing, no embeddings.
It lists files, searches Zotero metadata, and pulls bounded text excerpts
on demand so an AI edit prompt can include them as context.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from research_assistant.common import THESIS_ROOT
from research_assistant.researcher import _extract_pdf_text

logger = logging.getLogger(__name__)


def docs_dir() -> Path:
    """Return the active local-PDF folder, re-reading env vars each call.

    Override via ``THESIS_DOCS``; falls back to ``THESIS_PDF_DIR``; otherwise
    defaults to ``$THESIS_ROOT`` so a fresh install works without configuration.
    """
    return Path(
        os.getenv("THESIS_DOCS")
        or os.getenv("THESIS_PDF_DIR")
        or str(THESIS_ROOT)
    ).expanduser()


def zotero_storage() -> Path | None:
    """Return the resolved Zotero storage path, re-reading env vars each call.

    Returns ``None`` when ``ZOTERO_STORAGE`` is unset or the path does not exist.
    """
    raw = os.getenv("ZOTERO_STORAGE", "").strip()
    if not raw:
        return None
    expanded = Path(raw).expanduser()
    return expanded if expanded.exists() else None


# Per-document excerpt cap when feeding text into an AI edit prompt. Keeps
# total token usage predictable even when the user attaches many sources.
MAX_EXCERPT_CHARS = 4000


# ── Data model ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class LocalPdf:
    """A PDF file found under :data:`DOCS_DIR` or ZOTERO_STORAGE."""

    rel_path: str           # path relative to root (used as the form value)
    name: str               # filename only, for display
    size_kb: int
    modified: str           # ISO date for sorting / display
    source: str = "local"   # "local" or "zotero"


@dataclass(frozen=True)
class LibraryResult:
    """A search result from Zotero API or local PDF scan."""

    title: str
    authors: str = ""
    year: str = ""
    citekey: str = ""
    item_type: str = ""
    source: str = ""        # "zotero_api", "zotero_storage", "local"
    pdf_path: str = ""      # relative path to PDF if available


# ── Public API ──────────────────────────────────────────────────────────────


def configured_root() -> Path:
    """Return the active local-PDF folder so the UI can show it to the user."""
    return docs_dir()


def zotero_storage_path() -> str:
    """Return the resolved Zotero storage path as a string for the UI."""
    zs = zotero_storage()
    if zs:
        return str(zs)
    raw = os.getenv("ZOTERO_STORAGE", "").strip()
    if raw:
        expanded = str(Path(raw).expanduser())
        return f"{expanded} (not found)"
    return "(not configured)"


def zotero_storage_diagnostics() -> dict:
    """Return diagnostics about Zotero storage for the UI."""
    raw = os.getenv("ZOTERO_STORAGE", "").strip()
    if not raw:
        return {"configured": False, "resolved": "", "exists": False,
                "subfolders": 0, "pdfs": 0, "error": None}

    expanded = Path(raw).expanduser()
    resolved = str(expanded)
    exists = expanded.exists() and expanded.is_dir()
    subfolders = 0
    pdfs = 0
    error = None

    if exists:
        try:
            subfolders = len([d for d in expanded.iterdir() if d.is_dir()])
            pdfs = len(list(expanded.rglob("*.pdf")))
        except (PermissionError, OSError) as e:
            error = str(e)

    return {
        "configured": True,
        "raw": raw,
        "resolved": resolved,
        "exists": exists,
        "subfolders": subfolders,
        "pdfs": pdfs,
        "error": error,
    }


def search(query: str, field: str = "all") -> list[dict]:
    """Search Zotero library and local PDFs.

    If Zotero API credentials are available, searches via the API for metadata.
    Also searches local PDFs by filename in ZOTERO_STORAGE and DOCS_DIR.

    Returns a list of result dicts safe for template rendering.
    """
    results: list[dict] = []

    # ── Zotero API search (if configured) ───────────────────────────────
    zotero_user = os.getenv("ZOTERO_USER_ID", "").strip()
    zotero_key = os.getenv("ZOTERO_API_KEY", "").strip()
    if zotero_user and zotero_key and query:
        try:
            from pyzotero import zotero as _zotero_mod
            zot = _zotero_mod.Zotero(zotero_user, "user", zotero_key)
            items = zot.top(q=query, limit=30)
            for item in items:
                data = item.get("data", {})
                creators = data.get("creators", [])
                author_str = ", ".join(
                    c.get("lastName", "") for c in creators[:3]
                )
                if len(creators) > 3:
                    author_str += " et al."
                citekey = _extract_citekey_from_item(data)
                results.append({
                    "title": data.get("title", "Untitled"),
                    "authors": author_str,
                    "year": (data.get("date", "") or "")[:4],
                    "citekey": citekey or data.get("key", ""),
                    "item_type": data.get("itemType", ""),
                    "source": "Zotero API",
                    "pdf_path": "",
                })
        except Exception:
            logger.exception("Zotero API search failed (user=%r)", zotero_user)
            # fall through to local search

    # ── Local PDF search in ZOTERO_STORAGE ──────────────────────────────
    zs = zotero_storage()
    if zs and zs.exists() and query:
        query_lower = query.lower()
        try:
            for pdf_path in zs.rglob("*.pdf"):
                if query_lower in pdf_path.name.lower():
                    rel = pdf_path.relative_to(zs).as_posix()
                    # Avoid duplicates with API results
                    if not any(r.get("pdf_path") == rel for r in results):
                        results.append({
                            "title": pdf_path.stem,
                            "authors": "",
                            "year": "",
                            "citekey": "",
                            "item_type": "PDF",
                            "source": "Zotero Storage",
                            "pdf_path": rel,
                        })
        except (PermissionError, OSError):
            pass

    # ── Local PDF search in DOCS_DIR ────────────────────────────────────
    docs = docs_dir()
    if docs.exists() and query:
        query_lower = query.lower()
        try:
            for pdf_path in docs.rglob("*.pdf"):
                if query_lower in pdf_path.name.lower():
                    rel = pdf_path.relative_to(docs).as_posix()
                    if not any(r.get("pdf_path") == rel for r in results):
                        results.append({
                            "title": pdf_path.stem,
                            "authors": "",
                            "year": "",
                            "citekey": "",
                            "item_type": "PDF",
                            "source": "Local",
                            "pdf_path": rel,
                        })
        except (PermissionError, OSError):
            pass

    return results


def list_pdfs(root: Path | None = None, *, limit: int = 200) -> list[LocalPdf]:
    """List PDFs under ``root`` (defaults to :func:`docs_dir`).

    Also includes PDFs from ZOTERO_STORAGE if configured.
    The result is sorted by modified-time, newest first, and capped at
    ``limit`` entries so the sidebar stays usable on a 5 000-PDF library.
    """
    items: list[LocalPdf] = []

    # ── DOCS_DIR ───────────────────────────────────────────────────────
    base = (root or docs_dir()).expanduser()
    if base.exists() and base.is_dir():
        for path in base.rglob("*.pdf"):
            try:
                stat = path.stat()
            except OSError:
                continue
            if not path.is_file():
                continue
            rel = path.relative_to(base).as_posix()
            items.append(
                LocalPdf(
                    rel_path=rel,
                    name=path.name,
                    size_kb=max(1, stat.st_size // 1024),
                    modified=_iso_date(stat.st_mtime),
                    source="local",
                )
            )

    # ── ZOTERO_STORAGE ─────────────────────────────────────────────────
    zs = zotero_storage()
    if zs and zs.exists() and base != zs:
        for path in zs.rglob("*.pdf"):
            try:
                stat = path.stat()
            except OSError:
                continue
            if not path.is_file():
                continue
            rel = path.relative_to(zs).as_posix()
            items.append(
                LocalPdf(
                    rel_path=rel,
                    name=path.name,
                    size_kb=max(1, stat.st_size // 1024),
                    modified=_iso_date(stat.st_mtime),
                    source="zotero",
                )
            )

    items.sort(key=lambda p: p.modified, reverse=True)
    return items[:limit]


def excerpt(rel_path: str, *, max_chars: int = MAX_EXCERPT_CHARS) -> str:
    """Return up to ``max_chars`` of plain text from a PDF inside the library.

    Path traversal is rejected — the resolved path must live inside the
    configured root. Returns an empty string if extraction fails.
    """
    safe_path = _resolve(rel_path)
    if safe_path is None or not safe_path.exists():
        return ""
    text = _extract_pdf_text(safe_path) or ""
    if not text:
        return ""
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars].rstrip() + "\n…[truncated]"


def resolve(rel_path: str) -> Path | None:
    """Public wrapper around the internal path resolver."""
    return _resolve(rel_path)


# ── Internals ───────────────────────────────────────────────────────────────


def _resolve(rel_path: str) -> Path | None:
    """Resolve ``rel_path`` against :func:`docs_dir`, rejecting escapes."""
    if not rel_path:
        return None
    root = docs_dir().expanduser().resolve()
    candidate = (root / rel_path).expanduser().resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _extract_citekey_from_item(item_data: dict) -> str | None:
    """Extract BetterBibTeX citekey from item data."""
    extra = item_data.get("extra", "") or ""
    for line in extra.splitlines():
        if line.lower().startswith("citation key:"):
            return line.split(":", 1)[1].strip()
    return item_data.get("citekey")


def _iso_date(mtime: float) -> str:
    from datetime import UTC, datetime

    return datetime.fromtimestamp(mtime, tz=UTC).isoformat(timespec="seconds")
