# The Bridge-to-Channel Assignment — a candidate solution

**Prepared:** 2026-08-30 · **Status:** PROPOSAL with a stated falsifier.
Not a ruling. Everything below is computed from structures already in the
framework; nothing is fitted and no new constant is introduced.

---

## The open problem

Two modules each left the same gap, from opposite ends:

- `PM/gauge/topological_terms.py` established that the topological term
  carries cross-shadow coupling at the θ = 90° vacuum, but recorded that
  **"which coordinate pairs the twelve physical bridges occupy on the cycle
  is NOT derived. The selection rule is exact; the assignment of bridges to
  channels is a modelling input still to be fixed."**
- `PM/geometry/four_face_structure.py` records that of **15400** possible
  4×3 groupings of the twelve bridges, **576** satisfy the cross-E₈
  property, and that the standard grouping is *"one of 576, NOT unique by
  cross-E₈ alone."*

So one module needs an assignment it cannot derive, and the other has 576
candidates it cannot narrow. This note supplies an independent constraint
computed from the G₂ structure itself.

---

## What the selection rule actually is, geometrically

The 42 allowed ordered channels are 21 unordered ones. Take each of the
C(7,2) = 21 coordinate pairs as a vertex and each allowed coupling as an
edge. The result is a graph on 21 vertices with 21 edges in which **every
vertex has degree exactly 2** — therefore a disjoint union of cycles. It
resolves into **seven triangles**:

| Triangle | Vertices (coordinate pairs) | Omits point |
|---|---|---|
| T₀ | (1,2) (3,4) (5,6) | 0 |
| T₁ | (0,2) (3,5) (4,6) | 1 |
| T₂ | (0,1) (3,6) (4,5) | 2 |
| T₃ | (0,4) (1,5) (2,6) | 3 |
| T₄ | (0,3) (1,6) (2,5) | 4 |
| T₅ | (0,6) (1,3) (2,4) | 5 |
| T₆ | (0,5) (1,4) (2,3) | 6 |

Each triangle *T_k* is a perfect matching of the six points other than *k*,
and — verified by enumeration, not asserted — **its three edges are exactly
the three Fano lines through *k***.

This is the selection rule restated as geometry rather than as a filter.
φ's seven associative triples *are* the Fano plane; the coupling graph is
its point–line incidence turned inside out. The 42 was never arbitrary:
7 points × 3 lines through each × 2 orderings.

---

## The constraint on the twelve bridges

The bridges occupy twelve of the twenty-one vertices, and the number of
live couplings is the number of edges internal to that choice. Enumerated
over **all C(21,12) = 293,930 placements**:

| Live couplings | 5 | 6 | 7 | 8 | 9 | 10 | **12** |
|---|---|---|---|---|---|---|---|
| Placements | 45927 | 107163 | 76545 | 51030 | 9450 | 3780 | **35** |

Two things follow.

**The maximum is 12, reached by exactly 35 placements — and 35 = C(7,4).**
Those 35 are precisely the placements that take **four complete triangles**.
Nothing else reaches 12; there is no 11.

**The framework independently carries four faces of three bridges each.**
`four_face_structure` derives 4 faces from b₂ = 4 of the TCS building
block, with 12 = 4 × 3 bridges. The coupling graph, derived from φ with no
knowledge of faces, says the twelve bridges maximise coupling exactly when
they form four complete triangles of three.

### The proposal

**Each face IS a triangle.** A face's three bridges occupy the three
coordinate pairs of one triangle *T_k*, so the four faces select four of
the seven Fano points, and inter-face coupling is inter-triangle coupling.

If true, this fixes the assignment up to which four of the seven points are
chosen (35 options), reduces the 576 cross-E₈ groupings by an independent
criterion, and gives the face structure a meaning inside the coupling
geometry rather than only in the Kähler moduli count.

---

## Narrowing 35 → 7 (criterion, not derivation)

Each triangle *T_k* is labelled by the coordinate *k* it omits, so choosing
four faces means choosing a **4-subset of the seven Fano points**. Under the
Fano symmetry those 35 subsets fall into exactly two orbits — computed, not
asserted:

