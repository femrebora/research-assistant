# Architecture

## Module map

```
research_assistant/
├── __init__.py              # Loads .env, sets up logging
├── common.py                # Shared constants: MODELS, THESIS_ROOT, ask_model
├── cli.py                   # Click CLI entry points (ra-ask, ra-researcher, etc.)
├── researcher.py            # RAG engine: indexing, querying, session management
│
├── rag/
│   └── embedding.py         # Text embedding via LiteLLM (any provider)
│
├── web/
│   ├── app.py               # Flask application (~39 routes, ~1400 lines)
│   ├── settings_store.py    # .env read/write with secret protection
│   ├── providers.py         # Provider health checks and test endpoint
│   ├── tool_runner.py       # Generic Click-tool dispatch from web forms
│   ├── templates/           # Jinja2 templates (31 files)
│   │   ├── base.html        # Shell: sidebar, theme, panel
│   │   ├── macros/ui.html   # Reusable components (card, alert, empty_state, …)
│   │   ├── ask_library.html # RAG Q&A with tabbed interface
│   │   ├── settings.html    # .env editor (design-token themed)
│   │   ├── providers.html   # API/CLI provider health dashboard
│   │   ├── index_setup.html # Step-by-step Zotero and index wizard
│   │   └── …                # Feature pages (projects, compare, peer-review, …)
│   └── static/
│       ├── style.css        # Design tokens, component classes (~1300 lines)
│       └── app.js           # Theme toggle, tabs, control panel, debounce
│
├── workspace/
│   ├── library.py           # Zotero API + local PDF search and listing
│   ├── projects.py          # Project CRUD and active-project tracking
│   ├── editor.py            # Three-pane workspace editor
│   ├── document.py          # Draft document management
│   ├── defense.py           # Thesis defense Q&A simulator
│   ├── peer_review.py       # Multi-model AI peer review
│   ├── prompts_library.py   # Saved prompt templates
│   └── telemetry.py         # AI usage logging and disclosure
│
├── research/
│   ├── discover.py          # Paper discovery (OpenAlex, Semantic Scholar, Elicit)
│   └── compare.py           # Multi-model comparison engine
│
├── writing/
│   └── outline_recommender.py # Outline builder from project metadata
│
└── verification/
    ├── claim_verify.py      # Claim extraction and verification
    ├── paraphrase_check.py  # Near-verbatim paraphrase detection
    ├── originality.py       # Internal + external similarity check
    └── external_match.py    # OpenAlex/Crossref search for verification

scripts/                     # Bash lifecycle management (20 files)
├── research-assistant       # CLI wrapper installed to ~/.local/bin
├── start_web.sh             # Start Flask in background
├── stop_web.sh              # Graceful shutdown
├── restart_web.sh           # Stop + start
├── status.sh                # Server status (PID, port, health)
├── logs.sh                  # Log viewer
├── doctor.sh                # System diagnostics (no secrets)
├── setup.sh                 # One-command venv + pip install
├── install_cli.sh           # Install the `research-assistant` command
└── install_desktop_launcher.sh  # .desktop file for pywebview

agentic/                     # PaperForge multi-agent pipeline (optional)
tests/                       # pytest suite (~329 tests, 35 files)
```

## Data flow

### RAG Q&A ("Ask Library")

```
User question
  → app.py: ask_library()
    → researcher.py: ask_research_question()
      → chroma_dir() / _get_collection()    [ChromaDB vector store]
      → _embed_single(question)             [LiteLLM embedding]
      → collection.query(…)                 [vector similarity search]
      → ask_model(question + context)       [LiteLLM chat completion]
      → return answer with source citations
```

### Indexing

```
User clicks "Build index"
  → POST /index/start
    → _run_index_in_background() thread
      → index_zotero_papers() or index_local_pdfs()
        → Zotero API (pyzotero) or local PDF scan
        → pdfplumber text extraction
        → text chunking (800-char, 200-char overlap)
        → LiteLLM embedding
        → ChromaDB persistent storage
  → GET /index/status polls progress
```

### Provider test

```
User clicks "▷ claude"
  → POST /providers/test
    → providers.py: test_provider()
      → ask_model("hello", model=alias, max_tokens=16)
      → return timing, token count, success/error
  → HTMX swaps result into the provider card
```

### Settings save

```
User edits settings → clicks "Save changes"
  → POST /settings
    → settings_store.py: validate(updates)
      → reject non-editable keys
      → reject secret writes on non-loopback RA_HOST
      → validate numeric fields
    → settings_store.py: save(clean)
      → read .env, update matching lines, append new keys
      → write back, set os.environ
      → return success/error flash message
```

## Where files live

| What | Where |
|------|-------|
| Project files & drafts | `$THESIS_ROOT/projects/<slug>/` |
| Vector index | `$THESIS_ROOT/chroma_db/` |
| Saved Q&A sessions | `$THESIS_ROOT/research_sessions/` |
| AI usage logs | `$THESIS_ROOT/logs/YYYY-MM-DD.jsonl` |
| Cached API responses | `$THESIS_ROOT/cache/` |
| PID file | `$XDG_DATA_HOME/research-assistant/research-assistant.pid` |
| Server log | `$XDG_DATA_HOME/research-assistant/research-assistant.log` |
| User config | `.env` (project root, copied from env.example) |
| CLI wrapper | `~/.local/bin/research-assistant` |

## Key design decisions

- **Local-first.** Everything runs on your machine. No cloud dependency beyond the model provider APIs you choose to configure.
- **Flask + HTMX.** Server-rendered HTML with minimal JavaScript. HTMX handles partial updates. No SPA framework.
- **LiteLLM abstraction.** One interface for all model providers. Swap models by changing an env var or model alias.
- **ChromaDB persistence.** Vector index stored on disk under your thesis workspace. Survives restarts.
- **Surgical .env writes.** Settings changes update individual keys in place. Comments, blank lines, and untouched secrets are preserved.
- **Design tokens.** CSS custom properties (`--color-surface`, `--color-primary`, …) support light and dark themes with a single stylesheet.
- **Loopback-only secret editing.** API keys can be set from the Settings UI when the server is on localhost, but not when exposed on a network.
