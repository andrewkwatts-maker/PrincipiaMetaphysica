# Brief L3b: which D-028 classes could source SU(3)×SU(2) with chiral matter (2026-10-27)

Plan: `track_l_action_ladder.md` ("L3a result", owner decision on the gauge source). Scan:
`simulations/PM/geometry/orbifold_gauge_scan.py` (Rust-backed), report `d028_rust.md`, records
`H:/claude-scratch/d028_full/records.jsonl` (740 classes, cap 1536; read-only).
Computation only: nothing is adopted and no D-028 ruling changes. The owner decides.

## What is already known (main session tally of the records)
- 139 classes have SU(3)×SU(2). All 139 have crossings, so `betti_valid` is false for all.
- 92 of them have codim-7 points, a necessary condition for chiral 4D matter in M-theory
  on G2 (Acharya–Witten hep-th/0109152; Atiyah–Witten hep-th/0107177).
- No hit has every SU(3) locus with b1 = 0. 57 have SU(3) loci with b1 in {0, 1}; 35 have
  only b1 = 1 (one adjoint chiral per locus).

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-gaugesrc -b claude/gaugesrc core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/l3b/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/gaugesrc` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lanes W3 (wording) and P3b (variants forks) run at the same time; stay out of their files.

## 1. Reasons per invalid class (generic, in the scan module)
`invalid_reasons(record) -> List[str]`, from: "crossings", "non_A_strata", "non_free_normal".
Tally over all 740 records, and over the 139 hits. Test it on the recorded fixtures.

## 2. Local type of codim-7 points and crossings (the open item in d028_rust.md)
For each codim-7 orbit and each crossing in the 92 codim-7 hits, compute from the group
elements (re-run `analyse` per class if the records lack them):
- the stabiliser H and its linear action on R^7: its character, its decomposition into real
  irreducibles, and whether H acts freely on S^6 (an isolated cone R^7/H);
- which A-type loci (k, as SU(k)) pass through the point.
Write `codim7_local_type(elems, point) -> dict` (≤ 60 lines per function), with a control: a
hand-built H for which the answer is known, and a failing control.

## 3. Candidate table (no adoption)
`scripts/d028_gauge_source.py` writes `<scratch>/l3b/gauge_source.json` and a short Markdown
table in `PrincipiaMetaphysica/docs/plan/geometry/d028_gauge_source.md`. One row per hit:
class, family, order, gauge text, number of codim-7 points where an SU(3) and an SU(2) locus
meet (candidate bifundamental chiral points), the b1 of each SU(3) and SU(2) locus (adjoint
chirals), and the invalid reasons. Rank by: (a) SU(3)–SU(2) meeting points > 0; (b) fewest
adjoint chirals; (c) smallest order. Say plainly that this is a necessary-condition filter,
not a chirality or generation count.

## Acceptance
New tests pass; `test_orbifold_gauge_scan`, `test_orbifold_gauge_scan_rust` and
`tests/actions` pass. The table reproduces the 139 / 92 counts above, or explains the
difference.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; the reason tally; how many hits have SU(3)–SU(2) meeting codim-7 points; the
top 5 rows; what was not computable and why.
