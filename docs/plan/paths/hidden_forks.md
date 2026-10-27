# Hidden forks: choices the code makes that the catalogue does not declare (H1, 2026-10-28)

Brief: `briefs/H1-hidden-forks.md`. Source read: `metaphysica/src/metaphysica` (core-paper), static
grep only, no builds. "Rows reached" is judged from imports and callers; it is not a traced count
unless a number is given. Classes: F fork, S shadow (recomputed, not read), D dead (declared or
chosen, never read).

Evidence base: the f2b build's `fork_reads.json` shows reads only for 14 of the 25 catalogue forks
(b3_seed 5395, g2_form_convention 17077, chi_eff_route 1987, others far lower).

## Table

| id | file:line | class | alternatives (adopted first) | rows reached | existing fork it should read |
|---|---|---|---|---|---|
| H01 | `core/dependency_resolver.py:898-909` `build_seed_values()` (`seeds.elder_kads: 24`, also `mephorash_chi` 72, `logos_joint` 153, `visible_gates` 135, `bulk_pressure` 163, `logic_closure` 288) | S, contradicts fork | b3 = 43 (live) vs literal 24; feeds `base/registry.py:1060` auto-resolve | every graph node under `seeds.elder_kads` (about 10 nodes at lines 588-786: 2pi/b3, b3^1.5, 3/(8+b3), -1+1/b3, ...) | `b3_seed` |
| H02 | `core/dependency_resolver.py:700-701` `H0_base = 24*3 - 0.45` | S, contradicts fork | live-seed H0 via `h0_route` vs hardcoded 71.55 | H0 node and descendants | `b3_seed`, `h0_route` |
| H03 | `PM/paper/appendices/appendix_f_72gates.py:990, 1300` `validate_gate` `torsion == 24` (`TORSION_PINS` is read from `elder_kads` at line 120, then compared with 24) | S, contradicts fork | gates 6 and ~13x test the live value against a literal; fails or passes by seed, not by physics | gates 6 and 2 others; `GATES_72*.json`, gate pass counts | `b3_seed` |
| H04 | `PM/paper/appendices/appendix_f_72gates.py:1077` `24/288` | S | literal ratio vs registry (`elder_kads`/`nitzotzin_roots`) | gate 22 | `b3_seed` |
| H05 | `core/FormulasRegistry.py:653` static table `"elder_kads": {"value": 24, ...}` and the `:631` comment table | S | the property `elder_kads` (`:3655`) returns `_b3` (live, from `b3_path.seed_values`), the table says 24; two sources in one file | any consumer of the dict (value table, LaTeX symbol table) | `b3_seed` |
| H06 | `core/FormulasRegistry.py:1135` fallback `self._b3 = 43` on ImportError | F (benign) | import-cycle fallback; correct today because it matches the adopted branch, but is a second literal that must track `b3_path.PATHS` | all registry rows | `b3_seed` (documented, keep) |
| H07 | `core/FormulasRegistry.py:1157-1158` `_chi_eff = 72`, `_chi_eff_total = 144` set unconditionally | F | chi_eff constant (adopted) vs seed-dependent (6*b3 or b3^2/4; see `PM/geometry/chi_eff_routes.py`, `chi_eff_branches.py`) | `topology.mephorash_chi`, n_gen = chi/48, alpha_leak, everything downstream (1987 reads of `chi_eff_route` in f2b, none changing the value) | `chi_eff_route` (currently UNRULED but its reads cannot change the registry value) |
| H08 | `chi_eff = 144` literal, 13 sites (`rg "chi_eff\s*=\s*144"`); incl. `asymptotic_safety.py:506`, `bridge_geometry.py:512`, `four_face_structure.py:2415`, `dynamical_lambda.py:191` | S | literal vs registry chi_eff | per site: lambda_6, alpha_leak, bridge outputs | `chi_eff_route` |
| H09 | `alpha_leak = 1/sqrt(6)` literal, 7 sites (`four_face_structure.py` x5 and others) | S | 1/sqrt(chi_eff/b3) at the live seed vs fixed 6 (= 144/24) | portal, mixing and face-structure rows | `b3_seed`, `chi_eff_route` |
| H10 | `b3 = 24` literal in `PM/geometry/four_face_structure.py:853,1708,2412,2604,2695` (k_gimel = b3/2 + 1/pi, T1..T4) | S, contradicts fork | live seed vs 24 | face-structure outputs, k_gimel-derived rows (v = k_gimel*(b3-4)) | `b3_seed` |
| H11 | `b3 = 24` literal in `PM/algebra/e7_representation.py:331,428`, `e8x8_splitting.py:305,378,397`, `freudenthal_triple.py:287,344,371` (condensate scale b3/27, exp(-2pi/b3)) | S, contradicts fork | live seed vs 24 | section content, certificates, `validate_self` of the three algebra modules | `b3_seed` |
| H12 | `PM/cosmology/dynamical_lambda.py:190-191` class constants `B3 = 24`, `CHI_EFF = 144`, `N_BRIDGES = 12` | S, contradicts fork | live seed vs class constants | dynamical-lambda relaxation, Lambda rows | `b3_seed`, `dark_energy_betti`, `dark_energy_mechanism` |
| H13 | `PM/gauge/asymptotic_safety.py:505-506` `b3 = 24; chi_eff = 144` | S | as above | lambda_6, enhancement | `b3_seed` |
| H14 | `PM/geometry/bridge_geometry.py:512-513` `chi_eff = 144; b3 = 24` ("topological value") | S | as above | `d_t_w`, alpha_leak_derived | `b3_seed`, `chi_eff_route` |
| H15 | `PM/validation/geometric_pipeline.py:198` `b3 = 24  # From Leech lattice dimension` | S, mislabel | b3 as the Leech dimension vs b3 as the Betti number: a second meaning for 24 (`lattice_24d` fork exists) | pipeline observables | `lattice_24d` for the Leech reading; `b3_seed` for the Betti reading |
| H16 | `PM/support/complete_residue_registry.py:487` `b3 = 24` (M_GUT_G2 = M_Pl/sqrt(b3)) | S | live seed vs 24 | M_GUT_G2 and proton-decay residue rows | `b3_seed` |
| H17 | `PM/validation/consistency_beacons.py:442` `b3 = 24; d_bulk = b3 + 2` | S | live seed vs 24; D_bulk = 26 is the declared 26D bulk, the beacon pins it | one beacon | `b3_seed`, `bulk_signature` |
| H18 | `base/precision.py:105` `B3: int = 24` (demon-lock precision constants) | S | live seed vs 24 | precision-lock constants (k_gimel, phi) | `b3_seed` |
| H19 | `core/canonical_values.py:40` `B3 = 24`, `CHI_EFF = 6*B3`, `CHI_SECTOR` | S/F | canonical table is built from the retired seed; consumed by `candidate_closure_gate.py:103`, `de_plane_gate.py:88`, `variants/adopted.py:205`, `generate_canonical_values.py` (6 import sites) | candidate-closure and DE-plane gates; canonical prose audit | `b3_seed`, `chi_eff_route` |
| H20 | `validation/eta_s_derivation_test.py:69` `B3 = 24` (registry-unavailable fallback) | S (fallback) | fallback differs from the live seed | one test script | `b3_seed` |
| H21 | `PM/paper/appendices/appendix_c_derivations.py:1037` `b3 = 24; n_gen = b3 // 8` | F, labelled | the retired generation count b3/8 pinned in a validator (comment says so); contradicts `n_gen_source` (adopted b2/4) | one validator check | `n_gen_source` (annotated pin; confirm it is intended) |
| H22 | `PM/paper/appendices/appendix_q_index_theorem.py:1393` `b3 = 24`, `passed: b3 == 24` | F, labelled | typed seed check that cannot follow the path | one validator check | `b3_seed` (annotated pin) |
| H23 | `PM/validation/CERTIFICATES.py:753` `b3 = 24` (cert_cosmo_015_h0, "CALIBRATED at the off-path seed") | F, labelled | H0 certificate computed at 24 | H0 certificate, reaches `h0_route` readers | `b3_seed`, `h0_route` (annotated pin) |
| H24 | `PM/field_dynamics/thermal_time.py:1100` `b3 = 24` (alpha_T check, "evaluated at the off-path seed") | F, labelled | pinned check | one validator check | `b3_seed` (annotated pin) |
| H25 | `PM/field_dynamics/pneuma_mechanism.py:262` `b3 = 24` fallback after `registry.get_param("topology.elder_kads")` | F (benign) | fallback only when registry lacks the row | pneuma outputs if the registry is absent | `b3_seed` (documented fallback) |
| H26 | `PM/algebra/gaugino_condensation.py:255, 675` `n_gen = 3`; N1 = b3 = 24, N2 = 23 | S | n_gen literal vs `n_gen_source`; N1 literal | Wolfenstein lambda_W = eps^(1/n_gen), gaugino rows | `n_gen_source`, `b3_seed` |
| H27 | `PM/algebra/neutrino_algebraic.py:134-441` (n_gen = 3, b3/n_gen = 8, chi_eff = 144 written as inputs) | S, labelled | text and checks pinned to the off-path seed | neutrino algebraic outputs | `b3_seed`, `n_gen_source`, `chi_eff_route` |
| H28 | `PM/geometry/closed_geometry/selection.py:43` `SELECTION_ROUTE = "wa1_correspondence"` | F (declared) | matches the catalogue source (`seed_selection`); import-cycle fallback only | none beyond `seed_selection` | OK, already the fork source |
| H29 | `PM/cosmology/spectral_routes.py:22`, `late_time_routes.py:25-26`, `geometry/chi_eff_*` : `ADOPTED_*` constants | F (declared) | catalogue `source=` points at these; reads go through `resolve()`; checked `inflation.py:447`, `geometric_anchors_core.py:1139`, `FormulasRegistry.py:4253` | n_s, H0, DE rows | OK |
| H30 | `PM/cosmology/inflation.py:447-450` slow-roll n_s vs canonical n_s | S | two live n_s (0.9996 vs 0.9636), already `KNOWN_CONFLICTS` in `scripts/audit_shadow_derivations.py` | n_s rows | `spectral_index_route` (the route is read, but the inflation module's own value is still published as a separate row) |
| H31 | `scripts/audit_shadow_derivations.py` KNOWN_CONFLICTS: `theta_13` (9.594 vs 8.669), `n_s`, `neutrino.mass_sum` (0.060/0.082/0.101 eV) | S | two or three derivations per observable | theta_13, n_s, three mass-sum rows | `flavour_seed_coupling` for theta_13; none for mass_sum (a missing fork) |
| H32 | `simulations/base/units.py:358`, `derivations/matter_sector_complete.py:111`, `appendix_r_vacuum_stability.py:124` `m_higgs = 125.1` | S | PDG literal in three modules vs `pdg.m_higgs` row (`registry.get("pdg.m_higgs", default=...)` at appendix_r:207 reads it, the others do not) | Higgs-dependent vacuum-stability and matter rows | none (measured input, so read the one row) |
| H33 | catalogue fork `moduli_indexing` (g2_forms.py:243) | D | no `resolve("moduli_indexing")` and no mention outside the catalogue | none | n/a, nothing consumes it |
| H34 | catalogue fork `bulk_signature` (g2_forms.py:320) | D | no `resolve()`; only `config/parameters/bridge.py:268,337` carry an unrelated `'bulk_signature'` key; 26D (24,2) is hardcoded in `canonical_values.py` and H17 | bulk-dimension rows | n/a, wire it or retire it |
| H35 | catalogue fork `face_genericity` (policy.py:97) | D | only a docstring in `gauge/topological_terms.py:445`; the narrowing 35 -> 7 is hardcoded | face-count rows | n/a |
| H36 | catalogue fork `g2_construction` (g2_forms.py:179) | D (one read) | 1 read in the f2b build; code mentions it only in comments about the REFUSED TCS #187 seed (`gauge_sector_complete.py:92`, `electroweak_mixing.py:232`, which still compute on the retired TCS seed) | gauge-sector rows built on the retired seed | `g2_construction` |
| H37 | catalogue forks read once or never in f2b: `render_policy` (1), `theory_uncertainty_policy` (1), `joyce_contribution_table`, `metric_construction`, `twisted_norm_convention`, `n_gen_source`, `b3_origin` (zero reads in f2b although each has a `resolve()` caller; callers are `switch_search.py` and `b3_path.py:250`, so they are read only on a search or report path) | D-ish | the engine cannot sweep forks the build never reads | none | confirm each has a build-path reader |

Counts: F 8 (H06, H07, H21-H25, H28/H29 counted as OK), S 25, D 4 plus the H37 group.
Distinct hardcoded `b3 = 24` assignments in non-test code: 24 across 18 files (grep of
`^\s*(b3|B3) = 24`), plus the 7 `alpha_leak = 1/sqrt(6)` and 13 `chi_eff = 144` literals.

## Ranked: the 10 worth doing first

1. **H01** `build_seed_values` hardcodes 24 under the dependency graph. Reaches every `seeds.elder_kads` node and everything the auto-resolver computes. Contradicts `b3_seed`. One-line fix: read `FormulasRegistry.elder_kads`.
2. **H03** `validate_gate` torsion == 24 (and `24/288`). Gates pass or fail on the seed rather than the physics; this is the owner-decision-7 case. Contradicts `b3_seed`.
3. **H19** `canonical_values.B3 = 24`. Feeds the closure gate, DE-plane gate and canonical prose audit, so these judge the live seed against the retired one.
4. **H07** `FormulasRegistry` `_chi_eff = 72` / `144` unconditional. Every `chi_eff_route` read (1987) is inert because the registry value does not follow the route. Biggest single reach.
5. **H05** The `FormulasRegistry` table `"elder_kads": 24` against the property returning `_b3`. One file, two sources.
6. **H10** `four_face_structure.py` five `b3 = 24` sites (k_gimel, T1..T4). Largest cluster in one module; reaches the EW vev derivation.
7. **H11** The nine algebra-module `b3 = 24` sites (e7, e8x8, freudenthal): condensate scale and hidden-condensate rows.
8. **H02** `H0_base = 24*3 - 0.45`. Contradicts both `b3_seed` and `h0_route`.
9. **H12 and H08** `dynamical_lambda` class constants and the 13 `chi_eff = 144` literals: Lambda and bridge rows.
10. **H34/H35/H33** Dead catalogue forks (`bulk_signature`, `face_genericity`, `moduli_indexing`). A sweep over them changes nothing; wire or retire them.

Next tier: H09 (alpha_leak literal), H26/H27 (n_gen = 3 literals, contradict `n_gen_source`), H31
(mass_sum has three derivations and no fork), H36 (gauge sector still computed on the REFUSED seed).

## Candidates that contradict a catalogue fork today
- H01, H02, H03, H05, H10, H11, H12, H16, H18, H19 against `b3_seed` (value does not follow the chosen seed).
- H07 against `chi_eff_route` (route is read but cannot move the registry value).
- H21, H26 against `n_gen_source`.
- H36 against `g2_construction` (REFUSED option still drives gauge rows).
- Labelled pins (H22-H25, H27) say "off-path seed" in their own comments; they are intentional but invisible to the engine.

## Not done
- Rows reached are not traced; a runtime read-trace (as `fork_reads.json` does for forks) for the literal sites would give counts.
- Did not search `config/` or `website/` for the same literals.
