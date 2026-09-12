# Claude Code Adapter

Exposes the canonical `.agents/` assets to Claude Code.

Mapping:
- Repository instructions → root `CLAUDE.md` (points to `.agents/AGENTS.md`)
- Skills → discovered from `.agents/skills/<skill>/SKILL.md`
- MCP → register `connected-workspace` from `.agents/mcp/connected-workspace.json`
- Templates → `.agents/templates/`

Skills are plain folders with a `SKILL.md` (YAML frontmatter: `name`, `description`,
optional `argument-hint`). No `skill.json`, no `.claude-plugin` manifest.

Keep `.agents/` as the source of truth. Do not diverge copies.
