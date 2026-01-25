#!/usr/bin/env python3
"""
Decoherence Protection Mechanisms for Orch-OR v18.0
====================================================

Licensed under the MIT License. See LICENSE file for details.

Addresses the "Warm Brain Problem": standard physics predicts tau_dec ~ 10^-13 s
for biological systems at 310K, but Orch-OR requires tau ~ 10^-2 s (100x neural
timescale of 25ms). This is a 10^11 enhancement factor needed.

This simulation implements and critically evaluates three protection mechanisms:

1. DEBYE LAYER SHIELDING
   - Ordered water shell around microtubules
   - Debye screening: V(r) = (Q/r) * exp(-r/lambda_D)
   - Lambda_D ~ 0.7 nm in cytoplasm (ionic strength ~150 mM)
   - Can provide ~10^2 protection factor

2. G2 TOPOLOGICAL PROTECTION
   - Holonomy restriction: G2 subset SO(7) limits decoherence channels
   - Cycle isolation: 3-cycles separated by d/R ~ 0.12
   - Flux quantization provides topological stability
   - Theoretical enhancement: ~10^2-10^3

3. FROHLICH CONDENSATION
   - Collective dipole oscillation in metabolically driven system
   - Critical frequency: omega_F ~ 10^12 Hz (THz range)
   - Bose-Einstein-like condensation of vibrational modes
   - Can provide ~10^3-10^5 enhancement if achieved

HONEST ASSESSMENT:
- Total achievable protection: ~10^6 to 10^8
- Still short of required 10^11 by 10^3-10^5
- This represents a significant gap in Orch-OR theory
- Additional mechanisms or parameter refinement needed

References:
- Tegmark (2000): Importance of quantum decoherence in brain processes
- Hameroff & Penrose (2014): Consciousness in the universe
- Frohlich (1968): Long-range coherence and energy storage in biological systems
- Craddock et al. (2017): Anesthetic alterations of collective terahertz oscillations

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from decimal import Decimal, getcontext
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import sys
from pathlib import Path

# High precision for fundamental constant calculations
getcontext().prec = 50

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

# Import base classes if available
try:
    from simulations.base import (
        SimulationBase,
        SimulationMetadata,
        ContentBlock,
        SectionContent,
        Formula,
        Parameter,
        PMRegistry,
    )
    SCHEMA_AVAILABLE = True
except ImportError:
    SCHEMA_AVAILABLE = False

# Try to import FormulasRegistry
try:
    from core.FormulasRegistry import get_registry
    _REG = get_registry()
    REGISTRY_AVAILABLE = True
except ImportError:
    _REG = None
    REGISTRY_AVAILABLE = False


# =============================================================================
# PHYSICAL CONSTANTS (CODATA 2022)
# =============================================================================

# Fundamental Constants
HBAR = 1.054571817e-34      # J*s - Reduced Planck constant
K_B = 1.380649e-23          # J/K - Boltzmann constant
C = 2.99792458e8            # m/s - Speed of light
G_NEWTON = 6.67430e-11      # m^3/(kg*s^2) - Gravitational constant
EPSILON_0 = 8.8541878e-12   # F/m - Vacuum permittivity
E_CHARGE = 1.602176634e-19  # C - Elementary charge

# Derived Constants
K_COULOMB = 1 / (4 * np.pi * EPSILON_0)  # N*m^2/C^2

# Biological Parameters
T_BRAIN = 310.0             # K - Brain temperature (~37C)
M_TUBULIN = 1.8e-22         # kg - Tubulin dimer mass (~110 kDa)
R_TUBULIN = 4.0e-9          # m - Tubulin radius (~4 nm)
L_TUBULIN = 8.0e-9          # m - Tubulin length (~8 nm)

# Cytoplasmic Parameters
IONIC_STRENGTH = 0.15       # M - Typical cytoplasmic ionic strength (~150 mM)
DIELECTRIC_WATER = 80.0     # Relative permittivity of water at 310K
VISCOSITY_CYTO = 0.01       # Pa*s - Cytoplasmic viscosity

# G2 Topology Parameters (via FormulasRegistry SSoT)
B3 = _REG.elder_kads if REGISTRY_AVAILABLE else 24                     # Third Betti number
CHI_EFF = _REG.qedem_chi_sum if REGISTRY_AVAILABLE else 144            # Effective Euler characteristic
CYCLE_SEPARATION = 0.12     # d/R ratio for TCS G2


@dataclass
class DecoherenceAnalysis:
    """Container for decoherence analysis results."""
    mechanism: str
    protection_factor: float
    raw_decoherence_time_s: float
    protected_decoherence_time_s: float
    description: str
    limitations: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)


class DebyeLayerShielding:
    """
    Debye Layer Shielding Model for Microtubule Protection.

    The Debye-Huckel screening model describes how ions in solution
    create a screening layer that shields electrostatic interactions.

    Around microtubules, ordered water forms a "exclusion zone" (EZ water)
    that may provide additional shielding from thermal fluctuations.

    Key Physics:
    - Debye length: lambda_D = sqrt(epsilon_0 * epsilon_r * k_B * T / (2 * N_A * e^2 * I))
    - Screened potential: V(r) = (Q/r) * exp(-r/lambda_D)
    - Protection factor from screening: P ~ exp(r_eff / lambda_D)

    LIMITATIONS:
    - Standard Debye-Huckel only provides ~10^1-10^2 protection
    - EZ water claims are controversial (Pollack et al.)
    - Does not address phonon/vibrational decoherence
    """

    def __init__(self, temperature_k: float = T_BRAIN, ionic_strength_m: float = IONIC_STRENGTH):
        """
        Initialize Debye layer model.

        Args:
            temperature_k: Temperature in Kelvin
            ionic_strength_m: Ionic strength in Molar
        """
        self.T = temperature_k
        self.I = ionic_strength_m
        self.kT = K_B * temperature_k

    def calculate_debye_length(self) -> float:
        """
        Calculate Debye screening length in cytoplasm.

        lambda_D = sqrt(epsilon_0 * epsilon_r * k_B * T / (2 * N_A * e^2 * I))

        For I = 150 mM at 310K: lambda_D ~ 0.7-0.8 nm

        Returns:
            Debye length in meters
        """
        N_A = 6.02214076e23  # Avogadro's number

        numerator = EPSILON_0 * DIELECTRIC_WATER * K_B * self.T
        denominator = 2 * N_A * (E_CHARGE ** 2) * self.I * 1000  # Convert M to mol/m^3

        lambda_D = np.sqrt(numerator / denominator)
        return lambda_D

    def screened_potential(self, charge_c: float, distance_m: float) -> float:
        """
        Calculate screened Coulomb potential at distance r.

        V(r) = (Q / 4*pi*epsilon_0*epsilon_r*r) * exp(-r/lambda_D)

        Args:
            charge_c: Charge in Coulombs
            distance_m: Distance from charge in meters

        Returns:
            Potential in Volts
        """
        lambda_D = self.calculate_debye_length()

        prefactor = charge_c / (4 * np.pi * EPSILON_0 * DIELECTRIC_WATER * distance_m)
        screening = np.exp(-distance_m / lambda_D)

        return prefactor * screening

    def calculate_protection_factor(self, effective_radius_m: float = R_TUBULIN) -> float:
        """
        Calculate protection factor from Debye screening.

        The screening exponentially suppresses long-range interactions.
        For a system of size r_eff, screening provides protection:

        P_Debye ~ exp(r_eff / lambda_D) for r_eff > lambda_D

        HONEST ASSESSMENT:
        - For r_eff ~ 4 nm and lambda_D ~ 0.7 nm: P ~ exp(5.7) ~ 300
        - This is a factor of ~10^2, not 10^11
        - Debye screening alone is insufficient

        Args:
            effective_radius_m: Effective radius of protected region

        Returns:
            Protection factor (dimensionless)
        """
        lambda_D = self.calculate_debye_length()

        # Basic screening factor
        if effective_radius_m > lambda_D:
            protection = np.exp(effective_radius_m / lambda_D)
        else:
            # For small systems, screening is less effective
            protection = 1.0 + (effective_radius_m / lambda_D)

        # Cap at physically reasonable values
        # Even with EZ water claims, protection > 10^4 is unrealistic
        max_protection = 1e4
        return min(protection, max_protection)

    def analyze(self, raw_decoherence_time_s: float) -> DecoherenceAnalysis:
        """
        Complete Debye shielding analysis.

        Args:
            raw_decoherence_time_s: Unprotected decoherence time

        Returns:
            DecoherenceAnalysis with results
        """
        lambda_D = self.calculate_debye_length()
        protection = self.calculate_protection_factor()
        protected_time = raw_decoherence_time_s * protection

        return DecoherenceAnalysis(
            mechanism="Debye Layer Shielding",
            protection_factor=protection,
            raw_decoherence_time_s=raw_decoherence_time_s,
            protected_decoherence_time_s=protected_time,
            description=(
                f"Debye-Huckel screening with lambda_D = {lambda_D*1e9:.2f} nm. "
                f"Protection factor ~ {protection:.1f} (10^{np.log10(protection):.1f}). "
                f"Protected time: {protected_time:.2e} s ({protected_time*1e12:.2f} ps)."
            ),
            limitations=[
                "Standard Debye theory provides only ~10^2 protection",
                "EZ water claims (Pollack) are controversial and not established",
                "Does not protect against phonon/vibrational modes",
                "Assumes static screening - dynamic effects may reduce efficacy"
            ],
            assumptions=[
                "Cytoplasmic ionic strength ~ 150 mM",
                "Temperature ~ 310 K (body temperature)",
                "Dielectric constant of water ~ 80",
                "Effective radius ~ tubulin size (4 nm)"
            ],
            references=[
                "Debye & Huckel (1923) - Electrolyte theory",
                "Pollack (2013) - Fourth phase of water (controversial)",
                "Tegmark (2000) - Decoherence in brain processes"
            ]
        )


class G2TopologicalProtection:
    """
    G2 Topological Protection Model.

    G2 manifolds (7-dimensional spaces with exceptional holonomy) may provide
    geometric protection for quantum states through:

    1. HOLONOMY RESTRICTION
       - G2 is a subgroup of SO(7): dim(G2)=14 vs dim(SO(7))=21
       - Restricts allowed decoherence channels
       - Factor: 21/14 = 1.5

    2. CYCLE ISOLATION
       - 3-cycles in G2 are topologically protected
       - Separation d/R ~ 0.12 provides exponential suppression
       - Factor: exp(2*pi*d/R) ~ 2.13

    3. FLUX QUANTIZATION
       - M-theory flux on 3-cycles is quantized
       - Provides discrete stability against continuous deformations
       - Factor: chi_eff / b3 = 144/24 = 6

    Combined G2 protection: ~19 (10^1.3)

    LIMITATIONS:
    - Highly speculative - G2 manifolds in biology are unproven
    - Even generous estimates give only ~10^2-10^3
    - Physical mechanism for topology-decoherence coupling unclear
    """

    def __init__(self, b3: int = B3, chi_eff: int = CHI_EFF, cycle_sep: float = CYCLE_SEPARATION):
        """
        Initialize G2 protection model.

        Args:
            b3: Third Betti number
            chi_eff: Effective Euler characteristic
            cycle_sep: Cycle separation ratio d/R
        """
        self.b3 = b3
        self.chi_eff = chi_eff
        self.cycle_sep = cycle_sep

        # Use registry values if available
        if REGISTRY_AVAILABLE and _REG is not None:
            self.b3 = _REG.elder_kads
            self.k_gimel = _REG.demiurgic_coupling
        else:
            self.k_gimel = b3 / 2 + 1 / np.pi  # ~ 12.318

    def holonomy_suppression(self) -> Tuple[float, str]:
        """
        Calculate holonomy suppression factor.

        G2 holonomy restricts the allowed parallel transport operations,
        reducing the number of available decoherence channels.

        dim(SO(7)) = 7*6/2 = 21
        dim(G2) = 14

        Suppression factor: 21/14 = 1.5

        Returns:
            (factor, explanation)
        """
        dim_SO7 = 21
        dim_G2 = 14
        factor = dim_SO7 / dim_G2

        explanation = (
            f"Holonomy restriction: G2 subset SO(7) reduces interaction channels. "
            f"dim(SO(7))/dim(G2) = {dim_SO7}/{dim_G2} = {factor:.3f}"
        )

        return factor, explanation

    def cycle_isolation(self) -> Tuple[float, str]:
        """
        Calculate exponential suppression from 3-cycle separation.

        On G2 manifolds, 3-cycles (on which flux is quantized) are
        topologically separated. Interactions between cycles are
        suppressed exponentially with separation distance.

        P_cycle = exp(2*pi*d/R)

        For d/R = 0.12: P_cycle ~ 2.13

        Returns:
            (factor, explanation)
        """
        factor = np.exp(2 * np.pi * self.cycle_sep)

        explanation = (
            f"Cycle isolation: 3-cycles separated by d/R = {self.cycle_sep}. "
            f"exp(2*pi*{self.cycle_sep}) = {factor:.3f}"
        )

        return factor, explanation

    def flux_quantization(self) -> Tuple[float, str]:
        """
        Calculate protection from flux quantization.

        M-theory flux on G2 3-cycles is quantized in units of the
        Euler characteristic. This provides topological stability.

        P_flux = chi_eff / b3 = 144/24 = 6

        Returns:
            (factor, explanation)
        """
        factor = self.chi_eff / self.b3

        explanation = (
            f"Flux quantization: chi_eff/b3 = {self.chi_eff}/{self.b3} = {factor:.1f}"
        )

        return factor, explanation

    def enhanced_g2_protection(self) -> Tuple[float, str]:
        """
        Calculate enhanced protection using k_gimel warp factor.

        In PM framework, the demiurgic coupling k_gimel provides
        additional geometric enhancement for gravitational effects.

        k_gimel = b3/2 + 1/pi ~ 12.318

        This may enhance G2 topological protection.

        Returns:
            (factor, explanation)
        """
        explanation = (
            f"k_gimel warp factor: {self.k_gimel:.4f} from G2 geometry"
        )

        return self.k_gimel, explanation

    def calculate_total_protection(self, use_enhanced: bool = True) -> float:
        """
        Calculate combined G2 protection factor.

        Standard: P_G2 = P_holonomy * P_cycle * P_flux ~ 19
        Enhanced: P_G2 = Standard * k_gimel ~ 240

        HONEST ASSESSMENT:
        - Standard G2 protection: ~10^1.3 (factor of 19)
        - Enhanced (with k_gimel): ~10^2.4 (factor of 240)
        - Even enhanced is far from 10^11 requirement

        Args:
            use_enhanced: Whether to include k_gimel enhancement

        Returns:
            Total protection factor
        """
        hol, _ = self.holonomy_suppression()
        cyc, _ = self.cycle_isolation()
        flux, _ = self.flux_quantization()

        protection = hol * cyc * flux

        if use_enhanced:
            protection *= self.k_gimel

        return protection

    def analyze(self, raw_decoherence_time_s: float, use_enhanced: bool = True) -> DecoherenceAnalysis:
        """
        Complete G2 topological protection analysis.

        Args:
            raw_decoherence_time_s: Unprotected decoherence time
            use_enhanced: Whether to include k_gimel enhancement

        Returns:
            DecoherenceAnalysis with results
        """
        protection = self.calculate_total_protection(use_enhanced)
        protected_time = raw_decoherence_time_s * protection

        hol, hol_desc = self.holonomy_suppression()
        cyc, cyc_desc = self.cycle_isolation()
        flux, flux_desc = self.flux_quantization()

        return DecoherenceAnalysis(
            mechanism="G2 Topological Protection",
            protection_factor=protection,
            raw_decoherence_time_s=raw_decoherence_time_s,
            protected_decoherence_time_s=protected_time,
            description=(
                f"G2 holonomy protection combining: "
                f"Holonomy ({hol:.2f}) x Cycle ({cyc:.2f}) x Flux ({flux:.2f})"
                + (f" x k_gimel ({self.k_gimel:.2f})" if use_enhanced else "") +
                f" = {protection:.1f} (10^{np.log10(protection):.1f}). "
                f"Protected time: {protected_time:.2e} s."
            ),
            limitations=[
                "G2 manifolds in biology are highly speculative",
                "Physical mechanism for topology-decoherence coupling is unclear",
                "Even enhanced protection gives only ~10^2, not 10^11",
                "k_gimel enhancement is theoretical, not experimentally verified"
            ],
            assumptions=[
                "G2 holonomy is relevant to microtubule geometry",
                "Cycle separation d/R ~ 0.12 from TCS geometry",
                "Flux quantization applies at biological scales",
                "k_gimel from PM framework is applicable"
            ],
            references=[
                "Joyce (2000) - Compact manifolds with G2 holonomy",
                "Acharya et al. (2021) - G2 physics",
                "PM v17.2 - G2 geometric anchors"
            ]
        )


class FrohlichCondensation:
    """
    Frohlich Condensation Model for Quantum Coherence.

    Herbert Frohlich (1968) proposed that metabolically driven biological
    systems could exhibit Bose-Einstein-like condensation of dipole
    oscillations at THz frequencies.

    Key Physics:
    - Dipole oscillation frequency: omega_F ~ 10^12 Hz (THz)
    - Condensation threshold: Energy pumping rate > thermal dissipation
    - Collective mode emerges below critical "Frohlich temperature"

    If achieved, Frohlich condensation could provide:
    - Coherent superposition of N~10^9 oscillators
    - Protection factor: sqrt(N) to N depending on mechanism
    - Potential enhancement: 10^3 to 10^9

    LIMITATIONS:
    - Experimental evidence is controversial and inconsistent
    - Requires significant metabolic energy pumping
    - Brain may not sustain required energy flux
    - Craddock et al. (2017) found evidence, but not definitive
    """

    # Frohlich parameters
    OMEGA_FROHLICH = 1e12           # Hz - THz oscillation frequency
    DIPOLE_MOMENT = 100 * 3.33564e-30  # C*m - Typical protein dipole (~100 Debye)

    def __init__(self, temperature_k: float = T_BRAIN, n_oscillators: int = int(1e9)):
        """
        Initialize Frohlich condensation model.

        Args:
            temperature_k: Temperature in Kelvin
            n_oscillators: Number of coupled oscillators
        """
        self.T = temperature_k
        self.N = n_oscillators
        self.kT = K_B * temperature_k

        # Thermal energy at THz
        self.E_thermal = K_B * temperature_k

        # Frohlich phonon energy
        self.E_frohlich = HBAR * self.OMEGA_FROHLICH

    def critical_frequency(self) -> float:
        """
        Calculate critical Frohlich frequency.

        The condensation occurs when the oscillation energy exceeds
        thermal energy: hbar * omega_F > k_B * T

        omega_critical = k_B * T / hbar

        At T = 310K: omega_c ~ 4e13 rad/s ~ 6.4 THz

        Returns:
            Critical frequency in Hz
        """
        omega_c = self.kT / HBAR
        f_c = omega_c / (2 * np.pi)
        return f_c

    def calculate_condensation_ratio(self) -> float:
        """
        Calculate ratio of Frohlich energy to thermal energy.

        R = hbar * omega_F / k_B * T

        For omega_F = 10^12 Hz at 310K: R ~ 0.15

        PROBLEM: R < 1 means thermal fluctuations dominate!

        Returns:
            Energy ratio (dimensionless)
        """
        return self.E_frohlich / self.kT

    def estimate_protection_factor(self, pump_rate_ratio: float = 1.0) -> float:
        """
        Estimate protection factor from Frohlich condensation.

        If condensation is achieved (pump_rate > thermal_dissipation),
        coherent oscillation of N dipoles provides protection.

        OPTIMISTIC: P = N (full coherent enhancement)
        REALISTIC: P = sqrt(N) (partial coherence)
        PESSIMISTIC: P = 1 (no condensation)

        The pump_rate_ratio determines which regime:
        - ratio > 1: Realistic (sqrt(N) enhancement)
        - ratio > 10: Optimistic (approaching N enhancement)
        - ratio < 1: Pessimistic (thermal domination)

        Args:
            pump_rate_ratio: Metabolic pump rate / thermal dissipation

        Returns:
            Protection factor
        """
        condensation_ratio = self.calculate_condensation_ratio()

        # Effective condensation parameter
        eta = pump_rate_ratio * condensation_ratio

        if eta > 10:
            # Strong pumping - approach full N enhancement
            protection = self.N ** 0.9
        elif eta > 1:
            # Moderate pumping - sqrt(N) enhancement
            protection = np.sqrt(self.N)
        elif eta > 0.1:
            # Weak pumping - marginal enhancement
            protection = self.N ** 0.25
        else:
            # No condensation
            protection = 1.0

        return protection

    def analyze(
        self,
        raw_decoherence_time_s: float,
        pump_rate_ratio: float = 1.0
    ) -> DecoherenceAnalysis:
        """
        Complete Frohlich condensation analysis.

        Args:
            raw_decoherence_time_s: Unprotected decoherence time
            pump_rate_ratio: Metabolic pump rate / thermal dissipation

        Returns:
            DecoherenceAnalysis with results
        """
        protection = self.estimate_protection_factor(pump_rate_ratio)
        protected_time = raw_decoherence_time_s * protection

        f_critical = self.critical_frequency()
        ratio = self.calculate_condensation_ratio()

        return DecoherenceAnalysis(
            mechanism="Frohlich Condensation",
            protection_factor=protection,
            raw_decoherence_time_s=raw_decoherence_time_s,
            protected_decoherence_time_s=protected_time,
            description=(
                f"Frohlich coherent dipole oscillation at {self.OMEGA_FROHLICH/1e12:.1f} THz. "
                f"Critical frequency: {f_critical/1e12:.2f} THz. "
                f"Energy ratio E_F/kT = {ratio:.3f} {'< 1 (thermal dominated!)' if ratio < 1 else '>= 1'}. "
                f"N = {self.N:.0e} oscillators, pump ratio = {pump_rate_ratio}. "
                f"Protection: {protection:.2e} (10^{np.log10(max(protection, 1)):.1f})."
            ),
            limitations=[
                "Experimental evidence is controversial (Craddock 2017)",
                f"Energy ratio E_F/kT = {ratio:.3f} < 1 means thermal fluctuations dominate",
                "Requires sustained metabolic energy pumping beyond known rates",
                "Brain energy budget may not support required pump rates",
                "Coherence length may be limited by system size"
            ],
            assumptions=[
                "Frohlich frequency ~ 1 THz from protein dipole modes",
                f"N ~ {self.N:.0e} coupled oscillators in microtubule network",
                f"Pump rate ratio = {pump_rate_ratio} (metabolic pumping vs dissipation)",
                "Collective mode can form despite thermal noise"
            ],
            references=[
                "Frohlich (1968) - Long-range coherence and energy storage",
                "Craddock et al. (2017) - Anesthetic alterations of THz oscillations",
                "Reimers et al. (2009) - Critique of Frohlich condensation claims",
                "Hameroff & Penrose (2014) - Orch-OR and Frohlich condensation"
            ]
        )


class DecoherenceProtectionSimulation:
    """
    Complete Decoherence Protection Simulation for Orch-OR.

    Combines all protection mechanisms and provides honest assessment
    of whether the "warm brain problem" can be solved.

    THE PROBLEM:
    - Standard decoherence at 310K: tau_dec ~ 10^-13 s
    - Required for Orch-OR: tau ~ 10^-2 s (100x neural timescale)
    - Enhancement needed: 10^11

    WHAT CAN BE ACHIEVED:
    - Debye shielding: ~10^2
    - G2 topology: ~10^2
    - Frohlich condensation: ~10^3-10^5 (if achieved)
    - Combined (optimistic): ~10^6-10^8

    THE GAP:
    - Even with all mechanisms: 10^3 to 10^5 shortfall
    - This is a serious challenge to Orch-OR theory
    - Additional mechanisms or revised timescales needed
    """

    def __init__(
        self,
        temperature_k: float = T_BRAIN,
        n_tubulins: float = 1e9
    ):
        """
        Initialize decoherence protection simulation.

        Args:
            temperature_k: Brain temperature in Kelvin
            n_tubulins: Number of tubulins in coherent superposition
        """
        self.T = temperature_k
        self.N_tubulins = n_tubulins
        self.kT = K_B * temperature_k

        # Initialize protection mechanisms
        self.debye = DebyeLayerShielding(temperature_k)
        self.g2 = G2TopologicalProtection()
        self.frohlich = FrohlichCondensation(temperature_k, int(n_tubulins))

        # Raw thermal decoherence time (Tegmark estimate)
        self.tau_raw = self._calculate_raw_decoherence_time()

    def _calculate_raw_decoherence_time(self) -> float:
        """
        Calculate raw thermal decoherence time (Tegmark model).

        tau_dec ~ hbar^2 / (2 * m * k_B * T * r^2)

        For tubulin at 310K: tau_dec ~ 10^-13 s

        Returns:
            Raw decoherence time in seconds
        """
        # Effective mass (collective superposition)
        m_eff = M_TUBULIN * np.sqrt(self.N_tubulins)

        # Separation scale (tubulin radius)
        r = R_TUBULIN

        # Tegmark formula
        tau = (HBAR ** 2) / (2 * m_eff * self.kT * (r ** 2))

        return tau

    def calculate_required_protection(self, target_time_s: float = 0.025) -> float:
        """
        Calculate protection factor needed for target coherence time.

        Args:
            target_time_s: Target coherence time (default: 25ms for gamma)

        Returns:
            Required protection factor
        """
        return target_time_s / self.tau_raw

    def analyze_all_mechanisms(
        self,
        frohlich_pump_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """
        Run complete analysis of all protection mechanisms.

        Args:
            frohlich_pump_ratio: Metabolic pump rate / thermal dissipation

        Returns:
            Complete analysis dictionary
        """
        # Analyze each mechanism
        debye_result = self.debye.analyze(self.tau_raw)
        g2_result = self.g2.analyze(self.tau_raw)
        frohlich_result = self.frohlich.analyze(self.tau_raw, frohlich_pump_ratio)

        # Combined protection (multiplicative)
        combined_factor = (
            debye_result.protection_factor *
            g2_result.protection_factor *
            frohlich_result.protection_factor
        )
        combined_time = self.tau_raw * combined_factor

        # Target comparison
        target_time = 0.025  # 25 ms for gamma oscillation
        required_factor = self.calculate_required_protection(target_time)
        shortfall = required_factor / combined_factor

        # Build results
        results = {
            "raw_decoherence": {
                "tau_s": self.tau_raw,
                "tau_ps": self.tau_raw * 1e12,
                "description": f"Raw thermal decoherence: {self.tau_raw:.2e} s ({self.tau_raw*1e12:.2f} ps)"
            },
            "mechanisms": {
                "debye": {
                    "protection_factor": debye_result.protection_factor,
                    "log10": np.log10(debye_result.protection_factor),
                    "protected_time_s": debye_result.protected_decoherence_time_s,
                    "description": debye_result.description,
                    "limitations": debye_result.limitations
                },
                "g2": {
                    "protection_factor": g2_result.protection_factor,
                    "log10": np.log10(g2_result.protection_factor),
                    "protected_time_s": g2_result.protected_decoherence_time_s,
                    "description": g2_result.description,
                    "limitations": g2_result.limitations
                },
                "frohlich": {
                    "protection_factor": frohlich_result.protection_factor,
                    "log10": np.log10(max(frohlich_result.protection_factor, 1)),
                    "protected_time_s": frohlich_result.protected_decoherence_time_s,
                    "description": frohlich_result.description,
                    "limitations": frohlich_result.limitations
                }
            },
            "combined": {
                "protection_factor": combined_factor,
                "log10": np.log10(combined_factor),
                "protected_time_s": combined_time,
                "protected_time_ms": combined_time * 1000
            },
            "target_comparison": {
                "target_time_ms": target_time * 1000,
                "required_factor": required_factor,
                "required_log10": np.log10(required_factor),
                "shortfall_factor": shortfall,
                "shortfall_log10": np.log10(shortfall)
            },
            "honest_assessment": self._generate_honest_assessment(
                combined_factor, required_factor, shortfall
            )
        }

        return results

    def _generate_honest_assessment(
        self,
        achieved: float,
        required: float,
        shortfall: float
    ) -> Dict[str, Any]:
        """
        Generate honest scientific assessment of protection capability.

        Args:
            achieved: Combined protection factor achieved
            required: Required protection factor
            shortfall: Ratio of required to achieved

        Returns:
            Assessment dictionary
        """
        if shortfall <= 1:
            status = "SUFFICIENT"
            conclusion = "Combined mechanisms provide sufficient protection for Orch-OR"
            confidence = "HIGH"
        elif shortfall <= 10:
            status = "MARGINAL"
            conclusion = "Protection is within order of magnitude - plausible with parameter adjustment"
            confidence = "MODERATE"
        elif shortfall <= 1000:
            status = "CHALLENGING"
            conclusion = "Significant gap exists - requires additional mechanisms or revised physics"
            confidence = "LOW"
        else:
            status = "INSUFFICIENT"
            conclusion = "Protection falls far short - fundamental challenge to Orch-OR mechanism"
            confidence = "VERY LOW"

        return {
            "status": status,
            "achieved_protection_log10": np.log10(achieved),
            "required_protection_log10": np.log10(required),
            "shortfall_orders_magnitude": np.log10(shortfall),
            "conclusion": conclusion,
            "confidence": confidence,
            "caveats": [
                "Debye protection assumes optimal ionic conditions",
                "G2 topology in biology is speculative",
                "Frohlich condensation is controversial and may not occur",
                "Combined effects may not be simply multiplicative",
                "Additional unknown mechanisms may exist"
            ],
            "paths_forward": [
                "Discover additional protection mechanisms",
                "Revise target timescale (shorter coherence may suffice)",
                "Identify biological conditions that enhance protection",
                "Develop experimental tests of protection mechanisms",
                "Consider alternative quantum consciousness mechanisms"
            ]
        }

    def run(self, frohlich_pump_ratio: float = 1.0, verbose: bool = True) -> Dict[str, Any]:
        """
        Run complete decoherence protection simulation.

        Args:
            frohlich_pump_ratio: Metabolic pump rate / thermal dissipation
            verbose: Whether to print detailed output

        Returns:
            Complete results dictionary
        """
        results = self.analyze_all_mechanisms(frohlich_pump_ratio)

        if verbose:
            self._print_results(results)

        return results

    def _print_results(self, results: Dict[str, Any]) -> None:
        """Print formatted results."""
        print("\n" + "=" * 80)
        print(" DECOHERENCE PROTECTION ANALYSIS - Orch-OR v18.0")
        print(" The 'Warm Brain Problem' Assessment")
        print("=" * 80)

        print(f"\n{'='*80}")
        print(" RAW THERMAL DECOHERENCE (Tegmark Model)")
        print("-" * 80)
        raw = results["raw_decoherence"]
        print(f"  tau_raw = {raw['tau_s']:.2e} s = {raw['tau_ps']:.2f} ps")
        print(f"  Temperature: {self.T} K")
        print(f"  N_tubulins: {self.N_tubulins:.2e}")

        print(f"\n{'='*80}")
        print(" PROTECTION MECHANISMS")
        print("-" * 80)

        for name, mech in results["mechanisms"].items():
            print(f"\n  [{name.upper()}]")
            print(f"    Protection factor: {mech['protection_factor']:.2e} (10^{mech['log10']:.1f})")
            print(f"    Protected time: {mech['protected_time_s']:.2e} s")
            print(f"    Limitations:")
            for lim in mech['limitations'][:2]:
                print(f"      - {lim}")

        print(f"\n{'='*80}")
        print(" COMBINED PROTECTION")
        print("-" * 80)
        comb = results["combined"]
        print(f"  Combined factor: {comb['protection_factor']:.2e} (10^{comb['log10']:.1f})")
        print(f"  Protected time: {comb['protected_time_s']:.2e} s = {comb['protected_time_ms']:.2f} ms")

        print(f"\n{'='*80}")
        print(" TARGET COMPARISON")
        print("-" * 80)
        target = results["target_comparison"]
        print(f"  Target time (gamma): {target['target_time_ms']:.0f} ms")
        print(f"  Required factor: {target['required_factor']:.2e} (10^{target['required_log10']:.1f})")
        print(f"  SHORTFALL: {target['shortfall_factor']:.2e} (10^{target['shortfall_log10']:.1f})")

        print(f"\n{'='*80}")
        print(" HONEST ASSESSMENT")
        print("-" * 80)
        assess = results["honest_assessment"]
        print(f"  Status: [{assess['status']}]")
        print(f"  Confidence: {assess['confidence']}")
        print(f"  ")
        print(f"  {assess['conclusion']}")
        print(f"  ")
        print(f"  Achieved: 10^{assess['achieved_protection_log10']:.1f}")
        print(f"  Required: 10^{assess['required_protection_log10']:.1f}")
        print(f"  Gap: 10^{assess['shortfall_orders_magnitude']:.1f} orders of magnitude")

        print(f"\n  Paths Forward:")
        for path in assess["paths_forward"][:3]:
            print(f"    - {path}")

        print("\n" + "=" * 80)


# =============================================================================
# SIMULATION BASE WRAPPER (for PM Registry integration)
# =============================================================================

if SCHEMA_AVAILABLE:
    class DecoherenceProtectionSimulationV18(SimulationBase):
        """
        Schema-compliant v18 wrapper for decoherence protection simulation.
        """

        def __init__(self):
            """Initialize v18 simulation wrapper."""
            self._sim = DecoherenceProtectionSimulation()
            self._result = None

        @property
        def metadata(self) -> SimulationMetadata:
            return SimulationMetadata(
                id="decoherence_protection_v18_0",
                version="18.0",
                domain="quantum_bio",
                title="Decoherence Protection for Orch-OR (Critical Analysis)",
                description=(
                    "Analyzes Debye shielding, G2 topological protection, and Frohlich "
                    "condensation as mechanisms to extend quantum coherence in warm brains. "
                    "Provides honest assessment: achievable protection ~10^6-10^8, "
                    "required ~10^11, leaving 10^3-10^5 gap."
                ),
                section_id="7",
                subsection_id="7.3"
            )

        @property
        def required_inputs(self) -> List[str]:
            return ["topology.b3"]

        @property
        def output_params(self) -> List[str]:
            return [
                "quantum_bio.debye_protection_factor",
                "quantum_bio.g2_protection_factor",
                "quantum_bio.frohlich_protection_factor",
                "quantum_bio.combined_protection_factor",
                "quantum_bio.protection_shortfall",
                "quantum_bio.protection_status"
            ]

        @property
        def output_formulas(self) -> List[str]:
            return [
                "debye-screening",
                "g2-protection-factor",
                "frohlich-condensation-protection"
            ]

        def run(self, registry: PMRegistry) -> Dict[str, Any]:
            """Execute decoherence protection simulation."""
            self._result = self._sim.run(frohlich_pump_ratio=1.0, verbose=False)

            return {
                "quantum_bio.debye_protection_factor":
                    self._result["mechanisms"]["debye"]["protection_factor"],
                "quantum_bio.g2_protection_factor":
                    self._result["mechanisms"]["g2"]["protection_factor"],
                "quantum_bio.frohlich_protection_factor":
                    self._result["mechanisms"]["frohlich"]["protection_factor"],
                "quantum_bio.combined_protection_factor":
                    self._result["combined"]["protection_factor"],
                "quantum_bio.protection_shortfall":
                    self._result["target_comparison"]["shortfall_factor"],
                "quantum_bio.protection_status":
                    self._result["honest_assessment"]["status"]
            }

        def get_section_content(self) -> Optional[SectionContent]:
            """Return section content for paper."""
            return SectionContent(
                section_id="7",
                subsection_id="7.3",
                title="Decoherence Protection Mechanisms (Critical Analysis)",
                abstract=(
                    "Analysis of mechanisms proposed to protect quantum coherence "
                    "in warm biological systems. Debye shielding, G2 topology, and "
                    "Frohlich condensation together provide ~10^6-10^8 protection, "
                    "but 10^11 is required. This represents a significant gap."
                ),
                content_blocks=[
                    ContentBlock(
                        type="callout",
                        callout_type="warning",
                        content=(
                            "HONEST ASSESSMENT: Combined protection mechanisms fall "
                            "10^3-10^5 short of the required 10^11 enhancement factor. "
                            "This represents a fundamental challenge to Orch-OR theory."
                        )
                    ),
                    ContentBlock(
                        type="heading",
                        content="The Warm Brain Problem",
                        level=3
                    ),
                    ContentBlock(
                        type="paragraph",
                        content=(
                            "Standard physics predicts decoherence at T=310K occurs in "
                            "tau_dec ~ 10^-13 s. Orch-OR requires tau ~ 10^-2 s (25ms for "
                            "gamma oscillations). This is a factor of 10^11 enhancement needed."
                        )
                    ),
                    ContentBlock(
                        type="formula",
                        formula_id="debye-screening",
                        label="(7.3a)"
                    ),
                    ContentBlock(
                        type="formula",
                        formula_id="g2-protection-factor",
                        label="(7.3b)"
                    ),
                    ContentBlock(
                        type="formula",
                        formula_id="frohlich-condensation-protection",
                        label="(7.3c)"
                    )
                ],
                formula_refs=self.output_formulas,
                param_refs=self.output_params
            )

        def get_formulas(self) -> List[Formula]:
            """Return formula definitions."""
            return [
                Formula(
                    id="debye-screening",
                    label="(7.3a)",
                    latex=r"V(r) = \frac{Q}{4\pi\varepsilon_0\varepsilon_r r} \exp\left(-\frac{r}{\lambda_D}\right), \quad \lambda_D = \sqrt{\frac{\varepsilon_0 \varepsilon_r k_B T}{2 N_A e^2 I}}",
                    plain_text="V(r) = (Q/4*pi*eps_0*eps_r*r) * exp(-r/lambda_D), lambda_D ~ 0.7 nm",
                    category="SPECULATIVE",
                    description=(
                        "Debye-Huckel screening potential. At ionic strength I~150mM, "
                        "lambda_D~0.7nm provides ~10^2 protection factor."
                    ),
                    input_params=["constants.epsilon_0", "constants.k_B", "constants.T_brain"],
                    output_params=["quantum_bio.debye_protection_factor"]
                ),
                Formula(
                    id="g2-protection-factor",
                    label="(7.3b)",
                    latex=r"P_{G2} = \frac{\dim(SO(7))}{\dim(G_2)} \times e^{2\pi d/R} \times \frac{\chi_{\text{eff}}}{b_3} \times k_\gimel",
                    plain_text="P_G2 = (21/14) * exp(2*pi*0.12) * (144/24) * k_gimel ~ 240",
                    category="SPECULATIVE",
                    description=(
                        "G2 topological protection from holonomy restriction, cycle isolation, "
                        "flux quantization, and k_gimel enhancement. Provides ~10^2 protection."
                    ),
                    input_params=["topology.b3", "topology.chi_eff", "topology.k_gimel"],
                    output_params=["quantum_bio.g2_protection_factor"]
                ),
                Formula(
                    id="frohlich-condensation-protection",
                    label="(7.3c)",
                    latex=r"P_F \sim \sqrt{N} \text{ to } N, \quad \omega_F \sim 10^{12} \text{ Hz}, \quad R = \frac{\hbar\omega_F}{k_B T} \approx 0.15",
                    plain_text="P_F ~ sqrt(N) to N for N~10^9 oscillators, omega_F~THz",
                    category="SPECULATIVE",
                    description=(
                        "Frohlich coherent dipole oscillation. CAVEAT: Energy ratio R~0.15<1 "
                        "means thermal fluctuations dominate. Protection ~10^3-10^5 if achieved."
                    ),
                    input_params=["constants.hbar", "constants.k_B", "constants.T_brain"],
                    output_params=["quantum_bio.frohlich_protection_factor"]
                )
            ]

        def get_output_param_definitions(self) -> List[Parameter]:
            """Return output parameter definitions."""
            result = self._result or self._sim.run(verbose=False)

            return [
                Parameter(
                    path="quantum_bio.combined_protection_factor",
                    name="Combined Decoherence Protection",
                    units="dimensionless",
                    status="SPECULATIVE",
                    description=(
                        f"Combined protection from Debye, G2, and Frohlich mechanisms: "
                        f"{result['combined']['protection_factor']:.2e} (10^{result['combined']['log10']:.1f}). "
                        f"Required: 10^11. Status: {result['honest_assessment']['status']}."
                    ),
                    derivation_formula="g2-protection-factor",
                    no_experimental_value=True
                ),
                Parameter(
                    path="quantum_bio.protection_shortfall",
                    name="Protection Shortfall Factor",
                    units="dimensionless",
                    status="SPECULATIVE",
                    description=(
                        f"Ratio of required to achieved protection: "
                        f"{result['target_comparison']['shortfall_factor']:.2e} "
                        f"(10^{result['target_comparison']['shortfall_log10']:.1f}). "
                        "Values >1 indicate insufficient protection for Orch-OR."
                    ),
                    no_experimental_value=True
                ),
                Parameter(
                    path="quantum_bio.protection_status",
                    name="Protection Assessment Status",
                    units="string",
                    status="SPECULATIVE",
                    description=(
                        f"Honest assessment: {result['honest_assessment']['status']}. "
                        f"{result['honest_assessment']['conclusion']}"
                    ),
                    no_experimental_value=True
                )
            ]


# =============================================================================
# STANDALONE EXECUTION
# =============================================================================

def run_decoherence_protection_analysis(
    temperature_k: float = 310.0,
    n_tubulins: float = 1e9,
    frohlich_pump_ratio: float = 1.0,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run standalone decoherence protection analysis.

    Args:
        temperature_k: Brain temperature (default: 310K)
        n_tubulins: Number of tubulins in superposition (default: 10^9)
        frohlich_pump_ratio: Metabolic pump rate / thermal dissipation (default: 1.0)
        verbose: Whether to print detailed output

    Returns:
        Complete analysis results
    """
    sim = DecoherenceProtectionSimulation(temperature_k, n_tubulins)
    return sim.run(frohlich_pump_ratio, verbose)


