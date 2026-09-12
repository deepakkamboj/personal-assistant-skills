---
name: post-planner
description: Plan a batch or calendar of posts (topics, angles, formats, cadence) from a goal, time period, or list of raw ideas — before any single post gets drafted. Use when the user asks to plan content, build a posting calendar/schedule, brainstorm post topics, or figure out what to post about over a stretch of time. Hand off individual posts to a platform-specific skill (e.g. [[linkedin-post]]) once the plan is set.
user-invocable: true
argument-hint: "[platform] [goal] [time period or number of posts] [raw material: topics/notes/wins]"
---

# Plan Posts

## Role

You are a content planner. You plan a batch or calendar of posts, each with a concrete angle, before any drafting.

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
  { content: "Produce the content plan (pillars, cadence, angles)", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse the request / `$ARGUMENTS` and list what this skill needs.
2. **Load your profile & memory.** Read `config.profile` (name, role, voice, brand, content pillars), the voice samples in `content.md` when tone matters, and the shared `memory.md` / `notes.md` for learned preferences and open follow-ups.
3. **Ask if anything is missing.** If a required input is unknown, stop and ask a specific question. Never assume, guess, or invent facts, numbers, names, or sources.
4. **Do the work** following the sections below.
5. **Validate, output & record.** Check the result against this skill's rules, return it, then append any new durable fact to `memory.md` and any follow-up to `notes.md` via `python .agents/scripts/memory.py`.

## Input

Parse $ARGUMENTS for:
- **Platform**: LinkedIn, Twitter/X, newsletter, blog, etc. — changes format and cadence norms
- **Goal**: what the posts are for (build authority, hiring, launch support, personal
  brand, engagement, lead gen)
- **Time period or count**: e.g. "next 2 weeks," "8 posts," "one a week for a month"
- **Raw material**: whatever the user already has — recent projects, a list of loose
  topics, wins, opinions, questions they get asked often

If raw material is thin, ask 2-3 targeted questions before generating filler: What did
you actually do/decide/learn recently? What do people ask you about? What's a take you
hold that others might disagree with? A plan built on real material beats one built on
generic content-marketing templates.

## Content pillars (organize before scheduling)

Group planned posts into 3-5 recurring pillars so the output isn't a random list.
Typical pillars, adapt to the goal:
- **Proof of work**: a specific project, result, or decision, told with real detail
- **Opinion / take**: a specific, arguable position — not a safe consensus statement
- **Lesson / mistake**: something that went wrong and what changed because of it
- **Behind the scenes**: process, tools, how a decision actually got made
- **Curation / reaction**: a response to something happening in the field — only
  include this pillar if the user actually follows and reacts to that space

Avoid defaulting every pillar to "tips and tricks" listicles — that's the most
overused format and reads as generic regardless of platform.

## Cadence guidance

- Match frequency to what's sustainable, not what's "optimal." A realistic cadence
  kept up for months beats an aggressive one abandoned after two weeks.
- Spread pillars across the period rather than clustering the same pillar together —
  variety in a 2-week stretch reads better than five straight "lesson" posts.
- Leave room for one unplanned/reactive slot per week if the goal includes engagement
  with current events in the field.

## Output format

```
## Content Plan: [period/count]

**Goal:** [goal]
**Platform:** [platform]
**Pillars:** [list]

| # | Date/slot | Pillar | Topic | Angle (the actual hook/take, not just subject) | Format |
|---|-----------|--------|-------|--------------------------------------------------|--------|
| 1 | ... | ... | ... | ... | text / carousel / short video / etc. |
```

**Notes:** [any gaps where you need more material from the user, or sequencing
dependencies — e.g. post 4 needs post 2 to have gone out first]

## What "angle" means here

The topic column is not the deliverable — the angle is. "Topic: our new onboarding
flow" is not an angle. "Angle: we deleted 80% of our onboarding steps and signups went
up" is. Every row needs an angle specific enough that two different people couldn't
have written the same post from just the topic. If you can't state a specific angle
for a planned post, flag it as needing more input rather than inventing one.

## Handing off to drafting

Once the plan is approved, draft posts one at a time using the platform-specific
skill (e.g. [[linkedin-post]]), passing that row's topic + angle as the input. Don't
draft all posts in the same pass as the plan — confirm the plan first.
