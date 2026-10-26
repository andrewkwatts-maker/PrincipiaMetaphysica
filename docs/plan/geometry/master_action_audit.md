# Master action audit (Track M)

Worktree: metaphysica-master, branch master-audit (= core-paper 838bebc). Nothing committed.
Test: tests/test_master_action_is_one_consistent_statement.py (12 tests).

## 1. Verdict

The master action is not well defined. The engine holds seven to nine
different "master action" statements. They agree on the bulk dimension and
signature (26D, (24,2), two times, one per 13D (12,1) shadow, 12 bridge pairs,
Weyl Cl(24,2) spinor of 4096 components) after the 2026-08-31 signature ruling.
They disagree on field content, and no one of them is a complete functional:
several terms are named symbols with no definition (L_C, V_bridge, V_face,
V_tor, OR^i, rho_breath) and the coefficients lambda, m, g, K, xi-phi are not
produced by any simulation. The reduction 26 -> 13 -> 4 is described, not
performed: no code integrates any term over an internal space.

## 2. Inventory

| # | Where | id | Content |
|---|---|---|---|
| A | gauge/master_action.py | pneuma-master-action-v23 (1.1) | R + Psi-bar(i Gamma D - m)Psi + lambda (Psi-bar Psi)^2 + sum_12 L_bridge^i + L_C |
| B | derivations/lagrangian_master.py | master-action-26d-full (2.1.5) | (M^24/2) R - (1/4g^2) Tr F^2 + Psi-bar Gamma D Psi - K\|dT\|^2 - V(T); with 2.1.6-2.1.9 sector formulas, E8xE8 YM, xi R phi^2 |
| C | same | master-action-two-layer-or (2.1.G1) | R + Psi-bar i gamma(D+T) Psi + \|dPhi\|^2 - V + (1/24) F^phi + sum R_n psi_n D psi_n - ln Vol dt + V_bridge + sum_4 V_face |
| D | same | bulk-action-26d-v23 (2.1.H1, ANSATZ) | R/(2 kappa^2) - (1/2)\|F_4\|^2 + V_mod + V_tor + sum R_n psi_n D psi_n + V_bridge + sum_4 V_face |
| E | config/core_formulas.py | master-action-27d (id legacy, text 26D) | M^24 R + Psi-bar(i Gamma D - m)Psi + L_bridge |
| F | gauge/master_action.py | shadow-action-13d-v23; effective-action-4d-v23 | 13D: R_13 + Psi-bar i gamma D Psi + V_face; 4D: -(M_Pl^2/2) R + L_SM + L_portal + L_DM |
| G | lagrangian_master.py | reduced-lagrangian-13d / -4d | same chain, with torsion T_omega; 4D SM-like L |
| H | pneuma_mechanism.py | lagrangian-hierarchy-complete (L1-L4) | L1 R + Psi-bar(i Gamma D - m_P)Psi; L2 M^11 R_13 + Psi_64 bar(...)Psi_64 (v. core_formulas lagrangian-13d-effective: M^10 R_12 -- inconsistent) |
| I | config/parameters/master_action.py | class doc | M^25 R (was); BULK_PLANCK_POWER = 23 (25D legacy) |
| J | derivations/gauge_sector_complete.py | su3/su2/u1 *-lagrangian-*-v19 | Not a master action: 4D L = -1/4 F^2 + psi-bar(i gamma D - m)psi. Mostly-minus, canonical, consistent. Sources SU(3)/SU(2) are OPEN on smooth Y7 (D-011) |

## 3. Canonical statement (as the engine defines it, A with B's gauge and moduli sectors)

Bulk M^{24,2}, D = 26, ds^2 = -dt_1^2 - dt_2^2 + sum_{i=1}^{12}(dy_{1i}^2 + dy_{2i}^2). Measure sqrt|G| (det G > 0 for two times).

$$
S_{26} = \int d^{26}X \sqrt{|G|}\Big[\tfrac{M_*^{24}}{2}R_{26}
 + \bar\Psi_P\,(i\Gamma^M D_M - m)\Psi_P + \lambda(\bar\Psi_P\Psi_P)^2
 - \tfrac{1}{4g^2}\mathrm{Tr}\,F_{MN}F^{MN}
 - K_{T\bar T}|\partial T|^2 - V(T,\phi) + \xi R_{26}\phi^2
 + \sum_{i=1}^{12}\mathcal L^{i}_{\rm bridge} + \mathcal L_C\Big],
