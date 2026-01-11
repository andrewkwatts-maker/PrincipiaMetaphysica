"""
Principia Metaphysica - Cosmology Simulations v18

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

v18.0 Updates:
- New CosmologySimulationV18 wrapper consolidating all cosmology modules
- Hubble tension resolution via Ricci flow
- Dark energy thawing from G2 topology
- Full SSOT compliance via PMRegistry
"""

from .cosmology_intro_v16_0 import CosmologyIntroV16
from .dark_energy_v16_0 import DarkEnergyV16
from .dark_energy_thawing_v16_2 import DarkEnergyEvolution
from .multi_sector_v16_0 import MultiSectorV16
from .s8_suppression_v16_1 import S8SuppressionV16
from .ricci_flow_h0_v16_1 import RicciFlowH0V16
from .evolution_engine_v16_2 import EvolutionEngineV16
from .speed_of_light_v17_2 import SpeedOfLightV17

# V18 SimulationBase wrapper (primary export)
from .cosmology_simulation_v18 import CosmologySimulationV18, run_cosmology_simulation

# V18 Refined derivations for high-sigma fixes
from .cmb_temperature_v18 import CMBTemperatureV18
from .baryon_asymmetry_v18 import BaryonAsymmetryV18
from .attractor_potential_v18 import AttractorPotentialV18

# Optional: cosmological constant derivation
try:
    from .cosmological_constant_v16_1 import CosmologicalConstantV16
    _COSMOLOGICAL_CONSTANT_AVAILABLE = True
except ImportError:
    _COSMOLOGICAL_CONSTANT_AVAILABLE = False

__all__ = [
    # V16/V17 modules
    'CosmologyIntroV16',
    'DarkEnergyV16',
    'DarkEnergyEvolution',
    'MultiSectorV16',
    'S8SuppressionV16',
    'RicciFlowH0V16',
    'EvolutionEngineV16',
    'SpeedOfLightV17',
    # V18 wrapper
    'CosmologySimulationV18',
    'run_cosmology_simulation',
    # V18 refined derivations
    'CMBTemperatureV18',
    'BaryonAsymmetryV18',
    'AttractorPotentialV18',
]

if _COSMOLOGICAL_CONSTANT_AVAILABLE:
    __all__.append('CosmologicalConstantV16')

__version__ = "19.2"
