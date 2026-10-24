"""Generate theories/pm/lineage/branches.yaml from the archaeology JSONL.
Structure (ids, labels, parents, statuses) is curated here; every reason, result
and source is copied verbatim from the archaeology entries."""
import glob, json, sys
import yaml

ARCH, OUT = sys.argv[1], sys.argv[2]
E = {}
for f in sorted(glob.glob(ARCH + "/a?.jsonl")):
    for line in open(f, encoding="utf-8"):
        if line.strip():
            e = json.loads(line)
            E[e["id"]] = e

# id, label, era, parent, status, superseded_by, entries, maps_to
V = [
 ("v2025_10_2_dual_time", "(10,2) dual-time original", "2025-07", None, "trunk", "v2025_12d_eft",
  ["a1-v0-10-2-dual-time"], []),
 ("v2025_12d_eft", "12D EFT revision (10D sugra + F-theory torus)", "2025-07-29", "v2025_10_2_dual_time", "trunk", "v2025_12_1_thermal",
  ["a1-v1-12d-eft-ftheory", "a1-gauge-u1-consciousness", "a1-de-quintessence"], []),
 ("v2025_2t_rebuild", "Proposal: rebuild on Bars two-time physics", "2025-07-29", "v2025_10_2_dual_time", "branch", None,
  ["a1-crit-existence", "a1-dim-two-time-2t"], []),
 ("v2025_12_1_thermal", "(12,1) bulk, thermal time, 64-component Pneuma", "2025-07-29", "v2025_12d_eft", "trunk", "v2025_13d_cy4",
  ["a1-v2-12-1-thermal-time-brane", "a1-dim-single-time-12-1", "a1-time-thermal-modular-flow", "a1-pneuma-fermion-field",
   "a1-comp-m9-unspecified", "a1-de-mashiach-modulus-attractor", "a1-num-gw-sme-dispersion", "a1-gen-chirality-from-compactification"], []),
 ("v2025_qut_genesis", "Wastepad 1: thermodynamic genesis (QUT A-Q)", "2025-08-06", "v2025_12_1_thermal", "branch", None,
  ["a1-v3-qut-thermal-genesis", "a1-gen-index-thermal-winding", "a1-gauge-so10-thermal-chain", "a1-de-pi-attractor",
   "a1-comp-k-pneuma-coset", "a1-num-proton-decay"], []),
 ("v2025_qut_sp2r", "Wastepad 2: (12,1) with Sp(2,R)", "2025-08-06", "v2025_12_1_thermal", "branch", None,
  ["a1-v4-qut-math-sp2r", "a1-num-alpha-attractor-inflation", "a1-conscious-iit-orch-or-field"], []),
 ("v2025_14_2", "Wastepad 3: (14,2) fixed to (12,1)", "2025-08-06", "v2025_qut_sp2r", "branch", None,
  ["a1-v5-14-2-synthesis", "a1-dim-14-2-fundamental", "a1-de-frt-no-lambda", "a1-comp-orbifold-14-2"], []),
 ("v2025_so10_2t_report", "Extended SO(10) + 2T report", "2025-08-09", "v2025_14_2", "dead_end", None,
  ["a1-v6-so10-2t-report", "a1-gauge-so10-higgs", "a1-conscious-modular-flow-spin-liquid"], []),
 ("v2025_13d_cy4", "13D (12,1) bulk with CY4 and F-theory", "2025-11-22", "v2025_12_1_thermal", "trunk", "v2025_26d_sp2r",
  ["a2-13d-cy4-fof", "a2-w0-thermal-time", "a2-w0-holographic-mep", "a2-d13-division-algebras", "a2-ngen-chi-over-24",
   "a2-holographic-v0", "a2-joyce-fano-in-window"], []),
 ("v2025_26d_sp2r", "26D (24,2) with Sp(2,R) to 13D shadows", "2025-11-24", "v2025_13d_cy4", "trunk", "v6_g2_masterplan",
  ["a2-26d-24-2-sp2r", "a2-mirror-sector"], ["bulk_signature.24_2"]),
 ("v6_g2_masterplan", "v6.2: G2 replaces CY4 (26D to 13D to G2 to 4D)", "2025-11-28", "v2025_26d_sp2r", "trunk", "v7_v12_tcs",
  ["a2-masterplan2-chain", "a2-b3-24-tcs187", "a2-chi-eff-6b3", "a2-cmb-bubbles", "a2-version-hiding"],
  ["b3_seed.seed_24", "chi_eff_route.constant_144"]),
 ("v6_14dx2", "14D x 2 two-time decomposition", "2025-11-29", "v6_g2_masterplan", "dead_end", "v6_g2_masterplan",
  ["a2-14dx2-2t", "a2-ngen-chi-over-48"], []),
 ("v7_v12_tcs", "v7-v12.8: TCS couplings, Re(T) = 7.086, honest assessment", "2025-12-02", "v6_g2_masterplan", "trunk", "v12_9_racetrack",
  ["a2-alpha45-tcs", "a2-re-t-7086", "a2-extra-derivations-failed", "a2-swampland-modules-rejected",
   "a2-proton-decay-ckm", "a2-neutrino-ordering"], ["re_t_adoption.calibrated"]),
 ("v12_9_racetrack", "v12.9-v15: Pneuma racetrack, hype removed", "2025-12-20", "v7_v12_tcs", "trunk", "v16_gates",
  ["a2-racetrack-pneuma", "a2-v14-overclaim-removed", "a2-torsion-chi-over-6", "a2-ngen-b3-over-8", "a3-ng-b3-over-8"],
  ["n_gen_source.b3_over_dim_O"]),
 ("v16_gates", "v16: w0 = -23/24, 72 gates, Leech S8", "2025-12-25", "v12_9_racetrack", "trunk", "v17_v20",
  ["a3-v16-lineage", "a2-w0-thawing-b3", "a2-cert-42", "a2-gates-72", "a2-288-root", "a2-leech-s8", "a2-multi-sector-dm"],
  ["dark_energy_betti.b3_24", "lattice_24d.leech"]),
 ("v17_v20", "v17-v20: sterility pipeline, zero free parameters, dual chi_eff", "2026-01-03", "v16_gates", "trunk", "v21_25d",
  ["a2-ns-1-2-b3", "a2-ns-golden", "a2-zero-free-params", "a2-chi-eff-dual", "a2-5level-chain-v20", "a2-hierarchy-rs"], []),
 ("v21_25d", "v21: 25D (24,1) unified time", "2026-01-18", "v17_v20", "trunk", "v22_bridges",
  ["a2-25d-24-1-unified-time", "a2-breathing-de"], []),
 ("v22_bridges", "v22: 12 bridge pairs, dual 13D shadows", "2026-01-18", "v21_25d", "trunk", "v23_27d",
  ["a2-12-bridge-pairs", "a2-4-dice-gnosis", "a2-alpha-9963", "a2-ai-validation-wording"], []),
 ("v23_27d", "v23: 27D (26,1) central sampler, 4Faces", "2026-01-25", "v22_bridges", "trunk", "v24_m27",
  ["a2-27d-26-1-central-sampler", "a2-higgs-1728", "a2-4faces", "a2-two-layer-or", "a2-branding-hebrew"], []),
 ("v24_m27", "v23.8-v24.2: M27 (24,1,2), EDOF = 3", "2026-02-01", "v23_27d", "trunk", "v24_cleanup",
  ["a3-v23-8-to-9", "a3-v24-1-edof", "a3-v24-2-27d", "a3-bulk-dcrit-26", "a3-brst-bars-sp2r", "a3-mass-planck"], []),
 ("v24_cleanup", "v24.2.1 cleanup and the lost models", "2026-03-15", "v24_m27", "trunk", "v25_two_time",
  ["a3-v24-2-1-cleanup", "a3-lost-models", "a3-mirror-dm", "a3-ret-174", "a3-orch-or-consciousness",
   "a3-inflation-slowroll", "a3-cabibbo-gaugino", "a3-theta13-routes"], ["flavour_seed_coupling.calibrated_24"]),
 ("v25_two_time", "Two-time adoption: 26D (24,2)", "2026-08-19", "v24_cleanup", "trunk", "v26_joyce_43",
  ["a3-two-time-2026-08-19", "a3-bulk-26-2", "a3-bulk-25-1", "a3-plus2-readings", "a3-bc-ghost-24", "a3-minimog-4x3",
   "a3-leech-eisenstein", "a3-ng-denominator-fix", "a3-h0-odowd", "a3-h0-ricci-flow", "a3-h0-kk-bridge",
   "a3-w0-thermal-0-8528", "a3-wa-variants", "a3-sterile-mixing"],
  ["bulk_signature.24_2", "bulk_signature.26_2", "bulk_signature.25_1"]),
 ("v25_b3_24_origin", "Search for an origin of b3 = 24", "2026-08-20", "v25_two_time", "dead_end", "v26_joyce_43",
  ["a3-b3-24-realizable", "a3-b3-24-parity-refutation", "a3-b3-15-24", "a3-tcs-parity", "a3-b3-origins", "a3-b3-seed24",
   "a3-g2-tcs"],
  ["b3_origin.arc_flag_stabiliser", "b3_origin.d4_root_shell", "b3_origin.input_24", "g2_construction.fano_tcs"]),
 ("v26_joyce_43", "Joyce orbifold, (b2, b3) = (12, 43)", "2026-09-09", "v25_two_time", "trunk", "v27_d015",
  ["a3-g2-joyce", "a3-b3-seed43", "a3-b3-seeds-7-19-31", "a3-lattice-leech", "a3-lattice-niemeier", "a3-old-leech-generator",
   "a3-g2-form", "a3-metric-construction", "a3-ng-b2-over-4", "a3-free-set", "a3-ret-computed-37-85", "a3-moduli-indexing",
   "a3-w0-other-n", "a3-chi-seed-dependent"],
  ["g2_construction.joyce_orbifold", "b3_seed.seed_43_joyce", "g2_form_convention.octonion_derived",
   "metric_construction.quadratic_contraction", "n_gen_source.b2_over_faces", "moduli_indexing.b3_clusters"]),
 ("v27_d015", "Main path: the D-015 author rulings", "2026-10-01", "v26_joyce_43", "active", None,
  ["a3-path-assessment", "a3-chi-k3-reading", "a3-wa1-selection", "a3-ret-calibrated", "a3-ng-rank-stabiliser",
   "a3-w0-b3-24", "a3-ret-instanton-route", "a3-chirality-flavour", "a3-candidate-closures", "a3-de-flux-attractor",
   "a3-chi-144-constant"],
  None),  # None -> the whole active selection
]

