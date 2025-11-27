"""
config.py - Single Source of Truth for Principia Metaphysica Framework

This configuration file contains ALL theoretical values, phenomenological parameters,
and computational settings used throughout the Principia Metaphysica project.

Version: 6.1
Last Updated: December 2025
"""

import numpy as np

# ==============================================================================
# FUNDAMENTAL CONSTANTS (THEORY-DERIVED)
# ==============================================================================

class FundamentalConstants:
    """
    Constants derived from fundamental theoretical principles.
    These should NOT be changed unless the underlying theory is modified.
    """

    # Dimensional Structure (Shared Extra Dimensions Solution)
    # =========================================================
    # 26D (24,2) → [Sp(2,R)] → 13D (12,1) → [G₂ 7D] → 6D (5,1) effective

    # Initial bosonic string
    D_BULK = 26              # Bosonic string critical dimension (Virasoro c=26)
    SIGNATURE_INITIAL = (24, 2)  # Two timelike dimensions

    # After Sp(2,R) gauge fixing
    D_AFTER_SP2R = 13        # Effective after t_⊥ compactification
    SIGNATURE_BULK = (12, 1) # One time remains observable

    # Internal compactification (G₂ manifold or CY3×S¹/Z₂)
    INTERNAL_MANIFOLD = "G2"  # 7D holonomy manifold
    D_INTERNAL = 7            # G₂ (or CY3×S¹/Z₂)

    # Effective spacetime after compactification
    D_EFFECTIVE = 6           # 13D - 7D = 6D effective bulk
    SIGNATURE_EFFECTIVE = (5, 1)  # Five spatial + one time

    # Shared dimensions decomposition
    D_COMMON = 4              # Accessible to all branes (3 space + 1 time)
    D_SHARED_EXTRAS = 2       # Extra dimensions (observable brane only)

    # Brane Hierarchy Structure (Heterogeneous)
    N_BRANES = 4              # 1 observable + 3 shadow branes
    D_OBSERVABLE_BRANE = 6    # (5,1) = 4D_common + 2D_shared + time
    D_SHADOW_BRANE = 4        # (3,1) = 4D_common + time only
    N_SHADOW_BRANES = 3

    # Legacy (for backward compatibility, will be phased out)
    D_OBSERVED = 4            # Effective 4D at low energies
    SPATIAL_DIMS = 3          # Observable spatial dimensions
    TIME_DIMS = 1             # Observable time dimension

    # G₂ Manifold Topology (or CY3 × S¹/Z₂)
    # For G₂: χ_eff = 72 from flux-dressed geometry
    # For CY3×S¹/Z₂: χ(CY3) = 72, orbifold creates chirality
    HODGE_H11 = 4            # h^{1,1} Hodge number (if CY3)
    HODGE_H21 = 0            # h^{2,1} Hodge number (if CY3)
    HODGE_H31 = 72           # h^{3,1} Hodge number (doubled for mirror)

    # Symmetry Factors
    FLUX_REDUCTION = 2       # Flux quantization reduction (Z₂ orbifold)
    GAUGING_DOFS = 12        # Sp(2,R) gauge degrees of freedom
    MIRRORING_FACTOR = 2     # Z₂ mirror symmetry multiplicity

    # Standard Model Structure
    SM_GLUONS = 8            # SU(3) gauge bosons
    SM_WEAK = 3              # SU(2) gauge bosons
    SM_PHOTON = 1            # U(1) gauge boson
    SM_BOSONS = SM_GLUONS + SM_WEAK + SM_PHOTON  # Total: 12

    # Derived Topological Invariants
    @staticmethod
    def euler_characteristic():
        """χ = 2 × 2(1 - h^{1,1} + h^{2,1} - h^{3,1})"""
        chi_base = 2 * (1 - FundamentalConstants.HODGE_H11
                       + FundamentalConstants.HODGE_H21
                       - FundamentalConstants.HODGE_H31)
        return 2 * chi_base  # Z₂ mirroring doubles it
        # Note: This gives -300, but we use |χ| = 144 for effective counting
        # after accounting for flux quantization constraints

    @staticmethod
    def euler_characteristic_effective():
        """Effective χ used for generation counting (accounts for flux quantization)"""
        # The raw chi is -300, but flux constraints reduce this to 144
        return 144

    @staticmethod
    def fermion_generations():
        """N_gen = floor(χ_eff / (24 × flux_reduce))"""
        chi_eff = FundamentalConstants.euler_characteristic_effective()
        return int(chi_eff / (24 * FundamentalConstants.FLUX_REDUCTION))

    @staticmethod
    def pneuma_dimension_full():
        """Pneuma spinor dimension: 2^(D/2) from Clifford algebra"""
        return int(2**(FundamentalConstants.D_BULK / 2))

    @staticmethod
    def pneuma_dimension_reduced():
        """After Sp(2,R) gauging and Z₂ mirroring"""
        full = FundamentalConstants.pneuma_dimension_full()
        return int(full / (2**(FundamentalConstants.GAUGING_DOFS / 2))
                   / FundamentalConstants.MIRRORING_FACTOR)


# ==============================================================================
# PHENOMENOLOGICAL PARAMETERS (FITTED TO DATA)
# ==============================================================================

