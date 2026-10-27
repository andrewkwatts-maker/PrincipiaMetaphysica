# Brief P5a2: partial runs count, undeclared constraints, finish the singles sweep (2026-10-28)

Plan: `track_p.md` (P5a status). P5a's singles sweep (claude/sweep 8ac2f13, worktree
`H:/Projects/MathsPhysicsEcosystem/metaphysica-sweep`) died after 22 of 62 runs. The background
shell ended with the session that started it. Runs so far are in
`H:/claude-scratch/p5a/runs/pm/e78394bb2c878ee9/` (one directory per selection, `result.json`,
`configuration.json`, `run_logs/`):
- 7 COMPLETED.
- 7 NOT_RUNNABLE "not implemented": declared options with no implementation.
- 7 NOT_RUNNABLE "stage build exited 1", in two groups:
  - **A. The build halts on the shadow audit** (`scripts/audit_shadow_derivations.py` exits 1 on
    a conflict not in `KNOWN_CONFLICTS`). parameters.json was already written. Affected:
    h0_route=kk_bridge, h0_route=ricci_flow and b3_seed=seed_24 (new conflict H0_local).
  - **B. Fail-early ValueErrors in run_all_simulations.**
    - b3_seed=seed_7/19/31_joyce: "gives n_gen = 0.0 via b2_over_faces … the n_gen_source fork
      must move with b3_seed".
    - n_gen_source=b3_over_dim_O: "non-integral generation count (5.375)".
    These are constraints that the catalogue doesn't declare.

## Where to work
- Worktree W = `H:/Projects/MathsPhysicsEcosystem/metaphysica-sweep`, branch `claude/sweep`. It
  already has the pyd and `tools/texcheck/node_modules`.
- Every command: `PYTHONPATH=H:/Projects/MathsPhysicsEcosystem/metaphysica-sweep/src`, and
  `TEMP`/`TMP` = `H:/claude-scratch/tmp`. All builds and scratch go under `H:/claude-scratch/p5a/`,
  never C:.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write
  a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/sweep` only, with no AI attribution or Co-Authored-By lines. Never push.
- Change no published value of the default build. Functions ≤ 60 lines; a test per fix.
- Lane E4 (H0 route, `simulations/`) runs at the same time in another worktree; don't fix group
  A's physics here.

## 1. A run that wrote its rows is compared, not discarded
- PM's stage (`theories/pm/__init__.py:87`) passes `--keep-going`.
- A run whose stage exits non-zero but whose build wrote its rows is recorded as
  completed-with-failures. The failed steps come from `build_status.json`. `audit` compares the
  run's rows and also lists it under `failures`, grouped by step and reason.
- Keep testground generic: the theory declares how to tell that rows were written. Don't put a
  PM special case in `testground/`. Test it on the toy theory.

## 2. Declare the missing constraints
- For each b3_seed × n_gen_source pair, compute n_gen without a build, using the same functions
  the ValueErrors come from.
- In `simulations/core/variants/catalogue/`, declare `requires`/`excludes` that refuse every pair
  giving a non-integral count or one that isn't 3. Follow the pattern at `catalogue/seed.py:152`.
- `--singles` must not drop a refused option silently. Pick one:
  - If the constraint model gives a unique minimal repair (one other fork's option), run the
    repaired pair and label it.
  - Otherwise, the dry-run lists the option as refused, with the reason.
- Test both cases on the toy theory, and pin the PM pairs.

## 3. The not-implemented options
List the 7 (fork, option, and the file:line of the raise) in track_p's Status line. Don't
implement them.

## 4. Finish the sweep
- Run `tests/testground` and the variants tests.
- Commit, then restart the singles sweep. The source changed, so every run reruns.
- Start it **detached**, so it outlives your session: PowerShell `Start-Process` with
  `-RedirectStandardOutput H:/claude-scratch/p5a/sweep2.log` and
  `-RedirectStandardError H:/claude-scratch/p5a/sweep2.err`, with the env above.
- Record its PID.
- Command, from cwd W:
  `python -m metaphysica.testground sweep --theory pm --singles --runs-dir H:/claude-scratch/p5a/runs`.
- When it exits, run
  `python -m metaphysica.testground audit --theory pm --runs-dir H:/claude-scratch/p5a/runs --out H:/claude-scratch/p5a/report.json --md H:/claude-scratch/p5a/report.md`.
  If your budget runs out first, write the Checkpoint with the PID and stop.

## Acceptance
- `tests/testground` and the variants tests pass.
- A dry-run shows no single that the theory's constraints refuse.
- The default build's parameters.json is unchanged.
- The sweep is running detached (PID recorded), or the audit report exists.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
- The commits.
- The constraints added, with the pairs and their n_gen.
- How refused singles are handled.
- The 7 not-implemented options.
- The sweep PID, or the audit: classes, no-ops, closed-gate reads, failure groups with counts.
