# Brief L1: the action-ladder engine and its established-physics controls (2026-10-27)

Plan: `PrincipiaMetaphysica/docs/plan/geometry/track_l_action_ladder.md` (read Design).
This lane is generic only: no PM physics. The engine earns trust by re-creating known
physics, and every check has a failing control.

## Where to work
- Create the worktree: `git -C H:/Projects/MathsPhysicsEcosystem/metaphysica worktree add
  ../metaphysica-ladder -b claude/ladder core-paper`. Work only there (W below).
- Every Python command: `PYTHONPATH=W/src`. Check this once.
- Scratch: `C:/Users/Andrew/AppData/Local/Temp/claude/h--Projects-MathsPhysicsEcosystem-periodica/0e04300a-6655-4024-b6d7-a1accd423861/scratchpad/l1/`.
- Don't sleep or poll. Run long commands in the background and wait for the notification.
- Commit on `claude/ladder` only, with no AI attribution or Co-Authored-By lines. Never push.
- Other lanes are editing `simulations/core/variants*`, `testground/switches`, `theories/pm`
  and `build.py`. Don't edit them.
- sympy (BSD) is already a dependency. Add no new dependency.

## Package `src/metaphysica/actions/` (one concept per file, ≤ 300 lines, functions ≤ 60)
1. `model.py`: frozen dataclasses.
   - `Field(name, kind, components, mass_dim)`, with kind in scalar, vector, spinor,
     form:p and metric.
   - `Coefficient(symbol, mass_dim, source, provider)`, with source in INPUT, DERIVED,
     CALIBRATED and OPEN. `provider` is a string id or None and is required unless OPEN.
   - `Term(id, coefficient, factors: Tuple[(field_name or "R" or "d"), ...], derivatives,
     sign, open: bool)`. Mass dim = coeff + sum of field dims + derivatives (R counts 2).
   - `Action(id, dim, signature: (s, t), fields, terms, convention)`, with convention in
     mostly_plus and mostly_minus.
   - Validate at construction: unknown field names; s + t == dim; duplicate ids.
2. `dimensions.py`: canonical field dimensions in D: scalar (D−2)/2, spinor (D−1)/2,
   vector (D−2)/2. Use exact `Fraction`. `check_action(action) -> List[Check]` covers each
   term balancing to D, a source named for every coefficient, and OPEN only where
   `term.open`. `Check(id, measured, holds, can_fail, source, detail)`.
3. `reduction.py`: `InternalSpace(name, dim, ricci_flat, betti: Mapping[int, int] or None,
   volume_symbol)` and `Reduction(parent, child, internal, coefficient_map)`. The
   coefficient map is child symbol → sympy expression in the parent symbols and
   `volume_symbol`. `check_reduction` checks dims add up, signature times are preserved or
   the change is declared, and each mapped coefficient's mass dimension equals the child's
   (using Vol mass dim −dim). Zero modes are checked when betti is given and the step
   declares a `zero_mode_rule` (a function of betti → expected field counts).
4. `correspondence.py`: `Correspondence(id, step, reference, compute) -> Check`. The
   `ladder.py` `Ladder(steps)` returns a report dict: per step, its checks; `verdict` is
   VALIDATED or the first failing check id. The report is deterministic and JSON-ready.
5. `curvature.py`: sympy helpers `christoffel`, `ricci_tensor`, `ricci_scalar` and
   `einstein_tensor(metric, coords)`, with `simplify` used deliberately. Add a one-line note
   that this belongs in Arithma once its calculus bodies land.
6. `controls/`, the established physics, each as a `Correspondence` plus a failing control:
   - `kaluza_klein.py`: 5D metric `g_mn = η_mn + φ² A_m A_n`, `g_m5 = φ² A_m`,
     `g_55 = φ²`, with A, φ arbitrary functions of the 4 coordinates. Check
     `R_5 = −(1/4) φ² F_mn F^mn − (2/φ) □φ` symbolically (flat 4D part), and numerically
     at seeded points with a polynomially perturbed 4D metric (`R_4` term added). Also
     check `G_4 = G_5 / (2π L)`. Reference: Overduin and Wesson, Phys. Rep. 283 (1997) §2.
     Control: dropping the φ² in `g_m5` breaks it.
   - `ricci_flat_compactification.py`: on M4 × K with K Ricci-flat, R_D = R_4 (computed for
     a product metric with a flat torus K, and a non-flat K control: S² gives
     R_D = R_4 + 2/r²). Also check `M_Pl^2 = M_*^(D−2) Vol(K)` passes the dimension check.
   - `g2_zero_modes.py`: the citation-level counting rule for 11D supergravity on a G2
     manifold, giving b2 U(1) vectors and b3 neutral chiral multiplets in 4D N = 1
     (Papadopoulos and Townsend 1995; Acharya 1998). Provide it as a `zero_mode_rule`. Run
     it on a known Joyce example and record the numbers; don't apply it to PM.
   - `four_d.py`, each computed in sympy:
     - Schwarzschild is Ricci-flat (control: wrong g_rr power);
     - the static weak-field metric gives `∇²Φ = 4πGρ` from G_00 (control: wrong sign);
     - flat FLRW `G_00 = 3 (ȧ/a)²` gives `H² = 8πGρ/3`;
     - Euler-Lagrange of `−(1/4) F²` gives `∂_m F^mn = 0`;
     - the dimension check passes for 4D EH + Maxwell + Dirac + Higgs quartic and fails for
       `λ φ⁴` in 6D with dimensionless λ.
   - `controls/__init__.py`: `standard_ladder()` = the textbook ladder
     5D GR → (S¹) → 4D GR + Maxwell + dilaton → 4D checks, which must be VALIDATED.
7. An AST test: `metaphysica.actions` imports nothing from `metaphysica.simulations`,
   `generators` or `website`. Copy the testground contract test's approach.

## LEGAL.txt
metaphysica has no `LEGAL.txt` at its root. Create one listing every runtime dependency in
`pyproject.toml`, with the installed version and licence read through `importlib.metadata`
(a short script in scratch, not committed), plus the Arithma submodule if present. Flag any
non-permissive licence in the report; don't remove anything.

## Tests: `tests/actions/test_*.py`, deterministic
One per control and its failing control, the model validation errors, the dimension rules,
the reduction checks, and `standard_ladder()` giving VALIDATED. Keep the whole folder
under 60 s (cache the expensive sympy results within the test module).
Acceptance: the new tests pass; `tests/testground` still passes; ruff is clean on the new
package, if ruff is installed.

## If the brief is wrong
If a stated formula disagrees with sympy, recheck the convention first. If it still
disagrees, stop and report the derivation with the exact expressions. Don't change a
reference formula to make a test pass.

## Report (≤ 15 lines)
The commits; files with line counts; each control's result and its failing control; the
sympy runtime per control; the LEGAL.txt licence list summary; what should move to Arithma.
