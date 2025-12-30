"""
Principia Metaphysica - Cosmology Simulations v16

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .cosmology_intro_v16_0 import CosmologyIntroV16
from .dark_energy_v16_0 import DarkEnergyV16
from .dark_energy_thawing_v16_2 import DarkEnergyEvolution
from .multi_sector_v16_0 import MultiSectorV16
from .s8_suppression_v16_1 import S8SuppressionV16
from .ricci_flow_h0_v16_1 import RicciFlowH0V16
from .evolution_engine_v16_2 import EvolutionEngineV16

# Optional: cosmological constant derivation
try:
    from .cosmological_constant_v16_1 import CosmologicalConstantV16
    _COSMOLOGICAL_CONSTANT_AVAILABLE = True
except ImportError:
    _COSMOLOGICAL_CONSTANT_AVAILABLE = False

__all__ = [
    'CosmologyIntroV16',
    'DarkEnergyV16',
    'DarkEnergyEvolution',
    'MultiSectorV16',
    'S8SuppressionV16',
    'RicciFlowH0V16',
    'EvolutionEngineV16',
]

if _COSMOLOGICAL_CONSTANT_AVAILABLE:
    __all__.append('CosmologicalConstantV16')

__version__ = "16.2"
