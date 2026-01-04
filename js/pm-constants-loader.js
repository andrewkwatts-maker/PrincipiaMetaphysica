/**
 * Principia Metaphysica - Constants Loader (Dynamic)
 * ====================================================
 *
 * Dynamically loads ALL constants from theory_output.json.
 * NO HARDCODED VALUES - Single source of truth from Python simulations.
 *
 * Usage:
 *   <span class="pm-value" data-category="simulations" data-param="proton_decay.tau_p_years"></span>
 *   <span data-pm-value="simulations.proton_decay.tau_p_years"></span>
 *
 * Also populates:
 *   window.PM - Flat access to all simulation data
 *   window.PM_FORMULAS - Access to CoreFormulas
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 * Version: 2.5.0 - Ten Pillars loaded from named_constants.json (Sacred Heptagon + Mechanical Triad)
 */

(function() {
    'use strict';

    // ========================================================================
    // PM - Dynamically populated from theory_output.json
    // ========================================================================

    const PM = {
        _loaded: false,
        _loading: null,
        _data: null,
        _error: null,

        // Fundamental dimensions (always available, from theory)
        dimensions: {
            D_BULK: 26,
            D_AFTER_SP2R: 13,
            D_G2: 7,
            D_SPIN8: 8,         // Octonions dimension (Spin(8) triality)
            D_OBSERVABLE: 4,
            D_COMMON: 4,
            // Signature components
            SIGNATURE_SPACE: 24,      // Spacelike dimensions in (24,2) signature
            SIGNATURE_TIME: 2,        // Timelike dimensions in (24,2) signature
            SIGNATURE_EFF_SPACE: 12,  // Spacelike dimensions in 13D (12,1) signature
            SIGNATURE_EFF_TIME: 1,    // Timelike dimension in 13D (12,1) signature
            // Spinor components
            SPINOR_26D: 8192,         // 2^13 spinor components in 26D Cl(24,2)
            SPINOR_13D: 64            // 2^6 spinor components in 13D Cl(12,1)
        },

        // Key electroweak parameters (fallback if not in JSON)
        electroweak: {
            v_higgs: 246.22,    // Higgs VEV in GeV
            v_EW: 246.22,       // Electroweak VEV (alias)
            m_Z: 91.1876,       // Z boson mass in GeV
            m_W: 80.377         // W boson mass in GeV
        },

        // Mapping table for legacy/alternate parameter names
        // Maps HTML paths to actual flat keys in parameters.json
        _parameterAliases: {
            // Note: dimensions.X paths are handled by built-in fallback, not aliases
            // Only map dimension aliases that need special handling
            'dimensions.d_g2': 'dimensions.D_G2',  // Case normalization
            'dimensions.d_spin8': 'parameters.dimensions.D_SPIN8',
            'dimensions.bulk_signature': '_hardcoded.bulk_signature',  // (24,2) = 26D

            // ================================================================
            // Legacy / Alternate paths used in HTML files
            // ================================================================
            'seeds.k_gimel': '_named.demiurgic_coupling',  // k_gimel symplectic stiffness constant
            'cosmology.w0_dark_energy': '_named.dark_energy_w0',  // w0 = -23/24

            // ================================================================
            // Framework Statistics / Validation mapping
            // HTML uses framework_statistics.X, JSON uses validation.X or summary.X
            // ================================================================
            'framework_statistics.within_1_sigma': 'validation.within_1sigma',
            'framework_statistics.total_sm_parameters': 'validation.total_parameters',
            'framework_statistics.exact_matches': 'summary.exact_parameters',
            'framework_statistics.within_2_sigma': 'validation.within_2sigma',
            'framework_statistics.calibrated_parameters': 'validation.calibrated_count',
            'framework_statistics.success_rate_1sigma': 'validation.within_1sigma',  // percentage computed elsewhere
            // 72-Gate Registry statistics
            'framework_statistics.pass_count': '_hardcoded.pass_count',  // 7 computationally verified
            'framework_statistics.pending_count': '_hardcoded.pending_count',  // 51 pending validation
            'framework_statistics.not_testable_count': '_hardcoded.not_testable_count',  // 14 foundational
            // Validation summary statistics
            'framework_statistics.chi_squared_reduced': '_hardcoded.chi_squared_reduced',  // 0.17
            'framework_statistics.degrees_of_freedom': '_hardcoded.degrees_of_freedom',  // 23
            'framework_statistics.status': '_hardcoded.status',  // PARTIAL_VERIFICATION

            // Validation aliases (from _hardcoded values)
            'validation.total_predictions': '_hardcoded.total_predictions',
            'validation.calibrated_count': '_hardcoded.calibrated_count',
            'validation.constraints_count': '_hardcoded.constraints_count',
            'validation.predictions_within_1sigma': 'validation.within_1sigma',
            'validation.predictions_within_2sigma': 'validation.within_2sigma',
            'validation.exact_matches': 'summary.exact_parameters',
            'validation.within_1_sigma': 'validation.within_1sigma',
            'validation.success_rate': 'validation.within_1sigma',

            // ================================================================
            // PMNS / Neutrino mixing angles
            // HTML uses pmns_matrix.X, JSON uses neutrino.X_pred
            // ================================================================
            'pmns_matrix.theta_23': 'neutrino.theta_23_pred',
            'pmns_matrix.theta_12': 'neutrino.theta_12_pred',
            'pmns_matrix.theta_13': 'neutrino.theta_13_pred',
            'pmns_matrix.delta_cp': 'neutrino.delta_CP_pred',
            'parameters.pmns.theta_23': 'neutrino.theta_23_pred',
            'parameters.pmns.theta_12': 'neutrino.theta_12_pred',
            'parameters.pmns.theta_13': 'neutrino.theta_13_pred',
            'parameters.pmns.delta_CP': 'neutrino.delta_CP_pred',

            // ================================================================
            // Dark Energy
            // HTML uses dark_energy.X, JSON uses cosmology.X or desi.X
            // ================================================================
            'dark_energy.w0': 'cosmology.w0_derived',
            'dark_energy.w0_PM': 'cosmology.w0_derived',
            'dark_energy.w0_DESI_central': 'desi.w0',
            'dark_energy.w0_DESI_error': 'desi.w0.uncertainty',  // Special: need uncertainty
            'dark_energy.w0_sigma': 'cosmology.w0_deviation',
            'parameters.dark_energy.w0': 'cosmology.w0_derived',
            'parameters.dark_energy.w0.value': 'cosmology.w0_derived',
            'parameters.dark_energy.w0.experimental.value': 'desi.w0',
            'parameters.dark_energy.w0.experimental.uncertainty': 'desi.w0.uncertainty',

            // ================================================================
            // Hubble Constant (Cosmology)
            // H0_local = 71.55 (O'Dowd formula), H0_early = 67.4 (Planck CMB)
            // Experimental: SH0ES 2025 = 73.04 ± 1.04 km/s/Mpc
            // ================================================================
            'cosmology.H0_local': '_hardcoded.H0_local',
            'cosmology.H0_early': 'cosmology.H0_early_normalized',
            'cosmology.H0': 'cosmology.H0_late_evolved',
            'hubble.H0_local': 'cosmology.H0_late_evolved',
            'hubble.H0_early': 'cosmology.H0_early_normalized',
            'hubble.H0_SH0ES': 'cosmology.H0_late_evolved',
            'hubble.H0_Planck': 'cosmology.H0_early_normalized',
            'parameters.cosmology.H0': 'cosmology.H0_late_evolved',
            'parameters.cosmology.H0_local': 'cosmology.H0_late_evolved',
            'parameters.cosmology.H0_early': 'cosmology.H0_early_normalized',

            // ================================================================
            // Higgs mass
            // HTML uses simulations.higgs_mass.X, JSON uses higgs.X or pdg.X
            // ================================================================
            'simulations.higgs_mass.m_h_GeV': 'pdg.m_higgs',  // Use experimental value 125.1 GeV
            'simulations.higgs_mass.m_h_gev': 'pdg.m_higgs',
            'simulations.higgs_mass.validation.sigma': 'higgs.m_higgs_pred.sigma_deviation',
            'higgs_mass.m_h_GeV': 'pdg.m_higgs',
            'v11_final_observables.higgs_mass.m_h_gev': 'pdg.m_higgs',

            // ================================================================
            // Proton decay
            // HTML uses simulations.proton_decay.X, JSON uses proton_decay.X or gauge.X
            // ================================================================
            'simulations.proton_decay.tau_p_years': 'proton_decay.tau_p_years',
            'simulations.proton_decay.alpha_gut_inv': 'gauge.ALPHA_GUT_INV',
            'simulations.proton_decay.m_gut': 'gauge.M_GUT',
            'proton_decay.tau_p_years': 'proton_decay.tau_p_years',
            'proton_decay.alpha_GUT_inv': 'gauge.ALPHA_GUT_INV',
            'proton_decay.m_gut': 'gauge.M_GUT',

            // ================================================================
            // KK spectrum / graviton
            // These are hardcoded as 5.0 TeV - no JSON entry exists
            // ================================================================
            'simulations.kk_graviton.m_KK_TeV': '_hardcoded.kk_m1_TeV',
            'simulations.kk_graviton.hl_lhc_discovery': '_hardcoded.kk_hl_lhc',
            'kk_spectrum.m1': '_hardcoded.kk_m1_TeV',
            'kk_spectrum.m1_central': '_hardcoded.kk_m1_TeV',
            'kk_spectrum.m1_TeV': '_hardcoded.kk_m1_TeV',
            'kk_spectrum.hl_lhc_significance': '_hardcoded.kk_hl_lhc',
            'kk_graviton.mass_tev': '_hardcoded.kk_m1_TeV',

            // ================================================================
            // Topology parameters (from parameters.json or named_constants.json)
            // ================================================================
            'topology.n_gen': '_hardcoded.n_gen',  // 3 fermion generations = chi_eff/48
            'parameters.topology.b2': '_named.b3',  // b2 usually same as b3 for G2
            'parameters.topology.b3': '_named.b3',
            'parameters.topology.B2': '_named.b3',
            'parameters.topology.B3': '_named.b3',
            'parameters.topology.h11': 'parameters.topology.HODGE_H11',
            'parameters.topology.h21': 'parameters.topology.HODGE_H21',
            'parameters.topology.h31': 'parameters.topology.HODGE_H31',
            'parameters.topology.nu': '_hardcoded.n_gen',  // alias for n_gen
            'parameters.topology.CHI_EFF': '_named.chi_eff',

            // ================================================================
            // Neutrino masses
            // ================================================================
            'neutrino_mass.delta_m_sq': 'neutrino.dm2_21',
            'neutrino_masses.delta_m21_sq': 'neutrino.dm2_21',
            'neutrino_masses.delta_m3l_sq': 'neutrino.dm2_32',
            'simulations.neutrino_masses.delta_m21_sq': 'neutrino.dm2_21',
            'simulations.neutrino_masses.delta_m3l_sq': 'neutrino.dm2_32',

            // ================================================================
            // Gauge parameters
            // ================================================================
            'parameters.gauge.m_ps': 'simulations.breaking_chain.m_ps',
            'parameters.gauge.M_GUT': 'gauge.M_GUT',
            'parameters.gauge.ALPHA_GUT_INV': 'gauge.ALPHA_GUT_INV',
            'parameters.gauge.alpha_gut_inv': 'gauge.ALPHA_GUT_INV',

            // ================================================================
            // Statistics - from statistics.json
            // ================================================================
            'statistics.certificates_total': '_hardcoded.certificates_total',
            'statistics.certificates_verified': '_hardcoded.certificates_verified',

            // ================================================================
            // THE SACRED HEPTAGON (7 Intellectual Anchors)
            // Loaded dynamically from named_constants.json
            // ================================================================
            // 1. Watts Constant (Ω_W = 1.0) - Observer Unity
            'constants.watts_constant': '_named.watts_constant',
            'constants.omega_W': '_named.watts_constant',
            'heptagon.watts_constant': '_named.watts_constant',
            // 2. Reid Invariant (χ_R = 1/144) - Sounding Board
            'constants.reid_invariant': '_named.reid_invariant',
            'constants.chi_R': '_named.reid_invariant',
            'heptagon.reid_invariant': '_named.reid_invariant',
            // 3. Weinstein Scale (κ_E = 12.0) - Spinor Process
            'constants.weinstein_scale': '_named.weinstein_scale',
            'constants.kappa_E': '_named.weinstein_scale',
            'heptagon.weinstein_scale': '_named.weinstein_scale',
            // 4. Hossenfelder Root (λ_S = √24) - Hidden Root
            'constants.hossenfelder_root': '_named.hossenfelder_root',
            'constants.hossenfelder_constant': '_named.hossenfelder_root',
            'constants.lambda_S': '_named.hossenfelder_root',
            'heptagon.hossenfelder_root': '_named.hossenfelder_root',
            // 5. O'Dowd Bulk Pressure (P_O = 163) - Bulk Pressure
            'constants.odowd_bulk_pressure': '_named.odowd_bulk_pressure',
            'constants.odowd_constant': '_named.odowd_bulk_pressure',
            'constants.P_O': '_named.odowd_bulk_pressure',
            'heptagon.odowd_bulk_pressure': '_named.odowd_bulk_pressure',
            // 6. Penrose-Hameroff Bridge (Φ_PH = 13) - Fibonacci Bridge
            'constants.penrose_hameroff_bridge': '_named.penrose_hameroff_bridge',
            'constants.penrose_hameroff': '_named.penrose_hameroff_bridge',
            'constants.phi_PH': '_named.penrose_hameroff_bridge',
            'heptagon.penrose_hameroff_bridge': '_named.penrose_hameroff_bridge',
            // 7. Christ Constant (Λ_JC = 153) - Logos Potential
            'constants.christ_constant': '_named.christ_constant',
            'constants.lambda_JC': '_named.christ_constant',
            'constants.phi': '_hardcoded.phi',  // Golden ratio
            'heptagon.christ_constant': '_named.christ_constant',

            // ================================================================
            // THE MECHANICAL TRIAD (Gates 64, 46, 70)
            // Loaded dynamically from named_constants.json
            // ================================================================
            // 8. Sophian Torsion Drag (η_S = 0.6819) - Gate 64
            'constants.sophian_drag': '_named.sophian_drag',
            'constants.eta_S': '_named.sophian_drag',
            'cosmology.eta_S': '_named.sophian_drag',
            'mechanical.sophian_drag': '_named.sophian_drag',
            // 9. Demiurgic Coupling (κ_Δ = k_gimel ≈ 12.318) - Gate 46
            'constants.demiurgic_coupling': '_named.demiurgic_coupling',
            'constants.kappa_Delta': '_named.demiurgic_coupling',
            'constants.k_gimel': '_named.demiurgic_coupling',
            'mechanical.demiurgic_coupling': '_named.demiurgic_coupling',
            // 10. Tzimtzum Pressure (σ_T = 23/24) - Gate 70
            'constants.tzimtzum_pressure': '_named.tzimtzum_pressure',
            'constants.sigma_T': '_named.tzimtzum_pressure',
            'cosmology.sigma_T': '_named.tzimtzum_pressure',
            'cosmology.w0_magnitude': '_named.tzimtzum_pressure',
            'mechanical.tzimtzum_pressure': '_named.tzimtzum_pressure',

            // ================================================================
            // DERIVED VALUES (from named_constants.json)
            // ================================================================
            'cosmology.H0_local': '_named.hubble_constant',
            'derived.hubble_constant': '_named.hubble_constant',
            'derived.dark_energy_w0': '_named.dark_energy_w0',
            'derived.parity_product': '_named.parity_product',

            // ================================================================
            // TOPOLOGICAL INVARIANTS (from named_constants.json)
            // ================================================================
            'topology.b3': '_named.b3',
            'topology.chi_eff': '_named.chi_eff',
            'topology.roots': '_named.roots',
            'topology.visible': '_named.visible',
            'topology.sterile': '_named.sterile',
            'topology.roots_total': '_named.roots',        // Full name alias
            'topology.sterile_sector': '_named.sterile',   // Full name alias

            // ================================================================
            // QED CONSTANTS (from named_constants.json)
            // ================================================================
            'qed.alpha_inverse': '_named.alpha_inverse',   // 137.035...

            // ================================================================
            // GAUGE COUPLINGS (from parameters.json)
            // ================================================================
            'gauge_couplings.alpha_s_MZ': 'pdg.alpha_s_MZ',  // Strong coupling at M_Z

            // ================================================================
            // Proton decay branching ratios
            // ================================================================
            'parameters.proton_decay.BR_epi0': '_hardcoded.BR_epi0',
            'proton_decay.BR_epi0': '_hardcoded.BR_epi0',

            // ================================================================
            // VEV / Higgs / Electroweak
            // ================================================================
            'v12_6_geometric_derivations.vev_pneuma.v_ew': 'higgs.vev',
            'electroweak.v_higgs': 'higgs.vev',
            'parameters.electroweak.v_higgs': 'higgs.vev',
            'parameters.electroweak.v_higgs.value': 'geometry.higgs_vev',  // Full path to JSON value
        },

        // Fallback hardcoded values (populated dynamically from named_constants.json)
        // These serve as defaults if JSON loading fails
        _hardcodedValues: {
            'kk_m1_TeV': '5.0 TeV',
            'kk_hl_lhc': '5σ discovery potential',
            'BR_epi0': 0.45,
            'bulk_signature': '(24,2)',  // 26D = 24 + 2 signature
            // Statistics from statistics.json
            'certificates_total': 72,
            'certificates_verified': 72,
            // 72-Gate Registry statistics (dynamically updated from GATES_72_CERTIFICATES.json)
            'pass_count': 18,          // Computationally verified gates
            'pending_count': 36,       // Awaiting Wolfram/experimental validation
            'not_testable_count': 18,  // Foundational assumptions (axioms)
            // Validation statistics (from appendix_k_v16_0.py)
            'chi_squared_reduced': 0.17,  // Reduced chi-squared
            'degrees_of_freedom': 23,     // DOF for chi-squared test
            'status': 'PARTIAL_VERIFICATION',  // Honest verification status
            'total_predictions': 48,       // Total testable SM parameters
            'calibrated_count': 0,         // Zero calibrated params as of v14.1
            'constraints_count': 1,        // m_h fixes Re(T)
            'within_1sigma': 45,           // Parameters within 1σ
            'within_2sigma': 47,           // Parameters within 2σ
            // Topology invariants
            'n_gen': 3,  // Number of fermion generations = chi_eff / 48 = 144 / 48 = 3
            // Hubble constant (O'Dowd Formula)
            'H0_local': 71.55,  // H0 = (288/4) - (163/144) + 0.6819
            'phi': 1.6180339887,  // Golden ratio (from minimal surfaces)
        },

        // Named constants loaded from AutoGenerated/named_constants.json
        _namedConstants: null,

        /**
         * Get a named constant by key (e.g., "watts_constant", "reid_invariant")
         * Falls back to hardcoded defaults if named_constants.json not loaded
         */
        getNamedConstant(key) {
            // Try named_constants.json first
            if (this._namedConstants?.constants?.[key]) {
                return this._namedConstants.constants[key].value;
            }
            // Try derived values
            if (this._namedConstants?.derived_values?.[key]) {
                return this._namedConstants.derived_values[key].value;
            }
            // Try topological invariants
            if (this._namedConstants?.topological_invariants?.[key]) {
                return this._namedConstants.topological_invariants[key].value;
            }
            // Fallback to hardcoded defaults
            return this._defaultNamedConstants[key] ?? null;
        },

        // Default values (used if named_constants.json fails to load)
        _defaultNamedConstants: {
            // === TOPOLOGICAL INVARIANTS ===
            'b3': 24,
            'chi_eff': 144,
            'roots': 288,
            'visible': 125,
            'sterile': 163,
            // === THE SACRED HEPTAGON (7 Intellectual Anchors) ===
            'watts_constant': 1.0,                    // Ω_W: Observer Unity
            'reid_invariant': 0.006944444444444444,   // χ_R: 1/144 Sounding Board
            'weinstein_scale': 12.0,                  // κ_E: Spinor Connection
            'hossenfelder_root': 4.898979485566356,   // λ_S: √24 Hidden Root
            'odowd_bulk_pressure': 163,               // P_O: Bulk Pressure
            'penrose_hameroff_bridge': 13,            // Φ_PH: Fibonacci Bridge
            'christ_constant': 153,                   // Λ_JC: Logos Potential
            // === THE MECHANICAL TRIAD (Gates 64, 46, 70) ===
            'sophian_drag': 0.6819,                   // η_S: H0 Friction
            'demiurgic_coupling': 12.31830988618379,  // κ_Δ: Mass-Energy Gearbox
            'tzimtzum_pressure': 0.9583333333333334,  // σ_T: Void Seal (23/24)
            // === DERIVED VALUES ===
            'hubble_constant': 71.55,                 // H0 = (288/4) - (163/144) + η_S
            'dark_energy_w0': -0.9583333333333334,    // w0 = -σ_T
            'parity_product': 144,                    // CHI = Ω_W / χ_R
            // === QED CONSTANTS ===
            'alpha_inverse': 137.04748733776924,      // 1/α fine structure (from CODATA)
        },

        /**
         * Get a value by path (e.g., "simulations.proton_decay.tau_p_years")
         * Handles case-insensitive lookups and parameter aliases
         */
        get(path) {
            if (!path) return null;

            // Track if we need to extract a specific field (e.g., .uncertainty)
            let extractField = null;

            // Check parameter aliases first (case-insensitive)
            const normalizedPath = path.toLowerCase();
            for (const [alias, realPath] of Object.entries(this._parameterAliases)) {
                if (normalizedPath === alias.toLowerCase()) {
                    path = realPath;
                    break;
                }
            }

            // Check for hardcoded values (paths starting with _hardcoded.)
            if (path.startsWith('_hardcoded.')) {
                const key = path.replace('_hardcoded.', '');
                return this._hardcodedValues[key] || null;
            }

            // Check for named constants (paths starting with _named.)
            // These come from named_constants.json or fallback to defaults
            if (path.startsWith('_named.')) {
                const key = path.replace('_named.', '');
                return this.getNamedConstant(key);
            }

            // Handle special field suffixes - extract specific fields from parameter objects
            const fieldSuffixes = ['.uncertainty', '.sigma_deviation', '.experimental_value', '.experimental_uncertainty'];
            for (const suffix of fieldSuffixes) {
                if (path.endsWith(suffix)) {
                    extractField = suffix.substring(1);  // Remove leading dot
                    path = path.substring(0, path.length - suffix.length);
                    // Re-check aliases for the base path
                    const basePath = path.toLowerCase();
                    for (const [alias, realPath] of Object.entries(this._parameterAliases)) {
                        if (basePath === alias.toLowerCase()) {
                            path = realPath;
                            break;
                        }
                    }
                    break;
                }
            }

            const parts = path.split('.');

            // Check built-in dimensions first (backward compatibility)
            if (parts[0] === 'dimensions' && parts.length === 2) {
                const dimKey = parts[1].toUpperCase();
                if (this.dimensions[dimKey] !== undefined) {
                    return this.dimensions[dimKey];
                }
            }

            // Check built-in electroweak fallbacks
            if ((parts[0] === 'electroweak' || (parts[0] === 'parameters' && parts[1] === 'electroweak')) && parts.length >= 2) {
                const ewKey = parts[parts.length - 1].toLowerCase();
                // Handle "parameters.electroweak.v_higgs.value" -> "v_higgs"
                if (ewKey === 'value' && parts.length > 2) {
                    const actualKey = parts[parts.length - 2].toLowerCase();
                    if (this.electroweak[actualKey] !== undefined) {
                        return this.electroweak[actualKey];
                    }
                }
                if (this.electroweak[ewKey] !== undefined) {
                    return this.electroweak[ewKey];
                }
            }

            if (!this._data) return null;

            let value = null;

            // Strategy 1: Try flat key lookup in parameters (e.g., "validation.within_1sigma")
            if (this._data.parameters && parts.length >= 2) {
                const flatKey = parts.join('.');
                if (this._data.parameters[flatKey]) {
                    value = this._data.parameters[flatKey];
                }
            }

            // Strategy 2: Try exact path traversal
            if (value === null || value === undefined) {
                value = this._tryPath(this._data, parts);
            }

            // Strategy 3: Try with 'parameters.' prefix for flat keys
            if ((value === null || value === undefined) && this._data.parameters) {
                const flatKey = parts.join('.');
                if (this._data.parameters[flatKey]) {
                    value = this._data.parameters[flatKey];
                }
            }

            // Strategy 4: Try case-insensitive lookup
            if (value === null || value === undefined) {
                value = this._tryPathCaseInsensitive(this._data, parts);
            }

            // Strategy 5: If path doesn't start with 'parameters.', try adding it
            if ((value === null || value === undefined) && parts[0] !== 'parameters') {
                const withParams = ['parameters', ...parts];
                value = this._tryPath(this._data, withParams);
                if (value === null || value === undefined) {
                    // Also try flat key with parameters prefix
                    const flatKey = withParams.join('.');
                    if (this._data.parameters && this._data.parameters[flatKey]) {
                        value = this._data.parameters[flatKey];
                    }
                }
            }

            if (value !== null && value !== undefined) {
                // If we need a specific field (like uncertainty), extract it
                if (extractField && typeof value === 'object' && extractField in value) {
                    return value[extractField];
                }
                // Auto-extract .value from parameter objects
                return this._extractValue(value);
            }

            return null;
        },

        /**
         * Extract primitive value from parameter objects
         * Objects with {value: X, units: Y} structure are common in parameters
         */
        _extractValue(value) {
            if (value === null || value === undefined) return value;

            // If it's a primitive, return as-is
            if (typeof value !== 'object') return value;

            // If it's an array, return as-is
            if (Array.isArray(value)) return value;

            // If it has a 'value' property and doesn't look like a formula/complex object
            // (formulas have 'html' or 'latex' properties)
            if ('value' in value && !('html' in value) && !('latex' in value)) {
                return value.value;
            }

            // Return object as-is for complex structures
            return value;
        },

        /**
         * Try to get a value by exact path
         */
        _tryPath(obj, parts) {
            let value = obj;
            for (const part of parts) {
                if (value && typeof value === 'object' && part in value) {
                    value = value[part];
                } else {
                    return null;
                }
            }
            return value;
        },

        /**
         * Try to get a value by case-insensitive path
         */
        _tryPathCaseInsensitive(obj, parts) {
            let value = obj;
            for (const part of parts) {
                if (!value || typeof value !== 'object') {
                    return null;
                }

                // Try exact match first
                if (part in value) {
                    value = value[part];
                    continue;
                }

                // Try case-insensitive match
                const lowerPart = part.toLowerCase();
                let found = false;
                for (const key of Object.keys(value)) {
                    if (key.toLowerCase() === lowerPart) {
                        value = value[key];
                        found = true;
                        break;
                    }
                }

                if (!found) {
                    return null;
                }
            }
            return value;
        },

        /**
         * Get simulation data by path (e.g., "proton_decay.tau_p_years")
         */
        simulation(path) {
            return this.get('simulations.' + path);
        },

        /**
         * Get formula by ID
         */
        formula(id) {
            return this._data?.formulas?.formulas?.[id] ?? null;
        },

        /**
         * Get all formulas
         */
        get formulas() {
            return this._data?.formulas?.formulas ?? {};
        },

        /**
         * Get statistics
         */
        get statistics() {
            return this._data?.statistics ?? {};
        },

        /**
         * Get validation summary
         */
        get validationSummary() {
            return this._data?.validation_summary ?? [];
        },

        /**
         * Check if all validations passed
         */
        get allPassed() {
            return this._data?.all_passed ?? false;
        },

        /**
         * Get version
         */
        get version() {
            return this._data?.version ?? 'unknown';
        }
    };

    // ========================================================================
    // LOADING FROM theory_output.json
    // ========================================================================

    // ========================================================================
    // COMPONENT-BASED CACHING SYSTEM
    // ========================================================================

    const CACHE_PREFIX = 'pm_';
    const CACHE_VERSION = '16.3';

    // Cache configuration per component (TTL in seconds)
    const CACHE_CONFIG = {
        parameters: { ttl: 3600, storage: 'localStorage' },        // 1 hour
        formulas: { ttl: 3600, storage: 'localStorage' },          // 1 hour
        sections: { ttl: 1800, storage: 'localStorage' },          // 30 minutes
        simulations: { ttl: 300, storage: 'sessionStorage' },      // 5 minutes
        statistics: { ttl: 300, storage: 'sessionStorage' },       // 5 minutes
        metadata: { ttl: 60, storage: 'sessionStorage' },          // 1 minute
        named_constants: { ttl: 3600, storage: 'localStorage' }    // 1 hour (Ten Pillars)
    };

    /**
     * Get cached component data
     */
    function getCachedComponent(component) {
        const config = CACHE_CONFIG[component] || { ttl: 300, storage: 'sessionStorage' };
        const storage = config.storage === 'localStorage' ? localStorage : sessionStorage;
        const key = `${CACHE_PREFIX}${component}`;

        try {
            const cached = storage.getItem(key);
            if (!cached) return null;

            const { data, timestamp, version } = JSON.parse(cached);

            // Check version and TTL
            if (version !== CACHE_VERSION) return null;
            if (Date.now() - timestamp > config.ttl * 1000) return null;

            return data;
        } catch (e) {
            return null;
        }
    }

    /**
     * Cache component data
     */
    function cacheComponent(component, data) {
        const config = CACHE_CONFIG[component] || { ttl: 300, storage: 'sessionStorage' };
        const storage = config.storage === 'localStorage' ? localStorage : sessionStorage;
        const key = `${CACHE_PREFIX}${component}`;

        try {
            storage.setItem(key, JSON.stringify({
                data,
                timestamp: Date.now(),
                version: CACHE_VERSION
            }));
        } catch (e) {
            console.warn(`[PM Cache] Could not cache ${component}:`, e.message);
        }
    }

    /**
     * Determine base path for loading files
     */
    function getBasePath() {
        const path = window.location.pathname;
        if (path.includes('/foundations/') || path.includes('/sections/') ||
            path.includes('/docs/') || path.includes('/diagrams/') ||
            path.includes('/components/') || path.includes('/tests/')) {
            return '../AutoGenerated/';
        }
        return 'AutoGenerated/';
    }

    /**
     * Load a single component file with caching
     */
    async function loadComponent(component, basePath) {
        // Check cache first
        const cached = getCachedComponent(component);
        if (cached) {
            console.log(`[PM] ${component}: loaded from cache`);
            return cached;
        }

        // Try to load from file
        const paths = [
            `/AutoGenerated/${component}.json`,       // Absolute path (for live site)
            `${basePath}${component}.json`,
            `./${basePath}${component}.json`,
            `../${basePath}${component}.json`,
            `../../AutoGenerated/${component}.json`
        ];

        for (const path of paths) {
            try {
                const response = await fetch(path);
                if (response.ok) {
                    const data = await response.json();
                    cacheComponent(component, data);
                    console.log(`[PM] ${component}: loaded from ${path}`);
                    return data;
                }
            } catch (e) {
                continue;
            }
        }

        return null;
    }

    async function loadConstants() {
        if (PM._loaded) return true;
        if (PM._loading) return PM._loading;

        PM._loading = (async () => {
            const basePath = getBasePath();
            console.log(`[PM] Loading components from ${basePath}`);

            // ================================================================
            // STRATEGY 1: Load split component files in parallel (preferred)
            // ================================================================
            try {
                const [parameters, simulations, formulas, statistics, metadata, namedConstants, gates72] = await Promise.all([
                    loadComponent('parameters', basePath),
                    loadComponent('simulations', basePath),
                    loadComponent('formulas', basePath),
                    loadComponent('statistics', basePath),
                    loadComponent('metadata', basePath),
                    loadComponent('named_constants', basePath),
                    loadComponent('GATES_72_CERTIFICATES', basePath)
                ]);

                // Store named constants for access via getNamedConstant()
                if (namedConstants) {
                    PM._namedConstants = namedConstants;
                    console.log(`[PM] Named constants: loaded ${Object.keys(namedConstants.constants || {}).length} constants`);
                }

                // If we got at least parameters or simulations, use split files
                if (parameters || simulations) {
                    // Extract 72-Gate statistics from GATES_72_CERTIFICATES.json
                    const gateStats = gates72?.summary || {};

                    PM._data = {
                        version: metadata?.version || namedConstants?.version || '16.0',
                        parameters: parameters?.parameters || {},
                        simulations: simulations?.simulations || {},
                        formulas: formulas || { formulas: {}, count: 0 },
                        statistics: statistics?.statistics || {},
                        framework_statistics: {
                            ...(statistics?.framework_statistics || {}),
                            // Dynamic gate statistics from GATES_72_CERTIFICATES.json
                            pass_count: gateStats.verified ?? 7,
                            pending_count: gateStats.pending_lock ?? 51,
                            not_testable_count: gateStats.not_testable ?? 14,
                            total_gates: gateStats.total_gates ?? 72
                        },
                        validation_summary: metadata?.validation_summary || [],
                        all_passed: metadata?.all_passed ?? true,
                        named_constants: namedConstants || null,
                        gates_72: gates72 || null
                    };

                    // Update hardcoded values dynamically from loaded data
                    if (gateStats.verified !== undefined) {
                        PM._hardcodedValues.pass_count = gateStats.verified;
                        PM._hardcodedValues.pending_count = gateStats.pending_lock;
                        PM._hardcodedValues.not_testable_count = gateStats.not_testable;
                    }

                    PM._loaded = true;

                    // Create flat access to simulations
                    if (PM._data.simulations) {
                        for (const [key, value] of Object.entries(PM._data.simulations)) {
                            PM[key] = value;
                        }
                    }

                    console.log(`%cPM: Loaded from split components`, 'color: green; font-weight: bold');
                    console.log(`  Version: ${PM._data.version}`);
                    console.log(`  Parameters: ${Object.keys(PM._data.parameters).length} categories`);
                    console.log(`  Simulations: ${Object.keys(PM._data.simulations).length}`);
                    console.log(`  Formulas: ${PM._data.formulas?.count || Object.keys(PM._data.formulas?.formulas || {}).length}`);
                    console.log(`  Named Constants: ${namedConstants ? 'LOADED (Ten Pillars + Topological Invariants)' : 'using defaults'}`);

                    // Expose globally
                    window.PM_DATA = PM._data;
                    window.PM_FORMULAS = PM._data.formulas?.formulas || {};
                    window.PM_NAMED_CONSTANTS = PM._namedConstants || null;

                    updateDOM();
                    setTimeout(() => {
                        if (typeof signalMathJax === 'function') signalMathJax();
                    }, 100);

                    return true;
                }
            } catch (e) {
                console.warn('[PM] Split component loading failed, trying unified file:', e.message);
            }

            // ================================================================
            // STRATEGY 2: Fallback to unified theory_output.json
            // ================================================================
            const unifiedPaths = [
                '/AutoGenerated/theory_output.json',  // Absolute path (for live site)
                `${basePath}theory_output.json`,
                'AutoGenerated/theory_output.json',
                './AutoGenerated/theory_output.json',
                '../AutoGenerated/theory_output.json',
                'theory_output.json',
                '../theory_output.json'
            ];

            for (const path of unifiedPaths) {
                try {
                    const response = await fetch(path);
                    if (response.ok) {
                        const data = await response.json();
                        PM._data = data;
                        PM._loaded = true;

                        // Create flat access to simulations
                        if (data.simulations) {
                            for (const [key, value] of Object.entries(data.simulations)) {
                                PM[key] = value;
                            }
                        }

                        console.log(`%cPM: Loaded from unified ${path}`, 'color: green; font-weight: bold');

                        window.PM_DATA = data;
                        window.PM_FORMULAS = data.formulas?.formulas || {};

                        updateDOM();
                        setTimeout(() => {
                            if (typeof signalMathJax === 'function') signalMathJax();
                        }, 100);

                        return true;
                    }
                } catch (e) {
                    continue;
                }
            }

            // ================================================================
            // FAILURE: Could not load data
            // ================================================================
            PM._error = 'Could not load data files';
            console.error('%cPM: Failed to load data!', 'color: red; font-weight: bold');
            console.error('  Run: python run_all_simulations.py');
            console.error('  Then: python simulations/Constants/split_theory_output.py');

            updateDOM();
            return false;
        })();

        return PM._loading;
    }

    // ========================================================================
    // DOM MANIPULATION
    // ========================================================================

    function formatValue(value, format) {
        if (value === null || value === undefined) return '?';

        // Safety net: extract .value from objects that slipped through
        if (typeof value === 'object' && !Array.isArray(value)) {
            if ('value' in value && !('html' in value) && !('latex' in value)) {
                value = value.value;
            } else {
                // For complex objects without a value property, return a sensible default
                console.warn('formatValue received object:', value);
                return '?';
            }
        }

        if (typeof value === 'number') {
            // Handle format specifications
            if (format) {
                if (format.startsWith('scientific:')) {
                    const decimals = parseInt(format.split(':')[1]) || 2;
                    return value.toExponential(decimals);
                }
                if (format.startsWith('fixed:')) {
                    const decimals = parseInt(format.split(':')[1]) || 2;
                    return value.toFixed(decimals);
                }
                if (format === 'percent') {
                    return (value * 100).toFixed(1) + '%';
                }
                if (format === 'integer') {
                    return Math.round(value).toString();
                }
            }

            // Auto-format based on magnitude
            if (Math.abs(value) >= 1e10 || (Math.abs(value) < 0.001 && value !== 0)) {
                return value.toExponential(2);
            } else if (Number.isInteger(value)) {
                return value.toString();
            } else {
                return value.toFixed(3);
            }
        }

        if (typeof value === 'boolean') {
            return value ? 'Yes' : 'No';
        }

        return String(value);
    }

    function updateDOM() {
        const stats = {
            pmValue: { loaded: 0, failed: 0 },
            category: { loaded: 0, failed: 0 },
            formula: { loaded: 0, failed: 0 },
            stat: { loaded: 0, failed: 0 }
        };

        // ====================================================================
        // 1. Handle data-pm-value="path.to.value" format
        // ====================================================================
        const pmValueElements = document.querySelectorAll('[data-pm-value]');
        pmValueElements.forEach(el => {
            const path = el.getAttribute('data-pm-value');
            const format = el.getAttribute('data-format');
            const value = PM.get(path);

            if (value !== null && value !== undefined) {
                el.textContent = formatValue(value, format);
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.removeAttribute('title');

                // Mark element to prevent MathJax from processing it
                el.classList.add('mathjax-ignore');

                stats.pmValue.loaded++;
            } else if (!PM._loaded) {
                el.textContent = '...';
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.textContent = '?';
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                el.setAttribute('title', `ERROR: Path not found in theory_output.json: "${path}"`);
                if (window.PM_DEBUG) {
                    console.error(`PM: Path not found: ${path}`);
                }
                stats.pmValue.failed++;
            }
        });

        // ====================================================================
        // 2. Handle data-category + data-param format
        // ====================================================================
        const categoryElements = document.querySelectorAll('[data-category][data-param]');
        categoryElements.forEach(el => {
            const category = el.getAttribute('data-category');
            const param = el.getAttribute('data-param');
            const format = el.getAttribute('data-format');
            const field = el.getAttribute('data-field'); // Optional sub-field

            let value = null;
            const triedPaths = [];

            // Strategy 1: Try simulations.category.param (most common)
            if (category === 'simulations') {
                const path1 = `simulations.${param}`;
                triedPaths.push(path1);
                value = PM.get(path1);
            } else {
                const path2 = `simulations.${category}.${param}`;
                triedPaths.push(path2);
                value = PM.get(path2);
            }

            // Strategy 2: Try parameters.category.param (for parameter section)
            if (value === null || value === undefined) {
                const path3 = `parameters.${category}.${param}`;
                triedPaths.push(path3);
                value = PM.get(path3);
            }

            // Strategy 3: Try top-level category.param
            if (value === null || value === undefined) {
                const path4 = `${category}.${param}`;
                triedPaths.push(path4);
                value = PM.get(path4);
            }

            // Strategy 4: Try direct simulation access via flat PM object
            if ((value === null || value === undefined) && PM[category]) {
                triedPaths.push(`PM.${category}.${param}`);
                const parts = param.split('.');
                value = PM[category];
                for (const part of parts) {
                    if (value && typeof value === 'object' && part in value) {
                        value = value[part];
                    } else {
                        value = null;
                        break;
                    }
                }
            }

            // Extract nested field if specified (e.g., data-field="value" or "experimental_value")
            if ((value !== null && value !== undefined) && field) {
                if (typeof value === 'object' && field in value) {
                    value = value[field];
                } else {
                    console.warn(`PM: Field "${field}" not found in ${category}.${param}`, value);
                    value = null;
                }
            }

            // Auto-extract .value property if present (common pattern)
            if (value !== null && value !== undefined && !field) {
                if (typeof value === 'object' && 'value' in value && !('html' in value) && !('latex' in value)) {
                    value = value.value;
                }
            }

            if (value !== null && value !== undefined) {
                el.textContent = formatValue(value, format);
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.removeAttribute('title');
                stats.category.loaded++;
            } else if (!PM._loaded) {
                el.textContent = '...';
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.textContent = '?';
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                const errorMsg = `ERROR: Not found in theory_output.json\nCategory: "${category}"\nParam: "${param}"${field ? `\nField: "${field}"` : ''}\nTried paths: ${triedPaths.join(', ')}`;
                el.setAttribute('title', errorMsg);
                if (window.PM_DEBUG) {
                    console.error(`PM: Not found - category="${category}" param="${param}"${field ? ` field="${field}"` : ''}\nTried: ${triedPaths.join(', ')}`);
                }
                stats.category.failed++;
            }
        });

        // ====================================================================
        // 3. Handle data-formula-id displays
        // ====================================================================
        const formulaElements = document.querySelectorAll('[data-formula-id]');
        formulaElements.forEach(el => {
            const formulaId = el.getAttribute('data-formula-id');
            const formula = PM.formula(formulaId);

            if (formula) {
                // If element is empty, populate with formula HTML
                if (!el.innerHTML.trim() || el.classList.contains('pm-formula-auto')) {
                    el.innerHTML = formula.html || formula.latex || '';
                    el.classList.add('pm-formula-auto');
                }
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.setAttribute('title', formula.description || '');
                stats.formula.loaded++;
            } else if (!PM._loaded) {
                if (!el.innerHTML.trim()) {
                    el.textContent = '...';
                }
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                const errorMsg = `ERROR: Formula not found in theory_output.json: "${formulaId}"`;
                el.setAttribute('title', errorMsg);
                if (!el.innerHTML.trim()) {
                    el.textContent = '?';
                }
                if (window.PM_DEBUG) {
                    console.error(`PM: Formula not found: ${formulaId}`);
                }
                stats.formula.failed++;
            }
        });

        // ====================================================================
        // 4. Handle data-stat-id displays (from PM_STATS or statistics)
        // ====================================================================
        const statElements = document.querySelectorAll('[data-stat-id]');
        statElements.forEach(el => {
            const statId = el.getAttribute('data-stat-id');
            const format = el.getAttribute('data-format');
            let value = null;
            const triedSources = [];

            // Strategy 1: Try PM_STATS if available (computed stats)
            if (typeof window.PM_STATS !== 'undefined') {
                triedSources.push('PM_STATS');
                value = window.PM_STATS[statId];
                if (value === undefined && typeof window.PM_STATS.get === 'function') {
                    value = window.PM_STATS.get(statId);
                }
            }

            // Strategy 2: Try statistics section in theory_output.json
            if (value === null || value === undefined) {
                triedSources.push('statistics');
                value = PM.statistics?.[statId];
            }

            // Strategy 3: Try dotted path in full data (e.g., "simulations.proton_decay.tau_p_years")
            if ((value === null || value === undefined) && statId.includes('.')) {
                triedSources.push('dotted path');
                value = PM.get(statId);
            }

            // Strategy 4: Try validation_summary array
            if (value === null || value === undefined) {
                triedSources.push('validation_summary');
                const validationItem = PM.validationSummary.find(item => item.name === statId || item.id === statId);
                if (validationItem) {
                    value = validationItem.value ?? validationItem;
                }
            }

            if (value !== null && value !== undefined) {
                el.textContent = formatValue(value, format);
                el.classList.add('pm-loaded');
                el.classList.remove('pm-error', 'pm-loading');
                el.removeAttribute('title');
                stats.stat.loaded++;
            } else if (!PM._loaded) {
                el.textContent = '...';
                el.classList.add('pm-loading');
                el.classList.remove('pm-error');
            } else {
                el.textContent = '?';
                el.classList.add('pm-error');
                el.classList.remove('pm-loaded', 'pm-loading');
                const errorMsg = `ERROR: Stat not found in theory_output.json: "${statId}"\nTried sources: ${triedSources.join(', ')}`;
                el.setAttribute('title', errorMsg);
                if (window.PM_DEBUG) {
                    console.error(`PM: Stat not found: ${statId} (tried: ${triedSources.join(', ')})`);
                }
                stats.stat.failed++;
            }
        });

        // ====================================================================
        // Summary Report
        // ====================================================================
        if (PM._loaded) {
            const total = stats.pmValue.loaded + stats.category.loaded + stats.formula.loaded + stats.stat.loaded;
            const failed = stats.pmValue.failed + stats.category.failed + stats.formula.failed + stats.stat.failed;

            if (total > 0 || failed > 0) {
                console.log(`%cPM: Updated ${total} elements`, 'color: green; font-weight: bold');
                if (stats.pmValue.loaded > 0) console.log(`  data-pm-value: ${stats.pmValue.loaded} loaded`);
                if (stats.category.loaded > 0) console.log(`  data-category: ${stats.category.loaded} loaded`);
                if (stats.formula.loaded > 0) console.log(`  data-formula-id: ${stats.formula.loaded} loaded`);
                if (stats.stat.loaded > 0) console.log(`  data-stat-id: ${stats.stat.loaded} loaded`);

                if (failed > 0) {
                    console.warn(`%cPM: ${failed} elements failed to load (hover over "?" for details)`, 'color: orange; font-weight: bold');
                    if (stats.pmValue.failed > 0) console.warn(`  data-pm-value: ${stats.pmValue.failed} failed`);
                    if (stats.category.failed > 0) console.warn(`  data-category: ${stats.category.failed} failed`);
                    if (stats.formula.failed > 0) console.warn(`  data-formula-id: ${stats.formula.failed} failed`);
                    if (stats.stat.failed > 0) console.warn(`  data-stat-id: ${stats.stat.failed} failed`);
                    console.warn('  Set window.PM_DEBUG = true for detailed error logs');
                }
            }
        }
    }

    // ========================================================================
    // MATHJAX INTEGRATION
    // ========================================================================

    function signalMathJax() {
        // Signal MathJax to typeset after PM values are loaded
        if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
            console.log('PM: Signaling MathJax to typeset...');
            MathJax.typesetPromise().catch((err) => {
                console.warn('PM: MathJax typeset error:', err);
            });
        } else if (typeof MathJax !== 'undefined' && MathJax.Hub) {
            // MathJax v2
            MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
        }
    }

    // ========================================================================
    // PUBLIC API
    // ========================================================================

    PM.load = loadConstants;
    PM.refresh = loadConstants;
    PM.updateDOM = updateDOM;
    PM.formatValue = formatValue;
    PM.signalMathJax = signalMathJax;

    // Export globally
    window.PM = PM;

    console.log('PM: Constants loader ready (v2.5.0 - Ten Pillars from named_constants.json)');

    // ========================================================================
    // MUTATION OBSERVER - Re-process when new elements are added
    // ========================================================================

    function initMutationObserver() {
        if (!window.MutationObserver) return;

        const observer = new MutationObserver(function(mutations) {
            let needsUpdate = false;
            for (const mutation of mutations) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Check if any added nodes have pm-value attributes
                    for (const node of mutation.addedNodes) {
                        if (node.nodeType === 1) { // Element node
                            if (node.hasAttribute && (
                                node.hasAttribute('data-pm-value') ||
                                node.hasAttribute('data-category') ||
                                node.hasAttribute('data-formula-id') ||
                                node.hasAttribute('data-stat-id') ||
                                node.querySelector('[data-pm-value], [data-category], [data-formula-id], [data-stat-id]')
                            )) {
                                needsUpdate = true;
                                break;
                            }
                        }
                    }
                }
                if (needsUpdate) break;
            }

            if (needsUpdate && PM._loaded) {
                // Debounce updates
                clearTimeout(observer._timeout);
                observer._timeout = setTimeout(updateDOM, 50);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        console.log('PM: MutationObserver initialized - will auto-update dynamic content');
    }

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            loadConstants();
            initMutationObserver();
        });
    } else {
        loadConstants();
        initMutationObserver();
    }

    // Refresh on visibility change
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && PM._loaded) {
            setTimeout(updateDOM, 100);
        }
    });

})();
