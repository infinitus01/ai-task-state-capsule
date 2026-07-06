# ARCH-001: Pipeline sketches for HYP-001 / HYP-002

## Single-layer (HYP-002 baseline S)

```text
x ──► [ G ] ──► ŷ
         │
         └── error e_S = |y − ŷ|
```

## Two-layer (HYP-002 A/B)

```text
x ──► [ A ] ──► z ──► [ B ] ──► ŷ
              │              │
              └── e_A        └── e_AB = |y − ŷ|
```

## Architecture A for bound test (HYP-001)

```text
x ──► [ P precondition ] ──► [ X core formula ] ──► [ Q post-check ] ──► ŷ
              κ                      f
```

## Comparison rule (fair test)
- Same input distribution for S vs A/B
- Same compute budget or explicit budget table in RUN log
- Report max error, p95, and bound violation count