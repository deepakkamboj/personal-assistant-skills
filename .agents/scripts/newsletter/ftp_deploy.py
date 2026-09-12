#!/usr/bin/env python3
"""
FTP uploader for the newsletter skill.

Uploads newsletter HTML and tracker.php to example.com via FTP.
Uses Python stdlib ftplib — no external dependencies.

Usage:
  python scripts/ftp_deploy.py --slug 2026-02-27
  python scripts/ftp_deploy.py --slug 2026-02-27 --force-tracker  # re-upload tracker.php even if present
"""

import argparse
import ftplib
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assistant_config import output_dir  # noqa: E402

SCRIPT_DIR  = Path(__file__).resolve().parent
REPO_ROOT   = Path(__file__).resolve().parents[3]
OUTPUT_DIR  = output_dir() / "newsletter"
DB_SCRIPT   = SCRIPT_DIR / "db.py"
TRACKER_SRC = SCRIPT_DIR / "tracker.php"


# ── Environment ───────────────────────────────────────────────────────────────

def load_env():
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def require_env(key: str) -> str:
    val = os.environ.get(key, "").strip()
    if not val:
        print(f"ERROR: {key} not set in .env", file=sys.stderr)
        sys.exit(1)
    return val


# ── FTP helpers ───────────────────────────────────────────────────────────────

def ftp_connect(host: str, user: str, password: str) -> ftplib.FTP:
    ftp = ftplib.FTP()
    try:
        ftp.connect(host, 21, timeout=30)
        ftp.login(user, password)
        ftp.set_pasv(True)
        print(f"  Connected to FTP: {host}")
        return ftp
    except ftplib.all_errors as e:
        print(f"ERROR: FTP connection failed: {e}", file=sys.stderr)
        sys.exit(1)


def ftp_ensure_dirs(ftp: ftplib.FTP, remote_path: str):
    """Create remote directories if they don't exist."""
    parts = [p for p in remote_path.replace("\\", "/").split("/") if p]
    current = ""
    for part in parts:
        current += f"/{part}"
        try:
            ftp.cwd(current)
        except ftplib.error_perm:
            try:
                ftp.mkd(current)
                ftp.cwd(current)
                print(f"  Created remote dir: {current}")
            except ftplib.all_errors as e:
                print(f"  WARN: could not create {current}: {e}")


def ftp_file_exists(ftp: ftplib.FTP, remote_path: str, filename: str) -> bool:
    """Check if a file exists in the given remote path."""
    try:
        ftp.cwd(remote_path)
        files = ftp.nlst()
        return filename in files
    except ftplib.all_errors:
        return False


def ftp_upload(ftp: ftplib.FTP, local_path: Path, remote_dir: str, remote_name: str):
    """Upload a local file to the remote FTP directory."""
    try:
        ftp.cwd(remote_dir)
    except ftplib.all_errors as e:
        print(f"ERROR: cannot cd to {remote_dir}: {e}", file=sys.stderr)
        sys.exit(1)

    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_name}", f)
    print(f"  Uploaded: {remote_name} → {remote_dir}/{remote_name}")


# ── DB update ─────────────────────────────────────────────────────────────────

def update_ftp_url(slug: str, ftp_url: str):
    subprocess.run(
        [sys.executable, str(DB_SCRIPT),
         "--register", "--slug", slug, "--ftp-url", ftp_url],
        check=False
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deploy newsletter to FTP")
    parser.add_argument("--slug",          required=True, help="Newsletter date slug")
    parser.add_argument("--force-tracker", action="store_true",
                        help="Re-upload tracker.php even if already on server")
    args = parser.parse_args()

    load_env()

    host         = require_env("FTP_HOST")
    user         = require_env("FTP_USER")
    password     = require_env("FTP_PASSWORD")
    remote_path  = os.environ.get("FTP_NEWSLETTER_PATH", "public_html/newsletters/").rstrip("/")
    base_url     = os.environ.get("NEWSLETTER_BASE_URL", f"https://{host}/newsletters").rstrip("/")

    # Local files
    html_filename    = f"newsletter-{args.slug}.html"
    html_local       = OUTPUT_DIR / html_filename
    tracker_local    = TRACKER_SRC

    if not html_local.exists():
        print(f"ERROR: Newsletter HTML not found: {html_local}", file=sys.stderr)
        print(f"  Run: /newsletter create {args.slug}")
        sys.exit(1)

    if not tracker_local.exists():
        print(f"ERROR: tracker.php not found: {tracker_local}", file=sys.stderr)
        sys.exit(1)

    print(f"\nDeploying newsletter-{args.slug} to FTP...")
    print(f"  Host:        {host}")
    print(f"  Remote path: {remote_path}")

    ftp = ftp_connect(host, user, password)

    try:
        # Ensure remote directory exists
        ftp_ensure_dirs(ftp, remote_path)

        # Upload newsletter HTML
        ftp_upload(ftp, html_local, remote_path, html_filename)

        # Upload tracker.php (only if not already present, unless --force-tracker)
        tracker_present = ftp_file_exists(ftp, remote_path, "track.php")
        if tracker_present and not args.force_tracker:
            print("  tracker.php already on server (skipping). Use --force-tracker to re-upload.")
        else:
            ftp_upload(ftp, tracker_local, remote_path, "track.php")

    finally:
        ftp.quit()

    # Build public URL
    web_url = f"{base_url}/{html_filename}"
    print(f"\nDeployment complete.")
    print(f"  Web URL: {web_url}")

    # Update SQLite
    update_ftp_url(args.slug, web_url)
    print(f"  SQLite updated: ftp_url={web_url}")


if __name__ == "__main__":
    main()
