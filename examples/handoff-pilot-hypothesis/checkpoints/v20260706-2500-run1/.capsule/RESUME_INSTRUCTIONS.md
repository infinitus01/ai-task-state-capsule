# Resume Instructions — copy to other AI

## Resume Prompt

```text
You are resuming a Task State Capsule workspace.

Task: Architecture & Formula Hypothesis Pilot
Version Hash: v20260706-2500-run1
Branch: main
Workspace: <your-task-workspace>
Capsule: .capsule/
Artifacts: work/

READ FIRST:
- .capsule/TASK_STATUS_REPORT.md (§2, §4, §5)
- .capsule/DECISION_LOG.md
- work/hypotheses/HYP-001.md (accepted toy), HYP-002.md (queued)
- work/runs/RUN-001_HYP-001_bound.md (complete)

VERIFY:
python scripts/verify_capsule.py --capsule-dir examples/handoff-pilot-hypothesis/checkpoints/v20260706-2500-run1/.capsule

First response MUST:
1. State version hash + branch
2. Summarize stage in 3–5 sentences
3. Quote Priority Action 1 verbatim
4. Confirm no hypothesis In Progress (awaiting user choice)
5. Ask: start HYP-002, or pin real x,y,f?

Constraints:
- One In Progress only — log pivots in DECISION_LOG
- No accepted without falsify run
- paused side project — do not treat as active work

Resume this task from version v20260706-2500-run1.
```

## Attach these files
- `.capsule/TASK_STATUS_REPORT.md`
- `.capsule/DECISION_LOG.md`
- `.capsule/STATE_MANIFEST.json`
- `work/hypotheses/HYP-002.md`
- `work/runs/RUN-001_HYP-001_bound.md`