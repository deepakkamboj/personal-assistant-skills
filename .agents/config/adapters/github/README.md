# GitHub Copilot Adapter

Exposes the canonical `.agents/` assets to GitHub Copilot.

Mapping:
- Repository instructions → `.github/copilot-instructions.md` (points to `.agents/AGENTS.md`)
- Skills → discovered from `.agents/skills/<skill>/SKILL.md`
- MCP → configure `connected-workspace` in your MCP host from `.agents/mcp/connected-workspace.json`

Keep canonical instructions under `.agents/`. The Copilot entry file is intentionally thin.
