# LinkedIn Weekly Plan

> Plan a week of LinkedIn content — topics, angles, formats, and cadence across your pillars — ready
> to feed the daily post automation.

- **Skill:** `/assistant-post-planner` (Claude Code: `/assistant:post-planner`)
- **Runs in:** Microsoft Scout · GitHub Copilot · M365 Copilot
- **Schedule:** Mondays 8:00 AM
- **Session key:** `linkedin-weekly-plan`
- **Data source:** `config.profile.content_pillars`, recent posts (`linkedin_list_posts`), `memory.md`
- **Prerequisites:** `profile.content_pillars` set; MCP for post history (optional)

## Prompt to paste

```text
Run the post-planner skill for the coming week (Mon–Fri).

1. Load my profile, content pillars, and voice; check recent posts via linkedin_list_posts to avoid
   repeats and spot what's performing.
2. Propose a 5-day plan: for each weekday give a topic, angle, format (text / carousel / image),
   the pillar it serves, and a one-line hook idea.
3. Balance the week across my pillars; include at least one personal-story angle and one
   contrarian/POV angle.
4. Output a table (day, pillar, format, topic, hook) plus a short note on the week's theme.

Delivery: post this plan to every configured target in config.delivery, reusing the SAME
session/thread each run (session_key: linkedin-weekly-plan). See _shared.md.
```

## Delivery & session

Posts the weekly plan to **Teams · Microsoft Scout · this chat**, reusing the same thread/session
every run via `session_key: linkedin-weekly-plan`. Configure targets in `config.delivery` and paste
the delivery footer from [_shared.md](_shared.md).

## Steps (what the assistant does)

1. Loads pillars/voice; reviews recent posts for gaps and winners.
2. Drafts a balanced 5-day plan across pillars and formats.
3. Returns a day/pillar/format/topic/hook table + weekly theme note.

## Output & delivery

- **Weekly plan table** + theme note (saved to chat/Teams/Scout).
- Feeds [LinkedIn Daily Post](linkedin-daily-post.prompt.md): each morning pulls that day's row.

## Run it in each app

### Microsoft Scout
1. Schedule a Monday-morning task; keep one Scout session for the plan and the daily posts.

### GitHub Copilot
1. Invoke `/assistant-post-planner`; commit the plan to `output/linkedin/plan-{week}.md` via an Actions
   cron for the daily job to read.

### Microsoft 365 Copilot
1. Generate the plan; pin it in the Teams channel your daily posts thread into.

## Variations

- **Monthly calendar:** change "coming week" → "next 4 weeks" and group by theme.
- **Pillar refresh:** run `/assistant-content-pillars` first if your pillars feel stale.
