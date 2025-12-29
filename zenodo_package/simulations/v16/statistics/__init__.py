"""
Statistics Module for Principia Metaphysica v16
================================================

Statistical analysis and validation tools with proper treatment of
correlated uncertainties using covariance matrices.

Simulations:
- rigor_covariance_v16_1: Chi-square analysis with full covariance matrices

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .rigor_covariance_v16_1 import (
    RigorCovarianceV16_1,
    CovarianceData,
    ChiSquareResult,
    run_covariance_analysis,
)

__all__ = [
    "RigorCovarianceV16_1",
    "CovarianceData",
    "ChiSquareResult",
    "run_covariance_analysis",
]
