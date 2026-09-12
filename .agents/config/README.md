# Configuration

All user data lives in **two** files, plus **two** shared memory files (there is no `data/` folder):

| File         | Purpose                                                                    | Template               |
| ------------ | -------------------------------------------------------------------------- | ---------------------- |
| `config.json`| Structured data: profile, brand tokens, digest sources, newsletter settings | `config.example.json`  |
| `content.md` | Prose: writing voice/samples, graphics prompts, template guidance          | `content.example.md`   |
| `memory.md`  | Durable learned facts/preferences that keep improving your profile         | `memory.example.md`    |
| `notes.md`   | Running task/session notes and follow-ups                                  | `notes.example.md`     |

Skills read all four at the start of a run and append new facts/notes to `memory.md` /
`notes.md`. Helper: `python .agents/scripts/memory.py remember|note "..."`.

## Setup

1. Copy the templates to a private location (outside the repo is recommended):

   ```powershell
   New-Item -ItemType Directory -Force ~/.assistant | Out-Null
   Copy-Item .agents/config/config.example.json  ~/.assistant/config.json
   Copy-Item .agents/config/content.example.md   ~/.assistant/content.md
   Copy-Item .agents/config/memory.example.md    ~/.assistant/memory.md
   Copy-Item .agents/config/notes.example.md     ~/.assistant/notes.md
   ```

2. Point the `ASSISTANT_CONFIG` environment variable at your `config.json`:

   ```powershell
   setx ASSISTANT_CONFIG "$HOME\.assistant\config.json"
   ```

   If unset, skills and scripts fall back to `~/.assistant/config.json`.

3. The companion prose file path is read from `config.paths.content` (default: `content.md`
   next to `config.json`).

## Resolution order

1. `ASSISTANT_CONFIG` environment variable
2. `~/.assistant/config.json`

Never commit a real `config.json`, `content.md`, `memory.md`, or `notes.md` — they may
contain personal data.

## Adapters

`adapters/{claude,github,codex}/` document how each runtime exposes the canonical `.agents` assets.
