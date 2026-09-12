```
 █████╗ ███████╗███████╗██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗
██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝
███████║███████╗███████╗██║███████╗   ██║   ███████║██╔██╗ ██║   ██║
██╔══██║╚════██║╚════██║██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║
██║  ██║███████║███████║██║███████║   ██║   ██║  ██║██║ ╚████║   ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝
        ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
        ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
        ███████╗█████╔╝ ██║██║     ██║     ███████╗
        ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
        ███████║██║  ██╗██║███████╗███████╗███████║
        ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝
```

# personal-assistant-skills

[![npm version](https://img.shields.io/npm/v/personal-assistant-skills?logo=npm)](https://www.npmjs.com/package/personal-assistant-skills)
[![npm downloads](https://img.shields.io/npm/dm/personal-assistant-skills?logo=npm)](https://www.npmjs.com/package/personal-assistant-skills)
[![CI](https://github.com/deepakkamboj/personal-assistant-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/deepakkamboj/personal-assistant-skills/actions/workflows/ci.yml)
[![Publish](https://github.com/deepakkamboj/personal-assistant-skills/actions/workflows/publish.yml/badge.svg)](https://github.com/deepakkamboj/personal-assistant-skills/actions/workflows/publish.yml)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.9-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Skills](https://img.shields.io/badge/skills-24-6366f1)](.agents/skills)
[![Runtimes](https://img.shields.io/badge/runtimes-Claude%20%7C%20Copilot%20%7C%20Codex-0A7EA4)](#runtimes)
[![MCP](https://img.shields.io/badge/MCP-connected--workspace-0A7EA4)](.agents/mcp/connected-workspace.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](#license)

A **vendor-neutral personal-assistant plugin** that runs across **Claude Code**, **GitHub
Copilot**, and **Codex**. Skills cover a weekly AI digest, a daily briefing, personal
branding, a LinkedIn content toolkit, newsletters, writing quality, and visual artifacts.

The canonical source of truth is [`.agents/`](.agents/); thin runtime adapters point back to
it. Every skill follows the same contract — **Role → Context → Workflow (Step 0 TodoWrite
checklist → Steps)** — loads your profile, and asks instead of hallucinating. See
[.agents/docs/skill-authoring.md](.agents/docs/skill-authoring.md).

---

## Install (npm)

```bash
npm install --global personal-assistant-skills
```

Create your config from the bundled templates, then set the env var:

```bash
assistant-skills init                       # writes to ~/.assistant/
setx ASSISTANT_CONFIG "$HOME\.assistant\config.json"   # Windows
# export ASSISTANT_CONFIG="$HOME/.assistant/config.json"  # macOS/Linux
```

CLI commands:

| Command                              | What it does                                        |
| ------------------------------------ | --------------------------------------------------- |
| `assistant-skills init [--dir <p>]`  | Create `config.json` + `content.md` + `memory.md` + `notes.md` |
| `assistant-skills list`              | List the available skills                           |
| `assistant-skills install <dir>`     | Copy the `.agents` tree into a project              |
| `assistant-skills path`              | Print the installed `.agents` directory             |

Fill in `config.json` (profile, brand, sources) — see **[CONFIGURATION.md](CONFIGURATION.md)**.

---

## Slash commands

Every skill is exposed under an **`/assistant`** umbrella so you can invoke it explicitly:

```
/assistant:me linkedin AI agents are changing how we test
/assistant:linkedin post why flaky tests are a design problem
/assistant:ai-digest 2026-02-27
/assistant:daily-digest google morning
/assistant:pixel diagram AI test pipeline
/assistant:hook why most roadmaps are fiction
/assistant:cold-email VP Eng at Acme, book a demo
```

- **Claude Code** loads commands from [.claude/commands/assistant/](.claude/commands/assistant) →
  `/assistant:me`, `/assistant:linkedin`, `/assistant:post`, `/assistant:ai-digest`, …
- **GitHub Copilot** loads prompt files from [.github/prompts/](.github/prompts). Copilot has no
  `:` namespace, so the same set is invoked as `/assistant-me`, `/assistant-linkedin`,
  `/assistant-post`, …

Each command is thin: it points at the canonical `SKILL.md` and passes your text as
`$ARGUMENTS`, so behavior stays identical across runtimes. `assistant-skills install <dir>`
copies the commands and prompts into a target project alongside `.agents/`.

Full command reference with 2–3 examples each: **[.agents/docs/usage.md](.agents/docs/usage.md)**.

---

## Add to your assistant

### Claude Code (marketplace or local)

Claude discovers skills from `.agents/skills/**/SKILL.md` and commands from `.claude/commands/assistant/`.
Use the CLI to drop them into your project, or point Claude at this repo directly:

```bash
# Embed in a project (.agents + .claude/commands + .github/prompts):
assistant-skills install .

# Or point Claude at the canonical tree directly:
claude --plugin-dir "$(assistant-skills path)/.."
```

Then run e.g. `/assistant:linkedin post <topic>`. Repository instructions are surfaced through
[CLAUDE.md](CLAUDE.md) → [.agents/AGENTS.md](.agents/AGENTS.md).

### GitHub Copilot

Copilot reads [.github/copilot-instructions.md](.github/copilot-instructions.md), which points
to the canonical `.agents/`, and prompt files in [.github/prompts/](.github/prompts). Copy them
into your repo (or `assistant-skills install .`), then invoke a skill in Copilot Chat with its
slash command, e.g. `/assistant-linkedin post <topic>` or `/assistant-daily-digest google morning`.
Enable prompt files with the `chat.promptFiles` setting in VS Code.

### Codex

Codex reads the root [AGENTS.md](AGENTS.md) → [.agents/AGENTS.md](.agents/AGENTS.md). Skills
live in `.agents/skills/**/SKILL.md`.

---

## External capabilities (MCP)

Gmail, Google Calendar, and LinkedIn publish/fetch are **not** reimplemented here — they come
from the [`connected-workspace`](https://www.npmjs.com/package/connected-workspace-mcp) MCP
server, declared in [.agents/mcp/connected-workspace.json](.agents/mcp/connected-workspace.json).

```bash
npm install --global connected-workspace-mcp
```

Register it in your MCP host and require confirmation for write tools (send email, modify
calendar, publish/delete posts). The `daily-digest` skill uses these for Gmail/Google Calendar,
and your host's internal M365 tools for Outlook/Teams/calendar.

---

## Skills

| Skill              | What it does                                                       |
| ------------------ | ----------------------------------------------------------------- |
| `me`               | Bios, pitches, headlines, and posts in your voice                 |
| `ai-digest`        | Weekly AI news digest as a self-contained HTML file               |
| `daily-digest`     | "Daily Happenings" briefing from Outlook/Teams/M365 or Gmail/GCal |
| `pixel`            | Diagrams, banners, slides, charts, infographics                   |
| `newsletter`       | Generate, deploy (FTP), and track branded newsletters             |
| `humanize`         | Rewrite prose to sound natural, direct, and human                 |
| `email/*`          | `cold-email`, `follow-up-email`                                    |
| `writing/*`        | `readability`, `word-stats`                                        |
| `linkedin/*`       | Hub + `post`, `hook`, `carousel`, `post-planner`, `post-review`, `repurpose`, `positioning`, `content-pillars`, `comment`, `connect`, `collab`, `profile`, `newsletter` |

Run `assistant-skills list` for the full set.

---

## Repository layout

```text
.agents/
├── AGENTS.md            # Canonical repo instructions (read first)
├── manifest.yaml        # Directory + runtime + config + mcp map
├── skills/              # One folder per skill, each with SKILL.md
├── commands/            # Portable command definitions
├── mcp/                 # connected-workspace MCP definition
├── templates/           # Shared HTML/SVG artifact templates
├── scripts/             # assistant_config.py, memory.py + per-skill helpers
├── config/              # config/content/memory/notes templates + adapters
└── docs/                # skill-authoring.md
bin/cli.js               # assistant-skills CLI
AGENTS.md / CLAUDE.md / .github/copilot-instructions.md  # runtime entry points
```

---

## Publishing (maintainers)

CI runs on every push/PR ([.github/workflows/ci.yml](.github/workflows/ci.yml)): validates the
config template, byte-compiles the Python scripts, and checks every skill has a `## Role` and a
Step 0 `TodoWrite` with balanced code fences.

To publish to npm, add an `NPM_TOKEN` repository secret, then create a GitHub Release (or push a
`v*` tag). [.github/workflows/publish.yml](.github/workflows/publish.yml) runs
`npm publish --provenance --access public`.

```bash
npm version patch    # or minor / major
git push --follow-tags
# then publish a GitHub Release for that tag
```

---

## Security

Never commit `config.json`, `content.md`, `memory.md`, `notes.md`, `.env`, tokens, or logs.
The `connected-workspace` MCP server manages OAuth credentials in its own env file — keep
secrets out of `config.json`.

## License

MIT
