# Repository Agent Instructions (Codex entry)

This repository uses a vendor-neutral `.agents/` agent system as the single source of truth.

**Read `.agents/AGENTS.md` first** — it defines the skills, configuration model, and operating rules.

Quick facts:
- Skills live in `.agents/skills/<skill>/SKILL.md` (no `skill.json`).
- Configuration is a single `config.json` resolved from the `ASSISTANT_CONFIG` env var
  (fallback `~/.assistant/config.json`) plus a `content.md` companion. There is no `data/` folder.
- Email, calendar, and LinkedIn publishing are provided by the `connected-workspace` MCP server
  (`.agents/mcp/`), not by local scripts.
