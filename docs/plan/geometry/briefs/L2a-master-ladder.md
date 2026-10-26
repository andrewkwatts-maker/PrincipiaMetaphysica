# Brief L2a: one master action as a checked ladder (2026-10-27)

Plan: `track_l_action_ladder.md` (PM ladder). Audit: `master_action_audit.md`; read §1, §3,
§5 and §7. Engine: `metaphysica.actions` (L1, merged c9c1f2f); read the package first.
Goal: the master action is well defined. Every term is either fully specified (dimension,
coefficient source, provider) or reported OPEN with the audit item that blocks it, and every
step down the chain is checked. This lane doesn't decide physics; owner items stay explicit.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-masterladder -b claude/masterladder core-paper`. Work only there (W below).
- Copy `src/metaphysica/_physica_core.cp313-win_amd64.pyd` from the main checkout into W.
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/l2a/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Commit on `claude/masterladder` only, with no AI attribution or Co-Authored-By lines. Never push.
- New files only, plus additive edits inside `src/metaphysica/actions/`. Other lanes are editing
  formula LaTeX in the simulations, the website, `variants*`, `testground/`, `theories/pm` and
  `build.py`. Don't edit published formula text: the rendering step comes after lane F1.

## 1. Generic: spinors (`actions/spinors.py`, theory-agnostic)
- `dirac_dim(D) = 2**(D // 2)`. `weyl_dim(D)` is half of that for even D and raises for odd D.
  `majorana_allowed(s, t)` and `majorana_weyl_allowed(s, t)` use the standard (s − t) mod 8
  table. Cite Polchinski Vol. II App. B or Van Proeyen, "Tools for supersymmetry" (1999),
  Table 3.
- `product_spinor_dim(D1, D2)`: the Dirac dimension of the spinor on a product
  M^{D1} × M^{D2} from the factors' spinors. When both factors are odd it is
  2 · dirac(D1) · dirac(D2); otherwise dirac(D1) · dirac(D2). Check it equals `dirac_dim(D1 + D2)`.
- Term-level check: a Dirac mass or a (ΨbarΨ)² term on a field declared Weyl in even D is a
  failing Check ("mass term vanishes for a Weyl spinor"). Add `chirality` to `Field` only if
  needed, defaulted so existing tests still pass.
- Controls, computed with a failing control each: 4D Dirac 4 and Weyl 2; 10D (9,1)
  Majorana-Weyl allowed with 16 real components; 11D (10,1) Majorana 32; 4D Euclidean (4,0)
  has no Majorana-Weyl; the product rule gives 2 · 2 · 2 = 8 for 3 + 3 = 6. Tests go in
  `tests/actions/test_spinors.py`.

## 2. PM: `src/metaphysica/simulations/PM/gauge/master_ladder.py` (may import actions)
- Build `Action`s for 26D (24,2), 13D (12,1) shadow, 6D (5,1) and 4D (3,1), following the
  chain in `geometry/geometric_anchors_core.py`. Build `Reduction`s between them: 26 → 13 over
  the bridge, 13 → 6 over G2 (7,0) with betti from the adopted seed, 6 → 4 over KK. The
  coefficient maps follow the audit's ruled forms (e.g. M_Pl² for the 13D shadow on a 9D
  internal space is M_*^{11} Vol_9). Each coefficient's `provider` is the simulation id that
  produces it, or the term is OPEN.
- The 26D action is the audit §3 canonical statement, one term per summand. L_C, V_bridge,
  V_face, V_tor, OR^i and rho_breath are OPEN with their audit reference.
- `OWNER_ITEMS`: a dict from audit §7 item number to `(question, options, recommended,
  reason)`. The ladder runs under `recommended` and records which items it used. My
  recommendations, to encode (state any you think wrong in the report, with the reason):
  - item 2 Weyl vs Dirac: two options, each run. Weyl 4096 with m and λ dropped, and Dirac
    8192 keeping them. Recommended: Weyl, because it matches the 2026-08-31 signature ruling.
  - item 4: exponent 24 (D − 2); already a convention.
  - item 5: mostly-plus, Riemann sign as in MTW.
  - item 11: computed by `product_spinor_dim(13, 13)` and `weyl_dim(26)`; record what it gives
    and which of the two engine claims it supports.
  - others: no recommendation, `recommended=None`. Their dependent terms are OPEN.
- `report(option_overrides=None) -> dict`: the L1 `Ladder` report plus `owner_items_used`,
  `open_terms` (term id → audit ref) and the spinor counts. Deterministic and JSON-ready.
  A `__main__` writes it to a given path.
- Read-only cross-check: list every published action formula (formulas.json from
  `PM_PUBLISHED_ROOT`, default `H:/claude-scratch/runs_g/active`, ids matching
  `action|lagrang`) and map each to a ladder step, a reduction of it, or `retire`, as a table
  in `PrincipiaMetaphysica/docs/plan/geometry/master_ladder_map.md`. Rendering from the single
  source is the next lane; don't edit those formulas.

## 3. Tests: `tests/test_master_ladder.py`
- The report is deterministic.
- Every non-OPEN term balances dimensionally at its step.
- Every coefficient names a provider that exists (an importable simulation id), or is OPEN.
- The Weyl and Dirac runs differ only in the mass and quartic terms and the spinor counts.
- A ratchet: the number of OPEN terms and failing checks under the recommended options only
  goes down (record the current numbers).
- Acceptance: the new tests pass; `tests/actions`, `tests/testground` and
  `test_master_action_is_one_consistent_statement` still pass.

## If the brief is wrong
If a stated rule disagrees with a computation or a cited table, recheck the convention. If it
still disagrees, stop and report with the exact numbers. Don't change a reference to make a
test pass.

## Report (≤ 15 lines)
The commits; files with line counts; the spinor control results; the ladder verdict and first
failure under each spinor option; the OPEN terms; the counts in the map table (step, reduction,
retire); your view on each recommendation.
