"""
Charge Cohomology Module
========================

Rigorous derivations of electric charge from cohomological, spectral,
and topological methods on G2 manifolds.

This module contains:
- SpectralFlowChargeV18: Charge quantization from spectral flow
- DiracOperatorG2: Dirac operator on G2 lattice
- APSIndexCalculator: Atiyah-Patodi-Singer index computation
- DiracMonopoleChargeQuantization: Dirac monopole condition in G2

Key Physics:
- Dirac quantization condition: eg = n*hbar*c/2 implies charge quantization
- G2 manifold provides natural monopole configurations via pi_2(G/H)
- Fractional charges {1/3, 2/3, 1} emerge from Z_3 center of SU(3)
- Intersection numbers on associative 3-cycles give integer charge assignments

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .spectral_flow_charge_v18 import (
    SpectralFlowChargeV18,
    DiracOperatorG2,
    SpectralFlowCalculator,
    APSIndexCalculator,
    ChargeQuantizationDerivation,
    SpectralFlowResult,
    APSIndexResult,
    run_spectral_flow_charge_simulation,
)

from .dirac_monopole_charge_v18 import (
    DiracMonopoleChargeQuantization,
    run_dirac_monopole_charge_simulation,
)

__all__ = [
    'SpectralFlowChargeV18',
    'DiracOperatorG2',
    'SpectralFlowCalculator',
    'APSIndexCalculator',
    'ChargeQuantizationDerivation',
    'SpectralFlowResult',
    'APSIndexResult',
    'run_spectral_flow_charge_simulation',
    'DiracMonopoleChargeQuantization',
    'run_dirac_monopole_charge_simulation',
]
