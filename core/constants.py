"""
Domain-Specific Configuration Classes
======================================

SOLID Principles Applied:
- Single Responsibility: Each class handles ONE domain
- Open/Closed: New domains can be added without modifying existing code
- Dependency Inversion: Classes depend on abstractions, not concretions

This module splits the monolithic config.py into focused domain classes.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional
import numpy as np


@dataclass(frozen=True)
class DimensionalStructure:
    """
    Dimensional structure of the Principia Metaphysica framework.

    Single Responsibility: Only handles dimensional/spacetime structure.
    Immutable (frozen=True) to prevent accidental modification.

    26D (24,2) → [Sp(2,R)] → 13D (12,1) → [G₂ 7D] → 6D (5,1) effective
    """
    # Bulk spacetime
    D_BULK: int = 26
    SIGNATURE_BULK: Tuple[int, int] = (24, 2)

    # After Sp(2,R) gauge fixing
    D_AFTER_SP2R: int = 13
    SIGNATURE_AFTER_SP2R: Tuple[int, int] = (12, 1)

    # G₂ internal manifold
    D_INTERNAL: int = 7
    INTERNAL_MANIFOLD: str = "G2"

    # Effective spacetime
    D_EFFECTIVE: int = 6
    SIGNATURE_EFFECTIVE: Tuple[int, int] = (5, 1)

    # Observable spacetime
    D_OBSERVABLE: int = 4
    SIGNATURE_OBSERVABLE: Tuple[int, int] = (3, 1)

    # Brane structure
    N_BRANES: int = 4
    D_OBSERVABLE_BRANE: int = 6
    D_SHADOW_BRANE: int = 4
    N_SHADOW_BRANES: int = 3

    # Gauge fixing parameters
    GAUGING_DOFS: int = 12
    MIRRORING_FACTOR: int = 2

    def pneuma_dimension_full(self) -> int:
        """Pneuma spinor dimension: 2^(D/2) from Clifford algebra"""
        return int(2 ** (self.D_BULK / 2))

    def pneuma_dimension_reduced(self) -> int:
        """After Sp(2,R) gauging and Z₂ mirroring"""
        full = self.pneuma_dimension_full()
        return int(full / (2 ** (self.GAUGING_DOFS / 2)) / self.MIRRORING_FACTOR)


@dataclass(frozen=True)
class TopologyParameters:
    """
    Topological invariants of the G₂ manifold.

    Single Responsibility: Only handles topology (Betti numbers, Euler char).

    TCS G₂ #187: b₂=4, b₃=24, χ_eff=144
    """
    # Betti numbers from TCS construction
    b2: int = 4
    b3: int = 24

    # Hodge numbers (CY3 interpretation)
    h11: int = 4
    h21: int = 0
    h31: int = 72

    # Effective Euler characteristic (after flux quantization)
    chi_eff: int = 144

    # Flux reduction factor
    FLUX_REDUCTION: int = 2

    # Torsion class (from TCS G₂)
    T_OMEGA: float = -0.884

    @property
    def n_gen(self) -> int:
        """Number of fermion generations: n_gen = χ_eff / 48"""
        return self.chi_eff // 48

    @property
    def nu(self) -> int:
        """Index for Dirac operator: ν = b₃"""
        return self.b3


@dataclass(frozen=True)
class EnergyScales:
    """
    Fundamental energy scales in the framework.

    Single Responsibility: Only handles energy/mass scales.

    All masses in GeV.
    """
    # Planck scales
    M_PLANCK_REDUCED: float = 2.435e18  # Reduced Planck mass [GeV]
    M_PLANCK_FULL: float = 1.221e19     # Full Planck mass [GeV]

    # GUT scale (from TCS G₂ torsion)
    M_GUT: float = 2.118e16
    M_GUT_ERROR: float = 0.09e16

    # String/fundamental scale
    M_STAR: float = 7.4604e15  # 13D fundamental scale [GeV]

    # Electroweak scale
    V_EW: float = 173.97  # VEV from Pneuma condensate [GeV]
    M_HIGGS: float = 125.10  # Higgs mass [GeV]

    # Right-handed neutrino scale
    M_RH_NEUTRINO: float = 1e14  # Seesaw scale [GeV]

    @property
    def M_PLANCK(self) -> float:
        """Default Planck mass (reduced)"""
        return self.M_PLANCK_REDUCED


@dataclass(frozen=True)
class GaugeParameters:
    """
    Gauge unification parameters for SO(10) GUT.

    Single Responsibility: Only handles gauge coupling unification.
    """
    # GUT coupling (3-loop + thresholds)
    ALPHA_GUT_INV: float = 23.54

    # SO(10) group theory
    C_A_SO10_ADJOINT: int = 9  # Quadratic Casimir for adjoint (45)
    DIM_ADJOINT: int = 45
    DIM_SPINOR: int = 16

    # Beta function normalization
    BETA_PREFACTOR: float = 1 / (16 * np.pi**2)

    # X,Y gauge boson properties (from SO(10))
    CHARGE_X: float = 4/3
    CHARGE_Y: float = 1/3
    N_X_BOSONS: int = 12
    N_Y_BOSONS: int = 12

    @property
    def ALPHA_GUT(self) -> float:
        """GUT fine structure constant"""
        return 1.0 / self.ALPHA_GUT_INV


@dataclass(frozen=True)
class NeutrinoConfig:
    """
    Neutrino physics configuration.

    Single Responsibility: Only handles neutrino masses and mixing.

    v12.3: Updated to NuFIT 6.0 (maximal mixing)
    """
    # PMNS mixing angles (degrees)
    theta_23: float = 45.0    # Maximal mixing from α₄ = α₅
    theta_12: float = 33.59   # From tri-bimaximal + perturbation
    theta_13: float = 8.57    # From cycle asymmetry
    delta_cp: float = 235.0   # CP phase from cycle overlaps

    # Uncertainties
    theta_23_error: float = 0.80
    theta_12_error: float = 1.18
    theta_13_error: float = 0.35
    delta_cp_error: float = 27.4

    # NuFIT 6.0 comparison values
    theta_23_nufit: float = 45.0
    theta_12_nufit: float = 33.41
    theta_13_nufit: float = 8.57
    delta_cp_nufit: float = 232.0

    # Hierarchy prediction
    HIERARCHY: str = "Normal"

    # Mass splittings (eV²)
    DELTA_M21_SQ: float = 7.42e-5  # Solar
    DELTA_M31_SQ: float = 2.515e-3  # Atmospheric

    # Alpha parameters (G₂ torsion derived)
    alpha_4: float = 0.576152
    alpha_5: float = 0.576152  # Equal for maximal mixing


@dataclass(frozen=True)
class DarkEnergyConfig:
    """
    Dark energy and cosmology configuration.

    Single Responsibility: Only handles dark energy/cosmology.
    """
    # Equation of state (from d_eff)
    w0: float = -0.8528
    wa: float = -0.75

    # DESI DR2 comparison
    w0_DESI: float = -0.83
    w0_DESI_error: float = 0.06
    wa_DESI: float = -0.75
    wa_DESI_error: float = 0.30

    # Cosmological parameters (Planck 2018)
    OMEGA_LAMBDA: float = 0.6889
    OMEGA_MATTER: float = 0.3111
    OMEGA_BARYON: float = 0.0486
    H0: float = 67.4  # km/s/Mpc

    # Effective dimension (from G₂ torsion)
    d_eff: float = 12.576  # 12 + 0.5*(α₄ + α₅)

    @classmethod
    def w0_from_d_eff(cls, d_eff: float) -> float:
        """Calculate w₀ from effective dimension: w₀ = -(d_eff - 1)/(d_eff + 1)"""
        return -(d_eff - 1) / (d_eff + 1)


@dataclass(frozen=True)
class ProtonDecayConfig:
    """
    Proton decay configuration.

    Single Responsibility: Only handles proton decay parameters.
    """
    # Lifetime (from geometric + RG hybrid)
    tau_p_median: float = 3.91e34  # years
    tau_p_lower_68: float = 2.35e34
    tau_p_upper_68: float = 5.39e34
    tau_p_uncertainty_oom: float = 0.177

    # Experimental bound
    SUPER_K_BOUND: float = 1.67e34  # Super-Kamiokande lower bound [years]

    # Branching ratios (approximate)
    BR_e_pi0: float = 0.45
    BR_K_nu: float = 0.35
    BR_mu_pi0: float = 0.20


# Singleton instances for convenience (backward compatibility)
_dimensions = None
_topology = None
_energy = None
_gauge = None
_neutrino = None
_dark_energy = None
_proton = None


def get_dimensions() -> DimensionalStructure:
    """Get singleton DimensionalStructure instance"""
    global _dimensions
    if _dimensions is None:
        _dimensions = DimensionalStructure()
    return _dimensions


def get_topology() -> TopologyParameters:
    """Get singleton TopologyParameters instance"""
    global _topology
    if _topology is None:
        _topology = TopologyParameters()
    return _topology


def get_energy_scales() -> EnergyScales:
    """Get singleton EnergyScales instance"""
    global _energy
    if _energy is None:
        _energy = EnergyScales()
    return _energy


def get_gauge() -> GaugeParameters:
    """Get singleton GaugeParameters instance"""
    global _gauge
    if _gauge is None:
        _gauge = GaugeParameters()
    return _gauge


def get_neutrino() -> NeutrinoConfig:
    """Get singleton NeutrinoConfig instance"""
    global _neutrino
    if _neutrino is None:
        _neutrino = NeutrinoConfig()
    return _neutrino


def get_dark_energy() -> DarkEnergyConfig:
    """Get singleton DarkEnergyConfig instance"""
    global _dark_energy
    if _dark_energy is None:
        _dark_energy = DarkEnergyConfig()
    return _dark_energy


def get_proton_decay() -> ProtonDecayConfig:
    """Get singleton ProtonDecayConfig instance"""
    global _proton
    if _proton is None:
        _proton = ProtonDecayConfig()
    return _proton
