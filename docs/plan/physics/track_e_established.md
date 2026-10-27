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
| E3a chains at source, honest scores, kill switches | briefs/E3a-chains-scores.md | E2 | metaphysica-chains / claude/chains |
| E3b one value per quantity; E3c per-sector cuts | (write after E3a) | E3a, owner | |

## Status
- 2026-10-27: plan and briefs E1, E2 written.
- E2 merged (3aaa2ec; summary `parameter_ledger.md`):
  - **`derivation_chain` is empty on all 813 rows**, so no registry row records how it was
    derived. The ledger rebuilds chains from formulas.json (inputs → outputs).
  - Classes: GEOMETRY 354, UNJUSTIFIED 223, MEASURED_INPUT 109, CONVENTION_SYSTEM 79,
    FITTED 21, CALIBRATED 16, ANSATZ 11, ACTION 0.
  - Falsifiability: TESTED_NOW 174, TESTABLE 3, UNFALSIFIABLE 46, UNSCORED 7, NOT_OBSERVABLE 583.
  - Circular (6): ckm.V_td, V_ts and V_tb, and neutrino.dm2_21 pass against the datum they were
    set from; e8_portal_coupling and v_ew_derived have their own datum in the chain.
  - Kill switches: 2 of 6 match the registry (ALP, proton decay). Fifth force, sterile ν and KK
    gravitons differ; Cross_Pair_Bell has no row.
  - Value conflicts: 39 groups, 10 with readers. b3: the 24s (geometry.elder_kads,
    topology.b3_modular) have no readers; 328 rows read 43. Others with readers: M_PLANCK 15,
    n_gen 13, sin2_theta_W 12, k_gimel 10.
  - Ratchets: unjustified 223, ANSATZ+FITTED 32, unfalsifiable 46, circular 6.
- E3 order (proposed): (1) record real derivation chains at the source (set_param) so the
  ledger stops guessing; (2) fix the 4 kill-switch mismatches and 6 circular scores; (3) one
  value per quantity for the 10 read conflict groups; (4) per sector, cut UNJUSTIFIED and
  UNFALSIFIABLE.
- E3a started (briefs/E3a-chains-scores.md), base 3aaa2ec.
- E3a merged (core-paper b41230b, lane 473236e): `generators/derivation_chain.py`; 227 of 813
  rows carry `derivation_chain`; 77 declared formulas fail the check (mostly the parameter is
  missing from `output_params`), pinned at a ceiling of 77. Circular count 6 → 2; ckm.V_td,
  V_ts, V_tb and neutrino.dm2_21 are now CALIBRATION_CHECK. The oracle reads every kill switch
  from its registry row: fifth force 5.62e-5 → 1.774e-9 (now VIABLE), sterile ν 0.01 → 7.86e-5
  (MARGINAL), KK gravitons 4.5 → 5.0, proton decay 4.757e34 → 4.7574e34; Cross_Pair_Bell has
  "no registry row". Beyond the brief: the ALP coupling is read from
  portals.alp_photon_coupling_gev_inv (1e-11 → 1.23e-6 GeV⁻¹, still IMMINENT_TEST); the owner
  may revert it. No row values changed. 355 of 553 DERIVED/GEOMETRIC/PREDICTED rows have no
  derivation_formula (geometric_anchors 82 lead).
- E1 merged (core-paper def7eeb, lane e528a48; 93 tests pass on it; b41230b fresh build passed, 26 E3a tests): generic
  `EstablishedCheck` catalogue in `actions/established*.py`; ladder report gains `established`.
  29 REPRODUCED, 0 FAILS, 16 BLOCKED. Gravity (Schwarzschild, weak field with G_N = 1/(8πM²),
  Friedmann, waves with D(D−3)/2 polarisations), Dirac, universal coupling and the Planck-mass
  step reproduce on A4/A6/A13 (A26 too, except Schwarzschild: symbolic D=26 > 20 min, skipped).
  Gauge (Maxwell, YM, anomalies, Higgs) BLOCKED on A4:L_SM (D-011), A26:ym, A26:V. A26's second
  time is a flat spectator in the weak-field and FLRW checks. Gauge checks are tested only on
  `sm_gauge_action()`. report() takes ~66 s.
