#!/usr/bin/env python3
"""
Shared profile-memory and notes helper.

Maintains two markdown files in the shared config location (next to config.json by
default, overridable via config.paths.memory / config.paths.notes):

- memory.md  — durable facts about you (profile updates, preferences, learned context)
- notes.md   — running task/session notes

Any skill can record to these so your profile keeps improving over time.

Usage:
    python memory.py remember "Prefers short, punchy LinkedIn hooks"      # -> memory.md
    python memory.py note     "Drafted Q1 launch post; awaiting metrics"  # -> notes.md
    python memory.py show     [memory|notes]                              # print a file
    python memory.py path     [memory|notes]                             # print resolved path
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assistant_config import memory_path, notes_path, append_entry  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Record or show profile memory / notes")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_rem = sub.add_parser("remember", help="Append a durable profile fact to memory.md")
    p_rem.add_argument("text")
    p_rem.add_argument("--heading", default=None, help="Optional section heading")

    p_note = sub.add_parser("note", help="Append a running note to notes.md")
    p_note.add_argument("text")
    p_note.add_argument("--heading", default=None)

    p_show = sub.add_parser("show", help="Print a file")
    p_show.add_argument("which", choices=["memory", "notes"], nargs="?", default="memory")

    p_path = sub.add_parser("path", help="Print the resolved file path")
    p_path.add_argument("which", choices=["memory", "notes"], nargs="?", default="memory")

    args = parser.parse_args()

    if args.cmd == "remember":
        print(append_entry(memory_path(), args.text, args.heading))
    elif args.cmd == "note":
        print(append_entry(notes_path(), args.text, args.heading))
    elif args.cmd in ("show", "path"):
        target = memory_path() if args.which == "memory" else notes_path()
        if args.cmd == "path":
            print(target)
        elif target.exists():
            print(target.read_text(encoding="utf-8"))
        else:
            print(f"(empty) {target}")


if __name__ == "__main__":
    main()
