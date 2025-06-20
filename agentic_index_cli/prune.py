"""Utilities for pruning stale repository data."""

import argparse
from datetime import datetime, timezone
from pathlib import Path

CHANGELOG = Path("CHANGELOG.md")
REPOS = Path("repos.json")


from .validate import load_repos as _load
from .validate import save_repos as _save


def load_repos(path: Path = REPOS):
    """Return repository data from ``path``."""
    return _load(path)


def save_repos(repos, path: Path = REPOS):
    """Write ``repos`` to ``path``."""
    _save(path, repos)


def append_changelog(entries, changelog: Path = CHANGELOG):
    """Append changelog ``entries`` to ``changelog`` file."""
    if not entries:
        return
    if changelog.exists():
        existing = changelog.read_text().rstrip().splitlines()
    else:
        existing = []
    for entry in entries:
        existing.append(entry)
    changelog.write_text("\n".join(existing) + "\n")


def prune(inactive_days, repos_path: Path = REPOS, changelog_path: Path = CHANGELOG):
    """Remove repos inactive for ``inactive_days`` days."""
    repos = load_repos(repos_path)
    keep = []
    removed_entries = []
    today = datetime.now(timezone.utc)
    for repo in repos:
        pushed_at = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
        delta = today - pushed_at
        if delta.days > inactive_days:
            removed_entries.append(repo["full_name"])
        else:
            keep.append(repo)
    if removed_entries:
        save_repos(keep, repos_path)
        date = today.strftime("%Y-%m-%d")
        log_lines = [
            f"{date}  Removed {name} – inactive > {inactive_days} d"
            for name in removed_entries
        ]
        append_changelog(log_lines, changelog_path)
    return removed_entries


def main(argv=None):
    """CLI wrapper for :func:`prune`."""
    parser = argparse.ArgumentParser(description="Prune inactive repositories")
    parser.add_argument(
        "--inactive", type=int, required=True, help="Days since last push"
    )
    parser.add_argument("--repos-path", type=Path, default=REPOS)
    parser.add_argument("--changelog-path", type=Path, default=CHANGELOG)
    args = parser.parse_args(argv)
    removed = prune(
        args.inactive, repos_path=args.repos_path, changelog_path=args.changelog_path
    )
    if removed:
        print("\n".join(removed))


if __name__ == "__main__":
    main()
