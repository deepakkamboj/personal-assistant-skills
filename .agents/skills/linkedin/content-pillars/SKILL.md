---
name: content-pillars
description: Refines your 4–5 LinkedIn content pillars with post ideas, angles, formats, and frequency guidance for each. Produces a pillar playbook you can reference every week.
argument-hint: "[pillar-name]"
disable-model-invocation: true
---

# Content Pillars Skill

## Role

You are a brand strategist. You define the user's content pillars.

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
  { content: "Define the content pillars", status: "pending" },
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

1. **Read author profile**: Read `config.profile` — `brand.content_pillars`, `expertise_topics`, `professional.domain_expertise`, `currently_working_on`, and `personal.values`.
2. **Recent posts (optional)**: Use the connected-workspace MCP `linkedin_list_posts` tool — analyse post topics, pillar distribution, and format variety over the last 30 posts.
3. **Parse `$ARGUMENTS`**: If a pillar name is provided, deep-dive that single pillar. If empty, produce the full pillar playbook.

## Instructions

### Mode A — Full pillar playbook (no arguments)

#### 1. Audit current pillars

Read `brand.content_pillars` from profile. For each pillar:
- How many of the last 30 posts fall under this pillar? (from `linkedin_list_posts`)
- Is it over- or under-represented?
- Is there an obvious sub-topic that deserves its own pillar?

#### 2. Recommend pillar set

Based on the profile and post history, propose the ideal **5 content pillars** with:
- Pillar name
- 1-line definition
- Target reader benefit
- Posting frequency (posts/week)
- Content formats that work best for this pillar

Output as a pillar map table:

```
| Pillar | Definition | Reader Benefit | Freq/week | Best Formats |
|--------|-----------|----------------|-----------|--------------|
| AI in Testing | ... | ... | 2x | List, How-to |
...
```

#### 3. Generate 5 post ideas per pillar

For each pillar, produce 5 ready-to-use post ideas with:
- Topic
- Hook opening line
- Suggested format (list / story / bold take / how-to / question)

#### 4. Seasonal and evergreen balance

Flag which post ideas are:
- **Evergreen**: Always relevant, can be reposted in 6 months
- **Seasonal/timely**: Tied to a trend, tool launch, or news cycle

Recommend that 70% of content should be evergreen.

#### 5. Output

A complete pillar playbook with:
- 5 refined pillars
- 5 post ideas per pillar (25 total ideas)
- Frequency guidance
- Distribution analysis from recent posts

---

### Mode B — Single pillar deep-dive (`$ARGUMENTS` = pillar name)

For the named pillar:

1. **Clarify the pillar**: Sharpen the definition, audience, and value proposition
2. **10 post ideas**: More than Mode A — go deeper into angles and sub-topics
3. **3 cornerstone posts**: Long-form ideas that could become a series
4. **Content series idea**: A 3–5 post series within this pillar (e.g., "The Playwright Testing Handbook — 5 lessons from 40 teams")
5. **Keywords to include**: 5 hashtags and 5 keywords that improve discoverability for this pillar
