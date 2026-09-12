# Commands

Portable command definitions map to the skills under `.agents/skills/`. Concrete, runtime-ready
commands are generated from these into `.claude/commands/assistant/<cmd>.md` (Claude Code, invoked
as `/assistant:<cmd>`) and `.github/prompts/assistant-<cmd>.prompt.md` (GitHub Copilot, invoked as
`/assistant-<cmd>`). Each is thin and points at the canonical `SKILL.md`, passing your text as
`$ARGUMENTS`.

Usage examples for every command: [../docs/usage.md](../docs/usage.md).

| Command            | Skill                        | Purpose                                               |
| ------------------ | ---------------------------- | ----------------------------------------------------- |
| `/me`              | `me`                         | Bios, pitches, headlines, posts in your voice         |
| `/ai-digest`       | `ai-digest`                  | Weekly AI news digest as a self-contained HTML file   |
| `/daily-digest`    | `daily-digest`               | Daily Happenings briefing (M365 + Google)             |
| `/pixel`           | `pixel`                      | Diagrams, banners, slides, charts, infographics       |
| `/newsletter`      | `newsletter`                 | Generate, deploy, and track branded newsletters       |
| `/humanize`        | `humanize`                   | Rewrite prose to sound natural and direct             |
| `/cold-email`      | `email/cold-email`           | Draft cold emails (AIDA/PAS/BAB)                       |
| `/follow-up-email` | `email/follow-up-email`      | Draft re-engagement follow-ups                        |
| `/readability`     | `writing/readability`        | Flesch-Kincaid / Gunning Fog / SMOG scores            |
| `/word-stats`      | `writing/word-stats`         | Word/char/reading-time statistics                     |
| `/linkedin`        | `linkedin`                   | LinkedIn hub (routes to sub-skills)                   |
| `/post`            | `linkedin/post`              | Draft a LinkedIn post in your voice                   |
| `/post-planner`    | `linkedin/post-planner`      | Plan a LinkedIn content calendar                      |
| `/hook`            | `linkedin/hook`              | Generate scroll-stopping post hooks                   |
| `/carousel`        | `linkedin/carousel`          | Draft multi-slide LinkedIn carousels                  |
| `/post-review`     | `linkedin/post-review`       | Score and improve a draft post                        |
| `/repurpose`       | `linkedin/repurpose`         | Repurpose content across formats                      |
| `/positioning`     | `linkedin/positioning`       | Sharpen positioning and value proposition             |
| `/content-pillars` | `linkedin/content-pillars`   | Define content pillars                                |
| `/comment`         | `linkedin/comment`           | Draft engagement comments                             |
| `/connect`         | `linkedin/connect`           | Draft connection-request notes                        |
| `/collab`          | `linkedin/collab`            | Draft collaboration outreach                          |
| `/profile`         | `linkedin/profile`           | Audit and improve your LinkedIn profile               |
| `/newsletter-li`   | `linkedin/newsletter`        | Draft a LinkedIn newsletter edition                   |

Publishing to LinkedIn, and reading/sending email or calendar, are provided by the
`connected-workspace` MCP server (see `.agents/mcp/`), not by these commands.
