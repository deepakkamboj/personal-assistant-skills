# Weekly Newsletter

> Turn the week's AI digest into a branded HTML newsletter, staged for review and one-click send +
> deploy.

- **Skill:** `/assistant-newsletter` (Claude Code: `/assistant:newsletter`)
- **Runs in:** GitHub Copilot (build/deploy) · Microsoft Scout · M365 Copilot
- **Schedule:** Fridays 9:00 AM
- **Data source:** `config.digest.sources` + `config.newsletter.settings` + `config.profile`
- **Delivery:** HTML to `output/newsletter/`, sent via `gmail_send_message` (MCP), deployed via FTP,
  tracked via PHP pixel
- **Prerequisites:** `newsletter.settings` (title, sections, base_url, FTP), MCP for send

## Prompt to paste

```text
Run the newsletter skill for this week's edition.

1. Load config.newsletter.settings, config.profile, and config.brand.
2. Gather this week's top items from config.digest.sources (reuse the latest ai-digest output if
   present in output/ai-digest/).
3. Assemble the sections defined in newsletter.settings.sections, with a masthead, a personal intro
   in my voice, 3–5 curated items with short takes, and the CTA.
4. Build the branded HTML at output/newsletter/newsletter-{slug}.html and show me a preview summary.

STOP before sending. Then wait for my confirmation. On "send", use gmail_send_message to the
subscriber list and deploy the HTML via FTP to newsletter.settings.base_url with the tracking pixel.

Delivery: post the preview summary + file path to every configured target in config.delivery, reusing
the SAME session/thread each run (session_key: weekly-newsletter). See _shared.md.
```

## Delivery & session

Posts the preview + link to **Teams · Microsoft Scout · this chat**, reusing the same thread/session
every run via `session_key: weekly-newsletter`. Configure targets in `config.delivery` and paste the
delivery footer from [_shared.md](_shared.md); IDs persist in `output/automations/state.json`.

## Steps (what the assistant does)

1. Loads newsletter settings, profile, and brand.
2. Pulls the week's items (reusing the latest AI digest when available).
3. Assembles masthead + intro + curated sections + CTA into branded HTML.
4. Saves `output/newsletter/newsletter-{slug}.html` and previews.
5. **On explicit confirm:** sends via Gmail MCP and deploys via FTP with the tracking pixel.

## Output & delivery

- **File:** `output/newsletter/newsletter-{slug}.html`.
- **Send:** `gmail_send_message` to `newsletter.subscribers`.
- **Deploy:** FTP to `newsletter.settings.base_url`; opens/clicks tracked by the PHP pixel.

## Run it in each app

### GitHub Copilot
1. Best for build + deploy: invoke `/assistant-newsletter`, review the HTML, then confirm.
2. Schedule a Friday cron in GitHub Actions to build + open a PR with the HTML for review before send.

### Microsoft Scout
1. Schedule a Friday task; connect Gmail for send. Keep send as a manual approval step.

### Microsoft 365 Copilot
1. Draft/preview the edition; hand the HTML to your deploy pipeline. Send via the connected Gmail MCP.

## Variations

- **Digest-driven:** chain after [Weekly deep AI Digest](daily-ai-digest.prompt.md#variations).
- **Segment sends:** append "Send only to subscribers tagged 'ai-weekly'."
- **LinkedIn edition:** also run `/assistant-linkedin-newsletter` to publish a LinkedIn newsletter
  version.
