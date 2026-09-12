#!/usr/bin/env python3
"""
Profile completeness checker for the Digital Me skill.

Reads the `profile` section of the assistant config (resolved via ASSISTANT_CONFIG,
default ~/.assistant/config.json) and reports which fields are incomplete.

Usage:
    python profile_check.py [--json]

Options:
    --json    Output raw JSON instead of human-readable text
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import load_config, config_path  # noqa: E402

# ── Fields considered important for profile completeness ─────────────────────
REQUIRED_FIELDS = [
    ("name",                    "Your full name"),
    ("title",                   "Current job title"),
    ("company",                 "Current company"),
    ("email",                   "Contact email"),
    ("linkedin",                "LinkedIn profile URL"),
    ("headline",                "LinkedIn-style headline"),
    ("tagline",                 "One-line personal tagline"),
    ("bio.short",               "2-3 sentence short bio"),
    ("content_pillars",         "3-5 topics you post about (list)"),
    ("keywords",                "Searchable keywords (list)"),
    ("writing_style.tone",      "Tone descriptors (list): direct, warm, etc."),
    ("writing_style.sentence_structure", "Sentence rhythm preference"),
]

OPTIONAL_FIELDS = [
    ("website",                 "Personal website URL"),
    ("photo",                   "Profile photo path"),
    ("bio.long",                "150-200 word long bio"),
    ("writing_style.vocabulary_prefer", "Words / phrases to prefer"),
    ("writing_style.vocabulary_avoid",  "Words / phrases to avoid"),
]


def get_nested(data: dict, dotted_key: str):
    """Access a nested dict value using dot notation."""
    keys = dotted_key.split(".")
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def is_empty(value) -> bool:
    """Return True if value is considered empty/unfilled."""
    if value is None:
        return True
    if isinstance(value, str) and (not value.strip() or value.startswith("{{") or value == ""):
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


def check_profile(profile: dict) -> dict:
    """Return completeness report as a dict."""
    missing_required = []
    missing_optional = []

    for field, label in REQUIRED_FIELDS:
        value = get_nested(profile, field)
        if is_empty(value):
            missing_required.append({"field": field, "label": label})

    for field, label in OPTIONAL_FIELDS:
        value = get_nested(profile, field)
        if is_empty(value):
            missing_optional.append({"field": field, "label": label})

    total_required = len(REQUIRED_FIELDS)
    total_optional = len(OPTIONAL_FIELDS)
    filled_required = total_required - len(missing_required)
    filled_optional = total_optional - len(missing_optional)

    return {
        "filled_required": filled_required,
        "total_required":  total_required,
        "filled_optional": filled_optional,
        "total_optional":  total_optional,
        "score":           round(filled_required / total_required * 100),
        "missing_required": missing_required,
        "missing_optional": missing_optional,
    }


def print_report(report: dict, profile: dict) -> None:
    name = get_nested(profile, "name") or "Unknown"
    print(f"\n{'─' * 55}")
    print(f"  Profile Completeness — {name}")
    print(f"{'─' * 55}")
    print(f"  Required fields:  {report['filled_required']} / {report['total_required']}  ({report['score']}%)")
    print(f"  Optional fields:  {report['filled_optional']} / {report['total_optional']}")

    if report["missing_required"]:
        print(f"\n  ✗ Missing required fields ({len(report['missing_required'])}):")
        for item in report["missing_required"]:
            print(f"      {item['field']}")
            print(f"          → {item['label']}")

    if report["missing_optional"]:
        print(f"\n  ○ Missing optional fields ({len(report['missing_optional'])}):")
        for item in report["missing_optional"]:
            print(f"      {item['field']}")

    if not report["missing_required"] and not report["missing_optional"]:
        print("\n  ✓ Profile is fully complete!")

    print(f"{'─' * 55}\n")


def main():
    parser = argparse.ArgumentParser(description="Check the config profile completeness")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    try:
        cfg = load_config()
    except FileNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {config_path()}: {e}", file=sys.stderr)
        sys.exit(1)

    profile = cfg.get("profile", {})
    report = check_profile(profile)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report, profile)

    # Exit code: 0 = complete, 1 = missing required fields
    sys.exit(0 if not report["missing_required"] else 1)


if __name__ == "__main__":
    main()
