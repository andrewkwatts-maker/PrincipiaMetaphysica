# Brief E3a: real derivation chains, honest scores, kill switches that match (2026-10-27)

Plan: `../track_e_established.md` (E2 result, E3 order items 1-2). Read `../parameter_ledger.md`
first. The ledger is `generators/parameter_ledger.py`, with its tests in
`tests/test_parameter_ledger.py`.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-chains -b claude/chains core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W.
- Every Python command uses an ABSOLUTE `PYTHONPATH=<W>/src`. A relative path breaks build
  subprocesses, which then silently import the main checkout. Check
  `metaphysica.__file__` once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/e3a/`.
  Build with `python -m metaphysica.build --fast --out <scratch>/build`, and set
  `PM_PUBLISHED_ROOT` to it for the tests.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Never read or print any Firebase or service-account key file.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/chains` only, with no AI attribution or Co-Authored-By lines. Never push.
- Change no parameter values. Statuses change only where §2 says so. Lane E1 (actions/,
  master_ladder) runs at the same time; stay out of its files.

## 1. Chains recorded at the source
`simulation_base.py:~500` carries `derivation_formula` into metadata, but `derivation_chain`
ships empty on all 813 rows.
- Fill `derivation_chain` at export from the declared formula's `input_params`. That is the
  rule the ledger already uses: move it to one shared function and have the ledger call it,
  with no second copy.
- Fail early: a declared `derivation_formula` that does not list the parameter in its
  `output_params`, or that names an unknown formula, is an error in a new test (with a
  pinned ceiling if there are many now).
- Report how many DERIVED/GEOMETRIC/PREDICTED rows have no `derivation_formula` at all, by
  source module. Don't invent formulas for them.

## 2. Honest scores
- **Circular rows** (ledger `circular`): a CALIBRATED or FITTED row compared with the datum it
  was set from gets the validation_status `CALIBRATION_CHECK`, not PASS. It no longer counts
  among the passes. The prediction rows with their own datum in the chain
  (`algebra.e8_portal_coupling`, `higgs.v_ew_derived`) are reported, and their status isn't
  changed. Make the rule generic, test it on fixtures, and lower the circular ceiling.
- **Kill switches:** `falsification_report.json` is generated. Find its generator and make every
  kill-switch number READ from its registry row, so no number is written twice. For fifth force,
  sterile ν and KK gravitons, report both old values. For Cross_Pair_Bell, either name its row
  or mark it "no registry row" in the report. Test: each kill switch equals its row.

## Acceptance
On a fresh build: `test_parameter_ledger` (with lowered ceilings), the new tests,
`test_every_fork_accounted`, `test_formula_lint` and `test_core_paper` pass. parameters.json
values are byte-identical to the base build, apart from timestamps and the new
`derivation_chain` and `validation_status` fields. Show the diff summary.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; rows with chains before → after; the declared-formula errors; the circular count
before → after; the old and new values for each kill switch; rows with no derivation_formula,
by module (top 5).
