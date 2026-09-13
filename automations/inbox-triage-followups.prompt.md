# Inbox Triage & Follow-ups

> Turn your unread mail into a triaged action list, and **stage** (never auto-send) follow-up replies
> for the threads that have gone quiet.

- **Skill:** `/assistant-daily-digest` + `/assistant-follow-up-email` (Claude Code: `/assistant:follow-up-email`)
- **Runs in:** Microsoft 365 Copilot (work) · Microsoft Scout (Gmail) · GitHub Copilot
- **Schedule:** Weekdays 8:30 AM
- **Session key:** `inbox-triage-followups`
- **Data source:** Outlook (M365) or Gmail (`gmail_search` via MCP)
- **Prerequisites:** mail access (M365 work tools or `connected-workspace` MCP)

## Prompt to paste

```text
Triage my inbox and stage follow-ups.

1. Pull unread/important mail from the last 3 days (Outlook work tools, or gmail_search via MCP).
2. Group into: Reply today · Waiting on me · Waiting on them · FYI · Unsubscribe/ignore.
   For each "Reply today", give one line: who, subject, the decision or action needed.
3. Find threads where I'm awaiting a reply and it's been 3+ business days. For each, draft a short,
   non-pushy follow-up using the follow-up-email framework, in my voice (50–125 words).
4. Save drafts to output/email/followups-{today}.md.

STOP before sending — drafts only. On my "send #N", send that draft via gmail_send_message (or the
work mail tool). Log anything I'm waiting on to notes.md.

Delivery: post the triage summary + draft list to every configured target in config.delivery, reusing
the SAME session/thread each run (session_key: inbox-triage-followups). See _shared.md.
```

## Delivery & session

Posts the triage summary + staged drafts to **Teams · Microsoft Scout · this chat**, reusing the same
thread/session every run via `session_key: inbox-triage-followups`. Configure targets in
`config.delivery` and paste the delivery footer from [_shared.md](_shared.md).

## Steps (what the assistant does)

1. Pulls recent unread/important mail (work or Gmail).
2. Buckets it into a triage list with per-item actions.
3. Drafts non-pushy follow-ups for stale threads (50–125 words, your voice).
4. Saves drafts to `output/email/followups-{today}.md`; sends only on explicit confirm.

## Output & delivery

- **Triage buckets** + a **staged follow-up draft** per stale thread.
- **Send** is per-draft and manual (`gmail_send_message` or work mail tool).
- **Waiting-on** items logged to `notes.md`.

## Run it in each app

### Microsoft 365 Copilot
1. Best for work mail; save the prompt and schedule 8:30 AM weekdays. Keep send manual.

### Microsoft Scout
1. Connect Gmail; schedule the task; deliver the triage to your inbox thread. Send stays approval-gated.

### GitHub Copilot
1. Invoke the prompt with the MCP available; stage drafts as a checklist issue for approval.

## Variations

- **VIP only:** append "Only triage mail from people/domains in memory.md."
- **Zero-inbox pass:** add "Also suggest archive/label actions for the FYI and Unsubscribe buckets."
- **Chain:** run after [Daily Digest](daily-digest-microsoft.prompt.md) and reuse its "Needs you" list.
