# ai-task-state-capsule

A lightweight, local-first task state capsule format for long-running AI workflows.

## Problem

Long AI coding and research tasks accumulate state in chat history. That state is:

- Hard to version or diff
- Fragile when sessions expire or context windows fill
- Difficult to hand off to another AI session or human
- Easy to lose when the model drifts or branches fail

This project provides a **structured, file-based capsule** you can commit to Git, branch, zip, and resume.

## What is an AI Task State Capsule?

An AI Task State Capsule is a small set of markdown and JSON files that compress the essential state of a long-running task:

| File | Purpose |
|------|---------|
| `TASK_STATUS_REPORT.md` | Progress, blockers, next actions, compressed summary |
| `DECISION_LOG.md` | Decisions, rationale, alternatives, status |
| `BRANCH_INFO.md` | Branch naming and lineage for experiments / rollbacks |
| `RESUME_INSTRUCTIONS.md` | Copy-paste prompt for the next AI session |
| `RECOVERY_CHECK.md` | Checklist when the task has drifted or failed |
| `STATE_MANIFEST.json` | Machine-readable metadata and file index |

The capsule is **not** a chat export. It is a **curated snapshot** optimized for resumption and audit.

## Use Cases

- Multi-day coding tasks across Codex, Claude Code, Grok, Cursor, or Antigravity
- Research tasks that need decision trails and experiment notes
- Prototype work where you branch ideas and may need rollback
- Handing off from one AI session to another with minimal context loss
- Local version control alongside your code repo (or as a sibling directory)

## Quick Start

1. Copy `templates/` into your task directory (or use an example as reference):

   ```bash
   cp -r templates/ my-task-capsule/
   ```

2. Fill in `TASK_STATUS_REPORT.md` and `STATE_MANIFEST.json` as you work.

3. Commit the capsule to Git when you reach a stable checkpoint.

4. When resuming, paste the contents of `RESUME_INSTRUCTIONS.md` into a new AI session.

5. If the AI drifts, run through `RECOVERY_CHECK.md` before continuing.

See `examples/example-coding-task/` for a filled-in sample.

## Release (v0.1.2)

Audit archives use **external sealing**:

```text
dist/ai-task-state-capsule-work-audit-v....zip
dist/ai-task-state-capsule-work-audit-v....zip.sha256
dist/ai-task-state-capsule-work-audit-v....sealed.json   # external .sealed.json
```

The audit ZIP itself does not record its final SHA-256.

## Release (v0.1.1)

```bash
python scripts/patch_release.py
```

Produces source ZIP, capsule ZIP, audit ZIP, and `audit/VERIFICATION_REPORT.md`.

## Generating a ZIP Capsule

From the project root:

```bash
python scripts/generate_capsule_zip.py --source templates
python scripts/generate_capsule_zip.py --source examples/example-coding-task
python scripts/generate_source_zip.py
python scripts/verify_zips.py
```

Output:

```text
Capsule ZIP:
Version Hash:
SHA-256:
Included Files:
```

ZIP filename format: `ai-task-state-capsule-vYYYYMMDD-HHMM-xxxx.zip`

## Version Hash

Each packaged capsule gets a version hash: `vYYYYMMDD-HHMM-xxxx`

- **Timestamp** (`YYYYMMDD-HHMM`): when the capsule was sealed
- **Short suffix** (`xxxx`): first 4 hex chars of SHA-256 over ZIP contents (or random fallback)

Use the hash to:

- Reference a specific checkpoint in `TASK_STATUS_REPORT.md` and `RESUME_INSTRUCTIONS.md`
- Chain versions via `previous_version_hash` in `STATE_MANIFEST.json`
- Verify integrity against the ZIP SHA-256

See `docs/VERSION_HASH_RULES.md` for details.

## Branching and Recovery

Treat capsule branches like lightweight Git branches:

- `main` — current canonical task state
- `experiment/<name>` — exploratory paths
- `rollback/<hash>` — frozen snapshot before a risky change
- `review/<name>` — human or AI review checkpoints

When an experiment fails, restore from `rollback/<hash>` or regenerate from a versioned ZIP.

See `docs/BRANCH_AND_ROLLBACK.md` and `docs/AI_RESUME_PROTOCOL.md`.

## What This Project Does Not Do

- HEA-specific or domain-locked workflows
- Cloud sync or hosted state services
- Clipboard monitoring or automatic chat capture
- Browser extensions, VS Code extensions, or sidecar daemons
- Financial compliance or enterprise platform narratives
- Replacing your code repository — it complements it

## Future Extensions

- JSON Schema validation for `STATE_MANIFEST.json`
- CLI to diff two capsule versions
- Optional encryption for sensitive task metadata
- Integration hooks (export from Cursor / Claude exports) as **optional** adapters, not core
- Template packs for research vs. coding vs. ops tasks

## License

MIT — see `LICENSE`.

## Documentation

- `docs/VERSION_HASH_RULES.md`
- `docs/BRANCH_AND_ROLLBACK.md`
- `docs/AI_RESUME_PROTOCOL.md`
- `docs/CUSTOMIZATION_GUIDE.md`