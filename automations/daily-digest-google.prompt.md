# Daily Digest — Google

> The same "Daily Happenings" briefing from your **personal** Google account: Gmail and Google
> Calendar, via the connected-workspace MCP.

- **Skill:** `/assistant-daily-digest` (Claude Code: `/assistant:daily-digest`)
- **Runs in:** Microsoft 365 Copilot · GitHub Copilot · **Microsoft Scout** (great for personal accounts)
- **Schedule:** Weekdays 7:00 AM
- **Data source:** Google — Gmail + Google Calendar via the `connected-workspace` MCP
- **Reads:** `config.profile`, `memory.md`, `notes.md`
- **Prerequisites:** `connected-workspace` MCP connected to your Google account

## Prompt to paste

```text
Run the daily-digest skill in Google (personal) mode for today's morning briefing.

Use the connected-workspace MCP tools:
- gmail_search for unread/important mail from the last 24h; gmail_get_message for details.
- calendar_list_events for today; calendar_free_busy to flag conflicts and free slots.

Then produce the "Daily Happenings" digest with these sections, in my voice:
### Needs you today (N)   — sender, subject, why it matters, the action
### Calendar (N events)   — start–end, title, location/link, prep or conflict
### FYI / read later (N)  — sender, subject
### Suggested focus       — 2–3 sentences on the top 1–2 things to do first

Rank by urgency and by people/projects in memory.md. Do NOT send or archive anything.
Append any follow-ups you spot to notes.md.

Delivery: post this briefing to every configured target in config.delivery, reusing the SAME
session/thread each run (session_key: daily-digest-google). See _shared.md.
```

## Delivery & session

Posts to **Teams · Microsoft Scout · this chat**, reusing the same thread/session every run via
`session_key: daily-digest-google`. Configure targets in `config.delivery` and paste the delivery
footer from [_shared.md](_shared.md); thread/session IDs persist in `output/automations/state.json`.

## Steps (what the assistant does)

1. Calls `gmail_search` / `gmail_get_message` for unread + important mail.
2. Calls `calendar_list_events` + `calendar_free_busy` for today's schedule and gaps.
3. Ranks by urgency and by `memory.md` people/projects.
4. Assembles the briefing and logs follow-ups to `notes.md`.

## Output & delivery

- **Chat/Markdown briefing** (Needs you / Calendar / FYI / Suggested focus).
- **Follow-ups** appended to `notes.md`.
- Read-only: nothing is sent, archived, or modified.

## Run it in each app

### Microsoft Scout
1. Best fit for personal Google — connect Gmail/Calendar, paste the prompt, schedule weekday mornings.
2. Let Scout deliver the briefing to chat or forward it to your inbox.

### GitHub Copilot
1. With the `connected-workspace` MCP available, invoke `/assistant-daily-digest` in Copilot Chat.
2. Schedule via a GitHub Actions cron (`0 7 * * 1-5`) running the Copilot CLI + MCP.

### Microsoft 365 Copilot
1. Works if the Google MCP is reachable from your Copilot environment; otherwise use the
   [Microsoft / Work](daily-digest-microsoft.prompt.md) recipe for work data.

## Variations

- **Unified view:** run both this and the Microsoft recipe, then add "Merge both briefings into one,
  de-duplicated, labeled [work]/[personal]."
- **Free-time finder:** append "List my three longest free blocks today for focus work."
- **Auto-draft replies:** hand items to [Inbox Triage & Follow-ups](inbox-triage-followups.prompt.md)
  to stage (not send) responses.
