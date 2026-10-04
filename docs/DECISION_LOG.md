# Decision log — the active path

Every change to the active switch path, and every hypothesis that could move a
published number or a published justification, is written here BEFORE it is
computed and committed first. Git history then proves the result could not have
chosen the decision. Results are appended to the same entry afterwards, never
edited into the pre-registered text.

Companion records: the live register (`OUTSTANDING_ISSUES.md`) carries the
narrative; this file carries the decisions and their evidence.

## How decisions are made (author's delegation, 2026-09-30)

The author delegated working decisions to the lead: make the assumptions and
conclusions needed to keep the geometry closing and the physics accurate, test
every option for the tightest closure, isolate dead ends so they can be switched
out, and keep the active path current. Three foundational rulings still go to the
author explicitly — the real form of φ, χ_eff, and Re(T) — and the author can
overturn anything at a checkpoint digest.

**Decision rule.** Options are ranked by, in order:

1. Mathematical validity — derivable, type-correct (every quantity states what it
   counts; nothing is converted silently), contradiction-free. A hard gate.
2. Closure — fewer free inputs; the zero-parameter geometry is never broken to fit.
3. Cross-domain consistency — identity ledger, triple-track, whole-family sweep.
4. Elegance — fewer special cases, one mechanism doing more work.
5. Empirical adequacy — used as a TEST. Choosing between options that tie on 1–4
   by agreement with data is allowed only if disclosed, with its trials factor, and
   counted as a fitted degree of freedom.

An option that fails 1–3 is never adopted because it matches data better.

**Working assumptions** are allowed and labelled. Each states the claim, why
closure needs it, what it costs, at least one NEW testable consequence beyond the
problem it solves, and its kill condition. A patch with no new consequence is a
degenerating move and is not adopted.

**Dead ends** — structurally refuted, a value match with no object behind it,
agreement only on a retired seed or calibration, one new input per problem solved,
or a fired kill condition — are demoted (fork priority 2), labelled with the
evidence, kept runnable, and never deleted. Switching one back in is one
environment variable.

**Entry format.** Question · hypothesis · discriminating test · kill condition ·
consequence if confirmed · status. Status moves PRE-REGISTERED → CONFIRMED /
KILLED / REVISED, with the result and its independent verification appended.

---

## D-001 · 2026-09-30 · G0 · PRE-REGISTERED

**Question.** Is χ(Y₇) = 0 derived from the construction, and is the resolved
Betti sequence of every reachable profile what the pipeline declares?

**Hypothesis.** For an A1-admissible assignment with n singular involutions
(n ∈ {0, 1, 2, 3}), Joyce's resolution formula
H^k(Y) = H^k(T⁷/Γ) ⊕ ⊕_j H^{k−2}(L_j), with the flat sector (1, 0, 0, 7, 7, 0, 0, 1)
from the Γ-invariant forms and each L_j = T³/Stab_j computed from its stabiliser's
action on the fixed coordinates, gives:

- 4n singular components, every one a plain flat T³ with Betti numbers (1, 3, 3, 1)
  (the stabiliser acts trivially on the fixed coordinates under A1);
- b(Y) = (1, 0, 4n, 7 + 12n, 7 + 12n, 4n, 0, 1); Poincaré duality holds;
- χ(Y) = 0 on every profile. At n = 3: (1, 0, 12, 43, 43, 12, 0, 1).

The off-family seed_24 cannot be constructed this way; for it, χ = 0 follows from
Poincaré duality alone and is labelled declared, not derived.

**Discriminating test.** Compute the sequence from a representative assignment of
each profile (the adopted one is `intersection_tensor.canonical_point()`) and
compare (b₂, b₃) with `b3_path.PATHS`.

**Kill condition.** A derived (b₂, b₃) that differs from the declared profile; a
Poincaré-duality failure; any component that is not a flat T³ with b₁ = 3 at the
adopted point.

**Consequence if confirmed.** χ(Y₇) = 0 is published as its own formula. The
formula currently called `euler-characteristic` is re-scoped: it computes an
effective index (χ_eff, unruled — G1) from Hodge numbers, and Hodge numbers are
not defined on a real 7-manifold, so it is not the Euler characteristic of Y₇. The
flat-T³ result (b₁(L_j) = 3 for all 12 components) is the input to G2 step 1.

---

## D-002 · 2026-09-30 · G0 · PRE-REGISTERED

**Question.** Does anything other than the observed number of generations select
(12, 43) within the reachable family?

**Background.** Today's selection is n_gen = b₂/4 = 3: the observed generation
count picks one of four family members. That is selection by data, with a trials
factor of 4.

**Hypothesis.** π₁(Y) is finite exactly on (12, 43).

- Singular involutions of an A1-admissible assignment are linearly independent over
  F₂ (if σ and τ are singular with disjoint fixed sets, στ is not singular), so the
  rank of their span is n = b₂/4.
- If the span is a proper subgroup, some coordinate c is fixed by every singular
  involution: the seven coordinates carry the seven non-trivial characters of Γ
  bijectively, and a proper subgroup has a non-trivial annihilator. The projection
  of the affine group G onto the c-th coordinate, G → Isom(ℝ), kills every element
  that has a fixed point (such an element acts on x_c with sign +1 and shift 0), so
  it kills the subgroup E those elements generate. It sends the translation t_c to
  x ↦ x + 1, so t_c has infinite order in π₁ = G/E. Expected counts of surviving
  directions: 7, 3, 1, 0 for n = 0, 1, 2, 3.
- If the span is Γ, the existing criterion (`fundamental_group.
  pi1_triviality_criterion`) gives π₁ = 1.

**Consequence, cited rather than computed.** For a compact torsion-free
G₂-structure, Hol = G₂ if and only if π₁ is finite (Joyce, *Compact Manifolds with
Special Holonomy*, OUP 2000). By the Cheeger–Gromoll splitting, infinite π₁ means
the universal cover is ℝ^k × N, so the restricted holonomy is reduced: flat, SU(2)
and SU(3) for n = 0, 1, 2. So within the reachable family, only (12, 43) is a
G₂-holonomy manifold in the strict sense. The family is the tower of special
holonomies in seven dimensions, with full G₂ at its top.

**Counterpoint recorded in advance, so the wrong argument is not made.**
Supersymmetry does NOT discriminate between the members. Under G₂ the spinor is
1 ⊕ 7, and extra parallel spinors correspond to parallel 1-forms. By Bochner's
argument on a compact Ricci-flat manifold, parallel 1-forms are the harmonic ones,
and b₁ = 0 on every member. So every member gives N = 1 in four dimensions. The
selection is holonomy, not supersymmetry.

**Discriminating test.** On a representative of each profile, and swept over every
A1-admissible assignment: the rank of the singular span equals n; the set of
coordinates fixed by all singular involutions has size 7, 3, 1, 0; π₁ is finite
iff that set is empty; and this agrees with `pi1_triviality_criterion`.

**Kill condition.**
- A seed_19 or seed_31 representative with finite π₁.
- The adopted point failing π₁ = 1.
- Any A1-admissible assignment whose singular involutions are dependent. That would
  break "b₂/4 = rank of the singular span" and force the n_gen wording to change.

**Consequence if confirmed.** (12, 43) is selected by the model's own defining
hypothesis — holonomy exactly G₂ — with no appeal to data. n_gen = b₂/4 = 3 becomes
an output of the selection that is tested against the three observed generations,
instead of the input that chose the point. The trials factor for the seed falls
from 4 to 1.

**Scope.** Holonomy is a Riemannian statement. It applies on the compact real form
(`g2_form_convention = octonion_derived`). The adopted convention is the split form
G₂*, where only the topological half holds: π₁ = 1 exactly at n = 3. Adoption of
this selection route is therefore bundled with the G3 real-form ruling, which is the
author's. Until then it is recorded as a candidate second selection route with that
scope, and it counts as evidence in the G3 packet.

A4 note: "rank(Γ) = 3" in current prose is imprecise. Γ has rank 3 on every family
member; what equals b₂/4 is the rank of the singular span, which equals rank Γ
exactly at the adopted point. Wording is corrected wherever this lands.

---

## D-001 · RESULT · 2026-09-30 · CONFIRMED (lead run)

Each member's representative assignment was found by search. The adopted one is
identical to `canonical_point()`, and the old duplicate search loop now delegates
to the shared one.

| member | derived (b₂, b₃) | resolved Betti sequence | χ | components |
|---|---|---|---|---|
| seed_7 | (0, 7) | (1, 0, 0, 7, 7, 0, 0, 1) | 0 | none |
| seed_19 | (4, 19) | (1, 0, 4, 19, 19, 4, 0, 1) | 0 | 4 × T³ |
| seed_31 | (8, 31) | (1, 0, 8, 31, 31, 8, 0, 1) | 0 | 8 × T³ |
| seed_43 | (12, 43) | (1, 0, 12, 43, 43, 12, 0, 1) | 0 | 12 × T³, each (1, 3, 3, 1) |
| seed_24 | declared only | (1, 0, 4, 24, 24, 4, 0, 1) | 0 by duality | not constructible |

Every derived pair matches its declared profile. Poincaré duality holds on every
row. Every singular component is a flat T³ (b₁ = 3) and every Γ-orbit has 4
members. No kill condition fired.

The falsifiers were checked to have teeth. A non-A1 component is refused rather
than counted, and a lopsided sequence fails the duality check and gives χ = −1.

**Published.** A new certificate module (`PM/geometry/closed_geometry.py`, the
seed of G4) publishes:

- `y7-resolved-betti-numbers`, `y7-euler-characteristic`,
  `y7-singular-components`, and parameter `topology.chi_y7 = 0`;
- each with its statement rendered from the live computation, what it counts, its
  proof, its test, its falsifier and its references.

`euler-characteristic` keeps its id and value, and its labels were corrected: it is
the effective index χ_eff (the open G1 ruling), computed from the Hodge data of the
off-path TCS model, not the Euler characteristic of Y₇.

## D-002 · RESULT · 2026-09-30 · CONFIRMED (lead run), adoption held for G3

**Representatives.** The flat ranks k (coordinates fixed by every singular
involution) are 7, 3, 1, 0. π₁ is infinite on seed_7, seed_19 and seed_31, and
trivial on seed_43. The witness side and the span criterion agree on every row.

**Whole enumeration.** 458,752 assignments were visited. 411,488 are admissible:
176,288, 166,208, 61,152 and 7,840 with n = 0, 1, 2, 3 singular involutions. There
were zero violations:

- the singular involutions are independent every time;
- no admissible assignment has n ≥ 4;
- k = 2^(3−n) − 1 throughout;
- π₁ is finite exactly when n = 3.

No kill condition fired.

**Consequence (cited, compact real form).** Only (12, 43) has holonomy exactly G₂.
The restricted holonomy of the other three members is trivial, SU(2) or SU(3).

