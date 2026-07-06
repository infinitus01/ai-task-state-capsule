# Resume Instructions

Copy the block below into a **new AI session** to resume this task with minimal context loss.

---

## Resume Prompt (copy from here)

```text
You are resuming a long-running AI task from a Task State Capsule.

Task / Project:
Version Hash:
Branch:
Capsule location (path or ZIP):

Instructions:
1. Read TASK_STATUS_REPORT.md — especially sections 2 (status), 4 (next actions), and 5 (compressed summary).
2. Read DECISION_LOG.md for accepted decisions; do not reverse them without explicit user approval.
3. Read BRANCH_INFO.md to understand the current branch and any active experiments.
4. Confirm Git tag exists when applicable: git tag -l capsule/[VERSION_HASH]
5. Confirm RECOVERY_CHECK.md items if the previous session ended abruptly or drifted.
6. Continue from "Next Actions" in TASK_STATUS_REPORT.md unless the user redirects.

First response MUST:
- State version hash and branch explicitly
- Summarize current stage in 3–5 sentences
- Cite Priority Action 1 verbatim
- Ask what the user wants next (do not start large work unprompted)

Constraints:
- Do not redo completed work listed under Done unless asked.
- Treat blockers as hard stops until resolved or user overrides.
- Update the capsule files when you make material progress.

Resume this task from version [VERSION_HASH].
```

---

## Optional Attachments

When pasting the prompt, also attach or paste:

- [ ] `TASK_STATUS_REPORT.md`
- [ ] `DECISION_LOG.md`
- [ ] `BRANCH_INFO.md`
- [ ] `STATE_MANIFEST.json`

## After Resume

The AI should:

1. Acknowledge version hash and branch
2. Summarize current stage in 3–5 sentences
3. Propose the next concrete action from Priority Action 1