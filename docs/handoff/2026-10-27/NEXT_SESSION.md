# Handoff 2026-10-27: paths, master action ladder, formulas, wording

Owner requests this session: "branches/pipeline clearly defined, generic solvers that test all
paths"; "keep closing geometry, master action validation and sub-actions at each step,
re-create established physics"; "paper wordings concise, up to date, clear"; "master action
well defined, all formulas' LaTeX rendered correctly, correct formulas"; "keep working on
closing/solving".
Plans: `docs/plan/paths/track_p.md` (P), `docs/plan/geometry/track_l_action_ladder.md` (L),
`docs/plan/paper/track_f_formulas.md` (F, W). Each lane has a brief under `briefs/`.
Token rule (receipts session): each brief has a budget of about 60 tool calls and a hard stop at about 100 turns,
then a checkpoint in the brief. Never kill processes by name; kill only your own PIDs.

## Merged into engine `core-paper` (now f06142f, not pushed)
- F1 3190f90 + d61220b: MathJax 3.2.2 render gate (`tools/texcheck`, build step), one shared
  config, formula lints (measure, Planck exponent, superseded). Render errors 11 → 0.
- L1 c9c1f2f, L2a 36bb6a4, L2c e7ae865: `metaphysica.actions` (fields, terms, dimensions,
  reductions, correspondence controls, spinors); the PM master action is a checked ladder
  26D → 13D → 6D → 4D; the 26D/13D/4D action formulas render from it; 5 duplicates retired.
- W1 8615661: stale autogen 277 → 265, website 15 → 3; prose_lint and duplicate_statements
  with ratchets; `_RETIRED` pattern pinned. 1d6451b re-pins the old-introduction hash.
- P1 f06142f: `variants` is a package; testground's `Fork` is the only fork model. Full
  suite on f06142f: 3873 passed, 424 skipped, 0 failed.

## Running at handoff (worktrees beside the engine; review, merge `--no-ff`, remove)
- P3 `metaphysica-pathgates` / claude/pathgates: fork gates (dark_energy_betti only under
  thawing), read tracker → `fork_reads.json`, PM `testground validate` (5 problems).
- W2 `metaphysica-wording2` / claude/wording2: "b3 = 24" prose → the dark_energy_betti
  option; stale hits; 21 duplicate groups with a keeper; long sentences (317).
- L3a `metaphysica-zeromodes` / claude/zeromodes: generic `actions/zero_modes.py` (controls:
  Joyce (12, 43); T^7 → 28 vectors and 70 scalars), wired into the G2 step, plus the
  `nonabelian_gauge_source` check (expected to fail: a smooth G2 gives only U(1)^12).

## Findings
- w0 = -23/24 is correct for the dark_energy_betti default `b3_24` (n = 24), not the
  geometry's b3 = 43. The prose that says "b3 = 24" is the error (W2).
- Spinors: 26D (24,2) has s−t ≡ 6 mod 8, so pseudo-Majorana but no Majorana–Weyl; 64×64 =
  4096 is the Weyl half of 8192 (item 11 resolved).
- The build at `H:/claude-scratch/runs_g/active` is stale; tests that use PM_PUBLISHED_ROOT
  need a fresh `metaphysica.build --fast` (the latest good one is
  `<scratchpad>/w1m/build`, pre-P1).

## Owner decisions open
1. Item 6: where the second time goes in 26 → 13 (the ladder's only failing check).
2. Retire de-frt-lagrangian-v19, f-r-t-tau-lagrangian-v18, pneuma-lagrangian? (marked "Not
   derived from the master action").
3. reduced-lagrangian-4d sign convention (item 5).
4. The 34 duplicate-statement groups with no keeper.
5. Declared-only forks gauge_origin and consciousness_model (if P3 can't resolve them).

## Next briefs to write
F2 (triple-track for the 347 unchecked formulas), P4, P5, L2b (action forks, after P3),
L3b (reason per invalid D-028 Betti class; then pre-register D-029).
