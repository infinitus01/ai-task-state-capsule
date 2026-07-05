# Branch Info

This capsule uses lightweight branch names to track parallel paths without requiring a full Git workflow for the capsule itself. You may mirror these names in Git tags or branches if helpful.

## Naming Rules

| Branch pattern | Purpose |
|----------------|---------|
| `main` | Canonical current state of the task |
| `experiment/<short-name>` | Exploratory work (e.g. `experiment/alternate-parser`) |
| `rollback/<version-hash>` | Frozen snapshot before a risky change (e.g. `rollback/v20260705-1430-a1b2`) |
| `review/<short-name>` | Checkpoint for human or AI review (e.g. `review/milestone-1`) |

## Current Branch

- **Name:**
- **Parent branch:**
- **Created at:**
- **Reason for branch:**

## Lineage

```text
main
 └── experiment/<name>   (optional)
 └── rollback/<hash>     (optional)
 └── review/<name>       (optional)
```

## Merge / Abandon Rules

- **Merge to main:** When experiment outcomes are validated and `TASK_STATUS_REPORT.md` is updated.
- **Abandon branch:** Mark status in `DECISION_LOG.md`; do not delete rollback snapshots.
- **Rollback:** Copy files from `rollback/<hash>` ZIP or Git tag; set `previous_version_hash` in manifest.

## Active Branches

| Branch | Status | Notes |
|--------|--------|-------|
| main | active | |