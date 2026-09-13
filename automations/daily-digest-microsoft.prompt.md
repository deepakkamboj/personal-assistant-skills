# Daily Digest — Microsoft / Work

> A prioritized "Daily Happenings" briefing from your **work** account: Outlook mail, Teams messages,
> and your Microsoft 365 calendar.

- **Skill:** `/assistant-daily-digest` (Claude Code: `/assistant:daily-digest`)
- **Runs in:** **Microsoft 365 Copilot** (best) · GitHub Copilot · Microsoft Scout
- **Schedule:** Weekdays 7:00 AM (morning) and 5:30 PM (end-of-day wrap)
- **Data source:** Microsoft 365 — Outlook mail, Teams, M365 calendar (via Microsoft Graph)
- **Reads:** `config.profile`, `memory.md`, `notes.md`
- **Prerequisites:** host exposes M365 work tools (native in M365 Copilot)

## Prompt to paste

```text
Run the daily-digest skill in Microsoft 365 (work) mode for today's morning briefing.

Use my work tools:
- Outlook mail: unread + flagged from the last 24h.
- Teams: unread @mentions, DMs, and channel messages that need a reply.
- Calendar: today's events, with locations/links and any conflicts or missing prep.

Then produce the "Daily Happenings" digest with these sections, in my voice:
### Needs you today (N)   — source, who, subject, why it matters, the action
### Calendar (N events)   — start–end, title, location/link, prep or conflict
### Chat highlights (N)   — channel/DM, who, summary, reply needed?
### FYI / read later (N)  — source, sender, subject
### Suggested focus       — 2–3 sentences on the top 1–2 things to do first

Rank by urgency and by people/projects in memory.md. Do NOT send replies — this is a briefing.
Append any follow-ups you spot to notes.md.

Delivery: post this briefing to every configured target in config.delivery, reusing the SAME
session/thread each run (session_key: daily-digest-microsoft). See _shared.md.
```

## Delivery & session

Posts to **Teams · Microsoft Scout · this chat**, reusing the same thread/session every run via
`session_key: daily-digest-microsoft`. Configure targets in `config.delivery` and paste the delivery
footer from [_shared.md](_shared.md); thread/session IDs persist in `output/automations/state.json`.

## Steps (what the assistant does)

1. Reads unread/flagged Outlook mail, Teams @mentions/DMs, and today's calendar.
2. Scores each item by urgency and by the people/projects tracked in `memory.md`.
3. Assembles the five-section "Daily Happenings" briefing in your voice.
4. Records any spotted follow-ups to `notes.md`.

## Output & delivery

- **Chat/Markdown briefing** with the five sections above.
- **Follow-ups** appended to `notes.md` for later action.
- Read-only: no messages are sent.

## Run it in each app

### Microsoft 365 Copilot
1. Best fit — Outlook/Teams/Calendar are available natively via Graph.
2. Save the prompt; add it as a **scheduled prompt** (if enabled) or a **Copilot Studio** agent with
   two daily triggers (7:00 AM, 5:30 PM). The 5:30 PM run can use "end of day" wrap wording.

### GitHub Copilot
1. Works if a Microsoft Graph MCP/connector is wired in; otherwise prefer the Google recipe here.
2. Schedule via GitHub Actions cron and post the briefing to an issue / Teams webhook.

### Microsoft Scout
1. Create a scheduled task, connect your work Microsoft account, paste the prompt.
2. Set two recurrences (morning + end of day); have Scout deliver the briefing to chat or email.

## Variations

- **End-of-day wrap:** change "morning briefing" → "end-of-day wrap: what slipped, what's due
  tomorrow, and what to prep tonight."
- **Meeting prep:** append "For each meeting, list attendees, the last related thread, and 2 talking
  points."
- **Triage mode:** hand the "Needs you today" list to
  [Inbox Triage & Follow-ups](inbox-triage-followups.prompt.md).
