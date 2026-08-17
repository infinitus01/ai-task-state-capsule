#!/usr/bin/env python3
"""
Inspect ZIP archives and prove required files exist before marking PASS.

v0.1.2: Audit ZIP final hash is verified only via external .sha256 and .sealed.json.
The in-zip VERIFICATION_REPORT.md must not record the final audit archive SHA-256.

Usage:
    python scripts/verify_zips.py
    python scripts/verify_zips.py --dist dist --output audit/VERIFICATION_REPORT.external.md
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pack_common import (
    INZIP_VERIFICATION_REPORT,
    RELEASE,
    capsule_content_sha256_from_zip,
    external_seal_paths,
    hash_from_filename,
    normalize_text,
    project_root,
    read_capsule_manifest_from_zip,
    sha256_file,
    suffix_from_version_hash,
)


CAPSULE_REQUIRED = {
    "TASK_STATUS_REPORT.md",
    "DECISION_LOG.md",
    "BRANCH_INFO.md",
    "RESUME_INSTRUCTIONS.md",
    "RECOVERY_CHECK.md",
    "STATE_MANIFEST.json",
}

AUDIT_REQUIRED = {
    "WORK_AUDIT_REPORT.md",
    "FILE_TREE.txt",
    "VERSION_RECORD.json",
    "SHA256SUMS.txt",
    "DELIVERABLE_MANIFEST.json",
    "ACCEPTANCE_CHECK.md",
    "LIMITATIONS.md",
    "NEXT_HANDOFF.md",
    "VERIFICATION_REPORT.md",
}

SOURCE_REQUIRED = {
    "README.md",
    "LICENSE",
    ".gitignore",
    "templates/TASK_STATUS_REPORT.md",
    "templates/DECISION_LOG.md",
    "templates/BRANCH_INFO.md",
    "templates/RESUME_INSTRUCTIONS.md",
    "templates/RECOVERY_CHECK.md",
    "templates/STATE_MANIFEST.json",
    "examples/example-coding-task/TASK_STATUS_REPORT.md",
    "examples/example-coding-task/DECISION_LOG.md",
    "examples/example-coding-task/BRANCH_INFO.md",
    "examples/example-coding-task/RESUME_INSTRUCTIONS.md",
    "examples/example-coding-task/RECOVERY_CHECK.md",
    "examples/example-coding-task/STATE_MANIFEST.json",
    "docs/VERSION_HASH_RULES.md",
    "docs/BRANCH_AND_ROLLBACK.md",
    "docs/AI_RESUME_PROTOCOL.md",
    "docs/CUSTOMIZATION_GUIDE.md",
    "scripts/generate_capsule_zip.py",
    "scripts/generate_audit_zip.py",
    "scripts/generate_source_zip.py",
    "scripts/verify_zips.py",
    "scripts/pack_common.py",
}


def classify_zip(path: Path) -> str:
    name = path.name
    if "work-audit" in name:
        return "audit"
    if "-source-" in name:
        return "source"
    if name.startswith("ai-task-state-capsule-v"):
        return "capsule"
    return "unknown"


def normalize_entries(names: list[str]) -> set[str]:
    normalized: set[str] = set()
    for name in names:
        normalized.add(name.replace("\\", "/"))
        if name.startswith("ai-task-state-capsule/"):
            normalized.add(name[len("ai-task-state-capsule/") :])
    return normalized


def check_version_record_in_zip(zf: zipfile.ZipFile) -> dict:
    if "VERSION_RECORD.json" not in zf.namelist():
        return {
            "integrity": "FAIL",
            "detail": "VERSION_RECORD.json not found in audit ZIP",
        }

    record = json.loads(zf.read("VERSION_RECORD.json").decode("utf-8"))
    declared_hash = record.get("audit_version_hash")
    declared_sha = record.get("zip_sha256")

    if declared_hash not in (None, "", "null") or declared_sha not in (None, "", "null"):
        return {
            "integrity": "FAIL",
            "detail": "Audit ZIP must not self-assert audit_version_hash or zip_sha256",
        }

    return {
        "integrity": "PASS",
        "detail": "VERSION_RECORD defers final archive hash to external seal files",
    }


def check_inzip_verification_report(zf: zipfile.ZipFile, actual_sha: str) -> dict:
    if "VERIFICATION_REPORT.md" not in zf.namelist():
        return {"integrity": "FAIL", "detail": "VERIFICATION_REPORT.md missing"}

    content = normalize_text(zf.read("VERIFICATION_REPORT.md").decode("utf-8"))
    expected = normalize_text(INZIP_VERIFICATION_REPORT)
    if content != expected:
        return {
            "integrity": "FAIL",
            "detail": "In-zip VERIFICATION_REPORT.md must be the external-only static notice",
        }
    if actual_sha in content:
        return {
            "integrity": "FAIL",
            "detail": "In-zip VERIFICATION_REPORT.md must not contain final audit archive SHA-256",
        }

    return {
        "integrity": "PASS",
        "detail": "In-zip verification report correctly defers final hash externally",
    }


def check_external_seal(zip_path: Path, actual_sha: str, filename_hash: str | None) -> dict:
    sha_path, sealed_path = external_seal_paths(zip_path)
    missing = [p.name for p in (sha_path, sealed_path) if not p.exists()]
    if missing:
        return {
            "integrity": "FAIL",
            "detail": f"Missing external seal files: {', '.join(missing)}",
        }

    recorded_sha = sha_path.read_text(encoding="utf-8").strip().split()[0]
    sealed = json.loads(sealed_path.read_text(encoding="utf-8"))

    checks = []
    if recorded_sha != actual_sha:
        checks.append(".sha256 does not match archive SHA-256")
    if sealed.get("archive_sha256") != actual_sha:
        checks.append(".sealed.json archive_sha256 mismatch")
    if sealed.get("archive") != zip_path.name:
        checks.append(".sealed.json archive name mismatch")
    if filename_hash and sealed.get("audit_version_hash") != filename_hash:
        checks.append(".sealed.json audit_version_hash mismatch")
    if sealed.get("seal_type") != "external_final_archive_record":
        checks.append("seal_type must be external_final_archive_record")

    if checks:
        return {"integrity": "FAIL", "detail": "; ".join(checks)}

    return {
        "integrity": "PASS",
        "detail": "External .sha256 and .sealed.json match sealed audit archive",
        "sealed_record": sealed,
    }


def check_capsule_manifest_and_content(
    zf: zipfile.ZipFile, filename_version_hash: str | None
) -> dict:
    try:
        manifest = read_capsule_manifest_from_zip(zf)
        recomputed_content_sha = capsule_content_sha256_from_zip(zf)
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        return {
            "integrity": "FAIL",
            "detail": f"Unable to read capsule manifest/content: {exc}",
            "state_version_hash": None,
            "capsule_content_sha256": None,
        }

    state_version_hash = manifest.get("version_hash")
    declared_content_sha = manifest.get("capsule_content_sha256")
    checks = []
    if not isinstance(state_version_hash, str) or not state_version_hash:
        checks.append("STATE_MANIFEST.json version_hash missing")
    elif filename_version_hash != state_version_hash:
        checks.append("filename state version does not match STATE_MANIFEST.json")
    if not isinstance(declared_content_sha, str) or not declared_content_sha:
        checks.append("STATE_MANIFEST.json capsule_content_sha256 missing")
    elif declared_content_sha != recomputed_content_sha:
        checks.append("recomputed capsule content SHA-256 does not match STATE_MANIFEST.json")

    if checks:
        return {
            "integrity": "FAIL",
            "detail": "; ".join(checks),
            "state_version_hash": state_version_hash,
            "capsule_content_sha256": declared_content_sha,
        }

    return {
        "integrity": "PASS",
        "detail": "Filename state version and recomputed capsule content SHA-256 match STATE_MANIFEST.json",
        "state_version_hash": state_version_hash,
        "capsule_content_sha256": declared_content_sha,
    }


def check_capsule_external_seal(
    zip_path: Path,
    actual_sha: str,
    filename_version_hash: str | None,
    manifest_content_sha: object,
) -> dict:
    sha_path, sealed_path = external_seal_paths(zip_path)
    missing = [path.name for path in (sha_path, sealed_path) if not path.exists()]
    if missing:
        return {
            "integrity": "FAIL",
            "detail": f"Missing capsule external seal files: {', '.join(missing)}",
        }

    sha_parts = sha_path.read_text(encoding="utf-8").strip().split()
    try:
        sealed = json.loads(sealed_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return {"integrity": "FAIL", "detail": f"Invalid capsule .sealed.json: {exc}"}

    checks = []
    if len(sha_parts) != 2:
        checks.append(".sha256 must record exactly archive SHA-256 and archive filename")
    else:
        if sha_parts[0] != actual_sha:
            checks.append(".sha256 does not match archive SHA-256")
        if sha_parts[1] != zip_path.name:
            checks.append(".sha256 archive filename mismatch")
    if sealed.get("archive_sha256") != actual_sha:
        checks.append(".sealed.json archive_sha256 mismatch")
    if sealed.get("archive") != zip_path.name:
        checks.append(".sealed.json archive name mismatch")
    if sealed.get("state_version_hash") != filename_version_hash:
        checks.append(".sealed.json state_version_hash mismatch")
    if sealed.get("capsule_content_sha256") != manifest_content_sha:
        checks.append(".sealed.json capsule_content_sha256 mismatch")
    if sealed.get("seal_type") != "external_capsule_archive_record":
        checks.append("seal_type must be external_capsule_archive_record")

    if checks:
        return {"integrity": "FAIL", "detail": "; ".join(checks)}
    return {
        "integrity": "PASS",
        "detail": "External capsule .sha256 and .sealed.json match archive, state version, and content hash",
        "sealed_record": sealed,
    }


def verify_zip(path: Path) -> dict:
    kind = classify_zip(path)
    actual_sha = sha256_file(path)
    filename_hash = hash_from_filename(path)
    suffix = suffix_from_version_hash(filename_hash) if filename_hash else None
    suffix_ok = bool(suffix and actual_sha.lower().startswith(suffix.lower()))

    with zipfile.ZipFile(path, "r") as zf:
        entries = normalize_entries(zf.namelist())
        if kind == "source":
            required = SOURCE_REQUIRED
        elif kind == "audit":
            required = AUDIT_REQUIRED
        elif kind == "capsule":
            required = CAPSULE_REQUIRED
        else:
            required = set()

        missing = sorted(req for req in required if req not in entries)
        present = sorted(req for req in required if req in entries)
        contents_ok = len(missing) == 0

        version_record = None
        inzip_report = None
        external_seal = None
        capsule_manifest = None
        capsule_external_seal = None
        if kind == "audit":
            version_record = check_version_record_in_zip(zf)
            inzip_report = check_inzip_verification_report(zf, actual_sha)
            external_seal = check_external_seal(path, actual_sha, filename_hash)
        elif kind == "capsule":
            capsule_manifest = check_capsule_manifest_and_content(zf, filename_hash)
            capsule_external_seal = check_capsule_external_seal(
                path,
                actual_sha,
                filename_hash,
                capsule_manifest.get("capsule_content_sha256"),
            )

    overall = "PASS" if contents_ok else "FAIL"
    if kind == "audit":
        for check in (version_record, inzip_report, external_seal):
            if check and check["integrity"] == "FAIL":
                overall = "FAIL"
    elif kind == "capsule":
        for check in (capsule_manifest, capsule_external_seal):
            if check and check["integrity"] == "FAIL":
                overall = "FAIL"

    return {
        "path": str(path),
        "kind": kind,
        "filename_hash": filename_hash,
        "sha256": actual_sha,
        "suffix_matches_sha256": suffix_ok,
        "required_count": len(required),
        "present_required": present,
        "missing_required": missing,
        "contents_check": "PASS" if contents_ok else "FAIL",
        "version_record": version_record,
        "inzip_report": inzip_report,
        "external_seal": external_seal,
        "capsule_manifest": capsule_manifest,
        "capsule_external_seal": capsule_external_seal,
        "overall": overall,
    }


def render_report(results: list[dict], generated_at: str) -> str:
    lines = [
        "# Verification Report (External)",
        "",
        f"Release: {RELEASE}",
        f"Generated At: {generated_at}",
        "",
        "Rule: **Do not mark PASS unless the ZIP contents themselves prove the required files exist.**",
        "",
        "Note: Audit and capsule final archive hashes are **not** recorded inside their ZIPs. "
        "See adjacent `.sha256` and `.sealed.json` files in `dist/`.",
        "",
    ]

    overall = "PASS" if results and all(item["overall"] == "PASS" for item in results) else "FAIL"
    lines.extend([f"## Overall: {overall}", ""])

    for item in results:
        lines.extend(
            [
                f"### {item['kind'].upper()} — `{Path(item['path']).name}`",
                "",
                f"- **Overall:** {item['overall']}",
                f"- **Contents Check:** {item['contents_check']}",
                f"- **SHA-256:** `{item['sha256']}`",
                f"- **Filename Version Hash:** `{item['filename_hash']}`",
                f"- **Suffix Matches SHA-256 Prefix:** {item['suffix_matches_sha256']}",
                "",
                "#### Required Files Present",
            ]
        )
        for name in item["present_required"]:
            lines.append(f"- [x] `{name}`")

        lines.extend(["", "#### Required Files Missing"])
        if item["missing_required"]:
            for name in item["missing_required"]:
                lines.append(f"- [ ] `{name}`")
        else:
            lines.append("- (none)")

        if item["kind"] == "audit":
            for label, check in (
                ("VERSION_RECORD", item["version_record"]),
                ("In-Zip Verification Report", item["inzip_report"]),
                ("External Seal", item["external_seal"]),
            ):
                if check:
                    lines.extend(
                        [
                            "",
                            f"#### {label}",
                            f"- **Integrity:** {check['integrity']}",
                            f"- **Detail:** {check['detail']}",
                        ]
                    )
            if item.get("external_seal", {}).get("sealed_record"):
                lines.extend(["", "#### External Sealed Record", ""])
                lines.extend(
                    [
                        "```json",
                        json.dumps(item["external_seal"]["sealed_record"], indent=2),
                        "```",
                    ]
                )
        elif item["kind"] == "capsule":
            for label, check in (
                ("Capsule Manifest and Content", item["capsule_manifest"]),
                ("Capsule External Seal", item["capsule_external_seal"]),
            ):
                if check:
                    lines.extend(
                        [
                            "",
                            f"#### {label}",
                            f"- **Integrity:** {check['integrity']}",
                            f"- **Detail:** {check['detail']}",
                        ]
                    )
            seal = item.get("capsule_external_seal")
            if seal and seal.get("sealed_record"):
                lines.extend(["", "#### Capsule Sealed Record", ""])
                lines.extend(
                    [
                        "```json",
                        json.dumps(seal["sealed_record"], indent=2),
                        "```",
                    ]
                )
        elif item["kind"] == "source":
            lines.extend(["", "#### Authoritative Archive Record", ""])
            lines.extend(
                [
                    "```json",
                    json.dumps(
                        {
                            "archive": Path(item["path"]).name,
                            "version_hash": item["filename_hash"],
                            "archive_sha256": item["sha256"],
                        },
                        indent=2,
                    ),
                    "```",
                ]
            )

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify ZIP deliverables")
    parser.add_argument("--dist", default="dist", help="Directory containing ZIP files")
    parser.add_argument(
        "--output",
        default="audit/VERIFICATION_REPORT.external.md",
        help="External verification report path relative to project root",
    )
    args = parser.parse_args(argv)

    root = project_root()
    dist = (root / args.dist).resolve()
    output = (root / args.output).resolve()

    if not dist.is_dir():
        print(f"dist directory not found: {dist}", file=sys.stderr)
        return 1

    all_zips = sorted(dist.glob("*.zip"), key=lambda p: p.name)
    if not all_zips:
        print(f"No ZIP files found in {dist}", file=sys.stderr)
        return 1

    latest: dict[str, Path] = {}
    for path in all_zips:
        kind = classify_zip(path)
        if kind == "unknown":
            continue
        current = latest.get(kind)
        if current is None or path.stat().st_mtime >= current.stat().st_mtime:
            latest[kind] = path

    zips = [latest[k] for k in sorted(latest)]
    results = [verify_zip(path) for path in zips]
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(results, generated_at), encoding="utf-8")

    print("Verification Report (External):")
    print(output)
    print("Overall:")
    overall = "PASS" if all(item["overall"] == "PASS" for item in results) else "FAIL"
    print(overall)
    for item in results:
        print(f"- {Path(item['path']).name}: {item['overall']}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
