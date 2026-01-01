"""
PRINCIPIA METAPHYSICA v16.2 - Validation Package
=================================================

Geometric validation and constraint checking modules.
"""

from .anisotropy_check import (
    verify_4_pattern_orthogonality,
    validate_torsion_matrix,
    AnisotropyError,
    InconsistencyError,
    IsotropyResult,
)

__all__ = [
    "verify_4_pattern_orthogonality",
    "validate_torsion_matrix",
    "AnisotropyError",
    "InconsistencyError",
    "IsotropyResult",
]
