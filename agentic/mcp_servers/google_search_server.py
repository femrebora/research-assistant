#!/usr/bin/env python3
"""Google-quality Search MCP — Brave Search API (free) + multi-backend fallback.

Brave Search API: https://brave.com/search/api/
  - Free tier: 2,000 queries/month, no credit card required
  - Sign up at https://api.search.brave.com/app/ (get API key)
  - export BRAVE_API_KEY=BSA...

Fallback chain: Brave → DuckDuckGo scraping → error

Run: python agentic/mcp_servers/google_search_server.py
"""
from __future__ import annotations

import json
import os
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import URLError

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Google-Quality Search")

MAX_RESULTS = 10
TIMEOUT = 15


# ── Brave Search (primary — free tier, 2000/mo) ──────────────────────────

def _search_brave(query: str, count: int = MAX_RESULTS) -> list[dict]:
    """Brave Search API — Google-quality results, free tier."""
    api_key = os.getenv("BRAVE_API_KEY", "")
    if not api_key:
        return [{"error": "BRAVE_API_KEY not set. Sign up: https://api.search.brave.com/app/"}]

    try:
        params = f"q={quote(query)}&count={count}"
        req = Request(
            f"https://api.search.brave.com/res/v1/web/search?{params}",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key,
            },
        )
        with urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        results = []
        for r in (data.get("web", {}).get("results", []) or [])[:count]:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("description", "")[:400],
            })

        # Also get news if available
        try:
            news_params = f"q={quote(query)}&count=3"
            news_req = Request(
                f"https://api.search.brave.com/res/v1/news/search?{news_params}",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "X-Subscription-Token": api_key,
                },
            )
            with urlopen(news_req, timeout=TIMEOUT) as resp:
                news_data = json.loads(resp.read().decode("utf-8"))
            for r in (news_data.get("results", []) or [])[:3]:
                results.append({
                    "title": f"[News] {r.get('title', '')}",
                    "url": r.get("url", ""),
                    "snippet": r.get("description", "")[:300],
                })
        except Exception:
            pass  # News is optional

        return results if results else [{"error": "No Brave results found"}]
    except Exception as e:
        return [{"error": f"Brave: {e}"}]


# ── DuckDuckGo via ddgs library (fallback) ────────────────────────────────

def _search_ddg(query: str, count: int = MAX_RESULTS) -> list[dict]:
    """DuckDuckGo search via ddgs library. No API key needed."""
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=count):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")[:300],
                })
        return results if results else [{"error": "No DDG results"}]
    except ImportError:
        return [{"error": "ddgs not installed. Run: pip install ddgs"}]
    except Exception as e:
        return [{"error": f"DDG: {e}"}]


# ── MCP Tools ─────────────────────────────────────────────────────────────

@mcp.tool()
def search(query: str, count: int = MAX_RESULTS) -> str:
    """Google-quality web search using best available free backend.

    Uses Brave Search API if BRAVE_API_KEY is set (free: 2,000/mo at
    https://api.search.brave.com/app/). Falls back to DuckDuckGo.

    Returns title, URL, and snippet for each result.
    Best for: companies, news, market data, clinical trials, products.

    Args:
        query: Search query string
        count: Max results (default 10)
    """
    # Try Brave first (best results)
    results = _search_brave(query, count)

    # Fall back to DDG
    if not results or "error" in results[0]:
        results = _search_ddg(query, count)

    if not results:
        return "No results found."
    if "error" in results[0]:
        return f"Search error: {results[0]['error']}"

    lines = [f"Results for: {query}\n"]
    for i, r in enumerate(results, 1):
        lines.append(
            f"{i}. **{r['title']}**\n"
            f"   {r.get('snippet', '')[:300]}\n"
            f"   {r['url']}"
        )
    return "\n\n".join(lines)


@mcp.tool()
def search_news(query: str, count: int = 5) -> str:
    """Search for recent news articles.

    Best for: funding announcements, product launches, regulatory decisions,
    partnership news, clinical trial results.

    Args:
        query: News search query
        count: Max results (default 5)
    """
    # Use Brave news if available
    api_key = os.getenv("BRAVE_API_KEY", "")
    if api_key:
        try:
            params = f"q={quote(query)}&count={count}"
            req = Request(
                f"https://api.search.brave.com/res/v1/news/search?{params}",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "X-Subscription-Token": api_key,
                },
            )
            with urlopen(req, timeout=TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            results = []
            for r in (data.get("results", []) or [])[:count]:
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("description", "")[:300],
                })

            if results:
                lines = [f"News: {query}\n"]
                for i, r in enumerate(results, 1):
                    lines.append(f"{i}. **{r['title']}**\n   {r['snippet']}\n   {r['url']}")
                return "\n\n".join(lines)
        except Exception as e:
            pass

    # Fall back to web search with "news" appended
    return search(f"{query} news", count)


if __name__ == "__main__":
    print("Google-Quality Search MCP starting...", file=sys.stderr)
    mcp.run()
