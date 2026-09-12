#!/usr/bin/env python3
"""
Newsletter skill — SQLite database operations.

Tables: subscribers, newsletters, events
Funnel stages: cold → warm → hot → engaged → converted → churned

Usage:
    python db.py --init                            Create/migrate schema
    python db.py --stats                           Show dashboard stats
    python db.py --subscribers                     List all subscribers
    python db.py --pipeline                        Funnel pipeline view
    python db.py --add-subscriber --email X [--name Y] [--tags t1,t2] [--source S]
    python db.py --remove-subscriber --email X
    python db.py --import                          Import from email-list.json
    python db.py --export                          Export to email-list.json
    python db.py --register --slug S --subject SUB --date D
    python db.py --log-event --slug S --email E --type T [--meta JSON]
    python db.py --recalc-funnel                   Recalculate all funnel stages
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import load_config, output_dir  # noqa: E402

OUTPUT_DIR     = output_dir() / "newsletter"
DB_PATH        = OUTPUT_DIR / "newsletter.db"
EMAIL_LIST     = OUTPUT_DIR / "subscribers.json"

# Funnel stage order
FUNNEL_STAGES  = ["cold", "warm", "hot", "engaged", "converted", "churned"]
FUNNEL_COLORS  = {
    "cold":      "#64748b",
    "warm":      "#f59e0b",
    "hot":       "#ef4444",
    "engaged":   "#22c55e",
    "converted": "#6366f1",
    "churned":   "#475569",
}


# ── Schema ────────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS subscribers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           TEXT    UNIQUE NOT NULL,
    name            TEXT    DEFAULT '',
    tags            TEXT    DEFAULT '[]',
    source          TEXT    DEFAULT '',
    funnel_stage    TEXT    DEFAULT 'cold',
    subscribed_at   TEXT    NOT NULL,
    unsubscribed_at TEXT,
    is_active       INTEGER DEFAULT 1,
    open_count      INTEGER DEFAULT 0,
    click_count     INTEGER DEFAULT 0,
    bounce_count    INTEGER DEFAULT 0,
    last_opened_at  TEXT,
    last_clicked_at TEXT
);

CREATE TABLE IF NOT EXISTS newsletters (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    slug             TEXT    UNIQUE NOT NULL,
    subject          TEXT    DEFAULT '',
    date             TEXT    NOT NULL,
    html_path        TEXT    DEFAULT '',
    ftp_url          TEXT    DEFAULT '',
    recipient_count  INTEGER DEFAULT 0,
    sent_at          TEXT,
    status           TEXT    DEFAULT 'draft'
);

CREATE TABLE IF NOT EXISTS events (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    newsletter_slug  TEXT    NOT NULL,
    subscriber_email TEXT    NOT NULL,
    event_type       TEXT    NOT NULL,
    metadata         TEXT    DEFAULT '{}',
    occurred_at      TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_slug    ON events(newsletter_slug);
CREATE INDEX IF NOT EXISTS idx_events_email   ON events(subscriber_email);
CREATE INDEX IF NOT EXISTS idx_events_type    ON events(event_type);
"""


def get_conn() -> sqlite3.Connection:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
    print(f"  ✓ Database ready: {DB_PATH}")


# ── Subscriber CRUD ───────────────────────────────────────────────────────────

def add_subscriber(email: str, name: str = "", tags: list = None,
                   source: str = "", skip_if_exists: bool = False) -> bool:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tags_json = json.dumps(tags or [])
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id, is_active FROM subscribers WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            if skip_if_exists:
                return False
            # Reactivate if was churned
            conn.execute(
                "UPDATE subscribers SET is_active=1, unsubscribed_at=NULL, "
                "funnel_stage='cold', name=COALESCE(NULLIF(?,''),(SELECT name FROM subscribers WHERE email=?)) "
                "WHERE email=?",
                (name, email, email),
            )
            return True
        conn.execute(
            "INSERT INTO subscribers (email, name, tags, source, subscribed_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (email.lower().strip(), name, tags_json, source, now),
        )
        return True


def remove_subscriber(email: str):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute(
            "UPDATE subscribers SET is_active=0, unsubscribed_at=?, funnel_stage='churned' "
            "WHERE email=?",
            (now, email.lower().strip()),
        )
    log_event("system", email, "unsubscribed", {"reason": "manual_removal"})


def list_subscribers(active_only: bool = False) -> list:
    with get_conn() as conn:
        q = "SELECT * FROM subscribers"
        if active_only:
            q += " WHERE is_active=1"
        q += " ORDER BY funnel_stage, open_count DESC"
        return [dict(r) for r in conn.execute(q).fetchall()]


# ── Newsletter CRUD ───────────────────────────────────────────────────────────

def register_newsletter(slug: str, subject: str, date: str, html_path: str = ""):
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM newsletters WHERE slug=?", (slug,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE newsletters SET subject=?, date=?, html_path=? WHERE slug=?",
                (subject, date, html_path, slug),
            )
        else:
            conn.execute(
                "INSERT INTO newsletters (slug, subject, date, html_path) VALUES (?, ?, ?, ?)",
                (slug, subject, date, html_path),
            )


