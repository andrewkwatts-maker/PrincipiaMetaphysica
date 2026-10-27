# Brief F2b: the 72 gates and the sector formulas, checked or explained (2026-10-27)

Plan: `track_f_formulas.md` (Target 4; F2a status line). F2a added `Formula.non_numeric`,
`closed_form(spec, env)` in `simulations/core/triple_helpers.py` and `tests/test_triple_ratchet.py`
(pin 273). Unchecked formulas have no `value` at all (status ""), so converting one means
supplying a value from the simulation's own float plus both trees from one `closed_form` spec.
Read F2a's Checkpoint at the end of `briefs/F2a-triple-track.md` first.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-triple2 -b claude/triple2 core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every Python command: `PYTHONPATH=<absolute W>/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/a62663e5-6bd8-49b9-bb70-198dbd2fa385/scratchpad/f2b/`.
  Builds: `python -m metaphysica.build --fast --out <scratch>/f2b/<name>`, in the background.
  Tests that read a build need both `PM_PUBLISHED_ROOT` and `METAPHYSICA_OUT` set to it. F2a's
  last build (`<scratchpad>/f2a/new`) can serve as the base.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write
  a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/triple2` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lanes P4 (`testground/`) and L2b (variants catalogue, `master_ladder.py`,
  `gauge/master_action.py`, `theories/pm/`, build steps) run at the same time. Don't touch those.
- Change no `parameters.json` value. A leg that disagrees is a finding: leave that formula
  unconverted, don't add it to RULED_DIVERGENCES, and report it.

## 1. The 72 gates (`simulations/PM/paper/appendices/appendix_f_72gates.py`)
Each gate has a `formula_id` and an evaluator branch in `validate_gate` (line ~944). Sort the 73
unchecked gate formulas into:
- **numeric:** the gate compares a computed quantity with a target. Give the formula that
  quantity as its value with trees from `closed_form` (triple-checked).
- **predicate:** a pass/fail condition with no single number. Mark `non_numeric` with the reason
  `"pass/fail gate N, evaluated by validate_gate"`.
A test asserts every gate formula is one of the two, and that `validate_gate` runs for every gate
on the model data without raising. Report how many gates pass and fail on PM; don't change a
gate to make it pass.

## 2. Sector formulas
Then convert closed forms in `derivations.matter_sector_complete`, `gauge_sector_complete`,
`cosmology_sector_complete` and `qed`, the same way as F2a; mark the honest non-numeric ones.
Stop at the budget, not at a count.

## Acceptance
On a fresh build: `test_triple_track`, `test_triple_ratchet` (pin lowered to the new count),
`test_triple_closed_form`, `test_published_formula_coverage`, `test_formula_lint` and the new
gate test pass. `parameters.json` values are byte-identical to the base build (timestamps
aside). Show the formulas.json diff summary.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; the ratchet pin before → after; gates numeric / predicate, and pass / fail on PM;
conversions by module; every disagreeing formula with both values; the remaining unchecked by
module (top 5).

## Checkpoint (2026-10-27)
Done (claude/triple2 in metaphysica-triple2, 2 commits, not pushed): (1) 72 gates: 11 numeric gates (g04, g08 as sin(theta_s), g11, g12, g18, g22, g24, g31, g37, g40, g66) now carry value + closed_form trees; the other 61 gates and omega-hash-72 are non_numeric "pass/fail gate N, evaluated by validate_gate"; new tests/test_gates_triple.py (4 tests pass). (2) Sectors: gauge 2 converted (su3-gluon-count, u1-hypercharge-ratio) + 8 non_numeric; matter 4 converted (christ-constant-153, yukawa-epsilon-cabibbo, majorana-scale, fermion-generations) + 5 non_numeric; cosmology 2 converted (de-w0-tzimtzum, cosmo-omega-matter-split) + 3 non_numeric.
PM gates with default registry data: 64 pass, 8 fail (6, 9, 12, 22, 29, 31, 63, 72). Cause for 6/9/12/22/31: GateRegistry.TORSION_PINS = elder_kads = 43 on the live registry while the gate code hardcodes b3 = 24 (appendix_f_72gates.py validate_gate, e.g. gate 6 torsion == 24; gate 31 gives 850.91 GeV). Not changed.
Finding: gauge ew-weinberg-angle-v19 states (12/24)*0.924 = 0.2312 but the product is 0.462; left unconverted.
NOT done: acceptance run. The fresh --fast build in scratchpad/f2b/new ended after 487 s with the C: volume at 0 bytes free (other sessions), so its output is incomplete and the ratchet pin (273) is not lowered. qed module not touched (formulas are X_bulk*(1+eps) with CODATA inputs).
Next: free C:, rebuild (PYTHONPATH absolute to W/src), count unchecked, lower _UNCHECKED_CEILING in tests/test_triple_ratchet.py to the measured value, run test_triple_track, test_triple_ratchet, test_triple_closed_form, test_published_formula_coverage, test_formula_lint, test_gates_triple; check parameters.json identical to base; convert qed.

## Checkpoint 2 (main session, 2026-10-27 23:00)
Finished on H: (build H:/claude-scratch/f2b/new2, 549 s, no failed steps): aa85c17 lowers the
pin 273 → 177; six suites 322 passed / 0 failed; parameters.json values identical to f2a/new.
Merged core-paper b34c640 (335 passed merged). Still unchecked (by source_simulation):
appendix_h_288_roots_v24_2, matter_sector_complete_v19, cosmology_sector_complete_v19,
complete_residue_registry_v18 7 each; four_face_g2_structure 6. qed not converted.
