# The Bridge-to-Channel Assignment — CLOSED, on one stated assumption

**Prepared:** 2026-08-30 · **Closed:** 2026-09-01 · **Status:** RESULT, resting
on one assumption that must travel with every quotation of it.
Everything below is computed from structures already in the framework;
nothing is fitted and no new constant is introduced. Register cross-reference:
`docs/OUTSTANDING_ISSUES.md` §1.8 and §1.11.

---

## The open problem (as it stood)

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

So one module needed an assignment it could not derive, and the other had 576
candidates it could not narrow. The register listed *"nothing maps a bridge
index to a G₂ coordinate pair"* as the load-bearing geometric gap.

Both 15400 and 576 were prose figures with no implementation behind them.
They are now enumerated in code and agree with the closed forms
12!/((3!)⁴·4!) = 15400 and (4!)² = 576.

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

**The maximum is 12, reached by exactly 35 placements — and 35 = C(7,4).**
Those 35 are precisely the placements that take **four complete triangles**.
Nothing else reaches 12; there is no 11. The minimum is five, never zero.

**Each face IS a triangle.** A face's three bridges occupy the three
coordinate pairs of one triangle *T_k*, so the four faces select four of
the seven Fano points, and inter-face coupling is inter-triangle coupling.

---

## The one assumption

> **The E₈ block a bridge carries is a property of the CHANNEL, not of the
> face observing it** — one global labelling of the 7 Fano lines by 3 blocks,
> shared by every face.

This is an input. It is not derived from anything else in the framework, and
**every statement of the results below must carry it.** Since a face holds one
bridge per block, the assumption says the 3 lines through each chosen point
must receive 3 distinct blocks — the chosen point is *rainbow*.

**Kill condition:** any 5-point rainbow set, or any line-containing 4-set
admitting a labelling, retracts the corresponding half of the result below.

---

## What follows: two inputs become consequences

Enumerating all 3⁷ = 2187 labellings:

| was | now |
|---|---|
| `n_faces = 4` read off h^{1,1} = 4 of the TCS #187 building block, which `four_face_structure` itself classifies **FITTED** and dependent on having selected that manifold | **4 is the maximum.** No labelling makes 5, 6 or 7 points simultaneously rainbow. n_faces = 4 is forced. |
| `face_genericity` narrowed 35 → 7 by fiat; the `variants.json` fork read OPEN with *"NOT derived — nothing in the framework forbids collinear labels"* | **The 28 line-containing 4-point sets admit zero labellings**; each of the 7 arcs admits exactly 18. Genericity is a consequence. Fork OPEN → **RULED**. |

The earlier version of this note carried genericity as
`status: CRITERION_STATED_NOT_DERIVED`. That status is withdrawn: it is
derived, conditional on the assumption above.

---

## The structure closes as K₄

With the four faces as vertices:

| object | count | K₄ role |
|---|---|---|
| faces | 4 | vertices |
| channel-lines | 6 | edges |
| **bridges** | **12** | the **directed** edges — ordered pairs of faces |
| E₈ blocks | 3 | the three perfect matchings |
| spare line | 1 | the arc's complement — incident to no face |

So **"bridge" is literal**: a directed connection between two faces. The bridge
count 12 is K₄'s directed-edge count, not a separate input. And
18 = 3! proper 3-edge-colourings of K₄ × 3 free colours for the complement
line.

`n_gen = 3` is fixed twice over — Leech 24 = 8 + 8 + 8, and q + 1 = 3 lines
through each point of the order-2 projective plane — rather than being
12/4 arithmetic.

---

## The assignment is unique up to symmetry

7 arcs × 18 labellings = 126 residual possibilities. All 126 are
relabellings, on three counts:

1. **The block partition is canonical given the arc.** Each K₄ edge {p, q}
   spans a Fano line, and that line meets the arc's complement line in
   exactly one point. Grouping the six edges by which complement point they
   hit gives fibres that are precisely the three perfect matchings of K₄. The
   arc fixes the partition of bridges into E₈ blocks; the counted 3! is only
   which complement point gets *called* block 0, and a block's name is not an
   observable.