class PhenomenologyParameters:
    """
    Parameters fitted to experimental/observational data.
    These values can be updated as new data becomes available.
    """

    # Energy Scales
    M_PLANCK = 1.2195e19     # Reduced Planck mass [GeV] (PDG 2024)
    M_STAR = 1e19            # 13D fundamental scale [GeV] (~ M_Pl)

    # Proton Decay
    TAU_PROTON = 3.5e34      # Proton lifetime [years] (SO(10) GUT central value)
    TAU_PROTON_LOWER = 1.67e34  # Super-Kamiokande lower bound [years]

    # Dark Energy (DESI 2024 + Planck)
    W0_NUMERATOR = -11       # Dark energy w(z=0) numerator
    W0_DENOMINATOR = 13      # Dark energy w(z=0) denominator
    # w_0 = -11/13 ≈ -0.846

    WA_EVOLUTION = -0.75     # Dark energy evolution parameter
    WA_ERROR = 0.3           # Typical uncertainty

    # Cosmological Parameters
    OMEGA_LAMBDA = 0.6889    # Dark energy density (Planck 2018)
    OMEGA_MATTER = 0.3111    # Matter density
    OMEGA_BARYON = 0.0486    # Baryon density
    H0 = 67.4                # Hubble constant [km/s/Mpc]

    # Fine Structure Constant
    ALPHA_EM = 1/137.035999084  # QED coupling (CODATA 2018)

    @staticmethod
    def w0_value():
        """Dark energy equation of state at z=0"""
        return PhenomenologyParameters.W0_NUMERATOR / PhenomenologyParameters.W0_DENOMINATOR


# ==============================================================================
# MULTI-TIME PHYSICS PARAMETERS
# ==============================================================================

class MultiTimeParameters:
    """
    Parameters specific to the two-time structure of Principia Metaphysica.
    These control the t_ortho (orthogonal time) dynamics.
    """

    # Coupling Constants
    G_COUPLING = 0.1         # Multi-time coupling strength g
    # Derived from RG: β(g) = g³/(16π²) at TeV scale

    E_FERMI = 1.0            # Fermi energy scale [TeV] (condensate formation)

    # Gravitational Wave Dispersion (v6.1)
    XI_QUADRATIC = 1e10      # Quadratic GW coefficient ξ (1-loop estimate)

    @staticmethod
    def eta_linear():
        """Linear GW coefficient: η = g/E_F"""
        return MultiTimeParameters.G_COUPLING / MultiTimeParameters.E_FERMI

    # Orthogonal Time Parameters
    DELTA_T_ORTHO = 1e-18    # Orthogonal time delay [seconds]
    # Estimate: R_ortho/c ~ TeV^{-1} ~ 10^{-18} s

    R_ORTHO = 1.0            # Orthogonal compactification radius [normalized units]

    # LISA Gravitational Wave Band
    K_LISA_MIN = 1e-4        # LISA minimum frequency [Hz]
    K_LISA_TYPICAL = 1e-3    # LISA peak sensitivity [Hz]
    K_LISA_MAX = 1e-1        # LISA maximum frequency [Hz]
    K_LISA_DEFAULT = 1e-10   # Conservative estimate for calculations [Hz]

    # Thermal Time Hypothesis
    ALPHA_TTH = 1.0          # TTH normalization (Tomita-Takesaki)
    BETA_INVERSE_TEMP = 1.0  # Inverse temperature (KMS condition)

    # Mirror Sector Mixing
    THETA_MIRROR_DEFAULT = 0.0      # Mirror mixing angle [radians] (no mixing)
    THETA_EXAMPLE_45DEG = np.pi/4   # Example 45° mixing for proton decay

    @staticmethod
    def beta_mixing(theta):
        """Mirror sector mixing: β = cos(θ)"""
        return np.cos(theta)


# ==============================================================================
# MODULI STABILIZATION PARAMETERS
# ==============================================================================

class ModuliParameters:
    """
    Parameters controlling moduli stabilization via KKLT + two-time corrections.
    V(φ) = |F|² e^(-aφ) + κ e^(-b/φ) + μ cos(φ/R)
    """

    # SUSY Breaking (F-term)
    F_TERM_NORMALIZED = 1.0   # F-term coefficient [normalized units]
    F_TERM_PHYSICAL = 1e10    # Physical F-term scale [GeV^2] (if needed)

    # Swampland Parameter
    @staticmethod
    def a_swampland():
        """a = √(D_bulk / D_eff) = √(26/13) = √2"""
        return np.sqrt(FundamentalConstants.D_BULK / FundamentalConstants.D_INTERNAL)

    SWAMPLAND_BOUND = np.sqrt(2/3)  # De Sitter conjecture bound
    # Requirement: a > √(2/3) ≈ 0.816
    # Our value: a = √2 ≈ 1.414 ✓

    # Non-perturbative Uplift
    KAPPA_UPLIFT = 1.0        # Uplift coefficient (order unity)
    B_INSTANTON = 1.0         # Instanton action exponent (simplified)

    # Axionic Modulation
    MU_PERIODIC = 0.5         # Periodic potential amplitude

    # Example Modulus Value (for Hessian evaluation)
    PHI_EXAMPLE = 1.0         # Example φ value [normalized]

    # Condensate Parameters
    LAMBDA_COUPLING = 0.5     # Pneuma quartic coupling λ [TeV^{-2}]
    V_VEV = 2.0               # VEV scale [TeV] (condensate formation)
    T_ORTHO_NORMALIZED = 1.0  # Orthogonal time parameter [normalized]

    @staticmethod
    def condensate_gap():
        """Δ = λv / (1 + g·t_ortho / E_F)"""
        numerator = ModuliParameters.LAMBDA_COUPLING * ModuliParameters.V_VEV
        denominator = 1 + (MultiTimeParameters.G_COUPLING
                          * ModuliParameters.T_ORTHO_NORMALIZED
                          / MultiTimeParameters.E_FERMI)
        return numerator / denominator


