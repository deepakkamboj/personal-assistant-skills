# Personal Brand Refresh

> A monthly check-up of your public identity — bio, headline, elevator pitch, and LinkedIn profile —
> kept aligned with what you're actually working on.

- **Skill:** `/assistant-me` + `/assistant-profile` (Claude Code: `/assistant:me`)
- **Runs in:** Microsoft Scout · GitHub Copilot · M365 Copilot
- **Schedule:** Monthly (first Monday)
- **Session key:** `personal-brand-refresh`
- **Data source:** `config.profile`, `content.md` (voice samples), recent wins in `memory.md`
- **Prerequisites:** `profile` filled; `content.md` voice samples

## Prompt to paste

```text
Run a monthly personal-brand refresh.

1. Load my profile, voice samples (content.md), and recent wins/updates from memory.md.
2. Regenerate my short bio, long bio, headline, tagline, and a 30-second elevator pitch in my voice.
3. Run the profile audit: score my LinkedIn headline, About, and featured sections; deliver
   ready-to-paste rewrites for anything scoring below "strong".
4. Flag anything stale — outdated title, old metrics, dead links — and suggest the fix.

Output: the refreshed assets as copy-paste blocks, plus a short "what changed and why" note.

Delivery: post the refresh summary to every configured target in config.delivery, reusing the SAME
session/thread each run (session_key: personal-brand-refresh). See _shared.md.
```

## Delivery & session

Posts the refresh summary to **Teams · Microsoft Scout · this chat**, reusing the same thread/session
every run via `session_key: personal-brand-refresh`. Configure targets in `config.delivery` and paste
the delivery footer from [_shared.md](_shared.md).

## Steps (what the assistant does)

1. Loads profile, voice samples, and recent wins.
2. Regenerates bios, headline, tagline, and elevator pitch in your voice.
3. Audits and rewrites LinkedIn profile sections with scores.
4. Flags stale details with fixes.

## Output & delivery

- **Copy-paste blocks** for each asset + a "what changed" note.
- Optionally push profile rewrites live via the LinkedIn MCP (manual confirm).

## Run it in each app

### Microsoft Scout
1. Schedule a monthly task; deliver the summary to your brand thread.

### GitHub Copilot
1. Invoke `/assistant-me` then `/assistant-profile`; save assets to `output/brand/`.

### Microsoft 365 Copilot
1. Generate and review; keep the assets in a pinned Teams/OneNote reference.

## Variations

- **New role:** append "I just changed roles to <X>; rewrite everything around that."
- **Speaker kit:** add "Also produce a 100-word speaker bio and a one-line intro."
