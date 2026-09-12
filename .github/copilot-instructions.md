# GitHub Copilot — Repository Instructions

This repository uses a vendor-neutral `.agents/` agent system as the single source of truth.

**Read `.agents/AGENTS.md` first.** Skills are discovered from `.agents/skills/<skill>/SKILL.md`.

Key conventions:
- Configuration is a single `config.json` resolved from the `ASSISTANT_CONFIG` environment
  variable (fallback `~/.assistant/config.json`), plus a `content.md` companion for prose,
  voice samples, and prompts. There is no `data/` folder.
- Email (Gmail), calendar, and LinkedIn publishing/fetching are provided by the
  `connected-workspace` MCP server (`.agents/mcp/connected-workspace.json`). Prefer those MCP
  tools over writing new scripts for those capabilities.
- Shared artifact templates live in `.agents/templates/`.
- Every skill is a folder with a `SKILL.md` (YAML frontmatter). Do not add `skill.json`.
- Skills are invocable as slash commands via prompt files in `.github/prompts/` (e.g.
  `/assistant-me`, `/assistant-linkedin`, `/assistant-post`, `/assistant-ai-digest`). Each
  prompt just points at the canonical `SKILL.md`; enable them with the `chat.promptFiles`
  VS Code setting. (Claude Code uses the `/assistant:<name>` form.)
