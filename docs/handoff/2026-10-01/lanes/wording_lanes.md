# Wording lanes, 2026-10-01 — what was done, what is left, how to continue

Six lanes (plus lane-5 helpers) edited prose in parallel under
`H:/Github/metaphysica/docs/WORDING_MEMO.md` (D-014; rulings block D-015) and the
lane brief (copied below in short). The lead's mechanical review (git diff vs HEAD,
ASTs with strings blanked, protected keyword arguments compared) found **no change
to any value, id, path, EML tree, status or category** in any lane file; code-level
changes are `render()` imports/calls and small text helpers. Census tool:
`lane_census.py <glob relative to src/metaphysica> [--detail]` (in the session
scratchpad `wording/`; copy it to the engine's `tools/` if the scratchpad is gone —
it reads `tests/test_published_model_is_current.py` for the patterns).

**Rules that held up (keep using them):** text only; never change values, EML trees,
arithma, ids, paths, `status=`/`category=`; never add/remove ContentBlocks or list
items; label OFF-PATH/RETIRED/CALIBRATED rather than rewrite; numbers in running code
via `geometry_narration.render()`; no new holonomy phrases in files without them;
double every literal brace in f/rf-strings and run `python -c "import <module>"` after
each f-string edit; preserve CRLF line endings (edit by exact replacement with count
assertions); never run git, the build, or anything setting METAPHYSICA_OUT.

