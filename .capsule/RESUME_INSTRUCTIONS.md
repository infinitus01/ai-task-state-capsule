# Resume Instructions

## Resume Prompt (copy from here)

```text
You are resuming a long-running AI task from a Task State Capsule.

Task / Project: ai-task-state-capsule (GitHub template + pilot)
Version Hash: v20260706-1600-flow
Branch: main
Capsule location: C:\Users\Ming\ai-task-state-capsule\.capsule\
Repo: https://github.com/infinitus01/ai-task-state-capsule

Instructions:
1. Read TASK_STATUS_REPORT.md — sections 2, 4, 5.
2. Read DECISION_LOG.md — do not reverse accepted decisions without user approval.
3. Read BRANCH_INFO.md — stay on main unless I open an experiment.
4. Confirm Git tag: git tag -l capsule/v20260706-1600-flow
5. If context feels wrong, run RECOVERY_CHECK.md.

First response MUST:
- State version hash and branch explicitly
- Summarize current stage in 3–5 sentences
- Cite Priority Action 1 verbatim
- Ask what I want next (do not start large work unprompted)

Constraints:
- Pilot scope: this repo only.
- Do not redo Done items unless I ask.
- Do not start v0.1.5 / JSON Schema unless I explicitly request.
- Update .capsule/ after material progress; verify with: python scripts/verify_capsule.py --check-git-tag

Resume this task from version v20260706-1600-flow.
```

## Optional Attachments

- [ ] `.capsule/TASK_STATUS_REPORT.md`
- [ ] `.capsule/DECISION_LOG.md`
- [ ] `.capsule/BRANCH_INFO.md`
- [ ] `.capsule/STATE_MANIFEST.json`