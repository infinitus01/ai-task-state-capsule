# Handoff Test Protocol

Repeatable pilot tests for capsule + Git alignment. Use during dogfood before copying `.capsule/` to another repo.

---

## Prerequisites

- Capsule directory exists (e.g. `.capsule/`)
- Git repo with at least one `capsule/<hash>` tag
- Local verifier:

```bash
python scripts/verify_capsule.py --check-git-tag
```

---

## Test matrix (3 runs)

| Test | Goal | Pass criteria |
|------|------|----------------|
| **T1 Cold handoff** | New AI resumes without chat history | See rubric below |
| **T2 Rollback drill** | Restore older checkpoint | Git + capsule match; AI cites old hash |
| **T3 Milestone roll** | Small change → new hash + tag | `verify_capsule.py` PASS; tag pushed |

Pilot complete when **T1 passes 2–3 times** (different tools optional) and **T3 done once**.

---

## T1 — Cold handoff

### Human steps

1. Open a **new** AI session (different tool optional).
2. Paste `RESUME_INSTRUCTIONS.md` fenced block.
3. Attach: `TASK_STATUS_REPORT.md`, `DECISION_LOG.md`, `BRANCH_INFO.md`, `STATE_MANIFEST.json`.
4. Do **not** paste prior chat history.

### AI first-response rubric

| # | Criterion | PASS |
|---|-----------|------|
| 1 | States `version_hash` exactly | Matches manifest |
| 2 | States `branch` | Matches manifest |
| 3 | Stage summary 3–5 sentences | Aligns with report §2 / §5 |
| 4 | Cites Priority Action 1 | From report §4 |
| 5 | No scope creep | No v0.1.5 / JSON Schema / other repos unless in Todo and user asked |
| 6 | Asks or waits for direction | Does not auto-start large work |

**PASS:** criteria 1–4 yes, 5 yes, 6 yes.  
**PARTIAL:** 1–4 yes but verbose re-explaining Done items.  
**FAIL:** wrong hash, wrong project, or unauthorized scope expansion.

### Record result

Add to `TASK_STATUS_REPORT.md` → Experiments / Tests, e.g.:

```text
T1 handoff — PASS — [tool name] — 2026-07-06
```

Roll capsule forward if milestone (see T3).

---

## T2 — Rollback drill

### Human steps

1. Note current hash `A` and previous hash `B`.
2. `git checkout capsule/B` (or `git show capsule/B:.capsule/`).
3. New AI session with **restored** `RESUME_INSTRUCTIONS.md` for hash `B`.
4. Confirm AI believes it is on hash `B`, not `A`.

### Pass criteria

- AI cites hash `B`
- Done section matches files at that Git commit
- No references to work that exists only in hash `A`

Return to tip: `git checkout main` and latest capsule.

---

## T3 — Milestone roll-forward

After doc/script change or recorded T1 PASS:

1. Update all six capsule files; bump `version_hash`, set `previous_version_hash`.
2. Run:

```bash
python scripts/verify_capsule.py --capsule-dir .capsule
git add .capsule/
git commit -m "chore: ... (capsule vYYYYMMDD-HHMM-xxxx)"
git tag -a capsule/vYYYYMMDD-HHMM-xxxx -m "Capsule checkpoint"
python scripts/verify_capsule.py --check-git-tag
git push origin master
git push origin capsule/vYYYYMMDD-HHMM-xxxx
```

### Pass criteria

- Verifier PASS with `--check-git-tag`
- `previous_version_hash` chain intact in manifest

---

## Failure → recovery

| Symptom | Action |
|---------|--------|
| Wrong hash in first reply | Re-paste resume block; attach manifest |
| AI redoes Done work | Cite Done list; run `RECOVERY_CHECK.md` §1 |
| Capsule / Git out of sync | `docs/GIT_CAPSULE_ALIGNMENT.md` rollback procedure |
| Verifier FAIL before handoff | Fix hash mismatch before testing |

---

## Pilot exit criteria

- [ ] T1 PASS × 2–3 (log in TASK_STATUS_REPORT)
- [ ] T2 rollback drill PASS × 1
- [ ] T3 milestone roll PASS × 2+ (hash chain ≥ 3 deep)
- [ ] `verify_capsule.py --check-git-tag` PASS on latest

Then consider copying `templates/` to a second repo.

See also: [`AI_RESUME_PROTOCOL.md`](AI_RESUME_PROTOCOL.md) · [`GIT_CAPSULE_ALIGNMENT.md`](GIT_CAPSULE_ALIGNMENT.md)