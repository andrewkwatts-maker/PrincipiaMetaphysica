"""
Pneuma Simulations v16
======================

V16 simulations for the Pneuma field dynamics and geometric framework.

This module contains simulations for Section 2 (Geometric Framework) that
compute Pneuma field properties, coupling constants, and Lagrangian validity.

Simulations:
- pneuma_mechanism_v16_0: Core Pneuma field dynamics and geometric coupling

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .pneuma_mechanism_v16_0 import PneumaMechanismV16

__all__ = ['PneumaMechanismV16']

__version__ = "16.0"
