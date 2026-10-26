# Brief F1: a LaTeX render gate, one MathJax config, formula lints, and fixing every hit (2026-10-27)

Plan: `PrincipiaMetaphysica/docs/plan/paper/track_f_formulas.md` (State lists the 11 known hits).

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-texgate -b claude/texgate core-paper`. Work only there (W below).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/f1/`.
  A working probe is in `../texprobe/` (`probe.js`, `probe2.js`): read it, reuse what helps.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Commit on `claude/texgate` only, with no AI attribution or Co-Authored-By lines. Never push.
- Other lanes are editing `simulations/core/variants*`, `testground/`, `theories/pm`,
  `build.py`, the new `src/metaphysica/actions/` and `LEGAL.txt`. Don't edit them. If
  `build.py` must change to run the gate, report the exact change instead of making it.
- Static pages: edit `src/metaphysica/website/` only. Builds overwrite the site copies.
- Don't consolidate or rewrite master-action statements; lane L2a does that. Fix only what
  fails to render there.

## 1. The checker: `tools/texcheck/` (node, dev only)
- `package.json` pins `mathjax-full` at exactly 3.2.2 (Apache-2.0) and commits a
  `package-lock.json`. `node_modules/` is gitignored.
- `check.js <inputs...>` reads formulas.json (`latex`, `eml_latex`, `arithma_latex`),
  sections.json (`content` of `formula`/`equation` blocks) and HTML files (delimited math,
  scripts stripped, HTML entities decoded first). It writes JSON
  `{checked, errors: [{surface, where, id, latex, error}]}` sorted, and exits 1 on any error.
- Errors are a thrown TeX error, an `merror` node, or an undefined macro (`noundefined` output).
- It loads the TeX config and macros from the shared config file in §2, so the gate and the
  site can't drift. Package set: the one `tex-mml-chtml` loads (base, ams, newcommand,
  noundefined, require, autoload, configmacros); say in the report if autoload has to be
  approximated.

## 2. One MathJax config for the site
- New `src/metaphysica/website/js/mathjax-config.js`, the one config. It holds the current tex
  options (delimiters, processEscapes, tags: 'ams') and `macros` with `slashed`. Pick a
  definition that renders well, render it to SVG in scratch with mathjax-full, and name the
  file in the report so the owner can look.
- Replace the inline config in all 12 files that load MathJax (grep `mathjax@3`) with this file.
  Pin the CDN URL to `mathjax@3.2.2`.
- Generators that emit MathJax config (grep `MathJax` in `src/metaphysica/generators`) use
  the same file or the same macros. Report each one.

## 3. Formula lints: `src/metaphysica/generators/formula_lint.py`
Pure functions over (id, latex), each a check returning findings:
- `measure`: `\int d^{D}x` with D = 26 needs `\sqrt{|G...|}`, and D in {4, 6, 11, 13} needs
  `\sqrt{-g...}`. Take the signature table from one place, the chain comment in
  `geometry/geometric_anchors_core.py`, and say where it now lives.
- `planck_exponent`: `M_*^{n}` under `\int d^{D}` needs n = D − 2.
- `superseded`: `superseded_scan.is_hit` on the formula's latex and plain_text.
Each lint needs a test with a passing and a failing example.

## 4. Fix every hit at its source
- Run the checker and the lints on a fresh `metaphysica.build --fast` with output in scratch
  (check `--help`). Fix each hit in the simulation, section or page that emits it.
  `grep` for the latex text to find the source.
- Fix TeX, not physics. For a lint hit that is a real physics error (e.g. `\sqrt{-G}` in 26D),
  fix the notation only when the audit `geometry/master_action_audit.md` already rules on it.
  Otherwise list it in the report for the owner.
- Rebuild and rerun until there are 0 render errors.

## 5. Tests
- `tests/test_tex_renders.py`: run the checker on the published build (`PM_PUBLISHED_ROOT`,
  the same pattern and skip as `test_superseded_surfaces.py`) and on the website source.
  `CEILING = 0`. Skip with a clear reason when node or `tools/texcheck/node_modules` is
  absent. One fixture string per error kind proves the checker catches it.
- `tests/test_formula_lint.py`: the lints, plus a ratchet on the published build at the
  count you leave. Ceilings only go down.
- `tests/test_mathjax_config_single.py`: no HTML under `website/` has an inline
  `MathJax = {`; every MathJax script tag is the pinned URL.
- Acceptance: the new tests pass; `test_latex_registry`, `test_superseded_surfaces` and
  `test_master_action_is_one_consistent_statement` still pass.

## If the brief is wrong
Stop and report the precise conflict (file:line). Don't redesign.

## Report (≤ 15 lines)
The commits; files changed; render errors before → after per surface; each lint's count
before → after, with the physics-level hits left for the owner (id + one line); the `slashed`
SVG path; the build.py change needed to run the gate per build; the dev-dependency line for
LEGAL.txt.
