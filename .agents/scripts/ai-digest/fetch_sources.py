#!/usr/bin/env python3
"""
AI Digest — source content fetcher.

Reads the `digest.sources` list from the assistant config, fetches recent content from
RSS feeds and web pages, and saves structured JSON for the digest skill to process.

Usage:
    python fetch_sources.py [--date YYYY-MM-DD] [--categories cat1,cat2]
                            [--output path.json] [--max-items N]

Examples:
    python fetch_sources.py                             # fetch all sources for today
    python fetch_sources.py --date 2026-02-17           # fetch for a specific week start
    python fetch_sources.py --categories models_apis,research_papers
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import load_config, output_dir  # noqa: E402

USER_AGENT = "Mozilla/5.0 (compatible; PersonalAssistantSkills/3.0; +https://github.com/personal-assistant-skills)"


def load_sources() -> dict:
    cfg = load_config()
    digest = cfg.get("digest", {})
    if not digest.get("sources"):
        print("✗ config.digest.sources is empty", file=sys.stderr)
        sys.exit(1)
    return digest


class HTMLTextExtractor(HTMLParser):
    """Simple HTML → plain text extractor."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._in_skip = False
        self._skip_tags = {"script", "style", "noscript", "nav", "header", "footer"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._in_skip = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._in_skip = False

    def handle_data(self, data):
        if not self._in_skip:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

    def get_text(self) -> str:
        return " ".join(self.text_parts)


def fetch_url(url: str, timeout: int = 15) -> str | None:
    """Fetch URL content. Returns text or None on failure."""
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            charset = "utf-8"
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].split(";")[0].strip()
            return resp.read().decode(charset, errors="replace")
    except (URLError, HTTPError, Exception) as e:
        return None


def parse_rss(xml_text: str, max_items: int, since_date: datetime) -> list:
    """Parse RSS/Atom XML. Returns list of {title, url, summary, published}."""
    import xml.etree.ElementTree as ET
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    # RSS 2.0
    ns = {}
    for item in root.findall(".//item")[:max_items * 2]:
        title   = item.findtext("title", "").strip()
        link    = item.findtext("link",  "").strip()
        summary = item.findtext("description", "").strip()
        pub_str = item.findtext("pubDate", "")

        pub_date = None
        if pub_str:
            for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT"):
                try:
                    pub_date = datetime.strptime(pub_str.strip(), fmt)
                    break
                except ValueError:
                    continue

        if pub_date and pub_date.replace(tzinfo=timezone.utc) < since_date:
            continue

        # Strip HTML from summary
        extractor = HTMLTextExtractor()
        extractor.feed(summary)
        clean_summary = extractor.get_text()[:500]

        items.append({
            "title":     title,
            "url":       link,
            "summary":   clean_summary,
            "published": pub_str,
        })
        if len(items) >= max_items:
            break

    # Atom
    atom_ns = "http://www.w3.org/2005/Atom"
    for entry in root.findall(f".//{{{atom_ns}}}entry")[:max_items * 2]:
        title   = entry.findtext(f"{{{atom_ns}}}title", "").strip()
        link    = entry.find(f"{{{atom_ns}}}link")
        url     = link.get("href", "") if link is not None else ""
        summary = entry.findtext(f"{{{atom_ns}}}summary", "").strip() or \
                  entry.findtext(f"{{{atom_ns}}}content", "").strip()
        pub_str = entry.findtext(f"{{{atom_ns}}}updated", "") or \
                  entry.findtext(f"{{{atom_ns}}}published", "")

        extractor = HTMLTextExtractor()
        extractor.feed(summary)
        clean_summary = extractor.get_text()[:500]

        items.append({
            "title":     title,
            "url":       url,
            "summary":   clean_summary,
            "published": pub_str,
        })
        if len(items) >= max_items:
            break

    return items[:max_items]


def fetch_source(source: dict, max_items: int, since_date: datetime) -> dict:
    """Fetch one source. Returns dict with items list."""
    result = {
        "id":       source.get("id", ""),
        "name":     source.get("name", ""),
        "url":      source.get("url", ""),
        "category": source.get("category", ""),
        "type":     source.get("type", ""),
        "items":    [],
        "error":    None,
    }

    rss_url = source.get("rss")
    web_url = source.get("url", "")

    if rss_url:
        print(f"    RSS  {source['name'][:40]:<40}", end="", flush=True)
        xml = fetch_url(rss_url)
        if xml:
            items = parse_rss(xml, max_items, since_date)
            result["items"] = items
            print(f"  → {len(items)} items")
        else:
            result["error"] = f"Failed to fetch RSS: {rss_url}"
            print("  → failed")
    elif web_url:
        print(f"    Web  {source['name'][:40]:<40}", end="", flush=True)
        html = fetch_url(web_url)
        if html:
            extractor = HTMLTextExtractor()
            extractor.feed(html)
            text = extractor.get_text()[:2000]
            result["items"] = [{"title": source["name"], "url": web_url, "summary": text, "published": ""}]
            print("  → 1 item (web page)")
        else:
            result["error"] = f"Failed to fetch: {web_url}"
            print("  → failed")

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch AI source content for weekly digest")
    parser.add_argument("--date",       default="",  help="Target date YYYY-MM-DD (default: today)")
    parser.add_argument("--categories", default="",  help="Comma-separated category filter")
    parser.add_argument("--output",     default="",  help="Output JSON path")
    parser.add_argument("--max-items",  type=int, default=5, help="Max items per source")
    args = parser.parse_args()

    sources_data = load_sources()
    sources      = sources_data.get("sources", [])

    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.now(timezone.utc)
    since_date  = (target_date - timedelta(days=8)).replace(tzinfo=timezone.utc)
    date_str    = target_date.strftime("%Y-%m-%d")

    # Filter by categories
    filter_cats = [c.strip() for c in args.categories.split(",") if c.strip()] if args.categories else []
    if filter_cats:
        sources = [s for s in sources
                   if any(c in s.get("digest_categories", []) for c in filter_cats)]

    DATA_DIR = output_dir() / "ai-digest"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else DATA_DIR / f"fetched-{date_str}.json"

    print(f"\n  Fetching {len(sources)} sources for week of {date_str}...\n")

    results = []
    for source in sources:
        result = fetch_source(source, args.max_items, since_date)
        results.append(result)
        time.sleep(0.5)  # polite rate limiting

    output = {
        "fetched_at":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "week_date":   date_str,
        "since_date":  since_date.strftime("%Y-%m-%d"),
        "total_sources": len(results),
        "total_items":   sum(len(r["items"]) for r in results),
        "sources":       results,
    }

    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n  ✓ Fetched {output['total_items']} items from {output['total_sources']} sources.")
    print(f"  Saved: {output_path}\n")


if __name__ == "__main__":
    main()