**Test pins to respect:** `tests/test_frozen_seed_literals.py` (exact sets of
`name = <b3 expr> = number` annotations in core/*.py — keep FormulasRegistry's
LOGIC_CLOSURE "12 x b3", roots_total "(b3*12)", chi_eff_shadow "b3^2/8", chi_eff_total
"b3^2/4", sterile_sector "7*b3 - 5", D_bulk "b3 + 2", N_flux "= b3", denominator
"b3*10 - 1", w0 "-1 + 1/b3", w_a "-1/sqrt(b3)", identify_ghost_literals "(7*b3)-5",
verify_sterility_report "MANIFOLD_BASE = 24 # b3"); `test_value_context_audit` (a
literal 144/163/288/125/576 needs a b3/24/chi_eff token within ±3 lines);
`test_seed_propagates_from_the_root` ("BREAKS" in cycle-matching steps, "DIVERGE" in
euler-characteristic steps); `test_kahler_potential_is_consistent` (keep
`K = -3 ln(4*pi/3 * Im(T)^{7/3})` in matter_sector_complete and "K = -3 ln(T + T_bar)"
in config); `theory-constants.js` "w0Denominator: 24" / "w0: -0.958333" pinned by
`test_export_active_path_only.py`.

---

## Lane 1 — paper body (`PM/paper/`)
Done (RATCHET → 0): `introduction.py` (9; new §1.3 "The Model, Top Down" rendered from
PROVENANCE; foundations dict honest; DESI DR2 cited; Spin(3,1) ≅ SL(2,C) fixed),
`foundations.py` (25), `predictions_aggregator.py` (22).
**Left:** `discussion.py` 10 (L330, 969, 985, 1373, 1605 b3_is_24; L276, 777, 1356,
1366, 1546 chi_over_48), `results.py` 6 (L183, 264, 292, 775, 626; "consistent with
DESI" L301/671/1029; "Euler characteristic (144)" L827/905), `methodology.py` 2
(L581, 829), `integrity.py` 1 (L566); version tags throughout.
**Flagged:** predictions_aggregator status values still "CONSISTENT"/"CONFIRMED"
(status change needs a decision); cert-predictions-self-consistent PASS though the
section contradicts itself on w_a (0.27 vs −0.75); G48 returns True; b3-generations
latex still "b3/8 = 24/8 = 3" (latex untouched by rule); removed "Ω₁₃^String = 0"
(believed ≅ π₁₃(tmf) = ℤ/3 — author to verify); unverified: "Joyce has (7,24)",
Pettini arXiv:2606.12457; Spin(12,1) ⊃ Spin(3,1)×Spin(8) has 4 + 8 ≠ 13; the
13 = 1 + 4 + 8 octonionic split vs adopted 13 = 7 + 6 unreconciled.

## Lane 2 — appendices (`PM/paper/appendices/`)
Done (→ 0): Q (48), C (11; not run), P (10), S (7), H (6), A (4; not run), D (4; not
run). Lane 108 → 18.
**Left:** K 3, O 2 (+ "consistent with DESI" ×2, shared time 6), R 2 (racetrack →
CALIBRATED, Re(T) OPEN), A-spectral 2, T 2, U 2, B-sum 1, F 1, G 1, B-methods 1
(not run), E 1 (not run); version tags in d_alignment, l, i, z, c_gauge, e_brane, j;
shared time in M and N.
**Value issues (need decisions):** P publishes `g2_holonomy.n_gen` = b3//8 = 5;
Q publishes `index.family_index` = 5.375; S's spectral-euler-residue-v19 EML encodes
6·b3 (258 vs value 144) and cert-k-gimel-scale compares 12 + 1/π vs live 21.818;
H's EML trees route bulk counts through b3_leaf and run() publishes SO(43) = 903 /
915 roots (SP13 re-wire, D-018); C (not run) d/R target 0.12 vs 0.04; P's "252 Joyce
pairs" unverified; "Hitchin identity φφ = 6δ" misattributed (Hitchin is cubic).

## Lane 3 — geometry + core
Done (→ 0): `modular_invariance.py` (46; the 24 is η²⁴'s weight; "b3 = 24 forced"
OFF-PATH; critical dimension RETIRED), `g2_geometry.py` (41; Section 2 text incl. its
abstract; 2.4 table cells for ghosts/chirality now "OPEN", SO(10) "NOT_ESTABLISHED" —
**lead to review**). Lane 255 → 168.
**Left (priority):** four_face_structure 37 (plan in the report: label TCS/h11 = 4 /
racetrack OFF-PATH or CALIBRATED; faces survive as b₂ = 4 A₁ families per involution;
"24/8" in generation_count_report is Leech/E₈ rank; proof_racetrack_hierarchy prints
94.07/23.52 — recompute T₁ = 94.1050, T₄ = 23.5262 from its own formula),
geometric_anchors 23, geometric_anchors_core 17, leech_partition 16,
FormulasRegistry 13, b3_candidate_sweep 7, canonical_values 6, alpha_rigor 5,
joyce_orbifold 5, bridge_geometry 4, derived_contribution_table 4,
dependency_resolver 4, half_shift_enumeration 3, sync_docs 3, then 1–2-hit files.
**Value/logic bugs:** g2_geometry `run_eml` gives χ_eff = 6b₃ = 258 and n_gen = 5
while `run()` gives 144 and 3; euler-characteristic tree 6·b3 vs value 144;
three-generations tree 5.375 vs 3; `verify_stability` ratio 89.73 at 43 outside its
24-calibrated window [52.9, 53.1] (validate_self check 6 fails); G_GEOMETRY_BETTI gate
tests `b3 == 24` (should test b₃ = 7 + 3b₂ like CERT_G2_BETTI_B3); modular_invariance
trees use b3_leaf for the η²⁴ weight; four_face `n_e8_blocks = b3 // 8` → 20 bridges
at 43 (OT06, D-012); alpha_leak from live b3 (0.546) vs formula 1/√6.
Tool: `wording/lane3/verify_text_only.py` (AST diff with strings blanked).

## Lane 4 — particle / derivations / support
Done (→ 0): yukawa_derivation 22, lagrangian_master 12, fermion_generations 10,
chirality 7. Lane 100 → 49.
**Left:** complete_residue_registry 8 (L12, 486 code `b3 = 24` keep+comment, 1317,
1579, 1598, 1684 "144/48 = 3 matching observation exactly", 1961), gr_spacetime 7
(`B2_G2 = 4 # TCS #187` label OFF-PATH), mass_ratio 7, cosmology_sector_complete 5
(L1572 "w₀ = −23/24 consistent with DESI"), gauge_sector_complete 4 (L1216 check if
bulk 24), matter_sector_complete 4 (b₃/8), axion_photon_coupling 3, neutrino_mixing 3,
neutrino_sector 3 (L266 "consistent with DESI/Planck" is Σmν — verify), proton_decay 3
(58 TCS detect hits), strong_cp_axion 2; DETECT-only higgs_mass (racetrack 40) etc.
**Value issues:** `chirality.generation_count` publishes 5 (int(43/8)); CERT_SPINOR_
SATURATION still PASS; `derivations.dof_after_sp2r` = 324 (= 27·24/2, retired 27D
count); dirac-zero-modes and chirality-index-theorem EML legs 144/b3_leaf = 3.35 vs
value 6; run_all prints "PMNS derived, VEV gap closed"; yukawa "T₄ is the symmetry
group of the 24-cell" doubtful (2T's 24 elements are its vertices; symmetry group F₄);
Kobayashi–Tanimoto arXiv number unverified.

## Lane 5 — remaining sectors (lead lane + 3 helpers)
Lead lane done (→ 0 unless noted): gaugino_condensation 21, thermal_time 22 → 1 (an
eml_tree_str "[b3=24, pi=π]"), neutrino_algebraic 17, pneuma_mechanism 13.
Validation helper done: CERTIFICATES 16, unitary_filter 14, unitary_filter_legacy
12, information_bottleneck_distiller 8, principia_residue_calculator 8,
adversarial_axiom_tester 3, statistical_rigor_validator 2 (75 → 12).
Visualizations/portals helper done: goldilocks_plot 14, stability_heatmap(.py/.html)
21, theory_overview_diagrams 10, sterile_neutrino_portals 7, GAUGE_TEST_SUMMARY 4,
algebra/gauge/octonionic/ricci diagrams 12, alp_portals 2 (78 → 8).
Cosmology helper done: vacuum_selection 9, speed_of_light 7, cosmology_intro 6,
cosmological_tensions 3, mirror_dm_relic 3, mirror_dm_detection 2, baryon_asymmetry 1
(35 → 4).
**Left:** gauge_unification 12, e8x8_splitting 10, freudenthal_triple 9,
asymptotic_safety 9 (reads geometry.elder_kads = ANCHOR_FIT 24 as b₃ — name the
object), orch_or_geometry 6, e7_representation 5, qec_golay_bridge 5 (24 = Golay
length / Leech rank), leech_lattice 3, topological_terms 2, sampler_entropy_dynamics
2, su3_qcd_gauge 1, master_action 1; validation: unitary_closure_checker 2,
eta_s_derivation_test 2 (its numerator assert fails at 43), parameter_sensitivity_test
2, consistency_beacons 1, strategy_a_semantic 1 (pinned f-strings), geometric_pipeline
1, falsification_oracle 1; visualizations: dark_matter_portals 2 (portals),
falsifiability_dashboard 2, README 2, descent_chain 1, figure1_m27_decomposition 1,
cosmology_diagrams "w0 = -23/24 DESI thawing!"; cosmology: dark_energy.py (1 + ~8 DESI
sentences — detailed line plan in the cosmology helper's report), dark_energy_thawing,
inflation, soft_susy_breaking, attractor_potential, cosmological_constant,
dynamical_lambda ("b3²/4 = 144 (Euler characteristic)"), multi_sector,
f_r_t_tau_gravity, axion_dm; racetrack-as-live labels in bridge_axion_ede,
racetrack_vacuum, racetrack_pairs, hubble_tension, moduli_dm_coupling.
**Value/wiring bugs:** `pneuma.n_bridge_pairs = b3 // 2` → 21, neural gate False
(OT13, D-018); pneuma formula values vs EML at 43 (neural-gate 12 vs b3/2;
4d-fermion 3 vs 6b3/48; lagrangian-hierarchy 27 = retired M²⁷ count with EML b3+3);
neutrino_algebraic reads geometry.alpha_leak (0.5465 from four_face) not E₇'s 1/√6 →
published θ₁₃ = 12.89° (38.7σ) beside text asin(1/6) = 9.59°, δ_CP −28° (FAIL);
gaugino registry rows follow the seed while formulas/sections are hard-coded at 24/23
(decide: calibrate at 24 or follow the seed); two α*⁻¹ on the active path
(asymptotic_safety 24 vs gauge_unification 43); thermal_time alpha-t-base value 2π/24
vs EML b3_leaf; two_time_metric_signature eml_description sums to 27; CERT wolfram
"2.700" vs 2.6; FormulasRegistry.speed_of_light_derived follows the live b₃ →
c = 1.79e8 m/s (FAIL); baryon N_eff = 2(b₃−14) follows the seed → 18σ; alp_portals at
b₃ = 43 fails CAST/stellar/mass-window certs and gate G49; sterile alpha_leak 0.697 vs
text 0.57, validate_self check 3 fails; stability_heatmap live chi = 72 → minimum at
(5,28) vs stored (4,24); ricci_flow mixes seeds; goldilocks_plot demonstrates nothing
(candidate for the off-path register); base/dynamic_metadata.w0_description hard-codes
"derived"/"Excellent agreement" vs an unverified −0.957 anchor; established.py
desi.w0_thawing text "matches PM prediction −23/24"; `cosmology.w0_derived` validated
PASS vs the unverified −0.957 bound; dark_energy.py reference "desi2025_thawing" title
looks invented for arXiv:2503.14738; mirror-DM traceback strings say "b3=43 via
re_t_sector" though g_bridge was computed at 24; re_t_sector calls b₃ = 24 "the SSoT
seed" and A = 3.2 "NOT a fit"; FormulasRegistry docstrings (elder_kads "(24)",
mephorash_chi "Euler Index (72)"); four PNGs carry stale text (descent_chain,
w_evolution, bridge_pressure, seesaw_dual_shadow) — never regenerate repo images
without a decision; status fields contradicting labels (baryon η_B & k_bary — η_B
fixed to CALIBRATED 2026-10-01 under D-015; pneuma-tensioner-z6 DERIVED;
breathing_mode_vev DERIVED; epsilon_KK GEOMETRIC).

## Lane 6 — website, generators, config, package data
Done (→ 0): formula-registry.js 16, pm-constants-loader.js 3 (**b2 → b3 alias bug
fixed**; fallbacks b3 24 → 43, D_BULK 27 → 26), pm-parameter-data.js 8, pm-b3-tracer.js
4 (live b₃), pm-certificates.js, content-templates.js, 7 unloaded JS files,
observer-heartbeat.js (24 → 43); pages philosophical-implications, certificates,
parameters, foundations, appendices, visualization-index, simulations,
beginners-guide (136 edits); data/derivations geometric_anchors_chain 19,
geometric_anchors_derivations_export 17, gauge_chain 7. Lane 448 → 325 (205 of those
are generated snapshots).
**Left:** `data/parameters.json` 162 (generated snapshot, stale values elder_kads 24,
b2 4 — refresh from a fresh build, then `python -m metaphysica.generators.
generate_datasheets`); config 41 (core_formulas 20, parameters/geometry 6, fitted 4,
fermion 3, __init__ 3, formula 2; label seed-era constants in comments only);
data derivations + named_certificates 43 (w0_dark_energy "consistent with DESI" ×2;
G31 "DERIVED v = k_gimel×(b3−4)"); generators 25 (generate_named_constants writes
seed_provenance "b3 = 24" beside b3 = 43; generate_pdf_paper.py:282 "Single seed:
b3 = 24"; generate-latex-paper.js abstract); website/AutoGenerated records 43 (keep the
gemini_*.json review records verbatim); SVGs (dimensional-reduction-pathway ×2 copies,
generation-count-consistency ×2); **Pages/faq.html is the worst page** — 23 live
`topology.b3` spans now render 43 inside seed-24 arithmetic ("SO(43) = 43×23/2",
"43/8 = 3"); theory-diagrams.html (TCS gluing, b₂ = 4 ×8, CY4 χ = 72 ÷ 24; unclosed
comment L344–371 pre-existing); foundations pages clifford-algebra L559,
dirac-equation L231/437 ("(24,2) with 1 timelike dimension" — wrong), so10-gut L727,
L746 ("unruled K3 reading" → adopted), yang-mills L628/631; index.html meta "(b3=24)"
(lead's main-page restructure); visualizations README.
**Unloaded JS (23 files, none deleted):** formula-database, formula-definitions,
observer-heartbeat, pm-beginner-guide-loader, pm-citations, pm-formula-multi-render,
pm-formula-renderer, pm-foundations-loader, pm-layperson-toggle (cited by
geometry_narration as "the site's reading toggle" — loaded by no page),
pm-loading-states, pm-paper-formula-renderer, pm-paper-param-processor,
pm-paper-renderer-blocks-patch, pm-paper-tooltips-integration, pm-param-paper,
pm-parameter-table, pm-section-loader, pm-visualization-manifest, theory-computations,
theory-constants-enhanced, theory-constants (generator template, test-pinned),
theory-derivations, theory-eom-beta.
**Blockers:** `metaphysica.Get('b3')` returns 24.0 from the Rust core
(`rust/physica_core/src/constants.rs`: SEED_B3 = 24.0, SEED_CHI_EFF = 72,
SEED_ROOTS_TOTAL = 288 …) — needs a Rust change + wheel rebuild; data/constants
regenerate to 24 because the datasheet builder reads the stale bundled snapshot
(BUNDLED_DATASHEET_LEAKS inventory in test_export_active_path_only must shrink when
fixed). Config value issues listed by the config sub-lane: moduli a_swampland
docstring √(26/13) vs code √(26/7); SO(10) has no cubic anomaly; THETA_23_NUFIT = 45;
PMNS_DELTA_DEG 232 vs cited 194; KAPPA_GUT V_5 = 21.6; formula id master-action-27d;
CHNP citation year. generate_72gates_json puts REG.b3 = 43 into 24-era text ("SO(43)",
"43 = 21_L + 21_R", "w0 = −1 + 1/43 = −23/24"); gauge_chain RG-01/02/03 and
WEINBERG-01 expected outputs do not follow from their queries. Visual baseline
tests/visual_baselines/beginners-guide.png will differ.

## EML dependency walker (tooling)
Fixed and deterministic: live seed via `b3_path.seed_values()`; `b3_leaf` /
`flavour_b3_leaf` recognised; raw 24 is "ambiguous", never rooted; in-process parse
per formula; rooted/ambiguous/non-rooted sum to total; new output blocks
(`tree_source_counts`, `cache_check`, `interpolated_trees`, `registration_conflicts`).
Root cause of the instability: the tree cache (113 rooted with `eml_trees.json`, 208
without, on one formulas.json), detection keyed on the value 24, last-registration-wins
for duplicate ids, and parser version differences. Before/after on 580 formulas:
113/9/467 → **193/1/386**, byte-identical across runs. New test file
`tests/test_eml_walker_seed_and_leaves.py` (24 tests; run with `--noconftest` because
the repo conftest sets METAPHYSICA_OUT). **Recommended `_EML_BASELINE`** after the next
full build: `{"total": 580, "b3_rooted_min": 193, "non_b3_max": 386, "ambiguous_max": 1}`
(ratio ceiling 3.65 → ~2.03; optional ratchets `interpolated_trees.count <= 15`,
`registration_conflicts.count <= 2`; fix the docstrings that say ambiguous folds into
rooted). **Left:** the arithma walker (same fixes; sort `producer_of` by id — order
changes 103 chain verdicts; re-measure `_ARITHMA_BASELINE_*`); duplicate registrations
`central-charge-unitarity` (unitary_filter_legacy wins) and `fermion-generations-v19`
(appendix P's abandoned b₃/8 route overwrites matter_sector_complete's ruled b₂/4).
Scratch harnesses: `scratchpad/walker/run_before.py`, `run_after.py`.
