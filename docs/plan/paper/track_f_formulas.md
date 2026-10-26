# Track F: every published formula renders, is correct, and is stated once (2026-10-27)

Owner requests: "paper wordings concise, up to date, clear"; "master action well defined,
all formulas' LaTeX rendered correctly, correct formulas".

## State (probe of build `H:/claude-scratch/runs_g/active`, MathJax 3 TeX parse, all packages)
- No test parses the LaTeX. `test_latex_registry` checks brace balance only;
  `formula_renders.json` is the EML diagram pipeline, not TeX.
- Parsed 1,828 math strings: formulas.json 931 (latex, eml_latex, arithma_latex), sections.json
  560 equation/formula blocks, site pages 337 delimited spans. Errors: 11.
  - `\slashed` is not a MathJax macro (red on the site): reduced-lagrangian-4d,
    bulk-action-26d-v23, master-action-two-layer-or.
  - `\quadN_1` (missing space): gaugino-racetrack-superpotential.
  - `_` inside `\text{}`: sections block "b_1 = 0 ... b_2 is unconstrained" (twice).
  - Site: appendices.html `^` inside `\text{}`; consciousness-speculative.html `\kaf`;
    faq.html a stray `\)` and an HTML-escaped `&lt;` inside math.
- The site loads `mathjax@3` unpinned from the CDN in 12 files, each with its own inline config.
- Correctness: triple-track status is OK 206, RULED_DIVERGENCE 29, unchecked 347 of 582.
- 31 action/Lagrangian formulas, with at least six separate 26D master-action statements:
  pneuma-master-action-v23, master-action-26d-full, master-action-two-layer-or,
  bulk-action-26d-v23, lagrangian-hierarchy-complete (26D with `\sqrt{-G}`, the wrong measure
  for two times), plus the 13D/4D reductions. master-action-two-layer-or puts
  `\int F\wedge\phi` and `-\ln(\text{Vol})\,dt_{\text{phys}}` inside a Lagrangian density.
- Stale wording: the ceilings are autogen 277, website 15, pages 0 (`test_superseded_surfaces`).
  Three formulas still state b3 = 24.

## Target
1. **Render gate (F1):** the site's own MathJax version and config parse every published math
   string with no error or undefined macro. Ratchet at 0, run on every build.
2. **Formula lints (F1):** generic checks on action-like LaTeX. The measure matches the
   signature (two times → `\sqrt{|G|}`, one time → `\sqrt{-g}`); `M_*^{n}` under
   `\int d^{D}` has n = D − 2; no superseded vocabulary (superseded_scan) in a formula.
3. **One master action (L2a, Track L):** `gauge/master_action.py` is the single definition.
   Every published action statement renders from it or is a labelled reduction of it, and the
   L1 dimension check passes per step. The duplicate statements above are retired, not edited.
4. **Correct values (F2):** extend the triple track to the 347 unchecked formulas, or mark each
   one non-numeric with a reason.
5. **Wording (W1):** autogen 277 → 0 and website 15 → 0 stale hits. One statement per quantity
   (Track C3: w0 is published twice). Concision rules for section prose.

## Lanes
| Lane | Brief | Depends on | Worktree / branch |
|---|---|---|---|
| F1 render gate, shared MathJax config, formula lints, fix all hits | briefs/F1-render-gate.md | none | metaphysica-texgate / claude/texgate |
| L2a master action as a checked ladder | ../geometry/briefs/L2a-master-ladder.md | L1 | merged 36bb6a4 |
| L2c render action formulas from the ladder; retire duplicates | ../geometry/briefs/L2c-render-from-ladder.md | L2a, F1 | metaphysica-ladderrender / claude/ladderrender |
| F2 triple-track coverage of the unchecked 347 | (write after F1) | F1 | |
| W1 stale wording to 0, duplicates, concision | briefs/W1-wording.md | F1 | metaphysica-wording / claude/wording |

## Status
- 2026-10-27: probe done, plan written, F1 started.
- F1 merged (3190f90): render errors 11 → 0, one MathJax config pinned to 3.2.2, formula lints; build gate step d61220b.
- L2a merged (36bb6a4); L2c and W1 started.
