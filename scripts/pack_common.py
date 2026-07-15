"""Shared helpers for capsule packaging and verification."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

RELEASE = "v0.1.5 VALIDATION_HARDENING"
SCHEMA_VERSION = "0.1.5"
VERSION_HASH_PATTERN = r"v\d{8}-\d{4}-[A-Za-z0-9][A-Za-z0-9._-]*"
VERSION_HASH_RE = re.compile(rf"^{VERSION_HASH_PATTERN}$")

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
    """Legacy digest-derived ID used by source and audit release archives."""
    when = ts or datetime.now(timezone.utc)
    stamp = when.strftime("%Y%m%d-%H%M")
    suffix = zip_sha256[:4].lower() if zip_sha256 else secrets.token_hex(2)
    return f"v{stamp}-{suffix}"


def is_valid_version_hash(value: object) -> bool:
    return isinstance(value, str) and bool(VERSION_HASH_RE.fullmatch(value.strip()))


def hash_from_filename(path: Path) -> str | None:
    patterns = [
        rf"ai-task-state-capsule-source-({VERSION_HASH_PATTERN})\.zip$",
        rf"ai-task-state-capsule-({VERSION_HASH_PATTERN})\.zip$",
        rf"ai-task-state-capsule-work-audit-({VERSION_HASH_PATTERN})\.zip$",
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
    return Path(f"{zip_path}.sha256"), zip_path.parent / f"{zip_path.stem}.sealed.json"


def write_external_seal(zip_path: Path) -> dict:
    archive_sha = sha256_file(zip_path)
    version_hash = hash_from_filename(zip_path) or ""
    sealed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sha_path, sealed_path = external_seal_paths(zip_path)
    sha_path.write_text(f"{archive_sha}  {zip_path.name}\n", encoding="utf-8")
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


def write_capsule_external_seal(zip_path: Path, *, state_version_hash: str, capsule_content_sha256: str) -> dict:
    """Seal a capsule archive without storing the final ZIP hash inside itself."""
    archive_sha = sha256_file(zip_path)
    sealed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sha_path, sealed_path = external_seal_paths(zip_path)
    sha_path.write_text(f"{archive_sha}  {zip_path.name}\n", encoding="utf-8")
    sealed_record = {
        "archive": zip_path.name,
        "archive_sha256": archive_sha,
        "state_version_hash": state_version_hash,
        "capsule_content_sha256": capsule_content_sha256,
        "sealed_at": sealed_at,
        "seal_type": "external_capsule_archive_record",
    }
    sealed_path.write_text(json.dumps(sealed_record, indent=2) + "\n", encoding="utf-8")
    return {
        "sha256_path": sha_path,
        "sealed_path": sealed_path,
        "archive_sha256": archive_sha,
        "state_version_hash": state_version_hash,
        "capsule_content_sha256": capsule_content_sha256,
        "sealed_at": sealed_at,
    }


def _canonical_manifest_bytes(raw: bytes) -> bytes:
    manifest = json.loads(raw.decode("utf-8"))
    manifest["capsule_content_sha256"] = None
    return (json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _content_digest(file_map: Mapping[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(file_map):
        normalized = name.replace("\\", "/").lstrip("./")
        data = file_map[name]
        if normalized == "STATE_MANIFEST.json":
            data = _canonical_manifest_bytes(data)
        name_bytes = normalized.encode("utf-8")
        digest.update(len(name_bytes).to_bytes(8, "big"))
        digest.update(name_bytes)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def capsule_content_sha256_from_directory(source_dir: Path) -> str:
    file_map: dict[str, bytes] = {}
    for path in sorted(source_dir.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            file_map[path.relative_to(source_dir).as_posix()] = path.read_bytes()
    return _content_digest(file_map)


def _normalized_zip_file_map(zf: zipfile.ZipFile) -> dict[str, bytes]:
    names = [name.replace("\\", "/") for name in zf.namelist() if not name.endswith("/")]
    prefix = ""
    if names and all("/" in name for name in names):
        first = {name.split("/", 1)[0] for name in names}
        if len(first) == 1:
            candidate = next(iter(first)) + "/"
            stripped = [name[len(candidate):] for name in names]
            if "STATE_MANIFEST.json" in stripped:
                prefix = candidate
    file_map: dict[str, bytes] = {}
    for original in names:
        normalized = original[len(prefix):] if prefix and original.startswith(prefix) else original
        if normalized in file_map:
            raise ValueError(f"Duplicate normalized ZIP path: {normalized}")
        file_map[normalized] = zf.read(original)
    return file_map


def capsule_content_sha256_from_zip(zf: zipfile.ZipFile) -> str:
    return _content_digest(_normalized_zip_file_map(zf))


def read_capsule_manifest_from_zip(zf: zipfile.ZipFile) -> dict:
    file_map = _normalized_zip_file_map(zf)
    raw = file_map.get("STATE_MANIFEST.json")
    if raw is None:
        raise FileNotFoundError("STATE_MANIFEST.json not found in capsule ZIP")
    return json.loads(raw.decode("utf-8"))
