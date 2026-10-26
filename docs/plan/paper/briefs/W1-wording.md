# Brief W1: paper wording up to date, stated once, concise (2026-10-27)

Plan: `track_f_formulas.md` (Target 5). Owner request: "paper wordings concise, up to date,
clear". The published text is generated: sections from `simulations/PM/paper/*.py` and the
simulations' formula and parameter descriptions; static pages from
`src/metaphysica/website/` (builds overwrite the site copies, so edit the source).

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-wording -b claude/wording core-paper`. Work only there (W).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W, and
  run `npm ci` in `W/tools/texcheck`.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/w1/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Commit on `claude/wording` only, with no AI attribution or Co-Authored-By lines. Never push.
- Lane L2c owns the 31 action/Lagrangian formulas listed in
  `PrincipiaMetaphysica/docs/plan/geometry/master_ladder_map.md`; don't edit their text. Don't
  edit `variants*`, `testground/`, `theories/pm` or `build.py`.
- Change words, never values. A number in prose that disagrees with `parameters.json` is
  reported, not "fixed" by hand, unless the prose can read the value from the parameter the
  way neighbouring text already does.

## Baseline first
Run a fresh `metaphysica.build --fast` into scratch in the background, then record these
counts on it: `superseded_scan` per surface (ceilings autogen 277, website 15, pages 0), the
`formula_lint` superseded count (13), and §2 and §3 below.

## 1. Up to date: stale wording to 0
Fix each `superseded_scan` hit in one of three ways: (a) rewrite it for the active path
(seed_43_joyce, D-025); (b) move the history into the shared "Superseded path" callout; or
(c) delete it when it adds nothing. Never pass the scan by adding a word from its `_RETIRED`
list to the sentence. Add a test that the `_RETIRED` list doesn't grow: pin its pattern hash,
with a comment saying why. Lower `CEILINGS` in `test_superseded_surfaces.py` and the
`formula_lint` superseded ratchet to what you reach (target 0).

## 2. Stated once
New `generators/duplicate_statements.py`: published formulas grouped by output parameter.
A group with more than one formula whose latex differs is a duplicate statement (e.g. w0). For
each group, keep the formula the parameter's `derivation_formula` names. Point the others'
section references at it, or turn them into a short reference ("see (id)"). Ratchet test at
the count you reach. Report the groups you couldn't merge and why.

## 3. Concise and clear
New `generators/prose_lint.py`, pure functions over (where, text) for sections and page text:
- sentences over 40 words;
- filler: "it is important to note", "it should be noted", "in order to", "clearly",
  "obviously", "essentially", "very", "basically", "note that";
- internal version tags in reader-facing titles and headings (`v22`, `v23.1`, `_v19`);
- an identical paragraph published in more than one section.
Each check needs a test with a passing and a failing example. Fix the hits; rewrite long
sentences by splitting them, without dropping content. Ratchet each count at what you reach,
in `tests/test_prose_lint.py`.

## Acceptance
On a fresh build with `PM_PUBLISHED_ROOT` pointing at it: the new tests pass, and
`test_superseded_surfaces`, `test_superseded_geometry_prose`, `test_tex_renders`,
`test_formula_lint` and the formula-reference tests pass. The render gate stays at 0.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; each count before → after (stale per surface, formula superseded, duplicate
groups, each prose check); prose numbers that disagree with parameters.json (id + both values);
the duplicate groups left for the owner.
