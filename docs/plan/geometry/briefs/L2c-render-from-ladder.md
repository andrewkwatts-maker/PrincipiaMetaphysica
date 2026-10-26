# Brief L2c: publish the action formulas from the ladder; retire the duplicates (2026-10-27)

Plan: `track_l_action_ladder.md`. Input: `master_ladder_map.md` (31 formulas: step 17,
reduction 4, retire 6, out 4). Engine: `metaphysica.actions` and
`simulations/PM/gauge/master_ladder*.py` (merged 36bb6a4). Render gate: `tools/texcheck`
(merged 3190f90; run `npm ci` there first).
Goal: one master action. Each published action formula is generated from the ladder, so they
can't disagree again.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-ladderrender -b claude/ladderrender core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/l2c/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Commit on `claude/ladderrender` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lane W1 is editing stale wording in other formulas and prose. You own the 31 action formulas
  in the map; don't edit other formulas' text. Don't edit `variants*`, `testground/` or
  `theories/pm`.

## 1. Generic rendering: `actions/latex.py`
`action_latex(action) -> str`: `S_{D} = \int d^{D}x\,\sqrt{|g|}\,[\ldots]` with the measure
from the signature (two times → `|g|`, one → `-g`), one summand per term in declared order, and
OPEN terms rendered by symbol. Each `Term` gets an optional `latex` field (the summand's
display form), defaulted so existing tests pass. Test that the output passes the texcheck
render gate and `formula_lint` (measure, planck_exponent).

## 2. PM: render the step formulas from the ladder
- For each map row of kind `step` whose target is a whole action (26D, 13D, 4D), the
  publishing simulation takes its `latex` from `action_latex(...)` of that ladder step. For
  `step` rows that target one term (e.g. `26D:L_bridge`, `4D:L_SM`), the term's `latex` comes
  from the ladder. Keep each formula id stable, so links don't break.
- The EOM rows (`euler-lagrange-*`): keep their text, and add the ladder step they vary in
  their derivation metadata.
- `reduction` rows: keep the text, fix only what the ladder contradicts. Each fix is named in
  the report (e.g. `lagrangian-hierarchy-complete` "M^10 R_12").

## 3. Retire the duplicates
- Retire with the existing retirement mechanism (find how `sp2r-gauge-fixed-action` was
  retired; reuse it, don't invent a new one): `master-action-two-layer-or`,
  `bulk-action-26d-v23`, `v22-bridge-lagrangian` (a duplicate of `bridge-lagrangian-v22`), and
  the v19 twins `su3-qcd-lagrangian-g2-v19` and `su2-weak-lagrangian-g2-v19`, after checking
  that each twin's text matches its -v22 twin. Repoint every reference (formula ids in
  sections, derivation chains, tests) to the surviving id. `validate formula-id references`
  must stay at 0 dangling.
- `de-frt-lagrangian-v19`, `f-r-t-tau-lagrangian-v18` and `pneuma-lagrangian`: don't retire
  them; that is an owner decision. Mark each formula's description with "Not derived from the
  master action." and list them in the report.

## 4. Tests: `tests/test_master_action_single_source.py`
- Each rendered step formula's published latex equals `action_latex` of its step (read from
  the simulation's formula definitions, not a build).
- No retired id is referenced from a published surface.
- The map rows are all accounted for (the counts in the map).
- Acceptance: the new tests pass; `tests/actions`, `test_master_ladder`,
  `test_master_action_is_one_consistent_statement`, `test_tex_renders`, `test_formula_lint`
  and the formula-reference tests pass on a fresh `metaphysica.build --fast` in scratch,
  with `PM_PUBLISHED_ROOT` pointing at it.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; files changed; per map row, what happened (rendered / kept / retired / marked);
references repointed; test results; anything the ladder couldn't render.
