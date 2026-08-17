#!/usr/bin/env python3
"""Generate a sealed, versioned Task State Capsule ZIP."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from pack_common import (
    capsule_content_sha256_from_directory,
    is_valid_version_hash,
    project_root,
    sha256_file,
    write_capsule_external_seal,
)

REQUIRED = {
    "TASK_STATUS_REPORT.md",
    "DECISION_LOG.md",
    "BRANCH_INFO.md",
    "RESUME_INSTRUCTIONS.md",
    "RECOVERY_CHECK.md",
    "STATE_MANIFEST.json",
}


def build(source: Path, output_dir: Path, prefix: str) -> dict:
    if not source.is_dir():
        raise FileNotFoundError(source)
    manifest_path = source / "STATE_MANIFEST.json"
    if not manifest_path.is_file():
        raise ValueError("STATE_MANIFEST.json missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = str(manifest.get("version_hash", "")).strip()
    if not is_valid_version_hash(version):
        raise ValueError("manifest version_hash is missing or invalid")
    missing = sorted(name for name in REQUIRED if not (source / name).is_file())
    if missing:
        raise ValueError(f"missing required files: {', '.join(missing)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / "capsule"
        shutil.copytree(source, staging)
        content_sha = capsule_content_sha256_from_directory(staging)
        staged_manifest_path = staging / "STATE_MANIFEST.json"
        staged_manifest = json.loads(staged_manifest_path.read_text(encoding="utf-8"))
        staged_manifest["capsule_content_sha256"] = content_sha
        staged_manifest_path.write_text(json.dumps(staged_manifest, indent=2) + "\n", encoding="utf-8")

        zip_path = output_dir / f"{prefix}-{version}.zip"
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(staging.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                    zf.write(path, path.relative_to(staging).as_posix())

    seal = write_capsule_external_seal(
        zip_path,
        state_version_hash=version,
        capsule_content_sha256=content_sha,
    )
    return {
        "zip_path": zip_path,
        "version_hash": version,
        "capsule_content_sha256": content_sha,
        "archive_sha256": sha256_file(zip_path),
        "seal": seal,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate sealed AI Task State Capsule ZIP")
    parser.add_argument("--source", default="examples/example-coding-task")
    parser.add_argument("--output-dir", default="dist")
    parser.add_argument("--prefix", default="ai-task-state-capsule")
    args = parser.parse_args(argv)
    root = project_root()
    try:
        result = build((root / args.source).resolve(), (root / args.output_dir).resolve(), args.prefix)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Capsule ZIP: {result['zip_path']}")
    print(f"State Version: {result['version_hash']}")
    print(f"Capsule Content SHA-256: {result['capsule_content_sha256']}")
    print(f"Archive SHA-256: {result['archive_sha256']}")
    print(f"External Seal: {result['seal']['sealed_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
