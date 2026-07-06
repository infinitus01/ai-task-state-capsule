# AI Resume Protocol

Standard procedure for handing a long task to a new AI session.

## Prerequisites

- Capsule files are up to date (especially `TASK_STATUS_REPORT.md`)
- `version_hash` is consistent across report, manifest, and resume block
- Local check: `python scripts/verify_capsule.py --capsule-dir <path>`
- With Git: `python scripts/verify_capsule.py --check-git-tag`
- Optional: sealed ZIP for integrity reference

Pilot test script: [`HANDOFF_TEST_PROTOCOL.md`](HANDOFF_TEST_PROTOCOL.md) · [中文](HANDOFF_TEST_PROTOCOL.zh.md)

## Steps

### 1. Human prepares handoff

1. Update Done / In Progress / Todo in status report
2. Write compressed summary (150–250 words)
3. Set Priority Action 1 and 2
4. Seal ZIP if milestone reached: `python scripts/generate_capsule_zip.py --source <capsule-dir>`

### 2. Human opens new AI session

Paste contents of `RESUME_INSTRUCTIONS.md` (the fenced block).

Attach or paste:
- `TASK_STATUS_REPORT.md`
- `DECISION_LOG.md` (if decisions matter)
- `BRANCH_INFO.md` (if on experiment branch)

### 3. AI acknowledges

The AI should respond with:
- Confirmed version hash and branch
- 3–5 sentence stage summary
- Proposed first action from Priority Action 1

### 4. AI continues work

- Follow accepted decisions in `DECISION_LOG.md`
- Do not redo Done items
- Update capsule files after material progress

### 5. Session end

Before closing:
- Refresh status classifications
- Update compressed summary if stage changed
- Note blockers and next actions

## Failure Modes

| Symptom | Action |
|---------|--------|
| AI ignores version hash | Re-paste resume block; attach manifest |
| AI mixes tasks | Run `RECOVERY_CHECK.md` section 1 |
| AI reverses decisions | Run recovery section 4; cite DEC entries |
| Context too large | Send only report + manifest + relevant DEC entries |

## Optional: Minimal Handoff

For token-limited sessions, send only:
1. Resume prompt block
2. Section 5 (compressed summary)
3. Section 4 (next actions)
4. Accepted decisions list from `DECISION_LOG.md`