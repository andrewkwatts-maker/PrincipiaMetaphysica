"""
Validation Module
=================

Input validation and result verification utilities.

Features:
- Type checking with dataclass validation
- Physical constraint validation (positive masses, valid angles, etc.)
- Experimental comparison with sigma calculation
- Consistency checks across simulation results

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple, Callable
import numpy as np


@dataclass
class ValidationResult:
    """Result of a validation check"""
    valid: bool
    message: str
    value: Optional[Any] = None
    expected: Optional[Any] = None
    deviation: Optional[float] = None  # In sigma or percent


class PhysicsValidator:
    """
    Validates physical quantities against known constraints.

    Ensures:
    - Masses are positive
    - Angles are in valid ranges
    - Probabilities are between 0 and 1
    - Dimensionless couplings are reasonable
    """

    @staticmethod
    def validate_mass(value: float, name: str = "mass", min_val: float = 0) -> ValidationResult:
        """Validate a mass value (must be non-negative)"""
        if value < min_val:
            return ValidationResult(
                valid=False,
                message=f"{name} = {value} is below minimum {min_val}",
                value=value
            )
        if np.isnan(value) or np.isinf(value):
            return ValidationResult(
                valid=False,
                message=f"{name} = {value} is NaN or Inf",
                value=value
            )
        return ValidationResult(valid=True, message=f"{name} = {value:.6g} is valid", value=value)

    @staticmethod
    def validate_angle(value: float, name: str = "angle", unit: str = "degrees") -> ValidationResult:
        """Validate an angle (0 to 360 degrees or 0 to 2pi radians)"""
        if unit == "degrees":
            max_val = 360
        else:
            max_val = 2 * np.pi

        if value < 0 or value > max_val:
            return ValidationResult(
                valid=False,
                message=f"{name} = {value} is outside [0, {max_val}] {unit}",
                value=value
            )
        return ValidationResult(valid=True, message=f"{name} = {value:.2f} {unit} is valid", value=value)

    @staticmethod
    def validate_probability(value: float, name: str = "probability") -> ValidationResult:
        """Validate a probability (0 to 1)"""
        if value < 0 or value > 1:
            return ValidationResult(
                valid=False,
                message=f"{name} = {value} is outside [0, 1]",
                value=value
            )
        return ValidationResult(valid=True, message=f"{name} = {value:.4f} is valid", value=value)

    @staticmethod
    def validate_coupling(
        value: float,
        name: str = "coupling",
        min_val: float = 0,
        max_val: float = 10
    ) -> ValidationResult:
        """Validate a dimensionless coupling constant"""
        if value < min_val or value > max_val:
            return ValidationResult(
                valid=False,
                message=f"{name} = {value} is outside [{min_val}, {max_val}]",
                value=value
            )
        return ValidationResult(valid=True, message=f"{name} = {value:.6f} is valid", value=value)


class ExperimentalComparator:
    """
    Compares theoretical predictions with experimental data.

    Provides:
    - Sigma deviation calculations
    - Percent error calculations
    - Agreement assessment
    """

    @staticmethod
    def sigma_deviation(
        predicted: float,
        experimental: float,
        uncertainty: float
    ) -> Tuple[float, ValidationResult]:
        """
        Calculate deviation in standard deviations (sigma).

        Args:
            predicted: Theoretical prediction
            experimental: Experimental central value
            uncertainty: Experimental 1-sigma uncertainty

        Returns:
            (deviation_sigma, ValidationResult)
        """
        if uncertainty == 0:
            if predicted == experimental:
                return 0.0, ValidationResult(
                    valid=True,
                    message="Exact match (no uncertainty)",
                    deviation=0.0
                )
            else:
                return float('inf'), ValidationResult(
                    valid=False,
                    message="Cannot compute sigma with zero uncertainty",
                    deviation=float('inf')
                )

        sigma = abs(predicted - experimental) / uncertainty

        # Assess agreement level
        if sigma <= 1.0:
            message = f"Excellent agreement ({sigma:.2f} sigma)"
            valid = True
        elif sigma <= 2.0:
            message = f"Good agreement ({sigma:.2f} sigma)"
            valid = True
        elif sigma <= 3.0:
            message = f"Marginal agreement ({sigma:.2f} sigma)"
            valid = True
        else:
            message = f"Poor agreement ({sigma:.2f} sigma > 3)"
            valid = False

        return sigma, ValidationResult(
            valid=valid,
            message=message,
            value=predicted,
            expected=experimental,
            deviation=sigma
        )

    @staticmethod
    def percent_error(predicted: float, experimental: float) -> Tuple[float, ValidationResult]:
        """
        Calculate percent error from experimental value.

        Args:
            predicted: Theoretical prediction
            experimental: Experimental value

        Returns:
            (percent_error, ValidationResult)
        """
        if experimental == 0:
            return float('inf'), ValidationResult(
                valid=False,
                message="Cannot compute percent error with zero experimental value"
            )

        error = abs(predicted - experimental) / abs(experimental) * 100

        if error <= 1.0:
            message = f"Excellent match ({error:.2f}% error)"
            valid = True
        elif error <= 5.0:
            message = f"Good match ({error:.2f}% error)"
            valid = True
        elif error <= 10.0:
            message = f"Acceptable match ({error:.2f}% error)"
            valid = True
        else:
            message = f"Poor match ({error:.2f}% error > 10%)"
            valid = False

        return error, ValidationResult(
            valid=valid,
            message=message,
            value=predicted,
            expected=experimental,
            deviation=error
        )


class ConsistencyChecker:
    """
    Checks consistency across multiple simulation results.

    Ensures:
    - Parameters derived in multiple ways agree
    - Intermediate results satisfy physical relations
    - Conservation laws are respected
    """

    def __init__(self):
        self.checks: List[Tuple[str, Callable[[], ValidationResult]]] = []

    def add_check(self, name: str, check_fn: Callable[[], ValidationResult]):
        """Add a consistency check"""
        self.checks.append((name, check_fn))

    def run_all(self) -> Dict[str, ValidationResult]:
        """Run all consistency checks"""
        results = {}
        for name, check_fn in self.checks:
            try:
                results[name] = check_fn()
            except Exception as e:
                results[name] = ValidationResult(
                    valid=False,
                    message=f"Check failed with exception: {e}"
                )
        return results

    def all_passed(self, results: Optional[Dict[str, ValidationResult]] = None) -> bool:
        """Check if all validations passed"""
        if results is None:
            results = self.run_all()
        return all(r.valid for r in results.values())


# Pre-defined validation functions for common PM quantities

def validate_n_gen(n: int) -> ValidationResult:
    """Validate number of fermion generations"""
    if n != 3:
        return ValidationResult(
            valid=False,
            message=f"n_gen = {n} (expected 3)",
            value=n,
            expected=3
        )
    return ValidationResult(valid=True, message="n_gen = 3 (correct)", value=3)


def validate_chi_eff(chi: int) -> ValidationResult:
    """Validate effective Euler characteristic"""
    if chi != 144:
        return ValidationResult(
            valid=False,
            message=f"chi_eff = {chi} (expected 144)",
            value=chi,
            expected=144
        )
    return ValidationResult(valid=True, message="chi_eff = 144 (correct)", value=144)


def validate_m_gut(m_gut: float, tolerance_percent: float = 5.0) -> ValidationResult:
    """Validate M_GUT against expected range"""
    expected = 2.118e16
    error_pct = abs(m_gut - expected) / expected * 100

    if error_pct > tolerance_percent:
        return ValidationResult(
            valid=False,
            message=f"M_GUT = {m_gut:.3e} GeV ({error_pct:.1f}% from expected)",
            value=m_gut,
            expected=expected,
            deviation=error_pct
        )
    return ValidationResult(
        valid=True,
        message=f"M_GUT = {m_gut:.3e} GeV (within {tolerance_percent}%)",
        value=m_gut,
        expected=expected,
        deviation=error_pct
    )


def validate_proton_lifetime(tau_p: float) -> ValidationResult:
    """Validate proton lifetime against Super-K bound"""
    super_k_bound = 1.67e34  # years

    if tau_p < super_k_bound:
        return ValidationResult(
            valid=False,
            message=f"tau_p = {tau_p:.2e} years < Super-K bound {super_k_bound:.2e}",
            value=tau_p,
            expected=super_k_bound
        )
    ratio = tau_p / super_k_bound
    return ValidationResult(
        valid=True,
        message=f"tau_p = {tau_p:.2e} years ({ratio:.1f}x Super-K bound)",
        value=tau_p,
        expected=super_k_bound,
        deviation=ratio
    )
