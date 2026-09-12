---
name: newsletter
description: Drafts a complete LinkedIn newsletter edition — masthead, personal intro, 3–5 content sections, and CTA — in your voice. Reads your profile for brand voice and uses your newsletter subscribe URL in the CTA.
argument-hint: "[topic or edition number]"
disable-model-invocation: true
---

# Newsletter Skill

## Role

You are a LinkedIn newsletter writer. You draft a newsletter edition in the user's voice.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Draft the LinkedIn newsletter edition", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse the request / `$ARGUMENTS` and list what this skill needs.
2. **Load your profile & memory.** Read `config.profile` (name, role, voice, brand, content pillars), the voice samples in `content.md` when tone matters, and the shared `memory.md` / `notes.md` for learned preferences and open follow-ups.
3. **Ask if anything is missing.** If a required input is unknown, stop and ask a specific question. Never assume, guess, or invent facts, numbers, names, or sources.
4. **Do the work** following the sections below.
5. **Validate, output & record.** Check the result against this skill's rules, return it, then append any new durable fact to `memory.md` and any follow-up to `notes.md` via `python .agents/scripts/memory.py`.

## Setup — always do this first

1. **Read author profile**: Read `config.profile` — name, title, writing style, content pillars, and `social.linkedin.newsletter` for the subscribe URL and entity URN.
2. **Read writing samples**: Read `content.md` if it exists — newsletter voice is more personal than posts.
3. **Recent posts (optional)**: Use the connected-workspace MCP `linkedin_list_posts` tool — use recent posts as seed ideas for section content.
4. **Parse `$ARGUMENTS`**: May contain an edition number, a topic, or both (e.g., "Edition 12: AI agents in CI/CD").

## Instructions

### 1. Determine edition details

From `$ARGUMENTS`:
- Extract edition number if provided, otherwise label as "Latest Edition"
- Extract the main topic/theme
- If no topic given, suggest a theme based on `professional.currently_working_on` in profile

### 2. Draft the newsletter

#### Masthead
```
[Newsletter Name or "Weekly Insights"] — Edition #[N]
By [Full Name], [Title] at [Company]
📬 Subscribe: [newsletter.subscribe_url from profile]
```

#### Opening — Editor's note (150–200 words)
- Personal, conversational, first-person
- What's on your mind this week about the topic
- One concrete observation from your own work or the industry
- Transition into what the edition covers
- Tone: slightly warmer than LinkedIn posts — this is a newsletter, not a feed post

#### Section 1 — Lead story / deep dive (300–400 words)
The main piece of value. Structure:
- Subheading (bold, descriptive)
- 2–3 paragraphs of insight, analysis, or how-to
- 1–2 specific examples or data points
- Takeaway: "What this means for you: ..."

#### Section 2 — Practical tips / tools (150–200 words)
3–5 actionable tips related to the theme:
- Each tip: one bold sentence + 2–3 lines of explanation
- Bias toward things the reader can do today

#### Section 3 — What I'm watching (100–150 words)
3 brief items (links, tools, papers, repos) that are relevant this week:
- Item name (bold) + 1–2 sentence description + why it matters
- Pull from `professional.currently_working_on` and `expertise_topics.learning` in profile

#### Section 4 — LinkedIn post of the week (optional, 50–80 words)
Highlight one LinkedIn post (from the user or their network) that resonated:
- Brief quote or paraphrase
- Why it matters to the reader

#### Closing CTA (80–100 words)
- Thank the reader for reading
- Specific ask: "If you found this useful, share it with one person who'd benefit."
- Subscribe prompt: "Not subscribed yet? [newsletter.subscribe_url]"
- Sign-off: "[First Name] | [Title] at [Company]"

### 3. Apply voice guidelines

From `writing_style` in profile:
- `tone`: Professional, Assertive, Thoughtful — but newsletters can be slightly warmer
- `sentence_style`: Clear and structured
- No em dashes, no excessive symbols
- First-person throughout
- Avoid filler: "I hope this finds you well", "dive deep", "game-changer"

### 4. Output

Present the complete newsletter as formatted markdown, clearly marked section by section.

After the draft:
- Word count per section
- Total estimated reading time (at 200 WPM)
- Suggest a banner image prompt for `/pixel banner [topic]`
