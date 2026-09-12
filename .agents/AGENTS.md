# Repository Agent Instructions

## Mission

Provide a consistent, safe, vendor-neutral way for AI coding assistants (Claude Code,
GitHub Copilot, Codex, and others) to run the personal-assistant skills in this repository.

## Source of truth

- Skills: `.agents/skills/`
- Commands: `.agents/commands/`
- MCP definitions: `.agents/mcp/`
- Templates: `.agents/templates/`
- Scripts: `.agents/scripts/`
- Config: `.agents/config/`

Runtime adapters (`CLAUDE.md`, `.github/copilot-instructions.md`, root `AGENTS.md`) are thin
and only point back to this canonical tree. Never duplicate skill instructions into adapters.

## Configuration

All user data lives in a single JSON config plus one companion prose file:

- `config.json` — structured data (profile, brand tokens, digest sources, newsletter settings).
  Resolved from the `ASSISTANT_CONFIG` environment variable, falling back to `~/.assistant/config.json`.
- `content.md` — voice samples, graphics prompts, and template guidance. Path is in `config.paths.content`
  (default: `content.md` next to the config file).

Templates: `.agents/config/config.example.json` and `.agents/config/content.example.md`.
There is no `data/` folder. Never commit a real `config.json` (it may contain personal data).

## External capabilities via MCP

Email (Gmail), calendar (Google Calendar), and LinkedIn publishing/fetching are NOT skills in this
repo — they are provided by the `connected-workspace` MCP server (see `.agents/mcp/`). Skills that
need to send email or publish to LinkedIn should call the MCP tools, not local scripts.

## Skill authoring pattern (applies to every skill)

Full spec: `.agents/docs/skill-authoring.md`. In short, every skill:

1. **Defines Role → Context → Workflow.** Each `SKILL.md` opens with a `## Role` (who the
   assistant is and what it produces), a `## Context to load` (profile, content, memory, and
   skill-specific config), then a `## Workflow` that starts with a `### Step 0: TodoWrite
   Checklist`. Create that checklist first, then complete each task in order before the next.
2. **Loads the user's profile first.** Every skill reads `config.profile` (identity, role,
   voice, brand, content pillars) and personalizes its output to that person. Never produce
   generic output when a profile is available; if the profile lacks a field the skill needs,
   ask for it.
3. **Maintains shared profile memory.** Every skill also reads the shared `memory.md`
   (durable learned facts/preferences) and `notes.md` (running task notes), and appends new,
   confirmed facts or follow-ups back to them so the profile keeps improving. Paths come from
   `config.paths.memory` / `config.paths.notes` (default `memory.md` / `notes.md` next to
   `config.json`). Helper: `python .agents/scripts/memory.py remember|note "..."`.
4. **Asks instead of hallucinating.** If a required input is missing, stop and ask a specific
   question. Never fabricate facts, numbers, names, quotes, or sources. (Skills flagged to
   return immediately, like `word-stats`, still run the workflow but skip the "ask" step when
   the input is already present.)
5. **Reads configuration, not a `data/` folder.** Structured data from `config.json`
   (`ASSISTANT_CONFIG`), prose/prompts from `content.md` (`config.paths.content`).

## Operating rules

1. Read this file before performing repository work.
2. Inspect the relevant `SKILL.md` before executing a specialized task.
3. Follow the repository's existing coding, testing, security, and documentation conventions.
4. Prefer the smallest safe change.
5. Never expose secrets, tokens, credentials, or personal config.
6. Load configuration through the resolver, never hard-code paths.
7. Report what changed, what was validated, and any remaining risks.
8. Do not invent APIs, files, or requirements.

## Change workflow

Understand → Plan → Implement → Validate → Review → Summarize
