"""Shared helpers for capsule packaging and verification."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path


RELEASE = "v0.1.2 EXTERNAL_SEAL_PATCH"
SCHEMA_VERSION = "0.1.2"

INZIP_VERIFICATION_REPORT = (
    "# Verification Report\n\n"
    "Final archive hash is external-only.\n"
    "Do not record final audit ZIP SHA-256 inside the audit ZIP itself.\n"
    "See external .sha256 and .sealed.json files.\n"
)


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_version_hash(zip_sha256: str, ts: datetime | None = None) -> str:
    when = ts or datetime.now(timezone.utc)
    stamp = when.strftime("%Y%m%d-%H%M")
    suffix = zip_sha256[:4].lower() if zip_sha256 else secrets.token_hex(2)
    return f"v{stamp}-{suffix}"


def hash_from_filename(path: Path) -> str | None:
    patterns = [
        r"ai-task-state-capsule-source-(v\d{8}-\d{4}-[0-9a-f]{4})\.zip$",
        r"ai-task-state-capsule-(v\d{8}-\d{4}-[0-9a-f]{4})\.zip$",
        r"ai-task-state-capsule-work-audit-(v\d{8}-\d{4}-[0-9a-f]{4})\.zip$",
    ]
    for pattern in patterns:
        match = re.search(pattern, path.name)
        if match:
            return match.group(1)
    return None


def suffix_from_version_hash(version_hash: str) -> str | None:
    match = re.fullmatch(r"v\d{8}-\d{4}-([0-9a-f]{4})", version_hash)
    return match.group(1) if match else None


def external_seal_paths(zip_path: Path) -> tuple[Path, Path]:
    sha_path = Path(f"{zip_path}.sha256")
    sealed_path = zip_path.parent / f"{zip_path.stem}.sealed.json"
    return sha_path, sealed_path


def write_external_seal(zip_path: Path) -> dict:
    """Write dist-side .sha256 and .sealed.json for an audit archive."""
    archive_sha = sha256_file(zip_path)
    version_hash = hash_from_filename(zip_path) or ""
    sealed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    sha_path, sealed_path = external_seal_paths(zip_path)
    sha_path.write_text(f"{archive_sha}\n", encoding="utf-8")

    sealed_record = {
        "archive": zip_path.name,
        "archive_sha256": archive_sha,
        "audit_version_hash": version_hash,
        "sealed_at": sealed_at,
        "seal_type": "external_final_archive_record",
    }
    sealed_path.write_text(json.dumps(sealed_record, indent=2) + "\n", encoding="utf-8")

    return {
        "sha256_path": sha_path,
        "sealed_path": sealed_path,
        "archive_sha256": archive_sha,
        "audit_version_hash": version_hash,
        "sealed_at": sealed_at,
    }