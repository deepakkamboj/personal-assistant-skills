# Contributing

Thanks for helping improve **personal-assistant-skills** — a vendor-neutral agent plugin that
runs across Claude Code, GitHub Copilot, and Codex.

## Ground rules

- The canonical source of truth is [`.agents/`](.agents/). Runtime adapters (`CLAUDE.md`,
  `.github/copilot-instructions.md`, root `AGENTS.md`, `.claude/commands/`, `.github/prompts/`)
  must stay thin and point back to it — never duplicate skill instructions.
- **Never commit secrets.** `config.json`, `content.md`, `memory.md`, `notes.md`, and `.env` are
  gitignored. Keep tokens out of tracked files.
- No personal data in templates. `config.example.json` and the `*.example.*` files use
  placeholders only.

## Project layout

See [README.md](README.md) and [.agents/README.md](.agents/README.md). In short:

```
.agents/
├── skills/     # one folder per skill, each a SKILL.md
├── scripts/    # shared Python helpers (assistant_config.py, memory.py)
├── config/     # config/content/memory/notes templates + adapters
├── mcp/        # connected-workspace MCP definition
├── templates/  # shared HTML/SVG artifact templates
├── commands/   # portable command map
└── docs/       # skill-authoring.md, usage.md
bin/cli.js      # assistant-skills CLI
```

## Adding or changing a skill

Every skill follows the same contract (full spec in
[.agents/docs/skill-authoring.md](.agents/docs/skill-authoring.md)):

1. A folder under `.agents/skills/<name>/` with a single `SKILL.md` (YAML frontmatter:
   `name` matching the folder, `description`, optional `argument-hint`). No `skill.json`.
2. Body sections in order: `## Role` → `## Context to load` → `## Workflow`
   (starting with a `### Step 0: TodoWrite Checklist`) → `### Steps` → skill-specific sections.
3. Load `config.profile` and the shared `memory.md` / `notes.md`; ask for missing input rather
   than inventing it.
4. Regenerate the slash commands so Claude/Copilot pick up the new skill, then add a
   usage example to [.agents/docs/usage.md](.agents/docs/usage.md).

External capabilities (Gmail, Google Calendar, LinkedIn publishing) belong in the
`connected-workspace` MCP server, not in new skills or scripts.

## Local checks

Run these before opening a PR (the same checks run in CI):

```bash
# Validate the config template JSON
node -e "JSON.parse(require('fs').readFileSync('.agents/config/config.example.json','utf8'))"

# Byte-compile the Python scripts
python -m py_compile .agents/scripts/**/*.py

# Sanity-check the CLI
node bin/cli.js list
```

Every `SKILL.md` must have a `## Role`, a `### Step 0: TodoWrite Checklist`, and balanced code
fences — CI enforces this.

## Commit & PR

- Use clear, present-tense commit messages.
- Keep changes focused; update docs (`README.md`, `.agents/docs/usage.md`) when behavior changes.
- Describe what changed, what you validated, and any follow-ups in the PR description.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
