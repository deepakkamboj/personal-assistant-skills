# Skill Authoring Pattern

Every skill in `.agents/skills/` follows the same shape so agents run them the same way
across Claude Code, GitHub Copilot, and Codex.

## Frontmatter

```yaml
---
name: skill-name            # kebab-case, matches [[skill-name]] cross-references
description: >              # when to use it and what it produces
  ...
user-invocable: true        # optional
argument-hint: "[...]"      # optional
---
```

No `skill.json`. No `.claude-plugin` manifest.

## Required skill body — Role, Context, Workflow

Every skill body defines four things, in this order:

1. **`## Role`** — one or two sentences: who the assistant is for this skill and what it
   produces. Written in second person ("You are …"). Grounds tone and scope.
2. **`## Context to load`** — the exact inputs to read before acting: always
   `config.profile`, `content.md` (when tone matters), and the shared `memory.md` / `notes.md`,
   plus any skill-specific config (e.g. `config.brand`, `config.digest.sources`).
3. **`## Workflow`** — starts with a **`### Step 0: TodoWrite Checklist`** that creates the
   task list, then the detailed steps to follow in order.
4. The skill-specific sections (rules, formats, sub-commands).

### Step 0: TodoWrite Checklist

The workflow opens by materializing the task list. Mark the first task `in_progress` and the
rest `pending`; complete each before starting the next.

~~~text
## Workflow

### Step 0: TodoWrite Checklist

```
TodoWrite([
  { content: "Gather inputs; load profile, content, memory & notes", status: "in_progress" },
  { content: "Ask for any missing inputs (never assume or hallucinate)", status: "pending" },
  { content: "<the skill's core task>", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

Then work each task top to bottom. If a required input is missing, ask — never assume.
~~~

## The rules that apply to every skill

1. **Role first.** State the assistant's role and scope, then act within it.
2. **Sequential TodoWrite workflow.** Create the Step 0 checklist and complete items in order;
   don't skip ahead.
3. **Profile awareness.** Always load `config.profile` and tailor output to that person's
   identity, role, voice, and brand. Never return generic output when a profile exists.
4. **Shared memory.** Read `memory.md` / `notes.md` at the start and append new confirmed
   facts or follow-ups at the end, so the profile keeps improving across sessions.
5. **Ask, don't hallucinate.** If required information is missing, ask a specific question
   and wait. Never fabricate facts, numbers, names, quotes, or sources.

Exception: a skill whose description says it must return results immediately without
follow-up questions (e.g. `word-stats`) still creates the checklist but skips the "ask"
task when the needed input is already present.

## Configuration access

Structured data lives in `config.json` (resolved via `ASSISTANT_CONFIG`, default
`~/.assistant/config.json`); prose/voice/prompts live in `content.md`
(`config.paths.content`). Skills read these — never a `data/` folder.

Python helper: `.agents/scripts/assistant_config.py` (`load_config`, `content_path`,
`output_dir`, `memory_path`, `notes_path`, `append_entry`). Memory CLI:
`.agents/scripts/memory.py`.
