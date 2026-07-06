# Handoff pilot — architecture & formula hypothesis (sanitized)

Public, **de-identified** snapshot of a real cross-AI handoff trial. No API keys, no real domain data, no local machine paths.

- **Tip hash:** `v20260706-2700-run2` — HYP-001 and HYP-002 accepted on toy domain
- **Rollback checkpoint:** `checkpoints/v20260706-2500-run1/` — HYP-001 only; HYP-002 queued

## Layout

```text
handoff-pilot-hypothesis/
├── .capsule/              # six capsule files (tip)
├── work/                  # hypotheses, runs, arch sketches
├── checkpoints/           # frozen earlier states for T2 rollback demo
├── PILOT_EVIDENCE.md      # reproduce T1 / T2 / verify
└── README.md
```

## Verify capsule consistency (no git tag)

From the **format repo root**:

```bash
python scripts/verify_capsule.py --capsule-dir examples/handoff-pilot-hypothesis/.capsule
```

## Copy to a private local workspace

```bash
cp -r examples/handoff-pilot-hypothesis/ ~/my-task-workspace/
cd ~/my-task-workspace
git init
git add .capsule/ work/
git commit -m "chore: bootstrap from handoff-pilot example"
git tag -a capsule/v20260706-2700-run2 -m "Tip checkpoint"
python /path/to/ai-task-state-capsule/scripts/verify_capsule.py --capsule-dir .capsule --check-git-tag --repo .
```

Then continue your real task locally; do not push private work unless you sanitize again.

## What this demonstrates

| Trial | Evidence in this folder |
|-------|-------------------------|
| T1 cold handoff | `.capsule/RESUME_INSTRUCTIONS.md` + attachments list |
| Sync build | `work/runs/toy_bound_pilot.py`, `toy_layers_pilot.py`, RUN logs |
| T2 rollback | Compare `checkpoints/v20260706-2500-run1/` vs tip — no RUN-002 / HYP-002 accepted at old hash |
| Capsule verify | `scripts/verify_capsule.py` PASS on `.capsule/` |

See [PILOT_EVIDENCE.md](PILOT_EVIDENCE.md) for step-by-step reproduction.