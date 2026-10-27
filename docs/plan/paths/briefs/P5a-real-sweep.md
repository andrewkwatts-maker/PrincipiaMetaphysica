# Brief P5a: a real PM singles sweep and its audit (2026-10-27)

Plan: `track_p.md` (P4 status line). P4 merged `testground sweep` and `testground audit`
(core-paper 6eff829). Its PM smoke marked every run NOT_RUNNABLE, because a late build step
exits non-zero and the PM build has no keep-going. Read P4's Checkpoint at the end of
`briefs/P4-sweep-cli.md` first.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-sweep -b claude/sweep core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every command: `PYTHONPATH=<absolute W>/src`, and `TEMP`/`TMP` = `H:/claude-scratch/tmp`.
  All builds, runs and scratch go under `H:/claude-scratch/p5a/`, never C:.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write
  a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/sweep` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lane F2b (formula registration, `appendix_f_72gates.py`, triple tests) runs at the same time.
  Don't touch those files. Change no published value.

## 1. Why PM runs are NOT_RUNNABLE
Run one default fast build in W and read its `build_status.json`. Name the failing step and why.
- If it is environment (e.g. missing `node_modules`), fix the environment, not the code.
- If it is a real failure of the default build, report it and stop: the owner decides.
- If a run that published its rows is classed NOT_RUNNABLE only because a late, non-row step
  failed, make the worker (or PM's theory adapter) record it as completed-with-failures, so
  `audit` groups it under `failures` and still compares its rows. Test it on the toy theory.
Also move the hardcoded PM `shared_state` set in `testground/sweep/execute.py` into a
declaration on the theory (a `Theory` attribute, default False; PM sets True), with a test.

## 2. The sweep
`testground sweep --theory pm --singles --runs-dir H:/claude-scratch/p5a/runs` as ONE
background process (about 62 builds, about 13 min each, so expect many hours). It resumes, so
if your turn budget runs low while it runs, write the Checkpoint with its PID and the command,
and stop; the main session will pick up the audit.

## 3. The audit
`testground audit --theory pm --runs-dir H:/claude-scratch/p5a/runs --out
H:/claude-scratch/p5a/report.json --md H:/claude-scratch/p5a/report.md`.

## Acceptance
`tests/testground` passes. The default build's failing step is named, and either fixed or
reported. The audit report exists, or the Checkpoint names the running sweep's PID.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; the failing step and its fix; the sweep: runs completed / failed / stale; the
audit: number of classes, the no-op options, interaction sets, closed-gate reads, and the
failure groups with counts.

## Checkpoint (executor, 2026-10-27)
Done: worktree H:/Projects/MathsPhysicsEcosystem/metaphysica-sweep (claude/sweep), pyd copied, `npm ci` run in tools/texcheck. Default fast build (H:/claude-scratch/p5a/default) succeeds: build_status.json has no failed steps, 566 s. So P4's NOT_RUNNABLE was environment (missing texcheck node_modules, plus C: full / ENOSPC); the build now has --keep-going and needs no code fix. shared_state moved to a Theory attribute (PM True), test added; commit 8ac2f13. `tests/testground`: 525 passed, 1 skipped (test_2c_pool cache test failed once under load, passes alone).
Running: sweep started in the background, shell PID 2348584 (python child of that), log H:/claude-scratch/p5a/sweep.log. Command (cwd W, PYTHONPATH=W/src, TEMP/TMP=H:/claude-scratch/tmp): `python -m metaphysica.testground sweep --theory pm --singles --runs-dir H:/claude-scratch/p5a/runs` (about 62 builds, resumes if rerun; do not edit src in W meanwhile, the fingerprint covers it).
Not done: the audit. Next: when the sweep exits, run `python -m metaphysica.testground audit --theory pm --runs-dir H:/claude-scratch/p5a/runs --out H:/claude-scratch/p5a/report.json --md H:/claude-scratch/p5a/report.md`.
