# Resume Instructions — copy to other AI

## Resume Prompt

```text
You are resuming a Task State Capsule workspace.

Task: Architecture & Formula Hypothesis Pilot
Version Hash: v20260706-2700-run2
Branch: main
Workspace: <your-task-workspace>
Capsule: .capsule/
Artifacts: work/

READ FIRST:
- .capsule/TASK_STATUS_REPORT.md (§2, §4, §5)
- .capsule/DECISION_LOG.md
- work/hypotheses/HYP-001.md (accepted toy), HYP-002.md (accepted toy)
- work/runs/RUN-002_HYP-002_layers.md (complete)

VERIFY (from format repo root):
python scripts/verify_capsule.py --capsule-dir examples/handoff-pilot-hypothesis/.capsule

VERIFY (if copied to private git workspace):
python scripts/verify_capsule.py --capsule-dir .capsule --check-git-tag --repo .

First response MUST:
1. State version hash + branch
2. Summarize stage in 3–5 sentences
3. Quote Priority Action 1 verbatim
4. Confirm no hypothesis In Progress (awaiting user choice)
5. Ask: start next phase, or pin real x,y,f for HYP-001 or HYP-002?

Constraints:
- One In Progress only — log pivots in DECISION_LOG
- No accepted without falsify run
- paused side project — do not treat as active work
- No edits outside this workspace

Resume this task from version v20260706-2700-run2.
```

## Attach these files
- `.capsule/TASK_STATUS_REPORT.md`
- `.capsule/DECISION_LOG.md`
- `.capsule/STATE_MANIFEST.json`
- `work/hypotheses/HYP-002.md`
- `work/runs/RUN-002_HYP-002_layers.md`