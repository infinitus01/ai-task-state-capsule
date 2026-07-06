# Decision Log

## Entries

### DEC-20260706-001: Pilot on this repo only (no org-wide rollout)
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** User wants to trial capsule workflow on one real task before standardizing everywhere.
- **Decision:** Dogfood `.capsule/` inside `ai-task-state-capsule` repo; do not require other projects yet.
- **Rationale:** Lowest friction; state is non-confidential and repo already on GitHub.
- **Alternatives considered:** Start on a research repo (rejected — confidentiality / overhead).
- **Consequences:** This folder becomes the living task state for repo maintenance only.
- **Links:** `docs/GIT_CAPSULE_ALIGNMENT.md`

### DEC-20260706-002: Git tag mirrors capsule hash
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** Rollback requires code + narrative alignment.
- **Decision:** Tag `capsule/<version_hash>` on each milestone commit that includes `.capsule/`.
- **Rationale:** Documented in GIT_CAPSULE_ALIGNMENT guide.
- **Alternatives considered:** ZIP-only snapshots (kept optional, not primary).
- **Consequences:** Recovery uses `git checkout capsule/v20260706-1200-caps` plus restored capsule files.
- **Links:** commit at pilot bootstrap

### DEC-20260705-001: File format over product (unchanged)
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** Early release scope.
- **Decision:** Ship templates + docs + scripts; no hosted platform, IDE plugin, or auto-sync.
- **Rationale:** Interlock Layer is a format, not an app.
- **Alternatives considered:** Chrome extension, clipboard watcher (rejected).
- **Consequences:** Promotion and integrations are out of scope for pilot.
- **Links:** `docs/INTERLOCK_LAYER.md`, GitHub tag `v0.1.4`