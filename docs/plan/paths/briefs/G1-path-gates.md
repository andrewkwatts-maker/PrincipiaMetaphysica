# Brief G1: gates on the selected path (2026-10-28)

Owner direction: "The 72 gates are a bit rusty; a simple number isn't really valid. Just gates
based on the selected path." A gate reads the value the selected path gives. A gate whose
premise the path doesn't use is not applicable rather than failed. The totals are counted, not
fixed at 72. This settles owner decisions 7 and 10 for the gates.

## Where the gates are
- `simulations/PM/paper/appendices/appendix_f_72gates.py`:
  - `run()` at about line 1708 builds `model_data` from 4 registry values, with defaults of 24
    and 288;
  - `validate_gate` is at about line 945;
  - about line 1128 says "torsion = b3 = 24";
  - about line 2134 is a literal `model_data`.
- `generators/generate_72_certificates.py`: `GATES_72_v16_2.json`, `total_gates: 72`, and the
  G72 seal as the AND over executed gates.
- F2b found 8 of 72 gates fail on PM, 5 of them because a gate assumes b3 = 24 while the registry
  says 43. See `docs/plan/paper/track_f_formulas.md`.

## Work
1. Each gate reads its quantities from the registry the selected path produced. Where a fork
   decides a quantity, read it through the fork-resolved helper; H2 did this with
   `registry_chi_eff_total` and `_resolved_n_gen()`. Remove the 24 and 288 defaults: a missing
   value fails early with the row name.
2. Each gate declares the forks or rows it reads. A gate is NOT_APPLICABLE when the path doesn't
   carry its premise. The statuses are PASS, FAIL and NOT_APPLICABLE.
3. Count the totals: applicable, passed, failed and not applicable, plus the selection digest
   they belong to. Keep the gate IDs and the JSON file name (consumers read them), but replace
   `total_gates: 72` with the count and add `path_id`. G72 stays the AND over the applicable
   gates that ran.
4. A literal that disagrees with the registry and that no fork decides is a hidden fork. List it
   (file:line, literal, registry value) in the report and in `docs/plan/paths/hidden_forks.md`
   under "G1". Don't invent a fork.
5. Prose that says "72 gates" is W4, later. Don't edit website pages or paper text.

## Acceptance
- On a fresh default build, the parameters.json values equal the base, except the `gates.*` rows
  and certificate fields. List those.
- `tests/test_variants.py`, `tests/testground`, the gate and certificate tests, and the new tests
  pass. New tests:
  - a gate reads the path value;
  - NOT_APPLICABLE;
  - a missing value fails early.

## Report (≤ 15 lines)
- The commits.
- Gate outcomes before → after on the default path: passed, failed, not applicable.
- Which of F2b's 8 failures changed.
- The hidden literals found.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-gates -b claude/gates core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every command: `PYTHONPATH=<absolute W>/src`, and `TEMP`/`TMP` = `H:/claude-scratch/tmp`.
  Builds and scratch go under `H:/claude-scratch/g1/`, never C:.
- Builds: `python -m metaphysica.build --fast --keep-going --out H:/claude-scratch/g1/<name>`,
  run in the background (about 10 min). Tests that read a build need `PM_PUBLISHED_ROOT` and
  `METAPHYSICA_OUT` set to it. Base build: `H:/claude-scratch/h3/default`.
- Run sweeps and builds with run_in_background and wait for the notification, or use Monitor with an until-condition, never sleep loops.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write
  a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/gates` only, with no AI attribution or Co-Authored-By lines. Never push.
- Functions ≤ 60 lines; fail early; a test per fix.
- Don't edit src in `metaphysica-sweep`; a detached sweep (PID 25076) runs from it.
- Lanes S1, G1 and V1 run at the same time:
  - S1 owns `testground/rank*`, `switch_search.py` and the variants rule text;
  - G1 owns the gate modules;
  - V1 owns `testground/graph/` and `website/js/pm-paths-page.js` plus its CSS.

  Don't touch another lane's files.
- The plan and the contract are in `docs/plan/paths/track_s_selection.md` in PrincipiaMetaphysica.
  Read it first.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.
