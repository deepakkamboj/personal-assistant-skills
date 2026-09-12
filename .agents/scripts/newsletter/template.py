#!/usr/bin/env python3
"""
Newsletter HTML generator for the newsletter skill.

Reuses the exact CSS design system from the digest HTML.
Provides:
  - CSS + HTML template functions
  - CLI to generate a blank newsletter shell or inject per-subscriber tracking

Usage:
  python scripts/template.py --slug 2026-02-27          # generate blank shell
  python scripts/template.py --inject-tracking \\
      --slug 2026-02-27 --email-hash abc123 \\
      --in newsletter-2026-02-27.html \\
      --out newsletter-2026-02-27-subscriber.html
"""

import argparse
import json
import os
import sys
from base64 import urlsafe_b64encode
from pathlib import Path
from urllib.parse import quote_plus

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import load_config, output_dir  # noqa: E402

REPO_ROOT  = Path(__file__).resolve().parents[3]
OUTPUT_DIR = output_dir() / "newsletter"

# ── CSS (exact design system from digest) ──────────────────────────────────────

CSS = """
  :root {
    --primary:       #6366f1;
    --primary-dark:  #4f46e5;
    --primary-light: #a5b4fc;
    --secondary:     #06b6d4;
    --accent:        #f59e0b;
    --success:       #22c55e;
    --danger:        #ef4444;
    --info:          #3b82f6;
    --bg:            #0f172a;
    --surface:       #1e293b;
    --surface2:      #334155;
    --border:        #475569;
    --text:          #f1f5f9;
    --text-muted:    #94a3b8;
    --text-faint:    #64748b;
    --c-breaking:    #ef4444;
    --c-models:      #8b5cf6;
    --c-research:    #3b82f6;
    --c-github:      #22c55e;
    --c-tools:       #f59e0b;
    --c-industry:    #06b6d4;
    --c-agents:      #ec4899;
    --c-reading:     #84cc16;
    --c-linkedin:    #0ea5e9;
    --font: 'Inter', 'Segoe UI', system-ui, sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: var(--font);
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    font-size: 1rem;
  }

  a { color: var(--primary-light); text-decoration: none; }
  a:hover { text-decoration: underline; color: var(--secondary); }

  .wrapper { max-width: 820px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }

  /* ── WEB ARCHIVE BANNER ─────────────────────────────────── */
  .web-banner {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    text-align: center;
  }
  .web-banner a { color: var(--primary-light); font-weight: 500; }

  /* ── HEADER ──────────────────────────────────────────────── */
  .header {
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
  }
  .header::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(255,255,255,0.03) 40px, rgba(255,255,255,0.03) 80px);
  }
  .header-inner { position: relative; }
  .header-label {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: rgba(255,255,255,0.7); margin-bottom: 0.5rem;
  }
  .header h1 { font-size: 2rem; font-weight: 800; color: #fff; line-height: 1.2; }
  .header-meta {
    margin-top: 1rem; font-size: 0.875rem; color: rgba(255,255,255,0.75);
    display: flex; gap: 1.5rem; flex-wrap: wrap;
  }
  .header-meta span { display: flex; align-items: center; gap: 0.35rem; }

  /* ── EDITOR NOTE ──────────────────────────────────────────── */
  .editor-note {
    background: var(--surface);
    border-left: 4px solid var(--primary);
    border-radius: 0 12px 12px 0;
    padding: 1.5rem;
    margin-bottom: 2.5rem;
  }
  .editor-note .label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--primary-light); margin-bottom: 0.75rem;
  }
  .editor-note p { color: var(--text); font-size: 0.975rem; line-height: 1.75; }
  .editor-note .sign-off { margin-top: 1rem; font-size: 0.875rem; color: var(--text-muted); }
  .editor-photo {
    display: flex; align-items: center; gap: 1rem; margin-top: 1.25rem;
  }
  .editor-photo img {
    width: 52px; height: 52px; border-radius: 50%;
    border: 2px solid var(--primary); object-fit: cover; flex-shrink: 0;
  }
  .editor-photo-info { font-size: 0.875rem; }
  .editor-photo-name { font-weight: 600; color: var(--text); }
  .editor-photo-role { color: var(--text-muted); font-size: 0.8rem; }

  /* ── SECTION ──────────────────────────────────────────────── */
  .section { margin-bottom: 2.5rem; }
  .section-header {
    display: flex; align-items: center; gap: 0.75rem;
    margin-bottom: 1.25rem; padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
  }
  .section-dot {
    width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0;
  }
  .section-header h2 {
    font-size: 1.125rem; font-weight: 700; color: var(--text);
  }
  .section-count {
    margin-left: auto; font-size: 0.75rem; color: var(--text-faint);
    background: var(--surface2); border-radius: 999px; padding: 0.15rem 0.6rem;
  }

  /* ── CARD ─────────────────────────────────────────────────── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.875rem;
    transition: border-color 0.2s;
  }
  .card:hover { border-color: var(--primary); }
  .card-title {
    font-size: 1rem; font-weight: 600; color: var(--text);
    margin-bottom: 0.4rem; line-height: 1.4;
  }
  .card-title a { color: var(--text); }
  .card-title a:hover { color: var(--primary-light); text-decoration: none; }
  .card-body { font-size: 0.9rem; color: var(--text-muted); line-height: 1.65; }
  .card-why {
    margin-top: 0.6rem; font-size: 0.825rem;
    padding: 0.4rem 0.75rem; border-radius: 6px;
    background: var(--surface2); color: var(--primary-light);
  }
  .card-why strong { color: var(--accent); }
  .card-meta {
    display: flex; gap: 0.5rem; flex-wrap: wrap;
    margin-top: 0.75rem; align-items: center;
  }
  .badge {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em;
    padding: 0.2rem 0.6rem; border-radius: 999px;
    text-transform: uppercase;
  }
  .source-link {
    font-size: 0.8rem; color: var(--text-faint); margin-left: auto;
  }

  /* ── HIGHLIGHT CARD (top pick) ────────────────────────────── */
  .card-highlight {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(6,182,212,0.08) 100%);
    border: 1px solid var(--primary);
  }

  /* ── WORTH READING LIST ───────────────────────────────────── */
  .reading-item {
    display: flex; align-items: flex-start; gap: 1rem;
    padding: 0.875rem 0; border-bottom: 1px solid var(--surface2);
  }
  .reading-item:last-child { border-bottom: none; }
  .reading-num {
    font-size: 0.75rem; font-weight: 700; color: var(--primary);
    background: rgba(99,102,241,0.15); border-radius: 6px;
    padding: 0.25rem 0.5rem; flex-shrink: 0; min-width: 2rem; text-align: center;
  }
  .reading-item-text { font-size: 0.9rem; color: var(--text-muted); }
  .reading-item-text a { color: var(--text); font-weight: 500; }

  /* ── CTA BLOCK ────────────────────────────────────────────── */
  .cta-block {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(6,182,212,0.1) 100%);
    border: 1px solid var(--primary);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 2.5rem 0;
  }
  .cta-block h3 {
    font-size: 1.25rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem;
  }
  .cta-block p {
    font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.25rem;
  }
  .cta-btn {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
    color: #fff !important;
    font-weight: 700; font-size: 0.9rem;
    padding: 0.7rem 2rem; border-radius: 999px;
    text-decoration: none !important;
    letter-spacing: 0.03em;
  }
  .cta-btn:hover { opacity: 0.9; text-decoration: none !important; }

  /* ── FOOTER ──────────────────────────────────────────────── */
  .footer {
    text-align: center; padding: 2rem 0 0;
    border-top: 1px solid var(--border);
    font-size: 0.85rem; color: var(--text-faint);
    margin-top: 3rem;
  }
  .footer strong { color: var(--text-muted); }
  .footer-photo {
    display: flex; align-items: center; justify-content: center;
    gap: 1rem; margin-bottom: 1.25rem;
  }
  .footer-photo img {
    width: 56px; height: 56px; border-radius: 50%;
    border: 2px solid var(--primary); object-fit: cover;
  }
  .footer-photo-info { text-align: left; }
  .footer-photo-name { font-weight: 600; color: var(--text); font-size: 0.95rem; }
  .footer-photo-role { color: var(--text-muted); font-size: 0.8rem; }
  .footer-links { margin-top: 0.75rem; display: flex; gap: 1.25rem; justify-content: center; flex-wrap: wrap; }
  .footer-links a { color: var(--text-faint); font-size: 0.8rem; }
  .footer-links a:hover { color: var(--primary-light); }
  .unsubscribe-link { margin-top: 0.75rem; font-size: 0.75rem; color: var(--text-faint); }
  .unsubscribe-link a { color: var(--text-faint); text-decoration: underline; }

  /* ── LIGHT MODE ──────────────────────────────────────────── */
  @media (prefers-color-scheme: light) {
    :root {
      --bg:            #f8fafc;
      --surface:       #ffffff;
      --surface2:      #eef2f7;
      --border:        #cbd5e1;
      --text:          #0f172a;
      --text-muted:    #334155;
      --text-faint:    #64748b;
      --primary-light: #4f46e5;
    }
    .card-why { color: #3730a3; background: #eef2ff; }
    .card-why strong { color: #b45309; }
    .editor-note { background: #eef2ff; border-left-color: var(--primary); }
    .editor-note .label { color: #4338ca; }
    .editor-note p, .editor-note .sign-off { color: #1e293b; }
    .section-count { background: #e2e8f0; color: #475569; }
    .reading-item-text { color: #334155; }
    .footer { color: #475569; }
    .footer a { color: #4f46e5; }
    .reading-num { background: #e0e7ff; color: #3730a3; }
    .card-highlight { background: linear-gradient(135deg, #eef2ff 0%, #ecfeff 100%); border-color: #818cf8; }
    .web-banner { background: #f1f5f9; border-color: #cbd5e1; }
  }

  @media (max-width: 600px) {
    .header h1 { font-size: 1.5rem; }
    .header-meta { flex-direction: column; gap: 0.5rem; }
    .footer-photo { flex-direction: column; text-align: center; }
    .footer-photo-info { text-align: center; }
  }
"""

