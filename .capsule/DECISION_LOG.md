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

### DEC-20260706-004: Formalize handoff tests before second repo
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** One T1 pass; need repeatable process.
- **Decision:** Add HANDOFF_TEST_PROTOCOL + verify_capsule.py; first-response contract in resume template.
- **Rationale:** Reduce variance; catch hash drift before handoff.
- **Alternatives considered:** Ad-hoc testing only (rejected).
- **Consequences:** Pilot exit criteria now explicit in protocol doc.
- **Links:** `docs/HANDOFF_TEST_PROTOCOL.md`, `scripts/verify_capsule.py`

### DEC-20260706-003: Cross-AI handoff trial passed
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** User handed RESUME_INSTRUCTIONS + capsule files to another AI.
- **Decision:** Record success; roll capsule forward to `v20260706-1400-hand`.
- **Rationale:** Confirms format works for session handoff without chat history.
- **Alternatives considered:** Skip recording (rejected — loses pilot evidence).
- **Consequences:** Exp-pilot-01 at 1/3; still need 1–2 more handoffs before second repo.
- **Links:** `capsule/v20260706-1400-hand`

### DEC-20260705-001: File format over product (unchanged)
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** Early release scope.
- **Decision:** Ship templates + docs + scripts; no hosted platform, IDE plugin, or auto-sync.
- **Rationale:** Interlock Layer is a format, not an app.
- **Alternatives considered:** Chrome extension, clipboard watcher (rejected).
- **Consequences:** Promotion and integrations are out of scope for pilot.
- **Links:** `docs/INTERLOCK_LAYER.md`, GitHub tag `v0.1.4`