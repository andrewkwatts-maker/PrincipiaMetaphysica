#!/usr/bin/env python3
"""
Bridge Axion EDE: KNP Alignment of 12 Bridge Axions for Early Dark Energy
==========================================================================

Implements Kim-Nilles-Peloso (KNP) alignment of 12 bridge axions from the
G2 compactification M^{27}(24,1,2) as a candidate mechanism for Early Dark
Energy (EDE) to address the Hubble tension.

PHYSICS:
    In the PM framework, each of the 12 bridge tori B_i^{2,0} carries an
    axion field phi_i = Im(T_i) from the racetrack superpotential. These
    individual axions have decay constants f_sub = M_Pl / k_gimel^6 ~ 3.5e12
    GeV and racetrack-scale masses m_ind ~ 10^13 GeV ~ 10^22 eV.

    The KNP mechanism aligns N_ax axion fields to produce a collective
    effective field with enhanced decay constant:

        f_eff = f_sub * sqrt(N_ax * b3) * kappa_sampler

    where:
        N_ax = 12          (number of bridge axions)
        b3 = 24            (third Betti number of G2 manifold)
        kappa_sampler = 2  (dim(S^{2,0}), topologically fixed)

    This gives f_eff ~ 1.19e14 GeV, an enhancement of ~34x.

    The effective mass is suppressed by 1/enhancement^2:
        m_eff = m_ind / enhancement^2

HONEST ASSESSMENT:
    The KNP enhancement provides ~3 orders of magnitude suppression of the
    axion mass (from ~10^22 eV to ~10^19 eV). However, EDE requires masses
    of ~10^{-27} eV to activate at z ~ 3000-5000. The remaining gap is
    ~46 ORDERS OF MAGNITUDE.

    The mechanism provides:
    - Architectural coherence (all 12 bridges participate)
    - Legitimate KNP enhancement from Leech lattice alignment
    - ~3 orders of mass suppression
    But it DOES NOT bridge the gap to EDE-relevant scales.

    CLASSIFICATION: PARTIAL -- architecturally sound, quantitatively
    insufficient by ~46 orders of magnitude.

GEMINI DEBATE RESULTS (3 rounds, 2026-03-16, gemini-2.5-flash):
-----------------------------------------------------------------
Round 1 (KNP legitimacy):
    Gemini found the sqrt(N_ax * b3) factor has "a legitimate basis within
    the KNP framework, especially in complex compactifications like G2."
    The factor represents "increased alignment leverage provided by a
    higher-dimensional charge space." The kappa_sampler=2 factor was
    noted as "less standard in the generic KNP literature" and requiring
    "model-specific details for full justification." Gemini confirmed
    f_eff = 1.19e14 GeV is a "substantial enhancement" but noted that
    bridging to 10^{-28} eV requires a potential generation scale
    Lambda ~ 0.245 MeV, "vastly lower than the QCD scale."

Round 2 (Counter-arguments and mass gap):
    Gemini accepted kappa_sampler=2 as "an intrinsic feature of your
    compactification scheme" once it was explained as dim(S^{2,0}) fixed
    by M^{27}=24+1+2 dimensional accounting. On the mass gap: Gemini
    confirmed the "41-46 order" remaining gap is "numerically correct"
    and that the honest framing is "entirely correct and commendable."
    Gemini noted a critical inconsistency in round 1's Lambda calculation
    and corrected it: the required Lambda for 10^{-28} eV with f_eff =
    1.19e14 GeV would be ~3.4e-9 MeV, not 0.245 MeV.

Round 3 (Final classification):
    Gemini: "The KNP alignment mechanism does NOT genuinely reduce the
    Hubble tension." While the mechanism "provides architectural coherence
    by involving all 12 bridge axions and demonstrates a theoretical
    framework for alignment from the Leech lattice structure," the
    quantitative outcome "falls drastically short of the required EDE
    mass scale." The 3-order suppression is "utterly insufficient to
    bridge the 46-order gap." Classification: mechanism is conceptually
    elegant but "fails to produce an axion light enough to act as Early
    Dark Energy."

    CONSENSUS: PARTIAL mechanism -- architecturally valid, quantitatively
    insufficient by ~46 orders of magnitude.

SPRINT 1 EXTENSION: Sampler Entropy Damping (v24.3)
====================================================

    Proposed extension: Q_eff = Q_Leech + kappa_sampler * 12 * (b3/24),
    giving Tr(Q_eff) = 242 + 2*12 = 266. Then multiply m_eff by
    exp(-0.5 * integrated_entropy_rate), where the sampler entropy
    integrates over cosmological time.

    RESULT: The entropy rate (0.0825 per thermal time unit) integrated
    over the full cosmological age in thermal time (T_min * t_cosmic =
    37.85 * 4.35e17 = 1.65e19 thermal units) gives integrated_entropy
    = 1.36e18, producing exp(-6.8e17) -- catastrophic OVER-suppression
    by ~3e17 orders of magnitude. The mechanism cannot deliver a precise
    44.5-order suppression without tuning the integration timescale.

    To achieve exactly 44.5 orders, one would need t_int ~ 1242 thermal
    time units, but there is NO independent derivation of this timescale.

GEMINI DEBATE (3 rounds, 2026-03-20):
    Round 1: Gemini described the mechanism as a "textbook example of a
        speculative, ill-justified attempt to force a fit." The exp(-8e17)
        result is not "over-suppression" -- it is "annihilation." The
        difference between 10^{-44.5} and 10^{-3.5e17} is so vast that
        the model is "fundamentally broken and irrelevant to the problem."
        Demanded rigorous derivation for every term in the exponential.

    Round 2: Gemini confirmed the honest framing. Noted that achieving
        exactly 44.5 orders requires t_int ~ 1242 thermal time units.
        Suggested physically motivated intermediate timescales (decoupling,
        EDE phase duration, phase transitions, Hubble expansion limit,
        thermalization time) but noted NONE are independently derived in
        the current framework. The key question: "identify a robust,
        physically motivated reason why the integration time should be
        ~1242 thermal time units."

    Round 3: Classification: **FITTED**. "This is the textbook definition
        of fitting. A parameter (t_thermal) is chosen precisely to achieve
        the desired numerical outcome (44.5 orders) without any independent
        theoretical or observational basis for that specific value." On
        Q_eff (Tr=266 vs 242): "moving from a trace of 242 (which has a
        deep connection to the Leech lattice) to 266, especially if the
        extra 24 is not independently justified, represents a substantive
        change" and "another instance of parameter fitting."

    CONSENSUS: The entropy damping mechanism is FITTED, not DERIVED. The
    individual components (entropy rate, racetrack T_min) are independently
    computed, but the integration timescale required to close the gap lacks
    independent motivation. Reporting honestly as FITTED/PARTIAL.

SECTION: 7.2 (Bridge Axion EDE)

OUTPUTS:
    - bridge_ede.f_sub: Individual axion decay constant (GeV)
    - bridge_ede.f_eff: KNP-enhanced effective decay constant (GeV)
    - bridge_ede.enhancement: KNP enhancement factor
    - bridge_ede.m_ind: Individual racetrack axion mass (eV)
    - bridge_ede.m_eff: KNP-aligned effective mass (eV)
    - bridge_ede.m_ede_target: Target EDE mass (eV)
    - bridge_ede.mass_gap_orders: Remaining mass gap (orders of magnitude)
    - bridge_ede.f_ede_peak: Peak EDE fraction at z ~ 3000-5000
    - bridge_ede.H0_shift: Predicted H0 shift (km/s/Mpc)
    - bridge_ede.status: Mechanism status (PARTIAL/VIABLE/FAILED)

FORMULAS:
    - bridge-ede-f-sub-v24: Individual axion decay constant
    - bridge-ede-knp-enhancement-v24: KNP alignment enhancement factor
    - bridge-ede-f-eff-v24: Effective decay constant
    - bridge-ede-mass-gap-v24: Mass gap assessment

REFERENCES:
    - Kim, Nilles, Peloso (2005) arXiv:hep-ph/0409138
    - Poulin, Smith, Karwal, Kamionkowski (2019) arXiv:1811.04083
    - Acharya, Bobkov, Kane, Kumar, Vaman (2007) arXiv:hep-th/0606262
    - Svrcek, Witten (2006) arXiv:hep-th/0605206

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import math
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from simulations.core.FormulasRegistry import get_registry

# Get registry SSoT
_REG = get_registry()

from simulations.base.simulation_base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)


# ---------------------------------------------------------------------------
# Physical constants (SI / natural units)
# ---------------------------------------------------------------------------
_EV_PER_GEV = 1.0e9           # eV per GeV
_H0_PLANCK = 67.4              # km/s/Mpc (Planck 2018 CMB)
_H0_SHOES = 73.04             # km/s/Mpc (SH0ES 2022)
_T_CMB = 2.7255               # CMB temperature today (K)
_OMEGA_R_H2 = 9.15e-5         # Radiation density parameter
_OMEGA_M_H2 = 0.1430          # Matter density parameter (Planck 2018)
_OMEGA_LAMBDA = 0.6847        # Dark energy density parameter


@dataclass
class KNPAlignmentResult:
    """Results from KNP alignment computation."""
    f_sub: float               # Individual decay constant (GeV)
    f_eff: float               # Effective decay constant (GeV)
    enhancement: float         # KNP enhancement factor (dimensionless)
    N_ax: int                  # Number of aligned axions
    b3: int                    # Third Betti number
    kappa_sampler: int         # Sampler sector dimensionality


@dataclass
class RacetrackMassResult:
    """Results from racetrack mass computation."""
    T_min: float               # Stabilized Kahler modulus (Planck units)
    V_min: float               # Potential at minimum (Planck units)
    V_double_prime: float      # Curvature at minimum (Planck units)
    m_ind_planck: float        # Individual axion mass (Planck units)
    m_ind_gev: float           # Individual axion mass (GeV)
    m_ind_ev: float            # Individual axion mass (eV)


@dataclass
class EDEEvolutionResult:
    """Results from EDE cosmological evolution."""
    m_eff_ev: float            # Effective aligned mass (eV)
    m_ede_target_ev: float     # Target EDE mass (eV)
    mass_gap_orders: float     # Remaining gap (orders of magnitude)
    f_ede_peak: float          # Peak EDE fraction (0-1)
    z_peak: float              # Redshift of peak EDE
    r_s_modified_mpc: float    # Modified sound horizon (Mpc)
    r_s_standard_mpc: float    # Standard sound horizon (Mpc)
    H0_predicted: float        # Predicted H0 (km/s/Mpc)
    H0_shift: float            # H0 shift from Planck value (km/s/Mpc)


@dataclass
class BridgeAxionEDEResult:
    """Complete results from bridge axion EDE analysis."""
    knp: KNPAlignmentResult
    racetrack: RacetrackMassResult
    ede: EDEEvolutionResult
    status: str                # PARTIAL / VIABLE / FAILED
    classification: str        # DERIVED / PLAUSIBLE / PARTIAL
    honest_assessment: str     # Free text summary


# Output parameter paths
_OUTPUT_PARAMS = [
    "bridge_ede.f_sub",
    "bridge_ede.f_eff",
    "bridge_ede.enhancement",
    "bridge_ede.m_ind",
    "bridge_ede.m_eff",
    "bridge_ede.m_ede_target",
    "bridge_ede.mass_gap_orders",
    "bridge_ede.f_ede_peak",
    "bridge_ede.H0_shift",
    "bridge_ede.status",
]

# Output formula IDs
_OUTPUT_FORMULAS = [
    "bridge-ede-f-sub-v24",
    "bridge-ede-knp-enhancement-v24",
    "bridge-ede-f-eff-v24",
    "bridge-ede-mass-gap-v24",
]


class BridgeAxionEDE(SimulationBase):
    """
    KNP alignment of 12 bridge axions for Early Dark Energy.

    Physics: The 12 bridge tori B_i^{2,0} of M^{27}(24,1,2) each carry
    an axion field phi_i = Im(T_i). The KNP mechanism aligns these 12
    axions to produce an effective field with enhanced decay constant
    f_eff = f_sub * sqrt(N_ax * b3) * kappa_sampler.

    This module honestly assesses whether the enhancement is sufficient
    to produce EDE-scale axion masses (~10^{-27} eV) from racetrack-scale
    masses (~10^{22} eV). Spoiler: it is not. The gap is ~46 orders.
    """

    def __init__(self):
        super().__init__()
        self._metadata = SimulationMetadata(
            id="bridge_axion_ede_v24",
            version="24.2",
            domain="cosmology",
            title="Bridge Axion EDE: KNP Alignment for Hubble Tension",
            description=(
                "KNP alignment of 12 bridge axions from G2 compactification "
                "for Early Dark Energy. Individual f_sub = M_Pl/k_gimel^6 ~ "
                "3.5e12 GeV, KNP enhancement ~ 34x gives f_eff ~ 1.19e14 GeV. "
                "Honest assessment: mechanism provides ~3 orders suppression "
                "but falls short of EDE target by ~46 orders of magnitude."
            ),
            section_id="7.2",
            subsection_id="7.2.1"
        )

        # ---------------------------------------------------------------
        # Fundamental constants from SSoT
        # ---------------------------------------------------------------
        self.M_Planck = 1.22e19                                  # GeV
        self.k_gimel = float(_REG.demiurgic_coupling)            # 12.318...
        self.b3 = int(_REG.elder_kads)                           # 24
        self.N_ax = 12                                           # bridge count = b3/2
        self.kappa_sampler = 2                                   # dim(S^{2,0})

        # Racetrack parameters (from bridge_geometry.py)
        self.RACETRACK_A = 1.0
        self.RACETRACK_B = -0.5
        self.RACETRACK_a = 2 * math.pi / self.b3                # 2pi/24
        self.RACETRACK_b = 2 * math.pi / 26                     # 2pi/26

        # EDE target parameters
        self.m_ede_target_ev = 1.0e-27                           # eV (Poulin+ 2019)
        self.z_ede_peak = 3500.0                                 # Redshift of peak EDE
        self.f_ede_target = 0.07                                 # ~7% EDE fraction

    # ===================================================================
    # METADATA
    # ===================================================================

    @property
    def metadata(self) -> SimulationMetadata:
        return self._metadata

    @property
    def required_inputs(self) -> List[str]:
        return [
            "geometry.k_gimel",
            "topology.elder_kads",
            "axion.f_a",
        ]

    @property
    def output_params(self) -> List[str]:
        return _OUTPUT_PARAMS

    @property
    def output_formulas(self) -> List[str]:
        return _OUTPUT_FORMULAS

    # ===================================================================
    # 1. KNP ALIGNMENT COMPUTATION
    # ===================================================================

    def compute_knp_alignment(self) -> KNPAlignmentResult:
        """
        Compute KNP alignment of 12 bridge axions.

        The Kim-Nilles-Peloso mechanism aligns N axion fields to produce
        an effective super-Planckian decay constant. For 12 bridge axions
        in the 24D Leech lattice ambient space:

            f_sub = M_Pl / k_gimel^6  (individual, from axion_dm.py)
            enhancement = sqrt(N_ax * b3) * kappa_sampler
            f_eff = f_sub * enhancement

        The factor sqrt(N_ax * b3) arises from the alignment matrix
        determinant of 12 axions in b3=24 dimensional instanton charge
        space. The factor kappa_sampler=2=dim(S^{2,0}) accounts for the
        sampler sector contribution to the alignment (topologically fixed).

        Returns:
            KNPAlignmentResult with decay constants and enhancement factor.
        """
        # Individual axion decay constant (from axion_dm.py)
        k_power = 6  # 6D moduli space of associative 3-cycle
        f_sub = self.M_Planck / (self.k_gimel ** k_power)
        # ~ 3.48e12 GeV

        # KNP enhancement factor
        # sqrt(N_ax * b3): alignment matrix determinant contribution
        # kappa_sampler: sampler sector dimensionality
        alignment_factor = math.sqrt(self.N_ax * self.b3)
        enhancement = alignment_factor * self.kappa_sampler
        # sqrt(12 * 24) * 2 = sqrt(288) * 2 ~ 16.97 * 2 ~ 33.94

        # Effective decay constant
        f_eff = f_sub * enhancement
        # ~ 1.18e14 GeV

        return KNPAlignmentResult(
            f_sub=f_sub,
            f_eff=f_eff,
            enhancement=enhancement,
            N_ax=self.N_ax,
            b3=self.b3,
            kappa_sampler=self.kappa_sampler,
        )

    # ===================================================================
    # 2. RACETRACK MASS COMPUTATION
    # ===================================================================

    def compute_racetrack_mass(self, f_sub: float) -> RacetrackMassResult:
        """
        Compute the individual axion mass from the racetrack potential.

        The racetrack superpotential W = A*exp(-a*T) + B*exp(-b*T) has
        a SUSY minimum at T_min. The axion mass at this minimum is:

            m_ind^2 = V''(T_min) / f_sub^2

        where V''(T_min) is the curvature of the F-term SUGRA potential.

        Args:
            f_sub: Individual axion decay constant (GeV).

        Returns:
            RacetrackMassResult with mass in various units.
        """
        A = self.RACETRACK_A
        B = self.RACETRACK_B
        a = self.RACETRACK_a
        b = self.RACETRACK_b

        # Find stabilized modulus T_min (same algorithm as bridge_geometry.py)
        T_min = self._find_racetrack_minimum(A, B, a, b)

        # Compute potential and its second derivative at T_min
        V_min = self._fterm_potential(T_min, A, B, a, b)

        # Numerical second derivative via finite differences
        dT = 1.0e-6
        V_plus = self._fterm_potential(T_min + dT, A, B, a, b)
        V_minus = self._fterm_potential(T_min - dT, A, B, a, b)
        V_double_prime = (V_plus - 2 * V_min + V_minus) / (dT ** 2)

        # Individual axion mass in Planck units
        # m_ind^2 = |V''(T_min)| (potential curvature)
        # The axion mass from the racetrack is set by the curvature of V
        # at the stabilized minimum, in Planck units
        m_ind_planck_sq = abs(V_double_prime)
        m_ind_planck = math.sqrt(m_ind_planck_sq)

        # Convert to GeV: M_Planck ~ 1.22e19 GeV
        m_ind_gev = m_ind_planck * self.M_Planck
        m_ind_ev = m_ind_gev * _EV_PER_GEV

        return RacetrackMassResult(
            T_min=T_min,
            V_min=V_min,
            V_double_prime=V_double_prime,
            m_ind_planck=m_ind_planck,
            m_ind_gev=m_ind_gev,
            m_ind_ev=m_ind_ev,
        )

    def _find_racetrack_minimum(self, A: float, B: float,
                                 a: float, b: float) -> float:
        """Find SUSY AdS minimum of racetrack potential via D_T W = 0.

        Replicates the algorithm from bridge_geometry.py
        compute_stabilized_cycle_volumes().

        Returns:
            T_min: stabilized Kahler modulus (real part).
        """
        from scipy.optimize import brentq

        def d_t_w(T_re):
            if T_re <= 0:
                return -1e10
            exp_aT = math.exp(-a * T_re)
            exp_bT = math.exp(-b * T_re)
            W = A * exp_aT + B * exp_bT
            dW = -a * A * exp_aT - b * B * exp_bT
            return dW - (3.0 / (2.0 * T_re)) * W

        # Scan for sign change
        T_lo, T_hi = 0.5, 200.0
        n_scan = 2000
        scan_T = np.linspace(T_lo, T_hi, n_scan)
        for idx in range(n_scan - 1):
            d1 = d_t_w(scan_T[idx])
            d2 = d_t_w(scan_T[idx + 1])
            if d1 * d2 < 0:
                return brentq(d_t_w, scan_T[idx], scan_T[idx + 1], xtol=1e-14)

        # Fallback: minimize potential directly
        from scipy.optimize import minimize_scalar
        result = minimize_scalar(
            lambda T: self._fterm_potential(T, A, B, a, b),
            bounds=(0.5, 100.0),
            method='bounded',
            options={'xatol': 1e-12}
        )
        return result.x

    @staticmethod
    def _fterm_potential(T_re: float, A: float, B: float,
                         a: float, b: float) -> float:
        """F-term N=1 SUGRA scalar potential for single Kahler modulus.

        V = e^K [ g^{TT_bar} |D_T W|^2 - 3|W|^2 ]
        with K = -3 ln(2T), g^{TT_bar} = (2T)^2 / 3.

        Replicates BridgeSystem.fterm_sugra_potential_single().
        """
        if T_re <= 0:
            return 1e10

        two_T = 2.0 * T_re

        exp_aT = math.exp(-a * T_re)
        exp_bT = math.exp(-b * T_re)
        W = A * exp_aT + B * exp_bT
        dW_dT = -a * A * exp_aT - b * B * exp_bT

        dK_dT = -3.0 / two_T
        D_T_W = dW_dT + dK_dT * W

        g_TT_inv = two_T ** 2 / 3.0
        exp_K = 1.0 / two_T ** 3

        V = exp_K * (g_TT_inv * D_T_W ** 2 - 3.0 * W ** 2)
        return V

    # ===================================================================
    # 3. EDE COSMOLOGICAL EVOLUTION
    # ===================================================================

    def compute_ede_evolution(self, knp: KNPAlignmentResult,
                               racetrack: RacetrackMassResult) -> EDEEvolutionResult:
        """
        Compute EDE cosmological evolution with KNP-aligned axion.

        Solves the coupled system:
            phi_eff_ddot + 3*H*phi_eff_dot + m_eff^2*f_eff*sin(phi_eff/f_eff) = 0
            H^2 = (8*pi*G/3) * (rho_r + rho_m + rho_Lambda + rho_phi)

        The effective mass after KNP alignment:
            m_eff = m_ind / enhancement^2

        Args:
            knp: KNP alignment results.
            racetrack: Racetrack mass results.

        Returns:
            EDEEvolutionResult with EDE fraction, sound horizon, H0 shift.
        """
        # KNP-aligned effective mass
        # The KNP mechanism suppresses the mass by 1/enhancement^2
        # because V_eff ~ Lambda^4 cos(phi/f_eff) and
        # m_eff^2 = Lambda^4 / f_eff^2 = (Lambda^4 / f_sub^2) / enhancement^2
        m_eff_ev = racetrack.m_ind_ev / (knp.enhancement ** 2)

        # Mass gap assessment
        mass_gap_orders = math.log10(m_eff_ev / self.m_ede_target_ev)

        # ---------------------------------------------------------------
        # EDE fraction computation
        # ---------------------------------------------------------------
        # For the actual m_eff (which is ~10^19 eV, far above EDE scale),
        # the axion oscillates extremely rapidly and dilutes as matter
        # well before recombination. It contributes negligibly to EDE.
        #
        # We compute what the EDE fraction WOULD be if the mechanism
        # worked (i.e., if m_eff were at the target), and also what it
        # actually is with the true m_eff.

        # Standard sound horizon (no EDE)
        r_s_standard = self._compute_sound_horizon(f_ede=0.0)

        # Actual EDE fraction with true m_eff
        # If m_eff >> H(z_peak), the field oscillates and dilutes before
        # recombination. The EDE fraction is exponentially suppressed.
        H_at_peak = self._hubble_at_z(self.z_ede_peak)  # eV (natural units)
        ratio_m_H = m_eff_ev / H_at_peak if H_at_peak > 0 else 1e50

        if ratio_m_H > 1e10:
            # Field oscillates and dilutes long before z_peak
            f_ede_actual = 0.0
            r_s_modified = r_s_standard
        else:
            # Field is frozen until m_eff ~ H, then oscillates
            # Approximate EDE fraction from Poulin+ (2019) parametrization
            f_ede_actual = self._compute_ede_fraction(m_eff_ev, knp.f_eff)
            r_s_modified = self._compute_sound_horizon(f_ede=f_ede_actual)

        # H0 shift from modified sound horizon
        # H0 scales as 1/r_s (from theta_s = r_s/D_A being fixed by CMB)
        if r_s_modified > 0 and r_s_standard > 0:
            H0_predicted = _H0_PLANCK * (r_s_standard / r_s_modified)
        else:
            H0_predicted = _H0_PLANCK

        H0_shift = H0_predicted - _H0_PLANCK

        return EDEEvolutionResult(
            m_eff_ev=m_eff_ev,
            m_ede_target_ev=self.m_ede_target_ev,
            mass_gap_orders=mass_gap_orders,
            f_ede_peak=f_ede_actual,
            z_peak=self.z_ede_peak,
            r_s_modified_mpc=r_s_modified,
            r_s_standard_mpc=r_s_standard,
            H0_predicted=H0_predicted,
            H0_shift=H0_shift,
        )

    def _hubble_at_z(self, z: float) -> float:
        """Compute Hubble parameter H(z) in eV (natural units).

        H(z) = H0 * sqrt(Omega_r*(1+z)^4 + Omega_m*(1+z)^3 + Omega_Lambda)

        Returns H in eV using H0 ~ 1.44e-33 eV (for 67.4 km/s/Mpc).
        """
        # H0 in eV: 67.4 km/s/Mpc ~ 1.44e-33 eV
        H0_ev = _H0_PLANCK * 2.133e-35  # km/s/Mpc -> eV conversion
        zp1 = 1.0 + z
        h2_ratio = (_OMEGA_R_H2 * zp1**4 + _OMEGA_M_H2 * zp1**3
                    + _OMEGA_LAMBDA * (_H0_PLANCK / 100.0)**2)
        h2_ratio /= (_H0_PLANCK / 100.0)**2
        return H0_ev * math.sqrt(max(h2_ratio, 0.0))

    def _compute_ede_fraction(self, m_eff_ev: float, f_eff_gev: float) -> float:
        """Compute peak EDE fraction from axion parameters.

        Uses the approximate relation from Poulin+ (2019):
            f_EDE ~ (phi_i^2 * m_eff^2) / (6 * H(z_peak)^2 * M_Pl^2)

        where phi_i ~ f_eff (natural initial displacement).

        Args:
            m_eff_ev: Effective axion mass in eV.
            f_eff_gev: Effective decay constant in GeV.

        Returns:
            Peak EDE fraction (0-1).
        """
        H_peak_ev = self._hubble_at_z(self.z_ede_peak)
        if H_peak_ev <= 0:
            return 0.0

        # Convert f_eff to eV
        f_eff_ev = f_eff_gev * _EV_PER_GEV
        M_Pl_ev = self.M_Planck * _EV_PER_GEV

        # EDE energy density at peak: rho_phi ~ m_eff^2 * f_eff^2 / 2
        # (for phi_i ~ f_eff, potential energy dominated)
        rho_phi = 0.5 * m_eff_ev**2 * f_eff_ev**2

        # Critical density at z_peak: rho_crit = 3*H^2*M_Pl^2
        rho_crit = 3.0 * H_peak_ev**2 * M_Pl_ev**2

        if rho_crit <= 0:
            return 0.0

        f_ede = rho_phi / rho_crit

        # EDE fraction capped at physically reasonable values
        return min(f_ede, 0.30)

    def _compute_sound_horizon(self, f_ede: float = 0.0) -> float:
        """Compute the comoving sound horizon at recombination.

        Uses the analytic approximation from Hu & Sugiyama (1996):
            r_s = integral_0^{z_rec} c_s / H(z) dz

        With EDE contribution reducing r_s by approximately:
            r_s(f_EDE) ~ r_s(0) * (1 - 0.6 * f_EDE)

        (from Poulin+ 2019 fits to Boltzmann code results).

        Args:
            f_ede: Peak EDE fraction at z ~ 3000-5000.

        Returns:
            Comoving sound horizon in Mpc.
        """
        # Standard sound horizon (Planck 2018)
        r_s_standard = 147.09  # Mpc

        # EDE reduces the sound horizon
        # Approximate scaling from Poulin+ (2019) and Smith+ (2020):
        # Delta(r_s)/r_s ~ -0.6 * f_EDE
        r_s = r_s_standard * (1.0 - 0.6 * f_ede)

        return r_s

    # ===================================================================
    # 4. HUBBLE TENSION ASSESSMENT
    # ===================================================================

    def assess_hubble_tension(self, ede: EDEEvolutionResult) -> Dict[str, Any]:
        """
        Honest assessment of Hubble tension resolution.

        Computes:
        - f_EDE at z ~ 3000-5000 (target: 5-10%)
        - Modified sound horizon r_s
        - Predicted H_0 shift
        - Remaining mass gap
        - Classification

        Args:
            ede: EDE evolution results.

        Returns:
            Dict with assessment metrics and classification.
        """
        # Tension metrics
        tension_total = _H0_SHOES - _H0_PLANCK  # ~ 5.6 km/s/Mpc
        tension_resolved = ede.H0_shift
        tension_remaining = tension_total - tension_resolved
        fraction_resolved = tension_resolved / tension_total if tension_total > 0 else 0.0

        # Status classification
        if ede.mass_gap_orders < 1.0:
            status = "VIABLE"
            classification = "DERIVED"
        elif ede.mass_gap_orders < 10.0:
            status = "PARTIAL"
            classification = "PLAUSIBLE"
        else:
            status = "PARTIAL"
            classification = "PARTIAL"

        # Honest assessment text
        honest_lines = [
            f"KNP alignment of {self.N_ax} bridge axions provides "
            f"enhancement factor {ede.m_eff_ev / self.m_ede_target_ev:.1e}x "
            f"above EDE target.",
            "",
            f"Mass gap: {ede.mass_gap_orders:.1f} orders of magnitude.",
            f"  Individual racetrack mass: ~{ede.m_eff_ev * (self.kappa_sampler * math.sqrt(self.N_ax * self.b3))**2:.2e} eV",
            f"  KNP-aligned mass:          ~{ede.m_eff_ev:.2e} eV",
            f"  EDE target mass:           ~{self.m_ede_target_ev:.2e} eV",
            "",
            f"EDE fraction at z={ede.z_peak:.0f}: {ede.f_ede_peak:.2e} "
            f"(target: {self.f_ede_target:.0%})",
            f"H0 shift: {ede.H0_shift:.4f} km/s/Mpc "
            f"(need: {tension_total:.1f} km/s/Mpc)",
            f"Tension resolved: {fraction_resolved:.2%}",
            "",
            "CONCLUSION: The KNP mechanism provides architectural coherence",
            "(all 12 bridge axions participate via Leech lattice alignment)",
            "and ~3 orders of mass suppression, but falls short of EDE",
            f"target by ~{ede.mass_gap_orders:.0f} orders of magnitude.",
            "",
            "The remaining gap would require either:",
            "  (a) Non-perturbative exponential suppression (e.g., ",
            "      gravitational instantons with S ~ 100)",
            "  (b) A fundamentally different potential mechanism",
            "  (c) Acceptance that KNP alignment alone is insufficient",
        ]
        honest_assessment = "\n".join(honest_lines)

        return {
            "status": status,
            "classification": classification,
            "honest_assessment": honest_assessment,
            "tension_total_kmsMpc": tension_total,
            "tension_resolved_kmsMpc": tension_resolved,
            "tension_remaining_kmsMpc": tension_remaining,
            "fraction_resolved": fraction_resolved,
            "mass_gap_orders": ede.mass_gap_orders,
            "f_ede_peak": ede.f_ede_peak,
            "f_ede_target": self.f_ede_target,
        }

    # ===================================================================
    # 5. SAMPLER ENTROPY DAMPING (Sprint 1 extension)
    # ===================================================================

    def compute_m_eff_with_entropy_damping(self) -> Dict[str, Any]:
        """
        KNP + sampler entropy damping for Hubble tension.

        Extension: Q_eff = Q_Leech + kappa * 12 * (b3/24)
        m_eff_damped = m_eff_undamped * exp(-0.5 * integrated_entropy)

        HONEST ASSESSMENT (Gemini-validated):
            The entropy rate (0.0825) and integration time (1.65e19 thermal
            units) are independently derived, but their combination produces
            exp(-6.8e17) -- catastrophic over-suppression by ~3e17 orders.
            To get exactly 44.5 orders, one needs t_int ~ 1242 thermal time
            units, which lacks independent derivation.

            Classification: FITTED (Gemini Round 3 consensus).
            The mechanism demonstrates that sampler entropy CAN provide
            exponential suppression, but the precise magnitude is not
            uniquely determined by topology.

        Returns:
            Dict with enhanced alignment, entropy damping, and honest gap
            assessment for both naive and tuned integration times.
        """
        # 1. Enhanced alignment matrix: Q_eff = Q_Leech + kappa * delta * (b3/24)
        Q_leech_trace = 242  # from leech_lattice.compute_axion_alignment_matrix()
        kappa_sampler = self.kappa_sampler  # = 2 = dim(S^{2,0})
        delta_bridges = self.N_ax  # = 12
        b3_factor = self.b3 / 24  # = 1 (normalization)
        Q_eff_trace = Q_leech_trace + kappa_sampler * delta_bridges * b3_factor  # = 266

        # 2. Enhanced f_eff using Q_eff trace
        f_sub = self.M_Planck / self.k_gimel ** 6
        f_eff_enhanced = f_sub * np.sqrt(Q_eff_trace)
        # Compare: original f_eff uses sqrt(N_ax * b3) * kappa = sqrt(288) * 2 ~ 33.94 * f_sub

        # 3. Racetrack mass (reuse existing computation)
        knp = self.compute_knp_alignment()
        racetrack = self.compute_racetrack_mass(knp.f_sub)
        m_ind_ev = racetrack.m_ind_ev

        # 4. Undamped effective mass with enhanced alignment
        m_eff_undamped = m_ind_ev / Q_eff_trace  # mass suppressed by 1/Tr(Q_eff)

        # 5. Entropy damping computation
        from simulations.PM.field_dynamics.sampler_entropy_dynamics import SamplerEntropyDynamics
        sed = SamplerEntropyDynamics()
        alpha_T = 2.700
        rho_matrices = [np.eye(2) / 2 for _ in range(12)]  # maximally mixed
        gradient = sed.compute_entropy_gradient(alpha_T, rho_matrices)
        entropy_rate = abs(gradient['entropy_gradient'])  # ~ 0.0825

        # Target EDE mass
        target_ev = 1e-28

        # Integration time: T_min * t_cosmic (naive cosmological integration)
        t_cosmic_seconds = 4.35e17  # 13.8 Gyr in seconds
        T_min = racetrack.T_min  # ~ 37.85 (stabilized Kahler modulus)
        t_thermal_naive = T_min * t_cosmic_seconds  # ~ 1.65e19

        # Naive integrated entropy (full cosmological age)
        integrated_entropy_naive = entropy_rate * t_thermal_naive
        damping_naive = np.exp(-0.5 * integrated_entropy_naive)
        m_eff_damped_naive = m_eff_undamped * damping_naive

        # Required integration time to close the ACTUAL gap
        # The actual gap is log10(m_eff_undamped / target_ev) orders
        # Need: m_eff_undamped * exp(-0.5 * S) = target_ev
        # => exp(-0.5 * S) = target_ev / m_eff_undamped
        # => 0.5 * S = ln(m_eff_undamped / target_ev)
        # => S = 2 * ln(m_eff_undamped / target_ev)
        required_suppression_orders = np.log10(m_eff_undamped / target_ev)
        S_required = 2.0 * required_suppression_orders * np.log(10)
        t_required_corrected = S_required / entropy_rate
        damping_tuned = np.exp(-0.5 * S_required)
        m_eff_damped_tuned = m_eff_undamped * damping_tuned

        # Gap assessments
        if m_eff_damped_naive > 0 and np.isfinite(m_eff_damped_naive):
            gap_naive = np.log10(m_eff_damped_naive / target_ev) if m_eff_damped_naive > 0 else float('-inf')
        else:
            gap_naive = float('-inf')  # over-suppressed to zero

        gap_tuned = np.log10(m_eff_damped_tuned / target_ev) if m_eff_damped_tuned > 0 else float('inf')

        # Undamped gap (for reference)
        gap_undamped = np.log10(m_eff_undamped / target_ev)

        return {
            # Enhanced alignment
            'Q_leech_trace': Q_leech_trace,
            'Q_eff_trace': Q_eff_trace,
            'f_sub_GeV': f_sub,
            'f_eff_enhanced_GeV': f_eff_enhanced,

            # Racetrack
            'm_ind_eV': m_ind_ev,
            'T_min': T_min,

            # Undamped
            'm_eff_undamped_eV': m_eff_undamped,
            'gap_undamped_orders': gap_undamped,

            # Entropy parameters
            'entropy_rate': entropy_rate,
            'entropy_gradient_full': gradient,

            # Naive integration (full cosmological age)
            't_thermal_naive': t_thermal_naive,
            'integrated_entropy_naive': integrated_entropy_naive,
            'damping_factor_naive': damping_naive,
            'm_eff_damped_naive_eV': m_eff_damped_naive,
            'gap_naive_orders': gap_naive,
            'naive_status': 'OVER-SUPPRESSED (catastrophic)',

            # Required (tuned) integration -- FITTED, not derived
            't_required_thermal_units': t_required_corrected,
            'S_required': S_required,
            'damping_factor_tuned': damping_tuned,
            'm_eff_damped_tuned_eV': m_eff_damped_tuned,
            'gap_tuned_orders': gap_tuned,
            'tuned_status': 'FITTED (t_int chosen to match target)',

            # Target
            'target_eV': target_ev,

            # Overall assessment
            'mechanism_classification': 'FITTED',
            'honest_assessment': (
                "Sampler entropy damping CAN provide exponential mass suppression, "
                "but the integration timescale is not uniquely determined by topology. "
                f"Naive cosmic-age integration gives exp(-{integrated_entropy_naive/2:.2e}), "
                "catastrophically over-suppressing the mass to zero. Achieving exactly "
                f"44.5 orders requires t_int ~ {t_required_corrected:.0f} thermal time "
                "units, which lacks independent derivation. "
                "Gemini classification: FITTED."
            ),
        }

    # ===================================================================
    # MAIN EXECUTION
    # ===================================================================

    def compute_all(self) -> BridgeAxionEDEResult:
        """
        Execute full bridge axion EDE analysis.

        Steps:
            1. Compute KNP alignment (f_sub, f_eff, enhancement)
            2. Compute racetrack mass (T_min, V'', m_ind)
            3. Compute EDE evolution (m_eff, f_EDE, r_s, H0)
            4. Assess Hubble tension honestly

        Returns:
            BridgeAxionEDEResult with complete analysis.
        """
        # Step 1: KNP alignment
        knp = self.compute_knp_alignment()

        # Step 2: Racetrack mass
        racetrack = self.compute_racetrack_mass(knp.f_sub)

        # Step 3: EDE evolution
        ede = self.compute_ede_evolution(knp, racetrack)

        # Step 4: Assessment
        assessment = self.assess_hubble_tension(ede)

        return BridgeAxionEDEResult(
            knp=knp,
            racetrack=racetrack,
            ede=ede,
            status=assessment["status"],
            classification=assessment["classification"],
            honest_assessment=assessment["honest_assessment"],
        )

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute bridge axion EDE simulation."""
        result = self.compute_all()

        # Register outputs
        registry.set_param(
            path="bridge_ede.f_sub",
            value=result.knp.f_sub,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "M_Pl / k_gimel^6",
                "units": "GeV",
                "note": "Individual bridge axion decay constant"
            }
        )

        registry.set_param(
            path="bridge_ede.f_eff",
            value=result.knp.f_eff,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "f_sub * sqrt(N_ax * b3) * kappa_sampler",
                "units": "GeV",
                "note": "KNP-enhanced effective decay constant"
            }
        )

        registry.set_param(
            path="bridge_ede.enhancement",
            value=result.knp.enhancement,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "sqrt(12 * 24) * 2 = sqrt(288) * 2",
                "units": "dimensionless",
                "note": "KNP enhancement factor from 12 axions in b3=24 space"
            }
        )

        registry.set_param(
            path="bridge_ede.m_ind",
            value=result.racetrack.m_ind_ev,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "sqrt(V''(T_min)) * M_Pl",
                "units": "eV",
                "note": "Individual racetrack axion mass"
            }
        )

        registry.set_param(
            path="bridge_ede.m_eff",
            value=result.ede.m_eff_ev,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "m_ind / enhancement^2",
                "units": "eV",
                "note": "KNP-aligned effective axion mass"
            }
        )

        registry.set_param(
            path="bridge_ede.m_ede_target",
            value=self.m_ede_target_ev,
            source=self._metadata.id,
            status="INPUT",
            metadata={
                "derivation": "Poulin+ (2019) EDE target",
                "units": "eV",
                "note": "Target mass for EDE to peak at z~3500"
            }
        )

        registry.set_param(
            path="bridge_ede.mass_gap_orders",
            value=result.ede.mass_gap_orders,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "log10(m_eff / m_ede_target)",
                "units": "orders of magnitude",
                "note": "Remaining gap between KNP mass and EDE target"
            }
        )

        registry.set_param(
            path="bridge_ede.f_ede_peak",
            value=result.ede.f_ede_peak,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "rho_phi / rho_crit at z_peak",
                "units": "dimensionless",
                "note": "Peak EDE fraction (0 if mass too high)"
            }
        )

        registry.set_param(
            path="bridge_ede.H0_shift",
            value=result.ede.H0_shift,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "H0_Planck * (r_s_std / r_s_mod - 1)",
                "units": "km/s/Mpc",
                "note": "H0 shift from EDE (0 if mechanism fails)"
            }
        )

        registry.set_param(
            path="bridge_ede.status",
            value=result.status,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "classification": result.classification,
                "note": result.honest_assessment[:200]
            }
        )

        # Step 5: Entropy damping extension (Sprint 1)
        entropy_result = self.compute_m_eff_with_entropy_damping()

        # Register entropy-damped outputs
        registry.set_param(
            path="bridge_ede.entropy_damping.classification",
            value=entropy_result['mechanism_classification'],
            source=self._metadata.id,
            status="FITTED",
            metadata={
                "note": "Sampler entropy damping -- FITTED per Gemini debate",
                "Q_eff_trace": entropy_result['Q_eff_trace'],
                "entropy_rate": entropy_result['entropy_rate'],
                "t_required_thermal": entropy_result['t_required_thermal_units'],
            }
        )

        registry.set_param(
            path="bridge_ede.entropy_damping.m_eff_undamped",
            value=entropy_result['m_eff_undamped_eV'],
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "m_ind / Tr(Q_eff), Q_eff = Q_Leech + kappa*12",
                "units": "eV",
            }
        )

        return {
            "bridge_ede.f_sub": result.knp.f_sub,
            "bridge_ede.f_eff": result.knp.f_eff,
            "bridge_ede.enhancement": result.knp.enhancement,
            "bridge_ede.m_ind": result.racetrack.m_ind_ev,
            "bridge_ede.m_eff": result.ede.m_eff_ev,
            "bridge_ede.m_ede_target": self.m_ede_target_ev,
            "bridge_ede.mass_gap_orders": result.ede.mass_gap_orders,
            "bridge_ede.f_ede_peak": result.ede.f_ede_peak,
            "bridge_ede.H0_shift": result.ede.H0_shift,
            "bridge_ede.status": result.status,
            "_entropy_damping": entropy_result,
            "_knp_result": {
                "f_sub_GeV": result.knp.f_sub,
                "f_eff_GeV": result.knp.f_eff,
                "enhancement": result.knp.enhancement,
                "N_ax": result.knp.N_ax,
                "b3": result.knp.b3,
                "kappa_sampler": result.knp.kappa_sampler,
            },
            "_racetrack_result": {
                "T_min": result.racetrack.T_min,
                "V_min": result.racetrack.V_min,
                "V_double_prime": result.racetrack.V_double_prime,
                "m_ind_planck": result.racetrack.m_ind_planck,
                "m_ind_GeV": result.racetrack.m_ind_gev,
                "m_ind_eV": result.racetrack.m_ind_ev,
            },
            "_ede_result": {
                "m_eff_eV": result.ede.m_eff_ev,
                "mass_gap_orders": result.ede.mass_gap_orders,
                "f_ede_peak": result.ede.f_ede_peak,
                "z_peak": result.ede.z_peak,
                "r_s_standard_Mpc": result.ede.r_s_standard_mpc,
                "r_s_modified_Mpc": result.ede.r_s_modified_mpc,
                "H0_predicted_kmsMpc": result.ede.H0_predicted,
                "H0_shift_kmsMpc": result.ede.H0_shift,
            },
            "_assessment": {
                "status": result.status,
                "classification": result.classification,
                "honest_assessment": result.honest_assessment,
            },
        }

    # ===================================================================
    # FORMULAS
    # ===================================================================

    def get_formulas(self) -> List[Formula]:
        """Return formulas for bridge axion EDE derivation."""
        return [
            Formula(
                id="bridge-ede-f-sub-v24",
                label="(7.3)",
                latex=(
                    r"f_{\rm sub} = \frac{M_{\rm Pl}}{k_\gimel^6} "
                    r"\approx 3.5 \times 10^{12}\,\text{GeV}"
                ),
                plain_text="f_sub = M_Pl / k_gimel^6 ~ 3.5e12 GeV",
                category="DERIVED",
                description=(
                    "Individual bridge axion decay constant, identical to "
                    "the QCD axion f_a from axion_dm.py. Each of the 12 "
                    "bridge tori B_i^{2,0} carries an axion phi_i = Im(T_i) "
                    "with this sub-Planckian decay constant."
                ),
                inputParams=["geometry.k_gimel"],
                outputParams=["bridge_ede.f_sub"],
                input_params=["geometry.k_gimel"],
                output_params=["bridge_ede.f_sub"],
                derivation={
                    "steps": [
                        {
                            "description": "Individual axion from bridge torus",
                            "formula": r"\phi_i = \text{Im}(T_i),\quad T_i = \text{Vol}(B_i) + i\phi_i"
                        },
                        {
                            "description": "Decay constant from Planck scale suppression",
                            "formula": r"f_{\rm sub} = M_{\rm Pl}/k_\gimel^6 \approx 3.5 \times 10^{12}\,\text{GeV}"
                        }
                    ],
                    "references": [
                        "Svrcek & Witten (2006) arXiv:hep-th/0605206",
                        "Acharya et al. (2007) arXiv:hep-th/0606262"
                    ],
                    "method": "geometric_ansatz",
                    "parentFormulas": ["axion-decay-constant-v18"]
                },
                terms={
                    "M_Pl": "Planck mass = 1.22e19 GeV",
                    "k_gimel": "Holonomy warp factor = b3/2 + 1/pi ~ 12.318",
                    "T_i": "Complexified Kahler modulus of bridge i"
                }
            ),
            Formula(
                id="bridge-ede-knp-enhancement-v24",
                label="(7.4)",
                latex=(
                    r"\mathcal{E}_{\rm KNP} = \sqrt{N_{\rm ax} \cdot b_3} "
                    r"\cdot \kappa_{\rm sampler} = \sqrt{12 \times 24} \times 2 "
                    r"\approx 33.94"
                ),
                plain_text="enhancement = sqrt(N_ax * b3) * kappa_sampler = sqrt(288) * 2 ~ 33.94",
                category="DERIVED",
                description=(
                    "KNP enhancement factor from alignment of 12 bridge axions "
                    "in b3=24 dimensional instanton charge space. The sqrt(N_ax*b3) "
                    "factor arises from the alignment matrix determinant of 12 "
                    "axions in the 24D Leech lattice ambient space. The factor "
                    "kappa_sampler=2=dim(S^{2,0}) accounts for the sampler sector "
                    "contribution, topologically fixed by M^{27}=24+1+2."
                ),
                inputParams=["topology.elder_kads"],
                outputParams=["bridge_ede.enhancement"],
                input_params=["topology.elder_kads"],
                output_params=["bridge_ede.enhancement"],
                derivation={
                    "steps": [
                        {
                            "description": "KNP alignment of N axions",
                            "formula": r"f_{\rm eff} \sim f_{\rm sub} \times \sqrt{N_1 N_2}"
                        },
                        {
                            "description": "In G2: N_1=N_ax=12 axions, N_2=b3=24 charge dimensions",
                            "formula": r"\sqrt{N_{\rm ax} \cdot b_3} = \sqrt{12 \times 24} = \sqrt{288} \approx 16.97"
                        },
                        {
                            "description": "Sampler sector multiplier (topologically fixed)",
                            "formula": r"\kappa_{\rm sampler} = \dim(S^{2,0}) = 2"
                        },
                        {
                            "description": "Total enhancement",
                            "formula": r"\mathcal{E}_{\rm KNP} = \sqrt{288} \times 2 \approx 33.94"
                        }
                    ],
                    "references": [
                        "Kim, Nilles, Peloso (2005) arXiv:hep-ph/0409138",
                        "Bachlechner et al. (2015) arXiv:1412.7988"
                    ],
                    "method": "knp_alignment",
                    "parentFormulas": ["bridge-ede-f-sub-v24"]
                },
                terms={
                    "N_ax": "Number of bridge axions = 12 = b3/2",
                    "b_3": "Third Betti number = 24",
                    "kappa_sampler": "Sampler dimensionality = dim(S^{2,0}) = 2"
                }
            ),
            Formula(
                id="bridge-ede-f-eff-v24",
                label="(7.5)",
                latex=(
                    r"f_{\rm eff} = f_{\rm sub} \cdot \mathcal{E}_{\rm KNP} "
                    r"= \frac{M_{\rm Pl}}{k_\gimel^6} \cdot \sqrt{N_{\rm ax} b_3} "
                    r"\cdot \kappa_{\rm sampler} \approx 1.19 \times 10^{14}\,\text{GeV}"
                ),
                plain_text="f_eff = f_sub * sqrt(N_ax*b3) * kappa_sampler ~ 1.19e14 GeV",
                category="DERIVED",
                description=(
                    "Effective axion decay constant after KNP alignment. "
                    "Enhanced by factor ~34 over the individual f_sub, but "
                    "still sub-Planckian (f_eff/M_Pl ~ 10^{-5}). This is "
                    "insufficient to produce EDE-scale masses from racetrack "
                    "potentials. The gap is ~46 orders of magnitude."
                ),
                inputParams=["bridge_ede.f_sub", "bridge_ede.enhancement"],
                outputParams=["bridge_ede.f_eff"],
                input_params=["bridge_ede.f_sub", "bridge_ede.enhancement"],
                output_params=["bridge_ede.f_eff"],
                derivation={
                    "steps": [
                        {
                            "description": "Combine individual decay constant with enhancement",
                            "formula": (
                                r"f_{\rm eff} = 3.48 \times 10^{12}\,\text{GeV} "
                                r"\times 33.94 \approx 1.18 \times 10^{14}\,\text{GeV}"
                            )
                        }
                    ],
                    "references": [
                        "Kim, Nilles, Peloso (2005) arXiv:hep-ph/0409138"
                    ],
                    "method": "knp_alignment",
                    "parentFormulas": [
                        "bridge-ede-f-sub-v24",
                        "bridge-ede-knp-enhancement-v24"
                    ]
                },
                terms={
                    "f_sub": "Individual decay constant ~ 3.5e12 GeV",
                    "E_KNP": "KNP enhancement ~ 33.94"
                }
            ),
            Formula(
                id="bridge-ede-mass-gap-v24",
                label="(7.6)",
                latex=(
                    r"m_{\rm eff} = \frac{m_{\rm ind}}{\mathcal{E}_{\rm KNP}^2} "
                    r"\sim \frac{10^{22}\,\text{eV}}{1152} \sim 10^{19}\,\text{eV}"
                    r"\quad \Rightarrow \quad "
                    r"\Delta = \log_{10}\!\left(\frac{m_{\rm eff}}{m_{\rm EDE}}\right) "
                    r"\sim 46"
                ),
                plain_text=(
                    "m_eff = m_ind / enhancement^2 ~ 10^22/1152 ~ 10^19 eV; "
                    "gap = log10(10^19 / 10^-27) ~ 46 orders"
                ),
                category="DERIVED",
                description=(
                    "Mass gap assessment for bridge axion EDE. The KNP mechanism "
                    "suppresses the racetrack mass by 1/enhancement^2 ~ 1/1152, "
                    "achieving ~3 orders of suppression. However, the remaining "
                    "gap to the EDE target mass (10^{-27} eV) is ~46 orders of "
                    "magnitude. This is an honest assessment: the KNP architecture "
                    "is sound but quantitatively insufficient for EDE."
                ),
                inputParams=["bridge_ede.m_ind", "bridge_ede.enhancement"],
                outputParams=["bridge_ede.m_eff", "bridge_ede.mass_gap_orders"],
                input_params=["bridge_ede.m_ind", "bridge_ede.enhancement"],
                output_params=["bridge_ede.m_eff", "bridge_ede.mass_gap_orders"],
                derivation={
                    "steps": [
                        {
                            "description": "Racetrack mass from F-term potential curvature",
                            "formula": r"m_{\rm ind}^2 = V''(T_{\rm min}), \quad m_{\rm ind} \sim 10^{13}\,\text{GeV}"
                        },
                        {
                            "description": "KNP mass suppression",
                            "formula": r"m_{\rm eff} = m_{\rm ind} / \mathcal{E}_{\rm KNP}^2"
                        },
                        {
                            "description": "Mass gap to EDE target",
                            "formula": (
                                r"\Delta = \log_{10}(m_{\rm eff} / m_{\rm EDE}) "
                                r"\sim \log_{10}(10^{19}/10^{-27}) \sim 46"
                            )
                        }
                    ],
                    "references": [
                        "Poulin, Smith, Karwal, Kamionkowski (2019) arXiv:1811.04083",
                        "Kim, Nilles, Peloso (2005) arXiv:hep-ph/0409138"
                    ],
                    "method": "knp_mass_suppression",
                    "parentFormulas": [
                        "bridge-ede-knp-enhancement-v24",
                        "bridge-ede-f-sub-v24"
                    ]
                },
                terms={
                    "m_ind": "Individual racetrack mass ~ 10^13 GeV",
                    "E_KNP": "KNP enhancement ~ 33.94",
                    "m_EDE": "Target EDE mass ~ 10^{-27} eV",
                    "Delta": "Mass gap in orders of magnitude"
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="bridge_ede.f_sub",
                name="Individual Bridge Axion Decay Constant",
                units="GeV",
                status="DERIVED",
                description=(
                    "Individual axion decay constant from G2 geometry: "
                    "f_sub = M_Pl/k_gimel^6 ~ 3.5e12 GeV."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.f_eff",
                name="KNP-Enhanced Effective Decay Constant",
                units="GeV",
                status="DERIVED",
                description=(
                    "Effective decay constant after KNP alignment of 12 "
                    "bridge axions: f_eff = f_sub * sqrt(N_ax*b3) * kappa_sampler "
                    "~ 1.19e14 GeV."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.enhancement",
                name="KNP Enhancement Factor",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "KNP alignment enhancement: sqrt(12*24)*2 ~ 33.94. "
                    "All factors are topologically fixed."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.m_ind",
                name="Individual Racetrack Axion Mass",
                units="eV",
                status="DERIVED",
                description=(
                    "Individual axion mass from racetrack potential curvature "
                    "at stabilized minimum."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.m_eff",
                name="KNP-Aligned Effective Axion Mass",
                units="eV",
                status="DERIVED",
                description=(
                    "Effective mass after KNP suppression: m_ind/enhancement^2. "
                    "Still ~46 orders above EDE target."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.m_ede_target",
                name="EDE Target Mass",
                units="eV",
                status="INPUT",
                description=(
                    "Target axion mass for Early Dark Energy to peak at "
                    "z ~ 3500 (Poulin+ 2019)."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.mass_gap_orders",
                name="Mass Gap to EDE Target",
                units="orders of magnitude",
                status="DERIVED",
                description=(
                    "Remaining gap between KNP-aligned mass and EDE target: "
                    "~46 orders. Honest assessment of mechanism limitation."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.f_ede_peak",
                name="Peak EDE Fraction",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Peak Early Dark Energy fraction at z ~ 3500. "
                    "Effectively zero due to mass gap."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.H0_shift",
                name="Hubble Constant Shift",
                units="km/s/Mpc",
                status="DERIVED",
                description=(
                    "Predicted H0 shift from EDE. Effectively zero "
                    "due to mass gap (~46 orders)."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="bridge_ede.status",
                name="Mechanism Status",
                units="categorical",
                status="DERIVED",
                description=(
                    "PARTIAL: KNP alignment provides architectural coherence "
                    "and ~3 orders of suppression but falls short of EDE "
                    "target by ~46 orders of magnitude."
                ),
                no_experimental_value=True
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for paper."""
        return SectionContent(
            section_id="7.2",
            subsection_id="7.2.1",
            title="Bridge Axion Early Dark Energy",
            abstract=(
                "We apply KNP alignment to the 12 bridge axions of "
                "M^{27}(24,1,2) to seek an ultralight axion for Early Dark "
                "Energy. The enhancement factor sqrt(N_ax*b3)*kappa_sampler ~ 34 "
                "provides ~3 orders of mass suppression, but the remaining gap "
                "to EDE-relevant masses (~10^{-27} eV) is ~46 orders of magnitude. "
                "The mechanism is architecturally coherent but quantitatively "
                "insufficient. Classification: PARTIAL."
            ),
            blocks=[],
        )

    # ===================================================================
    # CONTENT GENERATION (detailed)
    # ===================================================================

    def get_content(self, result: Optional[BridgeAxionEDEResult] = None) -> SectionContent:
        """Generate paper section content."""
        if result is None:
            result = self.compute_all()

        blocks = [
            ContentBlock(
                type="text",
                content=(
                    "The 12 bridge tori $B_i^{2,0}$ of $M^{27}(24,1,2)$ each carry "
                    "an axion field $\\phi_i = \\text{Im}(T_i)$ from the racetrack "
                    "superpotential. We apply the Kim-Nilles-Peloso (KNP) alignment "
                    "mechanism to these 12 axions, seeking an effective ultralight "
                    "axion as a candidate for Early Dark Energy (EDE) to address "
                    "the Hubble tension."
                ),
            ),
            ContentBlock(
                type="text",
                content=(
                    f"The individual decay constant $f_{{\\rm sub}} = M_{{\\rm Pl}}/k_\\gimel^6 "
                    f"\\approx {result.knp.f_sub:.2e}$ GeV is enhanced by the KNP factor "
                    f"$\\mathcal{{E}}_{{\\rm KNP}} = \\sqrt{{N_{{\\rm ax}} \\cdot b_3}} \\cdot "
                    f"\\kappa_{{\\rm sampler}} = \\sqrt{{288}} \\times 2 \\approx "
                    f"{result.knp.enhancement:.2f}$ to give $f_{{\\rm eff}} \\approx "
                    f"{result.knp.f_eff:.2e}$ GeV."
                ),
            ),
            ContentBlock(
                type="text",
                content=(
                    f"The racetrack-stabilized modulus $T_{{\\rm min}} = "
                    f"{result.racetrack.T_min:.4f}$ yields an individual axion mass "
                    f"$m_{{\\rm ind}} \\approx {result.racetrack.m_ind_ev:.2e}$ eV. "
                    f"KNP suppression by $1/\\mathcal{{E}}^2 \\approx 1/"
                    f"{result.knp.enhancement**2:.0f}$ gives $m_{{\\rm eff}} \\approx "
                    f"{result.ede.m_eff_ev:.2e}$ eV."
                ),
            ),
            ContentBlock(
                type="text",
                content=(
                    f"\\textbf{{Honest assessment:}} The EDE target mass is "
                    f"$m_{{\\rm EDE}} \\sim 10^{{-27}}$ eV. The remaining gap is "
                    f"$\\Delta \\approx {result.ede.mass_gap_orders:.1f}$ orders of "
                    f"magnitude. The KNP mechanism provides architectural coherence "
                    f"(all 12 bridge axions participate via Leech lattice alignment) "
                    f"and $\\sim 3$ orders of mass suppression, but falls short of "
                    f"the EDE target by $\\sim {result.ede.mass_gap_orders:.0f}$ orders. "
                    f"Classification: \\textbf{{{result.classification}}}."
                ),
            ),
        ]

        return SectionContent(
            section_id="7.2",
            title="Bridge Axion Early Dark Energy",
            blocks=blocks,
        )


# =====================================================================
# Module-level convenience function
# =====================================================================

def compute_bridge_axion_ede() -> BridgeAxionEDEResult:
    """Compute bridge axion EDE analysis (standalone usage)."""
    sim = BridgeAxionEDE()
    return sim.compute_all()


# =====================================================================
# CLI entry point
# =====================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("Bridge Axion EDE: KNP Alignment for Hubble Tension")
    print("=" * 72)

    sim = BridgeAxionEDE()
    result = sim.compute_all()

    print(f"\n--- KNP Alignment ---")
    print(f"  f_sub (individual):   {result.knp.f_sub:.4e} GeV")
    print(f"  Enhancement factor:   {result.knp.enhancement:.4f}")
    print(f"    sqrt(N_ax * b3):    {math.sqrt(result.knp.N_ax * result.knp.b3):.4f}")
    print(f"    kappa_sampler:      {result.knp.kappa_sampler}")
    print(f"  f_eff (KNP-aligned):  {result.knp.f_eff:.4e} GeV")
    print(f"  f_eff / M_Pl:         {result.knp.f_eff / 1.22e19:.4e}")

    print(f"\n--- Racetrack Mass ---")
    print(f"  T_min (stabilized):   {result.racetrack.T_min:.6f}")
    print(f"  V_min:                {result.racetrack.V_min:.6e}")
    print(f"  V'' at minimum:       {result.racetrack.V_double_prime:.6e}")
    print(f"  m_ind (Planck):       {result.racetrack.m_ind_planck:.6e}")
    print(f"  m_ind (GeV):          {result.racetrack.m_ind_gev:.4e}")
    print(f"  m_ind (eV):           {result.racetrack.m_ind_ev:.4e}")

    print(f"\n--- EDE Evolution ---")
    print(f"  m_eff (KNP-aligned):  {result.ede.m_eff_ev:.4e} eV")
    print(f"  m_EDE target:         {result.ede.m_ede_target_ev:.4e} eV")
    print(f"  Mass gap:             {result.ede.mass_gap_orders:.1f} orders of magnitude")
    print(f"  f_EDE peak:           {result.ede.f_ede_peak:.4e}")
    print(f"  z_peak:               {result.ede.z_peak:.0f}")
    print(f"  r_s (standard):       {result.ede.r_s_standard_mpc:.2f} Mpc")
    print(f"  r_s (modified):       {result.ede.r_s_modified_mpc:.2f} Mpc")
    print(f"  H0 predicted:         {result.ede.H0_predicted:.2f} km/s/Mpc")
    print(f"  H0 shift:             {result.ede.H0_shift:.4f} km/s/Mpc")

    print(f"\n--- Assessment ---")
    print(f"  Status:               {result.status}")
    print(f"  Classification:       {result.classification}")
    print(f"\n{result.honest_assessment}")

    # Sprint 1: Entropy damping extension
    print(f"\n{'=' * 72}")
    print(f"Sprint 1: Sampler Entropy Damping Extension")
    print(f"{'=' * 72}")

    ed = sim.compute_m_eff_with_entropy_damping()
    print(f"\n--- Enhanced Alignment ---")
    print(f"  Q_Leech trace:        {ed['Q_leech_trace']}")
    print(f"  Q_eff trace:          {ed['Q_eff_trace']}")
    print(f"  f_eff (enhanced):     {ed['f_eff_enhanced_GeV']:.4e} GeV")

    print(f"\n--- Undamped (Q_eff only) ---")
    print(f"  m_eff_undamped:       {ed['m_eff_undamped_eV']:.4e} eV")
    print(f"  Gap (undamped):       {ed['gap_undamped_orders']:.1f} orders")

    print(f"\n--- Entropy Parameters ---")
    print(f"  Entropy rate:         {ed['entropy_rate']:.4f}")
    print(f"  Entropy gradient:     {ed['entropy_gradient_full']}")

    print(f"\n--- Naive Integration (full cosmic age) ---")
    print(f"  t_thermal (naive):    {ed['t_thermal_naive']:.4e}")
    print(f"  Integrated entropy:   {ed['integrated_entropy_naive']:.4e}")
    print(f"  Damping factor:       {ed['damping_factor_naive']}")
    print(f"  m_eff_damped:         {ed['m_eff_damped_naive_eV']}")
    print(f"  Status:               {ed['naive_status']}")

    print(f"\n--- Required (Tuned) Integration ---")
    print(f"  t_required:           {ed['t_required_thermal_units']:.1f} thermal units")
    print(f"  S_required:           {ed['S_required']:.2f}")
    print(f"  m_eff_damped (tuned): {ed['m_eff_damped_tuned_eV']:.4e} eV")
    print(f"  Gap (tuned):          {ed['gap_tuned_orders']:.1f} orders")
    print(f"  Status:               {ed['tuned_status']}")

    print(f"\n--- Gemini Consensus ---")
    print(f"  Classification:       {ed['mechanism_classification']}")
    print(f"  {ed['honest_assessment']}")

    print(f"\n{'=' * 72}")
    print(f"VERDICT: {result.status} -- KNP alignment provides ~3 orders")
    print(f"  of mass suppression but falls short of EDE by")
    print(f"  ~{result.ede.mass_gap_orders:.0f} orders of magnitude.")
    print(f"  Entropy damping: FITTED (not DERIVED). Integration timescale")
    print(f"  not uniquely determined by topology.")
    print(f"{'=' * 72}")
