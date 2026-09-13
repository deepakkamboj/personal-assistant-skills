# Shared conventions — delivery & session

Every automation in this folder **posts its report to all configured targets** and **reuses the same
session/thread on every run**, so recurring reports stack in one place instead of creating a new
thread each day.

## Delivery targets

| Target | How it posts | Same-session behavior |
|--------|--------------|-----------------------|
| **Microsoft Teams** | Graph `chatMessage` to `config.delivery.teams` channel/chat, or an Incoming Webhook | Reply into the saved **root message / thread** for this `session_key` so runs thread together |
| **Microsoft Scout** | The automation's Scout task keeps one **session** | Append each run to the same Scout session, not a new one |
| **Chat session** | Reply in the current chat conversation | For scheduled hosts, reuse the saved `chat_thread_id` for this `session_key` |

Post to **all available** targets; skip silently any target that isn't configured.

## Session key

Each recipe declares a stable `session_key` (e.g. `daily-ai-digest`). All delivery state is keyed by
it, so the same automation always lands in the same Teams thread / Scout session / chat thread.

## State file

Thread and session IDs persist in `output/automations/state.json` (git-ignored):

```json
{
  "daily-ai-digest": {
    "teams_thread_id": "19:...@thread.tacv2;messageid=1699...",
    "scout_session_id": "scout-sess-abc123",
    "chat_thread_id": "chat-xyz789",
    "last_run": "2026-09-12T06:30:00Z"
  }
}
```

Rule: on each run, **read** the IDs for `session_key`; if a thread/session exists, **reply into it**;
if not, create it once and **write** the IDs back.

## Config additions

Add a `delivery` block to your `config.json` (all fields optional — configure only what you use):

```json
"delivery": {
  "teams": {
    "mode": "graph",
    "team": "My Team",
    "channel": "AI Briefings",
    "webhook_url": ""
  },
  "scout": { "session": "personal-assistant" },
  "chat": { "reuse_thread": true },
  "state_path": "output/automations/state.json"
}
```

- `teams.mode`: `graph` (reply-in-thread, needs Graph access) or `webhook` (simple channel post).
- `teams.webhook_url`: used when `mode` is `webhook`.
- `scout.session`: the Scout session name reports append to.

## Delivery footer (paste into any automation prompt)

Append this block to the end of any recipe's "Prompt to paste" to enable multi-target, same-session
delivery:

```text
Delivery: post this report to every configured target in config.delivery, reusing the SAME
session/thread each run (session_key: <SESSION_KEY>).
1. Read output/automations/state.json for session_key <SESSION_KEY>.
2. Teams: if teams_thread_id exists, reply into that thread; otherwise post a new message to
   config.delivery.teams (graph or webhook) and save its thread id.
3. Scout: append to the config.delivery.scout.session; save scout_session_id.
4. Chat: reply in this conversation (reuse chat_thread_id when running headless).
5. Write back any new thread/session ids and last_run to output/automations/state.json.
Skip any target that isn't configured. Keep sends review-gated unless I enabled auto-send.
```

Replace `<SESSION_KEY>` with the recipe's declared key.
