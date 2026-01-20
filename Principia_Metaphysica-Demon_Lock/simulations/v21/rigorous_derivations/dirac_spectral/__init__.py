"""
Dirac Spectral Module
======================

Rigorous derivations involving the Dirac operator spectrum on G2 manifolds,
including fermion generation counting via the Atiyah-Singer index theorem
and fermion mass hierarchy from Laplace-Beltrami eigenvalues.

MODULES:
-------
1. zero_mode_index_v18: Generation counting via Atiyah-Singer index
2. laplacian_eigenvalue_v18: Fermion mass hierarchy from Laplacian spectrum

MATHEMATICAL FOUNDATIONS (Established Physics):
----------------------------------------------
- Weyl's Law (1911): N(lambda) ~ lambda^(d/2) for d-dimensional manifolds
- Spectral Geometry: Eigenvalues encode geometric information
- Kaluza-Klein: m^2 = lambda_n / R^2 from dimensional reduction
- G2 Specialization: b3=24 cycles organize into 3 fermion generations

KEY FORMULA:
-----------
m_f = m_ref * sqrt(lambda_n) * (V_G2/V_cycle)^(1/3) * exp(-S_inst)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .zero_mode_index_v18 import (
    ZeroModeIndexV18,
    run_zero_mode_index_simulation,
)

from .laplacian_eigenvalue_v18 import (
    G2ManifoldParams,
    G2GraphLaplacian,
    FermionMassSpectrum,
    run_spectral_analysis,
    FERMION_MASSES_MEV,
    LEPTON_MASS_RATIOS,
)

# Conditionally export SimulationBase wrapper if available
try:
    from .laplacian_eigenvalue_v18 import LaplacianEigenvalueSimulation
    __all__ = [
        # Zero mode index
        'ZeroModeIndexV18',
        'run_zero_mode_index_simulation',
        # Laplacian eigenvalue
        'G2ManifoldParams',
        'G2GraphLaplacian',
        'FermionMassSpectrum',
        'LaplacianEigenvalueSimulation',
        'run_spectral_analysis',
        'FERMION_MASSES_MEV',
        'LEPTON_MASS_RATIOS',
    ]
except ImportError:
    __all__ = [
        # Zero mode index
        'ZeroModeIndexV18',
        'run_zero_mode_index_simulation',
        # Laplacian eigenvalue (no SimulationBase)
        'G2ManifoldParams',
        'G2GraphLaplacian',
        'FermionMassSpectrum',
        'run_spectral_analysis',
        'FERMION_MASSES_MEV',
        'LEPTON_MASS_RATIOS',
    ]
