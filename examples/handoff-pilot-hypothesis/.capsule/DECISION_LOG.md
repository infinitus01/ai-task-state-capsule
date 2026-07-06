# Decision Log

## Entries

### DEC-20260706-008: RUN-002 toy layers pilot — HYP-002 accepted (toy)
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** Run comparison between single-layer G and two-layer A/B under variance matching.
- **Decision:** Execute 6-seed pilot; error reduction Δ metric ≥ 10.0% (mean ~14.84%); all 6/6 PASS → HYP-002 accepted on toy domain.
- **Rationale:** Two-layer structure mitigates total variance propagation on benchmark distribution.
- **Consequences:** In Progress slot cleared again; awaiting user's direction on production domain or next phase.
- **Links:** `v20260706-2700-run2`, `work/runs/toy_layers_pilot.py`, `work/runs/RUN-002_HYP-002_layers.md`

### DEC-20260706-007: Start HYP-002 layer comparison
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** User chose HYP-002 (two-layer vs single-layer error propagation) rather than pin real x,y,f for HYP-001.
- **Decision:** Elevate HYP-002 to the unique "In Progress" status, create RUN-002 pilot scaffold, roll capsule forward.
- **Rationale:** Clear separation of sequential hypothesis testing.
- **Consequences:** HYP-002 active until RUN-002 complete.
- **Links:** `v20260706-2600-run2`, `work/hypotheses/HYP-002.md`, `work/runs/RUN-002_HYP-002_layers.md`

### DEC-20260706-006: RUN-001 toy bound pilot — HYP-001 accepted (toy)
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** Sync-build trial: implement toy_bound_pilot.py per RUN-001 δ-matrix scaffold.
- **Decision:** Execute 12-seed pilot; bound Y = C_δ·ε·√n + C_κ·κ; all PASS → HYP-001 accepted on toy domain only.
- **Rationale:** Falsify criteria met; real-domain pin deferred.
- **Consequences:** In Progress slot cleared; user chooses HYP-002 or real-domain rerun.
- **Links:** `v20260706-2500-run1`, `work/runs/toy_bound_pilot.py`, `work/runs/RUN-001_HYP-001_bound.md`

### DEC-20260706-005: Cross-AI handoff + sync build trial
- **Date:** 2026-07-06
- **Status:** accepted
- **Context:** External AI tests resume and sync-build RUN-001.
- **Decision:** Add `work/HANDOFF_SYNC_BUILD.md`; expand RESUME_INSTRUCTIONS; Exp-handoff-01 started.
- **Rationale:** Reuse handoff test protocol on a real hypothesis workspace.
- **Links:** `v20260706-2400-sync`

### DEC-20260706-004: Two hypotheses — test HYP-001 before HYP-002
- **Date:** 2026-07-06
- **Status:** accepted
- **Decision:** HYP-001 = bound test first; HYP-002 = layer comparison queued (Z default 10%).
- **Links:** `work/hypotheses/HYP-001.md`, `work/hypotheses/HYP-002.md`

### DEC-20260706-003: Charter hypothesis sandbox
- **Date:** 2026-07-06
- **Status:** accepted
- **Decision:** Workspace for formula + architecture experiments under `work/`.
- **Links:** `v20260706-2300-hyp`, `work/hypotheses/`

### DEC-20260706-002: Pause side project
- **Date:** 2026-07-06
- **Status:** accepted
- **Decision:** Do not maintain a paused side project from this workspace.
- **Links:** (private — not named in public example)

### DEC-20260706-001: Independent workspace
- **Date:** 2026-07-06
- **Status:** accepted
- **Decision:** Task workspace separate from format repo.
- **Links:** `v20260706-2200-init`