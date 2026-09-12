---
name: newsletter
description: >
  Full-stack newsletter system. Generates branded HTML newsletters (reusing
  digest CSS components), sends via the connected-workspace MCP (Gmail), deploys to example.com/newsletters/
  via FTP, and tracks opens/clicks via a PHP pixel. Subscriber engagement is
  stored in SQLite to power a funnel pipeline.
argument-hint: "[create|send|deploy|preview|subscribers|pipeline|setup]"
---

# Newsletter Skill — `/newsletter`

## Role

You are the user's newsletter producer. You generate branded HTML newsletters, deploy them, and track engagement.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups
- `config.newsletter.settings` and `config.newsletter.subscribers`

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Generate, deploy, or report on the newsletter as requested", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse the request / `$ARGUMENTS` and list what this skill needs.
2. **Load your profile & memory.** Read `config.profile` (name, role, voice, brand, content pillars), the voice samples in `content.md` when tone matters, and the shared `memory.md` / `notes.md` for learned preferences and open follow-ups.
3. **Ask if anything is missing.** If a required input is unknown, stop and ask a specific question. Never assume, guess, or invent facts, numbers, names, or sources.
4. **Do the work** following the sections below.
5. **Validate, output & record.** Check the result against this skill's rules, return it, then append any new durable fact to `memory.md` and any follow-up to `notes.md` via `python .agents/scripts/memory.py`.

## Commands

### `/newsletter` — Dashboard
Run `scripts/db.py --stats` and display:
- Total subscribers (active / churned)
- Newsletters sent (last 5)
- Pipeline summary: count per funnel stage
- Last newsletter date and open rate

---

### `/newsletter create [date]` — Generate newsletter HTML

Date format: `YYYY-MM-DD` (defaults to today). Slug = `{date}`.

**Content generation process:**
1. Read `config.digest.sources` for source URLs
2. Research the latest AI news using WebSearch for each section (same as digest)
3. Read `config.profile` for author voice and brand
4. Read `config.newsletter.settings` for title, CTA, sections
5. Build the newsletter HTML using the newsletter template (see HTML Design below)
6. Write to `output/newsletter/newsletter-{slug}.html`
7. Register in SQLite via `scripts/db.py --register --slug {slug} --subject "{subject}" --date {date}`
8. Report: file path, web URL (before deploy), item count per section

**Sections to include (same content categories as digest):**
- **Top Stories** (3–5 items): breaking_news + models_apis
- **Research Highlights** (2–3 items): research_papers
- **Tools & Repos** (4–6 items): github_repos + products_tools
- **Agents & Automation** (2–4 items): agents_automation
- **Industry Pulse** (2–3 items): industry_analysis
- **Worth Reading** (3–5 links): tutorials_learning + linkedin_insights

---

### `/newsletter preview [date]` — Open in browser

Run: `python -m http.server 8899 --directory output/newsletter/`
Then print: `http://localhost:8899/newsletter-{slug}.html`

---

### `/newsletter send [date] [--dry-run]` — Send via the Gmail MCP tool

Sending uses the `connected-workspace` MCP server (`gmail_send_message`), not a local script.

1. List active subscribers: `python .agents/scripts/newsletter/db.py --list`
2. For each subscriber, inject the per-recipient tracking pixel with
   `python .agents/scripts/newsletter/template.py inject --slug {date} --email-hash <hash> ...`
3. `--dry-run`: show the subject, preview, and full recipient list — do NOT send.
4. Without `--dry-run`: call the MCP `gmail_send_message` tool once per recipient, then log
   each send to SQLite via `db.py`. Confirm before sending to a real list.

---

### `/newsletter deploy [date]` — Upload to FTP

Run `scripts/ftp_deploy.py --slug {date}`

- Uploads `newsletter-{slug}.html` to FTP `public_html/newsletters/`
- Uploads `scripts/tracker.php` as `track.php` (only if not already on server)
- Prints web URL: `https://example.com/newsletters/newsletter-{slug}.html`
- Updates `ftp_url` in SQLite

---

### `/newsletter subscribers [subcommand]` — Manage list

- `list` → run `scripts/db.py --subscribers` (table: email, name, stage, opens, last seen)
- `add [email] [name]` → run `scripts/db.py --add-subscriber --email X --name Y`
- `remove [email]` → run `scripts/db.py --remove-subscriber --email X`
- `import` → re-import from `config.newsletter.subscribers` into SQLite
- `export` → export SQLite subscribers back to `config.newsletter.subscribers`

---

### `/newsletter pipeline` — Funnel view

Run `scripts/db.py --pipeline` and display:

```
Funnel Stage   Count   Avg Opens   Last Activity
────────────────────────────────────────────────
cold             12       0.0       2026-02-20
warm              8       1.5       2026-02-27
hot               4       4.2       2026-02-26
engaged           3       8.1       2026-02-27
converted         1      12.0       2026-02-24
churned           2        —        2026-02-15
```

---

### `/newsletter setup` — Configuration guide

Sending is handled by the `connected-workspace` MCP server (Gmail OAuth lives there, not in
this repo). For deploy + tracking you only need FTP credentials in `.env`:

1. Register the `connected-workspace` MCP server and authorize Google (for `gmail_send_message`).
2. FTP credentials — set `FTP_HOST`, `FTP_USER`, `FTP_PASSWORD`, `NEWSLETTER_BASE_URL` in `.env`.
3. `python .agents/scripts/newsletter/ftp_deploy.py --slug {date} --check` — verify FTP connection.

---

## HTML Design

**Reuse the exact design system from `output/ai-digest/digest-2026-02-26.html`:**

Same CSS variables (`:root`), same components:
- `.header` — gradient hero block with title, date range, author
- `.editor-note` — left-bordered intro block
- `.section` + `.section-header` + `.section-dot` — section containers
- `.card` + `.card-title` + `.card-body` + `.card-why` + `.card-meta` — content cards
- `.badge` + `.source-link` — item metadata
- `.footer` — author attribution
- Light/dark mode via `@media (prefers-color-scheme: light)`

**Newsletter-specific additions:**
- **Photo signature**: Author photo in footer (`photos/author.png`)
- **CTA block**: Prominent "Subscribe on LinkedIn" button from `settings.json`
- **Web archive link**: "Read in browser: {ftp_url}" banner at top of email
- **Unsubscribe**: Footer link `mailto:{reply_to}?subject={unsubscribe_subject}`
- **Tracking pixel**: 1×1 GIF at end of body (injected per-subscriber at send time)

---

## Output

- Web HTML: `output/newsletter/newsletter-{slug}.html`
- Sent log: `output/newsletter/newsletter.db` (events table)
- FTP URL: `https://example.com/newsletters/newsletter-{slug}.html`
