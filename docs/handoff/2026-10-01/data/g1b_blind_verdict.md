# Blind re-verification: bridges and singular components on the Joyce (Z/2)^3 orbifold

Verifier: independent re-derivation, 2026-10-01. I did not open the forbidden files:
`bridge_component_map.py`, its test, `DECISION_LOG.md`, `OUTSTANDING_ISSUES.md`,
`g1b_verify/`, and `closed_geometry/findings.py`.

I did read: `docs/BRIDGE_CHANNEL_ASSIGNMENT.md`, `joyce_resolution.py`,
`joyce_reachability.py`, `fundamental_group.py` (not used), `half_shift_enumeration.py`,
and parts of `joyce_orbifold.py` and `derived_contribution_table.py` (only to learn
what their outputs are).

## Verdicts at a glance

| # | Hypothesis | Verdict |
|---|---|---|
| 1 | Spanning singular triple = non-concurrent lines; this fixes an arc; the complement line is unique | **CONFIRMED** |
| 2 | Each perfect matching contains exactly one side of the triangle, so blocks and involutions are in bijection | **CONFIRMED** |
| 3 | 4 + 4 counts, a 3x4 bijection exists, "canonical up to a Klein-four relabelling" | **PARTLY CONFIRMED.** Counts, existence and the torsor structure are CONFIRMED. The canonicity clause is **REFUTED**. |
| 4 | Example-4 classes carry an 8-component involution, so no bijection; all-plain gives (12, 43) | **CONFIRMED**, with one caveat: (12, 43) is not exclusive to all-plain classes |

**Kill conditions.** None of the four listed kill conditions fired. Section 5 gives the counts.

## Coverage and method

- **Independent model** (`blindcore.py`). I make no use of the engine here.
  - An action is a homomorphism Γ → F₂⁷ (half-period shifts), taken modulo conjugation by quarter-period translations.
  - That gives 2¹⁴ = 16,384 classes.
  - The normalisation slice is deliberately different from the engine's.
  - Fixed sets, Γ-orbits of the fixed 3-tori, stabilisers and the (b₂, b₃) lift-character formula are all computed from the affine action directly.
  - On every n = 3 class I also brute-forced disjointness on the 4⁷ quarter-grid of T⁷.
- **Engine as input** (`s3_engine_crosscheck.py`).
  - Covers all 28 generating triples × 16,384 assignments = 458,752 assignments, using the engine's own `elements`, `is_singular`, `fixed_sets_disjoint`, `joyce_resolution.singular_components`, `joyce_reachability.class_options` and `all_components_are_a1`.
  - Every triple parametrises all 16,384 classes bijectively (checked against my canonical keys).
  - There are zero mismatches with the independent model, class by class: n, disjointness, singular lines, components per involution, (b₂, b₃) sets and the all-plain flag.
- **Counting conventions.** I give counts both as distinct classes (16,384 total) and as engine assignments over all 28 triples (each class appears 28 times).
- **Disjoint classes by n:**

  | n | classes |
  |---|---|
  | 0 | 6,296 |
  | 1 | 6,783 |
  | 2 | 2,520 |
  | 3 | 364 |
  | ≥ 4 | none |

  So n ∈ {0..3} is confirmed.

## H1: CONFIRMED (`s1_fano_h1_h2.py`, `s2_census.py`)

- **Γ from φ.** A sign flip on S preserves every term of φ exactly when |S ∩ line| is even for all lines. This gives |Γ| = 8, and the non-identity elements flip exactly the complements of the 7 lines.
  - This is independent of φ's coefficient signs; I also checked it with random-sign coefficients.
  - The group law is: σ_l σ_m = σ_n, where n is the third line through l ∩ m.
- **Spanning versus concurrent.** Of the 35 triples of distinct non-identity elements, 28 span Γ and 7 do not. The spanning ones are exactly the non-concurrent ones.
- **The arc.** For all 28 triangles:
  - the 3 vertices are distinct and non-collinear;
  - exactly one point q lies on none of the lines;
  - vertices + q form a 4-arc;
  - exactly one line misses the arc, and it equals the complement.
  - The 28 triangles give the 7 arcs, 4 triangles per arc.
  - Bonus: the complement line is the fixed line of σ₁σ₂σ₃, which is non-singular on every n = 3 class.