def update_newsletter_sent(slug: str, recipient_count: int, ftp_url: str = ""):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute(
            "UPDATE newsletters SET status='sent', sent_at=?, recipient_count=?, ftp_url=? "
            "WHERE slug=?",
            (now, recipient_count, ftp_url, slug),
        )


def update_newsletter_ftp(slug: str, ftp_url: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE newsletters SET ftp_url=? WHERE slug=?", (ftp_url, slug)
        )


def get_newsletter(slug: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM newsletters WHERE slug=?", (slug,)
        ).fetchone()
        return dict(row) if row else None


# ── Event Logging ─────────────────────────────────────────────────────────────

def log_event(newsletter_slug: str, subscriber_email: str,
              event_type: str, metadata: dict = None):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    meta_json = json.dumps(metadata or {})
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO events (newsletter_slug, subscriber_email, event_type, metadata, occurred_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (newsletter_slug, subscriber_email.lower().strip(), event_type, meta_json, now),
        )
        # Update subscriber counters
        if event_type == "opened":
            conn.execute(
                "UPDATE subscribers SET open_count=open_count+1, last_opened_at=? WHERE email=?",
                (now, subscriber_email.lower().strip()),
            )
        elif event_type == "clicked":
            conn.execute(
                "UPDATE subscribers SET click_count=click_count+1, last_clicked_at=? WHERE email=?",
                (now, subscriber_email.lower().strip()),
            )
        elif event_type == "bounced":
            conn.execute(
                "UPDATE subscribers SET bounce_count=bounce_count+1 WHERE email=?",
                (subscriber_email.lower().strip(),),
            )


# ── Funnel Recalculation ──────────────────────────────────────────────────────

def recalc_funnel():
    """Recompute funnel_stage for every active subscriber."""
    with get_conn() as conn:
        # Total newsletters sent
        total_sent = conn.execute(
            "SELECT COUNT(*) FROM newsletters WHERE status='sent'"
        ).fetchone()[0]

        subs = conn.execute(
            "SELECT email, open_count, click_count, bounce_count, is_active FROM subscribers"
        ).fetchall()

        cta_url = None
        try:
            cta_url = (load_config().get("newsletter", {}) or {}).get("settings", {}).get("cta_url")
        except Exception:
            pass

        for sub in subs:
            email       = sub["email"]
            opens       = sub["open_count"]
            clicks      = sub["click_count"]
            bounces     = sub["bounce_count"]
            is_active   = sub["is_active"]

            if not is_active or bounces >= 2:
                stage = "churned"
            elif cta_url and conn.execute(
                "SELECT 1 FROM events WHERE subscriber_email=? AND event_type='clicked' "
                "AND json_extract(metadata,'$.url') LIKE ?",
                (email, f"%{cta_url}%"),
            ).fetchone():
                stage = "converted"
            elif total_sent > 0 and (opens / max(total_sent, 1)) > 0.5:
                stage = "engaged"
            elif opens >= 3 or clicks >= 1:
                stage = "hot"
            elif opens >= 1:
                stage = "warm"
            else:
                stage = "cold"

            conn.execute(
                "UPDATE subscribers SET funnel_stage=? WHERE email=?", (stage, email)
            )


# ── Import / Export ───────────────────────────────────────────────────────────

def import_from_json():
    # Seed subscribers come from config.newsletter.subscribers; fall back to an exported file.
    subscribers = []
    try:
        subscribers = (load_config().get("newsletter", {}) or {}).get("subscribers", [])
    except Exception:
        subscribers = []
    if not subscribers and EMAIL_LIST.exists():
        subscribers = json.loads(EMAIL_LIST.read_text(encoding="utf-8")).get("subscribers", [])
    if not subscribers:
        print("  ERROR: no subscribers in config.newsletter.subscribers")
        return 0
    added = skipped = 0
    for sub in subscribers:
        email = sub.get("email", "").strip()
        if not email:
            continue
        ok = add_subscriber(
            email=email,
            name=sub.get("name", ""),
            tags=sub.get("tags", []),
            source=sub.get("source", "import"),
            skip_if_exists=True,
        )
        if ok:
            added += 1
        else:
            skipped += 1
    print(f"  Imported: {added} new, {skipped} already existed")
    return added


