#!/usr/bin/env python3
"""
AI Digest automation runner.

Invokes the /ai-digest skill via the assistant CLI and optionally
opens the result in a browser. Use this for scheduling or manual one-click runs.

Usage:
    python run_digest.py [--date YYYY-MM-DD] [--open] [--schedule]

Options:
    --date YYYY-MM-DD   Override the digest date (default: next Monday)
    --open              Open the HTML output in the default browser after generation
    --schedule          Print instructions for scheduling this script (cron / Task Scheduler)

Scheduling examples (printed with --schedule):
    Cron (Linux/macOS): 0 7 * * 1  cd /path/to/repo && python .agents/scripts/ai-digest/run_digest.py --open
    Windows Task Scheduler: run this script every Monday at 07:00
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import output_dir  # noqa: E402

SCRIPT_DIR  = Path(__file__).parent
REPO_ROOT   = Path(__file__).resolve().parents[3]


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip()
    return env


def next_monday(ref: datetime = None) -> datetime:
    """Return the date of the next (or current) Monday."""
    d = ref or datetime.now()
    days_ahead = (7 - d.weekday()) % 7  # Monday = 0
    return d + timedelta(days=days_ahead) if days_ahead else d


def print_schedule_instructions(date_str: str) -> None:
    script_abs = SCRIPT_DIR / "run_digest.py"
    print(f"""
  ── Scheduling Instructions ──────────────────────────────────

  Linux / macOS (cron):
    Edit crontab with: crontab -e
    Add this line (runs every Monday at 07:00):

      0 7 * * 1  cd "{REPO_ROOT}" && python "{script_abs}" --open

  Windows Task Scheduler:
    1. Open Task Scheduler → Create Task
    2. Trigger: Weekly → Monday → {date_str[:5]}07:00
    3. Action: Start program
         Program: python
         Arguments: "{script_abs}" --open
         Start in: "{REPO_ROOT}"
    4. Save with a meaningful name like "AI Weekly Digest"

  Manual run:
    python "{script_abs}" --date {date_str} --open

  ─────────────────────────────────────────────────────────────
""")


def main():
    parser = argparse.ArgumentParser(description="Run /ai-digest via the assistant CLI")
    parser.add_argument("--date",     default="",  help="Digest date YYYY-MM-DD (default: next Monday)")
    parser.add_argument("--open",     action="store_true", help="Open HTML output in browser")
    parser.add_argument("--schedule", action="store_true", help="Print scheduling instructions")
    args = parser.parse_args()

    # Resolve date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"✗ Invalid date format: {args.date} (expected YYYY-MM-DD)", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = next_monday()

    date_str = target_date.strftime("%Y-%m-%d")

    if args.schedule:
        print_schedule_instructions(date_str)
        sys.exit(0)

    digest_dir = output_dir() / "ai-digest"
    expected   = digest_dir / f"digest-{date_str}.html"

    print(f"\n╔══════════════════════════════════════════════╗")
    print(f"║       🧠  AI WEEKLY DIGEST GENERATOR        ║")
    print(f"╚══════════════════════════════════════════════╝\n")
    print(f"  Date     : {date_str}")
    print(f"  Output   : {expected}\n")

    # Check claude CLI
    claude_bin = "claude"
    result = subprocess.run(["where" if sys.platform == "win32" else "which", claude_bin],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("✗ 'claude' command not found.", file=sys.stderr)
        print("  Install Claude Code: https://claude.ai/code", file=sys.stderr)
        sys.exit(1)

    # Run the skill
    print(f"  Running /ai-digest {date_str} ...\n")
    run_result = subprocess.run(
        [claude_bin, "--print", f"/ai-digest {date_str}"],
        cwd=str(REPO_ROOT),
    )

    print()
    if run_result.returncode != 0:
        print(f"  ⚠  claude exited with code {run_result.returncode}", file=sys.stderr)

    if expected.exists():
        size_kb = round(expected.stat().st_size / 1024, 1)
        print(f"  ✓ Digest generated: {expected}  ({size_kb} KB)")
        if args.open:
            print("  Opening in browser...")
            webbrowser.open(expected.as_uri())
    else:
        print(f"  ⚠  Expected file not found: {expected}")
        print(f"     Check the assistant output above for the actual filename.")
        print(f"     All digests: {digest_dir}")

    print()


if __name__ == "__main__":
    main()
