# Limitations

Honest assessment of gaps and unverified items.

## Unverified

- Packaging scripts tested on Windows PowerShell only in this session; Linux/macOS path handling assumed correct via `pathlib` but not executed on those OSes
- `STATE_MANIFEST.json` schema is documented but not enforced by a JSON Schema file or validator
- Example version hash in `examples/example-coding-task/` (`v20260705-1430-a1b2`) is illustrative; it does not match the templates ZIP hash from this build

## Not Implemented

- Git repository initialization (`git init`) — user may do this before GitHub push
- GitHub Actions CI
- Unit tests for `generate_capsule_zip.py` / `generate_audit_zip.py`
- Diff tool for comparing two capsule versions
- Optional encryption for sensitive metadata

## Environment Notes

- ZIP files written to `dist/` (gitignored by design)
- Audit dynamic files (`FILE_TREE.txt`, `SHA256SUMS.txt`, `DELIVERABLE_MANIFEST.json`) regenerated each audit script run; checksums change if any source file changes
- v0.1.2 fix: final audit archive SHA lives only in external `.sha256` and external `.sealed.json` beside the audit ZIP in `dist/`; in-zip `VERIFICATION_REPORT.md` is static external-only notice

## Scope Boundaries (intentional)

Per requirements, the following were explicitly excluded and are not limitations of this delivery—they are out of scope:

- Cloud sync, extensions, sidecar daemons, clipboard automation
- Domain-specific (HEA) workflows