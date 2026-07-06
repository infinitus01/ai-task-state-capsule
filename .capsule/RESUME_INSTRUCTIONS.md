# Resume Instructions

## Resume Prompt (copy from here)

```text
You are resuming a long-running AI task from a Task State Capsule.

Task / Project: ai-task-state-capsule (GitHub template + pilot)
Version Hash: v20260706-1400-hand
Branch: main
Capsule location: C:\Users\Ming\ai-task-state-capsule\.capsule\

Instructions:
1. Read TASK_STATUS_REPORT.md — sections 2 (status), 4 (next actions), 5 (summary).
2. Read DECISION_LOG.md — do not reverse accepted decisions without user approval.
3. Read BRANCH_INFO.md — stay on main unless user opens an experiment.
4. Confirm Git tag exists: git tag -l capsule/v20260706-1400-hand
5. If context feels wrong, run RECOVERY_CHECK.md and align Git tag capsule/<version_hash>.

Constraints:
- Pilot scope: this repo only; do not mandate capsules on other user projects.
- Do not redo Done items unless asked.
- Update .capsule/ after material progress; commit with capsule hash in message.
- Capsule hash is not semver — release tags (v0.1.x) are separate.

Resume this task from version v20260706-1400-hand.
```

## Optional Attachments

- [ ] `.capsule/TASK_STATUS_REPORT.md`
- [ ] `.capsule/DECISION_LOG.md`
- [ ] `.capsule/BRANCH_INFO.md`
- [ ] `.capsule/STATE_MANIFEST.json`