\qquad M_*^{24}=\kappa^{-2}=(8\pi G_{26})^{-1}.
$$

This union is NOT any one formula in the engine; it is the superset of A and B.
Neither contains the other. C and D add flux, KK-tower and OR potentials on top.

## 4. Term table

Mass dimension in D = 26 with [d^26X] = -26. Needs each term = 26.

| Term | Coefficient | Mass dim of term as written | Source | Status |
|---|---|---|---|---|
| R_26 | M_*^24/2 (B, E now) ; bare 1 (A, C, F: was) | M^24 * 2 = 26 OK only with M^24; bare R is 2, unbalanced | input scale M_*; ~1e16 GeV is stated, no simulation derives it | INPUT |
| Psi-bar Gamma D Psi | 1 | 2 * 12.5 + 1 = 26 OK | Cl(24,2) Weyl, 4096 | POSTULATED |
| m Psi-bar Psi | m | 25 + 1 = 26 OK | no value | OPEN: Psi-bar Psi = 0 identically for one Weyl spinor in even D |
| lambda (Psi-bar Psi)^2 | lambda, dim -24 | 50 - 24 = 26 | no value, none derived; attached `value` 0.408 = 1/sqrt6 is not shown to be lambda | OPEN, same vanishing |
| -(1/4g^2) Tr F^2 | 1/g^2, dim +22 | 4 + 22 = 26 | uses gauge.g_gut, which is the dimensionless 4D coupling | OPEN (map bulk g -> g_4 not derived); E8xE8 vs SM group not reconciled |
| -K\|dT\|^2 | K | dim of K must be 24 for T dimensionless | no value | OPEN |
| V(T,phi) | racetrack Lambda_i, a_i = b3/i | Lambda_i must carry M^26 | a_i calibrated at b3 = 24 (off-path seed); Y7 has none; moduli OPEN | OFF-PATH / OPEN |
| xi R phi^2 | xi = (D-2)/(4(D-1)) = 6/25 | [phi] must be 12; but g_s = e^phi needs phi dimensionless | arithmetic correct | DERIVED arithmetic; conflict OPEN |
| sum_12 L_bridge^i | rho_breath^i + OR^i(Psi) | undefined | rho_breath, OR^i never given as functions | OPEN |
| L_C (S^{2,0}) | none | undefined; (24,2) count leaves no room | no definition | OPEN |
| -(1/2)\|F_4\|^2 (D) | 1 | M-theory 11D object in a 26D bulk | none | ANSATZ |
| sum R_n psi_n D psi_n (C, D) | R_n = exp(-lambda_n / b3) | KK tower is a reduction output, not a bulk term | b3 off-path seed 24 vs live 43 | double counts Psi_P |
| V_bridge, V_face^(f), V_tor | none | undefined | none | OPEN; V_bridge double counts L_bridge |

Reduction: M_Pl^2 for 13D -> 4D on 9 internal dims is M_*^{11} Vol_9 (D-2 = 11). The engine wrote M_*^9 Vol(V_7), which is the 11D formula; now stated as M_{11}^9 = M_*^{11} A_2 effective, A_2 = area of the 2 frozen residual bridge dims.
Cosmological constant Lambda = (int F^phi)^2 / Vol ~ 1e-52 m^-2: a size claim with no derivation in code.
Chain 26 -> 13 -> 7 -> 4: 13 = 7 (Y7) + 4 + 2 residual. The old kk-ansatz-7-4 reduced a "7D spacetime" on S^3.

## 5. Inconsistencies found

