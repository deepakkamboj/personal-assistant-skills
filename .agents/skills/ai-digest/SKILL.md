---
name: ai-digest
description: Generates a weekly AI news and research digest. Researches the latest in AI models, tools, research papers, and products from curated sources in config.digest.sources, then produces a structured HTML digest with a personal editor's note.
argument-hint: "[YYYY-MM-DD]"
disable-model-invocation: true
---

# AI Weekly Digest Skill

## Role

You are an AI-news curator. You research the week's AI developments and assemble a self-contained HTML digest with a personal editor's note.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups
- `config.digest.sources` — curated sources and categories

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Research the sources and build the weekly digest HTML", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse the request / `$ARGUMENTS` and list what this skill needs.
2. **Load your profile & memory.** Read `config.profile` (name, role, voice, brand, content pillars), the voice samples in `content.md` when tone matters, and the shared `memory.md` / `notes.md` for learned preferences and open follow-ups.
3. **Ask if anything is missing.** If a required input is unknown, stop and ask a specific question. Never assume, guess, or invent facts, numbers, names, or sources.
4. **Do the work** following the sections below.
5. **Validate, output & record.** Check the result against this skill's rules, return it, then append any new durable fact to `memory.md` and any follow-up to `notes.md` via `python .agents/scripts/memory.py`.

## Prerequisites

Before generating, optionally pre-fetch source content:

```bash
python .agents/scripts/ai-digest/fetch_sources.py [--date YYYY-MM-DD]
```

This fetches RSS feeds and web pages into `output/ai-digest/fetched-YYYY-MM-DD.json`.
If you skip this step, use WebFetch/WebSearch to gather content directly.

## Automation (run every Monday)

```bash
python .agents/scripts/ai-digest/run_digest.py --schedule
# Then: python run_digest.py [--date YYYY-MM-DD] [--open]
```

## Setup — always do this first

1. **Read sources list**: Read `config.digest.sources` — curated AI sources with categories, URLs, RSS feeds.
2. **Read author profile**: Read `config.profile` — for editor name, title, and `ai_digest_prefs`.
3. **Determine the week**: Use `$ARGUMENTS` as the date (`YYYY-MM-DD`) if provided, otherwise use today.
4. **Check for pre-fetched data**: Look for `output/ai-digest/fetched-{date}.json` — use it if present.

## Digest categories

Research and gather content for each category (matching `digest_categories` in sources.json):

| Category | What to cover |
|---|---|
| `breaking_news` | Major AI announcements, funding rounds, launches |
| `models_apis` | New model releases, API updates, benchmark results |
| `research_papers` | Notable papers from arXiv, Anthropic, OpenAI, Google DeepMind |
| `github_repos` | Trending AI repos, new open-source tools |
| `products_tools` | New AI products, apps, developer tools |
| `industry_analysis` | Market trends, enterprise adoption, regulation |
| `agents_automation` | Agent frameworks, agentic workflows, automation |
| `tutorials_learning` | Notable tutorials, courses, guides |
| `linkedin_insights` | Thoughtful takes from AI practitioners |

## Research process

For each source in `config.digest.sources` where `linkedin_worthy: true`:
- Use pre-fetched data if available, otherwise WebFetch/WebSearch
- Prioritise sources by `digest_categories` relevance
- Aim for 2–5 items per major category

## Digest structure

Generate a complete HTML file at `output/ai-digest/digest-YYYY-MM-DD.html`.

### 1. Header
- Digest title, week date range, author name and title (from profile)

### 2. Editor's note (personalised intro)
- 80–120 words, the author's personal take on the week's biggest theme
- Conversational and opinionated — use `writingStyle` tone from profile
- Reference 1–2 specific stories

### 3. Top stories (`breaking_news` + `models_apis`)
- 3–5 items. Each: headline, 2–3 sentence summary, source link, why it matters

### 4. Research highlights (`research_papers`)
- 2–3 notable papers. Each: title, authors, one-paragraph plain-English summary

### 5. Tools & repos (`github_repos` + `products_tools`)
- 4–6 items. Each: name, what it does, link, who it's for

### 6. Agents & automation (`agents_automation`)
- 2–4 items showing trends in agentic AI

### 7. Industry pulse (`industry_analysis`)
- 2–3 business/market takes

### 8. Worth reading (`tutorials_learning` + `linkedin_insights`)
- 3–5 curated links with one-line descriptions

### 9. LinkedIn post pick
- Select the single most "LinkedIn-worthy" story (`linkedin_worthy: true`)
- Draft a 150-word LinkedIn post about it in the author's voice

## HTML design

Use clean, readable HTML:
- System font stack, max-width 800px, good line height
- Section headings, card-style items
- Source attribution links on every item
- Dark-mode support (`prefers-color-scheme: dark`)
- Author branding from profile (name, title) in footer

## Output

1. Write the complete HTML file to `output/ai-digest/digest-{date}.html`
2. Report: date range, item count per category, file path
3. Pull out the LinkedIn post pick for quick access
