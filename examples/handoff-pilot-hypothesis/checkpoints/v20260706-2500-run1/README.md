# Checkpoint: v20260706-2500-run1

Frozen state **before** HYP-002 started. Use for T2 rollback drill.

- HYP-001: accepted (toy)
- HYP-002: proposed (queued)
- No RUN-002, no `toy_layers_pilot.py` results

Verify:

```bash
python scripts/verify_capsule.py --capsule-dir examples/handoff-pilot-hypothesis/checkpoints/v20260706-2500-run1/.capsule
```