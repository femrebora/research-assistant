#!/usr/bin/env python3
"""ask.py — ask any question to any configured model.

Usage:
    ./ask.py "Explain coverage-based NUMT filtering" --model claude
    ./ask.py "Same question" --model gemini
    ./ask.py "Same question" --model deepseek
    cat draft.md | ./ask.py --model claude --stdin

Use this for quick questions where you want a particular model's perspective.
Not for generating thesis prose — use ideas.py or critique.py for paragraph work.
"""
from __future__ import annotations

import sys

import click
from rich.console import Console
from rich.markdown import Markdown

from research_assistant.common import MODELS, ask_model

console = Console()


@click.command()
@click.argument("prompt", required=False)
@click.option("--model", "-m", default="claude",
              type=click.Choice(list(MODELS.keys())),
              help="Which model to use.")
@click.option("--system", "-s", default=None,
              help="Optional system prompt.")
@click.option("--stdin", "use_stdin", is_flag=True,
              help="Read prompt from stdin instead of argument.")
@click.option("--temperature", "-t", default=0.3, type=float,
              help="Model temperature (0.0-2.0).")
@click.option("--raw", is_flag=True,
              help="Print raw text instead of rendered markdown.")
def main(prompt, model, system, use_stdin, temperature, raw):
    if use_stdin:
        if prompt:
            console.print("[yellow]Warning: --stdin overrides prompt argument[/yellow]")
        prompt = sys.stdin.read()
    if not prompt:
        click.echo("Error: provide a prompt as argument or use --stdin", err=True)
        sys.exit(1)

    console.print(f"[dim]→ {model} ({MODELS[model]})[/dim]")
    result = ask_model(prompt, model=model, system=system, temperature=temperature)

    if raw:
        click.echo(result["text"])
    else:
        console.print(Markdown(result["text"]))

    if result["input_tokens"]:
        console.print(
            f"\n[dim]tokens: {result['input_tokens']} in, "
            f"{result['output_tokens']} out[/dim]"
        )
        if result.get("cost"):
            console.print(f"[dim]cost: ~${result['cost']:.4f}[/dim]")


if __name__ == "__main__":
    main()
