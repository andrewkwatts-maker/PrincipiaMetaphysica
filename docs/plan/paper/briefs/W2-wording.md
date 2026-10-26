# Brief W2: finish the wording ratchets W1 left (2026-10-27)

Plan: `track_f_formulas.md` (Target 5). Follows W1 (merged); start after P1 merges, because
the remaining stale hits come from `variants.py` output.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-wording2 -b claude/wording2 core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/w2/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/wording2` only, with no AI attribution or Co-Authored-By lines. Never push.
- Change words, never values. Don't edit the formula text of the 31 action formulas in
  `../geometry/master_ladder_map.md`; they render from the ladder.

## 1. w0 and b3 = 24
`cosmology.w0_derived` = -23/24 is right: it comes from the `dark_energy_betti` fork's
default option `b3_24` (n = 24), not from the geometry's b3 (43 on seed_43_joyce). The prose that
says "b3 = 24" is wrong. Say instead that n comes from the dark_energy_betti option, and
read n and w0 from the parameters the way neighbouring text already does
(`late_time_routes.de_betti_n`). The same applies to the arithmetic text "With b3 = 24 this is
23/24" and to `config/core_formulas.py` lines 398-412.

## 2. Stale wording to 0
Fix the remaining `superseded_scan` hits (autogen 265) with W1's three ways: rewrite, move into
the "Superseded path" callout, or delete. Most come from `variants.py` / `path_graph` /
`theory_output` description strings. The `_RETIRED` pattern stays pinned. Lower `CEILINGS`
and the `formula_lint` superseded ratchet (13) to what you reach.

## 3. Stated once
Merge the 21 duplicate groups that `duplicate_statements.py` gives a keeper. Point the others
at the keeper with "see (id)". Lower the ratchet. Leave the 34 groups that have no keeper, and list them.

## 4. Concise
Split sentences over 40 words without dropping content (317 now). Start with the sections
readers see first: the abstract, introduction and conclusion. Lower each prose_lint ratchet.

## Acceptance
On a fresh `metaphysica.build --fast` in scratch with `PM_PUBLISHED_ROOT` pointing at it:
the W1 tests, `test_superseded_surfaces`, `test_superseded_geometry_prose`, `test_tex_renders`,
`test_formula_lint`, `test_master_action_single_source` and the formula-reference tests
pass. The render gate stays at 0.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; each count before → after; the groups left for the owner.

## Checkpoint (2026-10-27, branch claude/wording2 in ../metaphysica-wording2)
Done: section 1 (w0 prose and core_formulas.py 398-412 now say n = 24 from dark_energy_betti);
stale autogen 160 -> 118 (fresh --fast build; the 265 in the plan predates P1), website 3 -> 0,
formula_lint superseded 13 -> 0; ceilings lowered. Fork-history strings in
`simulations/core/variants/catalogue/*.py` got an inline "(Superseded path)" label (23 places;
reads clumsily, a rewrite is nicer).
Not done: remaining 118 autogen hits (path_graph 30, theory_output 28, geometric_anchors chain/export 24,
formulas 7, identity_ledger 7, rest singles) are long-tail strings in many modules; section 2 tail,
section 3 (21 keeper groups, 56 groups now; non-keepers share an output_param, merging means
dropping it from their output_params or changing latex, which needs an owner call), section 4
(317 long sentences, abstract/introduction/conclusion first).
