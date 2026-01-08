"""
Principia Metaphysica - Validation Module v17.2

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

This module contains validation scripts for testing the theory's
geometric predictions against experimental data.
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

__all__ = [
    'RigorousValidatorV16_1',
    'PrincipiaResidueCalculator',
    'CosmologyValidation',
    'run_residue_calculator',
    'run_cosmology_validation',
]

__version__ = "17.2"
