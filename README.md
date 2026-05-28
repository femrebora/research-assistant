# research-assistant

[![python](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-A3E635)](LICENSE)
[![flask](https://img.shields.io/badge/web%20UI-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![zotero](https://img.shields.io/badge/Zotero-RAG-CC2936?logo=zotero&logoColor=white)](https://www.zotero.org/)
[![models](https://img.shields.io/badge/models-Claude%20%7C%20Gemini%20%7C%20DeepSeek%20%7C%20GPT--5-7C3AED)](#supported-models)
[![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-555)](#quick-start)
[![status](https://img.shields.io/badge/status-active-A3E635)](#)

A CLI toolkit + web UI for master's and PhD thesis research. Index your Zotero PDF library, ask research questions with cited answers from your own papers, compare answers across multiple AI models (Claude, Gemini, DeepSeek, GPT/Codex), and save everything for later paraphrasing.

## What's here

### Research

| Script | Purpose |
|--------|---------|
| `researcher.py` | **RAG research assistant** — index Zotero PDFs into local vector store, ask questions with cited answers, compare models |
| `compare.py` | **Multi-model comparison** — ask the same question to multiple AI models simultaneously, with or without document context |
| `ask.py` | **Single-model queries** — ask any question to any configured model (Claude, Gemini, DeepSeek, GPT, local) |
| `zot.py` | **Zotero search** — search your Zotero library from terminal |
| `evidence.py` | **PaperQA2 queries** — query your PDFs via PaperQA2, save cited output |
| `discover.py` | **External paper discovery** — find new papers via OpenAlex, Semantic Scholar, or Elicit |

### Writing pipeline

| Script | Purpose |
|--------|---------|
| `ideas.py` | **Paragraph angles** — get paragraph angles given evidence + a job statement |
| `outline.py` | **Section outline** — hierarchical outline with citation stubs from evidence + a job |
| `critique.py` | **Draft critique** — prose or sentence-anchored diff critique of a paragraph you've written |
| `coherence.py` | **Multi-paragraph flow** — check chapter-level transitions, redundancy, thesis support |
| `paraphrase_check.py` | **Near-duplicate check** — flag draft paragraphs too similar to your own indexed sources |
| `audit.py` | **Citation audit** — per-source counts, over-cited papers, unused .bib entries, density |
| `verify.py` | **Citation verification** — check all `[@citekey]` placeholders resolve in your `.bib` |

### PaperForge — Multi-Agent Paper Generation

PaperForge generates complete academic papers from a codebase or a research topic using 7 specialized AI agents.

| Script | Purpose |
|--------|---------|
| `run_agentic.py` | **Code → Paper** — generate an academic paper from a codebase. Analyzes code, writes draft, assesses quality, rewrites, checks plagiarism, generates figures. |
| `run_review.py` | **Topic → Review Article** — generate a literature review autonomously. Searches OpenAlex + DuckDuckGo, synthesizes research, writes a proper review article. |
| `quick_ai_score.py` | **AI Text Detection** — 7 mechanical checks (em dashes, sentence length, comma density, burstiness, formulaic phrases, paragraph openings, roadmap sentences) with 0-10 scoring. No LLM calls. |

**Pipeline Architecture:**

```
Codebase → Code Analyst (Gemini) → Writer (DeepSeek) → Assessor (Claude)
              ↓                         ↓                    ↓
        Technical report          Complete draft      Section scores
                                                              ↓
                                              Rewriter (Claude) ←──┘
                                              (loops ≤3× until score ≥7)
                                                              ↓
                                              Plagiarism Check (report-only)
                                                              ↓
                                              Figure Gen (Gemini) → Supervisor (Claude)
```

For review articles, `Code Analyst` is replaced by `Literature Researcher` which searches:
- **OpenAlex** — academic papers (free, no API key)
- **DuckDuckGo** — companies, market data, clinical news

**Agents:**

| Agent | Model | Role |
|-------|-------|------|
| Code Analyst | Gemini 2.5 Pro | Scans codebase, produces structured technical report |
| Literature Researcher | Claude Opus 4.7 | Searches web + academic databases, synthesizes research |
| Writer | DeepSeek | Generates complete paper from technical report |
| Assessor | Claude Opus 4.7 | Scores each section 1-10 for quality + AI-sounding patterns |
| Rewriter | Claude Opus 4.7 | Revises sections scoring <7, with rewrite loop (capped at 3) |
| Plagiarism Check | DeepSeek | Checks originality and AI-likelihood (report-only) |
| Figure Gen | Gemini 2.5 Pro | Generates figures from technical data |
| Figure Supervisor | Claude Opus 4.7 | Reviews figures for publication quality |

**Anti-AI prose safeguards:**
- Prompt-level: em dash ban, sentence length caps (35 words), comma limits
- Post-processing: `agentic/text_cleanup.py` mechanically removes remaining em dashes, splits overlong sentences
- Cached AI tells: `ai_tells.json` with overused words, formulaic structures
- `quick_ai_score.py`: 0-10 mechanical AI-text scoring

**Benchmark data:** `agentic/benchmark_parser.py` auto-discovers JSON/CSV/TSV benchmarks from the target codebase, injecting real numbers into the Writer prompt to prevent data fabrication.

### Web UI

| Script | Purpose |
|--------|---------|
| `app.py` | **Web UI** — Flask web interface for the research assistant |
| `agentic/web_server.py` | **PaperForge Web UI** — Flask blueprint with SSE progress streaming, form, and paper download |

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/femrebora/research-assistant
cd research-assistant
```

### 2. Create Python virtual environment

```bash
python3 -m venv ~/.venvs/thesis
source ~/.venvs/thesis/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp env.example .env
# Edit .env with your API keys and paths
```

Required variables:
```bash
# At least one model provider
ANTHROPIC_API_KEY=sk-ant-...     # or ANTHROPIC_AUTH_TOKEN (for Claude CLI)
GEMINI_API_KEY=...
DEEPSEEK_API_KEY=sk-...          # or ANTHROPIC_AUTH_TOKEN (fallback)
OPENAI_API_KEY=sk-...

# Zotero integration (for researcher.py and zot.py)
ZOTERO_USER_ID=1234567
ZOTERO_API_KEY=...

# Paths
THESIS_ROOT=/home/you/thesis
ZOTERO_STORAGE=/home/you/Zotero/storage
```

### 4. Index your papers

```bash
# Index all Zotero PDFs (one-time, takes a few minutes)
./researcher.py index

# Or index a specific collection
./researcher.py index --collection "Chapter 1" --limit 20
```

### 5. Ask your first question

```bash
./researcher.py ask "What are the main approaches to filtering NUMT in clinical mtDNA?"
```

## CLI Usage

### Researcher — RAG over your papers

```bash
# Index management
./researcher.py index                          # Index all Zotero PDFs
./researcher.py index --collection "Ch. 1"     # Index a specific collection
./researcher.py index --force                   # Re-index everything
./researcher.py index --limit 50               # Index first 50 items only
./researcher.py stats                          # View index statistics

# Ask questions with cited, paraphrase-ready answers
./researcher.py ask "What is NUMT contamination?"
./researcher.py ask "..." --model gemini        # Use a different model
./researcher.py ask "..." --k 10               # Retrieve fewer chunks
./researcher.py ask "..." --threshold 0.4      # Stricter relevance filter
./researcher.py ask "..." --save session_name  # Save Q&A to a session file
./researcher.py ask "..." --raw                # Plain text output (for piping)

# Compare answers from multiple models (same RAG context)
./researcher.py ask "..." --compare claude,gemini,gpt
./researcher.py ask "..." --compare claude,deepseek --save comparison

# Browse past sessions
./researcher.py sessions                        # List all sessions
./researcher.py sessions --view session_name    # View a session
./researcher.py sessions --view last            # View most recent session
```

### Compare — Multi-model comparison

```bash
# Direct comparison (no document context)
./compare.py "What is NUMT?" --models claude,gemini,gpt
./compare.py "..." --models claude,sonnet,haiku,gemini,deepseek,gpt

# RAG comparison (same context from your indexed papers)
./compare.py "What approaches exist for NUMT filtering?" --models claude,gemini --rag
./compare.py "..." --models claude,gpt --rag --k 15 --threshold 0.4

# Save comparison to session
./compare.py "..." --models claude,gemini,gpt --save my_comparison
```

### PaperForge — Paper generation

```bash
# One-time setup: refresh knowledge caches
./run_agentic.py --refresh-style --domain bioinformatics
./run_agentic.py --refresh-artifacts

# Generate a paper from a codebase
./run_agentic.py /path/to/your/project \
    --summary "A pipeline for detecting transient binding pockets from MD simulations" \
    --output ~/thesis/output/my-paper

# Generate a review article from a topic (autonomous web research!)
./run_review.py --topic "CRISPR-Based Therapeutics: Delivery Methods and Clinical Trials"

# Check a paper for AI-generated text patterns
./quick_ai_score.py paper.md --json
./quick_ai_score.py paper.md --ai-tells ~/thesis/cache/ai_tells.json

# Launch Streamlit dashboard
./run_agentic.py --ui
```

**Review article mode** does everything autonomously:
1. Searches OpenAlex for academic papers (free, no API key)
2. Searches DuckDuckGo for companies, market data, clinical news
3. Synthesizes 12K+ characters of research via Claude
4. Generates a proper literature review (surveys the field, cites real data)
5. Assesses, rewrites (≤3×), plagiarism-checks, generates figures

**Expected performance:**
- Code → Paper: 10 agent calls, ~$1.67, AI score <2/10
- Topic → Review: 12 agent calls, ~$2.08, AI score <2/10
- All sections typically score 7-9/10

### Other tools

```bash
# Ask a single model (quick questions)
./ask.py "Explain MitoScape's filtering approach" --model claude
./ask.py "Same question" --model gemini           # Second opinion
./ask.py "Same question" --model deepseek          # Cheaper option

# Search Zotero library
./zot.py "NUMT contamination"
./zot.py "MitoScape" --limit 20 --bib             # Just citekeys

# Evidence query via PaperQA2
./evidence.py "What evidence exists for NUMT affecting variant calling?" --save evidence/ch1.md

# Discover new papers from OpenAlex / Semantic Scholar / Elicit
./discover.py "NUMT filtering clinical mtDNA" --source openalex --limit 15
./discover.py "..." --source semantic_scholar --year-from 2020
./discover.py "..." --export bibtex > new_papers.bib
```

### Writing pipeline

```bash
# 1. Get paragraph angles from evidence
./ideas.py evidence/ch1/numt.md --job "Establish NUMT as clinically significant"

# 2. Or generate a full hierarchical outline (one stub per paragraph)
./outline.py evidence/ch1/numt.md \
    --job "Argue NUMT filtering is mandatory in clinical mtDNA pipelines" \
    --sections 4 --depth 2 --save outlines/ch1.md

# 3. Critique your draft paragraph (prose mode or sentence-anchored)
./critique.py drafts/para.md --job "Define NUMT contamination"
./critique.py drafts/para.md --job "..." --diff           # S1, S2, ... annotations

# 4. Check whole-chapter coherence and thesis support
./coherence.py drafts/chapter1.md \
    --thesis "NUMT filtering is mandatory for clinical mtDNA pipelines"

# 5. Catch paragraphs that drifted too close to source wording
./paraphrase_check.py drafts/chapter1.md --threshold 0.85

# 6. Audit citation usage (density, over-cites, unused .bib entries)
./audit.py drafts/chapter1.md --bib bib/thesis.bib --over-cite 6

# 7. Verify citations resolve to the .bib (catches typos / hallucinations)
./verify.py drafts/chapter1.md --bib bib/thesis.bib
```

## Web UI

Launch the Flask web interface:

```bash
flask --app app run
# Or with a custom port and debug mode:
flask --app app run --port 5050 --debug
```

Open **http://localhost:5000** in your browser.

To add the PaperForge web UI, register the blueprint in your Flask app:
```python
from agentic.web_server import paperforge_bp
app.register_blueprint(paperforge_bp)
```

Or run standalone: `python -m agentic.web_server` (opens on port 5055).

### Pages

- **Dashboard** — index stats, quick-ask box, recent sessions
- **Ask a Question** — type a question, select a model, get cited answers with source cards
- **Compare Models** — ask multiple models simultaneously, see side-by-side comparison
- **Sessions** — browse, view, and delete saved Q&A sessions
- **Manage Index** — start background indexing with progress tracking
- **PaperForge** — generate papers from code or topics with live SSE progress streaming, section scores, and paper download

## Supported Models

| Alias | Model | Provider | Input $/1M | Output $/1M |
|-------|-------|----------|-----------|------------|
| `claude` | Claude Opus 4.7 | Anthropic | $15.00 | $75.00 |
| `sonnet` | Claude Sonnet 4.6 | Anthropic | $3.00 | $15.00 |
| `haiku` | Claude Haiku 4.5 | Anthropic | $0.80 | $4.00 |
| `gemini` | Gemini 2.5 Pro | Google | $1.25 | $5.00 |
| `flash` | Gemini 2.5 Flash | Google | $0.075 | $0.30 |
| `deepseek` | DeepSeek Chat | DeepSeek | $0.27 | $1.10 |
| `gpt` | GPT-5 | OpenAI | $1.25 | $10.00 |
| `gpt-mini` | GPT-5 Mini | OpenAI | $0.15 | $0.60 |
| `codex` | GPT-5 (alias) | OpenAI | $1.25 | $10.00 |

Edit the `MODELS` dict in `common.py` to change model versions or add new providers.

## Typical Thesis Workflow

```bash
# 1. Index your Zotero library (once)
./researcher.py index

# 2. (Optional) Discover papers you don't have yet
./discover.py "NUMT contamination clinical mtDNA" --year-from 2020 --export bibtex >> new.bib

# 3. Research a topic — ask questions, save sessions
./researcher.py ask "What are the clinical implications of NUMT contamination?" --save numt_clinical
./researcher.py ask "What tools exist for NUMT detection?" --session numt_clinical
./researcher.py ask "What are the limitations of current approaches?" --session numt_clinical

# 4. Compare model perspectives on tricky questions
./compare.py "Is NUMT filtering necessary for clinical mtDNA sequencing?" --models claude,gemini,gpt --rag

# 5. Get evidence for a specific paragraph
./evidence.py "NUMT filtering methods comparison" --save evidence/ch1/numt_methods.md

# 6. Plan: paragraph angles + (optional) full outline
./ideas.py evidence/ch1/numt_methods.md --job "Compare NUMT detection tools"
./outline.py evidence/ch1/numt_methods.md --job "Compare NUMT detection tools" --sections 3

# 7. Write your paragraph yourself (in your editor / Google Docs)

# 8. Critique your draft — paragraph by paragraph
./critique.py drafts/ch1_para_3.md --job "Compare NUMT detection tools"
./critique.py drafts/ch1_para_3.md --job "..." --diff       # sentence-anchored

# 9. When the chapter is assembled, run the pre-submission gauntlet
./coherence.py drafts/chapter1.md --thesis "NUMT filtering is mandatory in clinical mtDNA"
./paraphrase_check.py drafts/chapter1.md --threshold 0.85
./audit.py drafts/chapter1.md --bib bib/thesis.bib
./verify.py drafts/chapter1.md --bib bib/thesis.bib
```

## Architecture

### RAG Research
```
Index:  Zotero API → ZOTERO_STORAGE PDFs → pdfplumber → text
        → chunk (800 char, 200 overlap, sentence-boundary aware)
        → litellm embedding (text-embedding-3-small, 1536 dims)
        → ChromaDB (cosine similarity, persistent on disk)

Query:  question → embed → ChromaDB top-k → deduplicate (max 3 chunks/source)
        → context + system prompt → common.ask_model()
        → bulleted answer with [@citekey] citations

Compare:  same RAG context → parallel ThreadPoolExecutor calls
          → side-by-side Rich table (CLI) or card grid (web UI)
```

### PaperForge Multi-Agent Pipeline
```
Code/Review → LangGraph StateGraph → 7-agent pipeline
              │
              ├─ Code Analyst (Gemini CLI)     or Literature Researcher (OpenAlex + DuckDuckGo)
              ├─ Writer (DeepSeek API)          → cleanup_prose() post-processing
              ├─ Assessor (Claude CLI)          → _extract_json() brace-matching parser
              ├─ Rewriter (Claude CLI)          ↻ up to 3× until score ≥ 7
              ├─ Plagiarism Check (DeepSeek API) → report-only, no loop
              ├─ Figure Gen (Gemini CLI)         ↻ up to 3× until PASS
              └─ Figure Supervisor (Claude CLI)

Bridge:  Claude → claude CLI (shell=False, list args)
         DeepSeek → direct HTTP API (OpenAI-compatible /v1/chat/completions)
         Gemini → gemini CLI (--approval-mode plan, no tool execution)
         Fallback chain: claude → deepseek → gemini
```

Every model call is logged to `~/thesis/logs/YYYY-MM-DD.jsonl` with timestamp, model, prompt, response, and cost — ready for AI-usage disclosure.

## Logging & AI Disclosure

All model calls (every script, every model) append one JSON line to `~/thesis/logs/YYYY-MM-DD.jsonl`:

```json
{"timestamp": "2026-05-19T14:30:00+00:00", "model_alias": "claude", "model_full": "anthropic/claude-opus-4-7", "prompt": "...", "response": "...", "input_tokens": 1200, "output_tokens": 400}
```

For venues requiring AI-usage disclosure, use the `/ars-disclosure` command if the academic-research-skills plugin is installed, or generate your own from these logs.

## FAQ

**Q: Do I need all model provider API keys?**
No. Only set the keys for providers you plan to use. At minimum, have one key.

**Q: How long does indexing take?**
~5-10 seconds per paper (text extraction + embedding). 100 papers ≈ 10 minutes.

**Q: Can I index without Zotero?**
Currently, no. The indexer uses the Zotero API for metadata (authors, citekeys, DOIs). PDF-only indexing could be added.

**Q: What if a PDF has no extractable text?**
Scanned/image-only PDFs are skipped with a warning. Use OCR first.

**Q: Can I use a local embedding model?**
Yes. Change `DEFAULT_EMBED_MODEL` in `researcher.py` to `"ollama/nomic-embed-text"` or any LiteLLM-supported embedding model.

**Q: How do I update the index after adding new papers to Zotero?**
Run `./researcher.py index` again. Already-indexed papers are skipped (checked by Zotero item key). Use `--force` to re-index everything.
