"""
Principia Metaphysica - Flavor Physics Simulations (v16)

This module contains simulations related to flavor physics:
- CP phases from pair interference
- Mixing matrices (CKM/PMNS)
- Flavor hierarchies

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .cp_phases_v22 import CPPhasesSimulation, run_cp_phases

__all__ = [
    "CPPhasesSimulation",
    "run_cp_phases",
]
