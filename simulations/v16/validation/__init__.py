"""
Principia Metaphysica v16 Validation Module
============================================

This module contains validation simulations that compare PM v16.1 predictions
against the latest observational data from NuFIT 6.0 (2025), DESI (2025),
and Planck (2025).

Available validators:
- rigorous_validator_v16_1: Comprehensive validation against latest datasets

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .rigorous_validator_v16_1 import RigorousValidatorV16_1

__all__ = [
    'RigorousValidatorV16_1',
]

__version__ = "16.1"
