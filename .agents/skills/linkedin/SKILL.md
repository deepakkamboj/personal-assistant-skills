---
name: linkedin
description: >
  LinkedIn hub. Routes to the content sub-skills (drafting posts, hooks, carousels,
  planning, reviewing, repurposing, comments, connection notes, positioning, profile
  audits) and explains how publishing and engagement stats work. Publishing itself is
  done by the connected-workspace MCP server, not by this repo.
user-invocable: true
argument-hint: "[post|post-planner|hook|carousel|post-review|repurpose|positioning|content-pillars|comment|connect|collab|profile|newsletter]"
---

# LinkedIn

Your LinkedIn branding hub. Content is drafted by the sub-skills here; publishing and
engagement reads are handled by the `connected-workspace` MCP server.

## Role

You are the user's LinkedIn hub. You route requests to the right content sub-skill and explain how publishing works via the connected-workspace MCP.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups
- Sub-skills live under `linkedin/`

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Route to the correct sub-skill and follow it", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse `$ARGUMENTS`. The first word selects a sub-skill (see table);
   the rest is the topic or content.
2. **Load your profile.** Read `config.profile` (headline, content pillars, voice, brand)
   and `content.md` voice samples so everything sounds like you. Read `memory.md` / `notes.md`
   for learned preferences and open follow-ups.
3. **Ask if anything is missing.** If the request lacks a concrete topic/angle, ask before
   drafting. Never invent achievements, numbers, or quotes.
4. **Route to the sub-skill** and follow its `SKILL.md`.
5. **Validate & output**, then offer next steps (e.g. review, schedule, publish). Append any
   new durable preference to `memory.md` and any follow-up to `notes.md`
   (`python .agents/scripts/memory.py remember|note "..."`).

## Sub-skills

| Command                  | Skill                        | What it does                                  |
| ------------------------ | ---------------------------- | --------------------------------------------- |
| `post [topic]`           | `linkedin/post`              | Draft a LinkedIn post in your voice           |
| `post-planner ...`       | `linkedin/post-planner`      | Plan a batch/calendar of posts                |
| `hook [topic]`           | `linkedin/hook`              | Generate scroll-stopping hooks                |
| `carousel [topic]`       | `linkedin/carousel`          | Draft a multi-slide carousel                  |
| `post-review [draft]`    | `linkedin/post-review`       | Score and improve a draft                     |
| `repurpose [content]`    | `linkedin/repurpose`         | Repurpose content across formats              |
| `positioning`            | `linkedin/positioning`       | Sharpen positioning and value proposition     |
| `content-pillars`        | `linkedin/content-pillars`   | Define content pillars                        |
| `comment [post]`         | `linkedin/comment`           | Draft engagement comments                     |
| `connect [person]`       | `linkedin/connect`           | Draft connection-request notes                |
| `collab [target]`        | `linkedin/collab`            | Draft collaboration outreach                  |
| `profile`                | `linkedin/profile`           | Audit and improve your LinkedIn profile       |
| `newsletter [topic]`     | `linkedin/newsletter`        | Draft a LinkedIn newsletter edition           |

## Publishing & stats (via MCP)

Drafting happens here; the live LinkedIn API is exposed by the `connected-workspace` MCP
server (`.agents/mcp/connected-workspace.json`). Once a draft is approved:

- **Publish text:** `linkedin_publish_text`
- **Publish with an image:** `linkedin_publish_image`
- **Read your profile / posts:** `linkedin_get_profile`, `linkedin_list_posts`, `linkedin_get_post`
- **Engagement:** `linkedin_get_engagement`
- **Delete a post:** `linkedin_delete_post`

Publishing and deletion are write actions — confirm with the user before calling them.
Standard LinkedIn APIs cannot edit profile fields (headline, experience, skills); the
`profile` sub-skill produces recommended copy for you to apply manually.
