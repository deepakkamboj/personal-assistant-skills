---
name: daily-digest
description: >
  Produce a "Daily Happenings" briefing that summarizes the day's email, chat
  messages, and calendar into one prioritized digest. Supports Microsoft 365
  (Outlook mail, Teams messages, Outlook/M365 calendar) via the host's internal
  work tools, and Google (Gmail, Google Calendar) via the connected-workspace MCP
  server. Use when the user asks for a daily/morning briefing, "what's happening
  today", an inbox + calendar catch-up, or an end-of-day summary.
user-invocable: true
argument-hint: "[microsoft|google|both] [date: today|YYYY-MM-DD] [morning|eod]"
---

# Daily Happenings

Pull together the day's mail, chats, and calendar into a single, prioritized briefing
so the user can see what needs attention without opening five apps.

This skill does not fetch data with local Python scripts. It calls the tools the host
runtime already provides:

- **Microsoft 365 (work):** the host's internal Outlook mail, Teams, and calendar tools.
  These are available when running inside the internal environment.
- **Google (personal):** the `connected-workspace` MCP server tools — `gmail_search`,
  `gmail_get_message`, `calendar_list_events`, `calendar_free_busy`.

## Role

You are the user's daily briefing assistant. You summarize their mail, chats, and calendar into one prioritized "Daily Happenings" digest.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups
- Provider tools: internal M365 (Outlook/Teams/calendar) or connected-workspace MCP (Gmail/Google Calendar)

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Collect, triage, and summarize the day's mail, chats, and calendar", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse `$ARGUMENTS`:
   - Provider: `microsoft`, `google`, or `both` (default `both`).
   - Date: `today` (default) or `YYYY-MM-DD`.
   - Mode: `morning` (look ahead + overnight items) or `eod` (recap the day). Default `morning`.
2. **Load your profile.** Read `config.profile` (name, role, company, content pillars,
   priorities) so triage reflects what matters to this person, and `content.md` voice for the
   summary tone. Read the shared `memory.md` / `notes.md` for standing priorities and open
   follow-ups to surface.
3. **Confirm access before assuming.** For each requested provider, check the tools are
   available:
   - Microsoft: internal Outlook/Teams/calendar tools present.
   - Google: `connected-workspace` MCP registered and authorized.
   If a requested provider is unavailable, tell the user which one and continue with what is
   available — do not invent messages or events.
4. **Collect the day's items** (only from real tool responses):
   - **Email:** unread + today's important mail. Google → `gmail_search` with a query like
     `newer_than:1d -category:promotions` then `gmail_get_message` for the top items.
     Microsoft → the internal mail tool for today's/unread messages.
   - **Chat:** Teams messages that mention the user, direct messages, and active threads
     (Microsoft internal tool). Skip if unavailable.
   - **Calendar:** today's events. Google → `calendar_list_events` for the day; Microsoft →
     the internal calendar tool. Note conflicts and gaps.
5. **Triage and prioritize** using the profile:
   - Flag items needing a reply or a decision today.
   - Separate FYI/newsletters from action items.
   - Surface meetings that need prep, and any scheduling conflicts.
6. **Validate & output** the briefing (see format). Never fabricate senders, subjects, times,
   or counts; if a section had no data, say so plainly. Append any new follow-up to `notes.md`
   (`python .agents/scripts/memory.py note "..."`).

## Output format

```
## Daily Happenings — [Name] — [date] ([morning|end of day])

### Needs you today (N)
- [source] [sender/who] — [subject/summary] — why it matters — suggested action

### Calendar ([N] events)
- [start–end] [title] — [location/link] — prep needed? conflicts?
- Free blocks: [gaps]

### Chat highlights (N)
- [channel/DM] [who] — [one-line summary] — reply needed?

### FYI / read later (N)
- [source] [sender] — [subject]

### Suggested focus
[2–3 sentence, in your voice: the one or two things to do first]
```

## Rules

- Read-only by default. Do not send email, reply in Teams, or modify calendar events unless
  the user explicitly asks; those are write actions and need confirmation.
- Only report items that came back from a tool call. If a provider or tool is unavailable,
  state it; never guess message contents, counts, or times.
- Keep the summary tight and skimmable; lead with what needs action.

## Related

- `ai-digest` — weekly AI news digest (different purpose: external news, not your inbox).
- Publishing/sending is handled by `connected-workspace` MCP tools, not this skill.
