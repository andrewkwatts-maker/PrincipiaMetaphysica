"""
Principia Metaphysica - Validation Module v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

This module contains validation scripts for testing the theory's
geometric predictions against experimental data.

v18.0: Added consolidated SimulationBase wrapper for unified validation.
"""

from .rigorous_validator_v16_1 import RigorousValidatorV16_1
from .principia_residue_calculator_v17 import (
    PrincipiaResidueCalculator,
    run_residue_calculator,
)
from .cosmology_validation_v17 import (
    CosmologyValidation,
    run_cosmology_validation,
)
from .validation_simulation_v18 import (
    ValidationSimulationV18,
    run_validation_simulation,
)

__all__ = [
    # v16/v17 modules
    'RigorousValidatorV16_1',
    'PrincipiaResidueCalculator',
    'CosmologyValidation',
    'run_residue_calculator',
    'run_cosmology_validation',
    # v18 consolidated wrapper
    'ValidationSimulationV18',
    'run_validation_simulation',
]

__version__ = "19.2"