| Orbit | Count | Description |
|---|---|---|
| contains a line | **28** | three of the four labels are collinear |
| arc (no 3 collinear) | **7** | each is the complement of one line |

All seven arcs leave exactly a **line** unchosen — verified for all seven. So
requiring the four face labels to be *generic* picks out seven candidates in
bijection with the seven lines, and the residual freedom becomes a labelling
(which line is omitted) rather than a further structural decision.

**This is a criterion with a name, not a result.** Nothing in the framework
forbids three collinear face labels, so the genericity assumption is stated
and carried as `status: CRITERION_STATED_NOT_DERIVED`. Adopt it and the
choice is 35 → 7; decline it and the choice remains 35. What *is* established
is that the space has exactly two orbits, so any future physical argument
only has to decide between two cases rather than among thirty-five.

---

## Which flux term the consciousness architecture needs

Under the **person-within-a-face** reading (the author's, 2026-08-31), the
argument that appeared to force Path A dissolves, and it is worth being
explicit about why.

A triangle is K₃ — complete. A face whose three bridges occupy one triangle
has all three internal pairwise couplings live, which is exactly the
condition for those three to reduce *jointly* rather than as three
independent events. Path B (Σ₇, degrees 3+2+2) supplies that.

And the framework's own OR operator is a **tensor product**,
`⊗_{i=1}^{12} R⊥_i` (`master_action.compute_distributed_or_reduction`), which
has no cross-terms by construction and factorises as 2¹² = (2³)⁴ — three
bridges per face, four faces. A central reduction across all twelve is
therefore the product of the four face-level ones and needs **no** inter-face
coupling.

So: **Path B is sufficient for the consciousness architecture under this
reading.** Path A would have been forced only under the alternative reading
in which a person integrates *across* faces — because the seven triangles are
disjoint components, inter-face coupling is structurally impossible in the
Σ₇ channel for every one of the 293,930 placements. That constraint is worth
keeping on record, since it means the two readings are experimentally
distinguishable in principle rather than a matter of taste.

Path A may still be required for reasons in the 13D sector; it is simply not
required by *this* argument, and it remains blocked on an underived C₃.

---

## Falsifier

**If the face grouping, once derived, does not correspond to four complete
triangles, this identification is dead.** Only 35 of 293,930 placements
qualify — 0.012% — so the data can rule it out decisively. The test is
mechanical once the grouping is available: map each face's three bridges to
their coordinate pairs and check whether the three pairs form one triangle.

Two ways it could fail that are worth naming in advance: the four faces
might map onto four triangles but with bridges *interleaved* between them
(same vertices, wrong partition), which would preserve the count of 12 while
falsifying the face↔triangle identification specifically; or the grouping
might sit at 9 or 10 live couplings, which would say the framework does not
maximise topological coupling and would need its own explanation.

---

## A retired kill condition (correction)

`AutoGenerated/topological_flux.json` previously stated:

> if the bridge-to-channel assignment places the physical bridges only on
> complementary NON-associative 4-sets, every physical channel is forbidden
> and this route is dead.

**That outcome cannot occur.** The minimum over all 293,930 placements is
five live couplings; zero never happens. The condition was written before
the placement spectrum was computed, and it describes an impossible event —
a kill condition that cannot fire is not a kill condition. It is retired in
the artifact (`kill_condition_retired`) rather than quietly deleted, and
replaced by the falsifier above, which can fire.

The correction strengthens the underlying result rather than weakening it:
cross-shadow coupling is not merely non-zero at the vacuum, it is
**structurally unavoidable** — no placement of twelve bridges on the cycle
can switch it off. What remains genuinely open is the magnitude and the
compact-manifold question, both unchanged and both still recorded as NOT
ESTABLISHED.

---

## What this does not establish

Still flat ℝ⁷ with constant-coefficient forms, so still coefficient ×
volume — a number, not a topological invariant, exactly as the Stage-4
report states. The triangle structure is a fact about φ's associative
triples and would hold on any G₂ structure with the same Fano incidence;
it does not by itself demonstrate topological content.

Nor does it derive *which* four of the seven points the faces choose. It
narrows an unbounded modelling input to a 35-element set with a testable
identification, which is progress, not closure.
