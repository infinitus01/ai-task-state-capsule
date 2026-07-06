# RUN-002: HYP-002 layers comparison — pilot

**Status:** executed (toy domain)  
**Hypothesis:** HYP-002  
**Capsule:** v20260706-2700-run2  
**Script:** `work/runs/toy_layers_pilot.py`

## Pinned domain (toy)
| Slot | Value |
|------|-------|
| Target `Z%` (reduction) | Z = 10.0% |
| Input `x` / Output `y` | x ∈ R^2 ~ N(0, I); y = cos(x_1^2 + x_2^2) |
| Single-layer `G_approx(x)` | G(x) = cos(x_1^2 + x_2^2) + η_G; η_G ~ N(0, σ_S^2) |
| Upstream layer `A_approx(x)` | A(x) = x_1^2 + x_2^2 + η_A; η_A ~ N(0, σ_A^2) |
| Downstream layer `B_approx(z)`| B(z) = cos(z) + η_B; η_B ~ N(0, σ_B^2) |
| Match Work Condition | Variance of total error matched: σ_S^2 = σ_A^2 + σ_B^2 |

## Results
| seed | e_S (Single-layer error) | e_AB (Two-layer error) | Δ (Reduction %) | PASS/FAIL (Δ ≥ 10%) |
|------|--------------------------|------------------------|-----------------|---------------------|
| 0 | 0.0796 | 0.0676 | 15.14% | PASS |
| 1 | 0.0783 | 0.0677 | 13.51% | PASS |
| 2 | 0.0804 | 0.0670 | 16.63% | PASS |
| 3 | 0.0787 | 0.0676 | 14.14% | PASS |
| 4 | 0.0801 | 0.0680 | 15.08% | PASS |
| 5 | 0.0785 | 0.0670 | 14.56% | PASS |

**Summary:** Mean single-layer MAE 0.0793, two-layer MAE 0.0675; mean error reduction Δ = 14.84% (all seeds ≥ 10%).

## Verdict
- [x] PASS Δ ≥ Z% on all seeds
- [ ] FAIL Δ < Z% on any seed
- [ ] PAUSE awaiting script implementation and execution

**HYP-002 (toy domain): accepted** — error reduction target of 10% was met on all 6 seeds.
