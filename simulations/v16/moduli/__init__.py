"""
Principia Metaphysica - Moduli Stabilization Module
=====================================================

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

This module provides moduli stabilization simulations for G2 manifold
compactifications. Key features:

1. Racetrack Potential Stabilization
   - Competing non-perturbative effects from gaugino condensation
   - VEV from flux quantization: <T> = ln(Aa/Bb)/(a-b)

2. KKLT Framework
   - F-term SUSY breaking with de Sitter uplift
   - Swampland constraint verification

3. Vacuum Stability Analysis
   - Hessian positivity at racetrack minimum
   - Moduli mass spectrum

Key Classes:
- ModuliSimulationV18: Main v18 SimulationBase wrapper

Key Functions:
- run_moduli_simulation(): Standalone execution with verbose output

References:
- KKLT (2003): arXiv:hep-th/0301240
- Acharya et al. (2010): arXiv:1006.5559
- CHNP (2015): TCS G2 constructions
"""

from .moduli_simulation_v18 import (
    ModuliSimulationV18,
    run_moduli_simulation,
)

__all__ = [
    # Main simulation class
    'ModuliSimulationV18',

    # Convenience function
    'run_moduli_simulation',
]

__version__ = "19.2"
