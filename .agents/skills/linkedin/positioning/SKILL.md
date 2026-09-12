---
name: positioning
description: Defines your LinkedIn content niche, target audience, unique point of view, and differentiation vs. other voices in the AI and test automation space. Produces a clear positioning statement and content strategy brief.
argument-hint: "[refresh|competitor|niche]"
disable-model-invocation: true
---

# Positioning Skill

## Role

You are a positioning strategist. You sharpen the user's value proposition and positioning.

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
  { content: "Produce positioning options", status: "pending" },
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

1. **Read author profile**: Read `config.profile` — full professional section, content pillars, brand, network target audience, expertise topics, and values.
2. **Recent posts (optional)**: Use the connected-workspace MCP `linkedin_list_posts` tool — analyse the last 20 posts for topic frequency, engagement patterns, and tone.
3. **Parse `$ARGUMENTS`**: Optional focus (`refresh` = full positioning review, `competitor` = differentiation focus, `niche` = niche refinement).

## Instructions

### 1. Audience definition

From `network.target_audience` and `professional.domain_expertise` in profile, define:

**Primary audience** (the person who benefits most from your content):
- Role / seniority
- Pain points your content solves
- What they gain from following you

**Secondary audience** (adjacent, also benefits):
- Who else reads and reshares your content

Output as a 2-paragraph "audience persona" description.

---

### 2. Content niche statement

Define the user's niche in one sentence using this formula:

> "I help [audience] achieve [outcome] through [unique method/perspective], specifically by covering [topic 1], [topic 2], and [topic 3]."

Derive all inputs from `config.profile`. Produce 3 variations.

---

### 3. Unique point of view (POV)

LinkedIn's most-followed creators have a clear, repeatable POV — a lens through which they see their industry.

Based on `expertise_topics.opinion_on` and `personal.values` in profile, articulate:

**The user's POV in 3 parts**:
1. **What most people get wrong** about AI testing / automation
2. **What the user believes** instead (their contrarian or nuanced take)
3. **How their work proves it** (evidence from `career_highlights`)

Output as a 150-word "creator manifesto" paragraph.

---

### 4. Competitive differentiation

Identify 3 types of voices covering similar topics (AI, Playwright, testing, developer productivity):
- The academic/research angle
- The vendor/tool-selling angle
- The practitioner-at-scale angle

Place the user clearly in one of these, or identify a gap they uniquely fill.

Produce: "You are the _______ in this space because _______."

---

### 5. Positioning statement

Combine the above into a concise positioning document:

```
## LinkedIn Positioning Brief — [Name]

**Niche**: [one sentence]
**Primary audience**: [2–3 sentences]
**Unique POV**: [2–3 sentences]
**Differentiation**: [2 sentences]
**Content promise**: "Every post from [name] helps [audience] [benefit]."

**Tone**: [from writing_style in profile]
**Posting frequency**: [from social.linkedin.posting_frequency]
**Content pillars**: [from brand.content_pillars]
```

---

### 6. Recommendations

5 specific actions to sharpen the positioning:
1. Profile change (headline or about)
2. Content type to add or drop
3. Topic to double down on
4. Topic to deprioritise
5. Audience segment to engage more deliberately
