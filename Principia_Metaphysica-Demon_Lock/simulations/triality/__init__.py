"""
Triality Module for Principia Metaphysica
==========================================

This module implements the mathematical foundations of G2 triality
and octonionic structures for fermion generation physics.

Key Components:
- fano_plane.py: Octonion multiplication via Fano plane
- octonion_algebra.py: Full octonion algebra implementation
- spin7_automorphism.py: Spin(7) outer automorphism for shadow duality

Key Physics:
- G2 ~ Aut(O): G2 is automorphisms of octonions
- Triality: 7 = 1 + 3 + 3' decomposition
- n_gen = chi_eff/48 = 144/48 = 3 exactly

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .fano_plane import FanoPlane, OctonionMultiplier
from .spin7_automorphism import Spin7Automorphism

__all__ = [
    'FanoPlane',
    'OctonionMultiplier',
    'Spin7Automorphism',
]
