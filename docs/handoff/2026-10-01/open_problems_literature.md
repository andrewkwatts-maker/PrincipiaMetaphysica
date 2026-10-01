# Open problems C1–C4: literature check and pre-registration drafts

Research agent report, 2026-10-01 (recorded in the decision log as D-016; the
computations are pre-registered as D-017). No repository file was edited and no
engine computation was run; predictions marked **ANALYTIC** were derived by hand
and are what D-017 asks the engine to test. Every citation was checked against a
fetched record (arXiv API, Crossref, INSPIRE, full texts).

**Scope.** Every source concerns the compact (Riemannian) G₂ form — the active path
since D-015.

## 0. Verdicts at a glance

| # | Direction | Verdict | Reason |
|---|---|---|---|
| 1 | Chirality via the heterotic dual | **KILLED** | The dual of exactly this orbifold is published (Acharya–Kinsella–Morrison 2021, Ex. 3.2) and is non-chiral. Its bundle is the image of the G₂ geometry, so there is no extra datum to make chiral. Chirality would be a postulate that changes the internal space. |
| 2 | Chirality from the shadows as Hořava–Witten walls | **KILLED** | HW is anomaly inflow onto even-dimensional walls of an odd-dimensional (11D) bulk. In the 26D bulk, walls are 25D and the shadows 13D: both odd. A 10D wall also needs a 6D internal space, not Y₇. Y₇'s one wall-like limit is the non-chiral dual of row 1. |
| 3a | Moduli: M2 instantons on rigid associatives | **NEEDS COMPUTATION** (PR-1; predicted KILL in the flat class) | Harvey–Moore need rigid rational homology spheres. The known associatives of this resolution (Dwivedi–Platt–Walpuski 2023, Ex. 4.9) are S¹×S² with b₁ = 1. An analytic lemma excludes every totally geodesic candidate. |
| 3b | Moduli: corrections to K beyond (U/T)² | **KILLED** | The exact classical K = −3 ln V_X is homogeneous (ADV eq. 3.2), so the λ⁻⁵ runaway holds to all orders in U/T. Quantum corrections preserve the moduli space to all orders in 1/R (Becker–Robbins–Witten 2014). |
| 4 | Dark energy, multi-field | **KILLED** for sustained acceleration (ANALYTIC); **NEEDS COMPUTATION** to confirm (PR-3) | The bound holds off the axion slice; late-time attractors give ε ≥ 25/7 (Shiu–Tonioni–Tran 2023); the hyperinflation window (Bjorkmo–Marsh 2019) is empty because L ≥ 1/√2 > 1/√3. |
| 5 | Flavour from the three locus volumes | **KILLED** (as derivable) | No chiral points means no Yukawas. The locus volumes are gauge-kinetic functions f(τ) = T⁷, T⁶, T⁵ (Lukas–Morris eq. 1.3): gauge couplings, and unfixed moduli. |
| 6 | arXiv:2106.03886 | **IDENTIFIED**, directly relevant | Acharya, Kinsella, Morrison, JHEP 11 (2021) 065. Example 3.2 is the orbifold limit of the adopted Y₇. |

**Bottom line.** All four problems stay open; the verified literature offers no
candidate mechanism for any of them inside Y₇. C1 and C4 become "not derivable on
Y₇" — a chiral sector would be a postulate that changes the construction. C2 has
lost its last internal candidate, pending PR-1. C3's multi-field loophole is closed
at the classical level, pending PR-3.

## (a) Verified citations

### Website "standard physics used" list
| # | Citation | arXiv | DOI / ISBN | Status |
|---|---|---|---|---|
| W1 | I. Bars, "Survey of two-time physics", Class. Quantum Grav. 18 (2001) 3113–3130 | hep-th/0008164 | 10.1088/0264-9381/18/16/303 | CONFIRMED. Background only: the ghost-freedom theorem is not inherited. |
| W2 | I. Bars, C. Kounnas, "String and particle with two times", Phys. Rev. D 56 (1997) 3664–3671 | hep-th/9705205 | 10.1103/PhysRevD.56.3664 | CONFIRMED. "For the bosonic system in flat spacetime the critical dimension is 27 or 28, with signature (25,2) or (26,2)". Never 26. |
| W3 | T. Eguchi, A. J. Hanson, "Asymptotically flat self-dual solutions to Euclidean gravity", Phys. Lett. B 74 (1978) 249–251 | — | 10.1016/0370-2693(78)90566-X | CONFIRMED. |
| W4 | J. Polchinski, *String Theory, Vol. 1*, CUP 1998 | — | DOI 10.1017/CBO9780511816079; ISBN 978-0-521-63303-1 (hb), 978-0-521-67227-6 (pb) | CONFIRMED (cite the volume; D = 26 is the one-time (25,1) result). |
| W5 | B. S. Acharya, E. Witten, "Chiral fermions from manifolds of G₂ holonomy" | hep-th/0109152 | none (preprint) | CONFIRMED as a preprint. |
| W6 | J. Cheeger, D. Gromoll, "The splitting theorem for manifolds of nonnegative Ricci curvature", J. Differential Geom. 6 (1971) 119–128 | — | 10.4310/jdg/1214430220 | CONFIRMED. "Theorem 3" number UNVERIFIED. |
| W7 | M. Atiyah, E. Witten, "M-theory dynamics on a manifold of G₂ holonomy", Adv. Theor. Math. Phys. 6 (2002) 1–106 | hep-th/0107177 | 10.4310/ATMP.2002.v6.n1.a1 | CONFIRMED (arXiv/INSPIRE say 2003). Not a source for Yukawas. |

