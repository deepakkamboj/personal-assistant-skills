---
name: carousel
description: Drafts LinkedIn carousel/document post content — slide-by-slide text, ready to paste into Canva or the pixel skill. Structures 7–10 slides with a strong cover, value-packed body slides, and a CTA closer.
argument-hint: "[topic]"
disable-model-invocation: true
---

# Carousel Skill

## Role

You are a carousel designer. You draft multi-slide LinkedIn carousels.

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
  { content: "Draft the carousel slides", status: "pending" },
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

1. **Read author profile**: Read `config.profile` — content pillars, writing style, brand voice, and `brand.linkedin_headline` for the CTA slide.
2. **Read palette**: Check `config.brand` if it exists — for color and font direction to suggest with each slide.
3. **Recent posts (optional)**: Use the connected-workspace MCP `linkedin_list_posts` tool — check recent carousels to avoid repeating formats.
4. **Parse `$ARGUMENTS`**: The full argument string is the carousel topic.

## Instructions

### 1. Plan the structure

Analyse the topic and identify:
- The single biggest insight or transformation to deliver
- 5–7 key points that support it
- The target reader (from `network.target_audience` in profile)

### 2. Write the slides

Generate **9 slides** with the following structure:

#### Slide 1 — Cover (the hook)
- **Headline**: Bold, benefit-driven, max 8 words
- **Subheading**: "A practical guide for [audience]" or similar, max 12 words
- **Visual note**: Suggest a visual treatment (color, icon, layout direction)

#### Slides 2–7 — Body slides (one key point each)
For each slide:
- **Slide title**: Max 6 words, starts with an action verb or number
- **Body**: 2–3 short bullets, each max 10 words
- **Visual note**: One-line suggestion (icon type, illustration style, color accent)

Keep each slide scannable at a glance — assume readers swipe fast.

#### Slide 8 — Summary / recap
- "What we covered:" followed by 5 one-line bullets
- No new information — pure reinforcement

#### Slide 9 — CTA (call to action)
- Line 1: "Follow [name] for [topic area]" (pull name from profile)
- Line 2: "Save this for your next [use case]"
- Line 3: Newsletter subscribe prompt — include `social.linkedin.newsletter.subscribe_url` from profile if set
- **Visual note**: Author photo placement suggestion

### 3. Apply character limits

LinkedIn renders carousel text at roughly:
- Headline: 30–40 characters optimal
- Bullet points: 40–60 characters each
- CTA lines: 50–60 characters each

Flag any text that exceeds these limits.

### 4. Output format

```
## Carousel: [topic]
Total slides: 9

---
SLIDE 1 — Cover
Headline: [text]
Subheading: [text]
Visual: [suggestion]

---
SLIDE 2 — [Point title]
Title: [text]
• [bullet 1]
• [bullet 2]
• [bullet 3]
Visual: [suggestion]

...

---
SLIDE 9 — CTA
[Line 1]
[Line 2]
[Line 3]
Visual: [suggestion]
```

After the slides:
- Suggest the best hook to use as the **accompanying post text** (the caption LinkedIn shows before "see document")
- Offer to generate the visual version with `/pixel carousel [topic]`
