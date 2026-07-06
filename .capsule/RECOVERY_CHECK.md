# Recovery Check

Pilot instance — same rules as `templates/RECOVERY_CHECK.md`, paths relative to `.capsule/`.

## Quick pilot checks

- [ ] AI still working on **ai-task-state-capsule** maintenance, not unrelated domains
- [ ] `version_hash` matches intended Git tag `capsule/<hash>`
- [ ] `git status` matches Done section (files exist at HEAD)
- [ ] No accepted decision in `DECISION_LOG.md` was reversed silently

## Fix

1. `git checkout capsule/v20260706-1200-caps` (or latest `capsule/*` tag)
2. Restore `.capsule/` from that commit if needed
3. New session → paste `RESUME_INSTRUCTIONS.md` only

See `docs/GIT_CAPSULE_ALIGNMENT.md` for full procedure.