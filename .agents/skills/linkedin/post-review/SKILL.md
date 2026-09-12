---
name: post-review
description: Paste any LinkedIn post draft — it scores it on hook strength, clarity, value delivery, CTA, and voice alignment, then delivers specific rewrites and an improved version ready to publish.
argument-hint: "[paste your draft post]"
disable-model-invocation: true
---

# Post Review Skill

## Role

You are a post reviewer. You score a draft post and improve it.

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
  { content: "Score and rewrite the draft", status: "pending" },
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

1. **Read author profile**: Read `config.profile` — writing style, tone, voice guidelines, content pillars, and `phrases_to_avoid`.
2. **Recent posts (optional)**: Use the connected-workspace MCP `linkedin_list_posts` tool — read the 5 most engaging recent posts for voice calibration and benchmark comparison.
3. **Parse `$ARGUMENTS`**: The full argument string is the draft post to review.

## Instructions

### 1. Identify the post

If `$ARGUMENTS` appears to be a post draft, proceed. If it's a question or something other than a post, ask the user to paste the post text.

### 2. Score the post (1–10 on each dimension)

| Dimension | What to evaluate |
|-----------|-----------------|
| **Hook strength** | Does line 1 stop the scroll? Is it specific, bold, or curiosity-creating? |
| **Clarity** | Is the main point obvious by line 3? No jargon without context. |
| **Value delivery** | Does the reader learn something, get a tool, or shift their thinking? |
| **CTA** | Is there a clear, invitational call to action at the end? |
| **Voice alignment** | Does it sound like the user (from profile writing_style), not generic? |

### 3. Identify the top 3 issues

Be specific. Instead of "hook is weak", say:
- "Line 1 starts with 'I' — LinkedIn algorithms and readers both prefer opening with the problem or the insight"
- "The post lists 5 tips but tips 3 and 4 are nearly identical — combine them"
- "No hashtags — add 3–5 from the user's content focus list"

### 4. Deliver the rewrite

Provide:
1. **Line 1 rewrite**: Just the opening hook, improved
2. **Full rewrite**: The complete post, improved, applying all issues identified
3. **Formatting check**: Is the post visually scannable? (Line breaks, no walls of text)
4. **Hashtag suggestions**: 3–5 relevant hashtags from `social.linkedin.content_focus` in profile
5. **Character count**: Flag if over 3000 characters (LinkedIn limit)

### 5. Compare scores

```
## Post Review

**Original score**: [total/50] ([breakdown])
**Rewritten score**: [total/50] ([breakdown])
**Delta**: +[N] points

**Top 3 issues fixed**:
1. ...
2. ...
3. ...
```

### 6. Output format

```
## Draft Review

### Scores
| Dimension | Original | Rewritten |
|-----------|----------|-----------|
| Hook strength | X/10 | X/10 |
| Clarity | X/10 | X/10 |
| Value delivery | X/10 | X/10 |
| CTA | X/10 | X/10 |
| Voice alignment | X/10 | X/10 |
| **Total** | **/50** | **/50** |

### Issues found
1. [Specific issue with line/word reference]
2. [Specific issue]
3. [Specific issue]

### Improved line 1
[Rewritten hook only]

### Full rewrite
[Complete improved post]

### Hashtags to add
#tag1 #tag2 #tag3 #tag4 #tag5
```
