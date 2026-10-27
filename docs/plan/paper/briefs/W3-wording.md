# Brief W3: close the callout loophole, then real rewrites (2026-10-27)

Plan: `track_f_formulas.md` (Target 5). Follows W2 (merged in part, 30fd32a). Read W2's
Checkpoint at the end of `W2-wording.md` first.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-wording3 -b claude/wording3 core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/w3/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Never kill processes by name (no `taskkill /IM python.exe`, no `Stop-Process -Name`). Kill
  only PIDs you started; other sessions share this machine.
- Budget: about 60 tool calls; hard stop at about 100 turns. Near it, commit what passes, write a "## Checkpoint" (done / not done / next) at the end of this brief, report and stop.
- Commit on `claude/wording3` only, with no AI attribution or Co-Authored-By lines. Never push.
- Change words, never values. Don't edit the formula text of the 31 action formulas in
  `../geometry/master_ladder_map.md`.

## 1. Close the loophole first (`generators/superseded_scan.py`)
A hit counts as `in_callout` when `SUPERSEDED_MARK` appears anywhere in its text or nearby,
so writing "(Superseded path)" inline excuses a hit without changing what the reader sees. Make
`in_callout` true only inside the shared callout itself (find how the callout is emitted, and
match its element or block type, not its text). Test: an inline "(Superseded path)" inside an
ordinary sentence is still a hit; a hit inside the real callout is not. Re-measure and set
`CEILINGS` (autogen is 159 under the old rule; the new rule can only raise it). Record both
numbers.

## 2. Rewrite stale text where it is generated
Biggest sources (W2's checkpoint): `path_graph` 30, `theory_output` 28, the
`geometric_anchors` chain and exports 24, `formulas.json` 7, `identity_ledger` 7. For each
source, find the string that generates the text and fix it with W1's three ways: rewrite it
for the active path, move it into the real callout, or delete it. Fork-option descriptions of
superseded options belong in the callout the site renders for that option, not in the
sentence itself. Lower the ratchets to what you reach.

## 3. Concise: the abstract, introduction and conclusion first
Split sentences over 40 words without dropping content (317 now). Lower the prose_lint ratchet.

## Not in scope
The 21 duplicate groups with a keeper: merging them needs an owner decision (drop the shared
output parameter from the others, or change their latex). Leave them.

## Acceptance
On a fresh `metaphysica.build --fast` in scratch with `PM_PUBLISHED_ROOT` pointing at it:
`test_superseded_surfaces`, `test_superseded_geometry_prose`, `test_tex_renders`,
`test_formula_lint`, `test_prose_lint`, `test_duplicate_statements`, `test_core_paper`,
`test_retired_pattern_pinned` and the new scan tests pass.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; the autogen count under the old and new rule; each count before → after.

## Checkpoint (2026-10-27, branch claude/wording3 in ../metaphysica-wording3)
Done: section 1 (scanner: only the shared callout block/lead or retired wording excuses a hit; the
"Superseded path" label struck from the retired-wording check; 2 new tests). Autogen active hits
144 under the old rule and 144 under the new (the loophole was not yet used in the build);
then 144 -> 98 by rewriting: geometric_anchors chain/export data (24), ~14 generator strings
(chirality, foundations, mass_ratio, geometric_anchors, results ...). Long sentences 317 -> 288
(shared callout split; abstract g2_geometry); filler 5->2, version_tag 14->0 (measured).
Not done: path_graph 46 (testground history graph, P3b territory), variants.json 14 (fork notes),
theory_output remainder, identity_ledger 7 (claim ids), formulas.json 3; long sentences in the
introduction and conclusion.
