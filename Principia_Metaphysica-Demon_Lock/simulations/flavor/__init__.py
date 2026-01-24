"""
Flavor Physics Module for Principia Metaphysica
================================================

This module implements the unified CKM/PMNS mixing matrix derivation
from G2 triality and dual-shadow geometry.

Key Components:
- unified_mixing_matrices.py: Complete CKM/PMNS from triality
- fano_plane.py: Octonion multiplication tables

Key Physics:
- G2 triality geometrically forces exactly 3 generations
- Normal shadow: Asymmetric residue fluxes -> hierarchical CKM
- Mirror shadow: Symmetric fluxes + OR flip -> democratic PMNS
- CP violation from multi-pair OR interference

SSOT Constants:
- chi_eff = 72 (per-sector effective Euler characteristic)
- chi_eff_total = 144 (cross-shadow total)
- b_3 = 24
- n_gen = chi_eff/24 = 3 (per-sector formula) OR chi_eff_total/48 = 3 (total formula)
- lambda_Cabibbo = 0.224
- theta_23_PMNS ~ 45 degrees

PMNS uses chi_eff_total (144) because neutrinos propagate across both shadows.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

# Import the main simulation class
# Note: Running standalone (python unified_mixing_matrices.py) works directly
from .unified_mixing_matrices import (
    UnifiedMixingMatricesSimulation,
    G2Triality,
    CKMFromNormalShadow,
    PMNSFromMirrorShadow,
    YukawaFromTriality,
    ResidueFluxStructure,
)

__all__ = [
    'UnifiedMixingMatricesSimulation',
    'G2Triality',
    'CKMFromNormalShadow',
    'PMNSFromMirrorShadow',
    'YukawaFromTriality',
    'ResidueFluxStructure',
]
