# TODO — bugs, code smells and decisions from the 2026-10-01/02 review

Sources: the lane reports (`lanes/wording_lanes.md`), the computation reports
(`lanes/pr1_pr2_pr3.md`), the verifications (`verifications_and_classifications.md`),
the exploration reports behind the plan, and the lead's review. Each item names its
track in the plan (B = bug-fix track; P3/P8 = turned into a switch; W = wording;
A = author decision). Tick items here as they land, with the commit.

## Bugs — values or logic wrong on the active path (B, decision entry where a value moves)
- [ ] Off-path generation routes published live: `chirality.generation_count` = 5,
      `g2_holonomy.n_gen` = 5, `index.family_index` = 5.375, `topology.n_gen` = 24//8
      alias. → OFF-PATH (n_gen_source = b3_over_dim_O) or re-point to b₂/4.
- [ ] Triple-track legs that disagree on the active path, re-expressible through the
      adopted K3 reading (48n): dirac-zero-modes, chirality-index-theorem,
      euler-characteristic, three-generations; heal their `ruled_divergences` rows.
- [ ] `g2_geometry.run_eml` computes χ_eff = 6b₃ = 258 and n_gen = 5 while `run()` gives
      144 and 3.
- [ ] `topology.mephorash_chi` is sourced by the off-path euler-characteristic formula
      (TCS); re-point to k3-reading-generations.
- [ ] Duplicate registrations, last-wins: `central-charge-unitarity`
      (unitary_filter_legacy wins); `fermion-generations-v19` (appendix P's abandoned
      b₃/8 route overwrites matter_sector's ruled b₂/4).
- [ ] G_GEOMETRY_BETTI gate tests `b3 == 24` (should test b₃ = 7 + 3b₂ like
      CERT_G2_BETTI_B3).
- [ ] `g2_geometry.verify_stability` window [52.9, 53.1] calibrated at 24; ratio 89.73 at 43.
- [ ] `derivations.dof_after_sp2r` publishes 324 (= 27·24/2, the retired 27D count).
- [ ] `generate_72gates_json` injects b₃ = 43 into 24-era text ("SO(43)", "43 = 21_L + 21_R").
- [ ] `gauge_chain` RG-01/02/03 and WEINBERG-01 expected outputs do not follow from
      their queries.
- [ ] Config docstring/code mismatches: moduli a_swampland (√(26/13) stated, √(26/7)
      computed); THETA_23_NUFIT = 45; PMNS_DELTA_DEG 232 vs cited 194; KAPPA_GUT V_5 = 21.6.
- [ ] Two α*⁻¹ on the active path (asymptotic_safety 24 vs gauge_unification 43).
- [ ] `base/dynamic_metadata.w0_description` hard-codes "derived"/"Excellent agreement";
      `cosmology.w0_derived` validated PASS against the unverified −0.957 bound.
- [ ] `dark_energy.py` reference "desi2025_thawing": title looks invented for
      arXiv:2503.14738 — verify against the fetched record.
- [ ] Rust core `SEED_B3 = 24.0` (and SEED_CHI_EFF = 72, SEED_ROOTS_TOTAL = 288):
      `metaphysica.Get('b3')` returns 24. Needs a Rust change and a wheel rebuild.
- [ ] `data/parameters.json` is a stale hand-copied snapshot (elder_kads 24, b2 4);
      refresh from a fresh build, then `generate_datasheets` (shrinks
      `BUNDLED_DATASHEET_LEAKS`).
- [ ] Arithma dependency walker: live seed, `root_seed`, sort `producer_of` by id
      (order changes 103 chain verdicts); re-measure `_ARITHMA_BASELINE_*`.
- [ ] EML `_EML_BASELINE` → {"total": 580, "b3_rooted_min": 193, "non_b3_max": 386,
      "ambiguous_max": 1} after the next full build; fix the docstrings that say
      ambiguous folds into rooted.
- [ ] 7 published sentences derive χ_eff = 144 as "6·b₃" (e.g. the n_s infrared
      closure in theory_output: "chi_eff = 6*b3 = 144"). Under D-015 the value 144 is
      live via the K3 reading (48n); the 6b₃ attribution is not (258 at b₃ = 43).
      Re-attribute; ratchet `chi_from_6b3` ceiling 7 (2026-10-02).
- [ ] `spectral-residue-general-v19`: its LaTeX fails to render ("parse error"), so the
      build lists it as unrenderable (pre-existing: already in the committed
      `formula_renders.json`; not caused by the 10-01 wording edits).
- [ ] `alpha-t-derivation`: `eml_tree_str` entirely commented out (5 candidate forms);
      choosing the canonical one is an authoring decision (A).

## Calibrate-versus-follow-seed modules → switches (P3/P8)
Each computes at the live b₃ from a formula written for 24. Each becomes a fork with
`calibrated_24` and `follow_seed` options, kept honest in both:
`speed_of_light` (c = 1.79e8 m/s at 43), `alp_portals` (fails CAST/stellar/mass window,
G49), baryon N_eff = 2(b₃−14), gaugino rows, sterile alpha_leak, neutrino_algebraic
reading four_face's alpha_leak (θ₁₃ 12.89°), four_face `n_e8_blocks = b3//8` (OT06,
bulk), pneuma formulas (neural gate, 4d-fermion, lagrangian-hierarchy 27),
thermal_time alpha-t-base.

## Code smells (P9)
- [ ] 9 fork readers silently fall back to the default on `except Exception` (P3B list).
- [ ] 123 import-time asserts in 15 files (P1E).
- [ ] `_arithma_num` defined 103 times in 53 files; 111 `get_references` copies; 5
      sigma-verdict copies with 3 vocabularies; 3 experimental-data loaders.
- [ ] 21 SimulationBase subclasses not wired, with no allow-list test.
- [ ] `run_all_simulations.py` import-time side effects (.env, sys.path), hand-kept
      phase table, hard-coded V16 bounds.
- [ ] `config/core_formulas.py`: a second formula library with 7 colliding ids.
- [ ] 23 JS files no page loads (decide: stop shipping or wire).
- [ ] `core/parameter_artifact.py` hard-codes `H:` and sibling-repo fallbacks.
- [ ] Stale docs: engine `docs/FUTURE.md` ("16,763 dead lines" already revived).

## Wording (W) — see `lanes/wording_lanes.md` for per-file lists and line numbers
L1 4 files · L2 ~13 appendices · L3 ~25 files (168 hits) · L4 11 files (49) · L5 ~30
files · L6 config/generators/data/pages (faq.html worst; theory-diagrams; 4 foundations
pages; SVGs; main-page restructure).

## Author decisions needed (A)
- [ ] Ratify the D-019 amendments (a)–(f) before the first PM assessment run.
- [ ] Whether to stop shipping the 23 unloaded JS files and the website/AutoGenerated
      records nobody reads.
- [ ] Regenerating the stale PNG figures (descent_chain, w_evolution, bridge_pressure,
      seesaw_dual_shadow).
- [ ] The duplicate `H:/Github/MathsPhysicsEcosystem/*` clones (metaphysica,
      PrincipiaMetaphysica, metaphysica-app …): which is canonical.
- [ ] Items the lanes flagged as possibly wrong, to verify (never assume): Ω₁₃^String;
      Spin(12,1) ⊃ Spin(3,1)×Spin(8) (4 + 8 ≠ 13); the 13 = 1+4+8 vs 7+6 split;
      "T₄ is the symmetry group of the 24-cell"; Pettini arXiv:2606.12457; the "252
      Joyce pairs" count; "Hitchin identity φφ = 6δ"; muon g-2 2025 status.
