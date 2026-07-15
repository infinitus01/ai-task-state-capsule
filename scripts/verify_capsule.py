#!/usr/bin/env python3
"""Verify a task state capsule directory for structural consistency and handoff readiness."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from pack_common import is_valid_version_hash, project_root

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


def extract(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None


def verify_capsule(capsule_dir: Path, ready_for_handoff: bool, check_git_tag: bool, repo: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (capsule_dir / name).is_file():
            errors.append(f"MISSING: {name}")
    if errors:
        return errors

    try:
        manifest = json.loads(read_text(capsule_dir / "STATE_MANIFEST.json"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"STATE_MANIFEST.json invalid: {exc}"]

    version_hash = str(manifest.get("version_hash", "")).strip()
    if not is_valid_version_hash(version_hash):
        errors.append("STATE_MANIFEST.json: invalid version_hash")

    for field in ("project_name", "branch", "created_at", "created_by", "status"):
        if not str(manifest.get(field, "")).strip():
            errors.append(f"STATE_MANIFEST.json: {field} is empty")

    try:
        created_at = str(manifest.get("created_at", ""))
        if not created_at.endswith("Z"):
            raise ValueError
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        errors.append("STATE_MANIFEST.json: created_at must be ISO-8601 UTC ending Z")

    listed = manifest.get("files")
    if not isinstance(listed, list):
        errors.append("STATE_MANIFEST.json: files must be an array")
    else:
        for name in REQUIRED_FILES:
            if name not in listed:
                errors.append(f"STATE_MANIFEST.json files missing: {name}")

    report = read_text(capsule_dir / "TASK_STATUS_REPORT.md")
    resume = read_text(capsule_dir / "RESUME_INSTRUCTIONS.md")
    report_hash = extract(r"^Version Hash:\s*(\S+)\s*$", report)
    resume_hash = extract(r"Resume this task from version\s+(\S+)\.", resume)
    if report_hash != version_hash:
        errors.append(f"HASH_MISMATCH: manifest={version_hash} report={report_hash}")
    if resume_hash != version_hash:
        errors.append(f"HASH_MISMATCH: manifest={version_hash} resume={resume_hash}")

    if ready_for_handoff:
        placeholders = (
            "[VERSION_HASH]",
            "<!-- Single concrete next step -->",
            "Task / Project Name:\n",
            "Version Hash:\n",
        )
        if any(value in report + resume for value in placeholders):
            errors.append("HANDOFF_NOT_READY: unresolved template placeholder")
        priority_action = extract(r"### Priority Action 1\s*\n(.+)", report)
        if not priority_action or priority_action.startswith("<!--"):
            errors.append("HANDOFF_NOT_READY: Priority Action 1 missing")

    if check_git_tag and version_hash:
        tag = f"capsule/{version_hash}"
        result = subprocess.run(
            ["git", "tag", "-l", tag],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )
        if tag not in result.stdout.splitlines():
            errors.append(f"GIT_TAG_MISSING: {tag}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify capsule internal consistency")
    parser.add_argument("--capsule-dir", type=Path, default=project_root() / ".capsule")
    parser.add_argument("--ready-for-handoff", action="store_true")
    parser.add_argument("--check-git-tag", action="store_true")
    parser.add_argument("--repo", type=Path, default=project_root())
    args = parser.parse_args()
    if not args.capsule_dir.is_dir():
        print(f"ERROR: capsule directory not found: {args.capsule_dir}")
        return 1
    errors = verify_capsule(
        args.capsule_dir.resolve(),
        args.ready_for_handoff,
        args.check_git_tag,
        args.repo.resolve(),
    )
    if errors:
        print("Capsule verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Capsule verification: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
