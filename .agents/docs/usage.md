# Usage

How to invoke every skill, with 2–3 examples each.

**Command forms**
- **Claude Code:** `/assistant:<name>` (from `.claude/commands/assistant/`)
- **GitHub Copilot:** `/assistant-<name>` (from `.github/prompts/`, enable `chat.promptFiles`)
- **Codex / plain chat:** just describe the task; the matching skill in `.agents/skills/` is used.

Everything after the command is passed as `$ARGUMENTS`. Each skill loads your `config.profile`
and shared `memory.md`/`notes.md` first, and asks if a required input is missing.

---

## Core

### `me` — personal branding

Args: `[bio|linkedin|pitch|headline|post|intro|digest-intro|update]`

```
/assistant:me bio short
/assistant:me headline
/assistant:me linkedin what I learned shipping an AI agent to production
```

### `ai-digest` — weekly AI news digest

Args: `[YYYY-MM-DD]`

```
/assistant:ai-digest
/assistant:ai-digest 2026-02-27
```

### `daily-digest` — Daily Happenings briefing

Args: `[microsoft|google|both] [today|YYYY-MM-DD] [morning|eod]`

```
/assistant:daily-digest
/assistant:daily-digest google morning
/assistant:daily-digest microsoft today eod
```

### `pixel` — visual artifacts

Args: `[diagram|infographic|banner|slides|chart|flow|roadmap|comparison] [topic]`

```
/assistant:pixel diagram AI test pipeline
/assistant:pixel banner AI Weekly Digest
/assistant:pixel comparison Playwright CLI vs MCP server
```

### `newsletter` — full newsletter system

Args: `[create|send|deploy|preview|subscribers|pipeline|setup]`

```
/assistant:newsletter create 2026-02-27
/assistant:newsletter preview 2026-02-27
/assistant:newsletter deploy 2026-02-27
```

---

## Writing

### `humanize` — make prose natural

No fixed args — paste or reference the text to rewrite.

```
/assistant:humanize <paste a stiff paragraph to rewrite>
/assistant:humanize make this LinkedIn draft sound less corporate
/assistant:humanize tighten this email and cut the filler
```

### `readability` — readability scores

Args: `[text to analyze]`

```
/assistant:readability <paste text>
/assistant:readability analyze the first paragraph of my draft
```

### `word-stats` — quick text statistics

Args: `[text to analyze]`

```
/assistant:word-stats <paste text>
/assistant:word-stats count words and reading time for this post
```

---

## Email

### `cold-email` — cold outreach

Args: `[target] [goal] [context/personalization]`

```
/assistant:cold-email VP Eng at Acme, book a 15-min demo, they just raised a Series B
/assistant:cold-email Head of Design, ask for feedback on our accessibility tool
/assistant:cold-email founder I met at a conference, propose a podcast swap
```

### `follow-up-email` — re-engage non-responders

Args: `[original email context] [days since sent] [follow-up number 1-3]`

```
/assistant:follow-up-email demo request, 4 days ago, #1
/assistant:follow-up-email partnership pitch, 9 days ago, #2
/assistant:follow-up-email intro request, 15 days ago, #3 break-up
```

---

## LinkedIn

### `linkedin` — hub (routes to a sub-skill)

Args: `[post|hook|carousel|post-planner|post-review|repurpose|positioning|content-pillars|comment|connect|collab|profile|newsletter]`

```
/assistant:linkedin post why flaky tests are a design problem
/assistant:linkedin hook the real cost of manual QA
/assistant:linkedin profile all
```

### `post` — draft a LinkedIn post

Args: `[topic or draft] [goal] [length]`

```
/assistant:post shipped an AI agent that cut triage time 80%, authority, standard
/assistant:post <paste a rough draft to rewrite>
/assistant:post we deleted 80% of our onboarding steps, engagement, short
```

### `post-planner` — plan a content calendar

Args: `[platform] [goal] [time period or count] [raw material]`

```
/assistant:post-planner LinkedIn, build authority, next 2 weeks, notes: AI agents, test automation
/assistant:post-planner LinkedIn, hiring, 8 posts, we're growing the platform team
```

### `hook` — scroll-stopping openers

Args: `[topic]`

```
/assistant:hook why most roadmaps are fiction
/assistant:hook the deploy that failed at 4:58 on a Friday
```

### `carousel` — multi-slide carousel

Args: `[topic]`

```
/assistant:carousel 6 ways to make your Copilot prompts better
/assistant:carousel anatomy of an AI test pipeline
```

### `post-review` — score and improve a draft

Args: `[paste your draft post]`

```
/assistant:post-review <paste your draft>
/assistant:post-review review this and make the hook stronger
```

### `repurpose` — adapt content across formats

Args: `[blog|talk|digest|readme|thread] [content or description]`

```
/assistant:repurpose blog <link or text of a blog post>
/assistant:repurpose talk my conference talk on AI agents
/assistant:repurpose thread turn this post into an X thread
```

### `positioning` — sharpen positioning

Args: `[refresh|competitor|niche]`

```
/assistant:positioning refresh
/assistant:positioning niche AI-driven test automation for enterprises
```

### `content-pillars` — define pillars

Args: `[pillar-name]`

```
/assistant:content-pillars
/assistant:content-pillars Developer Productivity
```

### `comment` — draft engagement comments

Args: `[paste the post or comment to reply to]`

```
/assistant:comment <paste a post you want to comment on>
/assistant:comment reply supportively to this take on AI testing
```

### `connect` — connection-request notes

Args: `[name and context of the person]`

```
/assistant:connect Priya, PM at Acme, met at the AI DevTools meetup
/assistant:connect speaker from the Playwright conf, want to stay in touch
```

### `collab` — collaboration outreach

Args: `[co-post|newsletter|podcast|webinar] [target name and context]`

```
/assistant:collab podcast Alex, host of the Testing Podcast
/assistant:collab co-post Dana, writes about DevEx
```

### `profile` — audit and rewrite your profile

Args: `[headline|about|featured|experience|all]`

```
/assistant:profile all
/assistant:profile headline
/assistant:profile about
```

### `linkedin-newsletter` — draft a LinkedIn newsletter edition

Args: `[topic or edition number]`

```
/assistant:linkedin-newsletter the state of AI agents in 2026
/assistant:linkedin-newsletter edition 12
```

---

> GitHub Copilot: replace `/assistant:` with `/assistant-` in any command above
> (e.g. `/assistant-post`, `/assistant-daily-digest`).