def parameter_sweep_analysis(verbose: bool = True) -> Dict[str, Any]:
    """
    Run parameter sweep to find conditions for sufficient protection.

    Varies:
    - N_tubulins: 10^8 to 10^12
    - Frohlich pump ratio: 0.1 to 100

    Returns:
        Sweep results showing which conditions (if any) achieve sufficient protection
    """
    results = []

    n_values = [1e8, 1e9, 1e10, 1e11, 1e12]
    pump_values = [0.1, 1.0, 10.0, 100.0]

    for n in n_values:
        for pump in pump_values:
            sim = DecoherenceProtectionSimulation(T_BRAIN, n)
            analysis = sim.run(pump, verbose=False)

            results.append({
                "n_tubulins": n,
                "pump_ratio": pump,
                "combined_factor": analysis["combined"]["protection_factor"],
                "shortfall": analysis["target_comparison"]["shortfall_factor"],
                "status": analysis["honest_assessment"]["status"]
            })

    if verbose:
        print("\n" + "=" * 80)
        print(" PARAMETER SWEEP - Finding Sufficient Protection Conditions")
        print("=" * 80)
        print(f"\n{'N_tubulins':>12} {'Pump Ratio':>12} {'Protection':>14} {'Shortfall':>14} {'Status':>14}")
        print("-" * 80)

        for r in results:
            print(f"{r['n_tubulins']:>12.0e} {r['pump_ratio']:>12.1f} {r['combined_factor']:>14.2e} {r['shortfall']:>14.2e} {r['status']:>14}")

        # Find best condition
        best = min(results, key=lambda x: x["shortfall"])
        print(f"\nBest condition: N={best['n_tubulins']:.0e}, pump={best['pump_ratio']}")
        print(f"  Shortfall: {best['shortfall']:.2e} ({best['status']})")

        if best["shortfall"] > 1:
            print(f"\n  CONCLUSION: Even with optimistic parameters, protection is insufficient.")
            print(f"  Additional mechanisms beyond Debye/G2/Frohlich are needed.")

    return {"sweep_results": results}