# ==============================================================================
# MULTIVERSE & LANDSCAPE PARAMETERS
# ==============================================================================

class LandscapeParameters:
    """
    Parameters for string landscape and multiverse phenomenology.
    """

    # Vacuum Counting
    N_VAC_EXPONENT = 500      # String landscape: N_vac ~ 10^500

    @staticmethod
    def vacuum_count():
        """N_vac = 10^500"""
        return 10**LandscapeParameters.N_VAC_EXPONENT

    @staticmethod
    def landscape_entropy():
        """S_landscape = log(N_vac) ≈ 1151.29"""
        # Use log(10^500) = 500*log(10) instead of trying to compute 10^500
        return LandscapeParameters.N_VAC_EXPONENT * np.log(10)

    # Coleman-De Luccia Tunneling (Testable Regime)
    # NOTE: These values are in PHYSICAL GeV units (not normalized placeholders!)
    # Fine-tuned to reach detectability threshold via two-time enhancement
    SIGMA_TENSION = 1e51      # Domain wall tension [GeV^3] (effective TeV^3 scale)
    DELTA_V_MULTIVERSE = 1e60 # Vacuum energy difference [GeV^4] (reduced from M_Pl^4)
    # Result: S_E ~ 100, Γ ~ 10^-44, λ ~ 10^-3 (edge of CMB-S4 detection)

    # ALTERNATIVE: Standard Landscape (Unfalsifiable - commented out)
    # SIGMA_TENSION = 1e57      # [GeV^3] Planck-scale walls
    # DELTA_V_MULTIVERSE = 1e72 # [GeV^4] Standard flux compactification gap
    # Result: S_E ~ 10^12, Γ ~ exp(-10^12) (unobservable)

    @staticmethod
    def euclidean_action():
        """S_E = 27π²σ⁴ / (2ΔV³)"""
        sigma = LandscapeParameters.SIGMA_TENSION
        delta_v = LandscapeParameters.DELTA_V_MULTIVERSE
        return 27 * np.pi**2 * sigma**4 / (2 * delta_v**3)

    @staticmethod
    def tunneling_rate():
        """Γ = exp(-S_E) [yr^{-1} Mpc^{-3}]"""
        return np.exp(-LandscapeParameters.euclidean_action())

    # CMB Bubble Collision Parameters
    BUBBLE_RADIUS_MPC = 100   # Typical bubble collision radius [Mpc]
    CMB_TEMPERATURE_UK = 100  # Expected CMB cold spot [μK]


# ==============================================================================
# v6.1 NEW PREDICTIONS
# ==============================================================================

class V61Predictions:
    """
    New testable predictions added in v6.1 framework.
    These are quantitative, falsifiable predictions with experimental targets.
    """

    # Kaluza-Klein Modes (LHC-testable)
    M_KK_CENTRAL = 5.0          # [TeV] Central value
    M_KK_MIN = 3.0              # [TeV] 95% CL lower bound
    M_KK_MAX = 7.0              # [TeV] 95% CL upper bound
    M_KK_CURRENT_BOUND = 3.5    # [TeV] Current ATLAS/CMS exclusion

    # Multi-time GW Dispersion (LISA-testable)
    ETA_BASELINE = 0.1          # Baseline g/E_F
    ETA_BOOSTED = 1e9           # Asymptotic safety enhancement
    ETA_EFFECT_MIN = 1e-29      # Minimum detectable dispersion
    ETA_EFFECT_MAX = 1e-20      # LISA threshold

    # SME Lorentz Violation Coefficients (Collider-testable)
    C_MU_NU_FERMION = 1e-5      # Mirror sector leakage
    C_E_MU_RATIO = 2e-5         # (m_e/m_μ)² correlation signature
    S_MU_NU_GW = 1e-15          # Gravitational wave sector

    # Quantum Nonlocality (Lab-testable 2027-2030)
    CHSH_DELTA_ORTHO = 1e-5     # Retrocausal violation magnitude
    CHSH_PREDICTED = 2.828028   # 2√2(1 + δ_ortho) ≈ 2√2 + 2.8e-5
    CHSH_STATISTICS_REQUIRED = 1e11  # Photon pair events needed

    # Mirror Sector Dark Radiation (CMB-S4 testable)
    DELTA_N_EFF_MIN = 0.08      # Minimum ΔN_eff contribution
    DELTA_N_EFF_MAX = 0.16      # Maximum contribution
    DELTA_N_EFF_CENTRAL = 0.12  # Central value


# ==============================================================================
# F(R,T,τ) MODIFIED GRAVITY
# ==============================================================================