### Other sources (each verified via arXiv API + Crossref unless noted)
- Hořava, Witten, Nucl. Phys. B 460 (1996) 506–524, hep-th/9510209, DOI 10.1016/0550-3213(95)00621-4.
- Hořava, Witten, Nucl. Phys. B 475 (1996) 94–114, hep-th/9603142, DOI 10.1016/0550-3213(96)00308-2.
- Acharya, "N=1 heterotic/M-theory duality and Joyce manifolds", Nucl. Phys. B 475 (1996) 579–596, hep-th/9603033, DOI 10.1016/0550-3213(96)00326-4.
- Acharya, Kinsella, Morrison, JHEP 11 (2021) 065, arXiv:2106.03886, DOI 10.1007/JHEP11(2021)065.
- Witten, "Anomaly cancellation on G₂ manifolds", hep-th/0108165 (preprint).
- Witten, "Deconstruction, G₂ holonomy, and doublet-triplet splitting", hep-ph/0201018.
- Pantev, Wijnholt, J. Geom. Phys. 61 (2011) 1223–1247, arXiv:0905.1968, DOI 10.1016/j.geomphys.2011.02.014.
- Braun, Cizel, Hübner, Schäfer-Nameki, JHEP 03 (2019) 199, arXiv:1812.06072.
- Barbosa, Cvetič, Heckman, Lawrie, Torres, Zoccarato, PRD 101 (2020) 026015, arXiv:1906.02212.
- Lukas, Morris, PRD 69 (2004) 066003, hep-th/0305078, DOI 10.1103/PhysRevD.69.066003.
- Acharya, Denef, Valandro (ADV), JHEP 0506 (2005) 056, hep-th/0502060, DOI 10.1088/1126-6708/2005/06/056.
- Becker, Robbins, Witten, JHEP 06 (2014) 051, arXiv:1404.2460, DOI 10.1007/JHEP06(2014)051.
- Harvey, Moore, "Superpotentials and membrane instantons", hep-th/9907026.
- Harvey, Lawson, "Calibrated geometries", Acta Math. 148 (1982) 47–157, DOI 10.1007/BF02392726.
- McLean, "Deformations of calibrated submanifolds", Comm. Anal. Geom. 6 (1998) 705–747, DOI 10.4310/CAG.1998.v6.n4.a4.
- Joyce, "Conjectures on counting associative 3-folds in G₂-manifolds", Proc. Sympos. Pure Math. 99 (2018) 97–160, arXiv:1610.09836.
- Dwivedi, Platt, Walpuski, Commun. Math. Phys. 401 (2023) 2327–2353, arXiv:2202.00522, DOI 10.1007/s00220-023-04716-7.
- Acharya, Braun, Svanes, Valandro, JHEP 03 (2019) 138, arXiv:1812.04008.
- Obied, Ooguri, Spodyneiko, Vafa, arXiv:1806.08362.
- Rudelius, JHEP 10 (2022) 018, arXiv:2208.08989.
- Calderón-Infante, Ruiz, Valenzuela, JHEP 06 (2023) 129, arXiv:2209.11821.
- Shiu, Tonioni, Tran, PRD 108 (2023) 063527 (arXiv:2303.03418) and 063528 (arXiv:2306.07327).
- Copeland, Liddle, Wands, PRD 57 (1998) 4686, gr-qc/9711068.
- Brown, "Hyperbolic inflation", PRL 121 (2018) 251601, arXiv:1705.03023.
- Bjorkmo, Marsh, JHEP 04 (2019) 172, arXiv:1901.08603.
- Acharya, "Compactification with flux and Yukawa hierarchies", hep-th/0303234.

**Caution.** Never construct ATMP DOIs by pattern: a guessed DOI for Acharya 1999
resolves to a different paper. `references.py` correctly carries none for it.

## (b) Directions — key evidence

