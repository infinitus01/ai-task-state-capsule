# RUN-001: HYP-001 error bound — pilot

**Status:** executed (toy domain)  
**Hypothesis:** HYP-001  
**Capsule:** v20260706-2500-run1  
**Script:** `work/runs/toy_bound_pilot.py`

## Pinned domain (toy)
| Slot | Value |
|------|-------|
| What is `x` / `y`? | x ∈ R^n ~ N(0, ε²I/n); y = (I + δ_true M_true) x |
| What is `f` in formula X? | f(P(x)) = (I + δ M) P(x); P scales x by 1/(1+α‖x‖) |
| Initial Y(ε, n, κ) | Y = C_δ · ε · √n + C_κ · κ |
| ε, n, κ | ε=1.0, n=8, κ measured per seed |

Coefficients (fixed matrices): C_δ = 0.3444, C_κ = 1.1179

## Results
| seed | max error | Y bound | PASS/FAIL |
|------|-----------|---------|-----------|
| 0 | 0.1549 | 1.0404 | PASS |
| 1 | 0.1003 | 1.0545 | PASS |
| 2 | 0.3668 | 1.1817 | PASS |
| 3 | 0.3882 | 1.2442 | PASS |
| 4 | 0.2257 | 1.0988 | PASS |
| 5 | 0.1166 | 1.0654 | PASS |
| 6 | 0.2945 | 1.2561 | PASS |
| 7 | 0.0910 | 1.0491 | PASS |
| 8 | 0.2090 | 1.2172 | PASS |
| 9 | 0.1179 | 1.0792 | PASS |
| 10 | 0.1942 | 1.0491 | PASS |
| 11 | 0.0900 | 1.0555 | PASS |

**Summary:** max observed error 0.3882 ≤ max bound 1.2561; 0/12 failures.

## Verdict
- [x] PASS bound held
- [ ] FAIL bound violated → REJECT or revise Y
- [ ] PAUSE need domain pin from user

**HYP-001 (toy domain): accepted** — bound Y held on all 12 seeds. Real-domain pin still needed before production claim.