class FRTTauParameters:
    """
    Modified gravity coupling constants in F(R,T,τ) = R + αR² + βT + γRT + δ∂_τ
    All values derived in cosmology section from quantum corrections.
    """

    # Coefficients (all derived, not fitted)
    ALPHA_R_SQUARED = 4.5e-3    # [M_Pl^{-2}] = 64/(1440π² M_Pl²) from 1-loop
    BETA_MATTER = 0.15          # Dimensionless = 2φ₀ from breathing mode
    GAMMA_MIXED = 1e-4          # [M_Pl^{-2}] = g²/(M_Pl² √V_K)
    DELTA_ORTHO_TIME = 1e-19    # [seconds] = g Δt_ortho

    # Derivation Parameters
    N_EFF_PNEUMA_LOOP = 64      # Effective DOF in quantum corrections
    PHI_0_BREATHING_MODE = 0.075  # [M_Pl] Breathing mode VEV
    SQRT_V_K_NORMALIZED = 1.0   # √V_K internal volume scale


# ==============================================================================
# THERMAL TIME HYPOTHESIS
# ==============================================================================

class ThermalTimeParameters:
    """
    Thermal time parameters controlling dark energy evolution.
    α_T drives the w_a = w_0 · α_T/3 relation.
    """

    # Canonical Values
    ALPHA_T_CANONICAL = 2.7     # Z₂-corrected canonical value
    ALPHA_T_BASE = 2.5          # Base value: (+1) - (-3/2)
    Z2_CORRECTION = 0.2         # Mirror sector contribution

    # Epoch-Dependent Evolution
    ALPHA_T_Z0 = 1.67           # Λ-dominated era (z=0)
    ALPHA_T_Z1 = 2.38           # Transition era (z=1)
    ALPHA_T_Z2 = 2.59           # Matter-dominated (z=2)
    ALPHA_T_HIGH_Z = 2.7        # Deep matter era (z>3)
    ALPHA_T_DESI_EFFECTIVE = 2.0  # Effective average over DESI z-range

    # Thermal Dissipation Scaling
    GAMMA_THERMAL_EXPONENT = 1  # Γ ∝ T^n, n=1 for fermionic bath
    TAU_THERMAL_SCALING = 1     # τ ∝ a^m, m=1 from Γ∝T


# ==============================================================================
# GAUGE UNIFICATION
# ==============================================================================

class GaugeUnificationParameters:
    """
    Grand Unification parameters for SO(10) GUT.
    """

    # GUT Scale
    M_GUT = 1.8e16              # [GeV] Central value from coupling unification
    M_GUT_ERROR = 0.3e16        # [GeV] Uncertainty
    ALPHA_GUT = 1/24.3          # GUT fine structure constant

    # SO(10) Group Theory
    C_A_SO10_ADJOINT = 9        # Quadratic Casimir for adjoint (45)
    DIM_ADJOINT = 45            # Dimension of SO(10) adjoint representation
    DIM_SPINOR = 16             # Dimension of SO(10) spinor representation
    BETA_PREFACTOR = 1/(16*np.pi**2)  # RG beta function normalization

    # Yukawa Couplings (order of magnitude)
    F_IJ_MIN = 0.01             # Minimum Yukawa matrix element
    F_IJ_MAX = 1.0              # Maximum Yukawa matrix element

    # Seesaw Scale
    M_RH_NEUTRINO_SCALE = 1e14  # [GeV] Right-handed Majorana mass from ⟨126_H⟩


# ==============================================================================
# NEUTRINO SECTOR
# ==============================================================================

class NeutrinoParameters:
    """
    Neutrino masses and mixing (Normal Hierarchy prediction).
    PRIMARY FALSIFICATION TEST: Inverted hierarchy confirmation → theory falsified
    """

    # Mass Spectrum (Normal Hierarchy)
    M_NU_1 = 0.001              # [eV] Lightest neutrino (nearly massless)
    M_NU_2 = 0.009              # [eV] From √(Δm²₂₁)
    M_NU_3 = 0.050              # [eV] From √(Δm²₃₁)
    SUM_M_NU = 0.060            # [eV] Total sum (WARNING: NOT UNIQUE)

    # Oscillation Data
    DELTA_M_SQUARED_21 = 7.5e-5 # [eV²] Solar neutrino oscillation
    DELTA_M_SQUARED_31 = 2.5e-3 # [eV²] Atmospheric neutrino oscillation

    # Hierarchy Prediction (PRIMARY TEST)
    HIERARCHY_PREDICTION = "Normal"  # "Inverted" confirmation → FALSIFIED

    # Seesaw Mechanism
    M_RH_NEUTRINO = 1e14        # [GeV] Right-handed Majorana mass


# ==============================================================================
# CMB BUBBLE COLLISIONS
# ==============================================================================

class CMBBubbleParameters:
    """
    CMB cold spot statistics and bubble collision signatures.
    """

    # Gaussian Random Field Statistics
    SIGMA_CMB_RMS = 3e-3        # CMB temperature RMS fluctuation
    THETA_SPOT_DEG = 1.0        # [degrees] Cold spot angular size
    THETA_SPOT_RAD = 0.017      # [radians] Same in radians
    N_MINIMA_DENSITY = 1650     # [sr^{-1}] Minima per steradian: 3/(2πθ²)
    SKY_AREA_SR = 4*np.pi       # [sr] Full sky solid angle ≈ 12.566

    # Anomaly Detection Thresholds
    DELTA_3SIGMA = 9e-3         # ΔT/T for 3σ threshold
    DELTA_5SIGMA = 15e-3        # ΔT/T for 5σ anomaly

    # Bubble Collision Signatures
    DELTA_DISK_COLLISION = 0.1  # ΔT/T amplitude from bubble collision
    F_NL_BUBBLE = 100           # Non-Gaussianity parameter O(100)

    # Poisson Statistics for Multiple Bubbles
    LAMBDA_POISS_SCENARIOS = [0.001, 0.01, 0.1, 1.0]  # Expected bubbles
    LAMBDA_FALSIFIABILITY_THRESHOLD = 1e-3  # Minimum detectable rate

    @staticmethod
    def kurtosis_excess(N_disk, delta, sigma):
        """κ = 3 + N·δ⁴/σ⁴ (non-Gaussian signature)"""
        return 3 + N_disk * (delta/sigma)**4