# ── Tracking placeholders (replaced per-subscriber at send time) ─────────────

PIXEL_PLACEHOLDER      = "{{TRACKING_PIXEL}}"
ARCHIVE_URL_PLACEHOLDER = "{{ARCHIVE_URL}}"


# ── HTML builder functions ────────────────────────────────────────────────────

def _html_shell(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>{CSS}
  </style>
</head>
<body>
<div class="wrapper">
{body}
</div>
</body>
</html>
"""


def build_web_archive_banner(web_url: str) -> str:
    return f"""
  <!-- ── WEB ARCHIVE BANNER ──────────────────────────────────────── -->
  <div class="web-banner">
    Having trouble reading this? <a href="{web_url}" target="_blank">Read in browser →</a>
  </div>
"""


def build_header(newsletter_title: str, subject: str, date: str,
                  author_name: str, author_role: str) -> str:
    return f"""
  <!-- ── HEADER ───────────────────────────────────────────────────── -->
  <header class="header">
    <div class="header-inner">
      <div class="header-label">{newsletter_title}</div>
      <h1>{subject}</h1>
      <div class="header-meta">
        <span>✦ {author_name}</span>
        <span>{author_role}</span>
        <span>Issue {date}</span>
      </div>
    </div>
  </header>
"""


def build_editor_note(note_html: str, author_name: str, author_role: str,
                       photo_path: str) -> str:
    photo_tag = ""
    if photo_path:
        photo_tag = f"""
    <div class="editor-photo">
      <img src="{photo_path}" alt="{author_name}">
      <div class="editor-photo-info">
        <div class="editor-photo-name">{author_name}</div>
        <div class="editor-photo-role">{author_role}</div>
      </div>
    </div>"""
    return f"""
  <!-- ── EDITOR'S NOTE ────────────────────────────────────────────── -->
  <section class="editor-note">
    <div class="label">Editor's Note</div>
    {note_html}{photo_tag}
  </section>
"""


def build_section(heading: str, dot_color: str, count: int, items_html: str) -> str:
    return f"""
  <!-- ── {heading.upper()} ──────────────────────────────────────────────── -->
  <section class="section">
    <div class="section-header">
      <div class="section-dot" style="background:{dot_color}"></div>
      <h2>{heading}</h2>
      <span class="section-count">{count} item{"s" if count != 1 else ""}</span>
    </div>
    {items_html}
  </section>
"""


def build_card(title: str, url: str, body: str, why: str,
               badge_label: str, badge_style: str, source_label: str,
               source_url: str, highlight: bool = False) -> str:
    highlight_cls = " card-highlight" if highlight else ""
    title_inner = f'<a href="{url}" target="_blank">{title}</a>' if url else title
    why_block   = f'<div class="card-why"><strong>Why it matters:</strong> {why}</div>' if why else ""
    badge_block = f'<span class="badge" style="{badge_style}">{badge_label}</span>' if badge_label else ""
    src_block   = f'<a class="source-link" href="{source_url}" target="_blank">{source_label} →</a>' if source_url else ""
    return f"""    <div class="card{highlight_cls}">
      <div class="card-title">{title_inner}</div>
      <div class="card-body">{body}</div>
      {why_block}
      <div class="card-meta">
        {badge_block}
        {src_block}
      </div>
    </div>
"""


def build_reading_list(items: list) -> str:
    """items: list of {title, url, description}"""
    rows = ""
    for i, item in enumerate(items, 1):
        rows += f"""    <div class="reading-item">
      <div class="reading-num">{i:02d}</div>
      <div class="reading-item-text">
        <a href="{item['url']}" target="_blank">{item['title']}</a>
        {' — ' + item.get('description', '') if item.get('description') else ''}
      </div>
    </div>
"""
    return rows


def build_cta_block(heading: str, subtext: str, btn_label: str, btn_url: str) -> str:
    return f"""
  <!-- ── CTA ──────────────────────────────────────────────────────── -->
  <div class="cta-block">
    <h3>{heading}</h3>
    <p>{subtext}</p>
    <a href="{btn_url}" class="cta-btn" target="_blank">{btn_label}</a>
  </div>
"""


def build_footer(author_name: str, author_role: str, photo_path: str,
                  reply_to: str, unsubscribe_subject: str,
                  linkedin_url: str, website_url: str) -> str:
    photo_tag = ""
    if photo_path:
        photo_tag = f"""    <div class="footer-photo">
      <img src="{photo_path}" alt="{author_name}">
      <div class="footer-photo-info">
        <div class="footer-photo-name">{author_name}</div>
        <div class="footer-photo-role">{author_role}</div>
      </div>
    </div>
"""
    unsub = ""
    if reply_to:
        subject_enc = quote_plus(unsubscribe_subject or "Unsubscribe")
        unsub = f"""    <div class="unsubscribe-link">
      <a href="mailto:{reply_to}?subject={subject_enc}">Unsubscribe</a> ·
      You're receiving this because you subscribed to {author_name}'s AI Weekly.
    </div>
"""
    return f"""
  <!-- ── FOOTER ───────────────────────────────────────────────────── -->
  <footer class="footer">
{photo_tag}    <div>
      <strong>{author_name}</strong><br>
      {author_role}
    </div>
    <div class="footer-links">
      <a href="{linkedin_url}" target="_blank">LinkedIn</a>
      <a href="{website_url}" target="_blank">Website</a>
      <a href="mailto:{reply_to}">Email</a>
    </div>
{unsub}    <div style="margin-top:1.5rem;font-size:0.75rem;color:var(--text-faint)">
      © {__import__('datetime').date.today().year} {author_name} · All rights reserved
    </div>
  </footer>
"""


def build_tracking_pixel_placeholder() -> str:
    """Returns the placeholder tag replaced with a real pixel at send time."""
    return f'\n  <!-- tracking -->\n  <img src="{PIXEL_PLACEHOLDER}" width="1" height="1" alt="" style="display:none">\n'


# ── Tracking injection (used at send time) ──────────────────────────────────

def inject_tracking(html: str, base_url: str, slug: str,
                    email_hash: str, archive_url: str = "") -> str:
    """
    Replace placeholders with per-subscriber tracking tokens.

    Replaces:
      {{TRACKING_PIXEL}}  →  {base_url}/track.php?t=open&n={slug}&e={email_hash}
      {{ARCHIVE_URL}}     →  archive_url (if given)
      All <a href="...">  →  click-tracked redirect URLs (except mailto/unsubscribe)
    """
    # Tracking pixel
    pixel_url = f"{base_url}/track.php?t=open&n={slug}&e={email_hash}"
    html = html.replace(PIXEL_PLACEHOLDER, pixel_url)

    # Archive URL
    if archive_url:
        html = html.replace(ARCHIVE_URL_PLACEHOLDER, archive_url)

    # Wrap all outbound links with click tracker (except mailto and already-tracked)
    import re
    def wrap_link(m):
        href = m.group(1)
        if href.startswith("mailto:") or "track.php" in href or not href.startswith("http"):
            return m.group(0)
        encoded = urlsafe_b64encode(href.encode()).decode().rstrip("=")
        tracked = f"{base_url}/track.php?t=click&n={slug}&e={email_hash}&u={encoded}"
        return f'href="{tracked}"'

    html = re.sub(r'href="(https?://[^"]+)"', wrap_link, html)
    return html


# ── Shell template generator ──────────────────────────────────────────────────

def generate_shell(slug: str, settings: dict, profile: dict) -> str:
    """
    Generate a blank newsletter HTML shell with placeholder sections.
    Claude Code fills in the actual content when running /newsletter-skill create.
    """
    title     = settings.get("title", "AI Weekly")
    tagline   = settings.get("tagline", "")
    cta_label = settings.get("cta_label", "Subscribe on LinkedIn")
    cta_url   = settings.get("cta_url", "#")
    reply_to  = settings.get("reply_to", "")
    unsub_sub = settings.get("unsubscribe_subject", "Unsubscribe")
    base_url  = settings.get("base_url", "")
    web_url   = f"{base_url}/newsletter-{slug}.html" if base_url else ""

    author_name = profile.get("name", "")
    author_role = (
        profile.get("title", "") + " · " + profile.get("company", "")
    ).strip(" ·")
    linkedin    = profile.get("linkedin", "#")
    website     = profile.get("website", "#")
    email_pub   = profile.get("email", reply_to)
    photo_path  = profile.get("photo", "")

    body = ""
    if web_url:
        body += build_web_archive_banner(ARCHIVE_URL_PLACEHOLDER if web_url else web_url)
    body += build_header(title, f"[Newsletter Subject — {slug}]", slug, author_name, author_role)
    body += build_editor_note(
        '<p>[Editor\'s note goes here]</p>',
        author_name, author_role, photo_path
    )

    # Placeholder sections
    section_configs = [
        ("Top Stories",          "var(--c-breaking)",  "<!-- cards go here -->"),
        ("Research Highlights",  "var(--c-research)",  "<!-- cards go here -->"),
        ("Tools & Repos",        "var(--c-tools)",     "<!-- cards go here -->"),
        ("Agents & Automation",  "var(--c-agents)",    "<!-- cards go here -->"),
        ("Industry Pulse",       "var(--c-industry)",  "<!-- cards go here -->"),
        ("Worth Reading",        "var(--c-reading)",   "<!-- reading items go here -->"),
    ]
    for heading, color, placeholder in section_configs:
        body += build_section(heading, color, 0, placeholder)

    body += build_cta_block(
        f"Enjoyed this issue of {title}?",
        tagline,
        cta_label,
        cta_url
    )
    body += build_footer(author_name, author_role, photo_path,
                         reply_to, unsub_sub, linkedin, website)
    body += build_tracking_pixel_placeholder()

    return _html_shell(f"{title} — {slug}", body)


# ── CLI ───────────────────────────────────────────────────────────────────────

def load_env():
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def main():
    parser = argparse.ArgumentParser(description="Newsletter HTML template tool")
    sub    = parser.add_subparsers(dest="cmd")

    # generate shell
    gen = sub.add_parser("generate", help="Generate blank newsletter shell HTML")
    gen.add_argument("--slug", required=True, help="Date slug, e.g. 2026-02-27")
    gen.add_argument("--out",  help="Output file path (default: output/newsletter/newsletter-{slug}.html)")

    # inject tracking tokens
    inj = sub.add_parser("inject", help="Inject per-subscriber tracking tokens into HTML")
    inj.add_argument("--slug",       required=True)
    inj.add_argument("--email-hash", required=True, dest="email_hash")
    inj.add_argument("--in",         required=True, dest="infile",  help="Source HTML file")
    inj.add_argument("--out",        required=True, dest="outfile", help="Output HTML file")
    inj.add_argument("--archive-url", default="", dest="archive_url")

    args = parser.parse_args()

    load_env()

    cfg      = load_config()
    settings = (cfg.get("newsletter", {}) or {}).get("settings", {})
    profile  = cfg.get("profile", {})

    if not settings:
        print("ERROR: config.newsletter.settings is empty", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "generate":
        html = generate_shell(args.slug, settings, profile)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out  = Path(args.out) if args.out else OUTPUT_DIR / f"newsletter-{args.slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"Generated: {out}")

    elif args.cmd == "inject":
        base_url = os.environ.get("NEWSLETTER_BASE_URL",
                                  settings.get("base_url", "")).rstrip("/")
        if not base_url:
            print("ERROR: NEWSLETTER_BASE_URL not set", file=sys.stderr)
            sys.exit(1)
        html = Path(args.infile).read_text(encoding="utf-8")
        html = inject_tracking(html, base_url, args.slug, args.email_hash, args.archive_url)
        Path(args.outfile).write_text(html, encoding="utf-8")
        print(f"Tracking injected: {args.outfile}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
