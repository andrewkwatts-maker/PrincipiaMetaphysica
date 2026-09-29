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
