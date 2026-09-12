# Assistant Content: Prompts, Voice & Templates

Prose companion to `config.json`. Copy this to the path set in `config.paths.content`
(default `content.md` next to your config file). Structured data lives in `config.json`;
free-form prompts, voice samples, and template guidance live here.

---

## Writing Voice & Samples

Used by the `me`, `linkedin`, `ai-digest`, and `newsletter` skills to calibrate tone.
For prose quality, apply the [[humanize]] skill to whatever you draft.
Paste 3-5 representative samples of your own writing below. Match the `profile.writing_style`
settings in `config.json`.

### Sample 1: LinkedIn post

> _(paste a real post you wrote here)_

### Sample 2: Short professional bio

> _(paste your preferred bio here)_

### Sample 3: Conversational / opinion

> _(paste an opinion-style paragraph here)_

**Voice rules**

- Open with a concrete hook, never "I'm excited to announce".
- Prefer short, punchy sentences; vary rhythm with the occasional longer line.
- No em dashes; no corporate jargon unless it appears in your samples.
- Be direct, conversational, and data-driven.

---

## Graphics Prompts: Visual Style Guide

Reference prompts for the `pixel` skill. Use these as style templates when generating
AI image prompts or designing HTML/SVG artifacts. Always reference the `brand.colors`
primary/secondary values from `config.json` in every prompt.

### 1. Futuristic Comparison (VS / Side-by-Side)

_Best for: technology comparisons, product comparisons, feature face-offs._
**Style:** Dark background, dual glow, 3D icons, cinematic lighting.

> A high-quality wide-angle digital graphic titled **[Main Title]**. Split into two halves:
> the left represents **[Topic A]** in a **[Color 1]** glow, the right **[Topic B]** in a
> **[Color 2]** glow. A large glowing "VS" in the center. Each side has a 3D icon and 3 bullet
> points. Dark blurred technological background with bokeh circuit patterns. Futuristic, sleek,
> 8k, cinematic lighting.

### 2. Narrative Cartoon (Problem vs. Solution)

_Best for: before/after stories, problem framing, educational content._
**Style:** 2D vector, split-screen, mascot characters, flat design.

> A vertical split-screen 2D vector illustration. Left: an orange-tinted background with a
> frustrated robot mascot struggling with **[Problem]**, messy scribbles, red warning sign.
> Right: a teal-tinted background with a happy robot mascot on a rocket labeled **[Solution]**
> soaring up a clean path. A gauge at the bottom shows **[Metric]**. Flat design, vibrant colors.

### 3. Technical Flowchart (Data Architecture)

_Best for: system diagrams, data flows, architectural overviews._
**Style:** Light grey background, blue arrows, minimalist icons, clean UI/UX.

> A professional technical infographic on a light grey background titled **[System Name]**.
> Left: a **[Primary Actor]** connected by blue arrows to folders labeled **[Folder Names]**.
> A central dashed line shows a **[Percentage]** reduction in **[Metric]**. Right: a funnel-shaped
> flow for **[Alternative Method]** into a **[Secondary Actor]**. Small comparison table at bottom.
> Minimalist icons, readable sans-serif typography.

### 4. Hand-Drawn Notebook Guide

_Best for: tips lists, how-to guides, LinkedIn carousels._
**Style:** Spiral notebook aesthetic, pastel colors, handwritten fonts, doodles.

> An educational infographic styled like a hand-drawn spiral notebook page. Title: "**[X] Ways to
> [Goal]**" in marker font. A 2x3 grid of colorful boxes, each with handwritten text, doodles, and
> UI screenshots. Pastel palette. Footer: "FOLLOW **[NAME]** FOR MORE CONTENT" with an avatar.

### 5. 3D Isometric Process Flow

_Best for: showing data/product movement through a system._
**Style:** Isometric 3D, glowing path, soft shadows, Octane render aesthetic.

> A high-quality isometric 3D process flow on a neutral background. Starts with a
> **[Starting Object]** and follows a glowing path through **[Station 1]**, **[Station 2]**,
> **[Station 3]**. Stylized 3D icons float above each station. Palette of **[Color 1]** and
> **[Color 2]**. Soft shadows, ambient occlusion, 8k, Octane render.

### 6. Subway Map Roadmap

_Best for: timelines, learning paths, multi-step journeys._
**Style:** Subway/transit map, dark background, neon colors, futuristic UI.

> A minimalist roadmap styled like a subway map on a dark background. A thick glowing line winds
> across the screen with **[Number]** circular stops, each labeled with a number and short title.
> Beside each stop a tiny glowing vector icon. High contrast, vibrant neon colors.

### 7. Hub & Spoke Breakdown

_Best for: explaining a core concept and its features or integrations._
**Style:** Glassmorphism, circular layout, frosted glass, soft backlighting.

> A circular hub-and-spoke diagram. Center: a detailed 3D icon for **[Core Subject]**. Radiating
> outward, **[Number]** thin lines to peripheral circles, each with a unique icon for
> **[Feature]**. Glassmorphism with frosted glass and soft backlighting.

### 8. Layered Tech Stack Pyramid

_Best for: architecture hierarchy, "levels of" concepts._
**Style:** 3D perspective pyramid, semi-transparent layers, corporate-tech.

> A layered pyramid infographic showing a 5-tier stack. Wide base labeled **[Base Layer]**, each
> layer smaller toward a glowing apex labeled **[Top Layer]**. Shades of **[Color Family]**,
> semi-transparent. Annotate each layer with white text. 3D perspective, sleek corporate-tech.

### Pro Tips

| Tip                    | Detail                                                             |
| ---------------------- | ----------------------------------------------------------------- |
| **Aspect ratio**       | `16:9` for comparison/architecture, `4:5` for notebook/portrait   |
| **Clean backgrounds**  | Add "white background" / "isolated on neutral gray" to cut noise  |
| **Text in images**     | Keep labels to 1-2 words, short labels render most accurately     |
| **Series consistency** | Reuse identical style descriptors for a cohesive set              |
| **Color palette**      | Always specify a two-tone palette                                  |
| **Brand alignment**    | Reference `brand.colors` primary/secondary from `config.json`      |
