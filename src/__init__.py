"""
PRINCIPIA METAPHYSICA v16.2 - Core Source Package
==================================================

This package contains the core physics and validation modules
for the Sterile Model implementation.

Subpackages:
    - physics: Core 288-root derivation logic
    - validation: Anisotropy and isotropy checks
    - audit: Certificate stack and Omega Seal generation
"""

from .physics.root_derivation import RootDerivation, BulkInsulationConstant
from .validation.anisotropy_check import verify_4_pattern_orthogonality, AnisotropyError
from .audit.certificate_stack import CertificateStack, CertificateStatus
from .audit.omega_seal_generator import generate_omega_seal, OmegaSeal

__version__ = "19.2"
__all__ = [
    "RootDerivation",
    "BulkInsulationConstant",
    "verify_4_pattern_orthogonality",
    "AnisotropyError",
    "CertificateStack",
    "CertificateStatus",
    "generate_omega_seal",
    "OmegaSeal",
]
