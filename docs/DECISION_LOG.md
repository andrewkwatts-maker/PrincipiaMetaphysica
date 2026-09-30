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
