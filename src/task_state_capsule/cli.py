from __future__ import annotations

import argparse
import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FILES = [
    "TASK_STATUS_REPORT.md",
    "DECISION_LOG.md",
    "BRANCH_INFO.md",
    "RESUME_INSTRUCTIONS.md",
    "RECOVERY_CHECK.md",
    "STATE_MANIFEST.json",
]
VERSION_RE = re.compile(r"^v\d{8}-\d{4}-[A-Za-z0-9][A-Za-z0-9._-]*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

TEMPLATES = {
    "TASK_STATUS_REPORT.md": "# Task Status Report\n\n## Goal\n\nDescribe the task.\n\n## Current status\n\n- Status: draft\n\n## Blockers\n\n- None recorded.\n\n## Next actions\n\n- Define the next verified action.\n",
    "DECISION_LOG.md": "# Decision Log\n\nRecord decisions, rationale, alternatives, and status here.\n",
    "BRANCH_INFO.md": "# Branch Info\n\n- Branch: main\n- Purpose: initial task-state capsule\n- Rollback point: not yet recorded\n",
    "RESUME_INSTRUCTIONS.md": "# Resume Instructions\n\n1. Read all files in this capsule.\n2. Treat recorded decisions and blockers as task state, not as external-world truth.\n3. Verify current repository/world state before taking irreversible action.\n4. Continue only from the documented next action.\n",
    "RECOVERY_CHECK.md": "# Recovery Check\n\n- [ ] Re-read TASK_STATUS_REPORT.md\n- [ ] Re-read DECISION_LOG.md\n- [ ] Verify branch/repository state independently\n- [ ] Verify external effects independently\n- [ ] Confirm the next action is still authorized\n",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def make_version(now: datetime | None = None) -> str:
    ts = now or utc_now()
    return f"v{ts.strftime('%Y%m%d-%H%M')}-{secrets.token_hex(2)}"


def init_capsule(target: Path) -> int:
    if target.exists() and any(target.iterdir()):
        print(f"ERROR: target is not empty: {target}", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)
    for name, content in TEMPLATES.items():
        (target / name).write_text(content, encoding="utf-8")

    created = utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "schema_version": "0.2.0",
        "project_name": target.name,
        "capsule_type": "ai_task_state_capsule",
        "version_hash": make_version(),
        "previous_version_hash": None,
        "branch": "main",
        "created_at": created,
        "created_by": "task-capsule-cli",
        "status": "draft",
        "files": REQUIRED_FILES,
        "notes": "Created by task-capsule init",
    }
    (target / "STATE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Initialized capsule: {target}")
    print(f"State version: {manifest['version_hash']}")
    return 0


def validate_manifest(manifest: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["STATE_MANIFEST.json must contain a JSON object"]
    required_keys = [
        "schema_version", "project_name", "capsule_type", "version_hash",
        "previous_version_hash", "branch", "created_at", "created_by",
        "status", "files",
    ]
    for key in required_keys:
        if key not in manifest:
            errors.append(f"manifest missing key: {key}")
    if manifest.get("capsule_type") != "ai_task_state_capsule":
        errors.append("capsule_type must be ai_task_state_capsule")
    version = manifest.get("version_hash")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        errors.append("version_hash is invalid")
    previous = manifest.get("previous_version_hash")
    if previous is not None and (not isinstance(previous, str) or not VERSION_RE.fullmatch(previous)):
        errors.append("previous_version_hash is invalid")
    if not isinstance(manifest.get("project_name"), str) or not manifest.get("project_name", "").strip():
        errors.append("project_name must be non-empty")
    if not isinstance(manifest.get("branch"), str) or not manifest.get("branch", "").strip():
        errors.append("branch must be non-empty")
    created_at = manifest.get("created_at")
    if not isinstance(created_at, str) or not created_at.endswith("Z"):
        errors.append("created_at must be a UTC timestamp ending in Z")
    files = manifest.get("files")
    if not isinstance(files, list):
        errors.append("files must be an array")
    else:
        for name in REQUIRED_FILES:
            if name not in files:
                errors.append(f"manifest files missing: {name}")
    content_sha = manifest.get("capsule_content_sha256")
    if content_sha is not None and (not isinstance(content_sha, str) or not SHA256_RE.fullmatch(content_sha)):
        errors.append("capsule_content_sha256 is invalid")
    return errors


def verify_capsule(target: Path) -> int:
    errors: list[str] = []
    if not target.is_dir():
        print(f"FAIL: not a directory: {target}", file=sys.stderr)
        return 2
    for name in REQUIRED_FILES:
        if not (target / name).is_file():
            errors.append(f"missing required file: {name}")
    manifest_path = target / "STATE_MANIFEST.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"manifest parse failed: {exc}")
        else:
            errors.extend(validate_manifest(manifest))

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    print(f"Capsule verified: {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="task-capsule", description="Create and verify AI Task State Capsules")
    parser.add_argument("--version", action="version", version="task-capsule 0.2.0")
    sub = parser.add_subparsers(dest="command", required=True)
    init_p = sub.add_parser("init", help="create a new task-state capsule")
    init_p.add_argument("target", type=Path)
    verify_p = sub.add_parser("verify", help="verify capsule structure and manifest identity fields")
    verify_p.add_argument("target", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        return init_capsule(args.target)
    if args.command == "verify":
        return verify_capsule(args.target)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