1. Field content differs across A, B, C, D, E (see inventory). No single action.
2. Measure sqrt(-G) in 8 places: imaginary for (24,2).
3. Gravity normalisation: bare R (A, C, F, H), M^24 R (E), (M^24/2) R (B), 1/(2 kappa^2) (D). Factor 2 and missing dimensional coefficient. A and C bare R is dimension 2 against a measure of -26.
4. Planck exponent: E latex M^25 vs its own html/plain M^24; I M^25; D "kappa^2 ~ M^-25" and "G_27" in a 26D bulk; EL1 "G_26 ... M^25 via G_27". Correct: kappa^2 = 8 pi G_26 = M^-24.
5. Metric (1.2) was -dt^2 + 24 space = (24,1), 25D, while titled 26D (24,2); derivation counted 24 + 2 sampler + 1 time = 27.
6. A's prose: "26D = 24 + 2 sampler + 1 time" = 27.
7. M_Pl^2 = M_*^9 Vol(V_7) is 11D, used for a 13D shadow on a 9D internal space.
8. kk-ansatz-26-13: internal "13D" metric g_mn has no time direction, so 26 = 13 + 13 cannot be (12,1)+(12,1) as a warped product with a Riemannian fibre. Not fixed (needs a ruling on how the second time sits).
9. kk-ansatz-7-4: S^3 on a "7D" space; contradicts 13 = 7 + 6. Fixed.
10. reduced-lagrangian-4d: +1/4 F^2 (wrong sign) next to +|D phi|^2. Fixed.
11. Sign conventions mixed: A and B use R with mostly-plus kinetic signs; F and G use -(M^2/2) R with (+) kinetic, i.e. mostly-minus; J mostly-minus. Not fixed: needs a stated convention for the Riemann sign and metric; notation only, but spread over 40 formulas.
12. Weyl spinor mass and quartic bilinears vanish identically (above).
13. YM coupling dimension, dilaton dimension (above).
14. Statuses: every action-definition formula was `DERIVED`, though the "derivation" is "construct by gauge principle". gauge_sector_complete formulas are also `DERIVED` with SU(3) and SU(2) OPEN (D-011): not changed (descriptions already say OPEN; category is a separate ruling).
15. core_formulas master-action-27d cites established_physics virasoro-anomaly / string-theory (the 26D critical-dimension argument, withdrawn for a two-time bulk). Id carries "27d". Not changed.
16. Three Kahler potential forms (tracked by test_kahler_potential_is_consistent).
17. lagrangian-13d-effective (core_formulas): M^10 R_12; lagrangian-hierarchy-complete: M^11 R_13; D-2 = 11 for 13D. The "M^10 R_12" is 12D. Not changed.

## 6. Fixes made (all prose/notation; no value changed)

- gauge/master_action.py: (1.1) sqrt|G|, coefficient (M_*^24/2) R, category DERIVED -> ANSATZ, dimension step corrected, terms for R, lambda, m, L_C marked OPEN with reasons; (1.2) metric now -dt_1^2 - dt_2^2 + 24 space, steps fixed; EL1 G_27 -> G_26, M^25 -> M^24; shadow, 4D formulas -> ANSATZ; M_Pl^2 relation restated; shadow derivation step uses sqrt|G|.
- derivations/lagrangian_master.py: sqrt|g_26| / sqrt|G_26| in 2.1.5-2.1.9, H1, docstrings; two-layer action coefficient and measure; kappa relations; five sector formulas -> ANSATZ; 4D F^2 sign; kk-ansatz-7-4 re-stated as 6D -> 4D with 2 residual; M_Pl relation; YM coupling and dilaton dimension notes.
- config/core_formulas.py: master-action-27d latex M^25 -> (M^24/2); html and plain_text to /2; M_* term says input.
- config/parameters/master_action.py: class doc corrected; BULK_PLANCK_POWER comment marked LEGACY (value 23 unchanged, unused).

## 7. Owner items (not changed)

1. Choose the single action: which sectors (E8xE8 YM? flux F_4? KK tower?) are in the bulk; drop or define L_C, V_bridge, V_face, V_tor, OR^i, rho_breath.
2. Weyl vs Dirac: the mass and quartic terms vanish for a 4096 Weyl spinor. Either an 8192 Dirac field, or remove m and lambda.
3. `value = 0.4082 (1/sqrt6)` attached to pneuma-master-action-v23; what is it? (Also alpha_leak ~ 0.57 "from 1/sqrt6".) Left as is.
4. BULK_PLANCK_POWER = 23 -> 24 if ever used.
5. Sign convention (mostly-plus vs minus, Riemann sign) for F, G, J.
6. How the second time enters kk-ansatz-26-13.
7. The M_* ~ 1e16 GeV and Lambda ~ 1e-52 m^-2 statements: derive or label input.
8. g_GUT <-> bulk g map; dilaton dimension.
9. Whether gauge_sector_complete SU(3)/SU(2) formulas should drop `DERIVED` while OPEN (D-011).
10. Items 15, 17 above.
11. The 26 = 13 + 13 split yields 2 x 64-component shadow spinors tensoring to 4096 (64 x 64): a tensor product doubles the dimension counts of a direct sum; the engine claims both. Needs a ruling.