2. **The spare colour touches nothing.** The other factor in 18 = 3! × 3 is
   the colour of the complement line, which lies on no face, is incident to no
   bridge, and enters no coupling.
3. **The seven arcs are one orbit.** Aut(Fano) = PSL(3,2) has order 168, is
   transitive on the 7 lines and hence on the 7 arcs; the arc stabiliser of
   order 168/7 = 24 acts as the full S₄ on that arc's four faces.

So the assignment is unique up to the symmetry group of the structure — the
ordinary sense in which a geometric object is determined.

**Conditional kill:** the uniqueness rests on nothing *else* in the framework
distinguishing a Fano direction. A preferred imaginary octonion, or a shadow
asymmetry singling out one coordinate, would break PSL(3,2) and make the
choice of arc physical again. Nothing currently does this, and the claim must
keep saying it is conditional.

---

## Stride-4 is a convention, not a fitted choice

The **576** cross-E₈-valid groupings form a single **regular** orbit under
S₄ × S₄ renaming bridges inside E₈ blocks. Since the orbit is regular
(576 = (4!)²), no grouping in it is distinguished: the stride-4 partition
{i, i+4, i+8} used by `leech_lattice` is a **coordinate convention**, not a
selection among rivals.

The long-standing "stride-4 vs contiguous" conflict is settled the other way:
they are **different objects**. The contiguous grouping used in
`consciousness/four_dice_sampling.py` puts its entire first face inside one
E₈ block, so it is not one of the 576 at all and was never a rival.

---

## A retired kill condition (correction, kept on record)

`AutoGenerated/topological_flux.json` previously stated:

> if the bridge-to-channel assignment places the physical bridges only on
> complementary NON-associative 4-sets, every physical channel is forbidden
> and this route is dead.

**That outcome cannot occur.** The minimum over all 293,930 placements is
five live couplings; zero never happens. The condition was written before
the placement spectrum was computed, and it describes an impossible event —
a kill condition that cannot fire is not a kill condition. It is retired in
the artifact (`kill_condition_retired`) rather than quietly deleted.

The correction strengthens the underlying result rather than weakening it:
cross-shadow coupling is not merely non-zero at the vacuum, it is
**structurally unavoidable** — no placement of twelve bridges on the cycle
can switch it off.

---

## Which flux term the consciousness architecture needs

Under the **person-within-a-face** reading (the author's, 2026-08-31):

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

So **Path B is sufficient for the consciousness architecture under this
reading.** Path A would have been forced only under the alternative reading
in which a person integrates *across* faces — because the seven triangles are
disjoint components, inter-face coupling is structurally impossible in the
Σ₇ channel for every one of the 293,930 placements. That constraint is worth
keeping on record, since it means the two readings are experimentally
distinguishable in principle rather than a matter of taste.

Path A may still be required for reasons in the 13D sector; it is simply not
required by *this* argument, and it remains blocked on an underived C₃ — the
framework derives φ only on the 7D cycle, and the 13D side carries scalars.

---

## What this still does not establish

Still flat ℝ⁷ with constant-coefficient forms, so still coefficient ×
volume — a number, not a topological invariant, exactly as the Stage-4
report states. The triangle structure is a fact about φ's associative
triples and would hold on any G₂ structure with the same Fano incidence;
it does not by itself demonstrate topological content. Topological content
requires harmonic representatives on a compact G₂ manifold with b₃ = 24
(deferred DEC work, `metaphysica/docs/FUTURE.md`).

**And the TCS obstruction is independent of all of this and still open.**
Crowley–Nordström forces b₂ + b₃ odd for any twisted connected sum; the
claimed (b₂, b₃) = (4, 24) gives 28, even. b₃ = 24 survives (Joyce 1996 has
(7, 24)); what fails is the pairing with b₂ = 4 — the four-faces reading this
whole note rests on. Note that n_faces = 4 no longer *depends* on b₂ = 4,
which weakens the coupling between the two problems but does not dissolve the
obstruction.
