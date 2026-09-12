# Claude Code — Project Instructions

This repository uses a vendor-neutral `.agents/` agent system as the single source of truth.

**Read `.agents/AGENTS.md` first.** Skills are discovered from `.agents/skills/<skill>/SKILL.md`.

- Configuration: single `config.json` via the `ASSISTANT_CONFIG` env var (fallback
  `~/.assistant/config.json`) plus a `content.md` companion. No `data/` folder.
- Email, calendar, and LinkedIn publishing come from the `connected-workspace` MCP server
  (`.agents/mcp/connected-workspace.json`), not local scripts.
- Templates for the `pixel` skill live in `.agents/templates/`.