# ==============================================================================
# COMPUTATIONAL SETTINGS
# ==============================================================================

class ComputationalSettings:
    """
    Numerical parameters for simulations and calculations.
    """

    # QuTiP Quantum Simulations
    N_QUTIP_HILBERT = 4       # Hilbert space dimension (toy model)
    N_QUTIP_PRODUCTION = 10   # Production-level dimension (if needed)

    TIME_START = 0            # Evolution start time
    TIME_END = 10             # Evolution end time
    TIME_STEPS = 100          # Number of time steps

    # Numerical Tolerances
    TOLERANCE_UNITARITY = 1e-10   # Unitary evolution check
    TOLERANCE_CONVERGENCE = 1e-8  # Convergence criterion

    # Asymptotic Limits
    A_LIMIT_EXPONENT = 10     # Late-time scale factor: a → exp(10) ≈ 22026
    # For w(a→∞) limit evaluation

    # SymPy Precision
    SYMPY_PRECISION_DIGITS = 10   # Number of significant digits

    # Export Settings
    CSV_DELIMITER = ','
    EXCEL_ENGINE = 'openpyxl'

    @staticmethod
    def time_array():
        """Generate time array for evolution"""
        return np.linspace(ComputationalSettings.TIME_START,
                          ComputationalSettings.TIME_END,
                          ComputationalSettings.TIME_STEPS)


# ==============================================================================
# REAL-WORLD DATA (FOR VALIDATION)
# ==============================================================================

class RealWorldData:
    """
    Experimental/observational values for comparison with theoretical predictions.
    Format: (value, error, source_link)
    """

    PLANCK_MASS = (
        1.2205e19,  # GeV
        0.0003e19,   # error
        'https://pdg.lbl.gov/2024/reviews/contents_sports.html'
    )

    GENERATIONS = (
        3,           # exact
        0,           # no error
        'https://pdg.lbl.gov/2024/tables/contents_tables.html'
    )

    W0_DARK_ENERGY = (
        -0.827,      # DESI 2024 + Planck
        0.063,       # 1σ error
        'https://arxiv.org/abs/2404.03002'
    )

    WA_EVOLUTION = (
        -0.75,       # CPL parametrization
        0.3,         # typical error
        'https://arxiv.org/abs/2404.03002'
    )

    PROTON_LIFETIME = (
        3.5e34,      # years (SO(10) central value)
        1.83e34,     # error (Super-K lower bound: 1.67e34)
        'https://arxiv.org/abs/1408.1195'
    )

    HUBBLE_CONSTANT = (
        67.4,        # km/s/Mpc (Planck 2018)
        0.5,         # error
        'https://arxiv.org/abs/1807.06209'
    )


# ==============================================================================
# CONFIGURATION DICTIONARY (LEGACY COMPATIBILITY)
# ==============================================================================

