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
