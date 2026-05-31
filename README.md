# research-assistant

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-A3E635)](LICENSE)
[![Web UI](https://img.shields.io/badge/web%20UI-Flask-000000?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![Zotero](https://img.shields.io/badge/Zotero-ready-CC2936?logo=zotero\&logoColor=white)](https://www.zotero.org/)
[![Local first](https://img.shields.io/badge/local%20first-research%20workspace-7C3AED)](#privacy-and-safe-academic-use)

A local first research workspace for thesis writing, literature review, Zotero based retrieval, model comparison, academic drafting, paper discovery, project organization, AI usage disclosure, and PaperForge.

`research-assistant` helps you keep your research workflow in one place:

1. Put your papers in Zotero.
2. Index your local PDFs.
3. Ask questions over your own library.
4. Compare answers from different models.
5. Save useful outputs into project workspaces.
6. Check claims before using generated text in your thesis or manuscript.
7. Keep AI usage logs for disclosure.

## Why use this?

Many research workflows become messy because papers, notes, drafts, citations, AI prompts, and model outputs are stored in different places. This project gives you a single local workspace for academic work.

| Problem                                                    | How this project helps                                                           |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Your papers are in Zotero but your AI tool cannot use them | Index local Zotero PDFs and ask questions over your own library                  |
| AI answers are hard to trust                               | Use retrieval, citation aware answers, claim verification, and citation auditing |
| Different models give different answers                    | Compare providers before trusting one answer                                     |
| Thesis work gets scattered                                 | Keep projects, drafts, sessions, evidence, logs, and exports under one workspace |
| AI disclosure is easy to forget                            | Save model usage logs and generate disclosure text when needed                   |

## Main features

| Feature             | What it does                                                                           |
| ------------------- | -------------------------------------------------------------------------------------- |
| Zotero RAG          | Indexes local Zotero PDF attachments and retrieves relevant paper chunks               |
| Ask Library         | Ask cited questions using your indexed library, ask without context, or compare models |
| Paper Discovery     | Search OpenAlex, Semantic Scholar, and Elicit when configured                          |
| Writing Studio      | Draft, outline, critique, paraphrase, and check coherence                              |
| Project Workspace   | Keep each thesis, manuscript, or review project separate                               |
| Workspace Editor    | Continue writing project documents with AI assisted revision and undo support          |
| Peer Review         | Simulate structural, methodological, and citation focused review                       |
| Defense Preparation | Generate thesis defense questions from different examiner styles                       |
| Claim Verification  | Check whether draft claims are supported by retrieved evidence                         |
| PaperForge          | Multi agent workflow for academic paper drafts from a topic or codebase                |
| AI Disclosure       | Save model usage logs and prepare transparent AI use statements                        |

## Requirements

| Requirement                 | Why it is needed                                       |
| --------------------------- | ------------------------------------------------------ |
| Python 3.11 or newer        | Main application runtime                               |
| Git                         | Clone and update the repository                        |
| Bash compatible shell       | Run setup scripts                                      |
| Zotero                      | Recommended for citation aware work with your own PDFs |
| At least one model provider | API key, local Ollama model, or CLI routed model       |

You do not need every API key. One working model provider is enough to start.

## Quick start

Run these commands from a terminal:

```bash
git clone https://github.com/femrebora/research-assistant.git
cd research-assistant
bash scripts/setup.sh
bash scripts/install_cli.sh
source ~/.bashrc
ra
```

Then open this address if the browser does not open automatically:

```text
http://127.0.0.1:5050
```

Daily use is simple:

```bash
ra          # start or reopen the app
ra stop     # stop the background server
ra doctor   # check setup problems
```

## What the setup scripts do

`bash scripts/setup.sh` does the main Python setup.

| It creates or updates       | Default location   |
| --------------------------- | ------------------ |
| Python virtual environment  | `~/.venvs/thesis`  |
| Project `.env` file         | `./.env`           |
| Main research workspace     | `~/thesis`         |
| Default logs folder         | `~/thesis/logs`    |
| Default Zotero storage path | `~/Zotero/storage` |

`bash scripts/install_cli.sh` installs the easy command.

| It creates or updates        | Location                                      |
| ---------------------------- | --------------------------------------------- |
| `research-assistant` command | `~/.local/bin/research-assistant`             |
| `ra` shortcut                | Added to `~/.bashrc` when possible            |
| PATH entry                   | Adds `~/.local/bin` to shell PATH when needed |

After running the installer, either run:

```bash
source ~/.bashrc
```

or open a new terminal.

If you use `zsh`, add this manually if needed:

```bash
export PATH="$HOME/.local/bin:$PATH"
alias ra="research-assistant"
```

## First run checklist

Do these steps in order after opening the Web UI.

| Step | Page           | What to do                                             |
| ---- | -------------- | ------------------------------------------------------ |
| 1    | `/settings`    | Add at least one API key or configure one CLI provider |
| 2    | `/providers`   | Test the model aliases you want to use                 |
| 3    | `/settings`    | Check `THESIS_ROOT` and `ZOTERO_STORAGE`               |
| 4    | `/index-setup` | Scan and index Zotero PDFs                             |
| 5    | `/projects`    | Create your thesis, manuscript, or review project      |
| 6    | `/ask-library` | Ask a small test question and confirm citations work   |

## Configure model providers

You can use the app with only one provider. Add keys in `.env` or from `/settings`.

```bash
# Choose at least one
ANTHROPIC_API_KEY=sk-ant-your-key
GEMINI_API_KEY=your-gemini-key
DEEPSEEK_API_KEY=sk-your-deepseek-key
OPENAI_API_KEY=sk-your-openai-key
```

After editing `.env`, restart the app:

```bash
ra restart
```

Then test providers from:

```text
http://127.0.0.1:5050/providers
```

### API providers

| Variable            | Purpose              |
| ------------------- | -------------------- |
| `ANTHROPIC_API_KEY` | Claude model aliases |
| `GEMINI_API_KEY`    | Gemini model aliases |
| `DEEPSEEK_API_KEY`  | DeepSeek model alias |
| `OPENAI_API_KEY`    | OpenAI model aliases |

### CLI routed providers

These are optional. They are useful when you already use command line model tools.

```bash
CLAUDE_CLI_CMD="claude -p"
GEMINI_CLI_CMD="gemini -p"
CODEX_CLI_CMD="codex exec"
OLLAMA_CLI_CMD="ollama run llama3.3"
CLI_TIMEOUT=600
```

Test them from `/providers`.

### Local models with Ollama

If you want local models:

```bash
ollama pull llama3.3
ollama serve
```

Then set:

```bash
OLLAMA_MODEL=ollama/llama3.3
```

## Configure Zotero

Zotero is optional, but it is the best way to use the tool for citation aware research.

Add these values in `.env` or from `/settings`:

```bash
ZOTERO_STORAGE=/home/yourname/Zotero/storage
ZOTERO_USER_ID=1234567
ZOTERO_API_KEY=your-zotero-api-key
```

Get `ZOTERO_USER_ID` and `ZOTERO_API_KEY` from:

```text
https://www.zotero.org/settings/keys
```

Important: `ZOTERO_STORAGE` must point to the folder that contains Zotero attachment subfolders. Do not point it to one single paper folder.

Correct:

```text
/home/yourname/Zotero/storage/
├── ABC12345/
│   └── paper.pdf
├── DEF67890/
│   └── another-paper.pdf
└── ...
```

Wrong:

```text
/home/yourname/Zotero/storage/ABC12345/
```

After setting Zotero paths, go to:

```text
http://127.0.0.1:5050/index-setup
```

Then run the scan and indexing steps.

You can also index from the terminal:

```bash
ra-researcher index
```

## How to use the app

### Daily workflow

1. Start the app.

```bash
ra
```

2. Check your active project at `/projects`.

3. Ask a question from your library at `/ask-library`.

4. Save useful answers into `/workspace`.

5. Run claim checks before using generated text in your thesis or manuscript.

6. Stop the app when you are finished.

```bash
ra stop
```

Closing the browser does not stop the server. The app keeps running in the background until you run `ra stop`.

### Main Web UI pages

| Page                | Route                  | Use it for                                                      |
| ------------------- | ---------------------- | --------------------------------------------------------------- |
| Dashboard           | `/`                    | Quick overview of the app                                       |
| Ask Library         | `/ask-library`         | Ask questions over indexed papers or compare models             |
| Sessions            | `/sessions`            | Return to previous Q&A sessions                                 |
| Index Setup         | `/index-setup`         | Check Zotero path and build the local index                     |
| Library Search      | `/library-search`      | Search indexed papers and Zotero metadata                       |
| Paper Discovery     | `/paper-discovery`     | Search OpenAlex, Semantic Scholar, or Elicit                    |
| Writing Studio      | `/writing-studio`      | Draft, outline, critique, paraphrase, and improve academic text |
| Outline Recommender | `/outline-recommender` | Build thesis, paper, or review outlines                         |
| Projects            | `/projects`            | Create and manage research projects                             |
| Workspace           | `/workspace`           | Continue writing and organize project files                     |
| Peer Review         | `/peer-review`         | Run reviewer style feedback passes                              |
| Defense             | `/defense`             | Generate thesis defense questions                               |
| Providers           | `/providers`           | Test API and CLI model providers                                |
| Settings            | `/settings`            | Edit paths, keys, commands, and timeout settings                |
| PaperForge          | `/paperforge`          | Run multi agent paper drafting workflows                        |

## Where your work is saved

Most research outputs are saved under `THESIS_ROOT`. The default is:

```text
~/thesis
```

| Output            | Default location                                           |
| ----------------- | ---------------------------------------------------------- |
| Model usage logs  | `~/thesis/logs/YYYY-MM-DD.jsonl`                           |
| Research sessions | `~/thesis/research_sessions/`                              |
| Vector index      | `~/thesis/chroma_db/`                                      |
| Project files     | `~/thesis/projects/<project-slug>/`                        |
| Server log        | `~/.local/share/research-assistant/research-assistant.log` |
| Server PID        | `~/.local/share/research-assistant/research-assistant.pid` |
| Environment file  | `./.env` inside the repository                             |

Recommended project structure:

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
├── chroma_db/
├── research_sessions/
└── disclosures/
```

Use these folders like this:

| Folder        | Save here                                                                 |
| ------------- | ------------------------------------------------------------------------- |
| `drafts/`     | Thesis chapters, manuscript sections, abstracts, and rewritten paragraphs |
| `notes/`      | Reading notes, meeting notes, supervisor comments, and research ideas     |
| `outlines/`   | Chapter plans, article structures, and section maps                       |
| `evidence/`   | Cited answers, claim verification results, and evidence tables            |
| `exports/`    | Text prepared for submission, reports, and final copied outputs           |
| `paperforge/` | PaperForge drafts, review outputs, figures, and final files               |
| `logs/`       | AI usage logs for disclosure and transparency                             |

## How to return to previous work

Start or reopen the app:

```bash
ra
```

Then use these pages:

| Goal                                 | Go to            |
| ------------------------------------ | ---------------- |
| Continue a saved question            | `/sessions`      |
| Continue a thesis or manuscript file | `/workspace`     |
| Change the active project            | `/projects`      |
| Review model calls and logs          | `/orchestration` |
| Rebuild or check the Zotero index    | `/index-setup`   |
| Check provider status                | `/providers`     |

Before closing your work session, copy important answers into the correct project file and keep cited Q&A sessions when you may need the evidence trail later.

## Terminal commands

### App control

| Command                              | What it does                         |
| ------------------------------------ | ------------------------------------ |
| `ra`                                 | Start or reopen the app              |
| `ra stop`                            | Stop the background server           |
| `research-assistant restart`         | Stop and start again                 |
| `research-assistant status`          | Show server status                   |
| `research-assistant logs`            | Show recent logs                     |
| `research-assistant logs -f`         | Follow logs live                     |
| `research-assistant doctor`          | Run diagnostics                      |
| `research-assistant doctor --export` | Export diagnostics                   |
| `research-assistant open`            | Open browser without starting server |
| `research-assistant config`          | Show configuration paths             |

### Research commands

```bash
ra-researcher ask "What are the main mechanisms of TRAIL resistance in glioblastoma?"
ra-researcher index
ra-ask "Explain this concept" --model claude
ra-compare "Compare these mechanisms across models"
ra-zot "glioblastoma TRAIL resistance"
ra-discover "metabolic rewiring glioblastoma resistance" --source openalex
ra-evidence "What evidence supports this claim?"
```

### Writing and verification commands

```bash
ra-outline-recommender
ra-ideas evidence.md --job "Find useful paragraph angles"
ra-outline evidence.md --job "Create an introduction outline"
ra-critique draft.md
ra-paraphrase draft.md
ra-coherence chapter.md
ra-audit draft.md
ra-claim-verify draft.md
ra-disclose
```

Run any command with `--help`:

```bash
ra-claim-verify --help
ra-outline-recommender --help
```

## Optional npm shortcuts

If you prefer npm scripts:

```bash
npm run setup
npm run start
npm run stop
npm run restart
npm run status
npm run logs
npm run doctor
npm run install-cli
npm run install-desktop
npm run test
npm run lint
npm run format
```

## Paper discovery

Open:

```text
http://127.0.0.1:5050/paper-discovery
```

| Source           | Key needed? | Notes                                                         |
| ---------------- | ----------- | ------------------------------------------------------------- |
| OpenAlex         | No          | Works by default. Add `OPENALEX_EMAIL` for better rate limits |
| Semantic Scholar | Optional    | Add `SEMANTIC_SCHOLAR_API_KEY` for higher limits              |
| Elicit           | Yes         | Requires `ELICIT_API_KEY` and a paid Elicit plan              |

## PaperForge

PaperForge is the multi agent paper drafting workflow inside `research-assistant`.

Open:

```text
http://127.0.0.1:5050/paperforge
```

Typical flow:

1. Enter a research topic or codebase summary.
2. Generate an outline.
3. Draft sections.
4. Review and edit sections.
5. Check figures and evidence.
6. Run assessment and peer review.
7. Export final files.

Useful scripts:

```bash
python scripts/run_agentic.py /path/to/project --summary "What the code does" --output /tmp/paper
python scripts/run_review.py --topic "CRISPR based therapeutics and delivery methods"
python scripts/generate_final_docx.py <job_id> --charts /path/to/charts
```

## Desktop launcher

Optional:

```bash
bash scripts/install_desktop_launcher.sh
```

This creates a Research Assistant launcher in your application menu.

## Updating

```bash
cd /path/to/research-assistant
git pull
bash scripts/setup.sh
bash scripts/install_cli.sh
ra restart
```

Keep a private backup of `.env` before major changes.

## Backup

Back up your research workspace regularly:

```bash
tar -czf thesis-backup-$(date +%Y%m%d).tar.gz ~/thesis
```

Recommended backup targets:

| Back up        | Why                                                                      |
| -------------- | ------------------------------------------------------------------------ |
| `.env`         | Contains local configuration and may contain API keys                    |
| `~/thesis`     | Contains your drafts, notes, logs, sessions, evidence, and project files |
| Zotero library | Contains paper metadata and PDFs used for retrieval                      |

For sensitive research, use encrypted storage or a trusted private backup location.

## Troubleshooting

### `ra` command not found

Run:

```bash
bash scripts/install_cli.sh
source ~/.bashrc
```

If you use `zsh`, add this manually:

```bash
export PATH="$HOME/.local/bin:$PATH"
alias ra="research-assistant"
```

### Web UI does not start

Run:

```bash
ra doctor
ra logs
ra restart
```

### Port 5050 is already in use

Check status:

```bash
ra status
```

Use another port:

```bash
RA_PORT=5051 ra
```

### Provider test fails

1. Go to `/settings`.
2. Check whether the key is set.
3. Restart with `ra restart`.
4. Go to `/providers`.
5. Click Test next to the provider.
6. Read the error message.

Common causes are missing API key, invalid key, quota limits, wrong CLI command, or CLI timeout.

### Zotero shows zero PDFs

Check that `ZOTERO_STORAGE` points to the correct folder:

```text
~/Zotero/storage
```

It should contain subfolders with PDFs inside them. Then run:

```bash
ra doctor
```

or use `/index-setup`.

### `.env` changes do not apply

Restart the app:

```bash
ra restart
```

### Old work is hard to find

Check these places:

```text
/sessions
/workspace
/projects
~/thesis/projects/
~/thesis/research_sessions/
~/thesis/logs/
```

## Privacy and safe academic use

`research-assistant` is designed to support academic work. It does not replace your supervisor, reviewer, clinician, or your own judgment.

Important rules:

1. Verify important claims against the original paper.
2. Check that citations really support the sentence you wrote.
3. Do not submit generated text without human revision.
4. Follow your university, journal, conference, or institution rules about AI use.
5. Disclose AI assistance when required.

Privacy notes:

1. Your workspace, drafts, indexes, sessions, and logs are local by default.
2. API based model calls may send prompts to external model providers.
3. Use local models or institution approved providers for sensitive work.
4. Never commit `.env`, Zotero PDFs, private drafts, patient data, unpublished manuscripts, or model logs to a public repository.

## Development

Install and run checks:

```bash
bash scripts/setup.sh
pytest tests/ -x --tb=short
ruff check research_assistant/ agentic/ tests/
ruff format research_assistant/ agentic/ tests/
```

The Python entry points are defined in `pyproject.toml`. The npm shortcuts are defined in `package.json`.

## More documentation

See:

```text
docs/USAGE.md
```

for additional daily workflow notes and troubleshooting details.

## Contributing

Feedback, issues, ideas, and pull requests are welcome.

Good contributions include:

1. Clear bug reports with command output.
2. Better setup documentation.
3. Better Zotero diagnostics.
4. New provider integrations.
5. More academic writing and verification tools.
6. UI improvements for long thesis workflows.

## License

MIT License. See [LICENSE](LICENSE).