**Status of the selection route.** `y7-fundamental-group` publishes the topological
half now, because it holds on either real form. The holonomy reading is computed
(`closed_geometry.holonomy_selection_pending()`) but held back from publication
until the G3 real-form ruling, as pre-registered. It goes into the G3 evidence
packet. If the author adopts the compact form, the seed's selection moves from
"n_gen = 3, chosen by data" to "holonomy G₂; n_gen = 3 predicted", and the trials
factor falls from 4 to 1.

Independent blind verification is running; its verdict is appended below when it
reports.

---

## D-003 · 2026-09-30 · G3 · EVIDENCE PACKET — ruling requested from the author

**Question.** Which real form does φ take: the adopted `all_plus_one` (split
G₂*, induced metric of signature (4, 3)) or `octonion_derived` (compact G₂,
signature (7, 0))? This is one of the three foundational rulings reserved for the
author. The lead has applied the decision rule and recommends; the author decides.

The measurements below were run BEFORE this entry was written, so this is an
evidence record, not a pre-registration. No published number depends on the
outcome, as the first measurement shows.

**1. What moves if φ becomes compact: nothing numeric.** Two full pipelines were
run in fresh processes, one per convention:

- 788 of 788 parameters are identical;
- 226 of 226 formulas with a numeric value are identical;
- the same ids are present under both.

What changes is what is true to write:

- `geometry_narration.holonomy_claim()` switches to "a Riemannian G₂-holonomy
  manifold is available and Joyce's construction applies";
- the generated forbidden-phrase list empties;
- the published "G₂ holonomy" strings, which the ratchet currently counts as false,
  become accurate.

**2. Where the split form comes from: a single sign.** The fork's own record
(opened 2026-09-13) establishes that `g2_structure_as_3form()` returns an all-(+1)
tensor. The framework's own octonion product — verified norm-multiplicative and
alternative — implies a form that differs from it by exactly one sign, on the
triple (1, 3, 5). So the adopted φ is not the form the framework's algebra
produces. It comes from transcribing a textbook sign convention.

**3. What the construction presupposes.** Joyce's existence theorem, which provides
the torsion-free structure on the resolution, is a theorem about the compact form.
The adopted pair (12, 43) is Joyce's own compact example. "Holonomy G₂", "Joyce
manifold" and the metric-moduli statements all name compact-form objects. On the
split form each of these has no object behind it (decision rule, criterion 1).

**4. A selection route that exists only on the compact form (D-002).** Holonomy
exactly G₂ selects (12, 43) within the reachable family. Three generations then
becomes an output tested against data rather than the input that picks the seed,
and the trials factor for the seed falls from 4 to 1.

**5. The det B = 0 "wall" does not distinguish the forms.** Measured on the same
700-point grid (`glued_orbit_scan.scan`), leading order in t:

| t | ≤ 0.1 | 0.5 | 1 | 2 | 5 | 10 | 100 |
|---|---|---|---|---|---|---|---|
| split: orientation flips | 0 | 5 | 15 | 23 | 33 | 38 | 51 |
| compact: points in the other orbit | 0 | 5 | 15 | 23 | 33 | 38 | 51 |

Both forms stay in their home orbit, with fixed orientation, for t ≤ 0.1. From
t = 0.5 up, both depart at the same grid points. The "wall" itself —
`degenerate_records`, i.e. det B sign changes bracketed between neighbouring
radii — is 36 crossings on each form: 3, 6, 6, 7, 7, 7 at t = 0.5, 1, 2, 5, 10,
100, identical on both, and none at t ≤ 0.1. The departure is a property of
the leading-order glued form at large t, not of the real form. The earlier reading
of this as a "dynamically generated singular structure" should be re-scoped on
either branch. That the leading-order form is invalid at t ≥ 0.5 is not
established here; the measured fact is the t-dependence.

**6. What does not depend on the choice.** The diagonal (ℤ/2)³ stabiliser depends
only on φ's support, which both forms share. So the enumeration, the family
b₃ = 7 + 3b₂, the resolved Betti sequences, χ = 0 and π₁ are identical on both.

**Recommendation (lead, under the decision rule).** Adopt `octonion_derived`.

- Criterion 1 (validity): it decides the question outright. The split form
  contradicts the construction the model names; the compact form is what the
  framework's own algebra produces.
- Criterion 2 (closure): nothing numeric moves, and one selection route is gained.
- Criterion 4 (elegance): φ is read off the octonions, not imported.

**Cost of adopting.** A wording sweep. Holonomy language changes from forbidden to
required-accurate, so the holonomy ratchets must be inverted, not merely relaxed.
The `metric_construction` fork (quadratic contraction or Hitchin), which follows
this ruling, must then be decided.

**Revert.** One environment variable: `METAPHYSICA_VARIANT_G2_FORM_CONVENTION`.

---

## D-004 · 2026-09-30 · G5 · PRE-REGISTERED — the rules, before the inventory

**Question.** For every place the number 24, or b₃, enters a computation, what
object does the derivation count? On the old seed every such 24 was called "b₃"
in the code's own text. So a formula that SAYS b₃ is not evidence that its 24 is
b₃. The adoption sweep classified consumers largely by that text, and the line
census (`generate_b3_24_census`) classifies by keywords on the same line. Both
would misfile a bulk 24 written as "b3".

These rules are fixed now, while the inventory is still being gathered, and
before any root has been classified or re-run.

**Object classes.**

| class | the derivation counts | on the adopted seed |
|---|---|---|
| B3 | 3-cycles, harmonic 3-forms, or metric moduli of Y₇ (dim H³) | moves to 43 |
| BULK | the (24,2) bulk: 24 space dimensions, the 12 (2,0) bridge pairs, D_space − 4, the 26D frame | stays 24 |
| NAMED | a constant independent of Y₇: the 24-cell, dim Leech, χ(K3), the modular weight of η²⁴ (bc ghosts), \|S₄\| | stays |
| NONE | nothing: arithmetic or a fit, with no counting reason stated | dead-end candidate |
| MIXED | parts from different classes, or different seeds, combined | split into parts; the mixture is a defect |

**Rules.**

1. **Object, not symbol.** A root is classified by the object its derivation text
   names as the thing counted. The variable name (`b3`, `elder_kads`) is not
   evidence, and neither is whether the resulting value matches data.
2. **Evidence is quoted.** Every classification cites the derivation text it
   rests on, verbatim, with a file and line.
3. **No object means NONE.** If the text gives only arithmetic ("7·24 − 5",
   "one less than decimal b₃ scaling") or a fit, the root is NONE however well its
   value agrees with data. A NONE root is re-labelled a calibration, with its
   trials factor, and is never counted as a derivation.
4. **Two readings means a fork.** If the text names a b₃ object and a bulk object
   for the same factor (for example "b₃/2" beside "the 26D-to-4D warping"), the
   root is AMBIGUOUS. It gets a switch carrying both readings, and rule 5 picks the
   adopted one.
5. **Choosing between readings** follows the decision rule:
   - validity: a reading whose object does not have that count on the adopted
     geometry is invalid — "b₃/2 = 12 bridge pairs" is false at b₃ = 43;
   - closure;
   - consistency: one reading for every consumer of the same root;
   - elegance.

   Agreement with data may not choose. It is scored after the choice, with trials
   factor 2 per ambiguous root, and a reading adopted with only a data advantage
   counts as a fitted degree of freedom.
6. **A MIXED root** is split into its parts, and each part is classified on its
   own. The combination is reported as a defect even when each part is fine: a
   frozen seed-24 numerator over a seed-following denominator is neither model's
   number.
7. **The census heuristics are not evidence.** `generate_b3_24_census` and the
   seed-blindness classifier are used only to FIND candidate lines. Where their
   text-based class disagrees with an object classification, the classifier is
   wrong and is recorded as such.

**Verification.** A separate agent, given these rules and the derivation texts
but not the lead's table, classifies a random sample of at least one third of the
roots, drawn with a fixed seed. Disagreements are resolved on the quoted evidence
and reported, never averaged.

**Kill conditions for the audit itself.**
- The blind agreement rate on the sample is below 80%. The rules are then too loose
  to use, and must be tightened and re-registered before anything is re-wired.
- The audit comes out one-directional by construction. It must be able to confirm a
  recorded cost as well as heal one. If every contested root lands on the reading
  that improves agreement with data, that pattern is itself reported as a sign of
  motivated reading.

**What happens after classification (not before).** Only roots classified BULK or
NAMED whose code reads b₃ are re-wired to read their object. Each is its own
commit with its measured before/after and a one-line revert. NONE roots are
demoted to labelled calibrations. B3 roots keep following the seed, and their
recorded costs stand.

---

## D-005 · 2026-09-30 · G2 · PRE-REGISTERED — does the adopted geometry fix Re(T)?

**Question.** The author asked for "the appropriate pair, with geometric reasons".
Which pair, if any, does the adopted geometry actually carry to fix the metric
moduli at leading order?

**Sources, verified before use.**
- Lukas & Morris, *Moduli Kähler potential for M-theory on a G₂ manifold*, Phys.
  Rev. D 69, 066003 (2004), hep-th/0305078. Eq. (5.10) and Table 1 give K for
  exactly Joyce's T⁷/ℤ₂³: 7 bulk moduli Tᴬ and 36 blow-up moduli U^(τ,n,a), three
  per blow-up, for 12 blow-ups. The formula is valid at large moduli and to
  quadratic order in U/T. The count matches D-001's b₁(L_j) = 3 on each of the 12
  components.
- Acharya, Denef & Valandro, *Statistics of M theory vacua*, JHEP 0506:056 (2005),
  hep-th/0502060, eqs. (3.1)–(3.18): W = N_i zⁱ + c₁ + i c₂, where c is the
  Chern–Simons invariant of the singular locus. Their words: "The addition of
  fluxes when X is smooth does not stabilise these moduli, as the induced potential
  is positive definite and runs down to zero at infinite volume." Stabilisation
  needs a codimension-four locus Q that "admits a complex, non-real Chern-Simons
  invariant … for instance, Q is a hyperbolic manifold."

**Hypothesis: absence at leading order, by three independent routes.**

1. **Flux on the smooth resolution runs away.** Homogeneity of V_X (degree 7/3)
   gives K_i sⁱ = −7 and K^{ij}K_j = −sⁱ. With c₂ = 0 these reduce the potential
   exactly to V = 4 e^K K^{ij} N_i N_j, which is positive definite. Along the
   volume ray s → λs it scales as λ⁻⁵, so dV/dλ = −5V/λ < 0 and there is no
   critical point at finite volume, for any flux. The (N_flat, N_twisted) pair of
   `flux_quantization` gives stationarity of W, which is not a vacuum.