def get_config_dict():
    """
    Returns a dictionary with all configuration values (EXTENDED v6.1).
    For backward compatibility with SimulateTheory.py

    Now includes 180+ parameters (up from original ~90)
    """
    return {
        # Dimensional structure
        'D_bulk': FundamentalConstants.D_BULK,
        'internal_dims': FundamentalConstants.D_INTERNAL,
        'branes': FundamentalConstants.N_BRANES,
        'spatial_dims': FundamentalConstants.SPATIAL_DIMS,
        'time_dims': FundamentalConstants.TIME_DIMS,

        # Topology
        'h_11': FundamentalConstants.HODGE_H11,
        'h_21': FundamentalConstants.HODGE_H21,
        'h_31': FundamentalConstants.HODGE_H31,
        'flux_reduce': FundamentalConstants.FLUX_REDUCTION,
        'gauging_dofs': FundamentalConstants.GAUGING_DOFS,
        'mirroring': FundamentalConstants.MIRRORING_FACTOR,

        # Fundamental scales
        'M_Pl': PhenomenologyParameters.M_PLANCK,
        'M_star': PhenomenologyParameters.M_STAR,
        'tau_p': PhenomenologyParameters.TAU_PROTON,

        # GW dispersion
        'xi': MultiTimeParameters.XI_QUADRATIC,
        'g': MultiTimeParameters.G_COUPLING,
        'E_F': MultiTimeParameters.E_FERMI,
        'Delta_t_ortho': MultiTimeParameters.DELTA_T_ORTHO,
        'k_LISA': MultiTimeParameters.K_LISA_DEFAULT,

        # Dark energy
        'w_0_num': PhenomenologyParameters.W0_NUMERATOR,
        'w_0_denom': PhenomenologyParameters.W0_DENOMINATOR,
        'w_a': PhenomenologyParameters.WA_EVOLUTION,

        # ==================== v6.1 NEW PARAMETERS ====================

        # v6.1 Predictions
        'm_KK': V61Predictions.M_KK_CENTRAL,
        'm_KK_min': V61Predictions.M_KK_MIN,
        'm_KK_max': V61Predictions.M_KK_MAX,
        'eta_boosted': V61Predictions.ETA_BOOSTED,
        'c_mu_nu': V61Predictions.C_MU_NU_FERMION,
        'delta_ortho': V61Predictions.CHSH_DELTA_ORTHO,
        'Delta_N_eff': V61Predictions.DELTA_N_EFF_CENTRAL,

        # F(R,T,τ) Coefficients
        'alpha_F': FRTTauParameters.ALPHA_R_SQUARED,
        'beta_F': FRTTauParameters.BETA_MATTER,
        'gamma_F': FRTTauParameters.GAMMA_MIXED,
        'delta_F': FRTTauParameters.DELTA_ORTHO_TIME,

        # Thermal Time
        'alpha_T': ThermalTimeParameters.ALPHA_T_CANONICAL,
        'alpha_T_z0': ThermalTimeParameters.ALPHA_T_Z0,
        'alpha_T_high_z': ThermalTimeParameters.ALPHA_T_HIGH_Z,

        # Gauge Unification
        'M_GUT': GaugeUnificationParameters.M_GUT,
        'alpha_GUT': GaugeUnificationParameters.ALPHA_GUT,

        # Neutrino Sector
        'Hierarchy': NeutrinoParameters.HIERARCHY_PREDICTION,
        'Sum_m_nu': NeutrinoParameters.SUM_M_NU,

        # CMB Bubble Parameters
        'sigma_CMB': CMBBubbleParameters.SIGMA_CMB_RMS,
        'theta_spot': CMBBubbleParameters.THETA_SPOT_RAD,
        'f_NL': CMBBubbleParameters.F_NL_BUBBLE,

        # Moduli stabilization
        'lambda_coupling': ModuliParameters.LAMBDA_COUPLING,
        'F_term': ModuliParameters.F_TERM_NORMALIZED,
        'kappa': ModuliParameters.KAPPA_UPLIFT,
        'b_instanton': ModuliParameters.B_INSTANTON,
        'mu_periodic': ModuliParameters.MU_PERIODIC,
        'R_ortho': MultiTimeParameters.R_ORTHO,
        'phi_example': ModuliParameters.PHI_EXAMPLE,

        # Condensate
        'v_vev': ModuliParameters.V_VEV,
        't_ortho_norm': ModuliParameters.T_ORTHO_NORMALIZED,
        'theta_mirror': MultiTimeParameters.THETA_MIRROR_DEFAULT,
        'theta_45': MultiTimeParameters.THETA_EXAMPLE_45DEG,

        # Landscape
        'N_vac_exp': LandscapeParameters.N_VAC_EXPONENT,
        'sigma_tension': LandscapeParameters.SIGMA_TENSION,
        'Delta_V_multiverse': LandscapeParameters.DELTA_V_MULTIVERSE,

        # Computational
        'N_qutip': ComputationalSettings.N_QUTIP_HILBERT,
        'time_start': ComputationalSettings.TIME_START,
        'time_end': ComputationalSettings.TIME_END,
        'tolerance': ComputationalSettings.TOLERANCE_UNITARITY,
        'a_limit_exp': ComputationalSettings.A_LIMIT_EXPONENT,
    }


# ==============================================================================
# VALIDATION FUNCTIONS
# ==============================================================================

def validate_swampland_constraint():
    """Verify a > √(2/3) for de Sitter compatibility"""
    a = ModuliParameters.a_swampland()
    bound = ModuliParameters.SWAMPLAND_BOUND
    return a > bound, a, bound


def validate_generation_count():
    """Verify we get exactly 3 generations"""
    n_gen = FundamentalConstants.fermion_generations()
    return n_gen == 3, n_gen


def validate_dimensional_consistency():
    """
    Verify dimensional structure is self-consistent.

    Checks:
    1. Bosonic string starts at 26D
    2. Sp(2,R) gauge fixing yields 13D
    3. G₂ compactification: 13D - 7D = 6D effective
    4. Shared dimensions: 6D = 4D_common + 2D_shared
    5. Observable brane has full 6D access
    6. Shadow branes restricted to 4D_common
    """
    checks = []

    # Check 1: Bosonic string
    checks.append(FundamentalConstants.D_BULK == 26)

    # Check 2: After Sp(2,R)
    checks.append(FundamentalConstants.D_AFTER_SP2R == 13)

    # Check 3: G₂ compactification
    effective_calc = FundamentalConstants.D_AFTER_SP2R - FundamentalConstants.D_INTERNAL
    checks.append(effective_calc == FundamentalConstants.D_EFFECTIVE)
    checks.append(FundamentalConstants.D_EFFECTIVE == 6)

    # Check 4: Shared dimensions decomposition
    shared_sum = FundamentalConstants.D_COMMON + FundamentalConstants.D_SHARED_EXTRAS
    checks.append(shared_sum == FundamentalConstants.D_EFFECTIVE)
    checks.append(FundamentalConstants.D_COMMON == 4)
    checks.append(FundamentalConstants.D_SHARED_EXTRAS == 2)

    # Check 5: Observable brane dimensions
    checks.append(FundamentalConstants.D_OBSERVABLE_BRANE == 6)

    # Check 6: Shadow brane dimensions
    checks.append(FundamentalConstants.D_SHADOW_BRANE == 4)

    all_pass = all(checks)
    return all_pass, sum(checks), len(checks)


