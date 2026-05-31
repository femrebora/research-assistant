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

You can configure the app from the browser:

```text
http://127.0.0.1:5050/settings
```

Or edit `.env` manually:

```bash
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
DEEPSEEK_API_KEY=sk-...
OPENAI_API_KEY=sk-...

ZOTERO_USER_ID=1234567
ZOTERO_API_KEY=...
THESIS_ROOT=/home/you/thesis
ZOTERO_STORAGE=/home/you/Zotero/storage

SEMANTIC_SCHOLAR_API_KEY=
ELICIT_API_KEY=

CLAUDE_CLI_CMD="claude -p"
GEMINI_CLI_CMD="gemini -p"
CODEX_CLI_CMD="codex exec"
OLLAMA_CLI_CMD="ollama run llama3.3"
CLI_TIMEOUT=600
```

Model aliases can be changed without editing source code:

```bash
RA_MODEL_CLAUDE=anthropic/claude-opus-4-8
RA_MODEL_SONNET=anthropic/claude-sonnet-4-6
RA_MODEL_GPT=openai/gpt-5
RA_MODEL_GEMINI=gemini/gemini-2.5-pro
RA_MODEL_FLASH=gemini/gemini-2.5-flash
RA_MODEL_LOCAL=ollama/llama3.3
```

Pattern:

```text
RA_MODEL_<ALIAS>=provider/model-name
```

Examples:

```text
RA_MODEL_GPT
RA_MODEL_GEMINI
RA_MODEL_DEEPSEEK
RA_MODEL_LOCAL
```

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

## Troubleshooting

<table>
  <thead>
    <tr>
      <th>Problem</th>
      <th>Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>research-assistant</code> is not found</td>
      <td>Run <code>bash scripts/install_cli.sh</code>. Make sure <code>~/.local/bin</code> is in your <code>PATH</code>.</td>
    </tr>
    <tr>
      <td><code>ra</code> is not found</td>
      <td>Add <code>alias ra="research-assistant"</code> to <code>~/.bashrc</code> or use the full command.</td>
    </tr>
    <tr>
      <td>Project directory not found</td>
      <td>The repo was moved or deleted after installing the wrapper. Reinstall from the new repo path with <code>bash scripts/install_cli.sh</code>.</td>
    </tr>
    <tr>
      <td>Web UI does not start</td>
      <td>Run <code>research-assistant doctor</code>, then check logs with <code>research-assistant logs</code>.</td>
    </tr>
    <tr>
      <td>Port 5050 is already in use</td>
      <td>Run <code>research-assistant restart</code> or start with another port: <code>RA_PORT=5051 research-assistant</code>.</td>
    </tr>
    <tr>
      <td>Provider test fails</td>
      <td>Open <code>/settings</code>, check the API key or CLI command, then test again from <code>/providers</code>.</td>
    </tr>
    <tr>
      <td>Zotero indexing finds zero PDFs</td>
      <td>Open <code>/index-setup</code> and check diagnostics. <code>ZOTERO_STORAGE</code> should point to the folder containing Zotero attachment subfolders.</td>
    </tr>
    <tr>
      <td>Answers have weak citations</td>
      <td>Index more relevant papers, ask a narrower question, or add stronger project keywords.</td>
    </tr>
    <tr>
      <td>CLI provider times out</td>
      <td>Increase <code>CLI_TIMEOUT</code> in <code>.env</code> or from <code>/settings</code>.</td>
    </tr>
    <tr>
      <td>You cannot find previous work</td>
      <td>Check <code>/sessions</code>, <code>/workspace</code>, <code>/projects</code>, <code>~/thesis/logs/</code>, and your project folder under <code>THESIS_ROOT</code>.</td>
    </tr>
  </tbody>
</table>

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
