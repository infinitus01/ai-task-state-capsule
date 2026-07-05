# Version Hash Rules

## Format

```text
vYYYYMMDD-HHMM-xxxx
```

| Segment | Meaning |
|---------|---------|
| `v` | Literal prefix |
| `YYYYMMDD` | UTC date when capsule was sealed |
| `HHMM` | UTC time (24h, no separator) |
| `xxxx` | 4-character suffix (see below) |

## Suffix Generation

When using `scripts/generate_capsule_zip.py`:

1. Build ZIP from source directory
2. Compute SHA-256 of the ZIP file
3. Take first 4 hexadecimal characters as `xxxx`

If hashing fails, the script falls back to 4 random hex characters.

## Usage in Capsule Files

| Field | Location |
|-------|----------|
| `version_hash` | `STATE_MANIFEST.json` |
| `previous_version_hash` | `STATE_MANIFEST.json` (null for first version) |
| `Version Hash` | `TASK_STATUS_REPORT.md` header |
| Resume line | Section 6 and `RESUME_INSTRUCTIONS.md` |

## Chaining Versions

When sealing a new capsule after changes:

1. Set `previous_version_hash` to the old `version_hash`
2. Generate new ZIP → new `version_hash`
3. Update report header and resume blocks

## Verification

```bash
# Linux / macOS
sha256sum ai-task-state-capsule-v*.zip

# Windows PowerShell
Get-FileHash -Algorithm SHA256 .\ai-task-state-capsule-v*.zip
```

Compare full SHA-256 to the value printed by the packaging script. The 4-char suffix is a human-friendly handle, not a complete integrity check.

## Audit ZIP External Seal (v0.1.2+)

Audit archives do **not** record their final SHA-256 inside the ZIP. Post-seal artifacts:

```text
ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.zip
ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.zip.sha256
ai-task-state-capsule-work-audit-vYYYYMMDD-HHMM-xxxx.sealed.json
```

The external `.sealed.json` file beside the audit ZIP in `dist/` is the authoritative final archive record.