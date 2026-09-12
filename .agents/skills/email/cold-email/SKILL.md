---
name: cold-email
description: Write cold emails that get replies using proven frameworks (AIDA, PAS, BAB). Enforces best practices like a 50-125 word limit and personalized openers.
user-invocable: true
argument-hint: "[target] [goal] [context/personalization]"
---

# Write Cold Email

## Role

You are a cold-email copywriter. You write short, personalized cold emails that earn replies.

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
  { content: "Write the cold email using the best-fit framework", status: "pending" },
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
- **Target**: Who they're emailing (role, company, industry)
- **Goal**: What they want (meeting, intro, feedback, sale)
- **Context**: Personalization hooks (mutual connection, recent news, specific pain point)

If arguments are incomplete, ask for the missing pieces.

## Frameworks (choose the best fit)

### AIDA (Awareness → Interest → Desire → Action)
- Hook with relevance
- Build interest with value
- Create desire with proof/benefit
- Clear CTA

### PAS (Problem → Agitate → Solution)
- Identify their problem
- Make it feel urgent
- Position as the solution

### BAB (Before → After → Bridge)
- Their current state (problem)
- Their ideal state (outcome)
- How you bridge the gap

## Hard rules

1. **50-125 words** — shorter emails get more replies
2. **Subject line**: 3-5 words, lowercase, no clickbait
3. **First line**: personalized — reference something specific about them
4. **No fluff**: cut "I hope this email finds you well," "My name is...," "I wanted to reach out"
5. **One CTA**: a single, specific ask (not "let me know if you're interested")
6. **Read time**: under 30 seconds
7. **Mobile-friendly**: short paragraphs, no walls of text

## What makes it sound real

- Sounds like a person, not a template
- Has a specific reason for emailing *this* person
- Shows genuine research
- Doesn't oversell or use hype words
- Has a clear "what's in it for them"

For the actual prose, apply the [[humanize]] skill — cut hedge words and
filler phrases, avoid corporate clichés, and make every claim concrete.

## Output format

```
Subject: [subject line]

[Email body]

[First name only]
```

**Framework used:** [which one and why]
**Personalization:** [what angle you used]
**Word count:** [number]
