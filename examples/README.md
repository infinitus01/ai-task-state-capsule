# Examples

## `example-coding-task/`

Generic capsule for a multi-day coding / planning task (Context Relay v0.1 planning).

Use when you want a **neutral template** without domain-specific gates.

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