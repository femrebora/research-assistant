# FAQ & Troubleshooting

## Why do I see "No document index found"?

You haven't indexed your PDFs yet. Go to **Index & Setup** → follow the wizard to connect Zotero (or a local PDF folder) → click **Build index**. The first index may take several minutes depending on your library size. After that, Ask Library will be able to search your papers.

## Why does Ask Library return empty results?

Check the following:

1. **Is ZOTERO_STORAGE set?** Run `ra doctor` to see configured paths. The Zotero storage folder must exist and contain PDFs.
2. **Are your PDFs indexed?** Go to Index & Setup → Step 5. The page shows document and chunk counts. If zero, click Build Index.
3. **Is your question specific enough?** Very broad questions may not match any chunks at the default similarity threshold. Try a more targeted question.
4. **Check the threshold.** In Ask Library → Advanced, lower the similarity threshold (default 0.35). A lower value returns more but less-relevant chunks.

## A model provider shows "Not configured"

Go to **Settings**. Each model provider needs its API key filled in. At minimum you need one working provider. The keys you set are saved to your local `.env` file and never leave your machine.

The provider health page (`/providers`) shows which keys are present and lets you test each one with a quick smoke test (one short message, ~16 tokens).

## Why doesn't Zotero search find my papers?

1. **ZOTERO_USER_ID and ZOTERO_API_KEY must both be set.** Check Settings → Zotero section.
2. **Your Zotero API key needs "read" access.** Create or verify at https://www.zotero.org/settings/keys.
3. **Library Search also scans local PDFs by filename.** Even without Zotero API, filenames containing your search term will appear.

## The app says "port 5050 is already in use"

Another instance is already running. Either:

```bash
ra stop         # graceful shutdown
ra restart      # stop + start
```

Or kill the process manually:
```bash
kill $(cat ~/.local/share/research-assistant/research-assistant.pid)
```

## I changed a setting but it didn't take effect

- **Paths** (THESIS_ROOT, ZOTERO_STORAGE) and **CLI commands** are read at startup. After changing them, restart the app (`ra restart`).
- **API keys** take effect immediately for API-routed providers. CLI-routed providers (claude-cli, gemini-cli, codex-cli, ollama-cli) may need a restart if the CLI tool itself reads env vars at startup.
- **Model alias overrides** (RA_MODEL_*) are read at startup. Restart to apply.

## "command not found: ra"

The `ra` alias is optional and is not installed automatically. You can either:

- Use the full command: `research-assistant`
- Add an alias manually: `alias ra="research-assistant"` in your `~/.bashrc` or `~/.zshrc`

The `research-assistant` command itself is installed by `bash scripts/install_cli.sh`. If even `research-assistant` is not found, run the installer.

## How do I use a local model (Ollama)?

1. Install [Ollama](https://ollama.com/).
2. Pull a model: `ollama pull llama3.3`
3. Set one of these in Settings or `.env`:
   - For API-style calls: `OLLAMA_MODEL=ollama/llama3.3`
   - For CLI-routed calls: `OLLAMA_CLI_CMD=ollama run llama3.3`
4. Select the **local** or **ollama-cli** alias from the model dropdown.

For embeddings with a local model, set `EMBEDDING_MODEL=ollama/nomic-embed-text`.

## How do I back up my data?

Your workspace is entirely file-based. Back up these directories:

- `$THESIS_ROOT/` — all projects, drafts, sessions, logs, and the vector index
- `.env` — your API keys and config (excluded from git)
- `$HOME/Zotero/storage/` — your Zotero PDF library (if using Zotero)

To restore, copy the directories back and point `.env` at the correct paths.

## How do I uninstall?

```bash
# From the research-assistant directory:
bash scripts/uninstall_cli.sh   # removes ~/.local/bin/research-assistant

# Then delete the project directory and your workspace:
rm -rf /path/to/research-assistant
rm -rf ~/thesis                  # or wherever THESIS_ROOT points
```

Your Zotero library is independent — uninstalling does not touch it.

## The app crashed. Where are the logs?

```bash
ra logs          # last 50 lines
ra logs -n 200   # last 200 lines
ra logs -f       # follow (tail -f)
```

The log file is at `$XDG_DATA_HOME/research-assistant/research-assistant.log` (typically `~/.local/share/research-assistant/research-assistant.log`).

## Is my data private?

Yes. The Research Assistant is **local-first**:

- Your PDFs, drafts, and notes stay on your machine.
- API keys are stored in your local `.env` file (never committed to git).
- Model calls go directly to the provider's API from your machine.
- No telemetry, no analytics, no cloud sync.

The only data that leaves your machine is the text you send to model providers (Anthropic, OpenAI, Google, DeepSeek) when you make queries. Review each provider's data usage policy if this concerns you.
