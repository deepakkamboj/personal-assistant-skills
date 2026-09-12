# .agents — Canonical Agent System

`.agents/` is the vendor-neutral source of truth for this personal-assistant plugin.
It works across Claude Code, GitHub Copilot, Codex, and other agent runtimes through
thin adapters that point back here.

```text
.agents/
├── AGENTS.md              # Repository agent instructions (canonical)
├── manifest.yaml          # Directory + runtime + config + mcp map
├── skills/                # One directory per skill, each with a SKILL.md
│   ├── me/                # Personal branding (bios, posts, pitches)
│   ├── ai-digest/         # Weekly AI news digest
│   ├── daily-digest/      # "Daily Happenings" briefing (M365 + Google)
│   ├── pixel/             # Visual artifacts (diagrams, banners, slides)
│   ├── newsletter/        # Full newsletter system
│   ├── humanize/          # Natural writing-style editor
│   ├── email/             # cold-email, follow-up-email
│   ├── writing/           # readability, word-stats
│   └── linkedin/          # Hub + content sub-skills (hook, carousel, post, …)
├── commands/              # Portable command definitions
├── mcp/                   # MCP server definitions (connected-workspace)
├── templates/             # Shared HTML/SVG artifact templates (pixel)
├── scripts/               # Shared helper scripts (assistant_config.py + per-skill)
├── config/                # Config + content templates + runtime adapters
│   ├── config.example.json
│   ├── content.example.md
│   └── adapters/{claude,github,codex}/
└── docs/
```

## Principles

1. Keep reusable knowledge vendor-neutral.
2. Repository-specific instructions live in `.agents/AGENTS.md`.
3. Every skill has its own directory and `SKILL.md` (no `skill.json`).
4. Prefer relative paths and portable scripts.
5. Never put secrets in agent configuration.
6. Runtime adapters stay thin.

## Configuration

See `.agents/AGENTS.md` → Configuration. One `config.json` (via `ASSISTANT_CONFIG`) plus one
`content.md` companion file replace the old `data/` folder.
