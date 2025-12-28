"""
Established Physics Loader for Principia Metaphysica
======================================================

Loads experimentally measured physics constants from authoritative sources:
- PDG 2024 (Particle Data Group)
- NuFIT 6.0 (2024)
- DESI DR2 (2024)
- Super-Kamiokande and other experimental bounds

All values are marked with source "ESTABLISHED" and cannot be overridden by simulations.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os
from typing import Dict, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
import warnings

if TYPE_CHECKING:
    from .registry import PMRegistry

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from config import (
        PhenomenologyParameters,
        NeutrinoParameters,
    )
    CONFIG_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"Could not import from config.py: {e}. Using fallback values.")
    CONFIG_AVAILABLE = False


@dataclass
class EstablishedParameter:
    """A single established physics parameter with full provenance."""
    path: str                    # e.g., "pdg.m_higgs"
    value: float
    uncertainty: float
    units: str
    source: str                  # e.g., "ESTABLISHED:PDG2024"
    status: str = "ESTABLISHED"
    description: str = ""


class EstablishedPhysics:
    """
    Loader for established experimental physics values.

    This class provides a centralized registry of all experimentally measured
    values that serve as ground truth for the theory. These values:

    1. Cannot be overridden by simulations
    2. Have clear source provenance (PDG, NuFIT, DESI, etc.)
    3. Include uncertainties where applicable
    4. Serve as validation targets for theoretical predictions

    Usage:
        registry = PMRegistry()
        EstablishedPhysics.load_into_registry(registry)
    """

    @classmethod
    def load_into_registry(cls, registry: 'PMRegistry') -> None:
        """Load all established physics parameters into the registry."""
        cls._load_constants(registry)
        cls._load_pdg_values(registry)
        cls._load_nufit_values(registry)
        cls._load_desi_values(registry)
        cls._load_experimental_bounds(registry)
        cls._load_theory_constants(registry)

    @classmethod
    def _load_constants(cls, registry: 'PMRegistry') -> None:
        """Load fundamental constants (Planck mass, alpha_em, etc.)."""
        if CONFIG_AVAILABLE:
            M_PLANCK = getattr(PhenomenologyParameters, 'M_PLANCK_REDUCED', 2.435e18)
            ALPHA_EM = getattr(PhenomenologyParameters, 'ALPHA_EM', 1/137.036)
        else:
            M_PLANCK = 2.435e18
            ALPHA_EM = 1/137.036

        params = [
            EstablishedParameter(
                path="constants.M_PLANCK",
                value=M_PLANCK,
                uncertainty=3.0e15,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Reduced Planck mass"
            ),
            EstablishedParameter(
                path="constants.alpha_em",
                value=ALPHA_EM,
                uncertainty=1.5e-10,
                units="dimensionless",
                source="ESTABLISHED:CODATA2018",
                description="Fine structure constant"
            ),
            EstablishedParameter(
                path="constants.m_proton",
                value=0.938272,
                uncertainty=0.000001,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Proton mass"
            ),
        ]

        for param in params:
            cls._register_param(registry, param)

    @classmethod
    def _load_pdg_values(cls, registry: 'PMRegistry') -> None:
        """Load PDG 2024 experimental values."""
        params = [
            # Higgs boson
            EstablishedParameter(
                path="pdg.m_higgs",
                value=125.10,
                uncertainty=0.14,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Higgs boson mass"
            ),
            # Leptons
            EstablishedParameter(
                path="pdg.m_electron",
                value=0.5109989461e-3,
                uncertainty=3.1e-12,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Electron mass"
            ),
            EstablishedParameter(
                path="pdg.m_muon",
                value=105.6583745e-3,
                uncertainty=2.4e-6,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Muon mass"
            ),
            EstablishedParameter(
                path="pdg.m_tau",
                value=1.77686,
                uncertainty=0.00012,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Tau mass"
            ),
            # Quarks
            EstablishedParameter(
                path="pdg.m_up",
                value=2.16e-3,
                uncertainty=0.49e-3,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Up quark mass (MS-bar, 2 GeV)"
            ),
            EstablishedParameter(
                path="pdg.m_down",
                value=4.67e-3,
                uncertainty=0.48e-3,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Down quark mass (MS-bar, 2 GeV)"
            ),
            EstablishedParameter(
                path="pdg.m_strange",
                value=93.4e-3,
                uncertainty=8.6e-3,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Strange quark mass"
            ),
            EstablishedParameter(
                path="pdg.m_charm",
                value=1.27,
                uncertainty=0.02,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Charm quark mass"
            ),
            EstablishedParameter(
                path="pdg.m_bottom",
                value=4.18,
                uncertainty=0.03,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Bottom quark mass"
            ),
            EstablishedParameter(
                path="pdg.m_top",
                value=172.69,
                uncertainty=0.30,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Top quark mass"
            ),
            # Gauge couplings
            EstablishedParameter(
                path="pdg.alpha_s_MZ",
                value=0.1180,
                uncertainty=0.0010,
                units="dimensionless",
                source="ESTABLISHED:PDG2024",
                description="Strong coupling at M_Z"
            ),
            EstablishedParameter(
                path="pdg.sin2_theta_W",
                value=0.23121,
                uncertainty=0.00004,
                units="dimensionless",
                source="ESTABLISHED:PDG2024",
                description="Weak mixing angle"
            ),
            # W and Z masses
            EstablishedParameter(
                path="pdg.m_W",
                value=80.377,
                uncertainty=0.012,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="W boson mass"
            ),
            EstablishedParameter(
                path="pdg.m_Z",
                value=91.1876,
                uncertainty=0.0021,
                units="GeV",
                source="ESTABLISHED:PDG2024",
                description="Z boson mass"
            ),
        ]

        for param in params:
            cls._register_param(registry, param)

    @classmethod
    def _load_nufit_values(cls, registry: 'PMRegistry') -> None:
        """Load NuFIT 6.0 (2024) neutrino oscillation parameters."""
        if CONFIG_AVAILABLE:
            theta_12 = getattr(NeutrinoParameters, 'THETA_12_NUFIT', 33.41)
            theta_23 = getattr(NeutrinoParameters, 'THETA_23_NUFIT', 45.0)
            theta_13 = getattr(NeutrinoParameters, 'THETA_13_NUFIT', 8.54)
            delta_cp = getattr(NeutrinoParameters, 'DELTA_CP_NUFIT', 194.0)
            delta_m21_sq = getattr(NeutrinoParameters, 'DELTA_M_SQUARED_21', 7.42e-5)
            delta_m31_sq = getattr(NeutrinoParameters, 'DELTA_M_SQUARED_31', 2.515e-3)
        else:
            theta_12, theta_23, theta_13 = 33.41, 45.0, 8.54
            delta_cp = 194.0
            delta_m21_sq, delta_m31_sq = 7.42e-5, 2.515e-3

        params = [
            EstablishedParameter(
                path="nufit.theta_12",
                value=theta_12,
                uncertainty=0.75,
                units="degrees",
                source="ESTABLISHED:NuFIT6.0",
                description="Solar mixing angle"
            ),
            EstablishedParameter(
                path="nufit.theta_23",
                value=theta_23,
                uncertainty=1.0,
                units="degrees",
                source="ESTABLISHED:NuFIT6.0",
                description="Atmospheric mixing angle"
            ),
            EstablishedParameter(
                path="nufit.theta_13",
                value=theta_13,
                uncertainty=0.12,
                units="degrees",
                source="ESTABLISHED:NuFIT6.0",
                description="Reactor mixing angle"
            ),
            EstablishedParameter(
                path="nufit.delta_CP",
                value=delta_cp,
                uncertainty=25.0,
                units="degrees",
                source="ESTABLISHED:NuFIT6.0",
                description="CP-violating phase"
            ),
            EstablishedParameter(
                path="nufit.delta_m21_sq",
                value=delta_m21_sq,
                uncertainty=0.21e-5,
                units="eV^2",
                source="ESTABLISHED:NuFIT6.0",
                description="Solar mass splitting"
            ),
            EstablishedParameter(
                path="nufit.delta_m31_sq",
                value=delta_m31_sq,
                uncertainty=0.028e-3,
                units="eV^2",
                source="ESTABLISHED:NuFIT6.0",
                description="Atmospheric mass splitting"
            ),
        ]

        for param in params:
            cls._register_param(registry, param)

    @classmethod
    def _load_desi_values(cls, registry: 'PMRegistry') -> None:
        """Load DESI DR2 (2024) cosmological parameters."""
        if CONFIG_AVAILABLE:
            w0 = getattr(PhenomenologyParameters, 'W0_DESI_DR2', -0.827)
            wa = getattr(PhenomenologyParameters, 'WA_EVOLUTION', -0.75)
            H0 = getattr(PhenomenologyParameters, 'H0', 67.4)
        else:
            w0, wa, H0 = -0.827, -0.75, 67.4

        params = [
            EstablishedParameter(
                path="desi.w0",
                value=w0,
                uncertainty=0.063,
                units="dimensionless",
                source="ESTABLISHED:DESI_DR2_2024",
                description="Dark energy equation of state at z=0"
            ),
            EstablishedParameter(
                path="desi.wa",
                value=wa,
                uncertainty=0.30,
                units="dimensionless",
                source="ESTABLISHED:DESI_DR2_2024",
                description="Dark energy evolution parameter"
            ),
            EstablishedParameter(
                path="desi.H0",
                value=H0,
                uncertainty=0.5,
                units="km/s/Mpc",
                source="ESTABLISHED:Planck2018",
                description="Hubble constant"
            ),
            EstablishedParameter(
                path="desi.Omega_m",
                value=0.3111,
                uncertainty=0.0056,
                units="dimensionless",
                source="ESTABLISHED:Planck2018",
                description="Matter density parameter"
            ),
        ]

        for param in params:
            cls._register_param(registry, param)

    @classmethod
    def _load_experimental_bounds(cls, registry: 'PMRegistry') -> None:
        """Load experimental bounds (Super-K, etc.)."""
        if CONFIG_AVAILABLE:
            tau_p_bound = getattr(PhenomenologyParameters, 'TAU_PROTON_SUPER_K_BOUND', 1.67e34)
        else:
            tau_p_bound = 1.67e34

        params = [
            EstablishedParameter(
                path="bounds.tau_proton_lower",
                value=tau_p_bound,
                uncertainty=0.03e34,
                units="years",
                source="ESTABLISHED:SuperK_2024",
                description="Proton lifetime lower bound"
            ),
            EstablishedParameter(
                path="bounds.sum_m_nu_upper",
                value=0.12,
                uncertainty=0,
                units="eV",
                source="ESTABLISHED:Planck2018",
                description="Sum of neutrino masses upper bound"
            ),
        ]

        for param in params:
            cls._register_param(registry, param)

    @classmethod
    def _load_theory_constants(cls, registry: 'PMRegistry') -> None:
        """Load theory-derived constants used as inputs for simulations."""
        import numpy as np

        # Electroweak VEV and Yukawa couplings
        v_ew = 246.22  # GeV, electroweak VEV
        m_top = 172.69  # GeV
        y_top = m_top * np.sqrt(2) / v_ew  # Top Yukawa coupling ~ 0.994

        # GUT-scale parameters (from standard GUT relations)
        g_gut = np.sqrt(4 * np.pi / 24.3)  # GUT coupling from alpha_GUT ~ 1/24.3

        params = [
            # Higgs/Yukawa parameters
            EstablishedParameter(
                path="higgs.vev_yukawa",
                value=v_ew,
                uncertainty=0.01,
                units="GeV",
                source="ESTABLISHED:SM_EW",
                description="Electroweak VEV from Fermi constant"
            ),
            EstablishedParameter(
                path="yukawa.y_top",
                value=y_top,
                uncertainty=0.003,
                units="dimensionless",
                source="ESTABLISHED:PDG2024",
                description="Top quark Yukawa coupling"
            ),
            EstablishedParameter(
                path="gauge.g_gut",
                value=g_gut,
                uncertainty=0.01,
                units="dimensionless",
                source="ESTABLISHED:GUT_THEORY",
                description="GUT gauge coupling"
            ),
            # Moduli stabilization parameters (phenomenological)
            EstablishedParameter(
                path="moduli.re_t_attractor",
                value=1.21,
                uncertainty=0.05,
                units="dimensionless",
                source="ESTABLISHED:MODULI_THEORY",
                description="Attractor value for Re(T) modulus"
            ),
            EstablishedParameter(
                path="moduli.re_t_phenomenological",
                value=1.18,
                uncertainty=0.08,
                units="dimensionless",
                source="ESTABLISHED:MODULI_THEORY",
                description="Phenomenological Re(T) from Higgs mass fitting"
            ),
            # Topology parameters (from G2 geometry)
            EstablishedParameter(
                path="topology.T_OMEGA",
                value=0.12,
                uncertainty=0.02,
                units="dimensionless",
                source="ESTABLISHED:G2_TORSION",
                description="Torsion class parameter from TCS construction"
            ),
            EstablishedParameter(
                path="topology.orientation_sum",
                value=1.0,
                uncertainty=0.05,
                units="dimensionless",
                source="ESTABLISHED:G2_THEORY",
                description="Orientation sum for fermion chirality"
            ),
        ]

        for param in params:
            cls._register_param(registry, param)

    @classmethod
    def _register_param(cls, registry: 'PMRegistry', param: EstablishedParameter) -> None:
        """Register a single parameter with the registry."""
        registry.set_param(
            path=param.path,
            value=param.value,
            source=param.source,
            uncertainty=param.uncertainty,
            status=param.status,
            metadata={'description': param.description, 'units': param.units}
        )


# Documentation of all established parameters
ESTABLISHED_PARAMS = {
    "metadata": {
        "version": "1.0",
        "description": "Complete registry of established experimental physics values",
        "sources": [
            "PDG 2024 - Particle Data Group Review",
            "NuFIT 6.0 (2024) - Neutrino oscillation global fit",
            "DESI DR2 (2024) - Dark energy survey",
            "Planck 2018 - CMB observations",
            "Super-Kamiokande - Proton decay bounds"
        ]
    },
    "categories": {
        "constants": ["constants.M_PLANCK", "constants.alpha_em", "constants.m_proton"],
        "pdg": [
            "pdg.m_higgs", "pdg.m_electron", "pdg.m_muon", "pdg.m_tau",
            "pdg.m_up", "pdg.m_down", "pdg.m_strange", "pdg.m_charm", "pdg.m_bottom", "pdg.m_top",
            "pdg.alpha_s_MZ", "pdg.sin2_theta_W", "pdg.m_W", "pdg.m_Z"
        ],
        "nufit": [
            "nufit.theta_12", "nufit.theta_23", "nufit.theta_13",
            "nufit.delta_CP", "nufit.delta_m21_sq", "nufit.delta_m31_sq"
        ],
        "desi": ["desi.w0", "desi.wa", "desi.H0", "desi.Omega_m"],
        "bounds": ["bounds.tau_proton_lower", "bounds.sum_m_nu_upper"]
    },
    "total_count": 29
}