2. **No non-real Chern–Simons invariant at the orbifold point.** Each locus Q is a
   flat T³ (D-001). A flat SU(2) connection on T³ is conjugate into the maximal
   torus, because π₁ = ℤ³ is abelian. Its Chern–Simons invariant is therefore 0,
   so c₂ = 0, and the Acharya mechanism (which needs a hyperbolic Q) is absent.
3. **No gaugino condensation.** Each SU(2) sits on a Q with b₁ = 3, which gives
   three adjoint chirals — not pure N = 1 super-Yang–Mills (Acharya's b₁(Q) = 0
   criterion). The racetrack `a = 2π/b₃` read a Betti number as a gauge rank.

**Discriminating test.**
- Implement the Lukas–Morris K (their Table 1, verbatim) and verify:
  homogeneity, K(λs) = K(s) − 7 ln λ; both identities, numerically at random
  admissible points; V = 4e^K K^{ij}N_iN_j with c₂ = 0 to rounding; and
  monotone decrease along the ray.
- Control: with a hypothetical c₂ ≠ 0, the supersymmetric AdS point with
  W = −(2/5)c₂ must appear, so the solver is shown able to find a vacuum when one
  exists.

**Kill condition.**
- A finite-volume critical point of V with c₂ = 0 for some flux.
- The Lukas–Morris K failing homogeneity or the identities. The general argument
  would then not apply, and the result must be re-derived.
- A flat SU(2) connection on T³ with non-zero Chern–Simons invariant.

**Consequence if confirmed.**
- Re(T) is not fixed by any leading-order mechanism the adopted geometry carries.
  This is published as ABSENCE and replaces the silent 7.086 fallback.
- `re_t_adoption` gains an option recording the absence. `calibrated` stays
  available, labelled as a fitted input with its trials factor.
- The Stage 2 digest presents the author with the real choice: an open modulus,
  a labelled calibration, or research beyond leading order.

**Scope, stated so the claim is not overstated.** This covers classical
supergravity at large volume, the leading-order Kähler potential, G₄ flux, and
gaugino condensation. It does NOT cover membrane (M2) instantons on associative
cycles, corrections to K beyond (U/T)², or quantum corrections. ADV note that the
latter "may change this". Those stay open and are listed as open.

## D-005 · RESULT · 2026-09-30 · CONFIRMED (lead run), the ruling goes to the author

**Numerical check** (`PM/geometry/flux_vacuum.py`; seed 20260930; 40 random
points inside the Lukas–Morris domain, with random fluxes in [−3, 3]⁴³):

| check | worst residual |
|---|---|
| homogeneity K(λs) = K(s) − 7 ln λ | 8 × 10⁻¹⁵ |
| K_i sⁱ = −7 | 3 × 10⁻¹⁵ |
| K_ij sʲ = −K_i | 7 × 10⁻¹⁷ |
| V = 4e^K K^{ij}N_iN_j (c₂ = 0) | 2 × 10⁻¹⁵ relative |
| V(λs) = λ⁻⁵ V(s) | 5 × 10⁻¹⁶ |

- The metric is positive definite at every sampled point (minimum eigenvalue
  2.5 × 10⁻³), and V > 0 at every sampled point.
- The analytic gradient and Hessian agree with central differences to 2 × 10⁻⁹
  and 2 × 10⁻¹¹.
- **The control finds a vacuum when one exists.** With a hypothetical c₂ = −10 or
  25, F = 0 holds exactly at s_A = −c₂/(5N_A), with W₂ = −(2/5)c₂ and V < 0 (AdS).

No kill condition fired.

**Gauge content** (Acharya, hep-th/9812205, quoted verbatim before use). The local
content is "precisely that of pure N = (1 + b₁) super Yang-Mills", and for
M ≅ T³ "those of pure N = 4 super Yang-Mills theory". Every adopted-path locus is
C²/ℤ₂ × T³ with trivial monodromy (D-001), so each carries N = 4 SU(2): no
confinement and no condensate. The b₁ = 0 case Acharya uses for pure N = 1 is
exactly the reflected, non-A1 case that admissibility excludes.

**Published** in the certificate:
- `y7-gauge-content` (CG.5): U(1)¹² on the resolution, N = 4 at each locus;
- `y7-flux-potential-runaway` (CG.6): the measured exponent −5, matching the
  closed form −7 + 2.

Each carries its scope: classical supergravity, large volume, leading-order K,
G₄ flux. Membrane instantons and corrections to K are not covered.

**What the author is asked (Stage 2).** The adopted geometry carries no
leading-order pair that fixes Re(T): no gaugino condensate, a runaway flux
potential, and a real Chern–Simons invariant. The options are:

- (a) **Open modulus.** Re(T) is recorded as undetermined at leading order, and
  every consumer is labelled as depending on an unfixed field value.
- (b) **Labelled calibration.** `re_t_adoption = calibrated`, counted as one
  fitted input with its trials factor.
- (c) **Research beyond leading order.** Membrane instantons on associative cycles
  (which needs a rigidity analysis of the calibrated cycles) or corrections to K.

The lead recommends (a) as the published position, with (c) as the open research
item. (b) would re-introduce a free parameter into a layer the programme is trying
to close. Today's silent 7.086 fallback is a reporting defect under every option,
and is labelled in Stage 3 whatever is ruled.

---

## D-001 / D-002 · INDEPENDENT VERIFICATION · 2026-09-30

A separate agent, told not to open the lead's modules or this log, re-derived
everything from the enumeration primitives and the literature. It also built its
own exact-rational model of the (ℤ/2)³ actions: 4⁷ = 16,384 conjugacy classes,
each of the 28 generating triples enumerating all of them.

- **D-001 CONFIRMED.** Same Betti sequences, Poincaré duality, χ = 0, and every
  component a plain T³ with stabiliser {1, σ}. Cross-checks: the n = 1 member is
  (T³ × K3)/(ℤ₂)², and Joyce's own JDG I example, mapped into codebase coordinates,
  gives (12, 43).
- **D-002 CONFIRMED, then REVISED.**
  - Confirmed: π₁ ≅ p(G), a crystallographic group of rank 2^(3−n) − 1.
    `h1_of_resolution` matches an independent Smith-normal-form computation on all
    14,696 admissible classes. Singular involutions are independent, and n ≤ 3,
    even under disjointness alone (proof via the 4-arc lemma).
  - Confirmed: supersymmetry does not discriminate (N = 1 on every member).
  - The holonomy criterion is Joyce, JDG II, Proposition 1.1.1, which the lead
    read in the source: "the holonomy group of g is G₂ if and only if the
    fundamental group π₁(M) is finite". It is also Joyce (2000), Proposition
    10.2.2, located via a citation only. Cheeger–Gromoll is JDG 6 (1971), Theorem 3.
  - REVISED: see D-006. "(12, 43) alone has holonomy G₂" holds only inside the
    A1-filtered subfamily.
- **Wording defects found and fixed.**
  - `pi1_finiteness`'s two "sides" are logically equivalent, so their agreement
    checks the code, not the mathematics twice.
  - The identification of k needed E = ker p; the proof is now stated.
  - "Joyce states simple connectivity for his examples" overgeneralised: his
    JDG II Examples 1–2 have π₁ = ℤ³ and ℤ.
  - The docstrings' assignment counts are 28-fold redundant, since each
    generating triple parametrises all 16,384 classes. The class counts at
    n = 0/1/2/3 are 6,296 / 5,936 / 2,184 / 280.

## D-003 · ADDENDUM · the split form does not support the resolution

The verifier computed B_φ for the codebase's φ as 6·diag(+, −, +, −, +, −, +):
signature (4, 3). With that φ, 6 of the 7 involutions have a neutral (2, 2)
transverse ℝ⁴, so Eguchi–Hanson — a Riemannian hyperkähler ALE space — is not
even the right local model. On the adopted split form, then, the resolution that
DERIVES (b₂, b₃) is not available. Only the compact form supports the derivation
the seed rests on. This strengthens the recommendation from "the holonomy wording
needs it" to "the seed's own derivation needs it".

---

## D-006 · 2026-09-30 · PRE-REGISTERED — the reachable set, corrected

**Finding (red-team, confirmed by the lead in the primary source).**
`derived_contribution_table.all_components_are_a1` tests a component's SETWISE
stabiliser, not the isotropy at its points.

- Under pairwise disjointness, every stabilising element other than σ acts freely
  on the component, because a fixed point would lie in two singular sets. So every
  singular point is already A1.
- A free extra stabiliser is exactly Joyce's JDG II setting: (T³ × ℂ²/{±1})/F
  with F acting freely, resolved by Theorems 2.2.2–2.2.3 with two choices of
  ℤ₂-action on each Eguchi–Hanson space.
- JDG II §3.1, **Example 4**, read by the lead: α and β give 4 plain T³ each; γ
  gives 8 copies of T³/ℤ₂. Each ℤ₂-action choice contributes (1, 1) or (0, 2).
  The result is "b₂(M) = 8 + l, b₃(M) = 47 − l, l = 0, 1, …, 8" — nine simply
  connected manifolds with holonomy G₂.
- The filter rejects this admissible structure. The withdrawn ε-table
  ((1, 1) / (0, 2)) was correct, and replacing it with the filter was the error.

**Hypothesis.** Under Joyce's actual hypotheses — pairwise disjoint singular sets
(his Condition 2.1.2), free extra stabilisers resolved equivariantly — the reachable
(b₂, b₃) are:

- (0, 7);
- b₂ + b₃ = 23 for b₂ = 0, …, 8 (n = 1);
- b₂ + b₃ = 39 for b₂ = 4, …, 12 (n = 2);
- b₂ + b₃ = 55 for b₂ = 8, …, 16 (n = 3).

That is 28 pairs, with b₂ + b₃ = 7 + 16n throughout.

**Discriminating test.** Recompute in the codebase from its own primitives:
pairwise-disjoint admissibility, family stabilisers, and Joyce's contributions —
plain (1, 3); free ℤ₂ reflecting two coordinates: (1, 1) or (0, 2). Families whose
stabiliser has order 8 are the verifier's own derivation, (0, 1) with three choices;
they are labelled NOT literature-checked and reported separately. Compare with the
verifier's set.

**Kill conditions.**
- The recomputation disagrees with the set above on any pair realised by
  literature-checked contributions.
- b₃ = 24 becomes reachable.
- An n ≤ 2 member has finite π₁.

**Consequences, if confirmed — stated before computing.**
1. b₃ = 24 stays unreachable, so the adoption's exclusion of the seed_24 branch
   survives.
2. **The published claims that fall:** "b₃ ∈ {7, 19, 31, 43}", "b₃ ≡ 7 mod 12",
   "b₃ = 7 + 3b₂" as the family law (it holds only on the all-plain subfamily), and
   "exactly four members". These are labelled, not deleted.
