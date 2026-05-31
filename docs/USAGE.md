# Research Assistant — Usage Guide

## Daily Workflow

### Start or reopen

```bash
ra
```

Your browser opens at `http://127.0.0.1:5050`. If the server was already running, it just reopens the browser.

### Stop

```bash
ra stop
```

### The simple rule

Type `ra` to start or reopen. Type `ra stop` to stop. That's all you need every day.

Key behaviors:
- **Closing the browser does not stop the app.** The server keeps running in the background.
- **Closing the terminal does not stop the app.** The server runs detached via nohup.
- **After restarting your computer, type `ra` again** to start fresh.
- **If the app is already running, `ra` reopens your browser** — no duplicate servers.

## Installation

### First time setup

```bash
git clone https://github.com/femrebora/research-assistant
cd research-assistant
bash scripts/setup.sh
bash scripts/install_cli.sh
source ~/.bashrc
```

### What gets installed

| Item | Location |
|------|----------|
| research-assistant command | `~/.local/bin/research-assistant` |
| ra alias | `~/.bashrc` (alias ra="research-assistant") |
| PATH entry | `~/.bashrc` (export PATH="$HOME/.local/bin:$PATH") |
| Virtual environment | `~/.venvs/thesis` |
| Project workspace | `~/thesis` (configurable via THESIS_ROOT) |

### Reinstalling or updating

The installer is safe to run multiple times:

```bash
bash scripts/install_cli.sh
```

It won't duplicate PATH entries or aliases.

## Commands

### Daily commands

| Command | What it does |
|---------|-------------|
| `ra` | Start or reopen Research Assistant |
| `ra stop` | Stop the background server |

### Alternative full command

| Command | What it does |
|---------|-------------|
| `research-assistant` | Same as `ra` (start or reopen) |
| `research-assistant stop` | Same as `ra stop` |

### Advanced commands

| Command | What it does |
|---------|-------------|
| `research-assistant restart` | Stop and start again |
| `research-assistant status` | Show server status (running/stopped, PID, uptime) |
| `research-assistant logs` | View last 50 log lines |
| `research-assistant logs -n 100` | View last 100 log lines |
| `research-assistant logs -f` | Follow logs live (Ctrl+C to exit) |
| `research-assistant doctor` | Run system diagnostics (safe — no secrets) |
| `research-assistant doctor --export` | Export diagnostics as text |
| `research-assistant open` | Open browser without starting server |
| `research-assistant config` | Show configuration paths |

## npm

If you prefer npm:

```bash
npm run setup          # First time setup
npm run start          # Start or reopen
npm run stop           # Stop
npm run restart        # Restart
npm run status         # Server status
npm run logs           # View logs
npm run doctor         # Diagnostics
npm run install-cli    # Install CLI command
```

## Python directly

If you prefer the Python virtual environment directly:

```bash
source ~/.venvs/thesis/bin/activate
ra-web                 # Start Flask in foreground (Ctrl+C to stop)
```

## Desktop launcher (optional)

```bash
bash scripts/install_desktop_launcher.sh
```

Creates a "Research Assistant" entry in your application menu. Clicking it starts the server and opens the browser.

## Where things are saved

| What | Where |
|------|-------|
| Server PID | `~/.local/share/research-assistant/research-assistant.pid` |
| Server logs | `~/.local/share/research-assistant/research-assistant.log` |
| Model usage logs | `~/thesis/logs/YYYY-MM-DD.jsonl` |
| Research sessions | `~/thesis/research_sessions/` |
| Vector index | `~/thesis/chroma_db/` |
| Project files | `~/thesis/projects/<slug>/` |
| Environment (.env) | `project/.env` |

## Configuring providers

### From the Web UI

1. Open `http://127.0.0.1:5050/settings`
2. Add your API keys (Anthropic, Gemini, DeepSeek, OpenAI)
3. Click Save
4. Go to `http://127.0.0.1:5050/providers`
5. Click "▷ Test" next to each model alias

### Configuration reference

#### API providers

| Setting | Description |
|---------|-------------|
| ANTHROPIC_API_KEY | Claude models via Anthropic API |
| GEMINI_API_KEY | Gemini models via Google API |
| DEEPSEEK_API_KEY | DeepSeek models |
| OPENAI_API_KEY | GPT models via OpenAI API |

