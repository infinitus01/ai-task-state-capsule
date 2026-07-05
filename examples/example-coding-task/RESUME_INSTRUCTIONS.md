# Resume Instructions

## Resume Prompt (copy from here)

```text
You are resuming a long-running AI task from a Task State Capsule.

Task / Project: Context Relay v0.1 local sidecar planning
Version Hash: v20260705-1430-a1b2
Branch: main
Capsule location: examples/example-coding-task/

Instructions:
1. Read TASK_STATUS_REPORT.md — especially sections 2 (status), 4 (next actions), and 5 (compressed summary).
2. Read DECISION_LOG.md for accepted decisions; do not reverse them without explicit user approval.
3. Read BRANCH_INFO.md to understand the current branch and any active experiments.
4. Confirm RECOVERY_CHECK.md items if the previous session ended abruptly or drifted.
5. Continue from "Next Actions" in TASK_STATUS_REPORT.md unless the user redirects.

Constraints:
- Do not redo completed work listed under Done unless asked.
- Treat blockers as hard stops until resolved or user overrides.
- Update the capsule files when you make material progress.
- Do not build Chrome/VS Code extensions or cloud sync — out of scope for v0.1.

Resume this task from version v20260705-1430-a1b2.
```

## Optional Attachments

- [x] `TASK_STATUS_REPORT.md`
- [x] `DECISION_LOG.md`
- [x] `BRANCH_INFO.md`
- [x] `STATE_MANIFEST.json`