3. **Holonomy G₂ selects n = 3,** the whole line b₂ + b₃ = 55. (12, 43) sits on it
   twice: as Joyce's Example 3 (all plain) and as Example 4 with l = 4.
4. **What picks (12, 43) on that line is open again.** Candidates, to be weighed by
   the decision rule, not by data:
   - all-plain (no free quotients; the maximally symmetric member);
   - b₂/4 = 3, which is data unless b₂/4 is given a meaning off the all-plain
     subfamily.

   This is a foundational matter — the seed ruling of 2026-09-22 — so it goes to
   the author in the Stage 2 digest with this evidence. The adopted seed is not
   changed here.
5. **The switch infrastructure** (`b3_path.PATHS`, the family fork) is enumerated
   from the corrected set only after the author has seen the digest. Until then
   the four-member family is labelled "all-plain subfamily" wherever it is named.

## D-006 · RESULT · 2026-09-30 · CONFIRMED (lead's recomputation agrees with the verifier)

`PM/geometry/joyce_reachability.py` recomputes the reachable set from the
codebase's own primitives. It uses pairwise-disjoint admissibility, and it computes
each family's contribution rather than looking it up: the part of H*(T³) that
transforms by a lift character ε: Stab → {±1}, with ε(σ) = +1.

- **Calibration by computation.** On the first Example-4-type class the
  computation returns exactly Joyce's eq. (27): (8 + l, 47 − l), l = 0 … 8. A plain
  family gives {(1, 3)}. A T³/ℤ₂ family gives {(1, 1), (0, 2)}.
- **Literature-checked reachable set.** (0, 7) plus b₂ + b₃ = 23 (b₂ = 0 … 8), 39
  (b₂ = 4 … 12) and 55 (b₂ = 8 … 16). That is 28 pairs, identical to the verifier's
  independent set, and b₂ + b₃ = 7 + 16n throughout.
- **b₃ = 24** is unreachable in every variant.
- **Open sub-question, labelled.** Eight more pairs, (9, 14) … (16, 7) on the 23
  line, arise only from the TRIVIAL lift character on the order-8 stabiliser
  families (7 classes, n = 1). No published example covers that case. The verifier
  derived three admissible lifts there (all non-trivial) and the lead's character
  computation allows four. They are reported separately and claim nothing.

No kill condition fired.

**Applied now (labels only; no computed number changed).**
- `derived_contribution_table`: the "SETTLED RESULT" is re-headed "the all-plain
  subfamily". `a1_admissible_survey` status: `SETTLED_NO_ASSUMPTION` →
  `ALL_PLAIN_SUBFAMILY`, with `superseded_by`. Its scope no longer claims the
  removed families "are not Joyce's".
- `b3_path`: the family provenance says "all-plain subfamily".
- `family_topology` / `closed_geometry`: uniqueness claims are scoped. CG.4 now
  states "π₁ finite exactly when n = 3", which holds in both families.
- The pinned status in `test_derived_contribution_table` was updated in the same
  change, with the reason in its docstring.

**Carried to the Stage 2 digest.** The seed's selection argument. Holonomy G₂
selects the n = 3 line, nine pairs. (12, 43) is its all-plain member (Joyce's
Example 3), and also Example 4 at l = 4. What picks it within the line is the
author's to rule.

---

## D-007 · 2026-09-30 · G5 · PRE-REGISTERED — the classification, before any re-wiring

The full table is in `docs/decisions/D-007-g5-classification.md`: 121 roots,
each with its class, the pre-registered action, and a fragment of the root's OWN
derivation text as evidence.

The source is a neutral inventory. A separate agent was told not to classify
anything; it gathered the texts verbatim, with file and line, and measured every
value in fresh processes under both seeds.

| class | count | pre-registered action |
|---|---|---|
| B3 — the text names 3-cycles, H³ or metric moduli of Y₇ | 20 | follow the live seed; the recorded cost stands |
| BULK — bridge pairs, the 13D shadow, SO(24) transverse, torsion pins, D_space | 7 (+ parts of 5 MIXED) | keep 24 / 12 / 13; re-wire code that reads b₃ |
| NAMED — the 24-cell and T₄ | 3 | re-wire the flavour route to the 24-cell reading |
| NONE — arithmetic, a fit, or a type error | 66 | demote to a labelled calibration, kept runnable |
| MIXED | 15 | split; the mixture is recorded as a defect |
| G1 (the χ_eff family) / INFRA | 7 / 3 | deferred to G1 / fixed or left |

**What the classification says, in brief.**

- **k_gimel = b₃/2 + 1/π is NONE.** Its texts name four different objects —
  "Mass-Energy Gearbox", "Holonomy Precision Limit", "Leech lattice spectral gap",
  "associative 3-cycles" — and derive none of them. Everything built on it is
  therefore a fit: α⁻¹, the Higgs VEV (its "b₃ − 4" counts TCS K3 matching fibres,
  an object absent from the Joyce construction), sin²θ_W, T_CMB and μ. They agree
  with data only at the retired 24, which is a pre-registered dead-end criterion.
  Their published values come from `ANCHOR_FIT` and will not move. Their status
  label will.
- **The w₀ family is B3** (its texts name "the b3 associative 3-cycles"). The
  `dark_energy_betti` option adopted today, `b3_24`, is by its own text "a constant
  rather than a topological read". So w₀ follows the seed to −42/43. **The cost is
  confirmed, not healed.**
- **The PMNS distortion η = √2 sin(π/24) is NAMED.** Its derivation builds on "the
  24-cell … T₄", and b₃ appears only as a variable name (rule 1). So the 2026-09-22
  `flavour_seed_coupling = follow_seed` ruling was a mis-disentanglement. The
  24-cell reading restores θ₁₃ = 8.67°. That improvement is **not evidence**
  (trials factor 2), and the route's own derivation status is flagged separately.
- **Misfiled bulk counts heal internal numbers only.** The bridge pairs (`pneuma`
  gives 21 pairs at 43), the 13D shadow's "b₃/2 + 1" (appendix C gives 22.5),
  SO(24) in appendices G and H, and G22's torsion pins.
- **δ_CP in `neutrino_algebraic` is B3** ("b3/n_gen associative 3-cycles"), so its
  cost stands.

**Direction check (D-004's second kill condition).** The contested outcomes run
both ways:
- w₀ gets worse against data;
- θ₁₃ gets better;
- 66 claimed derivations are withdrawn as fits;
- the bulk fixes are internal.

So the audit is not one-directional.

**Blind verification protocol, fixed now.**
1. **Random sample.** 41 roots — one third — drawn with `random.Random(20260930)`:
   FR01, FR03, FR04, FR06, FR07, FR09, FR10, FR11, FR23, FR29, FR32, FR36, FR40,
   FR42, FR45, FR49, NC02, NC04, NC06, NC10, NC14, NC15, NC19, NC23, OT02, OT06,
   OT08, OT09, OT10, OT14, OT18, OT19, OT20, OT21, OT23, OT24, OT30, SP02, SP12,
   SP16, SP17.
2. **Contested set.** The seven roots where rule 4 or 5 decided the outcome,
   verified SEPARATELY and not counted in the rate: FR02, SP01, SP05, SP11, SP13,
   SP14, OT13.
3. The verifier gets the D-004 rules and the inventory's texts, not this table.
   Agreement is measured on the class.
4. Below 80% on the random sample, the rules are tightened and re-registered
   before anything is re-wired.

**After verification.** Each action is one commit with its measured before/after
and a one-line revert:
- flip `dark_energy_betti` to `b3_live`;
- flip `flavour_seed_coupling` to the 24-cell reading;
- re-wire the bulk counts;
- demote the NONE layer in its labels.

---

## D-008 · 2026-09-30 · G1b · PRE-REGISTERED — are the two twelves one structure?

**Question.** Is there a structure-preserving map between the bulk's 12 bridges
and the resolved manifold's 12 A1 components, or is b₂ = 12 = D_space/2 a
coincidence of the adopted point?

**What each twelve is, from the framework's own records.**
- **Bridges** (`BRIDGE_CHANNEL_ASSIGNMENT.md`): the 12 bridges are the directed
  edges of K₄ on a Fano arc of 4 "faces". The 3 E₈ blocks are K₄'s three perfect
  matchings, labelled by the points of the arc's complement line. The arc is
  "unique up to symmetry", one PSL(3,2) orbit, with a stated conditional: "a
  preferred imaginary octonion … would break PSL(3,2) and make the choice of arc
  physical again."
- **Components:** 3 singular involutions × 4 Γ-orbits of fixed 3-tori (D-001).
  Each involution's fixed set is a Fano line.

**Hypothesis.**
1. Three singular involutions that span Γ are three non-concurrent Fano lines. They
   canonically fix an arc: the triangle's three vertices (the pairwise
   intersections) plus the one point lying on none of the lines. The complement
   line is the unique line meeting none of those four points.
2. Each perfect matching of K₄ on that arc contains exactly ONE side of the
   singular triangle. Therefore the E₈ blocks and the singular involutions are in
   canonical bijection.
3. Each block holds 4 bridges, and on an all-plain assignment each involution
   holds 4 components. So a bijection bridges ↔ components exists that respects
   the 3 × 4 structure. It is canonical up to a Klein-four relabelling within each
   block, since both sides are (ℤ/2)²-torsors.
4. On Joyce's Example-4 classes (D-006), one involution carries 8 components, so
   no structure-preserving bijection exists. The correspondence holds exactly on
   the all-plain members, and at n = 3 that is (12, 43).

**Discriminating test.** Compute 1–4 from the enumeration, on the canonical
point and on every n = 3 class. Check the correspondence against Lukas–Morris
(hep-th/0305078, eq. 1.3): the 12 U(1) gauge-kinetic functions depend on the
blow-up TYPE only, so they must come in 3 quartets, one per block.

**Kill conditions.**
- An n = 3 class whose singular lines are concurrent.
- A perfect matching holding 0 or 2 singular sides.
- A structure-preserving bijection on a non-all-plain class, which would remove the
  selection.
- The bridge records not describing K₄'s directed edges on an arc.

**Consequences if confirmed, stated before computing.**
- The two twelves are one structure, answering G1b positively. The Joyce singular
  set breaks PSL(3,2) and fixes the face arc, which the bridge record already
  anticipated.
- Combined with holonomy G₂ (n = 3, D-002/D-006), "one bridge per resolved A1
  component" selects (12, 43) on the n = 3 line without data. Three generations
  then become an output.

**Status of that last step.** "One bridge per component (one U(1) each)" is a
MODEL IDENTIFICATION: working assumption WA-1. It costs no parameter. Its testable
content is the 3 × 4 grouping of gauge couplings, and it fixes which Fano points
are faces. Any module that uses a different arc then disagrees with it. Adopting
it as the seed's selection criterion is the author's ruling at Stage 2.

## D-008 · RESULT · 2026-09-30 · CONFIRMED (lead run), blind verification running

