"""
Principia Metaphysica - Fermion Simulations v18

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

v18.0 Updates:
- New FermionSimulationV18 wrapper consolidating all fermion modules
- Unified CKM/PMNS derivation from octonionic triality
- Full SSOT compliance via PMRegistry
"""

from .chirality_v16_0 import ChiralitySpinorSimulation
from .fermion_generations_v16_0 import FermionGenerationsV16
from .ckm_matrix_v16_0 import CKMMatrixSimulation
from .muon_g2_anomaly_v16_1 import MuonG2AnomalySimulation
from .octonionic_mixing_v16_2 import OctonionicMixing
from .g2_triality_mixing_v17 import G2TrialityMixing

# V18 SimulationBase wrapper (primary export)
from .fermion_simulation_v18 import FermionSimulationV18, run_fermion_simulation

# V18 Yukawa texture analysis
from .yukawa_textures_v18 import YukawaTexturesV18, YukawaResult

# Conditionally import MassRatioSimulation (requires schema availability)
try:
    from .mass_ratio_v16_1 import MassRatioSimulation
    _MASS_RATIO_AVAILABLE = True
except ImportError:
    _MASS_RATIO_AVAILABLE = False

__all__ = [
    # V16 modules
    'ChiralitySpinorSimulation',
    'FermionGenerationsV16',
    'CKMMatrixSimulation',
    'MuonG2AnomalySimulation',
    'OctonionicMixing',
    'G2TrialityMixing',
    # V18 wrapper
    'FermionSimulationV18',
    'run_fermion_simulation',
    # V18 Yukawa
    'YukawaTexturesV18',
    'YukawaResult',
]

if _MASS_RATIO_AVAILABLE:
    __all__.append('MassRatioSimulation')

__version__ = "18.3"
