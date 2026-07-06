# Resume Instructions

## Resume Prompt (copy from here)

```text
You are resuming a long-running AI task from a Task State Capsule.

Task / Project: ai-task-state-capsule (GitHub template + pilot)
Version Hash: v20260706-2000-t2p
Branch: main
Capsule location: C:\Users\Ming\ai-task-state-capsule\.capsule\

Instructions:
1. Read TASK_STATUS_REPORT.md — sections 2, 4, 5.
2. Read DECISION_LOG.md — accepted decisions are binding.
3. Confirm: python scripts/verify_capsule.py --check-git-tag

First response MUST: state hash + branch, 3–5 sentence summary, cite Priority Action 1, ask next step.

Constraints: pilot complete on this repo; no v0.1.5 unless requested; no scope expansion.

Resume this task from version v20260706-2000-t2p.
```