- **Concrete classes.** On all 364 disjoint n = 3 classes (10,192 engine assignments) the singular lines are non-concurrent. The kill count is 0.
- **Engine canonical point.** `representative_point(3)` has:
  - triple (0, 1, 3), shifts ((0000000), (0000010), (0000101));
  - singular lines exactly **(0,1,2), (0,3,4), (1,3,5)**;
  - arc {0, 1, 3, 6}, q = 6, complement line 245.

## H2: CONFIRMED (`s1_fano_h1_h2.py`, `s2_census.py`)

- **One side per matching.** All 84 matchings (28 triangles × 3) contain exactly one triangle side: 0 have 0 sides and 0 have 2. This also holds on all 364 concrete n = 3 classes (1,092 matchings).
- **Two descriptions agree.** For every triangle, "block t ↔ the involution whose side lies in matching t" equals "block t ↔ the unique singular line through t".
- **Coset form.** Block t's two channel-lines are {line of σ_i, line of σ_i·ω}, with ω = σ₁σ₂σ₃. So the blocks are the non-trivial cosets of ⟨ω⟩.
- **Equivariance.** The bijection is equivariant under every symmetry of every all-plain class (asserted in `s4`).
- **Canonical point.** Blocks are 2 ↔ 012 ({01, 36}), 4 ↔ 034 ({03, 16}), 5 ↔ 135 ({06, 13}).

## H3: PARTLY CONFIRMED; the canonicity clause is REFUTED (`s1`, `s2`, `s3`, `s4_h3_torsor_canonicity.py`)

### Confirmed

- **Bridge record.** Reconstructed from its own definitions:
  - At most 4 points are simultaneously rainbow.
  - Each of the 7 arcs admits 18 labellings; each of the 28 line-containing 4-sets admits 0.
  - On every arc, the bridges (face k, line through k) are exactly K4's 12 directed edges.
  - Under every rainbow labelling, the blocks are the three perfect matchings, with **4 bridges per block** and one bridge per block at each face.
- **4 components per involution.** This holds on all **280** all-plain classes (7,840 engine assignments), read off the engine's `singular_components`.
  - The engine's A1 filter `all_components_are_a1` coincides exactly with all-plain.
- **The bijection exists.** A 3x4-respecting bijection exists on all 280 all-plain classes.
- **Both sides are torsors** (all 280 classes):
  - The arc's Klein group K (double transpositions, realised by collineations) acts regularly on every block.
  - V_i, the image of the half-period translations H = (Z/2)⁷ (isometries commuting with Γ), acts regularly on the 4 components of every involution. |V_i| = 4.

### Refuted: "canonical up to a Klein-four relabelling within each block"

1. **The torsor structure does not constrain the bijection.** For every block, all **24 of 24** bijections B_i → C_i intertwine K with V_i (f K f⁻¹ = V_i). The reason is that S₄ = AGL(2,2): every bijection between two V₄-torsors is affine for some identification of the two groups. Modulo Klein-four relabelling this leaves **6 classes per block, 216 per class**, not 1.
2. **Nothing in the geometry identifies the two Klein groups.**
   - K is realised only by collineations that move q. The orbifold's symmetries fix the singular triangle, so they lie in its stabiliser S₃, which meets K trivially.
   - V_i is realised by translations, and these fix every bridge.
3. **The orbifold's own symmetries obstruct it.** I computed, per class, every isometry x ↦ Px + b (P a signed permutation, b a quarter period) that preserves the class. All of them preserve the current framework φ (and Bryant's φ₀), so they are G₂ automorphisms. I then counted the V-classes of bijections they leave invariant.

| All-plain type (pair labels) | classes | symmetries mod H | invariant V-classes (of 216) | orbits on the 13,824 bijections |
|---|---|---|---|---|
| (0,1)(0,1)(0,1) | 28 | S₃ (6) | **0** | 146 |
| (0,1)(1,1)(1,1) | 84 | Z/2 | **0** | 108 |
| (0,1)(1,0)(1,1), incl. the engine's canonical point | 168 | trivial | 216 (no selection) | 432 |

Classes with exactly one invariant V-class: **0 of 280**.

**Explicit obstruction.** Take the S₃-symmetric class on the same triangle as the canonical point (012, 034, 135). The φ-preserving isometry induced by (0 1)(4 5):
- fixes all 4 components of the 012-involution;
- swaps bridges 0→1 and 1→0 of that involution's block;
- fixes 3→6 and 6→3.

Any bijection would have to conjugate this transposition into a Klein-four translation, which is impossible.

