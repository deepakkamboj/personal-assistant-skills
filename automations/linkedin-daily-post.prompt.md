# LinkedIn Daily Post

> Draft one high-quality LinkedIn post each morning — in your voice, on-pillar, reviewed and ready to
> publish.

- **Skill:** `/assistant-post` + `/assistant-post-review` (Claude Code: `/assistant:post`)
- **Runs in:** Microsoft Scout · GitHub Copilot · M365 Copilot
- **Schedule:** Weekdays 8:00 AM
- **Data source:** `config.profile.content_pillars` + the day's `ai-digest` LinkedIn pick
- **Delivery:** draft in response; publish via `linkedin_publish_text` (MCP) after review
- **Prerequisites:** `profile` filled, `content.md` voice samples; MCP for publish/stats

## Prompt to paste

```text
Draft today's LinkedIn post.

1. Load my profile, content pillars, and voice from ASSISTANT_CONFIG + content.md.
2. Pick an angle: prefer today's ai-digest LinkedIn pick (output/ai-digest/) if present, else choose
   an on-pillar topic I haven't covered recently (check linkedin_list_posts via MCP).
3. Write the post with a strong first-line hook, skimmable body, one clear takeaway, and a soft CTA.
   Match my voice; no em dashes; no corporate filler.
4. Run post-review on the draft: score hook, clarity, value, CTA, and voice; then output the improved
   final version plus 3 alternative hooks.

STOP before publishing. On my "publish", post it via linkedin_publish_text.

Delivery: post the final draft + review score to every configured target in config.delivery, reusing
the SAME session/thread each run (session_key: linkedin-daily-post). See _shared.md.
```

## Delivery & session

Posts the draft for approval to **Teams · Microsoft Scout · this chat**, reusing the same
thread/session every run via `session_key: linkedin-daily-post`. Configure targets in
`config.delivery` and paste the delivery footer from [_shared.md](_shared.md).

## Steps (what the assistant does)

1. Loads pillars + voice; checks recent posts via `linkedin_list_posts`.
2. Picks an angle (favoring the AI-digest pick).
3. Drafts the post, then self-reviews and improves it.
4. Returns the final post + 3 hook options.
5. **On confirm:** publishes via `linkedin_publish_text`.

## Output & delivery

- **Final post text** + 3 alternative hooks + a review score.
- **Publish:** `linkedin_publish_text` (manual confirm).
- Optionally pair with `/assistant-carousel` or `/assistant-pixel` for a visual.

## Run it in each app

### Microsoft Scout
1. Schedule a weekday-morning task; connect LinkedIn via the MCP. Keep publish as approval-gated.

### GitHub Copilot
1. Invoke `/assistant-post`; review; confirm publish. Cron via Actions to stage a daily draft as an
   issue for approval.

### Microsoft 365 Copilot
1. Draft + review in Copilot; publish through the connected LinkedIn MCP after you approve.

## Variations

- **Carousel day:** append "Make this a 7-slide carousel; hand slides to /assistant-pixel."
- **Repurpose:** feed a blog/README with "/assistant-repurpose into 3 post formats."
- **Engagement pass:** end of day, run "/assistant-comment on replies to my last post."
