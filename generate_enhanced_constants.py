#!/usr/bin/env python3
"""
Generate Enhanced Theory Constants with Rich Metadata
=====================================================

Creates theory-constants.js with full metadata for each constant:
- Value and display format
- Formula/derivation
- Uncertainties and error bars
- Experimental values and agreement
- Source traceability
- Hover tooltip data

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import numpy as np
import config
from datetime import datetime

def create_enhanced_constant(value, **metadata):
    """Create a constant entry with full metadata"""
    result = {
        'value': float(value) if not isinstance(value, str) else value,
    }
    result.update(metadata)
    return result

def generate_enhanced_constants():
    """Generate theory-constants.js with rich metadata"""

    # Load simulation results
    try:
        with open('theory_output.json', 'r') as f:
            sim_data = json.load(f)
    except FileNotFoundError:
        print("Warning: theory_output.json not found, using config values only")
        sim_data = {}

    constants = {
        'meta': {
            'version': '8.4',
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'description': 'Enhanced theory constants with full metadata - v8.4 with CKM rotation and TCS cycle orientations',
            'has_metadata': True,
            'hover_enabled': True
        },

        'dimensions': {
            'D_bulk': create_enhanced_constant(
                config.FundamentalConstants.D_BULK,
                unit='dimensions',
                display='26',
                description='Bosonic string critical dimension',
                formula='D = 26 from Virasoro anomaly cancellation',
                derivation='String theory consistency',
                source='fundamental',
                references=['Polchinski Vol 1']
            ),
            'D_after_sp2r': create_enhanced_constant(
                config.FundamentalConstants.D_AFTER_SP2R,
                unit='dimensions',
                display='13',
                description='After Sp(2,R) gauge fixing',
                formula='26D → 13D shadow via two-time projection',
                derivation='Sp(2,R) gauge symmetry',
                source='geometric',
                references=['Bars 2000']
            ),
            # Add more dimensions...
        },

        'topology': {
            'chi_eff': create_enhanced_constant(
                config.FundamentalConstants.euler_characteristic_effective(),
                unit='dimensionless',
                display='144',
                description='Effective Euler characteristic',
                formula='χ_eff = 144 from TCS G₂ construction',
                derivation='Flux quantization on TCS manifold',
                source='geometric',
                references=['Corti et al 2013']
            ),
            'b3': create_enhanced_constant(
                24,
                unit='dimensionless',
                display='24',
                description='Number of coassociative 4-cycles',
                formula='b₃ = 24 from TCS matching',
                derivation='G₂ cohomology',
                source='geometric',
                references=['CHNP 2018']
            ),
            'n_gen': create_enhanced_constant(
                config.FundamentalConstants.fermion_generations(),
                unit='generations',
                display='3',
                description='Number of fermion generations',
                formula='n_gen = χ_eff / 48 = 144 / 48',
                derivation='Index theorem on G₂ manifold',
                source='geometric:exact',
                experimental_value=3,
                experimental_source='PDG 2024',
                agreement_sigma=0.00,
                agreement_text='EXACT MATCH',
                references=['PDG 2024']
            ),
        },

        'shared_dimensions': {
            'alpha_4': create_enhanced_constant(
                config.SharedDimensionsParameters.ALPHA_4,
                unit='dimensionless',
                display='0.956',
                uncertainty=0.01,
                description='4th dimension coupling strength',
                formula='From TCS torsion: (Σ+Δ)/2 with Σ=1.178, Δ=0.733',
                derivation='G₂ torsion logarithms + θ₂₃ matching',
                source='geometric',
                references=['PM Section 3.7a']
            ),
            'alpha_5': create_enhanced_constant(
                config.SharedDimensionsParameters.ALPHA_5,
                unit='dimensionless',
                display='0.222',
                uncertainty=0.01,
                description='5th dimension coupling strength',
                formula='From TCS torsion: (Σ-Δ)/2 with Σ=1.178, Δ=0.733',
                derivation='G₂ torsion logarithms + θ₂₃ matching',
                source='geometric',
                references=['PM Section 3.7a']
            ),
            'd_eff': create_enhanced_constant(
                config.SharedDimensionsParameters.D_EFF,
                unit='dimensions',
                display='12.589',
                uncertainty=0.01,
                description='Effective quantum-corrected dimension',
                formula='D_eff = 12 + 0.5×(α₄+α₅)',
                derivation='Shared dimension coupling + quantum corrections',
                source='geometric',
                references=['PM Section 6']
            ),
        },

        'proton_decay': {},
        'pmns_matrix': {},
        'dark_energy': {},
        'kk_spectrum': {},
        'neutrino_mass_ordering': {},
        'proton_decay_channels': {},
        'planck_tension': {}
    }

    # Add proton decay with simulation data
    if 'proton_decay' in sim_data:
        pd = sim_data['proton_decay']
        constants['proton_decay'] = {
            'M_GUT': create_enhanced_constant(
                pd.get('M_GUT', config.GaugeUnificationParameters.M_GUT),
                unit='GeV',
                display='2.118×10¹⁶',
                uncertainty=pd.get('M_GUT_error', 0.09e16),
                uncertainty_percent=pd.get('M_GUT_percent_error', 4.25),
                description='Grand Unification scale',
                formula='M_GUT = M_base × (1 + c_warp × s)',
                derivation='TCS G₂ torsion logarithms: T_ω=-0.884, s=1.178, c_warp=0.15',
                source='simulation:proton_decay_rg_hybrid',
                references=['Acharya-Witten 2001', 'PM Section 3.7a']
            ),
            'tau_p_median': create_enhanced_constant(
                pd.get('tau_p_median', config.PhenomenologyParameters.TAU_PROTON),
                unit='years',
                display='3.84×10³⁴',
                uncertainty_lower=pd.get('tau_p_lower_68', 2.41e34),
                uncertainty_upper=pd.get('tau_p_upper_68', 5.61e34),
                uncertainty_oom=pd.get('tau_p_uncertainty_oom', 0.177),
                confidence_level='68%',
                description='Proton lifetime (Monte Carlo median)',
                formula='τ_p = 3.82×10³³ × (M_GUT/10¹⁶)⁴ × (0.03/α_GUT)²',
                derivation='Monte Carlo (1000 samples) with 3-loop RG + KK thresholds',
                source='simulation:proton_decay_rg_hybrid',
                experimental_bound=1.67e34,
                experimental_source='Super-K 2024',
                agreement='2.3× above bound',
                testable='Hyper-K 2030s',
                references=['PDG 2024', 'Super-K Collaboration']
            ),
            'uncertainty_oom': create_enhanced_constant(
                pd.get('tau_p_uncertainty_oom', 0.177),
                unit='OOM',
                display='0.177',
                description='Proton decay uncertainty in orders of magnitude',
                formula='OOM = log₁₀(upper_68/lower_68) / 2',
                derivation='Monte Carlo 68% confidence interval width',
                source='simulation:proton_decay_rg_hybrid',
                references=['PM v7.0: 4.5× improvement from 0.8 OOM']
            ),
        }

    # Add gauge unification category
    if 'proton_decay' in sim_data:
        pd = sim_data['proton_decay']
        constants['gauge_unification'] = {
            'alpha_GUT_inv': create_enhanced_constant(
                pd.get('alpha_GUT_inv', config.GaugeUnificationParameters.ALPHA_GUT_INV),
                unit='dimensionless',
                display='23.54',
                uncertainty=0.5,
                description='Inverse GUT coupling constant',
                formula='1/α_GUT from 3-loop RG + KK thresholds at 5 TeV',
                derivation='Renormalization group running from M_Z to M_GUT',
                source='simulation:proton_decay_rg_hybrid',
                references=['Acharya 2004', 'Improved from 24.68 to 23.54 in v7.0']
            ),
            'unification_precision': create_enhanced_constant(
                0.953,
                unit='fraction',
                display='95.3%',
                description='Gauge coupling unification precision',
                formula='Relative agreement of SU(3), SU(2), U(1) at M_GUT',
                derivation='3-loop RG with threshold corrections',
                source='simulation:gauge_unification',
                references=['PM Section 3']
            ),
        }

    # Add X,Y heavy gauge bosons
    constants['xy_bosons'] = {
        'M_X': create_enhanced_constant(
            config.XYGaugeBosonParameters.M_X,
            unit='GeV',
            display='2.118×10¹⁶',
            uncertainty=config.XYGaugeBosonParameters.M_X_ERROR,
            description='X boson mass (heavy gauge boson)',
            formula='M_X = M_GUT from SO(10) symmetry',
            derivation='Geometrically derived from TCS G₂ torsion',
            source='geometric:M_GUT',
            charge=config.XYGaugeBosonParameters.CHARGE_X,
            charge_display='±4/3 e',
            references=['Acharya-Witten 2001', 'SO(10) GUT']
        ),
        'M_Y': create_enhanced_constant(
            config.XYGaugeBosonParameters.M_Y,
            unit='GeV',
            display='2.118×10¹⁶',
            uncertainty=config.XYGaugeBosonParameters.M_Y_ERROR,
            description='Y boson mass (heavy gauge boson)',
            formula='M_Y = M_GUT from SO(10) symmetry',
            derivation='Assumed degenerate with M_X (mass splitting unknown)',
            source='geometric:M_GUT',
            charge=config.XYGaugeBosonParameters.CHARGE_Y,
            charge_display='±1/3 e',
            references=['Acharya-Witten 2001', 'SO(10) GUT']
        ),
        'alpha_GUT': create_enhanced_constant(
            config.XYGaugeBosonParameters.ALPHA_GUT,
            unit='dimensionless',
            display='0.0425',
            description='GUT coupling strength (fine structure at M_GUT)',
            formula='α_GUT = 1/23.54',
            derivation='3-loop RG running from M_Z to M_GUT',
            source='simulation:gauge_unification',
            references=['PM Section 3']
        ),
        'tau_estimate': create_enhanced_constant(
            1e-41,
            unit='seconds',
            display='~10⁻⁴¹ s',
            description='X,Y boson lifetime (theoretical estimate)',
            formula='τ ~ ℏ/M_GUT',
            derivation='Order of magnitude from decay width estimate',
            source='theoretical_estimate',
            uncertainty_type='order_of_magnitude',
            references=['Standard GUT phenomenology']
        ),
        'N_total': create_enhanced_constant(
            config.XYGaugeBosonParameters.N_TOTAL_BOSONS,
            unit='bosons',
            display='45',
            description='Total SO(10) gauge bosons',
            formula='dim[SO(10) adjoint] = 45',
            derivation='SO(10) Lie algebra dimension',
            source='group_theory',
            fixed=True,
            references=['Georgi-Glashow 1974']
        ),
        'N_X': create_enhanced_constant(
            config.XYGaugeBosonParameters.N_X_BOSONS,
            unit='bosons',
            display='12',
            description='Number of X-type bosons (charge ±4/3)',
            formula='From SO(10) representation decomposition',
            derivation='SO(10) → SU(5) → SM breaking pattern',
            source='group_theory',
            fixed=True,
            references=['SO(10) GUT literature']
        ),
        'N_Y': create_enhanced_constant(
            config.XYGaugeBosonParameters.N_Y_BOSONS,
            unit='bosons',
            display='12',
            description='Number of Y-type bosons (charge ±1/3)',
            formula='From SO(10) representation decomposition',
            derivation='SO(10) → SU(5) → SM breaking pattern',
            source='group_theory',
            fixed=True,
            references=['SO(10) GUT literature']
        ),
    }

    # Add PMNS matrix with simulation data
    if 'pmns_matrix' in sim_data and 'pmns_nufit_comparison' in sim_data:
        pm = sim_data['pmns_matrix']
        nf = sim_data['pmns_nufit_comparison']

        constants['pmns_matrix'] = {
            'theta_23': create_enhanced_constant(
                pm.get('theta_23', config.NeutrinoParameters.THETA_23),
                unit='degrees',
                display='45.00°',
                uncertainty=pm.get('theta_23_error', 0.80),
                description='Atmospheric mixing angle',
                formula='θ₂₃ = 45° + (α₄ - α₅) × n_gen',
                derivation='Asymmetric coupling to shared extra dimensions',
                source='geometric',
                experimental_value=nf.get('theta_23_nufit', 45.0),
                experimental_uncertainty=nf.get('theta_23_nufit_error', 2.0),
                experimental_source='NuFIT 5.2 (2024)',
                agreement_sigma=pm.get('theta_23_sigma', 0.00),
                agreement_text='EXACT MATCH',
                testable='JUNO 2028, Hyper-K 2030s',
                references=['NuFIT 5.2']
            ),
            'theta_12': create_enhanced_constant(
                pm.get('theta_12', config.NeutrinoParameters.THETA_12),
                unit='degrees',
                display='33.59°',
                uncertainty=pm.get('theta_12_error', 1.18),
                description='Solar mixing angle',
                formula='θ₁₂ = arcsin(1/√3 × |1 + δ_pert|)',
                derivation='Tri-bimaximal mixing + G₂ cycle perturbation',
                source='geometric',
                experimental_value=nf.get('theta_12_nufit', 33.41),
                experimental_uncertainty=nf.get('theta_12_nufit_error', 0.75),
                experimental_source='NuFIT 5.2 (2024)',
                agreement_sigma=pm.get('theta_12_sigma', 0.24),
                agreement_text='Excellent (0.24σ)',
                testable='JUNO 2028',
                references=['NuFIT 5.2']
            ),
            'theta_13': create_enhanced_constant(
                pm.get('theta_13', config.NeutrinoParameters.THETA_13),
                unit='degrees',
                display='8.57°',
                uncertainty=pm.get('theta_13_error', 0.35),
                description='Reactor mixing angle',
                formula='θ₁₃ = arctan(b₂/b₃ × exp(-ν/n_gen))',
                derivation='G₂ cycle intersection asymmetry',
                source='geometric',
                experimental_value=nf.get('theta_13_nufit', 8.57),
                experimental_uncertainty=nf.get('theta_13_nufit_error', 0.12),
                experimental_source='NuFIT 5.2 (2024)',
                agreement_sigma=pm.get('theta_13_sigma', 0.01),
                agreement_text='EXACT MATCH',
                testable='JUNO 2028',
                references=['NuFIT 5.2']
            ),
            'delta_cp': create_enhanced_constant(
                pm.get('delta_cp', config.NeutrinoParameters.DELTA_CP),
                unit='degrees',
                display='235.0',
                uncertainty=pm.get('delta_cp_error', 27.4),
                description='CP-violating phase',
                formula='δ_CP from complex phase of cycle overlaps',
                derivation='G₂ complex structure modulus + optional moonshine',
                source='geometric',
                experimental_value=nf.get('delta_cp_nufit', 232.0),
                experimental_uncertainty=nf.get('delta_cp_nufit_error', 30.0),
                experimental_source='NuFIT 5.2 (2024)',
                agreement_sigma=pm.get('delta_cp_sigma', 0.10),
                agreement_text='Excellent (0.10σ)',
                testable='DUNE 2028-2032',
                references=['NuFIT 5.2']
            ),
            'avg_sigma': create_enhanced_constant(
                pm.get('average_sigma', 0.09),
                unit='σ',
                display='0.09',
                description='Average deviation from NuFIT across all 4 parameters',
                formula='Average of |θ_theory - θ_exp| / σ_exp',
                derivation='Geometric predictions vs NuFIT 5.2',
                source='simulation:pmns_full_matrix',
                agreement_text='Exceptional agreement (2 exact matches)',
                references=['NuFIT 5.2']
            ),
        }

        # Add capital aliases for HTML compatibility
        if 'delta_cp' in constants['pmns_matrix']:
            constants['pmns_matrix']['delta_CP'] = constants['pmns_matrix']['delta_cp']

    # Add dark energy with simulation data
    if 'dark_energy' in sim_data and 'desi_dr2_data' in sim_data:
        de = sim_data['dark_energy']
        desi = sim_data['desi_dr2_data']

        constants['dark_energy'] = {
            'w0_PM': create_enhanced_constant(
                de.get('w0_PM', -0.8528),
                unit='dimensionless',
                display='-0.853',
                uncertainty=0.001,
                description='Dark energy equation of state at z=0',
                formula='w₀ = -(D_eff - 1) / (D_eff + 1)',
                derivation='Maximum Entropy Principle with D_eff=12.589',
                source='geometric',
                experimental_value=desi.get('w0', -0.83),
                experimental_uncertainty=desi.get('w0_error', 0.06),
                experimental_source='DESI DR2 (Oct 2024)',
                agreement_sigma=de.get('w0_deviation_sigma', 0.38),
                agreement_text='Excellent (0.38σ)',
                testable='Euclid 2027-2028',
                references=['arXiv:2510.12627']
            ),
            'wa_PM_effective': create_enhanced_constant(
                de.get('wa_PM_effective', -0.95),
                unit='dimensionless',
                display='-0.95',
                uncertainty=0.1,
                description='Effective evolution parameter',
                formula='w_a,eff = w₀ × α_T / 3',
                derivation='Logarithmic w(z) evolution with α_T=2.7',
                source='simulation:wz_evolution_desi_dr2',
                experimental_value=desi.get('wa', -0.75),
                experimental_uncertainty=desi.get('wa_error', 0.30),
                experimental_source='DESI DR2 (Oct 2024)',
                agreement_sigma=de.get('wa_deviation_sigma', 0.66),
                agreement_text='Good (0.66σ)',
                testable='Euclid 2027-2028',
                references=['arXiv:2510.12627']
            ),
            'w0_DESI_central': create_enhanced_constant(
                desi.get('w0', config.PhenomenologyParameters.W0_DESI_DR2),
                unit='dimensionless',
                display='-0.83',
                uncertainty=desi.get('w0_error', config.PhenomenologyParameters.W0_DESI_ERROR),
                description='DESI DR2 measured dark energy equation of state',
                formula='w₀ = P/ρ for dark energy',
                derivation='DESI BAO + supernovae + CMB',
                source='experimental:DESI_DR2',
                experimental_value=-0.83,
                experimental_uncertainty=0.06,
                experimental_source='DESI DR2 (Oct 2024)',
                references=['arXiv:2510.12627']
            ),
            'w0_DESI_error': create_enhanced_constant(
                desi.get('w0_error', config.PhenomenologyParameters.W0_DESI_ERROR),
                unit='dimensionless',
                display='0.06',
                description='DESI DR2 uncertainty on w₀',
                derivation='Statistical + systematic uncertainties',
                source='experimental:DESI_DR2',
                references=['arXiv:2510.12627']
            ),
            'w0_sigma': create_enhanced_constant(
                de.get('w0_deviation_sigma', 0.38),
                unit='σ',
                display='0.38',
                description='Agreement between PM prediction and DESI measurement',
                formula='σ = |w₀_PM - w₀_DESI| / σ_DESI',
                derivation='(−0.8528 − (−0.83)) / 0.06 = 0.38σ',
                source='simulation:dark_energy_wz_evolution',
                agreement_text='Excellent agreement',
                references=['PM v7.0 validation']
            ),
            'planck_tension_resolved': create_enhanced_constant(
                1.3,
                unit='σ',
                display='1.3',
                description='Planck tension reduced via frozen field mechanism',
                formula='Tension reduction via w(z) freezing at z>3000',
                derivation='Logarithmic w(z) evolution freezes to w=-1 at CMB, reducing 6σ→1.3σ',
                source='simulation:wz_evolution_desi_dr2',
                original_tension=6.0,
                reduced_tension=1.3,
                mechanism='Frozen field at high-z',
                testable='Future CMB experiments',
                references=['DESI DR2 2024', 'PM Section 7.2']
            ),
        }

    # Add KK spectrum (from config)
    constants['kk_spectrum'] = {
        'm1_central': create_enhanced_constant(
            config.V61Predictions.M_KK_CENTRAL,
            unit='TeV',
            display='5.0±1.5',
            uncertainty=1.5,
            uncertainty_lower=3.0,
            uncertainty_upper=7.0,
            confidence_level='95%',
            description='Lightest Kaluza-Klein graviton mass',
            formula='m₁ = 1/R_shared ≈ 5 TeV',
            derivation='Compactification radius from D_eff=12.589',
            source='config:V61Predictions',
            experimental_bound=3.5,
            experimental_source='ATLAS/CMS 2024',
            testable='HL-LHC 2027-2030 (6.2σ expected)',
            references=['ATLAS-CONF-2023-xxx']
        ),
        'hl_lhc_significance': create_enhanced_constant(
            6.2,
            unit='σ',
            display='6.2σ',
            uncertainty=0.5,
            description='Expected discovery significance at HL-LHC',
            formula='σ = √(N_signal) / √(N_background)',
            derivation='Monte Carlo with 3 ab⁻¹ luminosity',
            source='simulation:kk_spectrum_collider',
            testable='HL-LHC 2030',
            references=['PM predictions section']
        ),
    }

    # Add KK Spectrum (v8.0)
    if 'kk_spectrum' in sim_data:
        kk = sim_data['kk_spectrum']
        constants['kk_spectrum'] = {
            'm1': create_enhanced_constant(
                kk.get('m1', 5000),
                unit='GeV',
                display=f"{kk.get('m1', 5000)/1e3:.2f}±{kk.get('m1_std', 1500)/1e3:.2f} TeV",
                uncertainty=kk.get('m1_std', 1500),
                description='Lightest KK graviton mass from G₂ Laplacian',
                formula='m₁ = √λ₁ × (1/R_c) where λ₁ is first Laplacian eigenvalue',
                derivation='Harmonic expansion on G₂ co-associative 4-cycles (b₃=24)',
                source='simulation:kk_spectrum_full',
                experimental_bound=3500,
                experimental_source='ATLAS/CMS 2024',
                testable='HL-LHC 2027-2030',
                references=['Acharya et al hep-th/0505083']
            ),
            'sigma_m1_fb': create_enhanced_constant(
                kk.get('sigma_m1_fb', 0.10),
                unit='fb',
                display=f"{kk.get('sigma_m1_fb', 0.10):.3f}",
                uncertainty=kk.get('sigma_m1_std', 0.01),
                description='Production cross-section at HL-LHC',
                formula='σ(pp→KK+X) ~ α_s² / m_KK² × PDF',
                derivation='Parton luminosity at √s=14 TeV',
                source='simulation:kk_spectrum_full',
                testable='HL-LHC 100 fb⁻¹',
                references=['PM predictions section']
            ),
            'discovery_significance_sigma': create_enhanced_constant(
                kk.get('discovery_significance_sigma', 6.2),
                unit='σ',
                display=f"{kk.get('discovery_significance_sigma', 6.2):.1f}σ",
                description='Expected discovery significance at HL-LHC',
                formula='σ = N_signal / √(N_background) with 100 fb⁻¹',
                derivation='Monte Carlo with full detector simulation',
                source='simulation:kk_spectrum_full',
                testable='HL-LHC 2030',
                references=['PM predictions section']
            ),
            'BR_gg': create_enhanced_constant(
                kk.get('BR_gg', 0.65),
                unit='fraction',
                display=f"{kk.get('BR_gg', 0.65)*100:.0f}%",
                description='Branching ratio KK→gg (gluons)',
                formula='BR ~ α_s² × color_factor',
                derivation='QCD coupling strength + color degrees of freedom',
                source='simulation:kk_spectrum_full',
                references=['PM predictions section']
            ),
            'm1_central': create_enhanced_constant(
                kk.get('m1', 5000),
                unit='GeV',
                display=f"{kk.get('m1', 5000)/1e3:.2f}",
                description='Central value of lightest KK mass',
                formula='m₁ from Laplacian eigenvalue',
                derivation='Harmonic expansion on G₂ manifold',
                source='simulation:kk_spectrum_full',
                references=['PM v8.0']
            ),
            'hl_lhc_significance': create_enhanced_constant(
                kk.get('discovery_significance_sigma', 6.2),
                unit='σ',
                display=f"{kk.get('discovery_significance_sigma', 6.2):.1f}",
                description='Expected discovery significance at HL-LHC',
                formula='σ = N_signal / √N_background',
                derivation='Monte Carlo with 100 fb⁻¹',
                source='simulation:kk_spectrum_full',
                references=['PM v8.0']
            ),
        }

    # Add Neutrino Mass Ordering (v8.0)
    if 'neutrino_mass_ordering' in sim_data:
        nmo = sim_data['neutrino_mass_ordering']
        constants['neutrino_mass_ordering'] = {
            'ordering_predicted': create_enhanced_constant(
                nmo.get('ordering_predicted', 'IH'),
                unit='string',
                display=nmo.get('ordering_predicted', 'IH'),
                description='Predicted neutrino mass ordering',
                formula='Ind(D) > 0 → IH, Ind(D) < 0 → NH',
                derivation='Atiyah-Singer index on G₂ associative 3-cycles (b₃=24)',
                source='simulation:neutrino_mass_ordering',
                experimental_value='NH preferred at 2.7σ (NuFIT 5.3)',
                testable='DUNE 2027, Hyper-K 2030s (>5σ resolution)',
                references=['Atiyah-Singer theorem', 'NuFIT 5.3 2024']
            ),
            'prob_IH_mean': create_enhanced_constant(
                nmo.get('prob_IH_mean', 0.92),
                unit='probability',
                display=f"{nmo.get('prob_IH_mean', 0.92)*100:.1f}%",
                uncertainty=nmo.get('prob_IH_std', 0.08),
                description='Probability of inverted hierarchy from TCS cycle orientations (83.3% positive)',
                formula='P(IH) from flux dressing F ~ √(χ_eff/b₃) = √6',
                derivation='Monte Carlo (1000 samples) over moduli deformations. From TCS cycle orientations and index signs',
                source='simulation:neutrino_mass_ordering',
                testable='DUNE 2027',
                references=['PM fermion sector']
            ),
            'confidence_level': create_enhanced_constant(
                nmo.get('confidence_level', 0.92),
                unit='probability',
                display=f"{nmo.get('confidence_level', 0.92)*100:.1f}%",
                description='Confidence in mass ordering prediction',
                formula='max(P(IH), P(NH))',
                derivation='Geometric preference from index theorem',
                source='simulation:neutrino_mass_ordering',
                references=['PM v8.0']
            ),
            'prob_IH': create_enhanced_constant(
                nmo.get('prob_IH_mean', 0.92),
                unit='probability',
                display=f"{nmo.get('prob_IH_mean', 0.92)*100:.1f}%",
                description='Alias for prob_IH_mean',
                source='simulation:neutrino_mass_ordering'
            ),
            'prob_NH': create_enhanced_constant(
                nmo.get('prob_NH_mean', 0.08),
                unit='probability',
                display=f"{nmo.get('prob_NH_mean', 0.08)*100:.1f}%",
                description='Probability of normal hierarchy',
                source='simulation:neutrino_mass_ordering'
            ),
            'flux_dressing': create_enhanced_constant(
                np.sqrt(144/24),  # √(χ_eff/b₃) = √6
                unit='dimensionless',
                display=f"{np.sqrt(144/24):.3f}",
                description='Flux dressing parameter F = √(χ_eff/b₃)',
                formula='F = √(144/24) = √6',
                derivation='Flux quantization on G₂ manifold',
                source='geometric',
                references=['PM v8.0']
            ),
            'm1_IH': create_enhanced_constant(
                nmo.get('masses_IH_meV', [0, 0, 19])[0],
                unit='meV',
                display=f"{nmo.get('masses_IH_meV', [0, 0, 19])[0]:.1f}",
                description='Lightest neutrino mass if IH',
                source='simulation:neutrino_mass_ordering'
            ),
            'm2_IH': create_enhanced_constant(
                nmo.get('masses_IH_meV', [0, 0, 19])[1],
                unit='meV',
                display=f"{nmo.get('masses_IH_meV', [0, 0, 19])[1]:.1f}",
                description='Middle neutrino mass if IH',
                source='simulation:neutrino_mass_ordering'
            ),
            'm3_IH': create_enhanced_constant(
                nmo.get('masses_IH_meV', [0, 0, 19])[2],
                unit='meV',
                display=f"{nmo.get('masses_IH_meV', [0, 0, 19])[2]:.1f}",
                description='Heaviest neutrino mass if IH',
                source='simulation:neutrino_mass_ordering'
            ),
            'm1_NH': create_enhanced_constant(
                nmo.get('masses_NH_meV', [19, 21, 54])[0],
                unit='meV',
                display=f"{nmo.get('masses_NH_meV', [19, 21, 54])[0]:.1f}",
                description='Lightest neutrino mass if NH',
                source='simulation:neutrino_mass_ordering'
            ),
            'm2_NH': create_enhanced_constant(
                nmo.get('masses_NH_meV', [19, 21, 54])[1],
                unit='meV',
                display=f"{nmo.get('masses_NH_meV', [19, 21, 54])[1]:.1f}",
                description='Middle neutrino mass if NH',
                source='simulation:neutrino_mass_ordering'
            ),
            'm3_NH': create_enhanced_constant(
                nmo.get('masses_NH_meV', [19, 21, 54])[2],
                unit='meV',
                display=f"{nmo.get('masses_NH_meV', [19, 21, 54])[2]:.1f}",
                description='Heaviest neutrino mass if NH',
                source='simulation:neutrino_mass_ordering'
            ),
            'sum_m_IH': create_enhanced_constant(
                sum(nmo.get('masses_IH_meV', [0, 0, 19])),
                unit='meV',
                display=f"{sum(nmo.get('masses_IH_meV', [0, 0, 19])):.1f}",
                description='Sum of neutrino masses if IH',
                formula='Σm_i = m₁ + m₂ + m₃',
                source='simulation:neutrino_mass_ordering'
            ),
            'sum_m_NH': create_enhanced_constant(
                sum(nmo.get('masses_NH_meV', [19, 21, 54])),
                unit='meV',
                display=f"{sum(nmo.get('masses_NH_meV', [19, 21, 54])):.1f}",
                description='Sum of neutrino masses if NH',
                formula='Σm_i = m₁ + m₂ + m₃',
                source='simulation:neutrino_mass_ordering'
            ),
        }

    # Add Proton Decay Channels (v8.0)
    if 'proton_decay_channels' in sim_data:
        pdc = sim_data['proton_decay_channels']
        constants['proton_decay_channels'] = {
            'BR_epi0_mean': create_enhanced_constant(
                pdc.get('BR_epi0_mean', 0.62),
                unit='fraction',
                display=f"{pdc.get('BR_epi0_mean', 0.62)*100:.0f}±{pdc.get('BR_epi0_std', 0.08)*100:.0f}%",
                uncertainty=pdc.get('BR_epi0_std', 0.08),
                description='Branching ratio p→e⁺π⁰ (v8.4 with CKM rotation via Wolfenstein parameterization)',
                formula='BR = |C_epi0|² / Σ|C_i|² where C ~ Y²/M_GUT² with CKM rotation',
                derivation='Yukawa matrix from wavefunction overlaps on G₂ 3-cycles. Includes explicit CKM rotation breaking diagonal dominance',
                source='simulation:proton_decay_channels',
                experimental_bound='τ_p > 1.67×10³⁴ years (Super-K)',
                testable='Hyper-K 2027-2035',
                references=['Super-K Collaboration 2024']
            ),
            'BR_Knu_mean': create_enhanced_constant(
                pdc.get('BR_Knu_mean', 0.28),
                unit='fraction',
                display=f"{pdc.get('BR_Knu_mean', 0.28)*100:.0f}±{pdc.get('BR_Knu_std', 0.06)*100:.0f}%",
                uncertainty=pdc.get('BR_Knu_std', 0.06),
                description='Branching ratio p→K⁺ν̄ (CKM us-element weighted)',
                formula='BR = |C_Knu|² / Σ|C_i|² (CKM suppressed by V_us ≈ 0.22)',
                derivation='Wilson coefficients from SO(10)→SM breaking. Includes explicit CKM rotation breaking diagonal dominance',
                source='simulation:proton_decay_channels',
                experimental_bound='τ_p > 6.6×10³³ years (Super-K)',
                testable='Hyper-K 2027-2035',
                references=['Super-K Collaboration 2024']
            ),
            'tau_p_epi0': create_enhanced_constant(
                pdc.get('tau_p_epi0', 6.3e34),
                unit='years',
                display=f"{pdc.get('tau_p_epi0', 6.3e34):.2e}",
                description='Channel-specific lifetime p→e⁺π⁰ (v8.4 with CKM)',
                formula='τ_p(channel) = τ_p(total) / BR(channel)',
                derivation='Total lifetime divided by branching ratio. Includes explicit CKM rotation breaking diagonal dominance',
                source='simulation:proton_decay_channels',
                experimental_bound=1.67e34,
                experimental_source='Super-K 2024',
                agreement='2.4× above bound',
                testable='Hyper-K 2030s',
                references=['Super-K Collaboration']
            ),
        }

    # Add Planck tension
    constants['planck_tension'] = {
        'initial_sigma': create_enhanced_constant(
            6.0,
            unit='σ',
            display='6.0σ',
            description='Initial Planck-DESI tension',
            source='observational',
            references=['Planck 2018', 'DESI DR2 2024']
        ),
        'residual_sigma': create_enhanced_constant(
            1.3,
            unit='σ',
            display='1.3σ',
            description='Residual tension after corrections',
            formula='Combined effect of log w(z) + F(R,T) bias',
            derivation='Logarithmic DE evolution + breathing mode systematic',
            source='simulation:wz_evolution_desi_dr2',
            references=['PM cosmology section']
        ),
        'frt_bias': create_enhanced_constant(
            -0.10,
            unit='dimensionless',
            display='-0.10',
            uncertainty=0.03,
            description='F(R,T) breathing mode systematic bias',
            formula='Δw₀ = -β × (Ω_m/Ω_DE) × C_ISW',
            derivation='Pneuma condensate VEV couples to matter',
            source='geometric',
            references=['PM Section 6.1a']
        ),
    }

    return constants

def write_enhanced_js(constants, filename='theory-constants-enhanced.js'):
    """Write enhanced constants to JavaScript file"""

    js_content = """/**
 * Principia Metaphysica - Enhanced Theory Constants with Metadata
 * ================================================================
 *
 * AUTO-GENERATED - DO NOT EDIT MANUALLY
 *
 * Each constant includes:
 * - value: The actual number
 * - display: Formatted display string
 * - unit: Physical units
 * - formula: Mathematical derivation
 * - derivation: Physical explanation
 * - uncertainty: Error bars / confidence intervals
 * - experimental_value: Observed data (if available)
 * - agreement_sigma: σ deviation from experiment
 * - source: Config parameter or simulation that produced it
 * - references: Citations
 * - testable: Future experiments
 *
 * Usage: Hover over any .pm-value element to see full metadata
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

"""

    js_content += f"const PM = {json.dumps(constants, indent=2)};\n\n"

    # Add formatting functions
    js_content += """
// Enhanced formatting with metadata support
PM.format = {
    scientific: (obj, decimals = 2) => {
        const val = (typeof obj === 'object') ? obj.value : obj;
        return val.toExponential(decimals);
    },

    withUnit: (obj) => {
        if (typeof obj !== 'object') return obj.toString();
        return `${obj.display || obj.value} ${obj.unit || ''}`.trim();
    },

    withError: (obj) => {
        if (typeof obj !== 'object') return obj.toString();
        if (obj.uncertainty_lower && obj.uncertainty_upper) {
            const lower = typeof obj.uncertainty_lower === 'number' ? obj.uncertainty_lower.toExponential(2) : obj.uncertainty_lower;
            const upper = typeof obj.uncertainty_upper === 'number' ? obj.uncertainty_upper.toExponential(2) : obj.uncertainty_upper;
            return `${obj.display} [${lower}-${upper}]`;
        } else if (obj.uncertainty) {
            return `${obj.display} ± ${obj.uncertainty}`;
        }
        return obj.display || obj.value.toString();
    },

    sigma: (obj) => {
        const val = (typeof obj === 'object') ? obj.value : obj;
        return val.toFixed(2) + 'σ';
    },

    display: (obj) => {
        if (typeof obj !== 'object') return obj.toString();
        return obj.display || obj.value.toString();
    }
};

// Generate tooltip HTML for a constant
PM.getTooltip = (category, parameter) => {
    const obj = PM[category][parameter];
    if (typeof obj !== 'object') return null;

    let tooltip = `<div class="pm-tooltip">`;
    tooltip += `<div class="pm-tooltip-value"><strong>${obj.display || obj.value}</strong> ${obj.unit || ''}</div>`;

    if (obj.description) {
        tooltip += `<div class="pm-tooltip-desc">${obj.description}</div>`;
    }

    if (obj.formula) {
        tooltip += `<div class="pm-tooltip-formula"><em>Formula:</em> ${obj.formula}</div>`;
    }

    if (obj.derivation) {
        tooltip += `<div class="pm-tooltip-derivation"><em>Derivation:</em> ${obj.derivation}</div>`;
    }

    if (obj.uncertainty !== undefined || obj.uncertainty_oom !== undefined) {
        const unc = obj.uncertainty_oom
            ? `±${obj.uncertainty_oom} OOM`
            : obj.uncertainty_lower && obj.uncertainty_upper
                ? `${obj.confidence_level || '68%'} CI: [${obj.uncertainty_lower}-${obj.uncertainty_upper}]`
                : `±${obj.uncertainty}`;
        tooltip += `<div class="pm-tooltip-uncertainty"><em>Uncertainty:</em> ${unc}</div>`;
    }

    if (obj.experimental_value !== undefined) {
        tooltip += `<div class="pm-tooltip-experiment">`;
        tooltip += `<em>Experiment:</em> ${obj.experimental_value} ± ${obj.experimental_uncertainty} (${obj.experimental_source})`;
        tooltip += `</div>`;
    }

    if (obj.agreement_sigma !== undefined || obj.agreement) {
        const sigma = obj.agreement_sigma || 0;
        const color = sigma < 1 ? '#4caf50' : sigma < 3 ? '#ff9800' : '#f44336';
        tooltip += `<div class="pm-tooltip-agreement" style="color:${color}">`;
        tooltip += `<em>Agreement:</em> ${obj.agreement_text || obj.agreement || `${sigma.toFixed(2)}σ`}`;
        tooltip += `</div>`;
    }

    if (obj.testable) {
        tooltip += `<div class="pm-tooltip-testable"><em>Testable:</em> ${obj.testable}</div>`;
    }

    if (obj.source) {
        tooltip += `<div class="pm-tooltip-source"><em>Source:</em> ${obj.source}</div>`;
    }

    if (obj.references && obj.references.length > 0) {
        tooltip += `<div class="pm-tooltip-refs"><em>Refs:</em> ${obj.references.join(', ')}</div>`;
    }

    tooltip += `</div>`;
    return tooltip;
};

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PM;
}
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"* Generated {filename}")
    return filename

def add_sections_metadata(constants):
    """Add sections/content metadata to constants"""
    try:
        from sections_content import SECTIONS, get_required_values

        sections_meta = {
            'meta': {
                'description': 'Section content metadata for paper and website',
                'version': '1.0',
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            }
        }

        # Add each section's metadata
        for section_id, section_data in SECTIONS.items():
            sections_meta[section_id] = {
                'title': section_data.get('title', ''),
                'subtitle': section_data.get('subtitle', ''),
                'content': section_data.get('content', ''),
                'pages': section_data.get('pages', []),
                'values': section_data.get('values', []),
                'related_simulation': section_data.get('related_simulation', ''),
                'has_topics': 'topics' in section_data and len(section_data.get('topics', [])) > 0,
                'topic_count': len(section_data.get('topics', [])),
                'required_values': get_required_values(section_id)
            }

        constants['sections'] = sections_meta
        return constants

    except ImportError:
        print("Warning: sections_content.py not found, skipping sections metadata")
        return constants

if __name__ == '__main__':
    print("Generating enhanced theory constants with metadata...")
    constants = generate_enhanced_constants()

    # Add sections metadata
    constants = add_sections_metadata(constants)

    filename = write_enhanced_js(constants)
    print(f"\nEnhanced constants written to: {filename}")
    print(f"Total categories: {len(constants)}")
    print(f"Total constants: {sum(len(v) if isinstance(v, dict) else 1 for v in constants.values())}")