FRAMING = {"v27_d015": ("The D-015 author rulings: compact (octonion-derived) G2 form, the K3 reading "
    "chi_eff = 48n, Re(T) calibrated, WA-1 seed selection; Joyce seed (b2, b3) = (12, 43) in a 26D (24,2) bulk. "
    "This path generates the paper.")}

# Declared-only options: (fork, id, entry, status)
DECLARED_FORKS = [
 ("dark_energy_mechanism", "What drives dark energy (the mechanism, not the integer n)?"),
 ("spectral_index_route", "Where does the spectral index n_s come from?"),
 ("h0_route", "Where does the displayed H0 come from?"),
 ("gauge_origin", "How does the SO(10) gauge group arise?"),
 ("consciousness_model", "How is consciousness modelled, if at all?"),
]
O = [
 ("bulk_signature", "10_2", "a1-v0-10-2-dual-time", "disabled"),
 ("bulk_signature", "12_1", "a2-13d-cy4-fof", "disabled"),
 ("bulk_signature", "14_2", "a1-dim-14-2-fundamental", "disabled"),
 ("bulk_signature", "12_2_x2", "a2-14dx2-2t", "rejected"),
 ("bulk_signature", "24_1", "a2-25d-24-1-unified-time", "disabled"),
 ("bulk_signature", "26_1", "a2-27d-26-1-central-sampler", "disabled"),
 ("bulk_signature", "24_1_2", "a3-v24-2-27d", "disabled"),
 ("g2_construction", "cy4_ftheory", "a2-13d-cy4-fof", "disabled"),
 ("lattice_24d", "old_construction_a", "a3-old-leech-generator", "rejected"),
 ("lattice_24d", "eisenstein_split", "a3-leech-eisenstein", "disabled"),
 ("b3_origin", "betti_survey", "a3-b3-24-realizable", "disabled"),
 ("b3_origin", "profile_15_24", "a3-b3-15-24", "disabled"),
 ("n_gen_source", "chi_over_24", "a2-ngen-chi-over-24", "disabled"),
 ("n_gen_source", "chi_eff_over_48", "a3-ng-chi-over-48", "considered"),
 ("n_gen_source", "thermal_winding", "a1-gen-index-thermal-winding", "disabled"),
 ("chi_eff_route", "dual_72", "a2-chi-eff-dual", "disabled"),
 ("re_t_adoption", "higgs_vev_174", "a3-ret-174", "disabled"),
 ("re_t_adoption", "m2_instanton", "a3-ret-instanton-route", "rejected"),
 ("dark_energy_mechanism", "mep_11_13", "a2-w0-holographic-mep", "disabled"),
 ("dark_energy_mechanism", "thermal_time", "a3-w0-thermal-0-8528", "disabled"),
 ("dark_energy_mechanism", "mashiach_quintessence", "a1-de-quintessence", "disabled"),
 ("dark_energy_mechanism", "pi_attractor", "a1-de-pi-attractor", "disabled"),
 ("dark_energy_mechanism", "flux_attractor", "a3-de-flux-attractor", "rejected"),
 ("spectral_index_route", "one_minus_2_over_b3", "a2-ns-1-2-b3", "rejected"),
 ("spectral_index_route", "golden_modulated", "a2-ns-golden", "considered"),
 ("spectral_index_route", "re_t_slow_roll", "a3-inflation-slowroll", "rejected"),
 ("h0_route", "odowd_composite", "a3-h0-odowd", "considered"),
 ("h0_route", "ricci_flow", "a3-h0-ricci-flow", "disabled"),
 ("h0_route", "kk_bridge", "a3-h0-kk-bridge", "rejected"),
 ("gauge_origin", "so13_thermal_chain", "a1-gauge-so10-thermal-chain", "disabled"),
 ("gauge_origin", "conventional_higgs", "a1-gauge-so10-higgs", "considered"),
 ("consciousness_model", "u1_consciousness", "a1-gauge-u1-consciousness", "disabled"),
 ("consciousness_model", "iit_orch_or_field", "a1-conscious-iit-orch-or-field", "disabled"),
 ("consciousness_model", "spin_liquid_modular_flow", "a1-conscious-modular-flow-spin-liquid", "disabled"),
 ("consciousness_model", "orch_or_pair_shielding", "a3-orch-or-consciousness", "considered"),
 ("consciousness_model", "two_layer_or", "a2-two-layer-or", "disabled"),
]


