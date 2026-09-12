#!/usr/bin/env python3
"""Shared configuration resolver for assistant skill scripts.

Loads the single JSON config from the ``ASSISTANT_CONFIG`` environment variable,
falling back to ``~/.assistant/config.json``. There is no ``data/`` folder.

Usage from a skill script (``.agents/skills/<skill>/scripts/foo.py``)::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    from assistant_config import load_config, content_path, output_dir

    cfg = load_config()
"""

from __future__ import annotations

import json
import os
from pathlib import Path

ENV_VAR = "ASSISTANT_CONFIG"
DEFAULT_CONFIG = Path.home() / ".assistant" / "config.json"


def config_path() -> Path:
    """Resolve the active config path (env var, then default)."""
    env = os.environ.get(ENV_VAR)
    return Path(env).expanduser() if env else DEFAULT_CONFIG


def load_config() -> dict:
    """Load and parse the config JSON. Raises FileNotFoundError with guidance."""
    path = config_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Config not found at {path}. Set the {ENV_VAR} environment variable, or copy "
            f".agents/config/config.example.json to {DEFAULT_CONFIG}."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _load_config_safe() -> dict:
    try:
        return load_config()
    except (FileNotFoundError, ValueError):
        return {}


def content_path(cfg: dict | None = None) -> Path:
    """Resolve the companion prose file (config.paths.content, default sibling content.md)."""
    cfg = cfg if cfg is not None else _load_config_safe()
    rel = (cfg.get("paths") or {}).get("content", "content.md")
    base = config_path().parent
    p = Path(rel).expanduser()
    return p if p.is_absolute() else (base / p)


def output_dir(cfg: dict | None = None) -> Path:
    """Resolve the output directory (config.paths.output_dir, default sibling ./output)."""
    cfg = cfg if cfg is not None else _load_config_safe()
    rel = (cfg.get("paths") or {}).get("output_dir", "./output")
    base = config_path().parent
    p = Path(rel).expanduser()
    return p if p.is_absolute() else (base / p)


def _resolve_path(rel: str) -> Path:
    base = config_path().parent
    p = Path(rel).expanduser()
    return p if p.is_absolute() else (base / p)


def memory_path(cfg: dict | None = None) -> Path:
    """Resolve the persistent profile-memory file (config.paths.memory, default sibling memory.md)."""
    cfg = cfg if cfg is not None else _load_config_safe()
    return _resolve_path((cfg.get("paths") or {}).get("memory", "memory.md"))


def notes_path(cfg: dict | None = None) -> Path:
    """Resolve the running notes file (config.paths.notes, default sibling notes.md)."""
    cfg = cfg if cfg is not None else _load_config_safe()
    return _resolve_path((cfg.get("paths") or {}).get("notes", "notes.md"))


def append_entry(path: Path, text: str, heading: str | None = None) -> Path:
    """Append a timestamped entry to a shared markdown file, creating it if needed."""
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    path.parent.mkdir(parents=True, exist_ok=True)
    block = f"\n### {heading} — {ts}\n\n{text.strip()}\n" if heading else f"\n- {ts}: {text.strip()}\n"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(block)
    return path

