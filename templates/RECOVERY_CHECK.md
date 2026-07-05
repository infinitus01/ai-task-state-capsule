# Recovery Check

Use this checklist when the AI has drifted, mixed tasks, failed a branch, or lost track of progress.

## 1. Scope Drift

- [ ] Is the AI still working on the task named in `TASK_STATUS_REPORT.md`?
- [ ] Has it introduced unrelated features or domains not in Todo / In Progress?
- [ ] **Fix:** Re-paste `RESUME_INSTRUCTIONS.md` and attach the capsule files.

## 2. Version Integrity

- [ ] Does `Version Hash` in the report match `version_hash` in `STATE_MANIFEST.json`?
- [ ] Is `previous_version_hash` consistent with your last known good ZIP or Git commit?
- [ ] **Fix:** Restore from last `rollback/<hash>` or versioned ZIP; re-run recovery.

## 3. Branch Confusion

- [ ] Is work happening on the branch listed in `BRANCH_INFO.md`?
- [ ] Are experiment branches clearly marked in `DECISION_LOG.md`?
- [ ] **Fix:** Switch to `main` or the correct experiment branch; update manifest `branch` field.

## 4. Decision Contradictions

- [ ] Has the AI reversed an **accepted** decision without user approval?
- [ ] Are there conflicting entries in `DECISION_LOG.md` with status `accepted`?
- [ ] **Fix:** Mark superseded decisions; re-read accepted entries aloud to the AI.

## 5. Lost Progress

- [ ] Does the Done section still reflect reality (files, tests, deployed artifacts)?
- [ ] Are blockers still accurate?
- [ ] **Fix:** Diff against Git or last ZIP; rebuild `TASK_STATUS_REPORT.md` from artifacts.

## 6. Unsafe Continuation

- [ ] Are there unresolved blockers marked as hard stops?
- [ ] Was a risky change made without a `rollback/<hash>` snapshot?
- [ ] **Fix:** Stop work; create rollback snapshot; resolve blockers first.

## Recovery Outcome

After completing this checklist, record:

- **Recovery date:**
- **Restored from version hash:**
- **Branch after recovery:**
- **Notes:**