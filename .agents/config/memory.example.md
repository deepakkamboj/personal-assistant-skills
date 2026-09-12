# Profile Memory

Durable facts the assistant has learned about you. Skills read this at the start of every
run and append new, confirmed facts here so your profile keeps improving over time. Keep
entries short and factual. Structured identity/brand data still lives in `config.json`;
this file captures the softer, evolving context.

Resolved from `config.paths.memory` (default `memory.md` next to `config.json`).
Copy this template to your real `memory.md` (gitignored).

## Preferences

- (e.g. Prefers short, punchy LinkedIn hooks; no hashtag walls)

## Voice & phrasing

- (e.g. Avoids "excited to announce", em dashes)

## Recurring context

- (e.g. Currently focused on AI agents + test automation)

## Learned facts

<!-- Skills append timestamped entries below via `python .agents/scripts/memory.py remember "..."` -->
