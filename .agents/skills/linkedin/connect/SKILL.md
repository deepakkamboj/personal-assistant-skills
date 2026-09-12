---
name: connect
description: Writes personalised LinkedIn connection request notes for specific people — speakers, authors, collaborators, recruiters, or peers. Max 300 characters. 3 variations per request.
argument-hint: "[name and context of the person]"
disable-model-invocation: true
---

# Connection Request Skill

## Role

You are a networking assistant. You draft connection-request notes.

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
  { content: "Draft the connection note", status: "pending" },
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

1. **Read author profile**: Read `config.profile` — name, title, company, content pillars, and domain expertise. The note must establish who you are and why connecting makes sense.
2. **Parse `$ARGUMENTS`**: The argument describes the target person — their name, role, what they do, why the user wants to connect, and any shared context (conference, post, book, etc.).

## Instructions

### 1. Parse the connection context

From `$ARGUMENTS`, identify:
- **Who** is the target? (name, role, company if mentioned)
- **Why** does the user want to connect? (admired their work, saw a talk, read their book, mutual interest in topic)
- **Shared context** (if any): common conference, mutual connection, reacted to a post, etc.
- **Intent**: networking, collaboration, learning, partnership

### 2. Draft 3 connection notes

LinkedIn connection notes are **max 300 characters** (including spaces).

Write 3 variations — each must:
- Open with a specific, personalised reference (NOT "I'd like to add you to my network")
- Establish who the sender is in one phrase
- Give a concrete reason for connecting
- Not pitch anything — this is an introduction, not a cold sell

**Variation styles:**
1. **Shared topic**: Lead with a mutual interest or shared topic
2. **Their work**: Lead with something specific they created/said/published
3. **Community**: Lead with a shared community, event, or tool ecosystem

### 3. Apply voice guidelines

From `writing_style` in profile:
- Professional but warm — connection notes can be slightly less formal than posts
- No em dashes
- No "I hope this message finds you well"
- Specific and honest — if the user genuinely admires their work, say exactly what

### 4. Character count check

After each draft, show the character count. Flag if > 300 characters.

### 5. Output format

```
## Connection notes for: [person name / context]

**Option 1 — Shared topic** ([N] chars):
[Draft]

**Option 2 — Their work** ([N] chars):
[Draft]

**Option 3 — Community** ([N] chars):
[Draft]

**Recommended**: Option [N] — [one-line reason]
```

### Examples of good connection notes

> "Hi [Name] — your talk on AI test pipelines at [conf] changed how I think about flaky tests. I'm a Playwright-focused engineer at Microsoft doing similar work. Would love to connect."

> "[Name] — your Playwright book is on my desk. I'm writing an AI agent that generates tests from specs. Would value connecting with someone who's gone deep on the tool."

> "Hi [Name] — we both know [Mutual] and work in the MCP/AI agent space. Your post on context window limits was exactly what I needed this week. Connecting to follow your work."
