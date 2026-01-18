"""
Principia Metaphysica - Physical Constants Derivations v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

This module contains derivations of fundamental physical constants
from G2 manifold geometry and sterile residue extraction.

v18.0: SimulationBase-compliant wrappers with scientific honesty labels.
"""

# Core derivation classes (v17 implementations)
from .fine_structure_v17 import FineStructureDerivation, run_fine_structure_demo
from .sterile_angle_v17 import SterileAngleDerivation, run_sterile_angle_demo
from .speed_of_light_v17 import SpeedOfLightDerivation, run_speed_of_light_demo
from .weak_mixing_v17 import WeakMixingAngle, run_weak_mixing_demo
from .fermion_generations_v17 import FermionGenerations, run_generations_demo
from .parameter_residues_v17 import ParameterResidueExtractor, run_residue_demo

# SimulationBase wrapper (v18)
from .constants_simulation_v18 import ConstantsSimulationV18, run_constants_simulation

__all__ = [
    # Core classes
    'FineStructureDerivation',
    'SterileAngleDerivation',
    'SpeedOfLightDerivation',
    'WeakMixingAngle',
    'FermionGenerations',
    'ParameterResidueExtractor',
    # Demo functions
    'run_fine_structure_demo',
    'run_sterile_angle_demo',
    'run_speed_of_light_demo',
    'run_weak_mixing_demo',
    'run_generations_demo',
    'run_residue_demo',
    # SimulationBase wrapper
    'ConstantsSimulationV18',
    'run_constants_simulation',
]

__version__ = "19.2"
