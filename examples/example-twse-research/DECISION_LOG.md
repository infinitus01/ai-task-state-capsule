# Decision Log

## Entries

### DEC-20260703-001: Block virtual trade without positive baseline
- **Date:** 2026-07-03
- **Status:** accepted
- **Context:** Both scalp and confirmation baseline JSON files evaluate to null.
- **Decision:** `update_plus3_virtual_trades()` returns `no_positive_baseline` and creates no new trades.
- **Rationale:** Prevents research system from simulating trades on unproven expectancy.
- **Alternatives considered:** Force-open virtual trades on top grid row anyway.
- **Consequences:** System stays in data-collection mode; operators must read baseline files.
- **Links:** `research_results/plus3_scalp_baseline.json`, `plus3_virtual_trades.py`

### DEC-20260703-002: A-track direct entry not trade-ready
- **Date:** 2026-07-03
- **Status:** accepted
- **Context:** Best scalp grid row still negative avg net (-0.447%, n=158).
- **Decision:** Do not promote direct decision-price entry to baseline or live simulation.
- **Rationale:** Win rate alone insufficient; avg net and sample stability matter.
- **Alternatives considered:** Lower target / widen stop until positive — rejected as overfit risk.
- **Consequences:** A exports for C-track may be empty until a real baseline exists.
- **Links:** `plus3_scalp_backtest.py`, `research_results/plus3_scalp_baseline.json`

### DEC-20260703-003: Confirmation lead is research-only
- **Date:** 2026-07-03
- **Status:** accepted
- **Context:** `strong_revolume_vwap` shows +0.112% avg net on 2 samples, 50% symbol concentration.
- **Decision:** Label as research lead only; do not set as baseline.
- **Rationale:** Sample size and concentration fail baseline gate semantics.
- **Alternatives considered:** Promote because win rate 50%.
- **Consequences:** Continue collecting confirmation samples.
- **Links:** `research_results/plus3_confirmation_baseline.json`

### DEC-20260705-001: C-track adapter only, no main-loop integration
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** C-track handoff specifies post-close audit, not intraday control.
- **Decision:** Implement read-only export adapter under `adapters/c_track_export_adapter/` only.
- **Rationale:** Keeps research system conservative while enabling offline A/B snapshots.
- **Alternatives considered:** Background sidecar, gate auto-tuning, virtual trade triggers.
- **Consequences:** No broker/order_router/background_loop coupling.
- **Links:** `config/c_track_adapter_mapping.twse.yaml`

### DEC-20260705-002: Canonical export uses ratio units
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** Percentage-points vs ratio is the highest-risk mapping error.
- **Decision:** Canonical CSV outputs use ratio (`0.03` for 3%); explicit conversion from source.
- **Rationale:** Validator `abs(value) > 1` alone misses sub-1 percentage-point mistakes.
- **Alternatives considered:** Trust DB field names implicitly.
- **Consequences:** Requires dedicated percent-units unit tests.
- **Links:** `adapters/c_track_export_adapter/percent_units.py`

### DEC-20260705-003: B gate_level is not execution signal
- **Date:** 2026-07-05
- **Status:** accepted
- **Context:** Operators may confuse candidate events with entry permission.
- **Decision:** Document in capsule and resume prompts: A/B gate = quality label, not order signal.
- **Rationale:** Prevents accidental live-trading interpretation of research exports.
- **Alternatives considered:** Rename fields — deferred to avoid schema churn.
- **Consequences:** Recovery check includes scope-drift item for trading language.
- **Links:** `Plus3Candidate.gate_level`