#### CLI providers (subscription-based)

| Setting | Default | Description |
|---------|---------|-------------|
| CLAUDE_CLI_CMD | `claude -p` | Claude CLI command |
| GEMINI_CLI_CMD | `gemini -p` | Gemini CLI command |
| CODEX_CLI_CMD | `codex exec` | Codex CLI command |
| OLLAMA_CLI_CMD | `ollama run llama3.3` | Ollama local model |
| CLI_TIMEOUT | `600` | Seconds before CLI call is killed |

#### Zotero

| Setting | Description |
|---------|-------------|
| ZOTERO_USER_ID | Numeric user ID from zotero.org/settings/keys |
| ZOTERO_API_KEY | API key from zotero.org/settings/keys |
| ZOTERO_STORAGE | Path to Zotero storage folder (e.g. ~/Zotero/storage) |

#### Paper Discovery

| Setting | Description |
|---------|-------------|
| OPENALEX_EMAIL | Email for OpenAlex polite pool (optional) |
| SEMANTIC_SCHOLAR_API_KEY | API key for higher rate limits (optional) |
| ELICIT_API_KEY | Required for Elicit (paid plan) |

## Fixing "No results found" in Library Search

1. Go to `http://127.0.0.1:5050/settings`
2. Set `ZOTERO_STORAGE` to your Zotero storage path
   - Both `~/Zotero/storage` and `/home/you/Zotero/storage` work
3. Run `ra doctor` to verify the path exists and PDFs are found
4. For Zotero API metadata search, also set ZOTERO_USER_ID and ZOTERO_API_KEY
5. Go to `http://127.0.0.1:5050/library-search?q=keyword` to test

## Fixing "No results found" after indexing

1. Go to `http://127.0.0.1:5050/index-setup`
2. Check the diagnostics panel:
   - Is ZOTERO_STORAGE resolved correctly?
   - Does the path exist?
   - How many subfolders and PDFs are found?
   - Is the index built?
3. Click "Rebuild index" if needed
4. Increase the similarity threshold from `/settings` if results are too strict
5. Try broadening your search query

## Using Paper Discovery

1. Go to `http://127.0.0.1:5050/paper-discovery`
2. Check the Source Status badges at the top:
   - OpenAlex: always available (no key required)
   - Semantic Scholar: works without key, better with one
   - Elicit: requires API key
3. Choose a tab and search

## Using PaperForge

PaperForge generates academic paper drafts from codebases or research topics.

1. Go to `http://127.0.0.1:5050/paperforge`
2. Follow the 6-step wizard: Input → Generate → Edit → Figures → Assess → Finalize

## Continuing previous work

When you type `ra`, you return to exactly where you left off:
- **Sessions**: Browse, review, and delete saved Q&A at `/sessions`
- **Workspace**: Continue editing project files at `/workspace`
- **Projects**: Check or change the active project at `/projects`

## Safe use and backup

Do not commit these to a public repository:
- `.env` (contains API keys)
- `~/thesis/` (contains your research work)
- Zotero PDFs and storage

Recommended backup:

```bash
tar -czf thesis-backup-$(date +%Y%m%d).tar.gz ~/thesis
```

## Troubleshooting

### ra command not found

```bash
bash scripts/install_cli.sh
source ~/.bashrc
```

### Server won't start

```bash
ra doctor          # Run diagnostics
ra logs            # Check server logs
ra restart         # Try restarting
```

### Port 5050 already in use

```bash
ra status                         # Check what's running
RA_PORT=5051 ra                   # Use a different port
```

### Provider test fails with GPT-5

Some GPT-5 models don't support temperature=0. The test handler automatically uses temperature=1 for GPT-5 family models. If you still get errors, check your API key and account status.

### Zotero path not found

Make sure ZOTERO_STORAGE points to a folder that **contains subfolders with PDFs**. The typical Zotero structure is:

```
~/Zotero/storage/
├── ABC12345/
│   └── paper.pdf
├── DEF67890/
│   └── another.pdf
```

Not a single folder of PDFs directly in storage.
