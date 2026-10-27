# Brief F2a: every formula is triple-checked or says why not; first batch (2026-10-27)

Plan: `track_f_formulas.md` (Target 4). A registered formula's `triple_status`
(`simulations/base/registry.py:~1380-1440`) is OK, RULED_DIVERGENCE, ARITHMA_ONLY, EML_ONLY,
FLOAT_ONLY or "". Only OK means the published value was checked by three independent legs
(Arithma tree, EML tree, float). The probe counted OK 206, RULED_DIVERGENCE 29, and 347 of 582
unchecked. This lane makes the unchecked set explicit and ratcheted, then converts a first batch.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-triple -b claude/triple core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck` (the build's render-gate step needs it).
- Every Python command: `PYTHONPATH=<absolute W>/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/a62663e5-6bd8-49b9-bb70-198dbd2fa385/scratchpad/f2a/`.
  Builds: `python -m metaphysica.build --fast --out <scratch>/f2a/<name>`, in the background.
  Tests that read a build need `PM_PUBLISHED_ROOT=<that build>` (the default one is stale).
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write
  a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/triple` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lanes E1 (`actions/`, `simulations/PM/gauge/master_ladder.py`, `gauge/master_action.py`)
  and P4 (`testground/`) run at the same time. Don't touch those files.
- Change no published value. A leg that disagrees with the float is a finding: leave that
  formula unconverted, don't add it to RULED_DIVERGENCES, and report it.

## 1. Measure and ratchet
On a fresh build, count formulas by `triple_status` and by registering module. Add a test that
pins the count of unchecked formulas (anything not OK or RULED_DIVERGENCE, and not marked
non-numeric) at its current value; it may only fall.

## 2. Non-numeric with a reason
Some formulas have no number to check (definitions, action densities, symbolic identities).
Add one optional field on the formula, `non_numeric` (a short reason string), carried into
`formulas.json`. A formula with a value can't be non-numeric (validate at registration, fail
early). Mark the honest cases; the test in §1 excludes them and reports them separately.

## 3. First batch
Pick the 2–3 modules with the most FLOAT_ONLY formulas whose value is a closed form of
published rows. Supply `arithma` and `eml` trees, copying the pattern of an existing OK
formula (find one with `triple_env`). Aim for about 50 conversions; stop at the budget, not
at a count. Lower the ratchet to match.

## Acceptance
On a fresh build: `tests/test_triple_track.py`, `test_published_formula_coverage`, the new
ratchet test and `test_formula_lint` pass. `parameters.json` values are byte-identical to a
base build of core-paper (timestamps aside); `formulas.json` differs only in `triple_status`,
the new field and the added tree renderings. Show the diff summary.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; counts by status before → after; the non-numeric count with its 3 most common
reasons; converted formulas by module; every disagreeing formula with both values; the
remaining unchecked count by module (top 5).

## Checkpoint (2026-10-27)
Done (claude/triple b32c897, metaphysica-triple): non_numeric field + registration check; `closed_form` helper in core/triple_helpers.py; tests/test_triple_ratchet.py (pin 273) and test_triple_closed_form.py; 12 cosmology formulas converted (dark_energy, dark_energy_thawing, speed_of_light, attractor_potential); 62 marked non_numeric (gr_spacetime, appendix_m_tensor_calc, lagrangian_master). Acceptance suites pass; parameters.json identical to base.
Brief conflict: the 347 unchecked formulas have NO value (status ""), none is FLOAT_ONLY, so "modules with most FLOAT_ONLY" does not exist; conversions add value + both trees.
Not done: more conversions (273 left; top: appendix_f_72gates 73 gate predicates, matter/gauge/cosmology_sector_complete 15/14/12, qed 11); mark the 72 gates non_numeric or give them values.
