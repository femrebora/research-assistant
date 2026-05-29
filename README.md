# research-assistant

[![python](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-A3E635)](LICENSE)
[![flask](https://img.shields.io/badge/web%20UI-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![models](https://img.shields.io/badge/models-Claude%20%7C%20Gemini%20%7C%20DeepSeek%20%7C%20GPT--5-7C3AED)](#supported-models)

An AI-powered research toolkit for thesis writing. Ask questions against your Zotero library, compare answers across models, generate paper outlines, run peer reviews, simulate your defense, and generate full papers from code or topics — all through a **Flask web UI** or **CLI**.

---

## What can it do?

| You want to... | Use this |
|---|---|
| Ask questions about your papers with citations | **Ask** — RAG over your Zotero-indexed PDFs |
| See how different models answer the same question | **Compare** — side-by-side multi-model answers |
| Generate a structured paper outline with evidence | **Outline Recommender** — paper-type aware, evidence-mapped |
| Get a critique of your draft section | **Critique** — structural and argument feedback |
| Check your paper for AI-generated patterns | **AI Score** — 7 mechanical checks, no LLM calls |
| Run a full peer review before submission | **Peer Review** — parallel structural/methodology/citation reviewers |
| Simulate your thesis defense with examiner personas | **Defense** — 5 examiner types ask jury questions |
| Generate a complete paper from your code | **PaperForge** — 7-agent pipeline, code → paper |
| Generate a review article from a topic | **PaperForge Review** — autonomous web research → review |
| Check originality against external databases | **Originality** — internal + OpenAlex / Crossref |
| Audit your citations | **Citation Audit** — citekey resolution, support audit |
| Generate an AI-usage disclosure statement | **Disclosure** — venue-ready statement |
| Find papers outside your library | **Discover** — OpenAlex / Semantic Scholar / Elicit |
| Manage per-project context | **Projects** — title, research question, hypothesis, citation style |

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/femrebora/research-assistant
cd research-assistant
./setup.sh
```

This creates a virtualenv at `~/.venvs/thesis` and installs the package.

### 2. Add your API keys

```bash
cp env.example .env   # if setup.sh didn't already
```

Edit `.env` and set **at least one** model provider:

```bash
ANTHROPIC_API_KEY=sk-ant-...
# or
GEMINI_API_KEY=...
# or
DEEPSEEK_API_KEY=sk-...
# or
OPENAI_API_KEY=sk-...
```

### 3. Activate and launch

```bash
source ~/.venvs/thesis/bin/activate
ra-web                 # → http://127.0.0.1:5050
```

That's it. The dashboard shows index stats, a quick-ask box, and links to every tool.

---

## Web UI tour

The web UI at `http://127.0.0.1:5050` has these pages:

### Core research

| Page | Route | What it does |
|---|---|---|
| **Dashboard** | `/` | Index stats, quick-ask, active project banner, recent sessions |
| **Ask** | `/ask` | RAG-backed Q&A against your indexed papers with citations |
| **Compare** | `/compare` | Same question answered by multiple models side-by-side |
| **Sessions** | `/sessions` | Browse, view, and delete saved Q&A sessions |

### Writing tools

| Page | Route | What it does |
|---|---|---|
| **Outline Recommender** | `/outline-recommender` | Generates a structured outline with evidence mapping, pre-filled from your active project. Supports empirical, review, methods, case-study, and theoretical paper types |
| **Tools** | `/tools/<name>` | Form-based access to all 18 CLI tools: outline, critique, critic, paraphrase, paraphrase-check, coherence, audit, verify, claim-verify, originality, disclose, evidence, ideas, zot, discover, pipeline, single-ask |

### Project management

| Page | Route | What it does |
|---|---|---|
| **Projects** | `/projects` | Create and manage per-project context (title, research question, hypothesis, keywords, citation style, supervisor notes) |
| **Activate** | `/projects/<slug>/activate` | Set the active project — its context is injected into peer review, defense, and the outline recommender |

### Review & defense

| Page | Route | What it does |
|---|---|---|
| **Peer Review** | `/peer-review` | Structural, methodology, and citation reviewers run in parallel across multiple models, then synthesize a prioritized revision plan |
| **Defense** | `/defense` | Generates jury questions from 5 examiner personas: friendly supervisor, strict external reviewer, methodology examiner, statistics examiner, field expert |

### PaperForge — Multi-agent paper generation

| Page | Route | What it does |
|---|---|---|
| **PaperForge** | `/paperforge` | **Code → Paper**: 7 specialized agents generate a full academic paper from your codebase |
| **PaperForge Review** | `/paperforge` (review mode) | **Topic → Review Article**: autonomous web research via OpenAlex + DuckDuckGo |

How the pipeline works:

```
Codebase → Code Analyst → Writer → Assessor → Rewriter (loops ≤3×)
                                              → Plagiarism Check
                                              → Figure Gen → Supervisor
```

For review mode, `Code Analyst` becomes `Literature Researcher` which searches the web autonomously. All progress streams live via SSE.

### Workspace & orchestration

| Page | Route | What it does |
|---|---|---|
| **Workspace** | `/workspace` | Full-text editor with per-project file management, undo, and save |
| **Orchestration** | `/orchestration` | Model usage dashboard: per-model calls, tokens, cost, daily spend sparkline |
| **Prompt Library** | `/prompts` | 10 curated prompts across 10 academic categories. One-click copy or send-to-Ask |
| **Index** | `/index` | Background Zotero PDF indexing with live progress |

---

## CLI reference

All 18 tools are available from the terminal too. Run any with `--help`.

### Ask & search

| Command | What it does |
|---|---|
| `ra-ask "question"` | Single-model Q&A |
| `ra-compare "question"` | Multi-model comparison |
| `ra-researcher ask "question"` | RAG question with cited answer |
| `ra-researcher index` | Index Zotero PDFs for RAG |
| `ra-zot "query"` | Search your Zotero library |
| `ra-discover "topic"` | Find papers via OpenAlex / Semantic Scholar |
| `ra-evidence "claim"` | PaperQA2 cited evidence query |

### Writing & outlining

| Command | What it does |
|---|---|
| `ra-outline "topic"` | Section outline with citation stubs |
| `ra-outline-recommender "topic"` | Paper-type-aware outline with evidence mapping |
| `ra-ideas "topic"` | Paragraph angles from evidence |
| `ra-critique file.md` | Draft critique with structural feedback |
| `ra-critic file.md` | Writer + critic pipeline |
| `ra-paraphrase file.md` | Writer → paraphraser → checker pipeline |
| `ra-coherence chapter/` | Chapter coherence analysis |

### Verification & audit

| Command | What it does |
|---|---|
| `ra-audit file.md` | Citation audit |
| `ra-verify file.md` | Citekey resolution against .bib |
| `ra-claim-verify file.md` | Semantic per-claim support audit |
| `ra-originality file.md` | Originality check (internal + OpenAlex / Crossref) |
| `ra-disclose` | AI-usage disclosure statement |
| `ra-pipeline` | Full end-to-end orchestrator |

### PaperForge CLI

```bash
# Generate a paper from a codebase
./run_agentic.py /path/to/project --summary "What it does" --output /tmp/paper

# Generate a review article (autonomous web research)
./run_review.py --topic "CRISPR-Based Therapeutics: Delivery Methods"

# Check a paper for AI-generated patterns
./quick_ai_score.py paper.md --json
```

---

## Zotero integration (optional)

For RAG-backed Q&A, connect your Zotero library:

```bash
# In your .env file:
ZOTERO_USER_ID=1234567
ZOTERO_API_KEY=...
ZOTERO_STORAGE=/home/you/Zotero/storage
THESIS_ROOT=/home/you/thesis          # default: ~/thesis
```

Then index from the web UI (`/index`) or CLI:

```bash
ra-researcher index
```

Already-indexed papers are skipped. Use `--force` to re-index everything. Indexing takes ~5-10 seconds per paper.

---

## Supported models

| Alias | Model | Input $/1M | Output $/1M |
|---|---|---|---|
| `claude` | Claude Opus 4.7 | $15.00 | $75.00 |
| `sonnet` | Claude Sonnet 4.6 | $3.00 | $15.00 |
| `haiku` | Claude Haiku 4.5 | $0.80 | $4.00 |
| `gemini` | Gemini 2.5 Pro | $1.25 | $5.00 |
| `flash` | Gemini 2.5 Flash | $0.075 | $0.30 |
| `deepseek` | DeepSeek Chat | $0.27 | $1.10 |
| `gpt` | GPT-5 | $1.25 | $10.00 |
| `gpt-mini` | GPT-5 Mini | $0.15 | $0.60 |
| `local` | Ollama (configurable) | $0.00 | $0.00 |

CLI-subscription aliases (`claude-cli`, `gemini-cli`, `codex-cli`, `ollama-cli`) are also supported — see `common.py`.

---

## FAQ

**Do I need all API keys?** No. One provider is enough. PaperForge works best with 2-3 (it uses different models for different agents).

**How long does indexing take?** ~5-10 seconds per paper. Already-indexed papers are skipped automatically.

**Can I use a local embedding model?** Yes. Change `DEFAULT_EMBED_MODEL` in `researcher.py` to `"ollama/nomic-embed-text"`.

**How do I update the index?** Run indexing again — it skips already-indexed papers by Zotero item key. Use `--force` to re-index everything.

**Where are model call logs stored?** `~/thesis/logs/` — useful for disclosure statements.

**What's a typical PaperForge run cost?** ~$1.50-2.00 per full paper generation.
