"""
Principia Metaphysica - Fermion Simulations v16

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .chirality_v16_0 import ChiralitySpinorSimulation
from .fermion_generations_v16_0 import FermionGenerationsV16
from .ckm_matrix_v16_0 import CKMMatrixSimulation
from .muon_g2_anomaly_v16_1 import MuonG2AnomalySimulation
from .octonionic_mixing_v16_2 import OctonionicMixing

# Conditionally import MassRatioSimulation (requires schema availability)
try:
    from .mass_ratio_v16_1 import MassRatioSimulation
    _MASS_RATIO_AVAILABLE = True
except ImportError:
    _MASS_RATIO_AVAILABLE = False

__all__ = [
    'ChiralitySpinorSimulation',
    'FermionGenerationsV16',
    'CKMMatrixSimulation',
    'MuonG2AnomalySimulation',
    'OctonionicMixing',
]

if _MASS_RATIO_AVAILABLE:
    __all__.append('MassRatioSimulation')
