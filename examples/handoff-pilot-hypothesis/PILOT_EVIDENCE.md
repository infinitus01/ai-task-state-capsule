# Pilot evidence — handoff & rollback (public, sanitized)

Recorded: 2026-07-06  
Example tip hash: `v20260706-2700-run2`  
Rollback checkpoint: `v20260706-2500-run1`

This document lets a third party verify the **Task State Capsule** handoff workflow without access to any private workspace.

---

## 1. Capsule consistency (anyone)

From the `ai-task-state-capsule` repo root:

```bash
python scripts/verify_capsule.py --capsule-dir examples/handoff-pilot-hypothesis/.capsule
```

**PASS criteria:** single `version_hash` across manifest, report §6, and resume block.

Rollback checkpoint:

```bash
python scripts/verify_capsule.py --capsule-dir examples/handoff-pilot-hypothesis/checkpoints/v20260706-2500-run1/.capsule
```

**PASS criteria:** hash `v20260706-2500-run1`; no reference to RUN-002 completion in that report's Done section.

---

## 2. T1 — Cold handoff (reproduce)

1. Open a **new** AI chat (no prior history).
2. Paste the fenced block from `examples/handoff-pilot-hypothesis/.capsule/RESUME_INSTRUCTIONS.md`.
3. Attach:
   - `.capsule/TASK_STATUS_REPORT.md`
   - `.capsule/DECISION_LOG.md`
   - `.capsule/STATE_MANIFEST.json`
   - `work/hypotheses/HYP-002.md`
   - `work/runs/RUN-002_HYP-002_layers.md`
4. **Expected first reply:**
   - States hash `v20260706-2700-run2`, branch `main`
   - Quotes Priority Action 1 verbatim from report §4
   - Confirms **no** hypothesis In Progress
   - Does not treat paused side projects as active work

| # | Criterion | PASS |
|---|-----------|------|
| 1 | Correct `version_hash` | |
| 2 | Correct `branch` | |
| 3 | 3–5 sentence summary matches §2/§5 | |
| 4 | Priority Action 1 quoted | |
| 5 | No scope creep | |
| 6 | Asks or waits for direction | |

---

## 3. T2 — Rollback drill (reproduce)

1. Use files under `checkpoints/v20260706-2500-run1/` only (not tip).
2. Paste that checkpoint's `RESUME_INSTRUCTIONS.md` to a new AI session.
3. **Expected:**
   - AI cites hash `v20260706-2500-run1`
   - HYP-001 accepted (toy); HYP-002 **proposed**, not accepted
   - No `toy_layers_pilot.py`, no RUN-002 results
   - Priority Action 1: choose HYP-002 or pin real x,y,f

**FAIL if** AI mentions HYP-002 accepted, RUN-002 PASS, or hash `v20260706-2700-run2`.

---

## 4. Sync build (already recorded in tip)

Scripts are runnable without secrets:

```bash
python examples/handoff-pilot-hypothesis/work/runs/toy_bound_pilot.py
python examples/handoff-pilot-hypothesis/work/runs/toy_layers_pilot.py
```

| Run | Result |
|-----|--------|
| RUN-001 | 12/12 PASS — bound Y held |
| RUN-002 | 6/6 PASS — Δ ≈ 14.84% ≥ Z=10% |

---

## 5. Git tag alignment (optional, local)

The format repo example is **not** a git repo with tags. To test `--check-git-tag`:

1. Copy this folder to `~/my-task-workspace/`
2. `git init`, commit, tag `capsule/v20260706-2700-run2`
3. Run:

```bash
python scripts/verify_capsule.py --capsule-dir .capsule --check-git-tag --repo .
```

---

## 6. What is intentionally absent

- Windows user paths (`C:\Users\...`)
- Private project names (replaced with "paused side project")
- API keys, tokens, real datasets
- Links to unreleased repositories

The live workspace that produced this example remains **local and private**.