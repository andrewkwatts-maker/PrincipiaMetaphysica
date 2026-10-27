# Brief H2: hidden choices read their fork (the ones that don't wait on decision 7) (2026-10-28)

Plan: `paths/hidden_forks.md` (H1's survey). Each item below is code that ignores a catalogue
fork, so the path engine can't move it. Wire each one so it reads the fork through `resolve()`
(or the registry row the fork already feeds). The adopted option must give today's value, so
the default build doesn't change.

Out of scope:
- Every `b3 = 24` site (H01, H03, H05, H10, H11, H19, H21–H25, H27): owner decision 7.
- H02: lane E4 owns H0.
- H36: the gauge sector on the retired TCS seed. That changes values, so it's an owner decision.
- The dead forks H33–H35: retiring them is an owner decision.

## Items
- **H07:** `core/FormulasRegistry.py:1157-1158` sets `_chi_eff = 72` and `_chi_eff_total = 144`
  unconditionally. Read `chi_eff_route` (see `PM/geometry/chi_eff_routes.py` and
  `chi_eff_branches.py`).
- **H08:** the 13 `chi_eff = 144` literals (`rg "chi_eff\s*=\s*144" src/metaphysica/simulations`).
  Each one reads the registry's chi_eff. A literal that is a documented pin of a typed check
  stays, with a comment naming the fork.
- **H12:** in `PM/cosmology/dynamical_lambda.py:190-191`, wire only the `CHI_EFF` and
  `N_BRIDGES` class constants. `B3` waits on decision 7.
- **H26:** `PM/algebra/gaugino_condensation.py:255, 675` uses `n_gen = 3`. Read the resolved
  n_gen (`n_gen_source`). N1 = b3 waits on decision 7.

For each item, record in `hidden_forks.md` (a "Status" column or a section at the end): wired,
pinned with a reason, or refused, with file:line.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-wirehidden -b claude/wirehidden core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every command: `PYTHONPATH=<absolute W>/src`, and `TEMP`/`TMP` = `H:/claude-scratch/tmp`.
  Builds and scratch go under `H:/claude-scratch/h2/`, never C:.
- Builds: `python -m metaphysica.build --fast --keep-going --out H:/claude-scratch/h2/<name>`,
  run in the background (about 10 min).
- Tests that read a build need `PM_PUBLISHED_ROOT` and `METAPHYSICA_OUT` set to that build.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write
  a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/wirehidden` only, with no AI attribution or Co-Authored-By lines. Never push.
- Functions ≤ 60 lines; a test per fix.
- Other lanes running now:
  - P5a2 edits `testground/`, `theories/pm/` and `variants/catalogue/`.
  - E4 edits `core/observable_groups.py` and the H0 producers.
  Touch none of those.

## Tests
For each wired item, add a test that resolves a non-adopted option without a build and shows
the value moves. For example, under a non-adopted `chi_eff_route`, the registry's chi_eff
differs and `FormulasRegistry` follows it. If the value can't move, say why and pin it.

## Acceptance
On a fresh default build: `parameters.json` values are equal to the core-paper base build
`H:/claude-scratch/f2b/new2` (compare with `python H:/claude-scratch/cmp_params.py <base> <new>`;
timestamps aside). `test_derivation_chains`, `test_parameter_ledger`, `tests/variants` (or
wherever the variants tests live) and the new tests pass.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
- The commits.
- Each item: wired, pinned or refused.
- How many literal sites remain, and why.
- For each wired fork, the value under one non-adopted option.