def uniq(xs, cap):
    out = []
    for x in xs:
        if x and x not in out:
            out.append(x)
    return out[:cap]


def src_of(e):
    ev = e.get("evidence") or []
    return ev[0] if ev else (e.get("runnable_source") or "")


def version(v, active):
    vid, label, era, parent, status, sup, ids, maps = v
    es = [E[i] for i in ids]
    head = es[0]
    kr = [dict(quantity=k.get("quantity"), value=str(k.get("value")), source=k.get("source"))
          for e in es for k in (e.get("key_results") or []) if k.get("source")]
    return dict(
        id=vid, label=label, era=era, parent=parent, status=status, superseded_by=sup,
        framing=FRAMING.get(vid) or head.get("answer") or head.get("title"),
        why=head.get("why") or "",
        worked=uniq([w for e in es for w in (e.get("what_worked") or [])], 8),
        failed=uniq([w for e in es for w in (e.get("what_failed") or [])], 8),
        key_results=kr[:12],
        evidence=uniq([x for e in es for x in (e.get("evidence") or [])], 12),
        maps_to=maps if maps is not None else active,
        branches_considered=[dict(title=e["title"], answer=e.get("answer"), status=e.get("status_now"),
                                  why=e.get("why"), source=src_of(e)) for e in es[1:]],
    )


def option(o):
    fork, oid, eid, status = o
    e = E[eid]
    return dict(fork=fork, id=oid, summary=e.get("answer") or e["title"], consequence=e.get("why") or "",
                status=status, restored_from=e.get("runnable_source") or "", source=src_of(e),
                kill_condition="", decision_refs=[])


def main():
    from metaphysica.simulations.core import variants
    act = ["%s.%s" % kv for kv in sorted(variants.active_selection().items())]
    used = {i for v in V for i in v[6]} | {o[2] for o in O}
    missing = sorted(set(E) - used)
    doc = dict(schema="metaphysica.lineage/1",
               sources="PrincipiaMetaphysica/docs/plan/paths/archaeology/a{1,2,3}.{md,jsonl}",
               versions=[version(v, act) for v in V],
               forks=[dict(id=f, question=q, source="archaeology", notes="declared only: no engine switch")
                      for f, q in DECLARED_FORKS],
               options=[option(o) for o in O])
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generated by docs/plan/paths/gen_branches.py from the archaeology; edit there.\n")
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True, width=100)
    print("versions", len(V), "options", len(O), "unassigned entries", missing)


main()
