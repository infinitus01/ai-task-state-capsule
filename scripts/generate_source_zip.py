#!/usr/bin/env python3
"""
Generate a GitHub-ready source ZIP for the full project tree.

Usage:
    python scripts/generate_source_zip.py
    python scripts/generate_source_zip.py --output-dir dist
"""

from __future__ import annotations

import argparse
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pack_common import make_version_hash, project_root, sha256_file


SKIP_DIRS = {".git", "__pycache__", "dist", ".venv", "venv"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}


def collect_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name in SKIP_FILES or name.endswith(".pyc"):
                continue
            path = Path(dirpath) / name
            rel = path.relative_to(root)
            if rel.parts and rel.parts[0] in SKIP_DIRS:
                continue
            files.append(path)
    return files


def build_source_zip(root: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc)
    temp = output_dir / "ai-task-state-capsule-source-building.zip"
    if temp.exists():
        temp.unlink()

    included: list[str] = []
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in collect_source_files(root):
            rel = path.relative_to(root).as_posix()
            zf.write(path, f"ai-task-state-capsule/{rel}")
            included.append(rel)

    digest = sha256_file(temp)
    version_hash = make_version_hash(digest, ts)
    final = output_dir / f"ai-task-state-capsule-source-{version_hash}.zip"
    if final.exists():
        final.unlink()
    temp.rename(final)

    return {
        "zip_path": final,
        "version_hash": version_hash,
        "sha256": digest,
        "included_files": included,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate GitHub-ready source ZIP")
    parser.add_argument("--output-dir", default="dist", help="Output directory")
    args = parser.parse_args(argv)

    root = project_root()
    output_dir = (root / args.output_dir).resolve()
    result = build_source_zip(root, output_dir)

    print("Source ZIP:")
    print(result["zip_path"])
    print("Version Hash:")
    print(result["version_hash"])
    print("SHA-256:")
    print(result["sha256"])
    print("Included Files:")
    for name in result["included_files"]:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())