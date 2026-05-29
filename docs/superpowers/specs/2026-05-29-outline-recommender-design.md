# Outline Recommender + Focused UI Polish — Design

**Date:** 2026-05-29
**Status:** Approved

## Problem

The existing `outline` tool is "blind": it requires the user to *already know*
their one-sentence job statement **and** supply a gathered evidence file. There
is nothing that helps a researcher decide the *overall structure* of a paper or
chapter from a topic alone. New users do not know where to start.

## Goal

Add an **Outline Recommender** that turns a topic / research question into a
full, paper-type-aware section skeleton — with per-section purpose, suggested
length, paragraph stubs, optional organizational variants, and (when an index
exists) a map of which indexed papers cover each section plus coverage gaps.

This is **additive**: the existing `outline` tool and all other tools are
unchanged.

## Components

### 1. `research_assistant/writing/outline_recommender.py` (CLI `ra-outline-recommend`)

Inputs: `topic` (positional, required), `--paper-type`, `--discipline`,
`--audience`, `--target-words`, `--variants` (flag), `--map-evidence` (flag),
`--model`, `--temperature`, `--save`, `--raw`.

**Paper-type template registry** (pure data — testable without an LLM). Each
entry is an ordered list of canonical sections, each with a default purpose and
a suggested share of the total word budget:

- `imrad` — IMRaD research article
- `review` — narrative / literature review
- `systematic-review` — PRISMA-style systematic review
- `thesis-chapter` — single thesis chapter
- `methods` — methods / tools paper
- `case-study` — case study / report

**Flow:**

1. **Structure pass (LLM).** Build a prompt from the template + topic; ask the
   model to adapt sections to the topic, give a one-line purpose, an estimated
   word count (derived from `--target-words` × share), 2–4 note-style paragraph
   stubs per section, and `[needs evidence]` flags. Note-taking style only — no
   polished prose (consistent with the existing `outline` tool's contract).
2. **Variants pass (LLM, only if `--variants`).** Ask for 2–3 alternative
   *organizational schemes* (e.g. thematic / chronological / methodological),
   each a compact section list with a one-line rationale.
3. **Evidence mapping (only if `--map-evidence`).** For each top-level section,
   query the RAG index and attach matched citekeys; sections with no relevant
   chunks are flagged as coverage gaps. The retriever is **injected** so tests
   use a fake. If no Chroma index exists, the step is skipped with a clear note
   rather than erroring.

**Testable seams (no network/LLM):**
`PAPER_TYPES` registry, `build_structure_prompt()`, `build_variants_prompt()`,
`estimate_words()`, `merge_evidence_map()`, and input validation
(`--paper-type` choice, `--target-words` bounds).

### 2. Web wiring

- Register one `ToolSpec` (`outline_recommend`, category `writing`) in
  `tool_runner.TOOL_SPECS`. This auto-adds it to the sidebar nav and exposes
  `/tools/outline_recommend` + `/tools/outline_recommend/run` via the existing,
  already-tested generic runner. No new result-rendering code.
- Add a thin first-class route `/outline-recommender` + template: a guided
  intro and the same form, **pre-filled from the active project** (topic ←
  research question, discipline, citation style). It submits via HTMX to the
  existing `/tools/outline_recommend/run` endpoint and renders the standard
  `_result.html` partial.

### 3. Active-project concept (new, minimal)

`projects.py` gains:

- `set_active_slug(slug)` / `get_active_slug()` backed by a plain-text
  `PROJECTS_DIR/.active` file.
- `get_active_project()` → the active `Project`, falling back to the most
  recently updated project, or `None` when there are no projects.

Web: `POST /projects/<slug>/activate` + a "Set active" control on the projects
page. The active project drives the dashboard banner and recommender pre-fill.

### 4. Dashboard / UX polish

- **Active-project banner** at the top of the dashboard (title + research
  question, or a prompt to create one).
- **"Start writing" guided card** linking into the recommender.
- Fix the `base.html` footer version string to match the README.

## Error handling

- Invalid `--paper-type` → Click choice error (exit 2).
- `--target-words` out of range (e.g. < 250 or > 200000) → friendly error.
- Evidence mapping with no index → printed note, recommender still returns the
  structure.
- Empty/whitespace topic → friendly error.

## Testing

- Unit tests for the template registry, prompt builders, word estimation,
  evidence-map merge, and CLI validation (via Click `CliRunner`, model call
  monkeypatched).
- Unit tests for the active-project store (set/get/fallback/no-projects).
- Existing suite must stay green; new logic targets ≥80% coverage.

## Out of scope (YAGNI)

- Persisting recommender output history.
- Auto-filling *every* tool form from the active project (only the recommender).
- Editing the recommended outline in-app (use the existing workspace editor).