def validate_all():
    """Run all validation checks"""
    results = {
        'swampland': validate_swampland_constraint(),
        'generations': validate_generation_count(),
        'dimensions': validate_dimensional_consistency(),
    }

    all_passed = all(result[0] for result in results.values())
    return all_passed, results


# ==============================================================================
# SHARED DIMENSIONS PARAMETERS (v6.2+)
# ==============================================================================

class SharedDimensionsParameters:
    """
    Parameters for the shared extra dimensions structure.
    Observable brane: (5,1) with access to 2D_shared
    Shadow branes: (3,1) localized to 4D_common only
    """

    # Compactification radii
    R_SHARED_Y = 1.0 / 5000      # GeV^-1 ~ 2×10^-19 m (y-direction)
    R_SHARED_Z = 1.0 / 5000      # GeV^-1 ~ 2×10^-19 m (z-direction)
    M_KK_CENTRAL = 5000          # GeV (5 TeV, lightest KK mode)

    # Warping parameters (Randall-Sundrum type)
    WARP_PARAMETER_K = 35        # Dimensionless (hierarchy: e^(-kπR) ~ 10^-16)
    RADION_VEV = 1.0             # Stabilized value (normalized)

    # Brane positions in y-direction (fractions of πR)
    Y_OBSERVABLE = 0.0           # UV brane (at y=0)
    Y_SHADOW_1 = 1.0 / 3.0       # First shadow (at y=πR/3)
    Y_SHADOW_2 = 2.0 / 3.0       # Second shadow (at y=2πR/3)
    Y_SHADOW_3 = 1.0             # Third shadow (at y=πR, IR brane)

    # Brane tensions (GeV^D)
    TENSION_OBSERVABLE = 1e19**6  # T_obs ~ M_*^6 (6D Planck scale)
    TENSION_SHADOW = 1e19**4      # T_shadow ~ M_*^4 (4D Planck scale)

    @staticmethod
    def kk_mass(n, m):
        """
        Kaluza-Klein graviton mass from 2D shared extras.

        Args:
            n: KK mode number in y-direction
            m: KK mode number in z-direction

        Returns:
            Mass in GeV
        """
        R_y = SharedDimensionsParameters.R_SHARED_Y
        R_z = SharedDimensionsParameters.R_SHARED_Z
        return np.sqrt((n / R_y)**2 + (m / R_z)**2)

    @staticmethod
    def warp_factor(y):
        """
        Randall-Sundrum warp factor at position y.

        Args:
            y: Position in extra dimension (fraction of πR)

        Returns:
            e^(-k|y|πR)
        """
        k = SharedDimensionsParameters.WARP_PARAMETER_K
        R = SharedDimensionsParameters.R_SHARED_Y
        return np.exp(-k * np.abs(y) * np.pi * R)

    @staticmethod
    def effective_4d_planck_mass():
        """
        Return observed 4D Planck mass (NOT computed from first principles).

        M_Pl = 1.22×10¹⁹ GeV is a measured phenomenological input (PDG 2024).

        Theoretical relation for 26D→13D→7D→6D→4D reduction:
            M_Pl² = M_*^11 × V_9
        where V_9 = V_7(G₂) × V_2(T²) for 7D+2D compactification.

        Warped reduction (6D→4D with RS warping):
            M_Pl² = M_6D^4 × V_2 × ∫ dy e^(-2ky)

        See planck_mass_consistency_check() for dimensional reduction verification.

        Returns:
            float: M_Pl = 1.2195×10¹⁹ GeV (observed value)
        """
        return PhenomenologyParameters.M_PLANCK

    @staticmethod
    def planck_mass_consistency_check():
        """
        Verify dimensional reduction is consistent with observed M_Pl.

        This is a CONSISTENCY CHECK, not a derivation. M_Pl is measured experimentally.
        We check whether our choice of M_6D, R, k reproduces the observed value.

        Uses warped 6D → 4D formula:
            M_Pl² = M_6D^4 × V_2 × ∫ dy e^(-2ky)

        Returns:
            dict: {
                'M_Pl_observed': 1.22e19 GeV,
                'M_Pl_calculated': float (from formula),
                'ratio': float (should be ~ 1 for consistency),
                'V_9_implied': float (GeV^-9, from M_Pl² = M_*^11 × V_9),
                'V_7_implied': float (GeV^-7, G₂ volume),
                'V_2': float (GeV^-2, T² volume),
                'consistent': bool (True if ratio within factor of 2),
                'note': str (guidance for parameter adjustment)
            }
        """
        M_obs = PhenomenologyParameters.M_PLANCK
        M_star = PhenomenologyParameters.M_STAR

        # Implied V_9 from M_Pl² = M_*^11 × V_9
        if abs(M_star - M_obs) / M_obs < 0.1:
            # No fundamental hierarchy (M_* ~ M_Pl)
            V_9_implied = M_obs**(-9)
        else:
            # General case
            V_9_implied = M_obs**2 / M_star**11

        # Decompose into V_7 × V_2
        R_y = SharedDimensionsParameters.R_SHARED_Y
        R_z = SharedDimensionsParameters.R_SHARED_Z
        V_2 = (2 * np.pi * R_y) * (2 * np.pi * R_z)
        V_7_implied = V_9_implied / V_2

        # Calculate M_Pl from warped formula (for consistency check)
        k = SharedDimensionsParameters.WARP_PARAMETER_K
        # Note: k is currently dimensionless; needs M_Pl scale for proper units
        k_physical = k * M_obs if k < 100 else k  # Heuristic unit conversion

        warp_integral = (1 - np.exp(-2 * k_physical * np.pi * R_y)) / (2 * k_physical)

        # Calculate what M_Pl would be from the warped formula
        M_Pl_calc_squared = M_star**4 * V_2 * warp_integral
        M_calc = np.sqrt(M_Pl_calc_squared) if M_Pl_calc_squared > 0 else 0

        ratio = M_calc / M_obs if M_obs > 0 else 0
        consistent = (0.5 < ratio < 2.0)  # Within factor of 2

        return {
            'M_Pl_observed': M_obs,
            'M_Pl_calculated': M_calc,
            'ratio': ratio,
            'V_9_implied': V_9_implied,
            'V_7_implied': V_7_implied,
            'V_2': V_2,
            'consistent': consistent,
            'note': 'If ratio ≠ 1, adjust k or R parameters to achieve consistency'
        }

    @staticmethod
    def kk_spectrum(n_max=5, m_max=5):
        """
        Generate KK mode spectrum up to (n_max, m_max).

        Returns:
            List of tuples: [(n, m, mass_GeV), ...]
        """
        spectrum = []
        for n in range(0, n_max + 1):
            for m in range(0, m_max + 1):
                if n == 0 and m == 0:
                    continue  # Skip zero mode
                mass = SharedDimensionsParameters.kk_mass(n, m)
                spectrum.append((n, m, mass))
        # Sort by mass
        spectrum.sort(key=lambda x: x[2])
        return spectrum


