# Track E: established physics from the master action; every parameter justified and falsifiable (2026-10-27)

Owner request: all established physics reproduced from our master action, and every
parameter as falsifiable and justified as possible.

## State (measured 2026-10-27, core-paper b8916d5, fast build scratchpad/w2m)
- **Physics checks run on toy actions, not on PM.** `actions/controls/four_d.py`
  (Schwarzschild, weak-field Poisson, FLRW, Maxwell), `kaluza_klein.py`,
  `ricci_flat_compactification.py`, `g2_zero_modes.py` and `torus_sugra.py` act on hand-built
  actions. The PM ladder (`simulations/PM/gauge/master_ladder*.py`) checks only spinor products,
  spinor counts, zero modes and owner item 6.
- **PM's derived 4D action (A4)** = (M_Pl²/2) R + Ψ̄ iγ·D Ψ + the OPEN terms L_SM, L_portal, L_DM.
  So gravity can be tested now; gauge, Higgs and flavour physics cannot, because L_SM is OPEN
  (D-011, L3a: the 13D action has no p-form, so no gauge field comes down the ladder).
- **Parameters:** parameters.json has 813 rows with 30 status labels (DERIVED 336,
  GEOMETRIC 150, ESTABLISHED 75, PREDICTED 67, FITTED 19, CALIBRATED 15, ANSATZ 8, ...).
  - validation_status: NO_DATA 622, PASS 121, FAIL 25, MARGINAL 19, TENSION 11; 5 rows are FALSIFIED.
  - 44 PREDICTED rows have no experimental value and no named test.
  - `free_variables.json`: 70 not derived (UNRESOLVED 36, LOAD_BEARING_INPUT 11, COMPARISON_ONLY 22).
  - `free_set.py` already counts independent knobs.
  - `falsification_report.json` lists 6 kill switches as prose, not linked to registry values.
- No row links a parameter to the ladder step or term that justifies it.

## Target
1. **E1:** each established result is computed from the action that the PM ladder actually
   derives, never asserted. It gets one verdict: REPRODUCED, FAILS (with the residual) or
   BLOCKED (naming the OPEN term or owner item). Gravity items must reach REPRODUCED or FAILS
   now; gauge/matter items stay BLOCKED until L_SM has a source (owner decision 6).
2. **E2:** each parameter has one justification class with mechanical evidence and one
   falsifiability record. Ratchets: unjustified rows, ANSATZ+FITTED rows and unfalsifiable
   predictions may only fall. FAIL / TENSION / FALSIFIED rows are reported plainly, never retuned.
3. **E3 (after E1, E2; needs owner input):** reduce the list. For each ANSATZ/FITTED/UNRESOLVED
   row, either derive it from the ladder (a sub-action term), or name the datum it is
   calibrated to, or flag it for the owner. One lane per sector.

## Lanes
| Lane | Brief | Depends on | Worktree / branch |
|---|---|---|---|
| E1 established physics on the PM ladder | briefs/E1-established.md | L3a | metaphysica-established / claude/established |
| E2 parameter justification + falsifiability ledger | briefs/E2-param-ledger.md | none | metaphysica-paramledger / claude/paramledger |
| E3 reduce ANSATZ/FITTED/UNRESOLVED per sector | (write after E1, E2) | E1, E2, owner | |

## Status
- 2026-10-27: plan and briefs E1, E2 written.
