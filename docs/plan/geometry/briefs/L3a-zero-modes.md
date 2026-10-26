# Brief L3a: zero modes on the adopted seed, the first geometry → physics test (2026-10-27)

Plan: `track_l_action_ladder.md` ("Geometry next"). Engine: `metaphysica.actions`
(`reduction.py` already runs `zero_mode_rule` when a `Reduction` sets one). PM ladder:
`simulations/PM/gauge/master_ladder.py`. Its G2 step `r6` (13D → 6D over `G2_Y7`, Betti from
`b3_path.seed_values`) sets no rule today, so field content is never checked.
Goal: what the geometry gives is computed, not asserted, and compared with what PM's
actions declare. Any mismatch becomes a failing check; it is never patched.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-zeromodes -b claude/zeromodes core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/l3a/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Commit on `claude/zeromodes` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lanes P3 (forks and `variants`) and W2 (wording) run at the same time. Don't edit `variants*`,
  `testground/`, `theories/pm`, or any formula's or section's text.

## 1. Generic rule: `actions/zero_modes.py`
`zero_modes(parent_fields, internal_dim, betti, holonomy) -> Dict[str, int]`:
- a p-form gives b_k (p−k)-forms in the child for each k, with b_k = b_(n−k) by Poincaré duality;
- the metric gives the child metric, plus b1 vectors and the metric moduli: n(n+1)/2 for
  `holonomy="flat"` (torus), b3 for `"G2"`. Refuse any other holonomy;
- a spinor gives one child spinor per parallel spinor on the internal space: all
  `spinors.dirac_dim(n)` for flat, 1 of 8 for G2. Cite the source in the docstring;
- the result is the per-kind count of child fields. Dualising forms (for example a 4D 2-form
  into a scalar) is a separate, explicit function, never implicit.
- Controls (`actions/controls/`, each with a failing control):
  - 11D sugra on Joyce's (12, 43) G2: 12 vectors and 43 chiral multiplets. Re-express the
    existing `g2_zero_modes` control through `zero_modes`; keep its id.
  - 11D sugra on flat T^7 → 4D N = 8 (Cremmer–Julia): 28 vectors, and 70 scalars after
    dualising the 7 2-forms. The failing control drops the dualisation.
- Tests in `tests/actions/test_zero_modes.py`: each control, the refusals, Poincaré symmetry.

## 2. PM: wire it into the ladder
- `r6` gets `zero_mode_rule` built from `zero_modes(a13.fields, 7, betti, "G2")`, so
  `check_reduction` compares it with the 6D action's declared fields. Don't edit the 6D action
  to make it pass. The report lists each expected vs declared count.
- New check on the G2 step, `nonabelian_gauge_source`. A smooth G2 (resolved, Betti valid)
  gives only U(1)^b2. If the 6D or 4D action declares SU(3) or SU(2) fields, the check
  passes only when a source is declared: a D-028 class whose singular A_{k−1} loci are kept
  (`orbifold_gauge_scan.betti_with_keep`), with that class named. PM has none today, so the
  check fails, giving the reason and the citation (Acharya hep-th/9812205; Atiyah–Witten
  hep-th/0107177). Run on the active Z2^3: keeping its 12 A1 loci gives SU(2)^12 with b1 = 3
  adjoint chirals (non-chiral) and no SU(3). State this in the check detail, computed by the scan.
- `ladder_report()` (or the existing report) shows both checks. The ladder verdict changes:
  record before and after.

## 3. Acceptance
`tests/actions`, `test_master_ladder`, `test_master_action_single_source`,
`test_master_action_is_one_consistent_statement`, `test_orbifold_gauge_scan` and the new tests
pass. The full suite matches the baseline (run it first, in the background). Any ladder test
that pinned the old verdict changes only by the two new checks; say which.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign. If the 13D action has no
form fields at all, say so: that is a result.

## Report (≤ 15 lines)
The commits; the expected vs declared 6D field counts on seed_43_joyce; the
nonabelian_gauge_source detail; the ladder verdict before → after; test results.