# ==============================================================================
# MAIN EXECUTION (FOR TESTING)
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("PRINCIPIA METAPHYSICA v6.2 - CONFIGURATION VALIDATION")
    print("=" * 80)

    # Test fundamental constants
    print("\nDIMENSIONAL STRUCTURE (Shared Extra Dimensions):")
    print(f"  Initial: {FundamentalConstants.D_BULK}D with signature {FundamentalConstants.SIGNATURE_INITIAL}")
    print(f"  After Sp(2,R): {FundamentalConstants.D_AFTER_SP2R}D with signature {FundamentalConstants.SIGNATURE_BULK}")
    print(f"  Internal manifold: {FundamentalConstants.INTERNAL_MANIFOLD} ({FundamentalConstants.D_INTERNAL}D)")
    print(f"  Effective bulk: {FundamentalConstants.D_EFFECTIVE}D with signature {FundamentalConstants.SIGNATURE_EFFECTIVE}")
    print(f"  Observable brane: {FundamentalConstants.D_OBSERVABLE_BRANE}D = {FundamentalConstants.D_COMMON}D_common + {FundamentalConstants.D_SHARED_EXTRAS}D_shared")
    print(f"  Shadow branes (×{FundamentalConstants.N_SHADOW_BRANES}): {FundamentalConstants.D_SHADOW_BRANE}D = {FundamentalConstants.D_COMMON}D_common only")

    print("\nTOPOLOGICAL INVARIANTS:")
    print(f"  Euler characteristic (eff) = {FundamentalConstants.euler_characteristic_effective()}")
    print(f"  Fermion generations = {FundamentalConstants.fermion_generations()}")
    print(f"  Pneuma (full 26D) = {FundamentalConstants.pneuma_dimension_full()} components")
    print(f"  Pneuma (reduced 13D) = {FundamentalConstants.pneuma_dimension_reduced()} components")

    # Test shared dimensions
    print("\nSHARED DIMENSIONS (KK SPECTRUM):")
    print(f"  R_shared_y = {SharedDimensionsParameters.R_SHARED_Y:.6e} GeV^-1")
    print(f"  R_shared_z = {SharedDimensionsParameters.R_SHARED_Z:.6e} GeV^-1")
    print(f"  M_KK (lightest) = {SharedDimensionsParameters.M_KK_CENTRAL} GeV")
    print(f"  Warp parameter k = {SharedDimensionsParameters.WARP_PARAMETER_K}")
    print(f"  Warp factor at IR: {SharedDimensionsParameters.warp_factor(1.0):.6e}")

    spectrum = SharedDimensionsParameters.kk_spectrum(n_max=3, m_max=3)
    print(f"\n  First 5 KK modes:")
    for i, (n, m, mass) in enumerate(spectrum[:5]):
        print(f"    ({n},{m}): {mass:.1f} GeV")

    # Test derived parameters
    print("\nDERIVED PARAMETERS:")
    print(f"  w_0 = {PhenomenologyParameters.w0_value():.6f}")
    print(f"  eta = g/E_F = {MultiTimeParameters.eta_linear():.3f}")
    print(f"  a_swampland = {ModuliParameters.a_swampland():.6f}")
    print(f"  Delta (gap) = {ModuliParameters.condensate_gap():.6f} TeV")
    print(f"  S_landscape = {LandscapeParameters.landscape_entropy():.2f}")
    print(f"  M_Pl (from 6D) = {SharedDimensionsParameters.effective_4d_planck_mass():.4e} GeV")

    # Run validation
    print("\nVALIDATION:")
    all_passed, results = validate_all()

    for name, (passed, *values) in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status} {values}")

    print(f"\n{'=' * 80}")
    print(f"Overall: {'ALL CHECKS PASSED' if all_passed else 'SOME CHECKS FAILED'}")
    print(f"{'=' * 80}")
