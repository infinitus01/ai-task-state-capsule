#!/usr/bin/env python3
"""Verify a task state capsule directory for internal consistency."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from pack_common import project_root

REQUIRED_FILES = [
    "TASK_STATUS_REPORT.md",
    "DECISION_LOG.md",
    "BRANCH_INFO.md",
    "RESUME_INSTRUCTIONS.md",
    "RECOVERY_CHECK.md",
    "STATE_MANIFEST.json",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_report_hash(text: str) -> str | None:
    match = re.search(r"^Version Hash:\s*(\S+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def extract_resume_hash(text: str) -> str | None:
    match = re.search(r"Resume this task from version\s+(\S+)\.", text)
    return match.group(1) if match else None


def git_tag_exists(tag: str, repo: Path) -> bool:
    result = subprocess.run(
        ["git", "tag", "-l", tag],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    return tag.strip() in {line.strip() for line in result.stdout.splitlines() if line.strip()}


def verify_capsule(capsule_dir: Path, check_git_tag: bool, repo: Path) -> list[str]:
    errors: list[str] = []

    for name in REQUIRED_FILES:
        if not (capsule_dir / name).is_file():
            errors.append(f"MISSING: {name}")

    if errors:
        return errors

    manifest = json.loads(read_text(capsule_dir / "STATE_MANIFEST.json"))
    manifest_hash = manifest.get("version_hash", "").strip()
    if not manifest_hash:
        errors.append("STATE_MANIFEST.json: version_hash is empty")

    report_hash = extract_report_hash(read_text(capsule_dir / "TASK_STATUS_REPORT.md"))
    if not report_hash:
        errors.append("TASK_STATUS_REPORT.md: Version Hash line not found")
    elif manifest_hash and report_hash != manifest_hash:
        errors.append(
            f"HASH_MISMATCH: manifest={manifest_hash} report={report_hash}"
        )

    resume_hash = extract_resume_hash(read_text(capsule_dir / "RESUME_INSTRUCTIONS.md"))
    if not resume_hash:
        errors.append("RESUME_INSTRUCTIONS.md: closing resume line not found")
    elif manifest_hash and resume_hash != manifest_hash:
        errors.append(
            f"HASH_MISMATCH: manifest={manifest_hash} resume={resume_hash}"
        )

    report_resume = extract_resume_hash(read_text(capsule_dir / "TASK_STATUS_REPORT.md"))
    if report_resume and manifest_hash and report_resume != manifest_hash:
        errors.append(
            f"HASH_MISMATCH: manifest={manifest_hash} report_section6={report_resume}"
        )

    if check_git_tag and manifest_hash:
        tag = f"capsule/{manifest_hash}"
        if not git_tag_exists(tag, repo):
            errors.append(f"GIT_TAG_MISSING: {tag}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify capsule internal consistency")
    parser.add_argument(
        "--capsule-dir",
        type=Path,
        default=project_root() / ".capsule",
        help="Path to capsule directory (default: .capsule/)",
    )
    parser.add_argument(
        "--check-git-tag",
        action="store_true",
        help="Require git tag capsule/<version_hash> to exist",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=project_root(),
        help="Git repository root",
    )
    args = parser.parse_args()

    capsule_dir = args.capsule_dir.resolve()
    if not capsule_dir.is_dir():
        print(f"ERROR: capsule directory not found: {capsule_dir}")
        return 1

    errors = verify_capsule(capsule_dir, args.check_git_tag, args.repo.resolve())
    if errors:
        print("Capsule verification: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    manifest = json.loads(read_text(capsule_dir / "STATE_MANIFEST.json"))
    print("Capsule verification: PASS")
    print(f"Directory: {capsule_dir}")
    print(f"Version Hash: {manifest.get('version_hash')}")
    print(f"Branch: {manifest.get('branch')}")
    if args.check_git_tag:
        print(f"Git tag: capsule/{manifest.get('version_hash')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())