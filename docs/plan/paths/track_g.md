# Track G: G1, G3, G4 wiring map (2026-10-26)

Worktree `metaphysica-pathsg` (branch paths-g), uncommitted. No adopted value or default changed.

## What changed
- `src/metaphysica/simulations/core/variants.py`: `VariantOption.requires/excludes`;
  `validate_constraints` (run at import); `violations`, `compatible`, `departures`,
  `selection_id`, `load_selection`; `resolve()` honours `METAPHYSICA_SELECTION`
  (explicit override > selection file > `METAPHYSICA_VARIANT_<ID>` > default; file
  cached per path+mtime; unknown fork or option raises ValueError).
- `switch_search.py`: `combinations_for` now prunes (backtracking, same adopted-first
  order, cap semantics unchanged); new `count_compatible` (component-wise count, no expansion).
- `PM/geometry/b3_path.py` (small G1 fix): `n_gen_report` treated `n_gen_source` as
  explicit only via its env var, so a selection naming it was silently ignored. It now
  also checks the selection file.
- New `P/docs/plan/paths/sweep_paths.py`: takes RUNS and a JSON list of selections,
  writes `RUNS/<selection_id>/` + `selection.json`, same DONE.json/engine reuse rule as
  sweep.py, refuses incompatible selections. sweep.py untouched. Not executed.
- Tests: `tests/test_selections_and_compat.py` (9; all failed before the change):
  selection_id active / ignores defaults and key order; load_selection rejects unknown
  fork and option; resolve precedence; bad file fails in resolve; unknown constraint
  names fail validation; declared exclusion makes selection incompatible; enumeration
  prunes and matches count_compatible; selection file reaches n_gen_report.

Selection id: first 12 hex of sha256 of the sorted compact JSON of departures from
the adopted defaults; `active` when none. Partial maps are accepted (missing = default).

## G3 sizes (22 forks)
| space | size |
|---|---|
| all options | 2,786,918,400 (2.79e9) |
| all options, pruned | 2,090,188,800 (2.09e9, -25.0%) |
| sweepable only (non-DISABLED) | 17,418,240 |
| sweepable only, pruned | 11,612,160 (-33.3%) |
| open forks only (8) | 1,440, unchanged (no constraint touches an open fork) |

