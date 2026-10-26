# Path consistency check (2026-10-26)

Tool: `docs/plan/paths/path_consistency.py RUNS [OUT.json]` (python -I, read-only).
Run on `H:/claude-scratch/runs_g`: `active` plus 37 finished single-deviation runs (those with DONE.json; 38 in all). Engine: worktree `metaphysica-pathcheck` at core-paper 838bebc. No value was changed anywhere.

## What is checked

| | Check | Tolerance / scope |
|---|---|---|
| a | Each formula's `arithma_compact` tree is re-evaluated (literals, `pi`, `b3` from `topology.elder_kads`) and compared with its `value` | rel 1e-9 |
| a | A formula's sole numeric output row compared with its `value` (degree rows also accept radians) | rel 1e-6 |
| a | `input_params` must exist as rows; `terms[*].param_id` must exist and the term value equal the row | rel 1e-3 |
| b | Every `<span data-pm-value=K>` and `<span data-category=C data-param=P>` in `Pages/*.html` that carries static text, compared with the run's row | printed precision; FULL scan of all pages, not a sample |
| c | Soft status (DERIVED/GEOMETRIC/PREDICTED) with a calibrated/fitted source; DERIVED-category formula whose output row is FITTED/CALIBRATED | text match |
| c | Certificates: files vs GATES_CERTIFICATES registry, check values vs the run's rows, pass/fail recount vs `evaluation_summary`, `result` prose numbers vs executed checks; assertion_verdicts tally vs its own list | exact / printed precision |
| d | Rows changed against `active` (via `interactions.changed`); an ESTABLISHED row must never change | exact |

Structure limits found while building it: of 582 formulas, 347 carry `value: null` and cannot be re-evaluated; the 235 with a value have inputs baked into the tree as literals (only `b3` and `pi` are named leaves), so "re-evaluate from the published rows" can only test the tree against its own value and the term/row links, not substitute rows into the tree. The tool says so per formula (`no_value`).

## Counts per run

All 38 runs have identical counts except as listed. Row = per run.

| Check | active | typical option run | exceptions |
|---|---|---|---|
| formulas | 582 | 582 | |
| tree vs published value (non-ruled) | 0 mismatches | 0 | |
| tree vs value, flagged RULED_DIVERGENCE | 12 | 12 | `flavour_seed_coupling--calibrated_24` 11; `b3_seed--seed_24` 0 |
| no value, not evaluable | 347 | 347 | `metric_construction--hitchin_cubic` 348 |
| value vs output row differs | 74 | 74 | seed_24 66; dark_energy_betti (b2_4, bridges_12, chi_over_b3_6, ngen_3, octonion_8) and mep_11_13 75 |
| term param_id row missing | 5 | 5 | |
| inputs missing | 0 | 0 | |
| page spans / with static text / unresolved key / non-numeric | 257 / 107 / 73 / 3 | same | |
| page static text != row | 6 | 6 | seed_24 4; dark_energy_betti* and mep_11_13 7 |
| soft status with fit source | 1 | 1 | |
| DERIVED formula, FITTED/CALIBRATED row | 7 | 7 | |
| certificate file/registry/row/recount mismatches | 0 | 0 | |
| certificate `result` prose numbers not in executed checks | 7 gates | 7 | |
| assertion_verdicts tally mismatches | 5 | 5 | |
| ESTABLISHED rows changed | 0 | 0 | |
| rows changed vs active | 0 | 0 for 24 options; 189 seed_24; 15 dark_energy_betti; 17 mep_11_13; 16 calibrated_24; 4 spectral_index (both); 1 h0_route (both) | |

Worst offenders: the five dark_energy_betti options and `dark_energy_mechanism--mep_11_13` (75 formula/row differences, 7 stale page fallbacks).

Clean results worth stating: no formula tree disagrees with its published value except the 12 already flagged RULED_DIVERGENCE; no input row is missing; every certificate file equals its registry entry; every registry check value equals that run's row; `evaluation_summary` equals the recount; no ESTABLISHED row moves on any path; certificates follow the path (h0_route changes `cosmology.H0_local` and G47's check value follows it).

## Failures, classified

### Code bug, fixed
1. **Certificate `result` prose contradicts the executed check, silently.** G12 declares "0.68 sigma"; its check computes 17.12 sigma. Same for G27, G36, G39, G47, G50, G56 (list in section 3 below). Declared text is a hand-written claim (`src/metaphysica/generators/generate_72_certificates.py:48,62,71,73,84,110,118`). Fix: `result_unmatched_numbers()` (generate_72_certificates.py:577) and an additive `result_unmatched_numbers` field on every verifiable-gate certificate. The declared text is kept (demote, never delete). Tests: `tests/test_certificate_result_text_matches_evaluation.py` (5 tests; all 5 fail before the change, 5 pass after; the neighbouring `test_scorecard_agrees_with_evaluation.py` and `test_declarative_strategy_c.py` still pass). Takes effect on the next full build; the published artifacts do not have the field yet.