**Conclusion.** On 112 of 280 all-plain classes, no bijection is canonical even up to Klein-four. On the other 168 (including `representative_point(3)`) the torsor argument leaves 216 equally admissible V-classes. Under no reading is the bijection unique up to symmetry: there are 108 to 432 orbits per class.

## H4: CONFIRMED, with a caveat (`s2_census.py`, `s3_engine_crosscheck.py`)

- **Census.** The 364 n = 3 classes split into 280 all-plain (4,4,4) and **84 Example-4 type (4,4,8)**. In engine assignments this is 10,192 = 7,840 + 2,352. Per triangle it is 10 + 3.
- **Example-4 classes:**
  - Each has **exactly one** involution with 8 components; no involution anywhere has 16.
  - The 8 families have |Stab| = 4. The extra element acts freely on the T³: it flips 2 coordinates and half-translates the third. This is Joyce's T³/Z₂.
  - Engine `class_options` profile: {2: 8, 4: 8}.
- **No bijection on non-all-plain classes.** The 3x4 bijection exists on exactly the all-plain classes. On non-all-plain classes the count is 0, so the kill condition does not fire.
- **(b₂, b₃) on all-plain classes.** Every all-plain class gives exactly {(12, 43)}, from both the engine and the independent model.
- **Caveat.** Under the engine's per-family lift model (which I reimplemented independently), every Example-4 class reaches (8+k, 47−k) for k = 0…8. **All 84 of them include (12, 43)**, at k = 4.
  - So (12, 43) holds on the all-plain members, but it does not identify them.
  - The correspondence is characterised by the component profile (4,4,4), not by the Betti pair.

## Isomorphism types (`s5_isomorphism_types.py`)

Up to PSL(3,2) the 364 classes form 4 orbits:

| members | stabiliser | type |
|---|---|---|
| 168 | 1 | all-plain |
| 84 | Z/2 | all-plain |
| 28 | S₃ | all-plain |
| 84 | Z/2 | Example-4 |

## 5. Kill conditions

| Kill condition | Count |
|---|---|
| n = 3 class with concurrent singular lines | 0 / 364 classes (0 / 10,192 assignments) |
| Perfect matching with 0 or 2 singular sides | 0 / 84 abstract, 0 / 1,092 concrete |
| Structure-preserving bijection on a non-all-plain class | 0 / 84 classes (0 / 2,352 assignments) |
| Bridge record not K4's directed edges on an arc | does not fire (verified on all 7 arcs and all 18 labellings each) |

**Not a listed kill condition:** the "canonical up to Klein-four" clause fails (H3).

## Side note: the framework's φ changed during this run

- `g2_differential.py` was modified at 22:39:46. Before that, φ had all + signs on the seven lines; afterwards it has −1 on 135.
- **The all-plus form was split, not G₂.**
  - Its induced metric has signature (4,3).
  - Only 24 collineations lifted to φ-preserving signed permutations, and they all fix the line 135.
  - The current φ is definite, with signed-permutation stabiliser of order 1,344 = 2³·168 (Bryant's φ₀ gives the same).
- **Effect on these results.** None of H1–H4's numbers depend on it: Γ and the census are sign-independent, and the engine re-run after the change was identical. The H3 refutation also holds under the old split φ: 64 classes are obstructed and 0 have a unique invariant class (`s4`, `s6`).

## Scripts and outputs (all in this folder)

Run in this order: `s1`, `s2`, `s3`, `s4`, `s5`, `s6`. `s4` and `s5` read `s2_n3_classes.json`; `s4` reads `s3_results.json`.

| Script | Purpose | Output |
|---|---|---|
| `blindcore.py` | Independent model | — |
| `s1_fano_h1_h2.py` | H1, H2, bridge record, K torsor | `s1_results.json` |
| `s2_census.py` | Independent census | `s2_results.json`, `s2_n3_classes.json` |
| `s3_engine_crosscheck.py` | Engine cross-check over all 28 triples, canonical point | `s3_results.json` (first run under the all-plus φ kept as `s3_results_run1_allplus_phi.json`; identical) |
| `s4_h3_torsor_canonicity.py` | H3 torsors and symmetry obstruction | `s4_results.json` |
| `s5_isomorphism_types.py` | PSL(3,2) orbits | `s5_results.json` |
| `s6_phi_lift_check.py` | φ-lift validation (Bryant control) and metric signature | `s6_results.json` |
