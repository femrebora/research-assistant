# research-assistant

[![Python](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-A3E635)](LICENSE)
[![Web UI](https://img.shields.io/badge/web%20UI-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Zotero](https://img.shields.io/badge/Zotero-ready-CC2936?logo=zotero&logoColor=white)](https://www.zotero.org/)
[![Models](https://img.shields.io/badge/models-Claude%20%7C%20Gemini%20%7C%20DeepSeek%20%7C%20GPT%20%7C%20Ollama-7C3AED)](#supported-models)

**research-assistant** is a local first academic research workspace for thesis writing, literature review, Zotero based retrieval, citation aware drafting, model comparison, paper discovery, project organization, and transparent AI assisted research.

It gives you one place to index your own papers, ask cited questions, compare multiple models, organize thesis or manuscript work, generate outlines, audit claims, prepare for defense questions, and keep AI usage logs for disclosure.

## Why this exists

Academic AI tools are useful, but they often separate the work into too many places: papers in Zotero, notes in another app, prompts in a browser, drafts in a document editor, citations somewhere else, and AI usage logs nowhere.

**research-assistant** is built to make that workflow more organized:

<table>
  <thead>
    <tr>
      <th>Problem</th>
      <th>How research-assistant helps</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Your papers are scattered</td>
      <td>Index local Zotero PDFs and ask questions over your own library.</td>
    </tr>
    <tr>
      <td>AI answers are hard to trust</td>
      <td>Use citation aware retrieval, claim verification, and citation auditing.</td>
    </tr>
    <tr>
      <td>Different models give different answers</td>
      <td>Compare Claude, Gemini, DeepSeek, GPT, Ollama, and CLI routed models.</td>
    </tr>
    <tr>
      <td>Thesis work becomes messy</td>
      <td>Keep projects, sessions, drafts, evidence, notes, logs, and exports in one workspace.</td>
    </tr>
    <tr>
      <td>AI disclosure is easy to forget</td>
      <td>Save model usage logs and generate disclosure text for thesis or manuscript workflows.</td>
    </tr>
  </tbody>
</table>

## Main features

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>What it does</th>
      <th>Best for</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Zotero RAG</strong></td>
      <td>Indexes local Zotero PDFs and retrieves relevant paper chunks.</td>
      <td>Evidence based questions over your own literature library.</td>
    </tr>
    <tr>
      <td><strong>Ask Library</strong></td>
      <td>Ask cited questions with RAG, ask without context, or compare models.</td>
      <td>Daily thesis and literature review questions.</td>
    </tr>
    <tr>
      <td><strong>Paper discovery</strong></td>
      <td>Search OpenAlex, Semantic Scholar, and Elicit when configured.</td>
      <td>Finding new papers beyond your Zotero library.</td>
    </tr>
    <tr>
      <td><strong>Writing Studio</strong></td>
      <td>Generate paragraph angles, outlines, critiques, paraphrases, and coherence checks.</td>
      <td>Academic drafting and revision.</td>
    </tr>
    <tr>
      <td><strong>Project workspace</strong></td>
      <td>Stores project title, research question, hypothesis, keywords, citation style, discipline, and supervisor notes.</td>
      <td>Keeping each thesis, manuscript, or review project separate.</td>
    </tr>
    <tr>
      <td><strong>Workspace editor</strong></td>
      <td>Edit project documents, apply AI assisted revisions, select source PDFs, and undo changes.</td>
      <td>Continuing long writing work without losing context.</td>
    </tr>
    <tr>
      <td><strong>Peer review simulation</strong></td>
      <td>Runs structural, methodological, and citation focused review passes.</td>
      <td>Finding weaknesses before supervisor review or submission.</td>
    </tr>
    <tr>
      <td><strong>Defense preparation</strong></td>
      <td>Generates questions from different examiner personas.</td>
      <td>Preparing for thesis defense and project presentations.</td>
    </tr>
    <tr>
      <td><strong>Claim verification</strong></td>
      <td>Checks whether draft claims are supported by retrieved evidence.</td>
      <td>Reducing unsupported claims and citation mistakes.</td>
    </tr>
    <tr>
      <td><strong>PaperForge</strong></td>
      <td>Multi agent workflow for creating academic paper drafts from a topic or codebase.</td>
      <td>Research software papers, review drafts, and structured manuscript prototypes.</td>
    </tr>
    <tr>
      <td><strong>AI disclosure</strong></td>
      <td>Logs model usage and helps generate transparent AI use statements.</td>
      <td>Thesis, journal, conference, and institutional transparency requirements.</td>
    </tr>
  </tbody>
</table>

## Quick start

```bash
git clone https://github.com/femrebora/research-assistant.git
cd research-assistant
bash scripts/setup.sh
bash scripts/install_cli.sh
research-assistant
```

The Web UI opens at:

```text
http://127.0.0.1:5050
```

The setup script creates a Python virtual environment, installs the package in editable mode, creates `.env` from `env.example`, and prepares default local folders.

The CLI installer adds a `research-assistant` wrapper to:

```text
~/.local/bin/research-assistant
```

It does not modify your shell configuration automatically.

## Daily commands

After installation, this is usually all you need:

```bash
research-assistant          # Start the app or reopen it in the browser
research-assistant stop     # Stop the background server
research-assistant doctor   # Diagnose setup, paths, and common problems
```

Optional shortcut:

```bash
alias ra="research-assistant"
```

Then you can use:

```bash
ra
ra stop
ra doctor
```

Full command reference:

```bash
research-assistant          # Start or reopen
research-assistant stop     # Stop the background server
research-assistant restart  # Stop and start again
research-assistant status   # Show server status
research-assistant logs     # Show recent logs
research-assistant logs -f  # Follow logs live
research-assistant doctor   # Run diagnostics
research-assistant open     # Open browser without starting the server
research-assistant config   # Show project, log, PID, env, and URL paths
```

## Requirements

<table>
  <thead>
    <tr>
      <th>Requirement</th>
      <th>Why it is needed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Python 3.11 or newer</td>
      <td>Main application runtime.</td>
    </tr>
    <tr>
      <td>Git</td>
      <td>Clone and update the repository.</td>
    </tr>
    <tr>
      <td>Bash compatible shell</td>
      <td>Run setup and helper scripts.</td>
    </tr>
    <tr>
      <td>Zotero</td>
      <td>Recommended for citation aware Q&amp;A over your own PDF library.</td>
    </tr>
    <tr>
      <td>At least one model provider</td>
      <td>Use Anthropic, Gemini, DeepSeek, OpenAI, Ollama, or CLI routed providers.</td>
    </tr>
  </tbody>
</table>

You do not need every API key. One working model provider is enough to start.

## First run checklist

Open the Web UI and complete these steps in order:

<table>
  <thead>
    <tr>
      <th>Step</th>
      <th>Page</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><code>/settings</code></td>
      <td>Add at least one API key or configure a CLI provider.</td>
    </tr>
    <tr>
      <td>2</td>
      <td><code>/providers</code></td>
      <td>Test each model alias you want to use.</td>
    </tr>
    <tr>
      <td>3</td>
      <td><code>/settings</code></td>
      <td>Set <code>THESIS_ROOT</code>, <code>ZOTERO_STORAGE</code>, Zotero user ID, and Zotero API key if needed.</td>
    </tr>
    <tr>
      <td>4</td>
      <td><code>/index-setup</code></td>
      <td>Check Zotero path diagnostics and index your PDFs.</td>
    </tr>
    <tr>
      <td>5</td>
      <td><code>/projects</code></td>
      <td>Create your active thesis, manuscript, or review project.</td>
    </tr>
    <tr>
      <td>6</td>
      <td><code>/ask-library</code></td>
      <td>Ask a small test question and confirm that retrieval and citations work.</td>
    </tr>
  </tbody>
</table>

## Configuration

**You do not need every key.** One working model provider is enough to start. All others are optional.

### Quick setup (30 seconds)

```bash
cp env.example .env
# Edit .env with your editor — add at least one API key:
nano .env
```

Then start the app and open `/settings` to configure the rest from the browser:

```text
http://127.0.0.1:5050/settings
```

### Two ways to configure

| Method | Best for |
|--------|----------|
| **Web UI** (`/settings`) | Paths, CLI commands, timeouts, checking what's configured |
| **Edit `.env` directly** | API keys (never shown in browser), bulk edits, initial setup |

Changes to paths, CLI commands, and timeouts take effect after restarting the app. API keys are read at startup.

### Complete variable reference

#### Required — at least one

| Variable | What it does | Where used |
|----------|-------------|------------|
| `ANTHROPIC_API_KEY` | Claude models via Anthropic API | Ask, Compare, Writing tools, PaperForge |
| `GEMINI_API_KEY` | Gemini models via Google API | Ask, Compare, Writing tools, PaperForge |
| `DEEPSEEK_API_KEY` | DeepSeek models | Ask, Compare, Writing tools, PaperForge |
| `OPENAI_API_KEY` | GPT models via OpenAI API | Ask, Compare, Writing tools, PaperForge |

#### Paths

| Variable | Default | What it does |
|----------|---------|-------------|
| `THESIS_ROOT` | `~/thesis` | Main workspace. Logs, sessions, index, exports, and project files are stored here. |
| `ZOTERO_STORAGE` | _(none)_ | Path to Zotero's local storage folder containing PDF attachments. Required for indexing and RAG. |
| `THESIS_DOCS` | Falls back to `THESIS_ROOT` | Additional folder of PDFs included in library searches. |

**Examples:**

```bash
THESIS_ROOT=/home/username/thesis
ZOTERO_STORAGE=/home/username/Zotero/storage
```

#### Zotero

| Variable | What it does | Required for |
|----------|-------------|-------------|
| `ZOTERO_STORAGE` | Path to local Zotero PDF attachments | PDF indexing, RAG, and citation-aware Q&A |
| `ZOTERO_USER_ID` | Numeric user ID from zotero.org/settings/keys | Zotero API metadata search and library browsing |
| `ZOTERO_API_KEY` | API key with read access to your Zotero library | Zotero API metadata search and library browsing |

Get your credentials at **[https://www.zotero.org/settings/keys](https://www.zotero.org/settings/keys)**.

**Note:** `ZOTERO_STORAGE` must point to the folder that *contains* the randomly-named subfolders (e.g., `~/Zotero/storage/`), not to one of those subfolders. The typical structure looks like:

```text
~/Zotero/storage/
├── 2J4IK64G/
│   └── paper.pdf
├── 5TFZ9E85/
│   └── another-paper.pdf
└── ...
```

#### Paper Discovery

| Variable | What it does | Required? |
|----------|-------------|-----------|
| `OPENALEX_EMAIL` | Email for OpenAlex polite pool (higher rate limits) | No — OpenAlex works without it |
| `SEMANTIC_SCHOLAR_API_KEY` | API key for higher rate limits on Semantic Scholar | No — works without key at lower limits |
| `ELICIT_API_KEY` | API key for Elicit searches | Yes for Elicit — requires a paid plan |
| `BRAVE_API_KEY` | Web search via Brave Search API (2,000 free queries/month) | No — used by agentic pipeline |

#### CLI-routed providers

| Variable | Default | What it does |
|----------|---------|-------------|
| `CLAUDE_CLI_CMD` | `claude -p` | Command for the `claude-cli` model alias |
| `GEMINI_CLI_CMD` | `gemini -p` | Command for the `gemini-cli` model alias |
| `CODEX_CLI_CMD` | `codex exec` | Command for the `codex-cli` model alias |
| `OLLAMA_CLI_CMD` | `ollama run llama3.3` | Command for the `ollama-cli` model alias |
| `CLI_TIMEOUT` | `600` | Seconds before a CLI model call is killed |

#### Local models (Ollama)

| Variable | Default | What it does |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `ollama/llama3.3` | Model string for the `local` alias (LiteLLM-managed API calls) |

#### Model alias overrides

Override the LiteLLM model string for any alias without editing source code:

```bash
RA_MODEL_CLAUDE=anthropic/claude-opus-4-8
RA_MODEL_SONNET=anthropic/claude-sonnet-4-6
RA_MODEL_GPT=openai/gpt-5
RA_MODEL_GEMINI=gemini/gemini-2.5-pro
RA_MODEL_FLASH=gemini/gemini-2.5-flash
RA_MODEL_LOCAL=ollama/llama3.3
RA_MODEL_DEEPSEEK=deepseek/deepseek-chat
```

Pattern: `RA_MODEL_<ALIAS>=provider/model-name` (uppercase, hyphens become underscores).

#### Web UI

| Variable | Default | What it does |
|----------|---------|-------------|
| `RA_HOST` | `127.0.0.1` | Host the Flask app listens on |
| `RA_PORT` | `5050` | Port the Flask app listens on |
| `RA_BROWSER` | `xdg-open` | Browser command used by `ra open` |
| `FLASK_SECRET_KEY` | Auto-generated | Flask session encryption. Set a fixed value to keep sessions across restarts. |
| `FLASK_DEBUG` | `0` | Set to `1` for hot reload and detailed errors |

#### Miscellaneous

| Variable | Default | What it does |
|----------|---------|-------------|
| `EDITOR` | Falls back to `VISUAL`, then `nano` | Text editor for interactive review loops |
| `ANTHROPIC_AUTH_TOKEN` | Falls back to `ANTHROPIC_API_KEY` | Alternative auth token for Anthropic API |
| `CONTACT_EMAIL` | Falls back to `OPENALEX_EMAIL` | Contact email for external verification tools |
| `SERPAPI_API_KEY` | _(none)_ | Web search via SerpAPI (alternative to Brave) |
| `EMBEDDING_MODEL` | `openai/text-embedding-3-small` | Embedding model for vector index. Set to `ollama/nomic-embed-text` for local. |
| `RA_ENV_FILE` | Auto-detected `.env` | Override path to the `.env` file |

#### PaperForge Server

| Variable | Default | What it does |
|----------|---------|-------------|
| `PF_HOST` | `127.0.0.1` | Host for the PaperForge sub-app |
| `PF_PORT` | `5055` | Port for the PaperForge sub-app |

### Settings page reference

The `/settings` page shows two sections:

1. **API keys & secrets** — green "set" or grey "not set" pills. Values are NEVER shown or editable in the browser.
2. **Editable config** — paths, CLI commands, timeouts. You can edit and save these from the browser.

The following can be checked or edited from `/settings`:

| Setting | Visible at `/settings`? | Editable at `/settings`? |
|---------|------------------------|--------------------------|
| `ANTHROPIC_API_KEY` | ✓ (set/not-set pill) | ✗ (edit in `.env`) |
| `GEMINI_API_KEY` | ✓ (set/not-set pill) | ✗ (edit in `.env`) |
| `DEEPSEEK_API_KEY` | ✓ (set/not-set pill) | ✗ (edit in `.env`) |
| `OPENAI_API_KEY` | ✓ (set/not-set pill) | ✗ (edit in `.env`) |
| `ZOTERO_API_KEY` | ✓ (set/not-set pill) | ✗ (edit in `.env`) |
| `SEMANTIC_SCHOLAR_API_KEY` | ✓ (set/not-set pill) | ✓ (edit and save) |
| `ELICIT_API_KEY` | ✓ (set/not-set pill) | ✓ (edit and save) |
| `BRAVE_API_KEY` | ✓ (set/not-set pill) | ✓ (edit and save) |
| `FLASK_SECRET_KEY` | ✓ (set/not-set pill) | ✗ (edit in `.env`) |
| `THESIS_ROOT` | ✓ (current value) | ✓ (edit and save) |
| `ZOTERO_STORAGE` | ✓ (current value) | ✓ (edit and save) |
| `THESIS_DOCS` | ✓ (current value) | ✓ (edit and save) |
| `ZOTERO_USER_ID` | ✓ (current value) | ✓ (edit and save) |
| `OPENALEX_EMAIL` | ✓ (current value) | ✓ (edit and save) |
| `CLAUDE_CLI_CMD` | ✓ (current value) | ✓ (edit and save) |
| `GEMINI_CLI_CMD` | ✓ (current value) | ✓ (edit and save) |
| `CODEX_CLI_CMD` | ✓ (current value) | ✓ (edit and save) |
| `OLLAMA_CLI_CMD` | ✓ (current value) | ✓ (edit and save) |
| `OLLAMA_MODEL` | ✓ (current value) | ✓ (edit and save) |
| `CLI_TIMEOUT` | ✓ (current value) | ✓ (edit and save) |
| `RA_HOST` | ✓ (current value) | ✓ (edit and save) |
| `RA_PORT` | ✓ (current value) | ✓ (edit and save) |
| `RA_BROWSER` | ✓ (current value) | ✓ (edit and save) |
| `FLASK_DEBUG` | ✓ (current value) | ✓ (edit and save) |
| `EMBEDDING_MODEL` | ✓ (current value) | ✓ (edit and save) |
| `CONTACT_EMAIL` | ✓ (set/not-set pill) | ✓ (edit and save) |
| `EDITOR` | ✓ (current value) | ✓ (edit and save) |

## First time configuration

Follow these steps in order. Each step takes about 1–2 minutes.

### Step 1: Clone and set up

```bash
git clone https://github.com/femrebora/research-assistant.git
cd research-assistant
bash scripts/setup.sh
bash scripts/install_cli.sh
```

The setup script creates a Python virtual environment at `~/.venvs/thesis`, installs the package, and creates placeholder directories. The CLI installer adds the `research-assistant` wrapper to `~/.local/bin/`.

### Step 2: Copy and edit the environment file

```bash
cp env.example .env
```

Edit `.env` with your editor. Add at least one model provider API key:

```bash
# Choose at least one:
ANTHROPIC_API_KEY=sk-ant-your-real-key-here
# or
GEMINI_API_KEY=your-real-gemini-key
# or
DEEPSEEK_API_KEY=sk-your-real-deepseek-key
# or
OPENAI_API_KEY=sk-your-real-openai-key
```

**Never commit `.env` to git.** It is already in `.gitignore`.

### Step 3: Add Zotero settings (if you want citation-aware Q&A)

If you use Zotero, add these to `.env`:

```bash
ZOTERO_STORAGE=/home/username/Zotero/storage
ZOTERO_USER_ID=1234567
ZOTERO_API_KEY=your-zotero-api-key
```

- Find your user ID and create an API key at **[zotero.org/settings/keys](https://www.zotero.org/settings/keys)**
- `ZOTERO_STORAGE` must point to the folder containing your PDF attachment subfolders

### Step 4: Start the Web UI

```bash
research-assistant
```

The browser opens at `http://127.0.0.1:5050`.

### Step 5: Open `/settings`

Check that your API keys show as green "set" pills. Set your thesis workspace path and Zotero storage path. Save changes, then restart:

```bash
research-assistant restart
```

### Step 6: Open `/providers` and test

Test each model alias you plan to use. A green ✓ means the provider works. A red ✗ shows the error message — common fixes are in the troubleshooting section below.

### Step 7: Open `/index-setup` and index Zotero PDFs

The 6-step wizard walks you through: workspace → Zotero storage → credentials → scan → index → test. After indexing, your PDFs are searchable via Ask Library.

### Step 8: Start working

- **Ask Library** (`/ask-library`) — Ask cited questions over your indexed papers
- **Writing Studio** (`/writing-studio`) — Outline, draft, critique, paraphrase
- **Paper Discovery** (`/paper-discovery`) — Search for papers beyond your Zotero library
- **Workspace** (`/workspace`) — Edit project documents with AI assistance
- **PaperForge** (`/paperforge`) — Multi-agent paper drafting workflow

## Tool integration guide

Each tool or provider is documented below with setup instructions, testing steps, and common problems.

### Claude API

| | |
|---|---|
| **What it does** | Powers the `claude`, `sonnet`, and `haiku` model aliases via the Anthropic API. |
| **Env vars needed** | `ANTHROPIC_API_KEY` (required) |
| **Required?** | No — at least one model provider is needed, but it does not have to be Claude. |
| **How to test** | Open `/providers`, click **Test** next to `claude` or `sonnet`. |
| **Common problems** | Key does not start with `sk-ant-` → you may have copied an organizational key instead of a personal one. 403 error → key does not have the right permissions. Rate limit → wait and retry later. |

### Claude CLI

| | |
|---|---|
| **What it does** | Routes prompts through the `claude` CLI binary instead of the API. |
| **Env vars needed** | `CLAUDE_CLI_CMD` (default: `claude -p`) |
| **Required?** | No — only if you want to use the `claude-cli` alias. |
| **How to test** | Open `/providers`, click **Test** next to `claude-cli`. |
| **Common problems** | `claude: command not found` → install Claude Code CLI or check your PATH. CLI timeout → increase `CLI_TIMEOUT` in `/settings`. |

### OpenAI

| | |
|---|---|
| **What it does** | Powers the `gpt` and `gpt-mini` model aliases via the OpenAI API. |
| **Env vars needed** | `OPENAI_API_KEY` (required) |
| **Required?** | No — at least one model provider is needed. |
| **How to test** | Open `/providers`, click **Test** next to `gpt`. |
| **Common problems** | Key does not start with `sk-` → check you copied the full key. Insufficient quota → check your OpenAI billing dashboard. |

### Gemini

| | |
|---|---|
| **What it does** | Powers the `gemini` and `flash` model aliases via the Google Gemini API. |
| **Env vars needed** | `GEMINI_API_KEY` (required) |
| **Required?** | No — at least one model provider is needed. |
| **How to test** | Open `/providers`, click **Test** next to `gemini`. |
| **Common problems** | Key not authorized for Gemini API → enable it in Google AI Studio. 429 rate limit → wait and retry. |

### DeepSeek

| | |
|---|---|
| **What it does** | Powers the `deepseek` model alias. |
| **Env vars needed** | `DEEPSEEK_API_KEY` (required) |
| **Required?** | No — at least one model provider is needed. |
| **How to test** | Open `/providers`, click **Test** next to `deepseek`. |
| **Common problems** | Key not valid → generate a new one in the DeepSeek dashboard. |

### Ollama (local models)

| | |
|---|---|
| **What it does** | Runs models locally through Ollama, both via API (`local` alias) and CLI passthrough (`ollama-cli`). |
| **Env vars needed** | `OLLAMA_MODEL` (default: `ollama/llama3.3`), `OLLAMA_CLI_CMD` (default: `ollama run llama3.3`) |
| **Required?** | No — only if you want to use local models. |
| **How to test** | Open `/providers`, click **Test** next to `local` or `ollama-cli`. Make sure Ollama is running: `ollama serve`. |
| **Common problems** | `Connection refused` → Ollama is not running. Start it with `ollama serve`. Model not found → pull it first: `ollama pull llama3.3`. |

### Zotero

| | |
|---|---|
| **What it does** | Indexes your local Zotero PDFs for retrieval-augmented Q&A, searches metadata via the Zotero API, and enables citation-aware responses. |
| **Env vars needed** | `ZOTERO_STORAGE` (required for indexing), `ZOTERO_USER_ID` + `ZOTERO_API_KEY` (required for API metadata search) |
| **Required?** | No — the app works without Zotero, but Ask Library, Evidence, and Claim Verify are more powerful with it. |
| **How to test** | Open `/index-setup` and step through the wizard. The storage scan shows how many PDFs were found. Open `/library-search` and run a query. Use the **Test Zotero API** button in `/settings` or the index setup wizard. |
| **Common problems** | Zero PDFs found → `ZOTERO_STORAGE` points to the wrong folder. It must be the `storage/` folder containing the random subfolders, not a single paper folder. API key not working → check it has read access and the user ID is numeric. |

### Elicit

| | |
|---|---|
| **What it does** | Searches Elicit for papers via the Paper Discovery page. |
| **Env vars needed** | `ELICIT_API_KEY` (required) |
| **Required?** | No — and requires a paid Elicit plan. |
| **How to test** | Open `/paper-discovery`, select Elicit, and run a search. |
| **Common problems** | 401 error → API key is missing or invalid. 402 error → paid plan required. |

### Semantic Scholar

| | |
|---|---|
| **What it does** | Searches Semantic Scholar for papers via the Paper Discovery page. |
| **Env vars needed** | `SEMANTIC_SCHOLAR_API_KEY` (optional — works without a key at lower rate limits) |
| **Required?** | No. |
| **How to test** | Open `/paper-discovery`, select Semantic Scholar, and run a search. |
| **Common problems** | Rate limited → add a free API key from semanticscholar.org/product/api for higher limits. |

### OpenAlex

| | |
|---|---|
| **What it does** | Searches OpenAlex for papers via the Paper Discovery page. Always available — no key required. |
| **Env vars needed** | `OPENALEX_EMAIL` (optional — adds you to the polite pool for higher rate limits) |
| **Required?** | No — OpenAlex works without any configuration. |
| **How to test** | Open `/paper-discovery`, select OpenAlex, and run a search. |
| **Common problems** | Rate limited → add your email to `OPENALEX_EMAIL` for the polite pool. |

### Brave Search

| | |
|---|---|
| **What it does** | Web search via Brave Search API. Used by the agentic pipeline for literature research. |
| **Env vars needed** | `BRAVE_API_KEY` (required for this feature) |
| **Required?** | No — only used by the agentic pipeline. |
| **How to test** | The agentic pipeline will report `BRAVE_API_KEY not set` if not configured. Set the key and re-run. |
| **Common problems** | Free tier limit (2,000/month) exceeded → upgrade or wait until next month. |

### PaperForge

| | |
|---|---|
| **What it does** | Multi-agent workflow for generating academic paper drafts from a topic or codebase. |
| **Env vars needed** | Uses the same model provider keys listed above (Anthropic, Gemini, etc.). No additional keys required. Available at `/paperforge` when the agentic pipeline package is installed. |
| **Required?** | No. |
| **How to test** | Open `/paperforge`, enter a topic, and generate an outline. |

### AI usage disclosure

| | |
|---|---|
| **What it does** | Logs model usage to `~/thesis/logs/YYYY-MM-DD.jsonl` and generates AI-use disclosure statements. |
| **Env vars needed** | None — logs are written automatically. |
| **Required?** | No — but strongly recommended if your institution requires AI disclosure. |
| **How to test** | Run `ra-disclose` from the terminal or open `/disclosure` in the Web UI. |

### Local workspace paths

| | |
|---|---|
| **What it does** | Defines where your thesis projects, drafts, logs, sessions, indexes, and exports live. |
| **Env vars needed** | `THESIS_ROOT` (default: `~/thesis`), `THESIS_DOCS` (optional) |
| **Required?** | `THESIS_ROOT` is strongly recommended. It defaults to `~/thesis` if not set. |
| **How to test** | Open `/settings` — the resolved path is shown with a ✓ (exists) or ⚠ (not found) status pill. |
| **Common problems** | Path was moved or deleted → update `THESIS_ROOT` in `/settings` and restart. |

## Troubleshooting

### Installation and startup

| Problem | Fix |
|---------|-----|
| `research-assistant` is not found | Run `bash scripts/install_cli.sh`. Make sure `~/.local/bin` is in your `PATH`. |
| `ra` is not found | Add `alias ra="research-assistant"` to `~/.bashrc` or use the full command. |
| Project directory not found | The repo was moved or deleted after installing the wrapper. Reinstall from the new repo path with `bash scripts/install_cli.sh`. |
| Web UI does not start | Run `research-assistant doctor`, then check logs with `research-assistant logs`. |
| Port 5050 is already in use | Run `research-assistant restart` or start with another port: `RA_PORT=5051 research-assistant`. |

### API keys and providers

| Problem | Fix |
|---------|-----|
| API key is missing | Open `/settings` to see which keys are set. Add missing keys to `.env` and restart. |
| Provider test fails | Open `/providers`, click **Test**, read the error message. Check key validity on the provider's dashboard. |
| Claude CLI is installed but not detected | Verify with `which claude`. Check that `CLAUDE_CLI_CMD` matches the actual binary. The default is `claude -p`. |
| `.env` changes do not apply | Restart the app: `research-assistant restart`. Path and timeout changes are read at startup. |
| The Web UI shows an old setting | After saving in `/settings`, restart the app for path and CLI changes. API keys always require restart. |
| Rate limit errors | Wait and retry. Add API keys (Semantic Scholar, OpenAlex email) for higher rate limits. |

### Zotero

| Problem | Fix |
|---------|-----|
| Zotero path has zero PDFs | `ZOTERO_STORAGE` must point to the `storage/` folder *containing* the random subfolders, not to a subfolder itself. On Linux this is typically `~/Zotero/storage`. Run `research-assistant doctor` to see diagnostics. |
| Zotero API returns no results | Check that `ZOTERO_USER_ID` is numeric and `ZOTERO_API_KEY` has read access. Use the **Test Zotero API** button in `/settings`. |
| Zotero storage path was moved | Update `ZOTERO_STORAGE` in `/settings` or `.env`, then restart the app. |

### Paper discovery

| Problem | Fix |
|---------|-----|
| Elicit is not configured | Set `ELICIT_API_KEY` in `.env` or from `/settings`. Elicit requires a paid plan. |
| Paper discovery returns no results | Try a different source (OpenAlex works without any key). Broaden your search query. Check your internet connection. |
| Semantic Scholar rate limited | Add a free API key to `SEMANTIC_SCHOLAR_API_KEY`. Get one at semanticscholar.org/product/api. |

### Paths and workspace

| Problem | Fix |
|---------|-----|
| `THESIS_ROOT` path does not exist | Create it: `mkdir -p ~/thesis`. Or set a different path in `/settings`. |
| A path was moved or deleted | Update the path in `/settings` or `.env` and restart the app. |
| Workspace folder is empty | Workspace folders are created the first time you use a feature (e.g., `/workspace`, `/projects`). |

### Safety

| Problem | Prevention |
|---------|-----------|
| Accidentally committing API keys | `.env` is gitignored. Check `git status` before committing. Never add `.env` to the repo. |
| Accidentally committing private research data | Keep thesis PDFs, drafts, and logs outside the repository folder. They belong in `THESIS_ROOT` (default `~/thesis`). |
| Accidentally committing Zotero PDFs | The Zotero storage folder should be outside the repository. Never add it to git.

## Default locations

<table>
  <thead>
    <tr>
      <th>Item</th>
      <th>Default path</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Python virtual environment</td>
      <td><code>~/.venvs/thesis</code></td>
      <td>Python environment used to run the app and CLI tools.</td>
    </tr>
    <tr>
      <td>Research workspace</td>
      <td><code>~/thesis</code></td>
      <td>Main place for projects, drafts, notes, evidence, exports, logs, and runs.</td>
    </tr>
    <tr>
      <td>Zotero PDF storage</td>
      <td><code>~/Zotero/storage</code></td>
      <td>Local Zotero attachment folder used for indexing papers.</td>
    </tr>
    <tr>
      <td>Application settings</td>
      <td><code>.env</code></td>
      <td>API keys, model settings, Zotero paths, CLI commands, and timeouts.</td>
    </tr>
    <tr>
      <td>Server logs and PID</td>
      <td><code>~/.local/share/research-assistant/</code></td>
      <td>Background server log file and process ID.</td>
    </tr>
    <tr>
      <td>Model usage logs</td>
      <td><code>~/thesis/logs/</code></td>
      <td>Used for AI usage review and disclosure statements.</td>
    </tr>
  </tbody>
</table>

## Recommended project structure

The app works best when each thesis, manuscript, or review has its own project folder inside `THESIS_ROOT`.

```text
~/thesis/
├── projects/
│   └── my-thesis-project/
│       ├── drafts/
│       ├── notes/
│       ├── outlines/
│       ├── evidence/
│       ├── exports/
│       └── paperforge/
├── logs/
├── indexes/
├── disclosures/
└── runs/
```

<table>
  <thead>
    <tr>
      <th>Folder</th>
      <th>Save here</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>drafts/</code></td>
      <td>Thesis chapters, manuscript sections, abstracts, and rewritten paragraphs.</td>
    </tr>
    <tr>
      <td><code>notes/</code></td>
      <td>Your reading notes, meeting notes, supervisor comments, and research ideas.</td>
    </tr>
    <tr>
      <td><code>outlines/</code></td>
      <td>Generated outlines, section maps, chapter plans, and article structures.</td>
    </tr>
    <tr>
      <td><code>evidence/</code></td>
      <td>Cited answers, claim verification outputs, and evidence tables.</td>
    </tr>
    <tr>
      <td><code>exports/</code></td>
      <td>Submission ready text, copied outputs, reports, and disclosure text.</td>
    </tr>
    <tr>
      <td><code>paperforge/</code></td>
      <td>PaperForge drafts, review outputs, revision passes, charts, and final exports.</td>
    </tr>
    <tr>
      <td><code>logs/</code></td>
      <td>Automatic AI usage logs. Keep them if your university or journal requires disclosure.</td>
    </tr>
  </tbody>
</table>

## Where your work is saved

<table>
  <thead>
    <tr>
      <th>Work type</th>
      <th>Where to find it</th>
      <th>How to continue later</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Saved Q&amp;A sessions</td>
      <td><code>/sessions</code></td>
      <td>Open the session, review the answer, and keep the evidence trail.</td>
    </tr>
    <tr>
      <td>Project documents</td>
      <td><code>/workspace</code> and <code>THESIS_ROOT</code></td>
      <td>Continue editing the same project document.</td>
    </tr>
    <tr>
      <td>Project metadata</td>
      <td><code>/projects</code></td>
      <td>Reuse the title, research question, hypothesis, keywords, discipline, and supervisor notes across tools.</td>
    </tr>
    <tr>
      <td>Model usage logs</td>
      <td><code>~/thesis/logs/</code></td>
      <td>Review model usage or generate AI disclosure text.</td>
    </tr>
    <tr>
      <td>Zotero index</td>
      <td>Managed under the local research workspace</td>
      <td>Use Ask Library, Evidence, Claim Verify, Audit, and Outline tools with retrieved sources.</td>
    </tr>
    <tr>
      <td>PaperForge runs</td>
      <td><code>~/thesis/runs/</code> or the output folder you choose</td>
      <td>Review generated drafts, figures, checks, and final exports.</td>
    </tr>
  </tbody>
</table>

## Web UI pages

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>Route</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dashboard</td>
      <td><code>/</code></td>
      <td>Overview of index status, providers, sessions, and active project.</td>
    </tr>
    <tr>
      <td>Ask Library</td>
      <td><code>/ask-library</code></td>
      <td>Ask with RAG, ask without context, or compare models in one place.</td>
    </tr>
    <tr>
      <td>Sessions</td>
      <td><code>/sessions</code></td>
      <td>Review and delete saved research sessions.</td>
    </tr>
    <tr>
      <td>Index setup</td>
      <td><code>/index-setup</code></td>
      <td>Check Zotero paths and run PDF indexing.</td>
    </tr>
    <tr>
      <td>Library search</td>
      <td><code>/library-search</code></td>
      <td>Search Zotero items and local PDFs.</td>
    </tr>
    <tr>
      <td>Paper discovery</td>
      <td><code>/paper-discovery</code></td>
      <td>Search external paper discovery sources.</td>
    </tr>
    <tr>
      <td>Writing Studio</td>
      <td><code>/writing-studio</code></td>
      <td>Outline, draft, critique, paraphrase, and coherence tools.</td>
    </tr>
    <tr>
      <td>Outline Recommender</td>
      <td><code>/outline-recommender</code></td>
      <td>Create paper type aware outlines and optionally map evidence to sections.</td>
    </tr>
    <tr>
      <td>Projects</td>
      <td><code>/projects</code></td>
      <td>Create, edit, activate, and manage research projects.</td>
    </tr>
    <tr>
      <td>Workspace</td>
      <td><code>/workspace</code></td>
      <td>Edit project documents with source aware AI assistance and undo support.</td>
    </tr>
    <tr>
      <td>Peer Review</td>
      <td><code>/peer-review</code></td>
      <td>Run structural, methodology, and citation review passes.</td>
    </tr>
    <tr>
      <td>Defense</td>
      <td><code>/defense</code></td>
      <td>Generate thesis defense questions from examiner personas.</td>
    </tr>
    <tr>
      <td>Orchestration</td>
      <td><code>/orchestration</code></td>
      <td>Review model calls, token usage, cost estimates, and recent activity.</td>
    </tr>
    <tr>
      <td>Prompt Library</td>
      <td><code>/prompts</code></td>
      <td>Browse curated academic prompts.</td>
    </tr>
    <tr>
      <td>Providers</td>
      <td><code>/providers</code></td>
      <td>Check API and CLI provider status, then test each model alias.</td>
    </tr>
    <tr>
      <td>Settings</td>
      <td><code>/settings</code></td>
      <td>Edit API keys, paths, provider commands, and timeout settings.</td>
    </tr>
    <tr>
      <td>PaperForge</td>
      <td><code>/paperforge</code></td>
      <td>Generate and revise paper drafts through a multi agent workflow.</td>
    </tr>
  </tbody>
</table>

Older routes such as `/ask`, `/compare`, and `/index` redirect to the newer consolidated pages where possible.

## CLI tools

Everything important in the Web UI can also be used from the terminal.

### Research

```bash
ra-researcher ask "What are the main mechanisms of TRAIL resistance in glioblastoma?"
ra-researcher index
ra-ask "Explain this concept" --model claude
ra-compare "Compare these mechanisms across models"
ra-zot "glioblastoma TRAIL resistance"
ra-discover "metabolic rewiring glioblastoma resistance" --source openalex
ra-evidence "What evidence supports metabolic adaptation in GBM resistance?"
```

### Writing

```bash
ra-outline-recommender
ra-ideas evidence.md --job "Explain why this pathway matters"
ra-outline evidence.md --job "Structure the introduction"
ra-critique draft.md
ra-critic draft.md
ra-paraphrase draft.md
ra-coherence chapter.md
```

### Verification and transparency

```bash
ra-audit draft.md
ra-claim-verify draft.md
ra-originality draft.md
ra-verify bibliography.bib
ra-disclose
```

### Workspace tools

```bash
ra-project
ra-orchestration
ra-prompts
ra-peer-review
ra-defense
```

Run any command with `--help`:

```bash
ra-claim-verify --help
ra-outline-recommender --help
```

## Supported models

<table>
  <thead>
    <tr>
      <th>Alias</th>
      <th>Provider</th>
      <th>Recommended use</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>claude</code></td>
      <td>Anthropic Claude</td>
      <td>Long form reasoning, critique, synthesis, and revision.</td>
    </tr>
    <tr>
      <td><code>sonnet</code></td>
      <td>Claude Sonnet</td>
      <td>Balanced academic writing and review workflows.</td>
    </tr>
    <tr>
      <td><code>haiku</code></td>
      <td>Claude Haiku</td>
      <td>Fast lightweight tasks.</td>
    </tr>
    <tr>
      <td><code>gemini</code></td>
      <td>Google Gemini</td>
      <td>Long context synthesis and research comparison.</td>
    </tr>
    <tr>
      <td><code>flash</code></td>
      <td>Gemini Flash</td>
      <td>Fast lower cost processing.</td>
    </tr>
    <tr>
      <td><code>deepseek</code></td>
      <td>DeepSeek</td>
      <td>Drafting, rewriting, and general text generation.</td>
    </tr>
    <tr>
      <td><code>gpt</code></td>
      <td>OpenAI GPT</td>
      <td>General reasoning, structured output, and writing.</td>
    </tr>
    <tr>
      <td><code>gpt-mini</code></td>
      <td>OpenAI smaller model alias</td>
      <td>Lower cost general tasks.</td>
    </tr>
    <tr>
      <td><code>local</code></td>
      <td>Ollama</td>
      <td>Local model workflows.</td>
    </tr>
  </tbody>
</table>

CLI routed aliases can also be configured, including:

```text
claude-cli
gemini-cli
codex-cli
ollama-cli
```

## PaperForge

**PaperForge** is the multi agent paper drafting workflow included inside research-assistant.

It can help generate a structured paper draft from:

1. A research topic.
2. A codebase plus a short summary.
3. A review article idea.

Open it from:

```text
http://127.0.0.1:5050/paperforge
```

Typical PaperForge flow:

```text
Input topic or codebase
→ Generate outline
→ Analyze code or literature context
→ Draft sections
→ Edit sections interactively
→ Generate or review figures
→ Run assessment and peer review
→ Check claims and originality signals
→ Export final files
```

Useful scripts:

```bash
scripts/run_agentic.py
scripts/run_review.py
scripts/generate_final_docx.py
agentic/quick_ai_score.py
agentic/mcp_servers/chart_server.py
agentic/mcp_servers/zerogpt_server.py
agentic/mcp_servers/google_search_server.py
```

Example commands:

```bash
./scripts/run_agentic.py /path/to/project --summary "What the code does" --output /tmp/paper
./scripts/run_review.py --topic "CRISPR based therapeutics and delivery methods"
./scripts/generate_final_docx.py <job_id> --charts /path/to/charts
./agentic/quick_ai_score.py paper.md --json
```

## Example workflows

### Ask a cited question from your own papers

```bash
ra-researcher ask "What are the major mechanisms of TRAIL resistance in glioblastoma?"
```

### Compare model answers before trusting one output

```bash
ra-compare "Summarize the evidence for metabolic rewiring in glioblastoma resistance."
```

### Create a thesis chapter outline

```bash
ra-outline-recommender
```

### Check whether claims are supported

```bash
ra-claim-verify draft.md
```

### Generate AI usage disclosure

```bash
ra-disclose
```

## Safe use, privacy, and academic responsibility

research-assistant is designed to support academic work, not replace the researcher, supervisor, reviewer, or clinician.

Use it carefully:

1. Verify every important claim against the original paper.
2. Check whether cited sources actually support the sentence you wrote.
3. Do not submit generated text without human revision.
4. Follow your university, journal, conference, or institution rules for AI use.
5. Disclose AI assistance when required.

Privacy notes:

1. Your workspace, drafts, logs, and indexes are stored locally by default.
2. Model prompts may still be sent to external providers when you use API based models.
3. Use local or CLI routed models if your project requires stricter data control.
4. Never commit `.env`, unpublished drafts, private PDFs, Zotero files, model logs, or sensitive research data to a public repository.

## Backup

Recommended backup targets:

<table>
  <thead>
    <tr>
      <th>Back up</th>
      <th>Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>.env</code></td>
      <td>Contains local settings and may contain API keys. Store securely.</td>
    </tr>
    <tr>
      <td><code>THESIS_ROOT</code></td>
      <td>Contains drafts, notes, evidence, sessions, logs, exports, and project files.</td>
    </tr>
    <tr>
      <td>Zotero library</td>
      <td>Contains paper metadata and PDFs used for retrieval.</td>
    </tr>
  </tbody>
</table>

Basic backup command:

```bash
tar -czf thesis-backup-$(date +%Y%m%d).tar.gz ~/thesis
```

For sensitive research, use encrypted storage or a trusted private backup location.

## Updating

```bash
cd /path/to/research-assistant
git pull
bash scripts/setup.sh
bash scripts/install_cli.sh
research-assistant restart
```

If you changed `.env`, keep a private backup before major updates.

## Uninstall

Automatic uninstall if you still have the repo:

```bash
cd /path/to/research-assistant
bash scripts/uninstall_cli.sh
```

Manual cleanup:

```bash
rm -f ~/.local/bin/research-assistant
rm -f ~/.local/share/applications/research-assistant.desktop
rm -rf ~/.local/share/research-assistant
```

The uninstaller does not remove your research data.

These are your files and should be deleted only if you are sure:

```bash
rm -rf ~/thesis ~/.venvs/thesis
```

Your Zotero library is separate and is not removed by research-assistant.

## FAQ

### Do I need Zotero?

No, but Zotero is strongly recommended. Citation aware Q&amp;A works best when your own papers are indexed from Zotero storage.

### Do I need all API keys?

No. One working model provider is enough. More providers are useful for comparison, peer review, and PaperForge workflows.

### Can I use local models?

Yes. Ollama can be configured through the `local` alias or through CLI routed commands.

### Does this replace Zotero?

No. Zotero remains your reference manager. research-assistant uses Zotero as a source for retrieval, discovery, and writing workflows.

### Does this replace my supervisor or peer reviewer?

No. It helps you organize evidence, draft text, compare models, and find possible weaknesses. Final academic responsibility remains with you.

### Can I use it for sensitive or unpublished work?

Yes, but be careful. Local files stay on your machine by default, but API based model calls may send prompts to external providers. For sensitive work, use local models or institutionally approved providers and follow your data governance rules.

## Project philosophy

<table>
  <thead>
    <tr>
      <th>Principle</th>
      <th>Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Local first</td>
      <td>Your workspace, drafts, indexes, and logs are organized on your own machine by default.</td>
    </tr>
    <tr>
      <td>Evidence aware</td>
      <td>The tool is designed to keep retrieved papers visible during writing and verification.</td>
    </tr>
    <tr>
      <td>Model plural</td>
      <td>You can compare providers instead of trusting one model output immediately.</td>
    </tr>
    <tr>
      <td>Transparent</td>
      <td>AI assistance should be logged, reviewable, and disclosed when required.</td>
    </tr>
    <tr>
      <td>Researcher controlled</td>
      <td>The tool supports academic judgment. It does not replace it.</td>
    </tr>
  </tbody>
</table>

## Contributing

Feedback, issues, ideas, and pull requests are welcome.

Helpful contributions include:

1. Bug reports with command output and logs.
2. Documentation improvements.
3. New provider integrations.
4. Better Zotero and PDF indexing diagnostics.
5. More academic writing and verification tools.
6. UI improvements for long thesis workflows.

Before opening a pull request, run:

```bash
pytest tests/ -x --tb=short
ruff check research_assistant/ agentic/ tests/
ruff format research_assistant/ agentic/ tests/
```

## License

MIT License. See [LICENSE](LICENSE).
