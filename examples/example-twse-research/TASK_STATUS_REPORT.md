# AI Task Status Report

> **Disclaimer:** This capsule is **research-state handoff only**. It is not investment advice, trading instruction, or an execution authority pack.

Generated At: 2026-07-05T12:00:00Z
Task / Project Name: TWSE Plus-3 A/B research + C-track adapter (research state)
Version Hash: v20260705-1200-twse
Previous Version Hash: null
Current Branch: main
Current Stage: research-collection / adapter-dry-run

## 1. Overall Progress
- Completion: 45%
- Current Stage: research-collection / adapter-dry-run

## 2. Status Classification
### Done
- B-track candidate scanner operational (`plus3_candidate_scanner.py`, `Plus3Candidate`)
- A-track direct-entry scalp backtest grid completed (158 samples; all combos negative avg net)
- Confirmation-entry backtest grid completed; no accepted baseline
- Virtual trade gate correctly blocks when baseline is null (`no_positive_baseline`)
- C-track read-only export adapter scaffolded (`adapters/c_track_export_adapter/`)
- Adapter mapping config present (`config/c_track_adapter_mapping.twse.yaml`)
- Adapter unit tests: 9 passed (`test_c_track_export_adapter.py`)
- Canonical percent-units contract defined (ratio output; percentage-points source)

### In Progress
- C-track adapter dry-run export against local TWSE DB (read-only SELECT)
- Defining `reversed` / `reversal_threshold_ratio` / `time_window` semantics in exports
- Accumulating confirmation-entry samples beyond n=2 research lead

### Todo
- Run first full dry-run export:
  `python -m adapters.c_track_export_adapter.cli --dry-run ...`
- Produce `adapter_mapping_report.json` + `adapter_validation_findings.csv` for review
- Offline C-track PRELIMINARY report (expect `NO_ACCEPTED_A_BASELINE`)
- Continue B-track candidate collection without enabling virtual trade

### Blockers / Risks
- **Hard gate:** `plus3_scalp_baseline.json` = null, `plus3_confirmation_baseline.json` = null
- **Risk:** Treating `gate_level A/B` as trade signals — they are candidate quality labels only
- **Risk:** `strong_revolume_vwap` lead (n=2, 50% concentration) mistaken for strategy
- **Risk:** Percent unit drift (0.5 vs 0.005) silently corrupts C-track comparison
- **Blocker:** None for adapter dry-run; blockers exist for trading / virtual trade / gate changes

### Key Insights & Learnings
- A-track direct decision-price entry is not trade-ready (best: 24.68% win, -0.447% avg net, n=158)
- Broad confirmation best: 61.54% win but -0.131% avg net (n=13) — still fails baseline gate
- Virtual trade disabled is correct conservative behavior, not a bug
- C-track is post-close audit only; must not influence intraday decisions
- Empty A export with header is valid when baseline=null — semantics: `NO_ACCEPTED_A_BASELINE`, not adapter failure

### Experiments / Tests
- **Exp-A-01:** Plus-3 scalp grid — no positive baseline (2026-07-03)
- **Exp-A-02:** Confirmation grid — no positive baseline (2026-07-03)
- **Exp-C-01:** C-track adapter unit tests — 9 passed
- **Exp-C-02:** Full dry-run export against live DB — pending

## 3. Key Information Snapshot
### Major Decisions
- DEC-20260703-001: No virtual trade without positive baseline (accepted)
- DEC-20260705-001: C-track as read-only adapter only, not main-loop integration (accepted)
- DEC-20260705-002: Canonical export percentages as ratio, not percentage-points (accepted)

### Important Settings / Parameters / Resources
- Related repo: `twse_daytrade` (local path: private / user-specific)
- Local service: `<LOCAL_SERVICE_URL>` (e.g. dev API on your machine — not published)
- Last known full test run (handoff record): 2026-07-03, 104 passed
- Baseline files: `research_results/plus3_scalp_baseline.json`, `research_results/plus3_confirmation_baseline.json`
- Mapping: `config/c_track_adapter_mapping.twse.yaml`

### Rejected or Paused Options
- Enable virtual trade before baseline — rejected
- Integrate C-track into background loop — rejected (v0.1)
- Modify A/B gate from C-track output — rejected
- Treat n=2 confirmation lead as baseline — rejected

## 4. Next Actions
### Priority Action 1
Run C-track adapter dry-run for `plus3_open_target`; verify B export, A header-only path, and `NO_ACCEPTED_A_BASELINE` status.

### Priority Action 2
Add/lock percent-units regression tests: `1.2→0.012`, `0.8→0.008`, `0.5→0.005`, `-0.4→-0.004`.

## 5. Compressed Summary
TWSE daytrade is in research-collection mode, not trade-release mode. B-track Plus-3 candidate scanning is the primary data source. A-track direct-entry scalp across 158 samples remains negative expectancy; confirmation grids also fail baseline acceptance despite occasional high win rates on tiny samples. Both `plus3_scalp_baseline.json` and `plus3_confirmation_baseline.json` are null, so `plus3_virtual_trades.py` correctly returns `no_positive_baseline` and blocks new virtual trades. C-track work is limited to a read-only export adapter with mapping config and passing unit tests; it is not integrated into the main server loop and must not alter gates, broker paths, or intraday decisions. The next milestone is a dry-run canonical export producing B events and an A track that may be empty but header-valid, labeled PRELIMINARY or `NO_ACCEPTED_A_BASELINE`. Percent-unit conversion to ratio must be explicit and tested. Gate levels A/B remain candidate-quality labels, not execution signals.

## 6. Resume Instruction
Resume this task from version v20260705-1200-twse.