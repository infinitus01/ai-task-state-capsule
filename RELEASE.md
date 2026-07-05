# Release Notes

## v0.1.3 DOC_HYGIENE_PATCH

Documentation-only patch. No packaging architecture changes.

- Removed superseded interim FAIL records from `audit/VERIFICATION_REPORT.external.md`
- Updated `audit/NEXT_HANDOFF.md` artifact names and handoff layout
- Unified sealed-file naming to **external `.sealed.json`**
- Corrected file counts in `audit/WORK_AUDIT_REPORT.md`

## v0.1.2 EXTERNAL_SEAL_PATCH

### Changes

1. **External final archive seal** — audit ZIP no longer records its own final SHA-256 inside the archive.
2. **Three-part audit deliverable** in `dist/`:
   - `ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.zip`
   - `ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.zip.sha256`
   - `ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.sealed.json`
3. **In-zip `VERIFICATION_REPORT.md`** — static external-only notice only.
4. **Detailed verification** — written to `audit/VERIFICATION_REPORT.external.md` (not packed into audit ZIP).

### Release command

```powershell
python scripts/patch_release.py
```

## v0.1.1 AUDIT_CORRECTION_PATCH

### Changes

1. **GitHub-ready source ZIP** — `scripts/generate_source_zip.py` packages the full repository tree.
2. **Audit hash correction** — `VERSION_RECORD.json` inside sealed audit ZIP no longer asserts a wrong pre-seal `audit_version_hash` or `zip_sha256`. Authoritative values are written post-seal to external `.sealed.json` beside the audit ZIP in `dist/`.
3. **ZIP verification** — `scripts/verify_zips.py` opens each ZIP and marks PASS only when required internal files are proven to exist.

### Release command

```powershell
Set-Location C:\Users\Ming\ai-task-state-capsule
python scripts/patch_release.py
```

### Deliverables in `dist/`

- `ai-task-state-capsule-source-vYYYYMMDD-HHMM-xxxx.zip`
- `ai-task-state-capsule-vYYYYMMDD-HHMM-xxxx.zip`
- `ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.zip`