## Declared constraints (only those stated in code; none invented)
All on `n_gen_source` versus `b3_seed`; `variants.py` line numbers are of the pre-edit file.
1. `n_gen_source=b3_over_dim_O` excludes `b3_seed` in {seed_7, 19, 31, 43_joyce}:
   variants.py:936-939 ("incompatible with every Joyce-reachable value -- 7, 19, 31 and 43
   are all odd"); n_gen_source notes variants.py:920-922.
2. `n_gen_source=b2_over_faces` excludes `b3_seed=seed_24`: variants.py:951-953 ("gives 1
   at the off-path b_2 = 4, so it is wrong on the seed_24 branch"); notes 922-925.
Not declared (ambiguous in text): `chi_eff_over_48` (variants.py:981 says it fails on the
Joyce family on both chi_eff branches, yet survives under D-009 with the K3 reading);
`chi_eff_route=seed_dependent` (variants.py chi_eff notes: "IS" b3_over_dim_O, an identity
and not a stated requirement). No other fork states a constraint. `requires` is
implemented and tested through validation but no option uses it. The adopted state is compatible.

## G4 wiring map (report only)
Readers (file:line under `src/metaphysica`):
| fork | call sites |
|---|---|
| spectral_index_route | simulations/PM/cosmology/spectral_routes.py:44 |
| h0_route | PM/cosmology/late_time_routes.py:34 |
| dark_energy_mechanism | late_time_routes.py:40 |
| dark_energy_betti | late_time_routes.py:54 |
| re_t_adoption | PM/cosmology/baryon_asymmetry.py:168 |
| b3_seed | PM/geometry/b3_path.py:164 (resolve_path, used widely); g2_closure.py:496; env set by core/seed_blindness.py:104 |
| n_gen_source | PM/geometry/b3_path.py:247 (only when env var or selection names it) |
| b3_origin | core/switch_search.py:455, 486 only (consistency checks; no simulation) |
| joyce_contribution_table | PM/geometry/joyce_contributions.py:83 |
| g2_form_convention | PM/algebra/octonions.py:115; PM/geometry/g2_differential.py:343; glued_orbit_scan.py:199; geometry_narration.py:118; g2_closure.py:495 |
| flavour_seed_coupling | PM/particle/yukawa_derivation.py:912 (env first, then resolve at :917) |
| metric_construction | g2_differential.py:516; geometry_narration.py:163 |
| chi_eff_route | PM/geometry/chi_eff_branches.py:285,287; geometry_narration.py:384; core/fork_implications.py:152 |
| twisted_norm_convention | PM/geometry/metric_pairing.py:174 |
| lattice_24d | PM/algebra/leech_lattice.py:608 |
| g2_construction | PM/geometry/g2_closure.py:481 (only) |
| render_policy | generators/eml_render_validity.py:198 |
| theory_uncertainty_policy | generators/generate_validation_certificates.py:185 |
| seed_selection | PM/geometry/closed_geometry/selection.py:52 |
| **moduli_indexing** | **none: unwired** |
| **face_genericity** | **none: unwired** (read_adopted only) |
| **bulk_signature** | **none: unwired** (read_adopted reads CANON; bridge.py only carries the constant) |

Unwired (no reader outside variants/describe): moduli_indexing, face_genericity,
bulk_signature. b3_origin is read only by switch_search, so it cannot change a build row.
g2_construction is read once, in g2_closure.

Side findings: (a) yukawa_derivation.py:912 reads its env var before `resolve`, so that
one var outranks a selection file; (b) fork_implications.py:276, preferred_path.py:211 and
switch_search.py:524 evaluate combinations by setting per-fork env vars, so under an active
METAPHYSICA_SELECTION the file wins over those vars; (c) `testground/switches/resolve.py`
is a separate resolver with its own precedence and does not read the selection file.
None changed (outside scope).

## The 24 of 37 option runs that changed no row
Source: `/h/claude-scratch/pc.json` (`cross.changed_rows` = 0). Rule used: a fork with no
reader cannot change a row (unwired); one with a reader but zero changed rows is
coincident or feeds a non-row output. I did not run anything to separate those two.
- Unwired / no simulation reader (9 runs): b3_origin x4 (arc_flag_stabiliser, d4_root_shell,
  input_24, joyce_twisted_sector), bulk_signature x2 (25_1, 26_2), face_genericity--all,
  moduli_indexing x2 (b2_gauge, cy3_shadow).
- Reader exists, no row moved (15 runs), so merely coincident or non-row output (narration,
  certificates, render): chi_eff_route x3 (narration/branch text), g2_form_convention--all_plus_one,
  joyce_contribution_table--supplied, lattice_24d--niemeier_e8x3, metric_construction--hitchin_cubic,
  n_gen_source x2 (chi_eff_over_48, chi_over_24; the source text expects 3, same as adopted),
  re_t_adoption--computed_vacuum, render_policy--permissive, seed_selection--ruling_only,
  theory_uncertainty_policy x2, twisted_norm_convention--orbit_average.

## Joint sweep of the overlapping pairs (2026-10-27, engine c294094)

`interactions.py` on runs_g: 37 single-option runs (24 inert), 636 cross-fork pairs,
10 whose changed rows overlap. All 10 were built jointly with `sweep_paths.py`
(selections in `<scratchpad>/pair_selections.json`), and `interactions.py joint`
compared each joint build with the single-option runs (test_interactions.py, 5 cases).

Result: **0 non-additive rows in all 10.** Every joint row equals the baseline or one of
the two single-option values. On rows both options move:

| Pair | Shared rows | Joint takes |
|---|---|---|
| dark_energy_betti (any of 6) × dark_energy_mechanism=mep_11_13 | 15 | mep_11_13, all 15 |
| b3_seed=seed_24 × flavour_seed_coupling=calibrated_24 | 16 | identical values |
| b3_seed=seed_24 × dark_energy_mechanism=mep_11_13 | 2 (w0) | mep_11_13 |
| b3_seed=seed_24 × h0_route=kk_bridge / ricci_flow | 1 (H0_local) | h0_route |

So the 2.09e9-path space factorises on today's wiring: a path's rows are the union of
its single-option deltas, with the precedence above on shared rows. Two follow-ups:
- dark_energy_betti only acts under the default mechanism: declare it (`requires`
  dark_energy_mechanism default, or mark the betti options inert under mep_11_13), so
  describe() and the site stop offering 6 x mep paths that are one path.
- flavour_seed_coupling=calibrated_24 reproduces seed_24's 16 flavour rows exactly: one
  lever behind two forks. Owner: merge, or keep and say so.

Seed_24 joint selections must state `n_gen_source=b3_over_dim_O`: sweep_paths validates
against the adopted defaults, where b2_over_faces excludes seed_24, while b3_path uses the
path's declared source unless one is explicit. Every seed_24 build (single or joint)
exits 1 on "Audit shadow derivations across the registry" and publishes with --keep-going.
