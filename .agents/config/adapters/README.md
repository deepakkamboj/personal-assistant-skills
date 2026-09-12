# Runtime Adapters

Adapters translate the canonical `.agents/` assets to runtime-specific conventions.
They are thin: no business logic, no duplicated skill instructions.

- **Claude Code** → `claude/` (entry: `CLAUDE.md`)
- **GitHub Copilot** → `github/` (entry: `.github/copilot-instructions.md`)
- **Codex** → `codex/` (entry: root `AGENTS.md`)
