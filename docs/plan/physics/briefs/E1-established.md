# Brief E1: established physics computed from the actions the PM ladder derives (2026-10-27)

Plan: `../track_e_established.md`. Today the GR, Maxwell and KK checks
(`src/metaphysica/actions/controls/*.py`) run on hand-built actions. The PM ladder
(`simulations/PM/gauge/master_ladder*.py`) never runs them on its own A26/A13/A6/A4. Make
them run on the ladder's actions, so that a wrong coefficient, sign or dimension in PM fails.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-established -b claude/established core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/e1/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/established` only, with no AI attribution or Co-Authored-By lines. Never push.
- Other lanes run at the same time: W3 (wording), L3b (orbifold scan), E2 (parameter ledger).
  Stay out of their files. Don't edit published formula text (W3 and L2c own it).
- Functions ≤ 60 lines; `actions/` imports nothing from `simulations`, `generators` or `website`.

## 1. Generic: checks that take an Action (`actions/established.py`)
`EstablishedCheck(id, area, ref, needs, compute)`. `needs` lists the field kinds and term
roles it needs (e.g. gravity R term, a spinor kinetic term, a vector field strength).
`compute(action)` returns the same shape as Correspondence (measured, holds, can_fail, source).
`run(action, checks)` gives one verdict per check:
- **BLOCKED** when a needed term is missing or OPEN. Name the term and its audit reference.
- **REPRODUCED / FAILS** otherwise, with the residual.
Refactor the existing control computes so that they read the action (D, signature, sign
convention, R-term coefficient and mass dimension, field content) rather than constants. Every
existing control and failing control must still give its old result.

## 2. Catalogue (each computed with sympy, each with a textbook ref and a failing control)
- Gravity, from the R term:
  - Schwarzschild solves the vacuum equations.
  - The weak-field limit is Poisson with G_N = 1/(8π M²), and gravity is attractive. This
    checks the sign convention against the signature; PM's reduced-lagrangian-4d mostly-minus
    question shows up here.
  - FLRW gives the Friedmann equation.
  - Linearised waves are massless with 2 polarisations and travel at speed 1 (GW170817).
- Reduction steps: the KK Planck-mass relation M_child^(D_c−2) = M^(D−2) Vol, and child
  dimension D − dim, on every PM step. Reuse `reduction.py`; don't duplicate it.
- Matter:
  - The spinor kinetic term gives the Dirac equation, with mass dimension (D−1)/2.
  - Universal (minimal) coupling: every matter term couples to the same metric.
- Gauge (all BLOCKED today on A4:L_SM; prove that): Maxwell, Yang–Mills for SU(3)×SU(2)×U(1),
  anomaly cancellation for the declared content, the Higgs mechanism.

## 3. Wire into the PM ladder
`master_ladder.report()` gains `established`: per action, per check, the verdict. Pin in a test:
the REPRODUCED count may only rise, and every BLOCKED verdict names an OPEN term that exists in
`OPEN_TERMS`. A FAILS on PM is a finding: report it and don't fix PM's coefficients to pass.

## Acceptance
`tests/actions`, `test_master_ladder` and the new tests pass. Each catalogue check has a failing
control that fails.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; a table of action × check → verdict; each FAILS with its residual; the BLOCKED
list with blockers.
