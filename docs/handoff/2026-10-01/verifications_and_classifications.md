# Verifications and classifications, 2026-10-01

Agent reports condensed by the lead. Data files are in `data/`.

## 1. G1b blind re-derivation (D-008) — recorded in the decision log

Data: `data/g1b_blind_verdict.md` (the verifier's own report and script list).

- Coverage: all 2¹⁴ = 16,384 shift classes × 28 generating triples (458,752
  assignments); engine and independent model agree class by class (0 mismatches).
  n = 0/1/2/3 classes: 6,296 / 6,783 / 2,520 / 364; none with n ≥ 4.
- H1 CONFIRMED (spanning ⇔ non-concurrent; one complement line = fixed line of
  σ₁σ₂σ₃; canonical point lines (0,1,2), (0,3,4), (1,3,5); arc {0,1,3,6}).
- H2 CONFIRMED (84/84 abstract, 1,092/1,092 concrete matchings hold one triangle side).
- H3: existence CONFIRMED on all 280 all-plain classes; **canonicity REFUTED** —
  all 24 bijections per block are torsor maps; 112/280 classes have no
  symmetry-invariant choice; none unique. Engine wording corrected.
- H4 CONFIRMED with caveat: the 84 Example-4 classes are (4,4,8) and admit no
  bijection, but all 84 also reach (12,43) under the per-family lift model — the
  pair does not identify the all-plain members; the profile (4,4,4) does.
- No kill condition fired.

## 2. G5 second blind verification (D-012) — recorded as D-012 VERIFICATION + D-018

Data: `data/g5_second_verification_verdicts.json` (48 verdicts with quotes).

- 23/41 = 56.1% exact agreement with the amended table → kill fired; no global
  re-wiring. FR04 was the amended table's error (rule 8 gives it the family's B3).
- D-018 pre-registered consensus-only actions on 28 roots (16 labels; SP05 24-cell
  flavour flip; SP11 w₀ → −42/43; OT13 pneuma bridge pairs; SP13 appendix H SO(n);
  OT18 13D shadow). **Not yet executed.**
- The verifier's judgement calls (rules don't settle): SP11 (B3 vs INFRA), SP14/FR40
  (class carried through consumed inputs?), NC02/NC06 (a-exponent Leech vs b₃;
  "closure" undefined), OT14 (24 in χ_eff/24), "torsion pins" (SP13/SP14), NC10.

## 3. D-013 active-path classification — formulas

Data: `data/active_path_formulas.json` (155 non-LIVE entries with class, fork,
option, decision, reason, quoted evidence, source module; every id not in the file
is LIVE). Rulings of D-015 applied.

| class | count | displayed? |
|---|---|---|
| LIVE | 425 | yes |
| CALIBRATED | 76 | yes, labelled |
| DOUBTFUL | 19 | yes, listed for the author |
| OFF_PATH | 20 | no → off-path register |
| RETIRED | 40 | no → off-path register |

OFF_PATH by option: fano_tcs 6 (euler-characteristic, cycle-matching, kk-threshold,
cycle-separation-suppression, proton-lifetime, b3-from-euler-v19);
b3_over_dim_O 6 (octonionic-partition, generation-theorem,
spinor-saturation-generations, b3-generations, fermion-generations-v19,
topological-constraint-v19); dark_energy_betti=b3_live 4 (these swap with the 6
CALIBRATED −23/24 formulas if D-018's SP11 flip is executed); seed_24 2
(modular-anomaly-condition, partition-function-eta); chi_eff seed_dependent 2
(pressure-divisor-formula, euler-index-relation-v19).

RETIRED by decision: signature ruling 2026-08-31 (8); two-time migration (4);
D-005/D-015 racetrack and moduli vacuum (12); D-015+D-011 chirality index (2); R1
θ₁₃ (1); register §1.3 wₐ (3); CANON w₀ (1); CANON H0 "tension resolved" (6);
withdrawn fit headlines (2); betti-number-relation-v19 (1).

DOUBTFUL (author's call): dirac-zero-modes, doublet-triplet-splitting,
face-warping-potential, pneuma-lagrangian, bridge-12-pair-metric-v22,
v22-bulk-structure, dimensional-reduction-cascade, lagrangian-hierarchy-complete,
pneuma-master-action-v23, bulk-action-26d-v23, central-sampler-formula, kk-g2-volume,
einstein-hilbert-14D, calabi-yau-projection, spectral-euler-residue-v19,
portal-sterile-mass-v23, relaxation-factor, discussion-global-alignment,
chi-squared-convergence.

Caveats: `topology.mephorash_chi` = 144 is sourced by the OFF_PATH
euler-characteristic formula — re-point to k3-reading-generations before hiding;
proton-decay-lifetime-v18 is the on-path replacement for proton-lifetime.

## 4. D-013 active-path classification — parameters

Data: `data/active_path_parameters.json` (304 non-LIVE entries + `_summary` with 12
judgement notes + `_status`).

| class | count |
|---|---|
| LIVE | 523 (14 flagged) |
| CALIBRATED | 107 (74 not yet carrying a CALIBRATED/FITTED status) |
| RETIRED | 114 |
| OFF_PATH | 20 |
| DOUBTFUL | 49 |

OFF_PATH: fano_tcs 9 (geometry.h11/h21/h31, geometry.k_matching,
topology.K_MATCHING, topology.d_over_R, topology.T_OMEGA,
proton_decay.suppression_factor, ckm.delta_cp); b3_over_dim_O 6
(geometry.n_generations and its alias **topology.n_gen = 24//8**,
chirality.generation_count, chirality.saturation_ratio, g2_holonomy.n_gen,
index.family_index); niemeier 2; seed_24 1 (geometry.elder_kads); seed_dependent 1
(fermion.n_flux); theory_uncertainty=always 1.

RETIRED: Re(T)/racetrack/gaugino chain (58), signature ruling (8), two-time (1),
chirality index (8), validation summaries contradicting the real report (17, incl.
validation.chi2_total = 0.2304), CANON/register rulings (22).

**Re-wire before hiding:** consumers of `topology.n_gen` (an off-path 24//8 value!),
of `geometry.h11` (`geometry.n_faces` reads it), and the χ_eff copies still coded as
6×ANCHOR. Reconcile the racetrack label (RETIRED vs "calibrated at the off-path
seed") — one label must win.
