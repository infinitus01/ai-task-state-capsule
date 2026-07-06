# Examples

## `example-coding-task/`

Generic capsule for a multi-day coding / planning task (Context Relay v0.1 planning).

Use when you want a **neutral template** without domain-specific gates.

## `handoff-pilot-hypothesis/`

**Public sanitized** cross-AI handoff demo (no secrets, no local paths):

- Full workspace layout: `.capsule/` + `work/` (toy pilots RUN-001 / RUN-002)
- `PILOT_EVIDENCE.md` — reproduce T1 cold handoff, T2 rollback, `verify_capsule.py`
- `checkpoints/v20260706-2500-run1/` — frozen earlier hash for rollback drill

Use when you want **auditable proof** that capsule handoff and rollback work. Copy to a private workspace for real tasks.

## `example-twse-research/`

Research-state capsule modeled on a real long-running quant workflow:

- A/B tracks collecting data
- `baseline = null` → virtual trade correctly disabled
- C-track as **read-only post-close audit adapter**, not main-loop integration
- Explicit recovery rules against trading / gate / percent-unit drift

Use when your task is **research or audit mode**, not release mode.

## Copy an example

```bash
cp -r examples/example-twse-research/ ../twse_daytrade/.capsule/
```

Then update version hash, dates, and file paths to match your machine.