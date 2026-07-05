#!/usr/bin/env python3
"""
Generate work audit ZIP with external final archive sealing.

v0.1.2: Final audit ZIP SHA-256 is never recorded inside the audit ZIP.
Authoritative seal lives beside the archive as:
  <archive>.zip.sha256
  <archive>.sealed.json

Usage:
    python scripts/generate_audit_zip.py
    python scripts/generate_audit_zip.py --capsule-zip dist/ai-task-state-capsule-v*.zip
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pack_common import (
    INZIP_VERIFICATION_REPORT,
    RELEASE,
    SCHEMA_VERSION,
    make_version_hash,
    project_root,
    sha256_file,
    write_external_seal,
)


AUDIT_FILES = [
    "WORK_AUDIT_REPORT.md",
    "FILE_TREE.txt",
    "VERSION_RECORD.json",
    "SHA256SUMS.txt",
    "DELIVERABLE_MANIFEST.json",
    "ACCEPTANCE_CHECK.md",
    "LIMITATIONS.md",
    "NEXT_HANDOFF.md",
    "VERIFICATION_REPORT.md",
]


def tree_lines(base: Path, prefix: str = "") -> list[str]:
    lines: list[str] = []
    entries = sorted(base.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    visible = [e for e in entries if e.name not in ("dist", ".git", "__pycache__")]
    for i, entry in enumerate(visible):
        connector = "└── " if i == len(visible) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry.name}")
        if entry.is_dir() and entry.name not in ("dist", "audit"):
            extension = "    " if i == len(visible) - 1 else "│   "
            lines.extend(tree_lines(entry, prefix + extension))
    return lines


def build_file_tree(root: Path) -> str:
    return "ai-task-state-capsule/\n" + "\n".join(tree_lines(root))


def collect_project_files(root: Path) -> list[Path]:
    skip_dirs = {".git", "__pycache__", "dist"}
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in sorted(filenames):
            path = Path(dirpath) / name
            rel = path.relative_to(root)
            if rel.parts and rel.parts[0] == "audit":
                continue
            if rel.suffix == ".pyc":
                continue
            files.append(path)
    return files


def write_sha256sums(root: Path, extra_paths: list[Path], audit_dir: Path) -> None:
    lines: list[str] = []
    for path in sorted(collect_project_files(root), key=lambda p: str(p).lower()):
        rel = path.relative_to(root).as_posix()
        lines.append(f"{sha256_file(path)}  {rel}")
    for path in extra_paths:
        if path.exists():
            lines.append(f"{sha256_file(path)}  {path.name}")
    (audit_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def infer_purpose(rel: str) -> str:
    mapping = {
        "README.md": "Project overview and quick start",
        "LICENSE": "MIT license",
        ".gitignore": "Git ignore rules",
        "scripts/verify_zips.py": "ZIP content verification",
        "scripts/generate_source_zip.py": "GitHub-ready source ZIP builder",
        "scripts/pack_common.py": "Shared packaging helpers",
    }
    if rel in mapping:
        return mapping[rel]
    if rel.startswith("templates/"):
        return "Blank capsule template"
    if rel.startswith("examples/"):
        return "Filled example capsule"
    if rel.startswith("docs/"):
        return "Documentation"
    if rel.startswith("scripts/"):
        return "Packaging / tooling script"
    if rel.startswith("audit/"):
        return "Work audit artifact"
    return "Project file"


def write_deliverable_manifest(root: Path, capsule_zip: Path | None, audit_dir: Path) -> None:
    deliverables = []
    for path in collect_project_files(root):
        rel = path.relative_to(root).as_posix()
        deliverables.append(
            {
                "path": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "purpose": infer_purpose(rel),
            }
        )
    for audit_file in sorted((root / "audit").glob("*")):
        if not audit_file.is_file():
            continue
        if audit_file.name.endswith(".external.md"):
            continue
        rel = audit_file.relative_to(root).as_posix()
        deliverables.append(
            {
                "path": rel,
                "size_bytes": audit_file.stat().st_size,
                "sha256": sha256_file(audit_file),
                "purpose": infer_purpose(rel),
            }
        )
    if capsule_zip and capsule_zip.exists():
        deliverables.append(
            {
                "path": str(capsule_zip.relative_to(root)),
                "size_bytes": capsule_zip.stat().st_size,
                "sha256": sha256_file(capsule_zip),
                "purpose": "Packaged capsule ZIP",
            }
        )
    (audit_dir / "DELIVERABLE_MANIFEST.json").write_text(
        json.dumps(deliverables, indent=2) + "\n", encoding="utf-8"
    )


def write_version_record_for_seal(
    audit_dir: Path,
    capsule_hash: str,
    capsule_zip_sha256: str,
) -> None:
    record = {
        "schema_version": SCHEMA_VERSION,
        "release": RELEASE,
        "project_name": "ai-task-state-capsule",
        "audit_version_hash": None,
        "capsule_version_hash": capsule_hash or None,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generated_by": "grok",
        "status": "completed",
        "zip_sha256": None,
        "integrity_note": (
            "Final audit archive hash is external-only. "
            "See adjacent .sha256 and .sealed.json beside the audit ZIP in dist/."
        ),
        "notes": f"capsule_zip_sha256: {capsule_zip_sha256 or 'n/a'}",
    }
    (audit_dir / "VERSION_RECORD.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )


def write_inzip_verification_report(audit_dir: Path) -> None:
    (audit_dir / "VERIFICATION_REPORT.md").write_text(
        INZIP_VERIFICATION_REPORT, encoding="utf-8"
    )


def build_audit_zip(audit_dir: Path, output_dir: Path) -> dict:
    ts = datetime.now(timezone.utc)
    temp = output_dir / "ai-task-state-capsule-work-audit-building.zip"
    if temp.exists():
        temp.unlink()

    included: list[str] = []
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in AUDIT_FILES:
            path = audit_dir / name
            if not path.exists():
                raise FileNotFoundError(f"Missing audit file: {path}")
            zf.write(path, name)
            included.append(name)

    digest = sha256_file(temp)
    version_hash = make_version_hash(digest, ts)
    final = output_dir / f"ai-task-state-capsule-work-audit-{version_hash}.zip"
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
    parser = argparse.ArgumentParser(description="Generate work audit ZIP")
    parser.add_argument("--capsule-zip", default="", help="Path to capsule ZIP")
    parser.add_argument("--capsule-hash", default="", help="Capsule version hash")
    args = parser.parse_args(argv)

    root = project_root()
    audit_dir = root / "audit"
    output_dir = root / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)

    capsule_zip = Path(args.capsule_zip) if args.capsule_zip else None
    if capsule_zip and not capsule_zip.is_absolute():
        capsule_zip = root / capsule_zip

    capsule_hash = args.capsule_hash
    capsule_zip_sha256 = ""
    if capsule_zip and capsule_zip.exists():
        capsule_zip_sha256 = sha256_file(capsule_zip)
        if not capsule_hash:
            stem = capsule_zip.stem
            prefix = "ai-task-state-capsule-"
            capsule_hash = stem[len(prefix) :] if stem.startswith(prefix) else stem

    write_version_record_for_seal(audit_dir, capsule_hash, capsule_zip_sha256)
    write_inzip_verification_report(audit_dir)
    (audit_dir / "FILE_TREE.txt").write_text(build_file_tree(root), encoding="utf-8")
    write_sha256sums(root, [p for p in [capsule_zip] if p], audit_dir)
    write_deliverable_manifest(root, capsule_zip, audit_dir)

    result = build_audit_zip(audit_dir, output_dir)
    seal = write_external_seal(result["zip_path"])

    print("Audit ZIP:")
    print(result["zip_path"])
    print("Audit Version Hash:")
    print(result["version_hash"])
    print("SHA-256:")
    print(result["sha256"])
    print("External SHA-256 File:")
    print(seal["sha256_path"])
    print("External Sealed Record:")
    print(seal["sealed_path"])
    print("Included Files:")
    for name in result["included_files"]:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())