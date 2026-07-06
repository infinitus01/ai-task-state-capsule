# Resume Instructions

## Resume Prompt (copy from here)

```text
You are resuming a long-running TWSE research task from a Task State Capsule.

Task / Project: TWSE Plus-3 A/B research + C-track adapter
Version Hash: v20260705-1200-twse
Branch: main
Related repo: C:\Users\Ming\Downloads\TEST001\twse_daytrade
Capsule role: research-state handoff only — NOT trading instructions

Current mode:
research-collection / adapter-dry-run
NOT trade-release
NOT intraday decision authority

Read first:
1. TASK_STATUS_REPORT.md sections 2, 4, 5
2. DECISION_LOG.md accepted entries
3. BRANCH_INFO.md

Hard constraints (accepted decisions):
- plus3_scalp_baseline = null
- plus3_confirmation_baseline = null
- virtual trade must remain disabled (no_positive_baseline)
- gate_level A/B = candidate quality labels, NOT trade signals
- C-track = read-only post-close audit adapter only
- Do NOT integrate C-track into background_loop, broker, order_router, or gate logic
- Do NOT INSERT/UPDATE/DELETE market_data.db
- Canonical export percentages must be ratio (0.03 not 3.0)

Continue from Priority Action 1 unless user redirects.

Resume this task from version v20260705-1200-twse.
```

## Attach with prompt

- [x] `TASK_STATUS_REPORT.md`
- [x] `DECISION_LOG.md`
- [ ] Latest `research_results/plus3_*_baseline.json` (if changed)
- [ ] Latest dry-run export dir (if exists)