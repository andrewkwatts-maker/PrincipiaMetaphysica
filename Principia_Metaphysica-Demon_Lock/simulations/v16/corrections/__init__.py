"""
Corrections Module v18.0
========================

Radiative and higher-order corrections to geometric predictions.

This module bridges tree-level geometric predictions to loop-corrected
physical observables using standard QED/EW radiative corrections.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .gf_radiative_correction_v18 import GFRadiativeCorrectionV18

__all__ = [
    "GFRadiativeCorrectionV18",
]
