# Handoff: other AI — test resume + sync build

## Workspace
`<your-task-workspace>` (copy from `examples/handoff-pilot-hypothesis/`)

## Phase 1 — Cold resume (T1)
1. Read `.capsule/` six files + `work/hypotheses/HYP-001.md`, `HYP-002.md`
2. Run: `python scripts/verify_capsule.py --capsule-dir .capsule` (add `--check-git-tag --repo .` if using git)
3. First reply: hash, branch, 3–5 sentence summary, **verbatim Priority Action 1**, ask user

## Phase 2 — Sync build (after user confirms or says run toy)
Allowed writes **only under this workspace**:

| Path | Allowed |
|------|---------|
| `work/runs/` | toy script, results, RUN-*.md |
| `work/hypotheses/` | status, numeric results if derived |
| `work/arch/` | arch notes |
| `.capsule/` | after milestone — all six files |

Forbidden without user approval:
- Promote queued hypothesis while another is In Progress
- Mark hypothesis **accepted** without RUN evidence
- Edit the format repo from this workspace

## PASS rubric (handoff)
- Correct capsule hash in first message
- Cites correct sole In Progress hypothesis (or none if cleared)
- Does not leak paused side projects as active work
- Sync build stays in `work/` + `.capsule/` only