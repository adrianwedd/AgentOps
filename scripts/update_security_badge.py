#!/usr/bin/env python3
"""Update security badge in README from bandit.json."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from agentic_index_cli.helpers.markdown import render_badge

BADGE_RE = re.compile(
    r"!?\[security\]\(https://img\.shields\.io/badge/security-\d+%20issues-[a-zA-Z]+\)"
)


def fetch_badge(url: str, dest: Path) -> None:
    """Download an SVG badge or create a local placeholder when offline."""
    if os.getenv("CI_OFFLINE") == "1":
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        return
    try:
        import urllib.request

        resp = urllib.request.urlopen(url)
        try:
            content = resp.read().rstrip(b"\n")
            dest.write_bytes(content)
        finally:
            if hasattr(resp, "close"):
                resp.close()
    except Exception:
        if dest.exists():
            return
        dest.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"></svg>')


def _issue_count(path: Path) -> int:
    data = json.loads(path.read_text())
    return len(data.get("results", []))


def _badge_url(count: int) -> str:
    if count == 0:
        color = "brightgreen"
    elif count <= 5:
        color = "yellow"
    else:
        color = "red"
    return f"https://img.shields.io/badge/security-{count}%20issues-{color}"


def build_readme(readme_path: Path, count: int) -> str:
    text = readme_path.read_text(encoding="utf-8")
    url = _badge_url(count)
    new_text = BADGE_RE.sub(render_badge("security", url), text)
    return new_text


def main(
    readme: str = "README.md",
    report: str = "bandit.json",
    *,
    check: bool = False,
    write: bool = True,
) -> int:
    readme_path = Path(readme)
    report_path = Path(report)
    count = _issue_count(report_path)
    new_text = build_readme(readme_path, count)
    if check:
        if new_text != readme_path.read_text(encoding="utf-8"):
            print("Security badge out of date", file=sys.stderr)
            return 1
        return 0
    if write and new_text != readme_path.read_text(encoding="utf-8"):
        readme_path.write_text(new_text, encoding="utf-8")
        fetch_badge(_badge_url(count), Path("badges") / "security.svg")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update security badge in README")
    parser.add_argument("--check", action="store_true", help="Fail if badge stale")
    parser.add_argument("--write", action="store_true", help="Write README")
    parser.add_argument("report", nargs="?", default="bandit.json")
    parser.add_argument("readme", nargs="?", default="README.md")
    args = parser.parse_args()
    if not args.write:
        args.write = not args.check
    sys.exit(main(args.readme, args.report, check=args.check, write=args.write))
