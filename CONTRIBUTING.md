# Contributing

## Setup

```bash
git clone <repo-url>
cd research-assistant

# Create venv and install in editable mode
bash scripts/setup.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,desktop]"
```

## Run the app

```bash
source .venv/bin/activate
python -m research_assistant.web.app
# or: flask --app research_assistant.web.app run --port 5050 --debug
```

## Run tests

```bash
pytest tests/ -q            # full suite (~329 tests)
pytest tests/ -x -v         # stop on first failure, verbose
pytest tests/web/ -v        # web tests only
```

## Lint

```bash
ruff check .                # check all files
ruff check --fix .          # auto-fix where possible
ruff format .               # format (if using ruff format)
```

## Commit conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

<optional body>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`

Examples:
- `fix: add logging to silent exception handlers in web app`
- `feat: dynamic path resolution for Zotero storage`
- `test: add Flask test-client route smoke tests`
- `docs: add ARCHITECTURE.md and FAQ`

## Project structure

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for a module map and data flow diagrams.

## Design principles

- **Local-first.** No cloud dependency beyond model provider APIs.
- **Flask + HTMX.** Server-rendered HTML, minimal JavaScript. No SPA.
- **Immutable data patterns.** Prefer frozen dataclasses and new objects over mutation.
- **Explicit error handling.** Log the cause, surface a user-visible message, never silently swallow.
- **Surgical .env writes.** Settings changes preserve comments, blanks, and untouched keys.
- **Test driven.** Write tests first. Target 80%+ coverage. Mock external calls so the suite runs offline.
