#!/usr/bin/env python3
"""
Generate a versioned ZIP capsule from templates/ or a custom source directory.

Usage:
    python scripts/generate_capsule_zip.py --source templates
    python scripts/generate_capsule_zip.py --source examples/example-coding-task
    python scripts/generate_capsule_zip.py --source templates --output-dir dist
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def make_version_hash(zip_sha256: str, ts: datetime | None = None) -> str:
    when = ts or datetime.now(timezone.utc)
    stamp = when.strftime("%Y%m%d-%H%M")
    suffix = zip_sha256[:4].lower() if zip_sha256 else secrets.token_hex(2)
    return f"v{stamp}-{suffix}"


def collect_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for root, _dirs, filenames in os.walk(source_dir):
        for name in sorted(filenames):
            files.append(Path(root) / name)
    return files


def build_zip(source_dir: Path, zip_path: Path) -> list[str]:
    included: list[str] = []
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in collect_files(source_dir):
            arcname = file_path.relative_to(source_dir).as_posix()
            zf.write(file_path, arcname)
            included.append(arcname)
    return included


def rename_with_hash(zip_path: Path, version_hash: str, prefix: str) -> Path:
    final_name = f"{prefix}-{version_hash}.zip"
    final_path = zip_path.parent / final_name
    if zip_path != final_path:
        if final_path.exists():
            final_path.unlink()
        zip_path.rename(final_path)
    return final_path


def generate(
    source: Path,
    output_dir: Path,
    prefix: str = "ai-task-state-capsule",
) -> dict:
    if not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")

    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc)

    temp_name = output_dir / f"{prefix}-building.zip"
    if temp_name.exists():
        temp_name.unlink()

    included = build_zip(source, temp_name)
    digest = sha256_file(temp_name)
    version_hash = make_version_hash(digest, ts)

    final_path = rename_with_hash(temp_name, version_hash, prefix)

    return {
        "zip_path": final_path,
        "version_hash": version_hash,
        "sha256": digest,
        "included_files": included,
    }


def print_result(result: dict) -> None:
    print("Capsule ZIP:")
    print(result["zip_path"])
    print("Version Hash:")
    print(result["version_hash"])
    print("SHA-256:")
    print(result["sha256"])
    print("Included Files:")
    for name in result["included_files"]:
        print(f"  - {name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate AI Task State Capsule ZIP")
    parser.add_argument(
        "--source",
        default="templates",
        help="Source directory relative to project root (default: templates)",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Output directory relative to project root (default: dist)",
    )
    parser.add_argument(
        "--prefix",
        default="ai-task-state-capsule",
        help="ZIP filename prefix (default: ai-task-state-capsule)",
    )
    args = parser.parse_args(argv)

    root = project_root()
    source = (root / args.source).resolve()
    output_dir = (root / args.output_dir).resolve()

    try:
        result = generate(source, output_dir, prefix=args.prefix)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())