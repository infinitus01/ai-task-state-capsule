# Decision Log

## Entries

### DEC-20260705-001: File-based capsule over chat export
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** Long sessions produce noisy chat logs unsuitable for handoff.
- **Decision:** Use curated markdown + JSON capsule files.
- **Rationale:** Higher signal, Git-diffable, branch-friendly.
- **Alternatives considered:** Full chat export; single mega-prompt file.
- **Consequences:** Users must maintain capsule files during work.
- **Links:** `TASK_STATUS_REPORT.md` section 5

### DEC-20260705-002: No cloud sync in v0.1
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** Sync adds auth, conflict resolution, and compliance surface.
- **Decision:** Local-first only; ZIP for transport.
- **Rationale:** Matches developer workflow; zero infra.
- **Alternatives considered:** Private gist; S3 bucket; custom server.
- **Consequences:** Manual copy or Git for sharing.
- **Links:** README "What This Project Does Not Do"

### DEC-20260705-003: Default directory `.capsule/`
- **Date:** 2026-07-05
- **Status:** proposed
- **Context:** Need convention for where capsule lives relative to code repo.
- **Decision:** (pending) Prefer hidden `.capsule/` at repo root.
- **Rationale:** Keeps task state adjacent to code without cluttering top level.
- **Alternatives considered:** `capsule/` visible folder; sibling repo.
- **Consequences:** Document in CUSTOMIZATION_GUIDE once accepted.
- **Links:** Priority Action 1 in status report