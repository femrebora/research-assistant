#!/usr/bin/env python3
"""evidence.py — query your PDFs via PaperQA2, save cited output.

Usage:
    ./evidence.py "What evidence exists for NUMT contamination affecting clinical mtDNA variant calling?"
    ./evidence.py "..." --save evidence/ch1/numt_clinical.md
    ./evidence.py "..." --model sonnet --quality high

The save path is relative to THESIS_ROOT (default ~/thesis).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.markdown import Markdown

from common import MODELS, save_file

console = Console()


@click.command()
@click.argument("question")
@click.option("--save", "-o", default=None,
              help="Save output to this path (relative to THESIS_ROOT).")
@click.option("--quality", default="high_quality",
              type=click.Choice(["fast", "high_quality", "wikicrow"]),
              help="PaperQA2 settings preset.")
@click.option("--model", "-m", default="sonnet",
              type=click.Choice(list(MODELS.keys())),
              help="LLM model for PaperQA2 to use.")
@click.option("--storage", default=None,
              help="Path to PDF directory (default: $ZOTERO_STORAGE).")
def main(question, save, quality, model, storage):
    storage = storage or os.getenv("ZOTERO_STORAGE")
    if not storage or not Path(storage).expanduser().exists():
        console.print(
            "[red]ZOTERO_STORAGE not set or doesn't exist.[/red]\n"
            "Set it in .env to your Zotero storage folder, e.g. ~/Zotero/storage",
        )
        sys.exit(1)

    try:
        from paperqa import Settings, ask
    except ImportError:
        console.print("[red]paper-qa not installed. Run: pip install paper-qa[/red]")
        sys.exit(1)

    console.print(f"[dim]→ querying corpus at {storage} (preset: {quality}, model: {model})[/dim]")
    console.print(f"[dim]→ question: {question}[/dim]\n")

    # Change to storage dir so PaperQA2 picks up PDFs there
    original_cwd = Path.cwd()
    os.chdir(Path(storage).expanduser())
    try:
        settings = Settings.from_name(quality)
        settings.llm = MODELS[model]
        # Also set summary LLM if the attribute exists (PaperQA2 >= v5)
        if hasattr(settings, "summary_llm"):
            settings.summary_llm = MODELS[model]
        response = ask(question, settings=settings)
    finally:
        os.chdir(original_cwd)

    # Build markdown output with citations
    answer_text = str(response.session.answer) if hasattr(response, "session") else str(response)

    output = f"""# Evidence query

**Question:** {question}

**Preset:** {quality}
**Model:** {model} ({MODELS[model]})

---

{answer_text}
"""

    if save:
        path = save_file(save, output)
        console.print(f"[green]Saved to: {path}[/green]\n")

    console.print(Markdown(answer_text))


if __name__ == "__main__":
    main()