`PM/geometry/bridge_component_map.py`, reusing `arc_flag_structure`'s Fano
lines and arcs:

- **The adopted point.** The singular lines (0, 1, 2), (0, 3, 4) and (1, 3, 5) are
  non-concurrent, with triangle vertices {0, 1, 3} and missed point 6. They fix
  the arc {0, 1, 3, 6} with complement line (2, 4, 5).
- **The blocks.** The K₄ blocks, labelled by complement points, are
  2: {01, 36}, 4: {03, 16} and 5: {06, 13}. Each holds exactly one singular side
  (01 ⊂ L_α, 03 ⊂ L_β, 13 ⊂ L_γ), so block → involution is a canonical bijection.
- **The bijection.** Four bridges per block against four components per
  involution, 12 ↔ 12. It is canonical up to a Klein-four relabelling inside each
  block.
- **Every n = 3 class of the first generating triple:** 280 all-plain classes
  admit the bijection; the 84 Example-4-type classes admit none. There are zero
  exceptions.

No kill condition fired. Lukas–Morris eq. (1.3) — "The gauge-kinetic functions
for these multiplets depend on the type τ of the blow-up only" — gives three
quartets of U(1) couplings, consistent with blocks ↔ involutions.

**What this makes available to the author (Stage 2).** A seed selection that
uses no data: holonomy G₂ gives n = 3, and one bridge per resolved A1 component
(WA-1) gives the all-plain member, (12, 43). Three generations then become an
output.

WA-1 is a model identification, not a theorem. Its cost is zero parameters.
Its content is the 3 × 4 gauge-coupling grouping, which is consistent with the
literature, and a fixed face arc, {0, 1, 3, 6}. Every module that uses another
arc must be reconciled. The PSL(3,2) "uniqueness up to symmetry" of the bridge
record is then broken by the singular set, which that record itself named as the
condition that would make the arc physical.

---

## D-009 · 2026-09-30 · G1 · PRE-REGISTERED — what χ_eff is, starting from its consumers

**Step 1: the consumer inventory** (neutral agent; 946 consumers, 261 of them
feeding published quantities).
- There are **22 different definitions** of χ_eff in the code: 72, 144, 1/144,
  2(h¹¹ − h²¹ + h³¹) from off-path TCS Hodge data, b₃²/4, (b₃/2)², b₃²/8, 6b₃, 3b₃,
  4·b₃·n_gen, (288/24)², "χ(CY4) = 72 with n_gen = χ/24", even χ = −168, and more.
- 41 sites — 31 in the engine and website, 10 in published artifacts — call χ_eff
  the Euler characteristic of Y₇, which is 0 (CG.2).
- Consumers by stated purpose:
  - cosmology 184;
  - generation count 164;
  - gates/certificates 118;
  - particle physics 101;
  - flux/tadpole 33;
  - "Euler characteristic" 30;
  - sampler/Reid 29;
  - index/chirality 18;
  - the rest naming and instrumentation.

**Step 2: what each consumer's physics requires on Y₇.**
- **Generation count.** Needs a count of generations. On the construction the
  invariant count is n, the rank of the singular span. b₂/4 equals n only on the
  all-plain subfamily (D-006).
- **Index/chirality and flux/tadpole.** They invoke χ/24-type formulas: the M2
  tadpole of an 8-manifold, F-theory on a CY4. Those need an 8-manifold, and none
  is defined for a G₂ 7-manifold. They are therefore TYPE ERRORS, class NONE.
- **"Euler characteristic of Y₇".** That quantity is 0, so these sites are
  relabelled.
- **Cosmology, particle, gates and sampler.** These use 144 or 72 as a bare number,
  class NONE under D-007.

**Hypothesis: the K3 reading.** Each singular involution σ acts as −1 on its
transverse T⁴, which has 16 fixed points. The resolution K3_σ is a Kummer surface:
χ = (0 − 16)/2 + 2·16 = 24. Define

  χ_eff := 2 · Σ_σ χ(K3_σ) = 48n,

with the factor 2 for the two shadows, which is the two-time ruling. That gives
72 per shadow and 144 in total at n = 3. These are the registry's existing
mephorash_chi 72 and chi_eff_total 144, now with an object behind them. Then

  n_gen = χ_eff/48 ≡ n.

This is THE SAME STATEMENT as counting singular involutions, not a second
derivation.

**Discriminating test.**
- Compute Σ χ(K3_σ) from the enumeration on every pairwise-disjoint class of the
  first generating triple: all-plain, Example-4 type, and order-8 profiles.
- Check that χ_eff/48 = n on every class.
- Check where b₂/4 = n fails, over every reachable (b₂, b₃).

**The four readings of 144, recorded with their evaluation:**

| reading | what it counts | outcome |
|---|---|---|
| 2Σχ(K3_σ) | Euler characteristics of real 4-manifolds, two shadows | 48n; tracks n everywhere |
| (D_space/2)² | a squared bulk pair count, not an index | 144 on every seed, so gives 3 everywhere |
| b₂² | ordered pairs of 2-classes, a type change | varies inside the n = 3 line (b₂ = 8 … 16) |
| (b₃/2)² | "pairs of 3-cycles" | refuted: b₃ is odd on the whole family |

**Kill conditions.**
- A singular σ whose transverse quotient is not 16 A1 points.
- Any class with χ_eff/48 ≠ n.

