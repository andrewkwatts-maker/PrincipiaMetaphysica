"""
Spectral Module v18.0
=====================

Spectral analysis of the G2 manifold Laplacian.

This module contains the complete registry of 125 spectral residues
that generate the particle mass spectrum via dimensional reduction.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .complete_residue_registry_v18 import (
    CompleteResidueRegistryV18,
    SpectralResidue,
    RESIDUE_REGISTRY,
)

__all__ = [
    "CompleteResidueRegistryV18",
    "SpectralResidue",
    "RESIDUE_REGISTRY",
]
