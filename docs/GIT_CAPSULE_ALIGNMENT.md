# Git + Capsule Alignment

How to keep **code state** (Git) and **task state** (capsule) on the same timeline.

> Capsule rollback resets what the AI should believe. Git rollback resets what is on disk. Use both together.

---

## Why align at all

| Layer | Answers |
|-------|---------|
| **Git** | Which files changed, at which commit |
| **Capsule** | Task progress, decisions, next steps, boundaries |
| **Both aligned** | AI resumes from the correct narrative **and** the repo matches that narrative |

If only the capsule is restored, the AI may describe work that no longer exists in the repo — or miss changes that are still on disk.

---

## Recommended layout

```text
your-repo/
├── .capsule/                    # or my-project-capsule/ at repo root
│   ├── TASK_STATUS_REPORT.md
│   ├── DECISION_LOG.md
│   ├── BRANCH_INFO.md
│   ├── RESUME_INSTRUCTIONS.md
│   ├── RECOVERY_CHECK.md
│   └── STATE_MANIFEST.json
├── src/
└── ...
```

Commit capsule files in the **same repo** as the code when the task is code-adjacent. For research-only work with no repo, a sibling capsule folder + ZIP is enough.

---

## Naming alignment

Mirror capsule branch names in Git when practical:

| Capsule `branch` (manifest) | Git equivalent |
|----------------------------|----------------|
| `main` | `main` / `master` |
| `experiment/<name>` | `experiment/<name>` or `git checkout -b experiment/<name>` |
| `rollback/<version-hash>` | Git tag: `capsule/<version-hash>` |
| `review/<name>` | Optional branch or tag before merge |

Example tag at a known-good milestone:

```bash
git tag -a capsule/v20260706-1200-a1b2 -m "Capsule rollback point before risky refactor"
```

Record the same hash in `STATE_MANIFEST.json` → `version_hash` and `BRANCH_INFO.md`.

---

## Checkpoint workflow (happy path)

At each milestone:

1. **Finish the work slice** (code, docs, tests as applicable)
2. **Update all six capsule files** — especially `version_hash`, `branch`, Done / Todo
3. **Commit code + capsule together** (preferred) or back-to-back commits with linked message:

```bash
git add .capsule/ src/
git commit -m "feat: parser milestone — capsule v20260706-1200-a1b2"
```

4. **Optional:** seal a ZIP for audit / offline handoff (`python scripts/generate_capsule_zip.py`)
5. **Before risky work:** tag `capsule/<version-hash>` on current HEAD

---

## Rollback workflow (when AI or work drifts)

1. **Stop** the active AI session
2. Run [`RECOVERY_CHECK.md`](../templates/RECOVERY_CHECK.md)
3. Identify last known-good **`version_hash`** from manifest or Git tag
4. **Restore Git:**

```bash
git checkout capsule/v20260706-1200-a1b2
# or: git checkout main && git reset --hard <commit-sha>
```

5. **Restore capsule** (if not already at that commit):

```bash
git checkout capsule/v20260706-1200-a1b2 -- .capsule/
```

6. Set manifest `branch` to `main` or `rollback/<version-hash>` as appropriate
7. Log rollback in `DECISION_LOG.md` (supersede bad decisions)
8. **New AI session:** paste `RESUME_INSTRUCTIONS.md` only from the restored capsule

---

## Experiment branch workflow

```text
main ──► experiment/new-api
              │
              ├─ success → merge to main, update capsule on main
              └─ failure → checkout main, abandon experiment in DECISION_LOG
```

Git:

```bash
git checkout -b experiment/new-api
# work + update capsule (manifest branch = experiment/new-api)
```

On abandon:

```bash
git checkout main
# capsule: mark experiment rejected; restore main branch name in manifest
```

Do not delete `rollback/<hash>` tags — they are your safety net.

---

## Commit message convention (optional)

Link Git commits to capsule hashes for searchability:

```text
feat: add export adapter (capsule v20260706-1430-b2c3)
docs: update TASK_STATUS_REPORT (capsule v20260706-1500-c4d5)
rollback: restore to capsule v20260706-1200-a1b2
```

---

## Recovery checklist additions

When running recovery, verify **both** layers:

- [ ] `git status` is clean or intentionally dirty (documented in blockers)
- [ ] Files listed under **Done** in `TASK_STATUS_REPORT.md` exist at current HEAD
- [ ] `version_hash` in manifest matches the tag or commit you intend to resume from
- [ ] `RESUME_INSTRUCTIONS.md` was generated for that same hash — not a newer draft

---

## What this does not do

- Git does not auto-update the capsule — you still edit the six files
- Capsule does not auto-run `git checkout` — a human or scripted step does
- Tags are not a substitute for sealed audit ZIPs when you need SHA-256 evidence chains

---

## See also

- [`BRANCH_AND_ROLLBACK.md`](BRANCH_AND_ROLLBACK.md) — branch mental model
- [`AI_RESUME_PROTOCOL.md`](AI_RESUME_PROTOCOL.md) — cross-session resume
- [`RECOVERY_CHECK.md`](../templates/RECOVERY_CHECK.md) — drift recovery template