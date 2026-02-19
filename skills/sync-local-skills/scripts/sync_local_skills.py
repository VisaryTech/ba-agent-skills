#!/usr/bin/env python3
"""Install or update all skills from a local source directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def get_default_dest() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").is_file()


def sync_skills(source: Path, dest: Path, dry_run: bool) -> tuple[int, int, int]:
    installed = 0
    updated = 0
    skipped = 0

    if not source.exists() or not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")

    skills = sorted(p for p in source.iterdir() if is_skill_dir(p))
    if not skills:
        print(f"No skills found in source: {source}")
        return installed, updated, skipped

    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        target = dest / skill.name
        if target.exists():
            action = "update"
            updated += 1
        else:
            action = "install"
            installed += 1

        print(f"{action}: {skill.name}")
        if dry_run:
            continue

        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill, target)

    return installed, updated, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install or update all local Codex skills from a directory."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.cwd() / "skills",
        help="Source directory with local skills (default: ./skills).",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=get_default_dest(),
        help="Destination skills directory (default: $CODEX_HOME/skills or ~/.codex/skills).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without copying files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        installed, updated, skipped = sync_skills(
            source=args.source.resolve(),
            dest=args.dest.expanduser().resolve(),
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(
        f"done: installed={installed}, updated={updated}, skipped={skipped}, dry_run={args.dry_run}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