**1. Heterotic dual (KILLED).** AKM Example 3.2 "The Simplest Joyce Orbifold":
"Altogether, we find 12 T³'s of A₁ singularities (4 from each of α, β, and γ₂) …
we expect SU(2)¹² gauge symmetry with 3 adjoint chirals for each SU(2) and 7 neutral
chiral multiplets." "All of the matter in our examples lies in real representations
of the gauge group, so the spectra are non-chiral." The heterotic side is the
Borcea–Voisin (Schoen-limit) orbifold with point-like instantons. Acharya–Witten:
"chiral fermions will have to come from singularities of Q or points where Q passes
through a worse-than-orbifold singularity of X". On the loci (closed flat T³) a
harmonic Higgs 1-form is constant; the net chiral count is χ(T³) = 0 (Pantev–
Wijnholt eq. 3.40) — ANALYTIC, to check. Side findings: whether the RESOLVED Y₇ has a
coassociative K3 fibration is open (AKM footnote 1); the orbifold has three Kummer
fibrations — three duality frames, not three generations.

**2. Hořava–Witten walls (KILLED).** HW needs an 11D bulk with a gravitino,
even-dimensional codimension-1 walls and a 6D internal space; here walls are 25D,
shadows 13D (codimension 13), no gravitino multiplet is specified, Y₇ is 7D. The
model's E₈ blocks are rank-8 blocks of bulk directions, not HW's 248-dimensional
gauge groups (A4). Flagged, unverified: a single chiral spinor in 26 dimensions is
the classic gravitational-anomaly setting in one-time signature; whether that
carries to (24,2) is an open consistency question.

**3a. Instantons (NEEDS COMPUTATION, PR-1).** Harvey–Moore eq. (2.13): "the
contribution to the superpotential of a rigid supersymmetric rational homology sphere
in the G₂ manifold is W ∝ |H₁(Σ; Z)| exp[i∫_Σ(C + iφ)]". DPW Ex. 4.9 (this orbifold):
"up to 12 = 4 · 3 associative submanifolds", each S¹ × S², b₁ = 1, and "P[η] is never
unobstructed". Lemma (ANALYTIC): for N = (T_V + c)/S, b₁ = dim V^S; rigid ⇔
(V^⊥)^S = 0; dim(ℝ⁷)^S = 8/|S| − 1; so rigid + b₁ = 0 forces S = Γ, V a Fano line,
and then (n ≥ 1) a singular involution fixes points of the torus.

**3b. K corrections (KILLED).** ADV eq. (3.2): "K = −3 ln 4π^{1/3}V_X(s), where V_X …
is a homogeneous function of the sⁱ of degree 7/3". BRW: the Lagrangian moduli space
"remains valid to all orders in the α′ or inverse radius expansion" — "but not
exactly" (non-perturbative effects = 3a). The Chern–Simons term also vanishes for
flat SL(2,ℂ) connections on T³ (ANALYTIC).

**4. Dark energy (KILLED classically; PR-3).** 5√(2/7) is the universal
internal-G₄-flux volume exponent (V_E ∝ V_X^{−15/7}). For c₂ = 0,
V = 4e^K[K^{ij}N_iN_j + W₁²], terms scaling λ⁻⁵ and λ⁻⁷, so the bound holds on all
fields; the infimum is attained on the overall volume; µ_CH ≥ 5√(2/7) gives ε ≥ 25/7
(STT eq. IV.3, "analytic and not conjectural"); hyperinflation needs L < 1/√3 but
L ≥ 1/√2. Not excluded: transient acceleration. No G₂-specific bound exists in the
literature.

**5. Flavour (KILLED as derivable).** Lukas–Morris eq. (1.3): "The gauge-kinetic
functions for these multiplets depend on the type τ of the blow-up only and are given
by f(τ) = T⁷ for τ = α, T⁶ for τ = β, T⁵ for τ = γ." Witten hep-ph/0201018: "Yukawa
couplings … always come from membrane instantons". π₁(T³) = ℤ³ makes Wilson lines on
the loci continuous N = 4 moduli.

## (c) Pre-registration drafts — registered as D-017 (PR-1, PR-2, PR-3)

See `docs/DECISION_LOG.md` D-017 for the hypotheses, computations and kill conditions
exactly as registered. Implementation agents were launched 2026-10-01; their reports
are in this folder when they returned.

## (d) Notes for the lead
1. D-011's "K3 fibres" holds in the orbifold limit only (AKM fn. 1); D-009 is unaffected.
2. Cite arXiv:2106.03886 as JHEP 11 (2021) 065, DOI 10.1007/JHEP11(2021)065.
3. Acharya 1996's explicit pairs are J⁸₃₁ and the J^{8+l}_{47−l} family; the (12, 43) dual is AKM 2021.
4. Not Atiyah–Witten for Yukawas or chirality; Yukawas: Acharya–Witten §2.4 and Witten hep-ph/0201018; chirality: Acharya–Witten and Witten hep-th/0108165.
5. Bars–Kounnas give 27 or 28; Polchinski's 26 is the one-time result.
6. DOIs `references.py` could carry: Lukas–Morris 10.1103/PhysRevD.69.066003; ADV 10.1088/1126-6708/2005/06/056; Acharya 1996 10.1016/0550-3213(96)00326-4; none for Acharya 1999.
7. Harvey–Moore independently cite Joyce JDG II Prop. 1.1.1 for the π₁ criterion, agreeing with `references.py`.
