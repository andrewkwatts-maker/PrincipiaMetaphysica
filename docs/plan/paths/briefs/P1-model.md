# Brief P1: split variants.py into a package, then make testground's model the only one (2026-10-27)

Plan: `PrincipiaMetaphysica/docs/plan/paths/track_p.md`. Behaviour must not change. This
lane moves code and removes a duplicate; it adds no features.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-pathmodel -b claude/pathmodel core-paper`. Work only there (W below).
- Copy the gitignored extension: `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the
  main checkout into the same path in W.
- Every Python command: `PYTHONPATH=W/src`. The editable install points at the main checkout.
  Check this once with `python -c "import metaphysica;print(metaphysica.__file__)"`.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/p1/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Commit on `claude/pathmodel` only, with no AI attribution or Co-Authored-By lines. Never push.
  Never edit the main checkout.

## Step 0: baselines (before any edit)
1. `python -m metaphysica.simulations.core.variants --help`, then write its report JSON to
   `scratch/report_before.json`. If it takes an output path, use that; otherwise call
   `variants.write_report(<path>)`.
2. `list(variants.FORKS)` into `scratch/order_before.json`.
3. Run the full test suite in the background: `python -m pytest -q -p no:cacheprovider -x
   --co` first to count, then a full run with `-q` saved to `scratch/tests_before.txt`.
   Record the failing test ids.

## Step 1 (commit 1): split `simulations/core/variants.py` into the package `simulations/core/variants/`
- `model.py`: env constants, the status vocabulary, `SourceUnmeasurable`, `VariantOption`, `Fork`.
- `adopted.py`: every `_*_adopted` reader and `_DE_BETTI_BY_N`.
- `catalogue/`: one module per domain (cosmology, seed and b3, G2 geometry, flavour, algebra,
  policy; choose by each fork's `source`). `catalogue/__init__.py` assembles `FORKS` with
  an explicit list in the exact current key order.
- `selection.py`: `validate_constraints` … `active_selection`, including `_FORCED`,
  `_SELECTION_CACHE` and the env helpers. Mutable module state lives here once.
- `report.py`: `describe`, `write_report`, `main`. Add `__main__.py`, so
  `python -m metaphysica.simulations.core.variants` still works.
- `__init__.py`: re-export every name that `src/` or `tests/` imports from `variants`,
  private ones included (`_ENV_PREFIX`, `_FORCED`, `_DE_BETTI_BY_N`, `_chi_eff_route_adopted`,
  `_dark_energy_betti_adopted`, …). Find them with
  `grep -rnoE "variants\.[A-Za-z_]+" src tests | sort -u`. `validate_constraints(FORKS)`
  still runs at import.
- Every file ≤ 500 lines. If one catalogue domain is larger, split it further by sub-topic.
  Move text verbatim, comments included.
- `tests/test_forks_are_wired.py`, `test_frozen_seed_literals.py` and `test_silent_fork_defaults.py`
  refer to the file `variants.py`. Point them at the package directory and keep each test's intent
  (for example, SKIP_MODULES skips every file in the package).
- Acceptance: the report JSON is byte-identical to `report_before.json`; FORKS order is
  identical; the full suite has the same failing set as before.

## Step 2 (commit 2): one model
1. Diff `variants/model.py` against `testground/switches/model.py`. testground's
   `VariantOption`/`Fork` must be a superset. Add what it lacks: the option fields
   `requires` and `excludes` (tuples of (fork, option), default `()`), with their comments.
   `variants/model.py` then re-exports the testground classes and constants instead of
   defining them. Delete the duplicate code.
2. In `testground/constraints.py`, add
   `constraints_from_options(forks) -> List[Constraint]`. It turns every option's `requires`
   (grouped per named fork, options OR'd) into `Requires`, and every `excludes` into
   `Excludes`, with rationale `"declared on <fork>.<option>"` and source `fork.source`.
   Make `Requires.violated_by` partial-safe: violated only when `needs_fork` is in the
   selection, matching `variants.violations`. Add a test for both.
3. `variants.violations` / `compatible` delegate to `testground.constraints` over
   `constraints_from_options(FORKS)`. Keep their output strings identical; adapt the format
   in variants if needed.
4. In `theories/pm/__init__.py`, remove `_convert_option`/`_convert_fork`; `pm_forks` uses
   `variants.FORKS` objects directly. `PmSwitches.constraints()` returns
   `constraints_from_options(self._forks)`.
5. Add the test `tests/testground/test_pm_constraints_agree.py`: for every pair of options
   from different forks (full product of option ids, including DISABLED),
   `variants.compatible({a, b})` equals `testground.constraints.is_valid` with PM constraints.
   Also check that testground's enumeration in mode `assess` yields no selection that
   `variants.violations` refuses.
- Acceptance: the report JSON is still byte-identical; the full suite matches the baseline,
  plus the new tests; `python -m metaphysica.testground validate` (check `--help` for the
  theory argument) passes for pm and toy; the AST dependency test still passes.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign. Escalate after two failed
acceptance runs.

## Report (≤ 15 lines)
The commits (sha, subject); the file list with line counts; each behaviour difference found
and how it was resolved; tests before and after (counts and the failing set); the generic
code moved into testground; anything left PM-side that should move later.
