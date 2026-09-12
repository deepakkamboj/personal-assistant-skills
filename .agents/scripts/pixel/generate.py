#!/usr/bin/env python3
"""
Pixel — brand-aware artifact generator.

Reads brand tokens from the assistant config (`brand`) and the shared
`.agents/templates/` files, then generates a starter HTML/SVG file populated with
brand colours and author info. The agent fills in the actual content afterwards.

Usage:
    python generate.py --type diagram|banner|infographic|slides|chart|flow|roadmap|comparison
                       --topic "Topic description"
                       [--output path/to/output.html]
                       [--open]
"""

import argparse
import json
import re
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import load_config, output_dir  # noqa: E402

# Shared artifact templates live in .agents/templates
TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

# ── Artifact type → template + output subfolder ───────────────────────────────
ARTIFACT_CONFIG = {
    "diagram":     {"template": "diagram-base.html",      "folder": "diagrams"},
    "flow":        {"template": "diagram-base.html",      "folder": "flows"},
    "infographic": {"template": "infographic-base.html",  "folder": "infographics"},
    "banner":      {"template": "banner-base.svg",        "folder": "banners"},
    "slides":      {"template": "slides-base.html",       "folder": "slides"},
    "chart":       {"template": "infographic-base.html",  "folder": "charts"},
    "roadmap":     {"template": "infographic-base.html",  "folder": "diagrams"},
    "comparison":  {"template": "infographic-base.html",  "folder": "infographics"},
}


def load_json_safe(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).lower().strip("-")
    return slug[:max_len]


def get_brand_css(palette: dict) -> str:
    """Generate CSS custom properties from palette.json."""
    colours = palette.get("colors", palette.get("colours", {}))
    primary   = colours.get("primary",   "#0078d4")
    secondary = colours.get("secondary", "#106ebe")
    accent    = colours.get("accent",    "#f3a71e")
    bg        = colours.get("background", "#ffffff")
    text_col  = colours.get("text",      "#1a1a2e")

    typography = palette.get("typography", {})
    font_body  = typography.get("body",    "system-ui, -apple-system, sans-serif")
    font_head  = typography.get("heading", "system-ui, -apple-system, sans-serif")

    return f"""
    :root {{
        --color-primary:   {primary};
        --color-secondary: {secondary};
        --color-accent:    {accent};
        --color-bg:        {bg};
        --color-text:      {text_col};
        --font-body:       {font_body};
        --font-heading:    {font_head};
    }}"""


def get_author_block(profile: dict, palette: dict, output_subdir: Path) -> dict:
    """Build author metadata dict for template injection."""
    author   = palette.get("author", {})

    name     = profile.get("name", "")
    title    = profile.get("title", "")
    company  = profile.get("company", "")
    linkedin = profile.get("linkedin", "")

    # Photo path relative to output subdirectory
    photo_rel = author.get("photo_relative_from_output", "") or profile.get("photo", "")

    return {
        "name":    name,
        "title":   f"{title} @ {company}".strip(" @") if title or company else "",
        "linkedin": linkedin,
        "photo":   photo_rel,
    }


def inject_vars(template: str, replacements: dict) -> str:
    """Replace {{KEY}} placeholders in template string."""
    for key, value in replacements.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template


def generate_artifact(artifact_type: str, topic: str, palette: dict, profile: dict,
                       output_path: Path) -> str:
    """Load template, inject brand vars, write output file. Returns output path."""
    config        = ARTIFACT_CONFIG.get(artifact_type, ARTIFACT_CONFIG["diagram"])
    template_file = TEMPLATES_DIR / config["template"]

    if not template_file.exists():
        print(f"  ⚠  Template not found: {template_file}", file=sys.stderr)
        print( "     Creating minimal stub instead.")
        ext      = ".svg" if artifact_type == "banner" else ".html"
        template = f"<!-- Pixel stub: {artifact_type} — {topic} -->\n<!-- TODO: fill in content -->\n"
    else:
        template = template_file.read_text(encoding="utf-8")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    brand_css    = get_brand_css(palette)
    author_info  = get_author_block(profile, palette, output_path.parent)
    timestamp    = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    replacements = {
        "BRAND_CSS":       brand_css,
        "TOPIC":           topic,
        "ARTIFACT_TYPE":   artifact_type.title(),
        "AUTHOR_NAME":     author_info["name"],
        "AUTHOR_TITLE":    author_info["title"],
        "AUTHOR_LINKEDIN": author_info["linkedin"],
        "AUTHOR_PHOTO":    author_info["photo"],
        "GENERATED_AT":    timestamp,
        "COLOR_PRIMARY":   palette.get("colors", {}).get("primary",   "#0078d4"),
        "COLOR_SECONDARY": palette.get("colors", {}).get("secondary", "#106ebe"),
        "COLOR_ACCENT":    palette.get("colors", {}).get("accent",    "#f3a71e"),
    }

    output_content = inject_vars(template, replacements)
    output_path.write_text(output_content, encoding="utf-8")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate a brand-aware pixel artifact")
    parser.add_argument("--type",   required=True,
                        choices=list(ARTIFACT_CONFIG.keys()),
                        help="Artifact type")
    parser.add_argument("--topic",  required=True,   help="Topic / title for the artifact")
    parser.add_argument("--output", default="",      help="Custom output file path")
    parser.add_argument("--open",   action="store_true", help="Open in browser after generation")
    args = parser.parse_args()

    cfg     = load_config()
    palette = cfg.get("brand", {})
    profile = cfg.get("profile", {})

    if not palette:
        print("  ⚠  config.brand is empty — using default brand colours.")

    config    = ARTIFACT_CONFIG[args.type]
    ext       = ".svg" if args.type == "banner" else ".html"
    slug      = slugify(args.topic)
    ts        = datetime.now().strftime("%Y%m%d%H%M%S")
    subfolder = output_dir() / "pixel" / config["folder"]

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = subfolder / f"{args.type}-{slug}-{ts}{ext}"

    print(f"\n  Generating {args.type}: \"{args.topic}\"")
    print(f"  Template : {config['template']}")
    print(f"  Output   : {output_path}\n")

    path = generate_artifact(args.type, args.topic, palette, profile, output_path)

    print(f"  ✓ Created: {path}")
    if args.open:
        print("  Opening in browser...")
        webbrowser.open(Path(path).as_uri())
    print()


if __name__ == "__main__":
    main()
