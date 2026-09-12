---
name: pixel
description: Visual artifact generator. Creates diagrams, infographics, banners, slide decks, charts, flow diagrams, roadmaps, and feature comparisons as self-contained HTML or SVG files. Reads brand design tokens from config.brand and uses the generate.py script to prepare brand-aware starter files.
argument-hint: "[diagram|infographic|banner|slides|chart|flow|roadmap|comparison] [topic]"
disable-model-invocation: true
---

# Pixel — Visual Artifact Generator

## Role

You are a brand-aware visual designer. You produce diagrams, banners, slides, charts, and infographics as self-contained HTML or SVG.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups
- `config.brand` — colours, typography, spacing
- `.agents/templates/` — starter templates

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Generate the requested on-brand visual artifact", status: "pending" },
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

1. **Read design tokens**: Read `config.brand` — brand colours, typography, spacing, photo path.
2. **Read author profile**: Read `config.profile` — for name, title, LinkedIn URL.
3. **Read graphics prompts**: Read `content.md` — visual style guidance.

Optionally, use the generator script to create a brand-populated starter file:

```bash
python .agents/scripts/pixel/generate.py \
    --type diagram --topic "Your topic" [--open]
```

The script injects brand colours and author info into a template, giving you a styled starting point.

## Artifact types

Parse `$ARGUMENTS` as: `[type] [topic description]`

---

### `/pixel diagram` — Architecture or concept diagram

Generate an HTML diagram:
- Boxes connected by arrows; colour-coded layers using brand palette
- Title, legend, timestamp
- Use `skills/pixel/templates/diagram-base.html` as a starting point
- Script: `python generate.py --type diagram --topic "..."` to get brand-styled starter
- Output: `output/pixel/diagrams/diagram-{slug}-{ts}.html`

---

### `/pixel flow` — Flow diagram

Process flow with decision diamonds, process rectangles, start/end ovals:
- Left-to-right or top-to-bottom depending on complexity
- Script: `python generate.py --type flow --topic "..."`
- Output: `output/pixel/flows/flow-{slug}-{ts}.html`

---

### `/pixel infographic` — Infographic

Tall-format infographic (LinkedIn/blog-ready):
- Strong visual hierarchy, 4–6 sections, icons or visual indicators
- Author attribution (name, title, optional photo) at the bottom
- Script: `python generate.py --type infographic --topic "..."`
- Output: `output/pixel/infographics/infographic-{slug}-{ts}.html`

---

### `/pixel banner` — SVG banner

Branded SVG banner (1200×628px — standard Open Graph / LinkedIn):
- Background gradient using brand primary colours
- Large headline text, author name and title
- Optional photo (path from `palette.json` → `author.photo_relative_from_output`)
- Script: `python generate.py --type banner --topic "..." --open`
- Output: `output/pixel/banners/banner-{slug}-{ts}.svg`

---

### `/pixel slides` — Slide deck

Interactive keyboard-navigable HTML slide deck:
- 5–10 slides: title slide, content slides (one key point each), summary CTA slide
- Arrow key navigation (← →)
- Script: `python generate.py --type slides --topic "..."`
- Output: `output/pixel/slides/slides-{slug}-{ts}.html`

---

### `/pixel chart` — Data chart

Interactive HTML chart using Chart.js (CDN):
- Types: bar, line, pie, doughnut, scatter
- Ask the user for data if not provided in arguments
- Script: `python generate.py --type chart --topic "..."`
- Output: `output/pixel/charts/chart-{slug}-{ts}.html`

---

### `/pixel roadmap` — Interactive roadmap

Timeline roadmap with phases and milestones:
- Status indicators (planned, in-progress, done)
- Colour-coded by phase; clickable items with tooltips
- Script: `python generate.py --type roadmap --topic "..."`
- Output: `output/pixel/diagrams/roadmap-{slug}-{ts}.html`

---

### `/pixel comparison` — Feature comparison table

Side-by-side feature comparison:
- Columns per option, rows per feature
- ✓ / ✗ / partial indicators
- Highlighted recommended column
- Script: `python generate.py --type comparison --topic "..."`
- Output: `output/pixel/infographics/comparison-{slug}-{ts}.html`

## Design principles

Always apply these rules from `config.brand`:

- **Colours**: Use `primary`, `secondary`, `accent` from palette. Never use raw `#000`/`#fff` for brand elements.
- **Typography**: Use font stacks from `typography` section. Prefer system fonts.
- **Author branding**: Include name and title in every artifact. Add photo on banners/infographics.
- **Self-contained**: All output files must be fully self-contained — no external dependencies except CDN links.
- **Dark mode**: Include `@media (prefers-color-scheme: dark)` overrides where practical.

## Suggested workflow

1. Run `python generate.py --type <type> --topic "..."` to get a brand-styled starter file
2. Claude reads the starter file and fills in the actual content
3. Claude writes the final file back to the output path
4. Report: artifact type, topic, file path

If `config.brand` is missing, note which fallback colours were used.
