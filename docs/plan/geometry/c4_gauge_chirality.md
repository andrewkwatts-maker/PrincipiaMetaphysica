# C4: gauge group and chirality on the smooth (12, 43) manifold

Read-only audit. Engine root: `metaphysica/src/metaphysica/simulations` (abbrev. `S/`).

## Verdicts
| Item | Class | Summary |
|---|---|---|
| (a) SU(3)xSU(2)xU(1) | MISMATCH (plus partial ABSENT) | Names the right mechanism (ADE loci) but the active Y7 is the smooth resolution, which has U(1)^12 only |
| (b) n_gen = 3 | FORMULA | n_gen = b2/4 = 3: a counting rule, no mechanism. The engine says so itself |
| (c) fermion reps | ABSENT | Chirality is declared OPEN (D-011); nothing derives the reps |

## (a) Gauge group: MISMATCH
- `S/PM/gauge/non_abelian_kk_gauge.py:664-668`: "SU(3)_C arises from A2-type ADE singularities along associative 3-cycles ... SU(2)_L arises from A1 singularities". Header line 9 says "TCS manifold".
- `S/PM/geometry/g2_geometry.py:1142-1150`: "12 A1 loci, giving U(1)^12 on the resolution and SU(2)^12 at the orbifold point. Y7 has no D5 locus, so the SO(10) mechanism ... is the framework's model construction, not a property of Y7."
- The engine's own geometry layer is correct: the smooth resolution gives U(1)^b2 = U(1)^12.
- The gauge modules (`su3_qcd_gauge.py:9`, `non_abelian_kk_gauge.py`) still describe a TCS manifold with A2 loci. Y7 has only A1 loci, and TCS is REFUSED in the `g2_construction` fork.
- Published text contradicts itself. `sections.json` ~5537 says "SU(3)_C from associative 3-cycles, SU(2)_L from co-associative 4-cycles". A calibrated cycle is not an ADE singularity, and Acharya 1998 gives the gauge group only from singularities.
- Nothing produces SU(3): there is no A2 locus on Y7, and U(1)_Y is "residual Abelian structure" with no derivation.
- The SU(2) here is SU(2)^12 at the orbifold point, not a single SU(2)_L. The 12 is the A1 census, so the SU(2) count is also unexplained.

## (b) Generations: FORMULA
- `S/PM/particle/fermion_generations.py:17`: "n_gen = b_2 / n_faces = b_2 / 4 = rank(Gamma) = 3". The adopted route is `b2_over_faces` in fork `n_gen_source`.
- `S/PM/particle/fermion_generations.py:37-39`: chi_eff/48 "is not an index theorem for chirality" (codimension-7 points).
- Other fork options: `b3_over_dim_O`, `chi_over_24` and `chi_eff_over_48` are all formulas. chi/24 is the F-theory or CY4 flux/tadpole count, and chi(G2) = 0. chi_eff = 144 is a sum of K3 Euler characteristics, not chi(Y7).
- Valid mechanism: Acharya-Witten (hep-th/0109152). Generations equal the number of conical (C^3/Z_N-type) points, or the zero-mode count of the chiral index, so b2/4 has no standing as a count of them.

## (c) Representations: ABSENT
- `S/PM/particle/chirality.py:11-16`: Y7's "singular loci are disjoint, so it has no codimension-7 points, and a smooth G2 compactification gives no chiral fermions". `appendix_q_index_theorem.py:27-28` says "Chirality is OPEN (D-011)".
- The proposed projector P_L = (1+*Phi)/2 (`chirality.py:23-25`) is labelled "not established".
- `foundations.py:1130` says a CY3 route is OFF-PATH.
- Nothing derives the Q, u, d, L, e reps or hypercharges.

## What a correct mechanism needs (literature, not engine results)
- Non-abelian group: keep the A1 loci unresolved, with b2 = 0 locally and SU(2) along each associative T^3 (Acharya hep-th/9812205). SU(3) needs an A2 locus; SU(5) needs A4 (G2-MSSM, Acharya et al. 2007-08).
- Chirality and matter: conical points on the singular locus (Acharya-Witten hep-th/0109152; Atiyah-Witten hep-th/0107177). Matter at ADE enhancement points is a standard statement.
- Alternative: an N=1 duality or heterotic dual with explicit bundle data (index = n_gen), or intersecting-brane models. None is in the engine.

## Fork registry (`S/core/variants.py`)
- `b3_seed` (line 805): options at 851-882 include "b_3 = 7, b_2 = 0 -- the unresolved orbifold limit" and "four/eight A1 families". These are partial resolutions, but they only set (b2, b3) and do not change the gauge content.
- `b3_origin` (987) and `joyce_contribution_table` (1094, "T^3 x C^2/{+-1} singularities"): A1 only.
- `n_gen_source` (905): formulas only.
- `g2_construction` (1630): `joyce_orbifold` is adopted. `fano_tcs` is REFUSED.
- No fork models an A2/A4 locus, a conical point or a partial resolution that keeps SU(2). The needed fork is "singular vs resolved vs partially resolved", with a gauge-group consequence.

## Most important correction
State plainly that Y7 as the smooth (12, 43) resolution gives U(1)^12, not SU(3)xSU(2)xU(1). Either:
1. Move the SM gauge group and chirality to the unresolved or partially resolved orbifold with A1 SU(2) loci, add a stated source for SU(3) and U(1)_Y, and add conical points for chirality; or
2. Label (a) and (c) as external inputs.
Remove "TCS", "A2 loci" and "co-associative 4-cycles give SU(2)" from the published and engine text, and describe n_gen = b2/4 as a rule awaiting a conical-point count.