if __name__ == "__main__":
    # Run main analysis
    print("\n" + "#" * 80)
    print(" DECOHERENCE PROTECTION MECHANISMS FOR ORCH-OR")
    print(" Addressing the Warm Brain Problem")
    print("#" * 80)

    # Standard analysis
    results = run_decoherence_protection_analysis(
        temperature_k=310.0,
        n_tubulins=1e9,
        frohlich_pump_ratio=1.0,
        verbose=True
    )

    # Parameter sweep
    print("\n")
    sweep = parameter_sweep_analysis(verbose=True)

    print("\n" + "=" * 80)
    print(" FINAL CONCLUSION")
    print("=" * 80)
    print("""
    The 'warm brain problem' remains a significant challenge for Orch-OR.

    Combined protection mechanisms (Debye + G2 + Frohlich) provide:
      - Achievable: ~10^6 to 10^8 enhancement
      - Required:   ~10^11 enhancement
      - Shortfall:  ~10^3 to 10^5

    This analysis is SCIENTIFICALLY HONEST - we do not claim that current
    known mechanisms can solve the warm brain problem. Possible paths forward:

    1. Discovery of additional protection mechanisms
    2. Revision of required timescales (perhaps shorter coherence suffices)
    3. Novel biological conditions that enhance protection
    4. Alternative quantum consciousness mechanisms
    5. Acceptance that Orch-OR faces fundamental challenges

    This simulation provides a quantitative framework for evaluating
    proposed solutions to the decoherence protection problem.
    """)
