# Automations

Ready-to-run automation recipes built on **personal-assistant-skills**. Each file is a self-contained
prompt you can paste into — or schedule from — three hosts:

- **Microsoft 365 Copilot** — best for *work* data (Outlook mail, Teams, M365 calendar) via Microsoft Graph.
- **GitHub Copilot** (app / CLI / Chat) — best for repo-adjacent runs and cron scheduling via GitHub Actions.
- **Microsoft Scout** — best for personal, always-on scheduled agent tasks and account connectors.

Every recipe maps to a skill in [`.agents/skills/`](../.agents/skills) and follows the same layout:
purpose → prompt to paste → steps → output/delivery → how to run in each app → variations.

## Delivery & session

Every recipe **posts its report to Microsoft Teams, Microsoft Scout, and the chat session**, and
**reuses the same thread/session on every run** (keyed by a stable `session_key`) so recurring reports
stack in one place. Configure targets in `config.delivery` and see the full model + copy-paste
delivery footer in [`_shared.md`](_shared.md). Thread/session IDs persist in
`output/automations/state.json`.

## Catalog

| Automation | Skill | Data source | Typical schedule |
|------------|-------|-------------|------------------|
| [Daily AI Digest](daily-ai-digest.prompt.md) | `ai-digest` | Web sources in `config.digest.sources` | Weekdays 6:30 AM |
| [Daily Digest — Microsoft / Work](daily-digest-microsoft.prompt.md) | `daily-digest` | Outlook · Teams · M365 Calendar | Weekdays 7:00 AM & 5:30 PM |
| [Daily Digest — Google](daily-digest-google.prompt.md) | `daily-digest` | Gmail · Google Calendar (MCP) | Weekdays 7:00 AM |
| [Weekly Newsletter](weekly-newsletter.prompt.md) | `newsletter` | `config.digest.sources` + settings | Fridays 9:00 AM |
| [LinkedIn Daily Post](linkedin-daily-post.prompt.md) | `linkedin` / `post` | Your pillars + recent digest | Weekdays 8:00 AM |
| [LinkedIn Weekly Plan](linkedin-weekly-plan.prompt.md) | `post-planner` | `config.profile.content_pillars` | Mondays 8:00 AM |
| [Personal Brand Refresh](personal-brand-refresh.prompt.md) | `me` / `profile` | `config.profile` + `content.md` | Monthly |
| [Inbox Triage & Follow-ups](inbox-triage-followups.prompt.md) | `daily-digest` + `follow-up-email` | Mail (M365 or Gmail) | Weekdays 8:30 AM |

## Prerequisites (once)

1. **Config:** set `ASSISTANT_CONFIG` (fallback `~/.assistant/config.json`) and fill `profile`,
   `brand`, `digest.sources`, and `newsletter.settings`. Voice samples go in `content.md`.
   See [Getting started](../website/pages/getting-started.mdx).
2. **Google / LinkedIn actions:** require the [`connected-workspace`](../.agents/mcp/connected-workspace.json)
   MCP server (Gmail, Google Calendar, LinkedIn tools).
3. **Microsoft / work actions:** require the host to expose Microsoft 365 work tools (Outlook, Teams,
   calendar) — native in M365 Copilot.
4. **Publishing:** newsletter deploy needs FTP settings in `config.newsletter.settings`; LinkedIn/Gmail
   sending goes through the MCP.

## Safety

- These recipes **draft and stage** by default. Any send/publish/deploy step is called out explicitly
  and should stay **review-before-send** unless you deliberately enable auto-send in the host.
- Never paste secrets into a prompt. Credentials live in the MCP server / host connectors, not here.
