# Next Handoff

Instructions for the next AI session or human developer.

## Immediate Steps

1. **Initialize Git** (if publishing to GitHub):
   ```powershell
   cd C:\Users\Ming\ai-task-state-capsule
   git init
   git add .
   git commit -m "Initial commit: AI Task State Capsule v0.1 templates and tooling"
   ```

2. **Verify packaging**:
   ```powershell
   python scripts/patch_release.py
   python scripts/verify_zips.py
   ```

3. **Push to GitHub** when ready — create remote repo and push; not done in this session.

## Current Release Artifacts (v0.1.2 baseline)

```text
dist/ai-task-state-capsule-source-v20260705-0846-8f4d.zip
dist/ai-task-state-capsule-v20260705-0846-ab1b.zip
dist/ai-task-state-capsule-work-audit-v20260705-0846-5043.zip
dist/ai-task-state-capsule-work-audit-v20260705-0846-5043.zip.sha256
dist/ai-task-state-capsule-work-audit-v20260705-0846-5043.sealed.json
```

Audit final archive integrity uses **external** `.sha256` and **external** `.sealed.json` beside the audit ZIP. Do not look for final SHA inside the audit ZIP.

Re-release command:

```powershell
python scripts/patch_release.py
```

## Suggested v0.2 Work

- Add `schema/STATE_MANIFEST.schema.json` and validation script
- Add pytest for ZIP naming, hash format, and manifest JSON validity
- CLI subcommand: `diff` between two capsule directories
- Optional template pack: `templates-research/`

## Resume Prompt for Next AI

```text
Continue development of ai-task-state-capsule (local-first AI task state capsule format).

Current state: v0.1.3 doc hygiene on top of v0.1.2 external seal — templates, example, docs, packaging scripts, audit package.

Read:
- README.md
- audit/WORK_AUDIT_REPORT.md
- audit/LIMITATIONS.md
- audit/VERIFICATION_REPORT.external.md

Do not add: HEA content, cloud sync, browser/IDE extensions, clipboard automation.

Priority: JSON Schema validation + pytest for packaging scripts
```

## Key Paths

| Path | Purpose |
|------|---------|
| `templates/` | Blank capsule to copy |
| `examples/example-coding-task/` | Reference filled capsule |
| `scripts/generate_capsule_zip.py` | Produce versioned ZIP |
| `scripts/generate_audit_zip.py` | Produce audit ZIP + external seal files |
| `scripts/verify_zips.py` | Verify ZIP contents; write external verification report |
| `dist/` | Generated ZIP output and external `.sha256` / `.sealed.json` |
| `audit/` | Work audit source files (not the external sealed record) |

## Contact Points

- Final audit archive record: `dist/<audit-archive>.sealed.json` (external sealed record)
- In-zip capsule metadata: `audit/VERSION_RECORD.json` (deferred hash fields only)
- Questions about branch/recovery: `docs/BRANCH_AND_ROLLBACK.md`, `docs/AI_RESUME_PROTOCOL.md`