### Label / prose bugs, not fixed (report)
2. Seven DERIVED/GEOMETRIC/PREDICTED formulas whose output row is FITTED/CALIBRATED: higgs-mass (row CALIBRATED), higgs-quartic-coupling, mass-ratio-geometric, pmns-theta-12/13/23, neutrino-mass-sum (rows FITTED). A formula's category is set where it is registered (`simulations/base/registry.py:1648`) with no knowledge of the row status; the label belongs to the author. Not changed: it needs a ruling on which side is right.
3. Certificate prose vs executed value (declared text, `generate_72_certificates.py` lines above): G12 0.68 sigma vs 17.12; G27 theta_12 33.59 vs row 34.29, theta_13 8.65 vs 8.36, theta_23 49.75 vs 50.99, delta_CP 278.4 vs 148.46; G36 "5.8e-5" is not the check quantity (row 1.0); G39 "theta_23~45" vs 50.99; G47 "71.55" vs 71.74; G50 6.19e-10 / 1.63 sigma vs row 6.85e-10 / 18.16 sigma; G56 "4.5 TeV" vs row 5.0. G19 says "Matches NuFIT" but its check fails (theta_13 4.84 vs 8.58, 34 sigma).
4. Static page fallbacks differ from the run's row (display-only; `js/pm-constants-loader.js` overwrites them at load): `Pages/beginners-guide.html:1560` free_variable_count 65 vs row 70; `Pages/faq.html:349,1029,1030` H0_local 71.55 vs 71.74 (row, active), and `faq.html:419` w0 -0.9583 vs -0.75 on the dark_energy_betti and mep_11_13 paths; `beginners-guide.html` topology.b2 12 vs the seed_24 row. Source for site edits: `metaphysica/src/metaphysica/website/Pages/`.
5. `website/AutoGenerated/assertion_verdicts.json:8-9` states 24 assertions and counts FITTED 5, UNFOUNDED 5, NUMEROLOGICAL 2, CIRCULAR_NUMEROLOGY 1; the list holds 20 (FITTED 4, UNFOUNDED 4, NUMEROLOGICAL 1, CIRCULAR_NUMEROLOGY 0). Static hand file (dated 2026-03-16).
6. `topology.mephorash_chi` is status GEOMETRIC while its source says "calibrated at the retired TCS seed; not re-derived on Y7" (active parameters.json).
7. Already documented, not a new bug: six certificates (G12, 19, 22, 27, 50 and the G72 seal) are VERIFIED declaratively and COMPUTED_FAIL; covered by `tests/test_scorecard_agrees_with_evaluation.py`.
8. 5 `terms[].param_id` that name no published row: null-constraints-2t -> particle.invariant_mass; 4d-fermion-lagrangian -> fermion.yukawa_matrix; lagrangian-hierarchy-complete -> gravity.alpha_F, beta_F, gamma_F.

### Value questions for the owner
9. 74 formulas publish a `value` that differs from their sole output row (44 DERIVED rows, 8 GEOMETRIC, 7 FOUNDATIONAL, 6 FITTED, 4 PREDICTIONS, others). Some are definitional (a formula for a count, a row holding a flag), some are real: higgs-mass formula 125.1 vs row 120.62; alpha-leak-coupling 0.4082 vs 0.5465; pmns angles; intro-division-algebra-decomposition 13 vs `geometry.D_shadow` 12. Which of the two is the published claim?
10. 12 RULED_DIVERGENCE formulas whose tree value differs from the published value (euler-characteristic 258 vs 144, three-generations 5.375 vs 3, alpha-inverse-geometric 449.6 vs 137.04, critical-dimension 45 vs 26, ...). `simulations/core/ruled_divergences.py:104`. Category is still DERIVED/GEOMETRIC/PREDICTED on these; should it be demoted?
11. Inert options: 24 of 37 options change no row against `active` (all b3_origin, bulk_signature, chi_eff_route, face_genericity, g2_form_convention, joyce_contribution_table, lattice_24d, metric_construction, moduli_indexing, n_gen_source, re_t_adoption, render_policy, seed_selection, theory_uncertainty_policy, twisted_norm_convention options). Either they coincide with the adopted value on the adopted seed, or the fork is not wired to any row. `interactions.py` reports the same.
12. G59 check uses `vacuum.bounce_action` = 1e10 and G56 `geometry.m_KK_central` = 5.0 with no expected anchor: the pass is not against data.
13. 347 of 582 formulas have no published value, and the 235 that do are baked literals, so a real row-substitution check is impossible until formulas carry named input leaves.

## Not done
Cross-path was limited to the changed-row set and ESTABLISHED rows; no declared per-option "touches" list exists to define untouched rows exactly. The DERIVED-source-versus-fit test used only the `source` string.
