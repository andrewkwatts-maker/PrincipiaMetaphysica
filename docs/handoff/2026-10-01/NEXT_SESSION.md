# Next session — start here

**The plan in force:** `C:\Users\Andrew\.claude\plans\ensure-all-simulation-and-greedy-nygaard.md`
(approved 2026-10-02). It schedules everything — phases P0–P10 with a Gantt, hard gates,
agent lanes with disjoint ownership — and maps every carry-over todo to a track.

## Status by phase (update as phases land)

| Phase | State |
|---|---|
| P0 land 10-01 work, re-pin, pre-register | D-017 PR-1 RESULT, D-019, D-020 and the D-003 addendum 2 recorded; salvage refs tagged (`salvage/a67a30b2`, `salvage/ad29c1ee`); 11 pinned failures re-pinned or fixed; rebuild + suite + commit in progress |
| P1 run isolation | not started (gate: P0) |
| P2 test ground | contracts written (`src/metaphysica/testground/{theory,constraints}.py`, `switches/model.py`, `configurations/model.py`, `signals/model.py`, `assessment/score.py`, `schemas/*.json`, `tests/testground/test_contracts.py`); commit after P0 |
| P3–P10 | not started |
| Track W (wording) | per-lane remaining lists in `lanes/wording_lanes.md` |
| Track B (bugs) | `TODO.md` |
| Track C (PR-2/PR-3) | design in `lanes/pr1_pr2_pr3.md` |

## Where things are
- Decisions: `docs/DECISION_LOG.md` (D-001 … D-020).
- Wording rules: engine `docs/WORDING_MEMO.md` (rulings block D-015 at the top).
- Lane reports and remaining work: `lanes/wording_lanes.md`, `lanes/pr1_pr2_pr3.md`.
- Verifications and classifications (G1b, G5, D-013 data): `verifications_and_classifications.md`, `data/`.
- Open problems literature (verified citations): `open_problems_literature.md`.

## Standing rules
No AI attribution (author and committer andrewkwatts-maker <andrewkwatts@gmail.com>);
explicit-path commits; site commits `--no-verify`; pre-register before computing; suite
before each engine commit; rebuild both roots and restore the junction before a site
commit; agents never run git and never set `METAPHYSICA_OUT`; dead ends are demoted,
never deleted.
