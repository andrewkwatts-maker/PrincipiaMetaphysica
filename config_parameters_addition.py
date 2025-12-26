# ==============================================================================
# CORE PARAMETERS (ParameterMetadata Registry)
# ==============================================================================
# Centralized parameter definitions for formula linkage system
# These parameters are referenced by formulas in formula-database.js
#
# ADD THIS SECTION TO THE END OF config.py (after line 6965)

CORE_PARAMETERS = {
    # === GEOMETRIC PARAMETERS ===
    "effective-euler": ParameterMetadata(
        id="effective-euler",
        value=144,
        units="dimensionless",
        symbol="χ_eff",
        status=ParameterCategory.GEOMETRIC,
        title="Effective Euler Characteristic",
        description="G₂ manifold effective Euler from TCS construction",
        oom=2,
        long_description="The effective Euler characteristic of the TCS G₂ manifold #187. "
                        "Computed as χ_eff = 2(h¹¹ - h²¹ + h³¹) = 2(4 - 0 + 68) = 144. "
                        "Also derivable from flux quantization: χ_eff = 6 × b₃ = 6 × 24 = 144.",
        derivation="χ_eff = 2(h¹¹ - h²¹ + h³¹) = 2(4 - 0 + 68) = 144",
        derivation_formula_ids=["effective-euler", "tcs-topology"],
        used_in_formulas=["generation-number", "tcs-topology", "flux-quantization"],
        section_refs=["section-topology", "section-predictions"],
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    "betti-b2": ParameterMetadata(
        id="betti-b2",
        value=4,
        units="dimensionless",
        symbol="b₂",
        status=ParameterCategory.GEOMETRIC,
        title="Second Betti Number",
        description="Kähler moduli count (2-cycles)",
        oom=0,
        long_description="The second Betti number of the TCS G₂ manifold #187. "
                        "Equals h¹¹ = 4, representing the number of independent 2-cycles. "
                        "Controls Kähler moduli and doublet-triplet splitting via discrete torsion.",
        derivation="b₂ = h¹¹ = 4 from TCS G₂ topology",
        derivation_formula_ids=["tcs-topology"],
        used_in_formulas=["mirror-temp-ratio", "doublet-triplet"],
        section_refs=["section-topology"],
        version_introduced="v14.0",
        last_updated="v14.1"
    ),

    "betti-b3": ParameterMetadata(
        id="betti-b3",
        value=24,
        units="dimensionless",
        symbol="b₃",
        status=ParameterCategory.GEOMETRIC,
        title="Third Betti Number",
        description="Associative 3-cycle count",
        oom=1,
        long_description="The third Betti number of the TCS G₂ manifold #187. "
                        "Represents the number of independent associative 3-cycles. "
                        "Critical for flux quantization and CP phase geometric origin.",
        derivation="b₃ = 24 from TCS G₂ topology; χ_eff = 6 × b₃ = 144",
        derivation_formula_ids=["tcs-topology", "flux-quantization"],
        used_in_formulas=["cp-phase-geometric", "mirror-temp-ratio"],
        section_refs=["section-topology", "section-neutrinos"],
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    "generation-count": ParameterMetadata(
        id="generation-count",
        value=3,
        units="dimensionless",
        symbol="n_gen",
        status=ParameterCategory.GEOMETRIC,
        title="Generation Count",
        description="Number of fermion generations",
        oom=0,
        long_description="The number of fermion generations derived from TCS G₂ topology. "
                        "Computed as n_gen = χ_eff / (24 × flux_reduce) = 144 / (24 × 2) = 3. "
                        "Alternative derivation from spinor saturation: n_gen = N_flux / spinor_DOF = 24 / 8 = 3.",
        derivation="n_gen = χ_eff / (24 × 2) = 144 / 48 = 3",
        derivation_formula_ids=["generation-number", "tcs-topology"],
        used_in_formulas=["generation-number"],
        depends_on_params=["effective-euler"],
        section_refs=["section-fermions", "section-predictions"],
        testable=True,
        testable_by="Collider searches for 4th generation",
        testable_year=2030,
        version_introduced="v13.0",
        last_updated="v14.1"
    ),

    # === FUNDAMENTAL SCALES ===
    "planck-mass": ParameterMetadata(
        id="planck-mass",
        value=2.435e18,
        units="GeV",
        symbol="M_Pl",
        status=ParameterCategory.INPUT,
        title="Reduced Planck Mass",
        description="Fundamental gravitational scale",
        oom=18,
        long_description="The reduced Planck mass M_Pl = √(ℏc/8πG) = 2.435×10¹⁸ GeV. "
                        "This is the fundamental gravitational scale that sets the strength of gravity. "
                        "Used consistently throughout all formulas (not the full Planck mass M_P = √(ℏc/G)).",
        experimental_value=2.435e18,
        experimental_error=0.001e18,
        experimental_source="PDG 2024",
        derivation_formula_ids=["planck-mass-derivation"],
        used_in_formulas=["gut-scale", "hierarchy-ratio", "higgs-vev", "planck-mass-derivation"],
        section_refs=["section-scales"],
        notes="v12.4 FIX: Standardized to reduced mass everywhere (was inconsistent)",
        version_introduced="v1.0",
        last_updated="v12.4"
    ),

    "gut-scale": ParameterMetadata(
        id="gut-scale",
        value=2.118e16,
        units="GeV",
        symbol="M_GUT",
        status=ParameterCategory.DERIVED,
        title="GUT Unification Scale",
        description="Grand unification energy scale",
        oom=16,
        uncertainty=0.05e16,
        uncertainty_percent=2.4,
        long_description="The grand unification scale where gauge couplings unify. "
                        "Derived from TCS G₂ geometry: M_GUT = M_Pl × exp(-2π√(κ_GUT × χ_eff / b₃)). "
                        "Result: M_GUT = 2.118×10¹⁶ GeV with ~2.4% uncertainty.",
        derivation="M_GUT = M_Pl × exp(-2π√(κ_GUT × χ_eff / b₃))",
        derivation_formula_ids=["gut-scale", "tcs-topology"],
        simulation_file="simulations/g2_torsion_m_gut_v12_4.py",
        used_in_formulas=["gut-scale", "proton-lifetime", "gut-coupling"],
        depends_on_params=["planck-mass", "effective-euler", "betti-b3"],
        section_refs=["section-gauge-unification", "section-predictions"],
        testable=True,
        testable_by="Proton decay experiments",
        testable_year=2035,
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    "bulk-scale": ParameterMetadata(
        id="bulk-scale",
        value=7.4604e15,
        units="GeV",
        symbol="M_*",
        status=ParameterCategory.DERIVED,
        title="13D Fundamental Scale",
        description="Bulk fundamental scale from volume",
        oom=15,
        long_description="The fundamental scale in 13D after Sp(2,R) gauge fixing. "
                        "Derived from dimensional analysis: M_* = (M_Pl² / V₉)^(1/11). "
                        "Result: M_* = 7.4604×10¹⁵ GeV (LOW string scale scenario).",
        derivation="M_* = (M_Pl² / V₉)^(1/11)",
        derivation_formula_ids=["planck-mass-derivation", "master-action-26d"],
        used_in_formulas=["master-action-26d", "planck-mass-derivation"],
        depends_on_params=["planck-mass"],
        section_refs=["section-dimensional-reduction"],
        notes="v12.4: Low string scale from consistent volume calculation",
        version_introduced="v12.4",
        last_updated="v14.1"
    ),

    # === GAUGE SECTOR ===
    "gut-coupling": ParameterMetadata(
        id="gut-coupling",
        value=23.54,
        units="dimensionless",
        symbol="α_GUT^-1",
        status=ParameterCategory.DERIVED,
        title="Inverse GUT Coupling",
        description="Unified gauge coupling at M_GUT",
        oom=1,
        uncertainty=0.5,
        uncertainty_percent=2.1,
        long_description="The inverse unified gauge coupling constant at the GUT scale. "
                        "All three SM gauge couplings (g₁, g₂, g₃) unify to α_GUT^-1 ≈ 23.54 at M_GUT.",
        experimental_value=24.0,
        experimental_error=1.0,
        experimental_source="RG running from PDG 2024",
        sigma_deviation=0.46,
        derivation="From RG running of gauge couplings to M_GUT",
        derivation_formula_ids=["gut-coupling", "rg-running-couplings"],
        used_in_formulas=["gut-coupling", "proton-lifetime"],
        depends_on_params=["gut-scale"],
        section_refs=["section-gauge-unification"],
        testable=True,
        testable_by="Precision RG running",
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    "suppression-factor": ParameterMetadata(
        id="suppression-factor",
        value=2.1,
        units="dimensionless",
        symbol="S",
        status=ParameterCategory.DERIVED,
        title="TCS Suppression Factor",
        description="Geometric proton decay suppression",
        oom=0,
        uncertainty=0.3,
        uncertainty_percent=14,
        long_description="Geometric suppression factor for proton decay from TCS cycle separation. "
                        "Derived from d/R = 0.12 where d is the spatial separation of matter curves. "
                        "Result: S = exp(2π × d/R) = exp(2π × 0.12) ≈ 2.1.",
        derivation="S = exp(2π × d/R) with d/R = 0.12",
        derivation_formula_ids=["proton-lifetime", "tcs-suppression"],
        simulation_file="simulations/proton_decay_geometric_v13_0.py",
        used_in_formulas=["proton-lifetime", "tomita-takesaki"],
        depends_on_params=["gut-scale"],
        section_refs=["section-proton-decay", "section-predictions"],
        testable=True,
        testable_by="Super-Kamiokande, Hyper-Kamiokande",
        testable_year=2030,
        version_introduced="v14.0",
        last_updated="v14.1"
    ),

    # === ELECTROWEAK SECTOR ===
    "higgs-vev": ParameterMetadata(
        id="higgs-vev",
        value=246,
        units="GeV",
        symbol="v",
        status=ParameterCategory.INPUT,
        title="Higgs VEV",
        description="Higgs vacuum expectation value",
        oom=2,
        long_description="The Higgs vacuum expectation value v = 246 GeV. "
                        "Related to electroweak scale and fermion mass generation via Yukawa couplings. "
                        "Sets the scale for W and Z boson masses: M_W = gv/2, M_Z = √(g² + g'²)v/2.",
        experimental_value=246.22,
        experimental_error=0.06,
        experimental_source="PDG 2024",
        sigma_deviation=3.7,
        derivation="v = √2 × M_W / g = 246.22 GeV from electroweak precision",
        used_in_formulas=["hierarchy-ratio", "higgs-vev", "seesaw-mechanism", "higgs-quartic",
                         "bottom-quark-mass", "tau-lepton-mass"],
        depends_on_params=["planck-mass"],
        section_refs=["section-electroweak", "section-fermions"],
        version_introduced="v1.0",
        last_updated="v14.1"
    ),

    # === NEUTRINO SECTOR ===
    "delta-cp": ParameterMetadata(
        id="delta-cp",
        value=197,
        units="degrees",
        symbol="δ_CP",
        status=ParameterCategory.CALIBRATED,
        title="CP Violation Phase",
        description="Neutrino CP-violating phase",
        oom=2,
        uncertainty=25,
        uncertainty_percent=12.7,
        long_description="The CP-violating phase in the PMNS neutrino mixing matrix. "
                        "Geometrically derived from H₃(G₂,Z) 3-cycle orientations. "
                        "NuFIT 6.0 (2024): δ_CP = 197° ± 25° (normal ordering).",
        experimental_value=197,
        experimental_error=25,
        experimental_source="NuFIT 6.0 (2024)",
        sigma_deviation=0.0,
        derivation="δ_CP = 2π × (cycle_twist / cycle_period) from G₂ associative cycles",
        derivation_formula_ids=["cp-phase-geometric"],
        simulation_file="simulations/ckm_cp_rigor.py",
        used_in_formulas=["cp-phase-geometric"],
        depends_on_params=["betti-b3"],
        section_refs=["section-neutrinos", "section-predictions"],
        testable=True,
        testable_by="T2K, NOvA, DUNE",
        testable_year=2027,
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    # === DARK ENERGY SECTOR ===
    "thermal-exponent": ParameterMetadata(
        id="thermal-exponent",
        value=4.5,
        units="dimensionless",
        symbol="α_T",
        status=ParameterCategory.DERIVED,
        title="Thermal Time Exponent",
        description="Thermal friction scaling exponent",
        oom=0,
        uncertainty=0.3,
        uncertainty_percent=6.7,
        long_description="The thermal time scaling exponent controlling dark energy evolution. "
                        "Appears in thermal friction term: α_T = 4.5 at z=0. "
                        "Evolves to α_T ≈ 2.7 at high redshift (z>2).",
        derivation="α_T = 4 + geometric_correction from thermal friction",
        derivation_formula_ids=["dark-energy-w0", "dark-energy-wa", "thermal-time"],
        simulation_file="simulations/wz_evolution_desi_dr2.py",
        used_in_formulas=["dark-energy-w0", "dark-energy-wa", "thermal-time"],
        section_refs=["section-dark-energy", "section-predictions"],
        testable=True,
        testable_by="DESI, Euclid",
        testable_year=2026,
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    "dark-energy-w0": ParameterMetadata(
        id="dark-energy-w0",
        value=-0.8528,
        units="dimensionless",
        symbol="w₀",
        status=ParameterCategory.PREDICTED,
        title="Dark Energy EOS Today",
        description="Present-day dark energy equation of state",
        oom=0,
        uncertainty=0.02,
        uncertainty_percent=2.3,
        long_description="The present-day (z=0) dark energy equation of state parameter. "
                        "Predicted from thermal friction mechanism: w₀ = -0.8528. "
                        "DESI DR2 (2025): w₀ = -0.827 ± 0.063 (2.5σ tension with ΛCDM).",
        experimental_value=-0.827,
        experimental_error=0.063,
        experimental_source="DESI DR2 (2025)",
        sigma_deviation=0.41,
        derivation="w₀ = -1 + thermal_correction from α_T",
        derivation_formula_ids=["dark-energy-w0", "thermal-time"],
        simulation_file="simulations/wz_evolution_desi_dr2.py",
        used_in_formulas=["dark-energy-w0", "dark-energy-wa"],
        depends_on_params=["thermal-exponent"],
        section_refs=["section-dark-energy", "section-predictions"],
        testable=True,
        testable_by="DESI, Euclid, Roman",
        testable_year=2026,
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    "dark-energy-wa": ParameterMetadata(
        id="dark-energy-wa",
        value=-0.95,
        units="dimensionless",
        symbol="w_a",
        status=ParameterCategory.PREDICTED,
        title="Dark Energy Evolution",
        description="Dark energy EOS redshift evolution",
        oom=0,
        uncertainty=0.15,
        uncertainty_percent=15.8,
        long_description="The dark energy equation of state evolution parameter: w(a) = w₀ + w_a(1-a). "
                        "Predicted from thermal friction evolution: w_a = -0.95. "
                        "Controls how dark energy density changes with cosmic time.",
        experimental_value=-0.75,
        experimental_error=0.25,
        experimental_source="DESI DR2 (2025)",
        sigma_deviation=0.8,
        derivation="w_a from thermal friction evolution with α_T(z)",
        derivation_formula_ids=["dark-energy-wa", "thermal-time"],
        simulation_file="simulations/wz_evolution_desi_dr2.py",
        used_in_formulas=["dark-energy-wa"],
        depends_on_params=["dark-energy-w0", "thermal-exponent"],
        section_refs=["section-dark-energy", "section-predictions"],
        testable=True,
        testable_by="DESI, Euclid, Roman",
        testable_year=2027,
        version_introduced="v12.0",
        last_updated="v14.1"
    ),

    # === PROTON DECAY ===
    "proton-lifetime": ParameterMetadata(
        id="proton-lifetime",
        value=8.15e34,
        units="years",
        symbol="τ_p",
        status=ParameterCategory.PREDICTED,
        title="Proton Lifetime",
        description="Predicted proton decay lifetime",
        oom=34,
        uncertainty=1.2e34,
        uncertainty_percent=14.7,
        long_description="The predicted proton lifetime from geometric GUT breaking. "
                        "Derived from TCS suppression: τ_p = 8.15×10³⁴ years. "
                        "Super-K bound (2024): τ_p > 1.67×10³⁴ years (p→e⁺π⁰). "
                        "PM prediction is 4.9× above current experimental limit.",
        experimental_value=1.67e34,
        experimental_error=0.0,
        experimental_source="Super-Kamiokande 2024",
        sigma_deviation=5.4,
        derivation="τ_p = τ₀ × (M_GUT/M_Pl)⁴ × S² with geometric suppression",
        derivation_formula_ids=["proton-lifetime", "gut-scale", "tcs-suppression"],
        simulation_file="simulations/proton_decay_geometric_v13_0.py",
        used_in_formulas=["proton-lifetime"],
        depends_on_params=["gut-scale", "gut-coupling", "suppression-factor"],
        section_refs=["section-proton-decay", "section-predictions"],
        testable=True,
        testable_by="Hyper-Kamiokande, JUNO",
        testable_year=2030,
        notes="v14.1: Consolidated to single canonical value (was inconsistent)",
        version_introduced="v14.0",
        last_updated="v14.1"
    ),
}


def get_parameter_by_id(param_id: str) -> Optional[ParameterMetadata]:
    """Retrieve a parameter by its ID."""
    return CORE_PARAMETERS.get(param_id)


def get_all_parameters() -> Dict[str, ParameterMetadata]:
    """Get all registered parameters."""
    return CORE_PARAMETERS.copy()


def export_parameters_to_json() -> List[Dict[str, Any]]:
    """Export all parameters to JSON-serializable format."""
    return [param.to_dict() for param in CORE_PARAMETERS.values()]
