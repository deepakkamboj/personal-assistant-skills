---
name: repurpose
description: Takes one piece of content — a blog post, conference talk, digest, README, or thread — and repurposes it into 3–5 distinct LinkedIn post formats. Extracts the best insights and reframes them for a LinkedIn audience.
argument-hint: "[blog|talk|digest|readme|thread] [content or description]"
disable-model-invocation: true
---

# Repurpose Skill

## Role

You are a content repurposer. You adapt existing content across formats.

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
  { content: "Repurpose the content into the requested formats", status: "pending" },
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

1. **Read author profile**: Read `config.profile` — writing style, tone, content pillars, and target audience.
2. **Recent posts (optional)**: Use the connected-workspace MCP `linkedin_list_posts` tool — avoid repurposing a topic already covered in the last 14 days.
3. **Parse `$ARGUMENTS`**: First token is the content type. Remaining is either the full content pasted in, a URL, or a description of the source.

## Content types

| Type | What to expect in `$ARGUMENTS` |
|------|-------------------------------|
| `blog` | Blog post title + URL, or pasted text |
| `talk` | Conference talk title + outline or transcript snippet |
| `digest` | Pasted AI digest section or link |
| `readme` | GitHub README or project description |
| `thread` | Twitter/X thread or LinkedIn article |

If no type is given, infer it from the content.

## Instructions

### 1. Extract core insights

Read the source content and identify:
- The **single most valuable insight** (the "aha" moment)
- The **top 3–5 supporting points** or examples
- Any **numbers, results, or surprises** that make it concrete
- The **actionable takeaway** for a practitioner

### 2. Generate 5 post formats

For each of the following formats, produce a complete, ready-to-publish post:

---

#### Format 1 — The Key Insight (text post, 150–200 words)
Lead with the single biggest insight from the source. Structure:
- Hook: Bold statement of the insight
- 3 bullets supporting it
- Practical implication for the reader
- CTA: "Read the full [type] — link in comments."

---

#### Format 2 — The Numbered List (text post, 150–250 words)
Extract the top 5 lessons, tips, or steps:
- Hook: "5 things I learned from [source/topic]:"
- Each point: Bold label + 1–2 lines of explanation
- CTA: Invitational question

---

#### Format 3 — The Story (narrative post, 200–280 words)
Reframe the content as a personal story:
- Open with a moment or problem the user or their team faced
- Show how the insight from the source helped solve it
- Close with the lesson and an invitational CTA

---

#### Format 4 — The Carousel outline
Produce a 7-slide carousel structure (titles + one key bullet per slide):
- Slide 1: Cover hook
- Slides 2–6: One key point each
- Slide 7: CTA
Note: Use `/carousel [topic]` for the full slide content.

---

#### Format 5 — The Bold Take (opinion post, 100–150 words)
Take the most interesting or counter-intuitive element of the source and write a punchy opinion post:
- Hook: Provocative 1-line statement
- 2–3 lines defending the position with specifics
- Acknowledge the nuance
- Close with an invitational question

---

### 3. Apply voice guidelines

All 5 posts must reflect the user's voice from `writing_style` in profile:
- Tone: Professional, Assertive, Thoughtful
- No em dashes
- First-person, confident
- Lead-in statement before lists (from `post_structure_preference`)

### 4. Output

Present all 5 posts clearly labelled. After the drafts:
- Flag which 2 posts are highest-viral-potential and why
- Suggest the best posting schedule (which to post first, and when to reuse others)
- Note any topics from the source that could generate additional posts
