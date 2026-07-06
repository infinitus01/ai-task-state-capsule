# Branch and Rollback

For Git + capsule alignment (tags, commits, dual rollback): [`GIT_CAPSULE_ALIGNMENT.md`](GIT_CAPSULE_ALIGNMENT.md) · [中文](GIT_CAPSULE_ALIGNMENT.zh.md)

## Mental Model

A capsule branch is a **named snapshot lineage**, not necessarily a Git branch. You may mirror names in Git for convenience.

## Branch Types

### main
Canonical task state. Only one `main` should be "current" at a time.

### experiment/<name>
For trying alternate approaches without polluting `main`.

**Workflow:**
1. Copy capsule files to experiment folder or Git branch
2. Update `BRANCH_INFO.md` and manifest `branch`
3. Log intent in `DECISION_LOG.md` (status: proposed)
4. On success → merge learnings to `main`; on failure → abandon with log entry

### rollback/<version-hash>
Frozen copy before a risky change.

**Workflow:**
1. Seal ZIP at current `version_hash`
2. Create rollback branch name: `rollback/v20260705-1430-a1b2`
3. Store ZIP or Git tag pointing to that hash
4. Proceed with risky work on `main` or `experiment/*`

### review/<name>
Checkpoint for human or AI review before continuing.

## Rollback Procedure

1. Stop active AI session
2. Run `RECOVERY_CHECK.md`
3. Restore files from rollback ZIP or Git checkout
4. Set manifest `version_hash` and `branch` to restored values
5. Paste `RESUME_INSTRUCTIONS.md` with restored hash
6. Log rollback in `DECISION_LOG.md` (superseded entries as needed)

## When to Rollback

- AI reversed accepted decisions
- Done section no longer matches repo reality
- Experiment branch merged prematurely
- User requests return to last known good state