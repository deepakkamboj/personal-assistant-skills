# Daily AI Digest

> Every morning, research the latest in AI and produce a branded HTML digest with a personal
> editor's note and a LinkedIn-worthy pick.

- **Skill:** `/assistant-ai-digest` (Claude Code: `/assistant:ai-digest`)
- **Runs in:** Microsoft 365 Copilot · GitHub Copilot · Microsoft Scout
- **Schedule:** Weekdays 6:30 AM (before your first meeting)
- **Data source:** Web — the curated `config.digest.sources`
- **Reads:** `config.profile`, `config.digest.sources`, `config.brand`, `content.md`, `memory.md`
- **Prerequisites:** `digest.sources` populated; web access (WebSearch/WebFetch) in the host

## Prompt to paste

```text
Run the ai-digest skill for today.

1. Load my profile, brand tokens, content voice, and memory from ASSISTANT_CONFIG.
2. For each source in config.digest.sources, fetch today's items. Gather 2–5 items per category:
   breaking_news, models_apis, research_papers, github_repos, products_tools, industry_analysis,
   agents_automation, tutorials_learning, linkedin_insights.
3. Deduplicate, rank by relevance to my content pillars, and drop anything older than 48h.
4. Write an 80–120 word editor's note in my voice — opinionated, conversational, no em dashes.
5. Assemble the self-contained dark-mode HTML digest (800px max width) using my brand colors.
6. Pick ONE story worth a LinkedIn post and draft a 150-word post for it.

Output: save output/ai-digest/digest-{today}.html, then report the date, item counts per category,
the file path, and the LinkedIn post pick. Do not publish anything — staging only.

Delivery: post this report to every configured target in config.delivery, reusing the SAME
session/thread each run (session_key: daily-ai-digest). See _shared.md.
```

## Delivery & session

Posts to **Teams · Microsoft Scout · this chat**, reusing the same thread/session every run via
`session_key: daily-ai-digest`. Configure targets in `config.delivery` and paste the delivery footer
from [_shared.md](_shared.md); thread/session IDs persist in `output/automations/state.json`.

## Steps (what the assistant does)

1. Loads profile/brand/voice/memory from your config.
2. Fetches + normalizes items from each configured source.
3. Categorizes, dedupes, ranks against your pillars.
4. Generates the editor's note in your voice.
5. Builds the branded HTML file at `output/ai-digest/digest-{YYYY-MM-DD}.html`.
6. Surfaces one LinkedIn-worthy pick with a ready draft.

## Output & delivery

- **File:** `output/ai-digest/digest-{YYYY-MM-DD}.html` (self-contained).
- **Report:** counts per category + file path + LinkedIn pick.
- **Optional delivery:** email the HTML to yourself (`gmail_send_message` via MCP) or post the pick —
  keep these as a manual confirm step.

## Run it in each app

### Microsoft 365 Copilot
1. Save the prompt as a reusable Copilot prompt (Copilot → Prompts).
2. For recurring runs, add it as a **scheduled prompt** (if enabled on your tenant) or wrap it in a
   **Copilot Studio** declarative agent with a daily trigger at 6:30 AM.
3. Web fetch happens through Copilot's web grounding.

### GitHub Copilot
1. This repo already exposes it as `/assistant-ai-digest` (`.github/prompts/`). Invoke in Copilot Chat.
2. To schedule, add a GitHub Actions workflow on a cron (`30 6 * * 1-5`) that runs the Copilot CLI / an
   agent with the prompt and commits the generated HTML to `output/ai-digest/`.

### Microsoft Scout
1. Create a new **scheduled task/automation** in Scout and paste the prompt.
2. Set the recurrence to weekday mornings; let Scout store the HTML or email it to you.

## Variations

- **Weekly deep digest:** change "for today" to "for this week" and expand to 5 items/category; run
  Fridays. Feed the result straight into [Weekly Newsletter](weekly-newsletter.prompt.md).
- **Topic focus:** append "Focus only on: agents, evals, and RAG." to narrow the scan.
- **Auto-email:** add "Then email the HTML to me via the connected-workspace MCP."
