#!/usr/bin/env python3
"""zot.py — search your Zotero library from the terminal.

Usage:
    ./zot.py "NUMT contamination"
    ./zot.py "MitoScape" --limit 20
    ./zot.py "rare variant" --collection "Chapter 1"
    ./zot.py "mtDNA" --bib          # print citekeys only
    ./zot.py "NUMT" --export bibtex  # export to BibTeX
"""
from __future__ import annotations

import json
import os
import re
import sys

import click
from pyzotero import zotero
from rich.console import Console
from rich.table import Table

console = Console()

BIBTEX_TYPE_MAP = {
    "journalArticle": "article",
    "book": "book",
    "bookSection": "incollection",
    "thesis": "phdthesis",
    "conferencePaper": "inproceedings",
    "preprint": "article",
    "report": "techreport",
}


def get_client():
    user_id = os.getenv("ZOTERO_USER_ID")
    api_key = os.getenv("ZOTERO_API_KEY")
    if not user_id or not api_key:
        console.print(
            "[red]Missing ZOTERO_USER_ID or ZOTERO_API_KEY in environment.[/red]\n"
            "Get them from https://www.zotero.org/settings/keys",
            highlight=False,
        )
        sys.exit(1)
    return zotero.Zotero(user_id, "user", api_key)


def find_collection_key(zot, name: str):
    """Find collection key by partial name match."""
    for c in zot.collections():
        if name.lower() in c["data"]["name"].lower():
            return c["key"], c["data"]["name"]
    return None, None


def extract_citekey(item_data: dict) -> str | None:
    """Extract BetterBibTeX citekey from item data."""
    extra = item_data.get("extra", "") or ""
    for line in extra.splitlines():
        if line.lower().startswith("citation key:"):
            return line.split(":", 1)[1].strip()
    # Fallback: some plugins store it in a 'citekey' field
    return item_data.get("citekey")


def item_to_bibtex(item_data: dict) -> str:
    """Convert a Zotero item to a BibTeX entry string."""
    item_type = item_data.get("itemType", "misc")
    entry_type = BIBTEX_TYPE_MAP.get(item_type, "misc")
    citekey = extract_citekey(item_data) or item_data.get("key", "unknown")

    creators = item_data.get("creators", [])
    author_list = []
    for c in creators:
        last = c.get("lastName", "")
        first = c.get("firstName", "")
        if last:
            author_list.append(f"{last}, {first}" if first else last)

    lines = [f"@{entry_type}{{{citekey},"]
    if author_list:
        lines.append(f"  author = {{{' and '.join(author_list)}}},")
    title = item_data.get("title", "")
    if title:
        lines.append(f"  title = {{{title}}},")
    year = (item_data.get("date") or "")[:4]
    if year:
        lines.append(f"  year = {{{year}}},")
    pub = item_data.get("publicationTitle") or ""
    if pub:
        lines.append(f"  journal = {{{pub}}},")
    doi = item_data.get("DOI") or ""
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    url = item_data.get("url") or ""
    if url:
        lines.append(f"  url = {{{url}}},")
    abstract = item_data.get("abstractNote") or ""
    if abstract:
        lines.append(f"  abstract = {{{abstract}}},")
    lines.append("}")
    return "\n".join(lines)


@click.command()
@click.argument("query")
@click.option("--limit", "-n", default=15, help="Max results.")
@click.option("--collection", "-c", default=None,
              help="Restrict to a collection (partial name match).")
@click.option("--tag", default=None,
              help="Filter by tag name (exact match).")
@click.option("--bib", is_flag=True,
              help="Print citekeys only (for pasting into a draft).")
@click.option("--export", "export_format", default=None,
              type=click.Choice(["bibtex", "json"]),
              help="Export results as BibTeX or JSON.")
def main(query, limit, collection, tag, bib, export_format):
    zot = get_client()

    if collection:
        key, name = find_collection_key(zot, collection)
        if not key:
            console.print(f"[red]No collection matching '{collection}'[/red]")
            sys.exit(1)
        console.print(f"[dim]Searching in: {name}[/dim]")
        results = zot.collection_items(key, q=query, limit=limit, itemType="-attachment", tag=tag)
    else:
        kwargs = {"q": query, "limit": limit}
        if tag:
            kwargs["tag"] = tag
        results = zot.top(**kwargs)

    if not results:
        console.print(f"[yellow]No results for '{query}'[/yellow]")
        return

    if bib:
        for r in results:
            citekey = extract_citekey(r["data"])
            if citekey:
                click.echo("@" + citekey)
            else:
                click.echo(f"@ {r['data'].get('key', 'unknown')}   [dim]# no citekey set[/dim]")
        return

    if export_format == "bibtex":
        for r in results:
            click.echo(item_to_bibtex(r["data"]) + "\n")
        console.print(f"[dim]Exported {len(results)} entries as BibTeX[/dim]")
        return

    if export_format == "json":
        click.echo(json.dumps([r["data"] for r in results], indent=2, ensure_ascii=False))
        return

    table = Table(title=f"Zotero: '{query}' ({len(results)} hits)", show_lines=False)
    table.add_column("Year", style="cyan", width=4)
    table.add_column("Authors", style="green", width=25)
    table.add_column("Title", style="white")
    table.add_column("Key", style="dim", width=10)

    for r in results:
        d = r["data"]
        year = d.get("date", "")[:4]
        authors = ", ".join(
            c.get("lastName", "") for c in d.get("creators", [])[:2]
        )
        if len(d.get("creators", [])) > 2:
            authors += " et al."
        title = d.get("title", "")[:80]
        table.add_row(year, authors, title, d.get("key", ""))

    console.print(table)


if __name__ == "__main__":
    main()
