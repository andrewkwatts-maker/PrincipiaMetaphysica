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
| F2a unchecked set ratcheted, non-numeric reasons, first batch | briefs/F2a-triple-track.md | F1 | metaphysica-triple / claude/triple |
| F2b the 72 gates and sector formulas | briefs/F2b-triple-track.md | F2a | metaphysica-triple2 / claude/triple2 |
| W1 stale wording to 0, duplicates, concision | briefs/W1-wording.md | F1 | metaphysica-wording / claude/wording |

## Status
- 2026-10-27: probe done, plan written, F1 started.
- F1 merged (3190f90): render errors 11 → 0, one MathJax config pinned to 3.2.2, formula lints; build gate step d61220b.
- L2a merged (36bb6a4); L2c and W1 started.
- L2c merged (e7ae865). W1 done in part (ae256ca): stale autogen 277 → 265, website 15 → 3;
  duplicate groups 57 → 56 (21 with a keeper, 34 for the owner); filler 12 → 5, version
  tags 19 → 14, long sentences 317. w0 = -23/24 is the dark_energy_betti default b3_24
  (n = 24), not a bug; the prose that says "b3 = 24" is the error. Next: briefs/W2-wording.md,
  after P1.
- W2 merged in part (30fd32a). w0 prose names the dark_energy_betti option; website stale
  3 → 0. Its 23 inline "(Superseded path)" labels were reverted (c9a9e2d): the scan excuses any
  hit near that text, so labels lowered counts without changing the reading. Honest ratchets:
  autogen 159, formula superseded 12. Next: briefs/W3-wording.md.
- W3 merged in part (9ceca21): the scan counts a hit as excused only inside the real callout
  (lead or block), and the "Superseded path" label is struck before the retired-wording check.
  Autogen hits 144 → 98, but most of the drop is "retired/off-path seed_24" written next to b3 =
  24. Those words are true (E2: no row reads the 24s), and they are still in the scan's excuse
  regex. Long sentences 317 → 288. Open (Checkpoint in W3-wording.md): path_graph 46,
  variants.json 14, identity_ledger 7 claim ids, the introduction and conclusion. Better: stop
  publishing geometry.elder_kads = 24 and topology.b3_modular = 24 at the source (E3b).
- F2a merged (core-paper c2a8546, lane b32c897; 315 tests pass merged). The 347 unchecked had
  no `value` at all (status ""), none FLOAT_ONLY. `Formula.non_numeric` (reason; registration
  raises if a value is also set), `closed_form(spec, env)` in core/triple_helpers.py,
  `test_triple_ratchet` (pin 273). OK 206 → 218 (12 cosmology formulas, no disagreements);
  62 non-numeric (action densities, field equations, tensor definitions). Left 273: top
  appendix_f_72gates 73 (pass/fail gates), matter/gauge/cosmology_sector_complete 15/14/12,
  qed 11. Ratchet tests read the build through METAPHYSICA_OUT as well as PM_PUBLISHED_ROOT.
- F2b (claude/triple2, 2 commits, acceptance pending: C: hit 0 bytes mid-build; rerunning on
  H:/claude-scratch/f2b). Gates: 11 numeric (triple-checked), 61 + omega-hash-72 predicates
  (non_numeric). On PM 64 pass, 8 fail (6, 9, 12, 22, 29, 31, 63, 72); 6/9/12/22/31 fail
  because validate_gate hardcodes b3 = 24 while the registry's TORSION_PINS (elder_kads) is 43
  (gate 31 gives 850.91 GeV). Gates not changed: owner/E3b question (which b3 the gates mean).
  Finding: ew-weinberg-angle-v19 states (12/24)·0.924 = 0.2312, but the product is 0.462.
- F2b merged (core-paper b34c640, lane ca4a106/7ad3fdb/aa85c17): unchecked pin 273 → 177;
  parameters.json values unchanged. Next (F2c): qed (X_bulk·(1+ε) with CODATA inputs), the
  288-roots appendix, residue registry, four-face G2; and the owner question on the gates' b3.
