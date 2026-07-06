# Recovery Check

Use when AI drifts toward trading, gate changes, or C-track over-integration.

## 1. Scope Drift
- [ ] Still TWSE Plus-3 research + C-track adapter?
- [ ] AI did not propose live trading, broker wiring, or gate auto-tuning?
- [ ] **Fix:** Re-paste `RESUME_INSTRUCTIONS.md`; cite DEC-20260705-001

## 2. Baseline Integrity
- [ ] `plus3_scalp_baseline.json` still null?
- [ ] `plus3_confirmation_baseline.json` still null?
- [ ] Virtual trade still blocked with `no_positive_baseline`?
- [ ] **Fix:** Do not enable virtual trade; update status report only

## 3. Misread Signals
- [ ] AI did not treat `Plus3Candidate.gate_level` as entry permission?
- [ ] AI did not promote n=2 confirmation lead to baseline?
- [ ] **Fix:** Cite DEC-20260703-003 and DEC-20260705-003

## 4. C-track Boundaries
- [ ] Work limited to read-only adapter / dry-run export?
- [ ] No background loop integration proposed?
- [ ] Empty A export understood as `NO_ACCEPTED_A_BASELINE`, not failure?
- [ ] **Fix:** Cite DEC-20260705-001; run recovery before continuing

## 5. Percent Units
- [ ] No canonical CSV with raw 0.5 / -0.4 meaning 50% / -40%?
- [ ] Conversion tests for 1.2, 0.8, 0.5, -0.4 still passing?
- [ ] **Fix:** Stop export work; fix `percent_units` first

## Recovery Outcome

- **Recovery date:**
- **Restored from version hash:**
- **Branch after recovery:**
- **Notes:**