def export_to_json():
    subs = list_subscribers()
    export = {"subscribers": []}
    for s in subs:
        if s.get("is_active"):
            export["subscribers"].append({
                "email":  s["email"],
                "name":   s.get("name", ""),
                "tags":   json.loads(s.get("tags", "[]")),
                "source": s.get("source", ""),
            })
    EMAIL_LIST.write_text(
        json.dumps(export, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  Exported {len(export['subscribers'])} subscribers to {EMAIL_LIST}")


# ── Display Helpers ───────────────────────────────────────────────────────────

def print_stats():
    with get_conn() as conn:
        total        = conn.execute("SELECT COUNT(*) FROM subscribers").fetchone()[0]
        active       = conn.execute("SELECT COUNT(*) FROM subscribers WHERE is_active=1").fetchone()[0]
        newsletters  = conn.execute("SELECT COUNT(*) FROM newsletters WHERE status='sent'").fetchone()[0]
        recent = conn.execute(
            "SELECT slug, subject, sent_at, recipient_count FROM newsletters "
            "ORDER BY sent_at DESC LIMIT 5"
        ).fetchall()

    print(f"\n  Newsletter Skill — Dashboard")
    print("  " + "─" * 50)
    print(f"  Subscribers : {active} active / {total} total")
    print(f"  Sent        : {newsletters} newsletter(s)")

    if recent:
        print(f"\n  Recent newsletters:")
        for r in recent:
            sent = (r["sent_at"] or "draft")[:10]
            print(f"    {sent}  {r['slug']:<20}  {r['recipient_count']} recipients")
    print()


def print_subscribers():
    subs = list_subscribers()
    if not subs:
        print("\n  No subscribers yet. Add with --add-subscriber or --import\n")
        return
    print(f"\n  Subscribers ({len(subs)} total):")
    print(f"  {'Email':<35} {'Name':<18} {'Stage':<12} {'Opens':>6} {'Clicks':>7}  Active")
    print("  " + "─" * 88)
    for s in subs:
        tags = json.loads(s.get("tags", "[]"))
        active = "✓" if s["is_active"] else "—"
        print(
            f"  {s['email']:<35} {(s.get('name') or ''):<18} "
            f"{s.get('funnel_stage','cold'):<12} {s['open_count']:>6} "
            f"{s['click_count']:>7}  {active}"
        )
    print()


def print_pipeline():
    recalc_funnel()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT funnel_stage, COUNT(*) as cnt, "
            "AVG(CAST(open_count AS REAL)) as avg_opens, "
            "MAX(last_opened_at) as last_open "
            "FROM subscribers GROUP BY funnel_stage"
        ).fetchall()

    stage_data = {s: {"count": 0, "avg_opens": 0.0, "last_open": "—"} for s in FUNNEL_STAGES}
    for r in rows:
        stage = r["funnel_stage"] or "cold"
        if stage in stage_data:
            stage_data[stage] = {
                "count":     r["cnt"],
                "avg_opens": round(r["avg_opens"] or 0, 1),
                "last_open": (r["last_open"] or "—")[:10],
            }

    print(f"\n  Funnel Pipeline")
    print("  " + "─" * 56)
    print(f"  {'Stage':<14} {'Count':>6}  {'Avg Opens':>10}  {'Last Activity'}")
    print("  " + "─" * 56)
    for stage in FUNNEL_STAGES:
        d = stage_data[stage]
        avg = f"{d['avg_opens']:.1f}" if d["count"] > 0 else "—"
        print(f"  {stage:<14} {d['count']:>6}  {avg:>10}  {d['last_open']}")
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Newsletter SQLite database")
    parser.add_argument("--init",             action="store_true")
    parser.add_argument("--stats",            action="store_true")
    parser.add_argument("--subscribers",      action="store_true")
    parser.add_argument("--pipeline",         action="store_true")
    parser.add_argument("--add-subscriber",   action="store_true")
    parser.add_argument("--remove-subscriber",action="store_true")
    parser.add_argument("--import",           action="store_true", dest="do_import")
    parser.add_argument("--export",           action="store_true", dest="do_export")
    parser.add_argument("--register",         action="store_true")
    parser.add_argument("--log-event",        action="store_true")
    parser.add_argument("--recalc-funnel",    action="store_true")
    parser.add_argument("--email",   default="")
    parser.add_argument("--name",    default="")
    parser.add_argument("--tags",    default="")
    parser.add_argument("--source",  default="")
    parser.add_argument("--slug",    default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--date",    default="")
    parser.add_argument("--html-path", default="")
    parser.add_argument("--type",    default="")
    parser.add_argument("--meta",    default="{}")
    args = parser.parse_args()

    init_db()

    if args.init:
        pass  # already done above
    elif args.stats:
        print_stats()
    elif args.subscribers:
        print_subscribers()
    elif args.pipeline:
        print_pipeline()
    elif args.add_subscriber:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        ok = add_subscriber(args.email, args.name, tags, args.source)
        print(f"  {'✓' if ok else '!'} Subscriber {args.email} {'added' if ok else 'already exists'}")
    elif args.remove_subscriber:
        remove_subscriber(args.email)
        print(f"  ✓ Unsubscribed: {args.email}")
    elif args.do_import:
        import_from_json()
    elif args.do_export:
        export_to_json()
    elif args.register:
        register_newsletter(args.slug, args.subject, args.date, args.html_path)
        print(f"  ✓ Newsletter registered: {args.slug}")
    elif args.log_event:
        try:
            meta = json.loads(args.meta)
        except json.JSONDecodeError:
            meta = {}
        log_event(args.slug, args.email, args.type, meta)
        print(f"  ✓ Event logged: {args.type} for {args.email}")
    elif args.recalc_funnel:
        recalc_funnel()
        print("  ✓ Funnel stages recalculated")
    else:
        parser.print_help()
