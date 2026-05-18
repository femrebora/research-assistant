#!/usr/bin/env python3
"""ideas.py — get paragraph angles given evidence + a job statement.

This script does NOT write prose. It gives you a numbered list of angles
you could include in a paragraph. You pick, you write.

Usage:
    ./ideas.py evidence/ch1/numt_clinical.md \\
        --job "Establish NUMT contamination as a clinically significant problem"

    ./ideas.py evidence/ch1/numt_clinical.md \\
        --job "..." \\
        --manuscript manuscript/01_intro.md \\
        --model gemini
"""
from __future__ import annotations

import sys

import click
from rich.console import Console
from rich.markdown import Markdown

from common import MODELS, ask_model, read_file

console = Console()

PROMPT_TEMPLATE = """You are helping me expand a manuscript paragraph into a thesis paragraph.
I will write the prose myself. Your job is to suggest angles I could include,
not to write the paragraph.

## Job this paragraph must do
{job}

## Evidence retrieved from my library (with citations)
{evidence}

{manuscript_section}

## Your task

Give me 5-8 specific angles I could include in this paragraph, ranked by
what would most strengthen the argument for a thesis committee.

For each angle:
1. State the angle in one sentence.
2. Note what type of evidence supports it (refer to the evidence above by citation if applicable).
3. Briefly note a risk or weakness (e.g. "weak evidence base", "could distract from main point").

Format as a numbered markdown list. Do NOT write any prose I could paraphrase.
Do NOT write a draft paragraph. Just the angles.
"""

MANUSCRIPT_BLOCK = """## Existing manuscript version (for context — needs expansion)
{manuscript}
"""


@click.command()
@click.argument("evidence_file")
@click.option("--job", "-j", required=True,
              help="One sentence describing what this paragraph must do.")
@click.option("--manuscript", "-m", default=None,
              help="Optional: path to existing manuscript paragraph for context.")
@click.option("--model", default="claude",
              type=click.Choice(list(MODELS.keys())),
              help="Which model to use.")
@click.option("--temperature", "-t", default=0.4, type=float,
              help="Model temperature (0.0–2.0).")
def main(evidence_file, job, manuscript, model, temperature):
    evidence = read_file(evidence_file)

    manuscript_section = ""
    if manuscript:
        manuscript_section = MANUSCRIPT_BLOCK.format(manuscript=read_file(manuscript))

    prompt = PROMPT_TEMPLATE.format(
        job=job,
        evidence=evidence,
        manuscript_section=manuscript_section,
    )

    console.print(f"[dim]→ {model} | job: {job}[/dim]\n")
    result = ask_model(prompt, model=model, temperature=temperature)
    console.print(Markdown(result["text"]))

    if result["input_tokens"] and result.get("cost"):
        console.print(
            f"\n[dim]tokens: {result['input_tokens']} in, "
            f"{result['output_tokens']} out | "
            f"cost: ~${result['cost']:.4f}[/dim]"
        )


if __name__ == "__main__":
    main()
