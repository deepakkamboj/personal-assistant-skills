# Configuration

This plugin keeps **all** user data in a small set of files resolved from one environment
variable. There is no `data/` folder. This guide explains each file, the `config.json`
schema, and how to create them.

## Files at a glance

| File          | Format   | Purpose                                                        | Template                          |
| ------------- | -------- | -------------------------------------------------------------- | --------------------------------- |
| `config.json` | JSON     | Structured data: profile, brand tokens, digest sources, newsletter | `.agents/config/config.example.json` |
| `content.md`  | Markdown | Voice samples, graphics prompts, template guidance             | `.agents/config/content.example.md`  |
| `memory.md`   | Markdown | Durable learned facts/preferences (skills append here)         | `.agents/config/memory.example.md`   |
| `notes.md`    | Markdown | Running task/session notes and follow-ups                      | `.agents/config/notes.example.md`    |
| `.env`        | dotenv   | Secrets for the newsletter FTP deploy + MCP env-file pointer   | `.env.example`                    |

All are **gitignored** — never commit real ones.

## Resolution

- `config.json` is found via the **`ASSISTANT_CONFIG`** environment variable, falling back to
  `~/.assistant/config.json`.
- `content.md`, `memory.md`, `notes.md`, and the output directory are resolved from
  `config.paths.*`, relative to the folder that holds `config.json` (defaults: sibling files).

```jsonc
"paths": {
  "content": "./content.md",
  "memory": "./memory.md",
  "notes": "./notes.md",
  "output_dir": "./output"
}
```

## Create the files

### Option A — CLI (recommended)

```bash
npm install --global personal-assistant-skills
assistant-skills init                 # writes to ~/.assistant/
# or choose a location:
assistant-skills init --dir ./my-config
```

Then set the env var (printed by `init`):

```powershell
setx ASSISTANT_CONFIG "$HOME\.assistant\config.json"   # Windows
```

```bash
export ASSISTANT_CONFIG="$HOME/.assistant/config.json"  # macOS/Linux
```

### Option B — Manual copy

```bash
mkdir -p ~/.assistant
cp .agents/config/config.example.json ~/.assistant/config.json
cp .agents/config/content.example.md  ~/.assistant/content.md
cp .agents/config/memory.example.md   ~/.assistant/memory.md
cp .agents/config/notes.example.md    ~/.assistant/notes.md
```

## `config.json` schema

```jsonc
{
  "meta": { "description": "...", "version": "3.0.0" },

  "profile": {
    "name": "Your Name",
    "title": "Your Title",
    "company": "Your Company",
    "email": "you@example.com",
    "linkedin": "https://www.linkedin.com/in/your-handle/",
    "website": "https://example.com",
    "headline": "Your Title at Your Company | Topic One | Topic Two",
    "tagline": "Your one-line positioning statement",
    "bio": { "short": "", "long": "" },
    "content_pillars": ["Topic One", "Topic Two", "Topic Three"],
    "keywords": ["keyword1", "keyword2"],
    "writing_style": {
      "tone": ["direct", "conversational", "data-driven"],
      "vocabulary_prefer": [],
      "vocabulary_avoid": ["excited to announce", "game-changer", "synergy"],
      "sentence_structure": "short punchy sentences with occasional longer ones",
      "avoid_em_dashes": true
    },
    "photo": ""
  },

  "brand": {
    // Design tokens used by the pixel skill: colors, typography, spacing,
    // radius, shadows, canvas_sizes, diagram_themes, slide_themes.
  },

  "digest": {
    "categories": ["breaking_news", "models_apis", "research_papers", "..."],
    "sources": [
      {
        "id": "openai-blog",
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog",
        "rss": "https://openai.com/blog/rss.xml",
        "category": "AI Research & Company Blogs",
        "digest_categories": ["breaking_news", "models_apis"],
        "linkedin_worthy": true
      }
      // ... more sources
    ]
  },

  "newsletter": {
    "settings": {
      "title": "AI Weekly by Your Name",
      "tagline": "...",
      "cta_label": "Subscribe on LinkedIn",
      "cta_url": "https://www.linkedin.com/build-relation/newsletter-follow?entityUrn=YOUR_NEWSLETTER_URN",
      "reply_to": "you@example.com",
      "base_url": "https://example.com/newsletters",
      "sections": ["top_stories", "research_highlights", "..."]
    },
    "subscribers": [
      { "email": "you@example.com", "name": "Your Name", "tags": ["owner"], "source": "self" }
    ]
  },

  "paths": {
    "content": "./content.md",
    "memory": "./memory.md",
    "notes": "./notes.md",
    "output_dir": "./output"
  }
}
```

### Field notes

- **`profile`** — read by every skill to personalize output. Fill `name`, `title`,
  `company`, `headline`, `content_pillars`, and `writing_style` first.
- **`brand`** — design tokens for the `pixel` skill. Edit colors/typography to match your brand.
- **`digest.sources`** — the `ai-digest` skill researches these. Ships with 60 public AI sources.
- **`newsletter`** — settings + seed subscribers for the `newsletter` skill.
- **`paths`** — where the companion files and generated output live.

Run `python .agents/scripts/me/profile_check.py` to see which profile fields are still empty.

## `content.md`, `memory.md`, `notes.md`

- **`content.md`** — paste 3–5 of your own writing samples and keep the graphics-prompt
  templates. Skills read it when tone matters.
- **`memory.md`** — durable facts the assistant learns about you. Skills append here via
  `python .agents/scripts/memory.py remember "..."`.
- **`notes.md`** — running task notes. Skills append via
  `python .agents/scripts/memory.py note "..."`.

## `.env` (secrets)

Only the newsletter FTP deploy and the MCP server need secrets. See `.env.example`.
Never place OAuth secrets in `config.json` — the `connected-workspace` MCP server manages
Gmail/Calendar/LinkedIn credentials in its own env file.
