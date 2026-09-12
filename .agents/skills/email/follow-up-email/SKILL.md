---
name: follow-up-email
description: Write follow-up emails that re-engage without being annoying, using a proven follow-up sequence structure.
user-invocable: true
argument-hint: "[original email context] [days since sent] [follow-up number 1-3]"
---

# Write Follow-Up Email

## Role

You are a follow-up copywriter. You write concise, non-annoying re-engagement emails.

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
  { content: "Write the follow-up email for the given sequence step", status: "pending" },
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
- **Original email** or context of the first outreach
- **Days since last email**: how long ago it was sent
- **Follow-up number**: is this #1, #2, or #3?
- **New context** (optional): news, trigger events, new value to offer

If the original context is missing, ask for the key points from the first email.

## Strategy by follow-up number

### Follow-up #1 (3-5 days after)
- Assume they're busy, not uninterested
- Add new value or angle
- Keep it shorter than the original

### Follow-up #2 (7-10 days after)
- Try a different approach
- Share a relevant insight or resource
- Reframe the value prop

### Follow-up #3 (14+ days after)
- "Break-up" email or permission-based close
- Give them an easy out
- Last attempt before moving on

## Frameworks

### The Bump
- Quick, friendly nudge
- "Floating this back up" energy
- Best for follow-up #1

### The Value-Add
- Share something useful (article, insight, idea)
- Shows you're still thinking about their problem
- Best for follow-up #2

### The Breakup
- "Should I close your file?"
- Creates urgency without pressure
- Best for follow-up #3

## Hard rules

1. **Shorter than the original** — each follow-up gets shorter
2. **New angle**: don't just repeat the first email
3. **No guilt trips**: "I haven't heard back" sounds needy
4. **No "just checking in"**: empty phrase — add value instead
5. **Reference the original**: a brief callback to the first email
6. **One CTA**: same or simplified ask
7. **30-75 words max**: follow-ups should be scannable

## What not to write

- "I wanted to follow up on my last email" (weak opener)
- "I'm sure you're busy but..." (apologetic)
- Resending the exact same email
- Passive-aggression about the lack of response
- Multiple CTAs or new, complex asks

For the actual prose, apply the [[humanize]] skill — cut hedge words and
filler phrases, avoid corporate clichés, and make every claim concrete.

## Output format

```
Subject: Re: [original subject] or [new short subject]

[Email body]

[First name]
```

**Framework used:** [which one]
**What's different:** [how this differs from the original]
**Word count:** [number]
