"""
Hubble Tension Assessment: KK Modes from Bridge Dimensions
============================================================

ASSERTION: PM resolves Hubble tension via KK modes from bridge dimensions.

VERDICT: REFUTED -- The claim that Kaluza-Klein modes from bridge tori
resolve the Hubble tension is not supported by the codebase or by physics.

Evidence:

1. CODE CONTRADICTION: The actual Hubble tension module (ricci_flow_h0.py)
   does NOT use KK modes. It uses a smooth interpolation formula:
   H(z) = H0_shoes * f(z) + H0_planck * (1 - f(z)), where f(z) is a
   sigmoid-like function. The local H0 is derived from a mixing angle:
   H0_local = H0_planck * (1 + sin^2(31 deg)/2) ~ 72.96 km/s/Mpc.

2. MASS SCALE MISMATCH (47 ORDERS OF MAGNITUDE): Bridge geometry uses
   Planck-scale compactification (L1 = L2 = 1 Planck length). The lightest
   KK mass is 4.44 Planck masses ~ 10^19 eV. Early dark energy resolution
   of Hubble tension requires m ~ H(z~1000) ~ 10^{-28} eV. The gap is
   ~10^{47} -- KK modes at this scale have zero cosmological relevance.

3. BRIDGE RADII CANNOT BE LARGE ENOUGH: The stabilize_moduli() method
   bounds L1, L2 to (0.1, 10.0) Planck lengths. Even at the upper bound,
   KK masses remain ~10^{18} eV. Reaching 10^{-28} eV would require
   compactification radii of ~10^{47} Planck lengths (~10^{12} meters),
   ruled out by collider data, precision gravity tests, BBN, and CMB.

4. INCONSISTENT MECHANISMS: The codebase contains three mutually
   inconsistent Hubble tension "resolutions":
   (a) Ricci flow interpolation with mixing angle (ricci_flow_h0.py)
   (b) O'Dowd formula: H0 = (288/4) - (163/144) + 0.6819 = 71.55
       (Gate 47 certificate -- numerological)
   (c) Early Dark Energy pneuma pulse with phenomenological boost
       factor = 95 (h0_hubble_tension certificate)
   None of these use KK modes; none are mutually consistent.

5. FITTED, NOT DERIVED: The mixing angle theta = 31 degrees is described
   as a "13D/25D volume ratio" but lacks a derivation from the G2
   manifold geometry. The EDE certificate admits the boost factor 95
   is "phenomenological, from fit to CMB+BAO+SN." These are fitted
   parameters presented in geometric language, not topological derivations.

GEMINI CONSENSUS (3-round debate, 2026-03-16):
   "PM does not present a viable mechanism for resolving the Hubble tension.
   The KK mode claim is quantitatively unsupportable (47 orders of magnitude
   mass mismatch). The actual implementations rely on inconsistent,
   phenomenological adjustments -- interpolation with a fitted mixing angle,
   ad-hoc formulas with numerological constants, or phenomenological boost
   factors. These approaches lack a coherent, quantitatively derived physical
   model and represent assertions without robust theoretical backing."

SIMULATION OUTPUT (2026-03-16):
   Bridge KK spectrum (first 10): [4.44, 4.44, 4.44, 4.44, 4.44, 4.44,
                                    6.28, 6.28, 6.28, 6.28] (Planck units)
   Lightest KK mass: 4.442883 Planck masses
   Required for EDE: ~10^{-28} eV
   Mismatch: ~47 orders of magnitude

CLASSIFICATION: ASSERTION WITHOUT QUANTITATIVE BACKING
   The KK-mode mechanism is claimed but never implemented. The working
   Hubble tension code uses entirely different (and mutually inconsistent)
   phenomenological approaches with fitted parameters.

============================================================
v24.2 UPDATE: KNP-Aligned Bridge Axion EDE Attempt
============================================================

This module now computes a quantitative EDE cosmology using KNP-aligned
bridge axions from the G2 manifold. The computation shows that even with
the KNP alignment mechanism (12 axions from b3=24), the EDE fraction
is orders of magnitude too small to resolve the Hubble tension.

GEMINI CONSENSUS ON KNP EDE (3-round debate, 2026-03-16):
   "The proposed PM KNP EDE model fails to generate a sufficient early dark
   energy fraction (f_EDE ~ 7.2e-9) to resolve the Hubble tension. This
   value is orders of magnitude below the required 5-10% range. Additional
   concerns include extreme instanton action fine-tuning (S~134) and an
   incomplete racetrack mechanism that neglects the KK gap. Score: 1/10."

Key quantitative findings:
   - Required instanton action S ~ 134 (extreme tuning, typical S ~ 1-10)
   - rho_EDE / rho_crit ~ 7.2e-9 (need ~0.05-0.10 for tension resolution)
   - Sound horizon shift: delta_r_s / r_s ~ 7.2e-9 (negligible)
   - H0 shift: delta_H0 ~ 4.8e-7 km/s/Mpc (cosmologically irrelevant)

VERDICT ON KNP IMPROVEMENT: STILL REFUTED. The KNP mechanism addresses
the axion mass but not the energy density. The fundamental problem is that
f_eff ~ 1.19e14 GeV is too far below M_Planck to generate sufficient EDE.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

# ============================================================================
# SENSITIVITY ANALYSIS NOTES
# Output: cosmology.H0_ede
# Deviation: Negligible shift from LCDM (delta_H0 ~ 5e-7 km/s/Mpc)
#
# Classification: REFUTED (KNP mechanism insufficient for Hubble tension)
#
# Explanation:
#   This simulation computes the Early Dark Energy contribution from
#   KNP-aligned bridge axions in the G2 manifold framework. Despite the
#   theoretical improvement from axion alignment (12 axions, b3=24),
#   the resulting EDE fraction f_EDE ~ 7.2e-9 is ~8 orders of magnitude
#   below what is needed to meaningfully reduce the Hubble tension.
#
# Why it fails:
#   1. f_eff ~ 1.19e14 GeV is sub-Planckian by 4 orders of magnitude
#   2. rho_EDE = m^2 * f^2 is proportional to f^2, so sub-Planckian f
#      means sub-critical energy density
#   3. The racetrack mechanism can tune the mass but cannot boost the
#      energy density, which depends on f^2
#
# Status: REFUTED - mechanism quantitatively insufficient
# ============================================================================

import numpy as np
from typing import Dict, Any, List, Optional
from scipy.integrate import quad

# Import base infrastructure
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
    PMRegistry,
    MetadataBuilder,
)
from simulations.core.FormulasRegistry import get_registry

# Get registry SSoT
_REG = get_registry()


# =============================================================================
# Physical Constants (from PDG / Planck 2018)
# =============================================================================

# Hubble constant measurements
H0_PLANCK = 67.4       # km/s/Mpc (Planck 2018)
H0_SHOES = 73.04       # km/s/Mpc (SH0ES 2022)
H0_SHOES_ERR = 1.04    # km/s/Mpc

# Cosmological parameters (Planck 2018 best-fit LCDM)
OMEGA_M = 0.3153       # Total matter density
OMEGA_B = 0.04930      # Baryon density
OMEGA_R = 9.14e-5      # Radiation density (photons + 3 massless neutrinos)
OMEGA_LAMBDA = 0.6847  # Dark energy density
T_CMB = 2.7255         # CMB temperature today (K)
Z_DEC = 1089.92        # Redshift of decoupling
Z_EQ = 3402.0          # Redshift of matter-radiation equality

# Unit conversions
C_KMS = 2.99792458e5   # Speed of light (km/s)
MPC_TO_KM = 3.08568e19  # Mpc to km
EV_TO_GEV = 1.0e-9     # eV to GeV

# Planck mass
M_PLANCK_GEV = 2.435e18   # Reduced Planck mass (GeV)
M_PLANCK_EV = 2.435e27    # Reduced Planck mass (eV)

# Conversion: H0 in km/s/Mpc to eV
# H0 = 67.4 km/s/Mpc = 67.4 / (3.086e19 km) * (6.582e-16 eV*s)
H0_EV_FACTOR = 2.133e-33  # H0 / (km/s/Mpc) in eV


# =============================================================================
# KNP Axion Parameters (from G2 manifold with b3=24)
# =============================================================================

def compute_knp_parameters(b3=24):
    """
    Compute KNP-aligned axion parameters from G2 manifold topology.

    The KNP (Kim-Nilles-Peloso) alignment mechanism uses N axions to
    generate an effective super-Planckian decay constant from sub-Planckian
    individual constants.

    For G2 manifold with b3 Betti number:
    - N_axion = b3 / 2 = 12 (one per bridge pair)
    - f_single ~ M_GUT / sqrt(4*pi) ~ 2.82e15 GeV
    - f_eff ~ f_single / sqrt(N) for KNP alignment

    Note: The KNP mechanism actually REDUCES the effective decay constant
    (by 1/sqrt(N)) while allowing super-Planckian field range. This is a
    critical distinction that makes the EDE fraction even smaller.

    Returns:
        dict with axion parameters
    """
    N_axion = b3 // 2  # 12 axions from 12 bridge pairs

    # Individual axion decay constant
    # From M-theory: f ~ M_GUT / sqrt(4*pi)
    M_GUT = 2.0e16  # GeV (GUT scale)
    f_single = M_GUT / np.sqrt(4 * np.pi)  # ~ 2.82e15 GeV

    # KNP effective decay constant
    # In KNP alignment, the effective single-field decay constant is
    # f_eff = f_single / sqrt(N) for the aligned direction
    # (while the field RANGE can be N*f_single)
    f_eff_knp = f_single / np.sqrt(N_axion)  # ~ 8.14e14 GeV

    # Alternative: if f_eff is computed as stated in the sprint spec
    # f_eff ~ 1.19e14 GeV (from the specific PM calculation)
    f_eff_pm = 1.19e14  # GeV (from PM bridge axion calculation)

    # Use the PM-specific value for consistency with bridge_axion_ede.py
    f_eff = f_eff_pm

    # Required axion mass for EDE at z ~ 3500
    # m_a ~ 3 * H(z_peak) where z_peak ~ 3500
    H_z_peak_eV = H0_PLANCK * H0_EV_FACTOR * np.sqrt(
        OMEGA_R * (1 + 3500)**4 + OMEGA_M * (1 + 3500)**3
    )
    m_required_eV = 3.0 * H_z_peak_eV  # ~ 3.6e-28 eV

    # Racetrack superpotential mass
    # m_a ~ (M_string^2 / f_eff) * exp(-S)
    M_string = 1.0e18  # GeV (string scale ~ M_Planck)
    prefactor = M_string**2 / f_eff  # ~ 8.4e21 GeV

    # Required instanton action
    m_required_GeV = m_required_eV * EV_TO_GEV
    exp_neg_S = m_required_GeV / prefactor
    S_required = -np.log(exp_neg_S) if exp_neg_S > 0 else float('inf')

    return {
        'N_axion': N_axion,
        'f_single_GeV': f_single,
        'f_eff_GeV': f_eff,
        'f_eff_eV': f_eff * 1e9,  # Convert GeV to eV
        'm_required_eV': m_required_eV,
        'H_z_peak_eV': H_z_peak_eV,
        'S_required': S_required,
        'M_string_GeV': M_string,
        'prefactor_GeV': prefactor,
    }


# =============================================================================
# EDE Cosmology Computation
# =============================================================================

def f_ede_profile(z, z_peak, delta_z_frac=0.1):
    """
    Model EDE fraction as a function of redshift.

    Uses a Gaussian-like profile centered at z_peak:
    f_EDE(z) = f_EDE_peak * exp(-(z - z_peak)^2 / (2 * sigma_z^2))

    where sigma_z = delta_z_frac * z_peak.

    This captures the key feature of axion EDE: the field is frozen at
    early times, briefly dominates around z_peak, then dilutes rapidly.

    Args:
        z: redshift
        z_peak: peak redshift for EDE
        delta_z_frac: fractional width of EDE peak

    Returns:
        Normalized profile (multiply by f_EDE_peak for actual fraction)
    """
    sigma_z = delta_z_frac * z_peak
    return np.exp(-(z - z_peak)**2 / (2 * sigma_z**2))


def compute_H_squared(z, H0, Omega_m, Omega_r, Omega_Lambda, f_ede_peak=0.0,
                      z_peak=3500.0):
    """
    Compute H^2(z) with optional EDE contribution.

    H^2(z) = H0^2 [Omega_r (1+z)^4 + Omega_m (1+z)^3 + Omega_Lambda + f_EDE(z)]

    The EDE term f_EDE(z) is modeled as a brief injection around z_peak.

    Args:
        z: redshift (scalar or array)
        H0: Hubble constant in km/s/Mpc
        Omega_m: matter density parameter
        Omega_r: radiation density parameter
        Omega_Lambda: dark energy density parameter
        f_ede_peak: peak EDE fraction
        z_peak: peak redshift for EDE

    Returns:
        H^2(z) in (km/s/Mpc)^2
    """
    zp1 = 1.0 + z
    H2 = H0**2 * (
        Omega_r * zp1**4
        + Omega_m * zp1**3
        + Omega_Lambda
        + f_ede_peak * f_ede_profile(z, z_peak)
    )
    return H2


def compute_sound_speed(z, Omega_b, Omega_gamma):
    """
    Compute the baryon-photon sound speed c_s(z).

    c_s = c / sqrt(3 * (1 + R_b))
    R_b = 3 * Omega_b / (4 * Omega_gamma) * 1/(1+z)

    Args:
        z: redshift
        Omega_b: baryon density parameter
        Omega_gamma: photon density parameter

    Returns:
        c_s in units of c (dimensionless)
    """
    # Photon density parameter (photons only, not neutrinos)
    # Omega_gamma ~ Omega_r / (1 + 7/8 * (4/11)^(4/3) * N_eff)
    # For N_eff = 3.046: Omega_gamma ~ Omega_r / 1.6905
    R_b = (3.0 * Omega_b) / (4.0 * Omega_gamma) / (1.0 + z)
    return 1.0 / np.sqrt(3.0 * (1.0 + R_b))


def compute_sound_horizon(H0, Omega_m, Omega_r, Omega_b, z_dec,
                          f_ede_peak=0.0, z_peak=3500.0):
    """
    Compute the comoving sound horizon at decoupling.

    r_s = integral from z_dec to infinity of c_s(z) / H(z) dz

    This is the key quantity that connects EDE to H0: reducing r_s
    requires a higher H0 to maintain the observed CMB angular scale.

    Args:
        H0: Hubble constant (km/s/Mpc)
        Omega_m: matter density
        Omega_r: radiation density
        Omega_b: baryon density
        z_dec: decoupling redshift
        f_ede_peak: peak EDE fraction
        z_peak: peak EDE redshift

    Returns:
        r_s in Mpc
    """
    # Photon density (from radiation density)
    Omega_gamma = Omega_r / 1.6905  # Remove neutrino contribution

    def integrand(z):
        cs = compute_sound_speed(z, Omega_b, Omega_gamma)
        H = np.sqrt(compute_H_squared(
            z, H0, Omega_m, Omega_r, 0.0,  # Omega_Lambda negligible at high z
            f_ede_peak, z_peak
        ))
        return C_KMS * cs / H  # c_s * c / H(z) in Mpc

    # Integrate from z_dec to a large redshift (radiation dominated)
    r_s, _ = quad(integrand, z_dec, 1e6, limit=200)
    return r_s


def compute_angular_diameter_distance(z, H0, Omega_m, Omega_r, Omega_Lambda):
    """
    Compute the angular diameter distance D_A(z) in Mpc.

    D_A(z) = (c / (1+z)) * integral from 0 to z of dz'/H(z')

    Args:
        z: redshift
        H0: Hubble constant (km/s/Mpc)
        Omega_m, Omega_r, Omega_Lambda: density parameters

    Returns:
        D_A in Mpc
    """
    def integrand(zp):
        H = np.sqrt(compute_H_squared(
            zp, H0, Omega_m, Omega_r, Omega_Lambda
        ))
        return C_KMS / H

    d_C, _ = quad(integrand, 0, z, limit=200)
    D_A = d_C / (1.0 + z)
    return D_A


def compute_ede_energy_density(m_eV, f_eff_eV):
    """
    Compute the EDE energy density from axion parameters.

    rho_EDE = m^2 * f^2 (in natural units, eV^4)

    Args:
        m_eV: axion mass in eV
        f_eff_eV: effective decay constant in eV

    Returns:
        rho_EDE in eV^4
    """
    return m_eV**2 * f_eff_eV**2


def compute_critical_density_eV4(z, H0_eV):
    """
    Compute critical density at redshift z in eV^4.

    rho_crit = 3 * H(z)^2 * M_Pl^2

    Args:
        z: redshift
        H0_eV: H0 in eV

    Returns:
        rho_crit in eV^4
    """
    H_z = H0_eV * np.sqrt(
        OMEGA_R * (1 + z)**4 + OMEGA_M * (1 + z)**3 + OMEGA_LAMBDA
    )
    return 3.0 * H_z**2 * M_PLANCK_EV**2


# =============================================================================
# Main Simulation Class
# =============================================================================

class HubbleTensionV16(SimulationBase):
    """
    EDE-based Hubble tension analysis using KNP-aligned bridge axions.

    This module computes the Early Dark Energy contribution from the G2
    manifold's KNP-aligned axion sector and its effect on the Hubble tension.

    The computation proceeds:
    1. Compute KNP axion parameters from G2 topology (b3=24)
    2. Compute EDE energy density rho_EDE = m^2 * f_eff^2
    3. Compute EDE fraction f_EDE = rho_EDE / rho_crit at z_peak
    4. Compute modified expansion history H(z) with EDE
    5. Compute sound horizon shift and resulting H0
    6. Report honest tension reduction (or lack thereof)

    Result: The KNP mechanism generates f_EDE ~ 7.2e-9, approximately
    8 orders of magnitude below the ~5-10% needed for Hubble tension
    resolution. The mechanism is quantitatively non-viable.
    """

    def __init__(self):
        """Initialize Hubble tension EDE simulation."""
        self.knp_params = None
        self.f_ede_peak = None
        self.r_s_lcdm = None
        self.r_s_ede = None
        self.H0_ede = None

    # -------------------------------------------------------------------------
    # SimulationBase Interface - Metadata
    # -------------------------------------------------------------------------

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="hubble_tension_v16_0",
            version="24.2",
            domain="cosmology",
            title="Hubble Tension: KNP-Aligned Bridge Axion EDE",
            description=(
                "Computes Early Dark Energy from KNP-aligned bridge axions in "
                "M^{27}(24,1,2). With 12 axions from b3=24 and f_eff ~ 1.19e14 GeV, "
                "the EDE fraction f_EDE ~ 7.2e-9 is insufficient for Hubble tension "
                "resolution. Original 47-order KK gap remains unresolved by KNP."
            ),
            section_id="5",
            subsection_id="5.4"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return required input parameter paths."""
        return [
            "topology.elder_kads",  # b3 = 24
        ]

    @property
    def output_params(self) -> List[str]:
        """Return output parameter paths."""
        return [
            "cosmology.H0_ede",
            "cosmology.f_ede_peak",
            "cosmology.r_s_lcdm",
            "cosmology.r_s_ede",
            "cosmology.delta_H0",
            "cosmology.tension_sigma_lcdm",
            "cosmology.tension_sigma_ede",
            "cosmology.knp_S_required",
            "cosmology.knp_f_eff_GeV",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return formula IDs this simulation provides."""
        return [
            "ede-modified-friedmann",
            "ede-sound-horizon",
            "ede-h0-from-bao",
            "knp-axion-mass",
        ]

    # -------------------------------------------------------------------------
    # Core Computation
    # -------------------------------------------------------------------------

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute the Hubble tension EDE computation.

        Args:
            registry: PMRegistry instance

        Returns:
            Dictionary mapping parameter paths to computed values
        """
        # Validate inputs
        self.validate_inputs(registry)

        # Get b3 from registry
        b3 = self._get_b3(registry)

        # Step 1: Compute KNP axion parameters
        self.knp_params = compute_knp_parameters(b3=int(b3))

        # Step 2: Compute EDE energy density and fraction
        rho_ede = compute_ede_energy_density(
            self.knp_params['m_required_eV'],
            self.knp_params['f_eff_eV']
        )

        # Critical density at z_peak ~ 3500
        H0_eV = H0_PLANCK * H0_EV_FACTOR
        z_peak = 3500.0
        rho_crit = compute_critical_density_eV4(z_peak, H0_eV)

        self.f_ede_peak = rho_ede / rho_crit

        # Step 3: Compute LCDM sound horizon (baseline)
        self.r_s_lcdm = compute_sound_horizon(
            H0_PLANCK, OMEGA_M, OMEGA_R, OMEGA_B, Z_DEC,
            f_ede_peak=0.0
        )

        # Step 4: Compute EDE-modified sound horizon
        self.r_s_ede = compute_sound_horizon(
            H0_PLANCK, OMEGA_M, OMEGA_R, OMEGA_B, Z_DEC,
            f_ede_peak=self.f_ede_peak, z_peak=z_peak
        )

        # Step 5: Compute H0 from BAO constraint
        # The CMB angular scale theta_* = r_s / D_A(z_dec) is fixed
        # If r_s decreases, D_A must decrease, which means H0 increases
        # To first order: delta_H0/H0 ~ -delta_r_s/r_s
        delta_r_s_frac = (self.r_s_ede - self.r_s_lcdm) / self.r_s_lcdm
        self.H0_ede = H0_PLANCK * (1.0 - delta_r_s_frac)
        delta_H0 = self.H0_ede - H0_PLANCK

        # Step 6: Compute tension in sigma
        tension_lcdm = (H0_SHOES - H0_PLANCK) / H0_SHOES_ERR
        tension_ede = (H0_SHOES - self.H0_ede) / H0_SHOES_ERR

        return {
            "cosmology.H0_ede": self.H0_ede,
            "cosmology.f_ede_peak": self.f_ede_peak,
            "cosmology.r_s_lcdm": self.r_s_lcdm,
            "cosmology.r_s_ede": self.r_s_ede,
            "cosmology.delta_H0": delta_H0,
            "cosmology.tension_sigma_lcdm": tension_lcdm,
            "cosmology.tension_sigma_ede": tension_ede,
            "cosmology.knp_S_required": self.knp_params['S_required'],
            "cosmology.knp_f_eff_GeV": self.knp_params['f_eff_GeV'],
        }


    def run_eml(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        EML Math computation path — Hubble tension via Mirror Phase Mathematics.

        The numerical KNP/EDE/sound-horizon integrals delegate to normal path.
        Key EML derivations for the final arithmetic:
          δH₀/H₀ = −δr_s/r_s   →  ops.neg(ops.div(delta_rs, r_s_lcdm))
          H₀_EDE = H₀ × (1 − δr_s/r_s)
          tension = (H₀_SH0ES − H₀_EDE) / σ  →  ops.div(ops.sub(...), sigma)
        """
        from simulations.core.eml_integration import (
            eml_scalar, eml_compute, eml_sub, eml_mul, eml_div,
        )

        self.validate_inputs(registry)
        b3 = self._get_b3(registry)

        # Delegate numerical integrations to normal path
        self.knp_params = compute_knp_parameters(b3=int(b3))
        rho_ede = compute_ede_energy_density(
            self.knp_params['m_required_eV'], self.knp_params['f_eff_eV']
        )
        H0_eV = H0_PLANCK * H0_EV_FACTOR
        z_peak = 3500.0
        rho_crit = compute_critical_density_eV4(z_peak, H0_eV)
        self.f_ede_peak = rho_ede / rho_crit
        self.r_s_lcdm = compute_sound_horizon(H0_PLANCK, OMEGA_M, OMEGA_R, OMEGA_B, Z_DEC, f_ede_peak=0.0)
        self.r_s_ede = compute_sound_horizon(H0_PLANCK, OMEGA_M, OMEGA_R, OMEGA_B, Z_DEC, f_ede_peak=self.f_ede_peak, z_peak=z_peak)

        # EML: final arithmetic
        rs_lcdm_pt = eml_scalar(self.r_s_lcdm)
        rs_ede_pt = eml_scalar(self.r_s_ede)

        # δr_s / r_s
        delta_rs_frac = eml_compute(eml_div(eml_sub(rs_ede_pt, rs_lcdm_pt), rs_lcdm_pt))

        # H0_EDE = H0_PLANCK × (1 − δr_s/r_s)
        H0_ede = eml_compute(eml_mul(eml_scalar(H0_PLANCK), eml_sub(eml_scalar(1.0), eml_scalar(delta_rs_frac))))
        delta_H0 = H0_ede - H0_PLANCK

        # Tension in sigma
        tension_lcdm = eml_compute(eml_div(eml_sub(eml_scalar(H0_SHOES), eml_scalar(H0_PLANCK)), eml_scalar(H0_SHOES_ERR)))
        tension_ede = eml_compute(eml_div(eml_sub(eml_scalar(H0_SHOES), eml_scalar(H0_ede)), eml_scalar(H0_SHOES_ERR)))

        return {
            "cosmology.H0_ede": H0_ede,
            "cosmology.f_ede_peak": self.f_ede_peak,
            "cosmology.r_s_lcdm": self.r_s_lcdm,
            "cosmology.r_s_ede": self.r_s_ede,
            "cosmology.delta_H0": delta_H0,
            "cosmology.tension_sigma_lcdm": tension_lcdm,
            "cosmology.tension_sigma_ede": tension_ede,
            "cosmology.knp_S_required": self.knp_params['S_required'],
            "cosmology.knp_f_eff_GeV": self.knp_params['f_eff_GeV'],
        }

    def _get_b3(self, registry: PMRegistry) -> float:
        """Get number of associative 3-cycles from registry."""
        try:
            return registry.get_param("topology.elder_kads")
        except KeyError:
            return 24.0  # Default for G2 manifold

    # -------------------------------------------------------------------------
    # Abstract Method Implementations
    # -------------------------------------------------------------------------

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        # Use computed values if available, otherwise defaults
        knp = self.knp_params or compute_knp_parameters(b3=24)
        f_ede = self.f_ede_peak if self.f_ede_peak is not None else 7.2e-9
        H0_ede_val = self.H0_ede if self.H0_ede is not None else H0_PLANCK
        r_s_lcdm_val = self.r_s_lcdm if self.r_s_lcdm is not None else 144.12
        r_s_ede_val = self.r_s_ede if self.r_s_ede is not None else 144.12
        S_req = knp['S_required']
        f_eff = knp['f_eff_GeV']

        return SectionContent(
            section_id="5",
            subsection_id="5.4",
            title="Hubble Tension: KNP-Aligned Bridge Axion EDE",
            abstract=(
                f"REFUTED. We compute the Early Dark Energy (EDE) contribution from "
                f"KNP-aligned bridge axions in the G2 manifold framework. "
                f"With b3=24 giving N=12 axion species and f_eff = {f_eff:.2e} GeV, "
                f"the EDE fraction f_EDE = {f_ede:.2e} is ~8 orders of magnitude "
                f"below the 5-10% required for Hubble tension resolution. "
                f"This mechanism is quantitatively insufficient (46-order mass gap)."
            ),
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        f"The racetrack superpotential requires instanton action "
                        f"S = {S_req:.1f} to achieve the target axion mass "
                        f"m ~ 3.6e-28 eV. Typical instanton actions in G2 "
                        f"compactifications are S ~ 1-10, making S ~ {S_req:.0f} "
                        f"an extreme fine-tuning. The sound horizon shifts from "
                        f"r_s = {r_s_lcdm_val:.2f} Mpc (LCDM) to "
                        f"r_s = {r_s_ede_val:.2f} Mpc (EDE), yielding "
                        f"H0 = {H0_ede_val:.6f} km/s/Mpc -- a cosmologically "
                        f"negligible correction."
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        f"The fundamental limitation is that f_eff ~ {f_eff:.2e} GeV "
                        f"is ~4 orders of magnitude below M_Planck. Since "
                        f"rho_EDE = m^2 * f^2, the sub-Planckian decay constant "
                        f"directly suppresses the EDE energy density relative to "
                        f"rho_crit. The KNP alignment mechanism can tune the mass "
                        f"but cannot boost the energy density. "
                        f"VERDICT: STILL REFUTED."
                    )
                ),
            ],
            formula_refs=[
                "ede-modified-friedmann",
                "ede-sound-horizon",
                "knp-axion-mass",
            ],
            param_refs=[
                "cosmology.H0_ede",
                "cosmology.f_ede_peak",
                "cosmology.knp_S_required",
            ],
        )

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas this simulation provides."""
        knp = self.knp_params or compute_knp_parameters(b3=24)
        S_req = knp['S_required']

        return [
            Formula(
                id="ede-modified-friedmann",
                label="(5.16)",
                latex=(
                    r"H^2(z) = H_0^2\left[\Omega_r(1+z)^4 + \Omega_m(1+z)^3 "
                    r"+ \Omega_\Lambda + f_{\mathrm{EDE}}(z)\right]"
                ),
                plain_text="H^2(z) = H0^2 [Omega_r(1+z)^4 + Omega_m(1+z)^3 + Omega_Lambda + f_EDE(z)]",
                category="DERIVED",
                description=(
                    "Modified Friedmann equation with Early Dark Energy contribution "
                    "from KNP-aligned bridge axions. The EDE term f_EDE(z) is modeled "
                    "as a Gaussian profile centered at z_peak ~ 3500."
                ),
                input_params=["topology.elder_kads"],
                output_params=["cosmology.H0_ede"],
            ),
            Formula(
                id="ede-sound-horizon",
                label="(5.17)",
                latex=(
                    r"r_s = \int_{z_{\mathrm{dec}}}^{\infty} "
                    r"\frac{c_s(z)}{H(z)}\,dz, \quad "
                    r"c_s = \frac{c}{\sqrt{3(1 + R_b)}}"
                ),
                plain_text="r_s = integral from z_dec to inf of c_s(z)/H(z) dz",
                category="DERIVED",
                description=(
                    "Comoving sound horizon at decoupling. EDE increases H(z) at "
                    "early times, reducing r_s and requiring higher H0 to maintain "
                    "the observed CMB angular scale theta_* = r_s / D_A(z_dec)."
                ),
                input_params=["cosmology.H0_ede", "cosmology.f_ede_peak"],
                output_params=["cosmology.r_s_ede"],
            ),
            Formula(
                id="ede-h0-from-bao",
                label="(5.18)",
                latex=(
                    r"\frac{\delta H_0}{H_0} \approx "
                    r"-\frac{\delta r_s}{r_s}"
                ),
                plain_text="delta_H0/H0 ~ -delta_r_s/r_s",
                category="DERIVED",
                description=(
                    "First-order relation between sound horizon shift and H0 shift "
                    "from the fixed CMB angular scale constraint. A decrease in r_s "
                    "requires a proportional increase in H0."
                ),
                input_params=["cosmology.r_s_lcdm", "cosmology.r_s_ede"],
                output_params=["cosmology.delta_H0"],
            ),
            Formula(
                id="knp-axion-mass",
                label="(5.19)",
                latex=(
                    r"m_a \sim \frac{M_{\mathrm{string}}^2}{f_{\mathrm{eff}}} "
                    r"e^{-S}, \quad S \approx " + f"{S_req:.0f}"
                ),
                plain_text=f"m_a ~ (M_string^2 / f_eff) * exp(-S), S ~ {S_req:.0f}",
                category="DERIVED",
                description=(
                    f"Racetrack superpotential axion mass. The required instanton "
                    f"action S ~ {S_req:.0f} is extreme compared to typical values "
                    f"S ~ 1-10 in G2 compactifications, indicating severe fine-tuning."
                ),
                input_params=["topology.elder_kads"],
                output_params=["cosmology.knp_S_required"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        knp = self.knp_params or compute_knp_parameters(b3=24)
        H0_ede_val = self.H0_ede if self.H0_ede is not None else H0_PLANCK
        f_ede_val = self.f_ede_peak if self.f_ede_peak is not None else 7.2e-9
        r_s_lcdm_val = self.r_s_lcdm if self.r_s_lcdm is not None else 144.12
        r_s_ede_val = self.r_s_ede if self.r_s_ede is not None else 144.12
        delta_H0 = H0_ede_val - H0_PLANCK
        tension_lcdm = (H0_SHOES - H0_PLANCK) / H0_SHOES_ERR
        tension_ede = (H0_SHOES - H0_ede_val) / H0_SHOES_ERR

        return [
            Parameter(
                path="cosmology.H0_ede",
                name="H0 with PM EDE Correction",
                units="km/s/Mpc",
                status="PREDICTED",
                description=(
                    f"Hubble constant with KNP bridge axion EDE correction: "
                    f"H0 = {H0_ede_val:.6f} km/s/Mpc. The correction "
                    f"delta_H0 = {delta_H0:.2e} km/s/Mpc is cosmologically negligible. "
                    f"Tension with SH0ES remains {tension_ede:.1f} sigma "
                    f"(vs {tension_lcdm:.1f} sigma for LCDM)."
                ),
                derivation_formula="ede-h0-from-bao",
                experimental_bound=H0_SHOES,
                bound_type="measured",
                bound_source="SH0ES2022",
                uncertainty=H0_SHOES_ERR,
            ),
            Parameter(
                path="cosmology.f_ede_peak",
                name="Peak EDE Fraction",
                units="dimensionless",
                status="PREDICTED",
                description=(
                    f"Peak early dark energy fraction at z ~ 3500: "
                    f"f_EDE = {f_ede_val:.2e}. Required for Hubble tension "
                    f"resolution: 0.05-0.10. Shortfall: ~{0.05/max(f_ede_val, 1e-20):.0e}x."
                ),
                derivation_formula="ede-modified-friedmann",
                no_experimental_value=True,
            ),
            Parameter(
                path="cosmology.r_s_lcdm",
                name="LCDM Sound Horizon",
                units="Mpc",
                status="DERIVED",
                description=(
                    f"Comoving sound horizon at decoupling in standard LCDM: "
                    f"r_s = {r_s_lcdm_val:.4f} Mpc."
                ),
                derivation_formula="ede-sound-horizon",
                experimental_bound=147.09,
                bound_type="measured",
                bound_source="Planck2018",
                uncertainty=0.26,
            ),
            Parameter(
                path="cosmology.r_s_ede",
                name="EDE-Modified Sound Horizon",
                units="Mpc",
                status="PREDICTED",
                description=(
                    f"Sound horizon with KNP EDE contribution: "
                    f"r_s = {r_s_ede_val:.4f} Mpc. Negligible shift from LCDM."
                ),
                derivation_formula="ede-sound-horizon",
                no_experimental_value=True,
            ),
            Parameter(
                path="cosmology.delta_H0",
                name="H0 Shift from EDE",
                units="km/s/Mpc",
                status="PREDICTED",
                description=(
                    f"Change in H0 from KNP bridge axion EDE: "
                    f"delta_H0 = {delta_H0:.2e} km/s/Mpc. Cosmologically negligible."
                ),
                derivation_formula="ede-h0-from-bao",
                no_experimental_value=True,
            ),
            Parameter(
                path="cosmology.tension_sigma_lcdm",
                name="LCDM Hubble Tension",
                units="sigma",
                status="DERIVED",
                description=(
                    f"Hubble tension in standard LCDM: {tension_lcdm:.1f} sigma "
                    f"between Planck ({H0_PLANCK}) and SH0ES ({H0_SHOES} +/- {H0_SHOES_ERR})."
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="cosmology.tension_sigma_ede",
                name="PM EDE Hubble Tension",
                units="sigma",
                status="PREDICTED",
                description=(
                    f"Hubble tension with KNP EDE: {tension_ede:.1f} sigma. "
                    f"No meaningful reduction from LCDM ({tension_lcdm:.1f} sigma)."
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="cosmology.knp_S_required",
                name="Required Instanton Action",
                units="dimensionless",
                status="PREDICTED",
                description=(
                    f"Instanton action required in racetrack superpotential to achieve "
                    f"EDE axion mass m ~ 3.6e-28 eV: S = {knp['S_required']:.1f}. "
                    f"Typical values in G2 compactifications are S ~ 1-10."
                ),
                derivation_formula="knp-axion-mass",
                no_experimental_value=True,
            ),
            Parameter(
                path="cosmology.knp_f_eff_GeV",
                name="KNP Effective Decay Constant",
                units="GeV",
                status="PREDICTED",
                description=(
                    f"Effective axion decay constant from KNP alignment of 12 bridge "
                    f"axions: f_eff = {knp['f_eff_GeV']:.2e} GeV. Sub-Planckian by "
                    f"~4 orders of magnitude."
                ),
                no_experimental_value=True,
            ),
        ]

    # -------------------------------------------------------------------------
    # Detailed Report (convenience method, not required by base)
    # -------------------------------------------------------------------------

    def detailed_report(self) -> str:
        """Generate a detailed text report of the EDE analysis."""
        knp = self.knp_params or compute_knp_parameters(b3=24)
        f_ede = self.f_ede_peak if self.f_ede_peak is not None else 7.2e-9
        H0_ede_val = self.H0_ede if self.H0_ede is not None else H0_PLANCK
        r_s_lcdm_val = self.r_s_lcdm if self.r_s_lcdm is not None else 144.12
        r_s_ede_val = self.r_s_ede if self.r_s_ede is not None else 144.12

        lines = [
            "=" * 72,
            "HUBBLE TENSION: KNP-ALIGNED BRIDGE AXION EDE ANALYSIS",
            "=" * 72,
            "",
            "1. KNP AXION PARAMETERS (from G2 manifold, b3=24)",
            f"   N_axion        = {knp['N_axion']}",
            f"   f_single       = {knp['f_single_GeV']:.3e} GeV",
            f"   f_eff (PM)     = {knp['f_eff_GeV']:.3e} GeV",
            f"   m_required     = {knp['m_required_eV']:.3e} eV",
            f"   S_required     = {knp['S_required']:.1f}",
            f"   (typical S ~ 1-10; S ~ {knp['S_required']:.0f} is extreme tuning)",
            "",
            "2. EDE ENERGY DENSITY",
            f"   rho_EDE        = m^2 * f^2 = {compute_ede_energy_density(knp['m_required_eV'], knp['f_eff_eV']):.3e} eV^4",
            f"   rho_crit(z=3500) = {compute_critical_density_eV4(3500, H0_PLANCK * H0_EV_FACTOR):.3e} eV^4",
            f"   f_EDE_peak     = {f_ede:.3e}",
            f"   Required       = 0.05 - 0.10",
            f"   Shortfall      = ~{0.05/max(f_ede, 1e-20):.0e}x too small",
            "",
            "3. SOUND HORIZON",
            f"   r_s (LCDM)     = {r_s_lcdm_val:.4f} Mpc",
            f"   r_s (EDE)      = {r_s_ede_val:.4f} Mpc",
            f"   delta_r_s/r_s  = {(r_s_ede_val - r_s_lcdm_val) / max(r_s_lcdm_val, 1e-20):.3e}",
            "",
            "4. HUBBLE CONSTANT",
            f"   H0 (Planck)    = {H0_PLANCK} km/s/Mpc",
            f"   H0 (SH0ES)     = {H0_SHOES} +/- {H0_SHOES_ERR} km/s/Mpc",
            f"   H0 (PM EDE)    = {H0_ede_val:.6f} km/s/Mpc",
            f"   delta_H0       = {H0_ede_val - H0_PLANCK:.3e} km/s/Mpc",
            "",
            "5. TENSION ASSESSMENT",
            f"   LCDM tension   = {(H0_SHOES - H0_PLANCK) / H0_SHOES_ERR:.1f} sigma",
            f"   PM EDE tension = {(H0_SHOES - H0_ede_val) / H0_SHOES_ERR:.1f} sigma",
            "",
            "6. COMPARISON WITH ORIGINAL ASSESSMENT",
            f"   Original KK gap:     47 orders of magnitude",
            f"   KNP instanton tuning: S ~ {knp['S_required']:.0f} (extreme)",
            f"   EDE fraction:        {f_ede:.2e} (need ~0.05)",
            f"   Verdict:             STILL REFUTED",
            "",
            "=" * 72,
            "VERDICT: The KNP alignment mechanism addresses the axion mass",
            "scale via racetrack tuning but cannot generate sufficient EDE",
            "energy density. The fundamental limitation is that f_eff is",
            "~4 orders below M_Planck, giving rho_EDE ~ 8 orders below",
            "rho_crit. The Hubble tension remains unresolved.",
            "=" * 72,
        ]
        return "\n".join(lines)


# =============================================================================
# Standalone execution
# =============================================================================

def main():
    """Run standalone Hubble tension EDE analysis."""
    print("Computing KNP-aligned bridge axion EDE parameters...")
    print()

    # Compute KNP parameters
    params = compute_knp_parameters(b3=24)

    print(f"KNP Axion Parameters (b3=24, N=12):")
    print(f"  f_single     = {params['f_single_GeV']:.3e} GeV")
    print(f"  f_eff        = {params['f_eff_GeV']:.3e} GeV")
    print(f"  m_required   = {params['m_required_eV']:.3e} eV")
    print(f"  S_required   = {params['S_required']:.1f}")
    print()

    # Compute EDE fraction
    rho_ede = compute_ede_energy_density(
        params['m_required_eV'], params['f_eff_eV']
    )
    H0_eV = H0_PLANCK * H0_EV_FACTOR
    rho_crit = compute_critical_density_eV4(3500, H0_eV)
    f_ede = rho_ede / rho_crit

    print(f"EDE Energy Budget:")
    print(f"  rho_EDE      = {rho_ede:.3e} eV^4")
    print(f"  rho_crit     = {rho_crit:.3e} eV^4")
    print(f"  f_EDE        = {f_ede:.3e}")
    print(f"  Required     = 0.05 - 0.10")
    print(f"  Shortfall    = ~{0.05/f_ede:.0e}x")
    print()

    # Compute sound horizons
    print("Computing sound horizons (this may take a moment)...")
    r_s_lcdm = compute_sound_horizon(
        H0_PLANCK, OMEGA_M, OMEGA_R, OMEGA_B, Z_DEC
    )
    r_s_ede = compute_sound_horizon(
        H0_PLANCK, OMEGA_M, OMEGA_R, OMEGA_B, Z_DEC,
        f_ede_peak=f_ede, z_peak=3500.0
    )

    delta_rs_frac = (r_s_ede - r_s_lcdm) / r_s_lcdm
    H0_ede = H0_PLANCK * (1.0 - delta_rs_frac)

    print(f"Sound Horizon:")
    print(f"  r_s (LCDM)   = {r_s_lcdm:.4f} Mpc")
    print(f"  r_s (EDE)    = {r_s_ede:.4f} Mpc")
    print(f"  delta_r_s/r_s = {delta_rs_frac:.3e}")
    print()

    print(f"Hubble Constant:")
    print(f"  H0 (Planck)  = {H0_PLANCK} km/s/Mpc")
    print(f"  H0 (SH0ES)   = {H0_SHOES} +/- {H0_SHOES_ERR} km/s/Mpc")
    print(f"  H0 (PM EDE)  = {H0_ede:.6f} km/s/Mpc")
    print(f"  delta_H0     = {H0_ede - H0_PLANCK:.3e} km/s/Mpc")
    print()

    tension_lcdm = (H0_SHOES - H0_PLANCK) / H0_SHOES_ERR
    tension_ede = (H0_SHOES - H0_ede) / H0_SHOES_ERR
    print(f"Tension:")
    print(f"  LCDM:  {tension_lcdm:.1f} sigma")
    print(f"  PM EDE: {tension_ede:.1f} sigma")
    print()
    print("VERDICT: KNP mechanism does NOT resolve the Hubble tension.")
    print(f"  f_EDE ~ {f_ede:.1e} is ~{0.05/f_ede:.0e}x too small.")


if __name__ == "__main__":
    main()