**Consequence if confirmed (the author's ruling; χ_eff is foundational).**
Recommend that χ_eff means the K3 reading, stated as adding nothing beyond n. The
other 21 definitions are demoted as NONE or type errors. The 41 "Euler
characteristic of Y₇" sites are relabelled. The ruled generation route should
count n, not b₂/4. The alternative is to retire χ_eff altogether and use n.

## D-009 · RESULT · 2026-09-30 · CONFIRMED (lead run)

`PM/geometry/kummer_index.py`, engine `d271d97`:

- **Adopted point.** Each singular involution fixes 16 transverse points,
  counted on the quarter lattice rather than assumed. χ(K3) = 24 both from the
  quotient and from Betti numbers (b₂ = 6 + 16 = 22). Per shadow 72; χ_eff = 144;
  n_gen = 3.
- **All 15,963 pairwise-disjoint classes** (first generating triple): the reading
  equals n on every class, with no exceptions.
- **The ruled route b₂/4 = n** holds on only 15,963 of the 26,155 reachable
  (class, pair) combinations, one per class.

No kill condition fired.

**Recommendation to the author (χ_eff is a foundational ruling).**
- Rule χ_eff = the K3 reading: 72 per shadow and 144 in total are Euler
  characteristics of the Kummer surfaces, and n_gen = χ_eff/48 ≡ n.
- Switch the generation route from b₂/4 to n, the count of singular involutions.
- Demote the other 21 definitions as NONE or type errors.
- Relabel the 41 sites that call χ_eff "the Euler characteristic of Y₇".

---

## D-010 · 2026-09-30 · open problems C2 + C3 · PRE-REGISTERED

**C2: moduli stabilisation — can any full-holonomy member confine?**
Gaugino condensation needs pure N = 1 SYM on a locus Q, which means b₁(Q) = 0
(Acharya: N = 1 + b₁). In φ's Joyce family the loci are T³/Stab:
- plain loci have b₁ = 3 (N = 4);
- T³/ℤ₂ (Example 4) has b₁ = 1 (N = 2);
- only the order-8, Hantzsche–Wendt-type loci of some n = 1 classes can have
  b₁ = 0.

**Conjecture.** No class with n = 3 (the full-holonomy classes, D-002/D-006) has a
locus with b₁ = 0. Full holonomy and a confining sector would then be mutually
exclusive inside the construction.

**Test.** For every pairwise-disjoint class, compute each locus's b₁ from its
stabiliser's invariant 1-forms, and the minimum by n.

**Kill.** An n = 3 class with a b₁ = 0 locus.

**C3: the cosmological constant — can the flux potential accelerate the universe?**
Homogeneity (D-005) gives K_ij sⁱ sʲ = 7 and s·∇V = −5V. In canonical
normalisation the radial direction has norm √(7/2), so the RADIAL slope is
5/√(7/2) = 5√(2/7) ≈ 2.673. A gradient's norm is at least its projection, so

  |∇V|/V ≥ 5√(2/7)

at every point, for every flux. That exceeds √2, the threshold for accelerated
expansion from an exponential potential.

**Test.** Evaluate the full |∇V|/V in the canonical metric (K_ij/2 for the real
parts) at random points and fluxes. It must never fall below the bound.

**Kill.** A point below 2.673.

**Scope.** The leading-order Kähler potential, and a single-field reading of
acceleration. Multi-field rapid-turn trajectories are not excluded by a
gradient bound and are noted as open.

## D-010 · RESULT · 2026-09-30 · CONFIRMED (lead run)

**C2.** Classes by the smallest b₁ among their loci (first generating triple):

| n | b₁ = 0 | b₁ = 1 | b₁ = 3 |
|---|---|---|---|
| 1 | 7 | 840 | 5,936 |
| 2 | — | 336 | 2,184 |
| 3 | — | 84 | 280 |

Confining (b₁ = 0) loci occur ONLY at n = 1, whose π₁ is infinite. **Within φ's
Joyce family, holonomy exactly G₂ and a confining gauge sector are mutually
exclusive.** The mainstream route to moduli stabilisation — Acharya's pure
N = 1 SYM plus flux — is structurally unavailable on every full-holonomy
member, not just on (12, 43).

**C3.** Across 60 random points and fluxes, the canonical slope |∇V|/V was at
least 2.72. That respects the homogeneity bound 5√(2/7) = 2.673 and sits far
above √2. **The leading-order flux potential cannot drive accelerated
expansion.** Dark energy and the cosmological constant need physics beyond
leading order (open), and the w₀ values carry no mechanism.

No kill condition fired. Engine commit follows this entry.

**What remains open, and where to look (next session).**
- **Chirality** (absent structurally: disjoint loci have no codim-7 points).
  Candidate sources: a heterotic dual through the Kummer fibrations; the two
  shadows as boundary walls.
- **Moduli.** Membrane instantons on rigid associatives, cross-shadow potentials,
  corrections to K.
- **Flavour.** Tied to chirality. The 3 singular involutions ↔ 3 E₈ blocks ↔ 3
  gauge-coupling quartets structure is the hint.
- **Dark energy.** Beyond leading order, or multi-field.

---

## D-011 · 2026-09-30 · open problems C1 + C4 · ANALYSIS (no computation yet)

**Are the four problems really open, or does the geometry avoid them?**
Answered for all four:

| problem | status | why |
|---|---|---|
| C1 chiral matter | **really open**; absent inside Y₇ by structure | Smooth G₂ gives only neutral chirals. Acharya–Witten chirality needs codim-7 points where singular loci meet, and Joyce admissibility IS pairwise disjointness, so the whole family has none. The orbifold limit gives N = 4 SU(2), which is non-chiral. |
| C2 moduli | **really open**, sharpened (D-010) | Full holonomy and a confining sector are mutually exclusive. |
| C3 dark energy / CC | **really open**, sharpened (D-010) | The flux potential's slope is ≥ 2.673 > √2. |
| C4 flavour | **really open**, downstream of C1 | Without chiral loci there are no Yukawas, and π₁ = 1 closes Wilson lines. |

So the geometry avoids none of them. C2 and C3 are now no-go statements INSIDE
the construction. The remaining freedom lies OUTSIDE Y₇, in the model's own
postulates.

**Research directions, verified sources only.**
1. **Heterotic dual.** Acharya, *N=1 heterotic/M theory duality and Joyce
   manifolds*, Nucl. Phys. B475 (1996) 579–596, hep-th/9603033 (verified). It
   pairs M-theory on Joyce manifolds, as K3 fibrations, with heterotic strings on
   T³-fibred Calabi–Yau threefolds, and matches their massless spectra. The K3
   fibres are the Kummer surfaces of the K3 reading (D-009). Chirality on the
   heterotic side comes from the gauge bundle. The question: does the dual of
   (12, 43) carry a chiral bundle, and what is its M-theory image? A later
   non-perturbative treatment of heterotic duals of G₂ orbifolds exists
   (arXiv:2106.03886; to be verified before citing).
2. **The two shadows as boundary walls.** In Hořava–Witten, chiral E₈ matter lives
   on two walls (citation to be verified). The model already has two shadows and
   three E₈ blocks tied to the singular involutions (D-008). Test whether the
   shadow structure can carry wall-localised chiral multiplets. Kill: if the
   bulk's (24,2) signature cannot host 10D-type walls.
3. **Flavour hint.** The 3 singular involutions ↔ 3 E₈ blocks ↔ 3 quartets of U(1)
   couplings, f = T^A by type (Lukas–Morris). If generations ARE the involutions,
   hierarchies would come from the three locus volumes. Those are unfixed moduli,
   so C4 depends on C2.

Each direction must be pre-registered with a kill condition before it is
computed.

## D-007 · VERIFICATION · 2026-09-30 · KILL CONDITION FIRED — re-wires held

The blind verifier (rules and inventory texts only, not the D-007 table) was
interrupted by a usage limit after 32 of the 41 random-sample roots and none of
the contested set.

**Class agreement: 18/32 = 56%**, below the pre-registered 80%. As registered,
nothing is re-wired. The rules are to be tightened and re-registered, and the
sample re-verified.

**Where the disagreements fall.**
- **Mostly MIXED vs NONE on the same action** (FR03, FR29, FR32, FR42, FR45,
  NC10, OT08, OT09, OT10): a root combining a seed-moving b₃ with frozen
  numerology. The verifier labels it MIXED; the table labelled it NONE. Both lead
  to DEMOTE. **Rule to tighten:** a root is MIXED only when at least one part has
  an object; otherwise it is NONE.
- **Compatible** (NC14, NC15, OT14): MIXED with parts B3 / G1 or BULK / unused.
- **Substantive, and they change actions:**
  - **FR04 (σ_T = 23/24).** The table said B3. The verifier said NONE: its text
    names "Void Seal" and a "bridge size modulus", not 3-cycles, while SP07's text
    does name "the b3 associative 3-cycles". The w₀ family's texts CONFLICT. That
    is rule 4 — ambiguous — and must be resolved by rule 5 before any w₀ change.
    **The dark_energy_betti flip is held.**
  - **OT06 (24//8 E₈ blocks).** The table said NONE. The verifier said NAMED: 24
    read as a rank-24 lattice splitting into 3 E₈ blocks of 8 (Niemeier E₈³),
    which stays 3. A plausible object the table missed.

**This is the protocol working.** The rules were too loose to reproduce, so no
published number moves on them. Next, when usage allows:
1. Re-register D-007 with the tightened MIXED/NONE rule and the rule-5
   resolution of the w₀ texts.
2. Re-run the blind verifier on the full random sample plus the contested set.
3. Re-wire only on ≥ 80% agreement.

---

## D-012 · 2026-10-01 · G5 · RE-REGISTERED — tightened rules, before re-verification

D-007's blind verification fired its kill condition (18/32 = 56%). As registered
there, the rules are tightened and re-registered HERE, before the verifier runs
again. Nothing is re-wired until it passes.

**Amendments to D-004.**
- **Rule 6′ (MIXED).** A root is MIXED only when at least one of its parts names an
  object (B3, BULK or NAMED) and another part comes from a different class or seed.
  A root none of whose parts names an object is NONE, however many parts it has.
  (Nine of the fourteen disagreements were MIXED vs NONE on the same action.)
- **Rule 8 (families).** Roots that compute the same published quantity form a
  family. When their texts name DIFFERENT objects for the same factor, the family is
  AMBIGUOUS (rule 4) and rule 5 decides it once, for every member. A member whose own
  text names no object takes the family's class only if it consumes the same factor;
  otherwise it is NONE.
- **Rule 9 (names are symbols).** Legacy or esoteric names ("Elders", "Pleroma",
  "Void Seal", `elder_kads`, `tzimtzum`) are symbols, not objects (rule 1). A name
  counts only if the text says what is counted.
- **Rule 10 (a modulus is not a count).** A continuous modulus — a size, a volume, a
  vev — is not a count of 24 things. A text that names only a modulus for a factor
  of 24 names no object for it.

**Resolutions fixed now, on the quoted evidence.**
- **The w₀ family** (SP07, FR04, and the readers of `dark_energy_betti`). Only
  SP07's text names a counted object for the 24: "the b3 associative 3-cycles",
  i.e. H³ of Y₇ — valid on the adopted geometry, 43 classes. FR04 (σ_T = 23/24)
  names a symbol ("Void Seal") and a modulus ("bridge size modulus") — rules 9 and
  10 — so it is NONE. **Family class: B3.** If verified: `dark_energy_betti` →
  `b3_live` (w₀ = −42/43), and σ_T = 23/24 is labelled a calibration, value
  unchanged. The DESI comparison is reported after the choice and does not enter it
  (both −23/24 and −42/43 lie more than 3σ from the DR2 w0waCDM headline).
- **OT06** (`four_face_structure`: `n_e8_blocks = b3 // 8`, `n_bridges = n_faces ×
  n_e8_blocks`). The derivation text names "the 12 bridge pairs" — the bulk. The
  table's NONE is withdrawn and the verifier's NAMED is not adopted either: **BULK**
  (24 = the bulk's space directions = 3 E₈ blocks of 8; stays 3). If verified, the
  block count reads D_space, so n_bridges returns to 12 (it reads 20 at b₃ = 43 —
  more bridges than the bulk has).

**Re-verification protocol (fixed now).**
1. A fresh blind verifier receives D-004 as amended here and the inventory's
   derivation texts — not the D-007 table and not the first verifier's verdicts.
2. It classifies the same random sample of 41 roots (`random.Random(20260930)`)
   and, separately, the 7 contested roots (FR02, SP01, SP05, SP11, SP13, SP14,
   OT13).
3. **Pass: ≥ 80% exact class agreement on the 41**, measured against the D-007
   table as amended by the resolutions above (FR04 → NONE, OT06 → BULK, and every
   all-object-less MIXED → NONE under rule 6′). The amended table is written to
   `docs/decisions/D-012-amended-table.md` BEFORE the verdicts are read.
4. Below 80%: no re-wiring; the disagreements are published with their evidence.
5. At or above 80%: the D-007 actions run, one commit each, with before/after and a
   one-line revert.

---

## D-013 · 2026-10-01 · PUBLICATION · PRE-REGISTERED — the site shows the active path only

**Request (the author, 2026-10-01):** only active switch/path formulas and
parameters are displayed on the website, and only those are being updated.

**Rule.** A formula or parameter is published LIVE only if it is on the active
path:
1. it does not implement a non-adopted option of any fork, and
2. its claim has not been retired by a decision or ruling.

Everything else is published ONLY in a generated off-path register
(`off_path_register.json`), each entry with the fork option or decision that
retired it and a one-line reason. It stays runnable — dead ends are demoted,
never deleted.

**Mechanism.** Membership is declared once per object, in one registry module,
as (fork, option) or (decision, reason). It is evaluated against the LIVE fork
state at export, so flipping a fork moves an object between the live set and the
register. No typed list of hidden ids.

**Not off-path, and still displayed:**
- on-path quantities whose value is a calibration — labelled CALIBRATED;
- on-path quantities with stale wording — fixed by the wording pass (D-014);
- b₃-consumers awaiting G5 — displayed with their recorded divergence.

**Checks (tests).**
- Every declared id exists in a full run.
- No live artifact contains a declared off-path id on the adopted path.
- Flipping `b3_seed` to `seed_24` moves the seed-24-bound objects into the live
  set.
- Nothing is lost: live + register = everything the run produced.

**Kill condition.** If an object cannot be assigned without a judgement the
decision rule does not settle, it stays LIVE, labelled, and is listed for the
author. Hiding is never the default for a doubtful case.

---

## D-014 · 2026-10-01 · WORDING · the rules for the wording pass

The wording pass brings every surface — paper, website, beginner guide, formula
and parameter text — onto the adopted model with one voice. Its rules are the
engine's `docs/WORDING_MEMO.md`: what is true on the active path (certificate
CG.1–CG.11 and D-001…D-013), what is off-path, retired or calibrated, how a
remaining 24 is named by its object, and how numbers enter prose
(`geometry_narration.render`, generated from the live seed). A wording pass
changes no value, EML tree, arithma expression, formula id or parameter path.

---

## D-015 · 2026-10-01 · RULINGS — the author's, on the four held decisions

Asked directly (2026-10-01), the author ruled, and added the standing direction:
**adopt the sensible path on every fork, and keep the other options as switches,
so they can be simulated and compared quickly.**

| decision | ruling | active option | kept switchable |
|---|---|---|---|
| φ's real form (D-003) | adopt the sensible path; both stay runnable | `g2_form_convention = octonion_derived` (compact) | `all_plus_one` (split) |
| χ_eff (D-009) | adopt the K3 reading | new option `chi_eff_route = k3_reading`: χ_eff = 2Σχ(K3) = 48n | `unruled`, `constant_144`; `seed_dependent` demoted (refuted by D-009) |
| Re(T) (D-005) | an open modulus | `re_t_adoption = calibrated`, labelled a calibration | `computed_vacuum` demoted: it is the vacuum of a racetrack Y₇ does not have (CG.5, CG.10) |
| WA-1 (D-008) | adopt | new fork `seed_selection = wa1_correspondence` | `ruling_only` |

**What changed in the engine (one commit, with its tests).**
- `g2_differential.G2_TRIPLES` carries the compact signs (−1 on (1,3,5)); the split
  table is `ALL_PLUS_TRIPLES`. The octonion module's accessor follows the switch.
  Measured before the ruling (D-003): 0 of 788 parameters and 0 of 226 numeric
  formulas move.
- `geometry_narration.chi_eff_claim()` narrates per branch; on `k3_reading` a
  derivation is claimable. `fragments()` follows it.
- New certificate theorem **CG.12 `y7-selection`**: CG.7 + CG.4 + CG.8 read through
  WA-1 select (12, 43). Its statement follows both switches: on the split form it
  states only the topological half (π₁ finite exactly at n = 3); on `ruling_only`
  it reports the match as a finding beside the 2026-09-22 ruling. Falsifiable: on
  (8, 31) the chain still selects (12, 43), so the theorem does not hold there.
- Tests that pinned the pre-ruling state by design now assert BOTH paths (the
  adopted one, and the old one when switched back).

**WA-1's test, restated:** the 12 U(1) gauge-kinetic functions come in 3 quartets
(Lukas–Morris eq. 1.3: they depend on the blow-up type only). A class breaking the
quartet structure would kill it.

---

## D-008 · BLIND VERIFICATION · 2026-10-01 — H1, H2, H4 confirmed; one clause of H3 refuted

A fresh verifier, without the lead's module, tests or results, built its own model
of all 2¹⁴ = 16,384 shift classes and ran the engine over all 28 generating triples
(458,752 assignments; every triple covers every class once). Engine and model agree
class by class: zero mismatches. n = 0/1/2/3 classes: 6,296 / 6,783 / 2,520 / 364;
none with n ≥ 4.

- **H1 confirmed.** Of the 35 triples of non-identity elements, 28 span Γ, exactly
  the non-concurrent ones; every triangle gives a 4-arc, and exactly one line misses
  it — the fixed line of σ₁σ₂σ₃. All 364 n = 3 classes are non-concurrent. The
  canonical point's singular lines are (0,1,2), (0,3,4), (1,3,5); arc {0,1,3,6}.
- **H2 confirmed.** 84/84 abstract and 1,092/1,092 concrete perfect matchings hold
  exactly one triangle side.
- **H3: existence confirmed, canonicity REFUTED.** All 280 all-plain classes have
  4 components per involution and admit a 3 × 4-respecting bijection; both sides are
  (ℤ/2)²-torsors. But all 24 bijections of a block are torsor maps, so the torsor
  structure narrows nothing (216 choices per class), and on 112 of the 280 classes no
  choice is invariant under the orbifold's φ-preserving symmetries; none has a
  unique choice. Blocks ↔ involutions IS canonical; bridge ↔ component inside a
  block is a free choice. The selection (CG.12) needs only existence, so it stands;
  the wording "canonical up to a Klein-four relabelling" is withdrawn in the engine.
  Physically the four U(1)s of a block share one gauge-kinetic function, so the
  freedom sits exactly where they are indistinguishable.
- **H4 confirmed, with a caveat.** The 84 non-all-plain n = 3 classes all have
  components (4, 4, 8) and admit no bijection. But under the per-family lift model
  all 84 also reach (12, 43): the pair (12, 43) does not identify the all-plain
  members — the component profile (4, 4, 4) does. The selection reads the profile
  through WA-1, so this does not move CG.12.

No kill condition fired.

---

## D-016 · 2026-10-01 · OPEN PROBLEMS C1–C4 · LITERATURE VERDICTS (D-011 directions)

A research agent checked every candidate direction of D-011 against fetched sources
(arXiv API, Crossref, INSPIRE, full texts; evidence kept in the session scratchpad
`open_problems/`). Nothing was computed; the computations are pre-registered in
D-017. **All four problems stay open, and no direction is PROMISING.**

| # | Direction | Verdict | Why (verified source) |
|---|---|---|---|
| C1 | Chirality via the heterotic dual | **KILLED** | Acharya–Kinsella–Morrison, JHEP 11 (2021) 065 (arXiv:2106.03886), Example 3.2 *is* this orbifold: "SU(2)¹² gauge symmetry with 3 adjoint chirals for each SU(2) and 7 neutral chiral multiplets … the spectra are non-chiral". The dual's bundle is the image of the G₂ geometry, so there is no extra datum to make chiral. |
| C1 | Chirality from the shadows as Hořava–Witten walls | **KILLED** | HW (NPB 460 (1996) 506; NPB 475 (1996) 94) needs even-dimensional codimension-1 walls of an odd-dimensional bulk and a 6D internal space; here walls are 25D, shadows 13D, Y₇ 7D. The model's E₈ blocks are blocks of bulk directions, not HW's E₈ gauge groups (A4). |
| C2 | Corrections to K beyond (U/T)² | **KILLED** | ADV eq. (3.2): the exact classical K = −3 ln V_X with V_X homogeneous of degree 7/3, so the λ⁻⁵ runaway holds to all orders in U/T; Becker–Robbins–Witten (JHEP 06 (2014) 051): quantum corrections leave the moduli space unlifted to all orders in 1/R. |
| C2 | M2 instantons on rigid associatives | **NEEDS COMPUTATION** (PR-1; predicted kill) | Harvey–Moore need rigid rational homology spheres. The known associatives of this resolution (Dwivedi–Platt–Walpuski, CMP 401 (2023), Ex. 4.9) are S¹×S², b₁ = 1. An analytic lemma predicts no flat rigid b₁ = 0 cycle avoids the singular set. |
| C3 | Multi-field dark energy | **KILLED classically** (analytic; PR-3 confirms) | The slope 5√(2/7) is the universal internal-flux volume exponent and holds off the axion slice; late-time attractors give ε ≥ 25/7 (Shiu–Tonioni–Tran, PRD 108 (2023) 063528, eq. IV.3); the hyperinflation window (Bjorkmo–Marsh, JHEP 04 (2019) 172) is empty. Only brief transient acceleration remains possible. |
| C4 | Flavour from the three locus volumes | **KILLED as derivable** | No chiral points, no Yukawa couplings (Acharya–Witten hep-th/0109152 §2.4; Witten hep-ph/0201018). The locus volumes are gauge couplings, f(τ) = T⁷, T⁶, T⁵ (Lukas–Morris eq. 1.3), and unfixed moduli. |

**Status after D-016.** C1 and C4 are *not derivable on Y₇*: a chiral sector would be
a construction-level postulate (codimension-7 points outside Joyce's admissible
family), a fork option with its own consequence and kill condition, for the author.
C2 has no candidate mechanism inside Y₇ pending PR-1. C3's multi-field loophole is
closed classically pending PR-3.

**Corrections this forces.**
- D-011's "K3 fibres" holds in the ORBIFOLD limit only: whether the resolution has a
  coassociative K3 fibration is open (AKM 2021, footnote 1). D-009's count needs no
  fibration and is unaffected.
- Acharya 1996's explicit N = 1 pairs are J⁸₃₁ and the Example-4 family, not (12, 43);
  the (12, 43) dual is AKM 2021.
- Do not cite Atiyah–Witten for Yukawas or chirality.

**Citations verified for the 'standard physics' list (DOIs fetched):**
- Bars, CQG 18 (2001) 3113, DOI 10.1088/0264-9381/18/16/303.
- Bars & Kounnas, PRD 56 (1997) 3664, DOI 10.1103/PhysRevD.56.3664: two-time critical dimension 27 or 28, never 26.
- Eguchi & Hanson, PLB 74 (1978) 249, DOI 10.1016/0370-2693(78)90566-X.
- Polchinski, *String Theory* Vol. 1, CUP 1998, DOI 10.1017/CBO9780511816079: D = 26 is the one-time result.
- Acharya & Witten, hep-th/0109152: preprint, no DOI.
- Cheeger & Gromoll, JDG 6 (1971) 119, DOI 10.4310/jdg/1214430220. The theorem number "Theorem 3" is unverified.
- Atiyah & Witten, ATMP 6 (2002) 1, DOI 10.4310/ATMP.2002.v6.n1.a1.
- New DOIs for records already cited: Lukas–Morris 10.1103/PhysRevD.69.066003; ADV 10.1088/1126-6708/2005/06/056; Acharya 1996 10.1016/0550-3213(96)00326-4.

---

## D-017 · 2026-10-01 · PRE-REGISTERED — PR-1, PR-2, PR-3 (fixed before any computation)

**PR-1 · C2 — does Y₇ carry a Harvey–Moore instanton cycle?**
- Hypothesis: no totally geodesic associative N = (T_V + c)/S of T⁷/Γ avoiding the
  singular set is both rigid and a rational homology sphere, on any class with n ≥ 1.
  Lemma: b₁(N) = dim V^S; rigid ⇔ (V^⊥)^S = 0; dim(ℝ⁷)^S = 8/|S| − 1; so "rigid and
  b₁ = 0" forces S = Γ, V a Fano line, and then a singular involution fixes points of
  the torus.
- Computation: for the canonical point and every n ≥ 1 class of the first generating
  triple, every Fano line L and transverse offset c on the quarter lattice: S, b₁,
  rigid, free. Check dim(ℝ⁷)^S = 8/|S| − 1 on all 16 subgroups. Count rows that are
  b₁ = 0, rigid and free. **Prediction: 0.**
- Kill: any such row, or the subgroup identity failing.

**PR-2 · C2/C3 scope — are the runaway and the slope bound exact in U/T?**
- Hypothesis: both follow from homogeneity alone (degree 7/3), so any degree-0
  correction in X = Σ(8/3)u²/(s_A s_B) leaves V(λs) = λ⁻⁵V(s) and the bound intact.
- Test: replace −3 ln(1 − X) by −3 ln(1 − X − a₂X² − a₃X³), and separately add a
  degree-0 term g(u²/(s_A s_B)), keeping the metric positive definite; re-run the
  flux-vacuum identities and the acceleration report.
- Kill: any identity failing beyond rounding.

**PR-3 · C3 — can the classical flux potential accelerate, multi-field?**
- H3a: off the axion slice (c₂ = 0) V = 4e^K[K^{ij}N_iN_j + (N·a + c₁)²] and
  |∇V|_g/V ≥ 5√(2/7) on all fields.
- H3b: at u = 0 with equal bulk fluxes and equal s_A the slope equals 5√(2/7).
- H3c: with bulk flux only, u = 0 is consistent and ε ≥ 25/7.
- H3d: for every flat axion direction the hyperinflation window is empty
  (L_eff ≥ 1/√2).
- H3e: 200 FRW trajectories (seed 20260930), started at rest or with kinetic energy
  ≤ V: none has ≥ 1 uninterrupted e-fold of acceleration.
- Kills: H3a any point below 5√(2/7)(1 − 10⁻⁶); H3b relative deviation > 10⁻⁶;
  H3c µ_CH < √2; H3d any point with 3L_eff < |∇V|/V < 1/L_eff; H3e any trajectory
  with ≥ 1 e-fold.

Each is implemented as an engine module with tests, run, and its result recorded
here before any wording changes on its account.

---

## D-012 · VERIFICATION · 2026-10-01 · KILL CONDITION FIRED AGAIN (56%) — no global re-wiring

A fresh blind verifier (rules as amended in D-012, inventory texts only; neither the
D-007 nor the amended table, nor the first verifier's verdicts) classified all 41
random roots and the 7 contested ones. Verdicts: session scratchpad
`g5_reverify/verdicts.json`, each with its quote and reasoning.

**Agreement with the amended table: 23/41 = 56.1%**, below the registered 80%. As
registered, nothing is re-wired on the strength of the table.

**Where they disagree (18):**
- **MIXED vs NONE, again** (FR07, FR29, FR32, NC02, NC06, NC10, NC15, OT24, SP02). The
  verifier finds an object-bearing part (a B3 or BULK factor) in roots the table read
  as object-less. Rule 6′ removed one source of this; the remaining one is what counts
  as a text "naming" an object.
- **NONE vs B3** (OT08, OT09, OT10, OT21; FR04). **FR04 is the amended table's error,
  not the verifier's:** rule 8 gives a member that consumes the family's factor
  (σ_T = 1 − 1/b₃ documents exactly that) the family's class, B3.
- Others: FR01 (B3 vs INFRA: the seed accessor), FR36 (G1 vs NONE), OT06 (BULK vs
  NAMED — both "stay"), OT14 (B3 vs MIXED).

**Diagnosis.** The class labels are not reproducible at 80% because applying the
rules to texts that mix a symbol, a gloss and an object is a judgement call (the
verifier lists six such calls). Tightening the wording again would chase the same
judgement.

---

## D-018 · 2026-10-01 · G5 · PRE-REGISTERED — act only on consensus

**Rule.** A G5 action is taken on a root only where TWO independent classifications —
the amended table (D-012) and the second blind verifier — agree on the class, and the
action follows from that class without further judgement. Every other root stays
held, its value unchanged, its disagreement published with both readings.

**The consensus set (28 roots):** FR02, FR03, FR06, FR09, FR10, FR11, FR23, FR40,
FR42, FR45, FR49, NC04, NC14, NC19, NC23, OT02, OT13, OT18, OT19, OT20, OT23, OT30,
SP05, SP11, SP12, SP13, SP16, SP17.

**Actions it licenses** (each one commit, with before/after and a one-line revert;
executed next session, after the wording lanes are integrated):
- **Labels only** (16 DEMOTE roots, including the k_ℷ layer's FR02): status labels
  CALIBRATED / NUMEROLOGY, values unchanged.
- **SP05 — NAMED, the 24-cell** (agreed): `flavour_seed_coupling` → the 24-cell
  reading. Its θ₁₃ value moves 4.835° → 8.669°; the NuFIT comparison is reported
  after the change and did not choose it.
- **SP11 — B3, the w₀ family** (agreed): `dark_energy_betti` → `b3_live`; w₀ moves
  −23/24 → −42/43. Both lie more than 3σ from the DESI DR2 headline; reported, not
  chosen.
- **OT13 — MIXED, n_bridge_pairs part BULK** (agreed): pneuma's `n_bridge_pairs`
  reads D_space/2 = 12 instead of b₃//2 (21 at b₃ = 43).
- **SP13 — MIXED, SO(n) part BULK** (agreed): appendix H's SO(n) reads n = D_space.
- **OT18 — BULK** (agreed): the 13D shadow's "b₃/2 + 1" reads D_space/2 + 1 = 13.

**Kill condition.** If any licensed action, once made, breaks a test that is not a
pin of the old value, or moves a published number its decision did not name, it is
reverted and listed.

---

## D-017 · RESULT · 2026-10-01 · PR-1 CONFIRMED (prediction held, no kill)

Module `PM/geometry/instanton_cycles.py` (`subgroup_identity`,
`flat_associative_census`, `instanton_cycle_sweep`), tests
`tests/test_instanton_cycles.py` (7 passed).

- Subgroup identity dim(ℝ⁷)^S = 8/|S| − 1 holds on all 16 subgroups of Γ.
- Canonical point (n = 3): 1,792 rows (|S| = 1/2/4: 656/944/192; none with
  |S| = 8); rigid ∧ b₁ = 0: 0; qualifying: 0.
- Sweep: the canonical point and every n ≥ 1 pairwise-disjoint class of the first
  generating triple — 9,667 classes, 17,323,264 rows. **Qualifying rows: 0**, as
  predicted. The kill condition did not fire.
- The hypothesis is not vacuous: 245 classes carry 16 rows each with S = Γ that are
  rigid with b₁ = 0, and every one fails only on freeness — the lemma's mechanism. A
  hand-built free Hantzsche–Wendt control (outside Γ) is flagged; zeroing one shift
  switches it off.

**Consequence.** C2's M2-instanton route is KILLED for flat (totally geodesic)
associatives. Non-flat associatives stay out of scope; the known ones of this
resolution are S¹×S² with b₁ = 1 (Dwivedi–Platt–Walpuski 2023, Ex. 4.9). C2 (Re(T)) now
has no candidate mechanism inside Y₇.

**Correction to the PR-3 registration wording (kill condition unaffected).** H3c's
"ε ≥ 25/7" cannot hold, since ε ≤ 3 whenever V ≥ 0. The intended statement is
µ_CH²/2 = 25/7 > 3, so the late-time attractor is kination (ε → 3). PR-2 and PR-3 are
not yet run.

---

## D-019 · 2026-10-02 · PATH ASSESSMENT · PRE-REGISTERED (annex fixed before any run)

**Question.** Under the decision rule (lines 21–31 of this log), is the reasoned active
path — the D-015 selection — in the top group of all valid configurations of the
executable forks?

**Ruled by the author (2026-10-02):** ranking follows the decision rule
lexicographically; adoption is *recommend + one explicit accept*, never automatic.

**Comparator** (each criterion a tuple of integers, lower is better; a first difference
decides, whatever later criteria say):

| # | Criterion | Measured by |
|---|---|---|
| 1 | Validity (hard gate) | switch_search problem kinds CONTRADICTION / STRUCTURAL_FAILURE / VACUOUS; certificate claims with holds = False; converted import-time checks; target facts. A failing configuration is REJECTED with reasons and not ranked. |
| 2 | Closure | free_set_size from that configuration's own artifact plus discrete inputs declared by its options, then n_calibrated. UNMEASURED if the free set does not count the live forks. |
| 3 | Consistency | Count of broken identities (identity ledger with the narration's χ_eff), failing beacons, failing semantic gates, triple-track disagreements, disagreeing observable groups, OMEGA ≠ 0. A Pareto note marks fragile wins. |
| 4 | Elegance | (formulas not rooted in the seed, raw literal leaves) from that configuration's own dependency-walker output. Nothing typed by hand. |
| 5 | Data — tie-break only | (n_FAIL, n_TENSION, χ²) on rows common to the tied group, policy forks held fixed. Discloses the trials factor k; accepting on it adds one fitted degree of freedom. |

**Amendments pre-registered here:**
- (a) switch_search's `re_t_is_the_solved_vacuum` is re-scoped: only a configuration
  that claims a computed vacuum must have one (D-015 made Re(T) an open modulus).
- (b) Target fact: n_gen = 3 (the b₃_seed option texts already call one generation a
  structural refutation).
- (c) Checks failing in every assessed configuration are standing failures: excluded
  from the comparison and disclosed.
- (d) Policy forks (render_policy, theory_uncertainty_policy) are held at their active
  values.
- (e) A complete tie keeps the active path.
- (f) An UNMEASURED or UNEVALUABLE value on criteria 1–4 never falls through to a later
  criterion; such configurations are UNDECIDED.

**Kill conditions.** K1 the active run does not reproduce the published build; K2 the
screen and a full run disagree on a check (screen rejections for the forks involved are
void); K3 the null control (active against itself) is not identical; K4 a deciding
criterion rests on an UNMEASURED value or a run-stamp mismatch; K5 the sha256 of the
assessment configuration differs from the one recorded in the annex.

**Annex** `docs/decisions/D-019-path-assessment.md` holds the final assessment
configuration, its sha256, the constraint list and the measured run budget. It is
committed before the first PM assessment run; a run against any other sha256 is void.

**Code.** Only the comparator module may rank. switch_search, fork_implications and
preferred_path stay non-ranking (their tests are unchanged); new tests confine ranking
words to the comparator and pin the criteria order.

---

## D-020 · 2026-10-02 · PUBLICATION · PRE-REGISTERED — the Paths tab

**Request (the author, 2026-10-02):** export the switch/path graph and show it on the
website as a navigable, zoomable tab, with the active path (the one that generates the
paper) in gold and each node carrying its reasoning.

**Rule.** The Paths tab shows every declared fork, option, constraint and decision, and
every assessed configuration, each labelled by status (active, considered, retired,
rejected, not implemented) with its rationale, scores and verdict. It does NOT present
off-path physics values as predictions — D-013 still governs every other page, which
shows the active path only. The active path is drawn in gold with the decisions that
selected it.

---

## D-003 · ADDENDUM 2 · 2026-10-02 · the glued form on the compact (active) path

D-015 made the compact real form the active path, so the glued-orbit scan
(`PM/geometry/glued_orbit_scan.py`, the leading-order-in-t glued 3-form along the
resolution neck) was re-measured on it. Coarse grid, one family (radii 1, 1.2, 2, 10,
100; t = 0, 0.1, 1, 10; θ = π/4, π/2; 40 points):

| | t = 0 | t = 0.1 | t = 1 | t = 10 |
|---|---|---|---|---|
| compact orbit | 10/10 | 10/10 | 7/10 | 4/10 |
| split orbit | 0 | 0 | 3 | 6 |

Four points are degenerate (det B = 0); no point flips orientation inside the compact
orbit. On the split-form switch path the 2026-09-22 result stands unchanged
(DEGENERATE: never leaves the split orbit; orientation flips only).

**Reading.** At small amplitude the glued form is a genuine G₂ form of the compact
orbit at every sampled point. It leaves the orbit only at t ≥ 1, where the
leading-order expansion in t is outside its domain. This is consistent with Joyce's
construction, which needs a small resolution parameter and then corrects the glued
form to a torsion-free one. It marks where the leading-order ansatz breaks down, not a
failure of the construction. The holonomy wording therefore needs no domain qualifier
on the active path, provided the gluing amplitude is small — which is what the
construction assumes.

Tests re-pinned on both branches (`tests/test_glued_orbit_scan.py`): split
→ no crossover; compact → all points with t ≤ 0.1 compact, crossover only at t ≥ 1,
9 split and 4 degenerate on this grid.
