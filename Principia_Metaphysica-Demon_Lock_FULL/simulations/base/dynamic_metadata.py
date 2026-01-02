#!/usr/bin/env python3
"""
Dynamic Metadata Helper - Generate Description Strings from Computed Values
============================================================================

This module provides helper functions to generate metadata description strings
dynamically from computed simulation values, avoiding hardcoded numeric values
that can become stale when formulas are updated.

USAGE:
    from simulations.base.dynamic_metadata import MetadataBuilder

    # In simulation run() method:
    w0 = self._derive_dark_energy_eos(D_eff)  # Compute value

    # Generate description dynamically:
    description = MetadataBuilder.w0_description(w0, target=-0.957, sigma=0.067)
    # Returns: "w₀ = -23/24 = -0.9583. DESI 2025: w₀ = -0.957 ± 0.067. Deviation: 0.02σ."

PRINCIPLES:
    1. Computed values should NEVER be hardcoded in metadata strings
    2. All numeric values in descriptions should be generated from computed values
    3. Deviations and sigma values should be computed, not written manually
    4. Fractions should be detected automatically where possible

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Optional, Tuple, Dict, Any
import numpy as np
from fractions import Fraction


class MetadataBuilder:
    """
    Helper class for generating dynamic metadata strings from computed values.

    All methods are static - they take computed values and return formatted strings.
    """

    # Known simple fractions for common PM values
    KNOWN_FRACTIONS = {
        # w0 values
        -0.8461538461538461: "-11/13",  # Old formula
        -0.9583333333333333: "-23/24",  # v16.2 thawing
        -0.9583333333333334: "-23/24",  # Float precision variant
        # Other common ratios
        0.041666666666666664: "1/24",
        0.04166666666666666: "1/24",
        1.5: "3/2",
        0.5: "1/2",
        0.25: "1/4",
        0.75: "3/4",
        0.333333333333333: "1/3",
        0.666666666666666: "2/3",
    }

    @staticmethod
    def find_fraction(value: float, tolerance: float = 1e-9) -> Optional[str]:
        """
        Find a simple fraction representation for a computed value.

        Args:
            value: The computed numeric value
            tolerance: Tolerance for matching known fractions

        Returns:
            String fraction like "11/13" or None if no simple fraction found
        """
        # Check known fractions first
        for known_val, frac_str in MetadataBuilder.KNOWN_FRACTIONS.items():
            if abs(value - known_val) < tolerance:
                return frac_str

        # Try to find a simple fraction (denominator <= 100)
        try:
            frac = Fraction(value).limit_denominator(100)
            if abs(float(frac) - value) < tolerance:
                return f"{frac.numerator}/{frac.denominator}"
        except (ValueError, OverflowError):
            pass

        return None

    @staticmethod
    def compute_sigma(predicted: float, target: float, uncertainty: float) -> float:
        """
        Compute sigma deviation between predicted and target values.

        Args:
            predicted: The computed/predicted value
            target: The experimental target value
            uncertainty: The experimental uncertainty (1σ)

        Returns:
            Absolute deviation in units of sigma
        """
        if uncertainty <= 0:
            return float('inf')
        return abs(predicted - target) / uncertainty

    @staticmethod
    def format_value(value: float, precision: int = 4) -> str:
        """
        Format a numeric value, showing fraction if available.

        Args:
            value: The computed value
            precision: Decimal places for numeric display

        Returns:
            Formatted string like "-23/24 = -0.9583" or just "-0.9583"
        """
        frac = MetadataBuilder.find_fraction(value)
        if frac:
            return f"{frac} = {value:.{precision}f}"
        return f"{value:.{precision}f}"

    @staticmethod
    def w0_description(
        w0: float,
        target: float = -0.957,
        uncertainty: float = 0.067,
        source: str = "DESI 2025 (thawing)"
    ) -> str:
        """
        Generate dynamic description for dark energy equation of state w₀.

        Args:
            w0: The computed w₀ value
            target: Experimental target value
            uncertainty: Experimental uncertainty
            source: Source of experimental value

        Returns:
            Formatted description string with computed values
        """
        sigma = MetadataBuilder.compute_sigma(w0, target, uncertainty)
        value_str = MetadataBuilder.format_value(w0)

        return (
            f"Dark energy equation of state derived from G2 thawing dynamics: "
            f"w₀ = {value_str}. "
            f"{source}: w₀ = {target} ± {uncertainty}. "
            f"Deviation: {sigma:.2f}σ. "
            f"{'Excellent agreement.' if sigma < 1 else 'Good agreement.' if sigma < 2 else 'Moderate tension.'}"
        )

    @staticmethod
    def w0_formula_latex(w0: float, b3: int = 24) -> str:
        """
        Generate LaTeX formula for w₀ derivation.

        Args:
            w0: The computed w₀ value
            b3: Number of associative 3-cycles

        Returns:
            LaTeX formula string
        """
        numerator = b3 - 1
        return rf"w_0 = -1 + \frac{{1}}{{b_3}} = -\frac{{{numerator}}}{{{b3}}} \approx {w0:.4f}"

    @staticmethod
    def angle_description(
        name: str,
        predicted: float,
        target: float,
        uncertainty: float,
        source: str = "NuFIT 6.0"
    ) -> str:
        """
        Generate dynamic description for mixing angle predictions.

        Args:
            name: Name of the angle (e.g., "theta_12", "delta_CP")
            predicted: The computed angle value in degrees
            target: Experimental target value in degrees
            uncertainty: Experimental uncertainty
            source: Source of experimental value

        Returns:
            Formatted description string
        """
        sigma = MetadataBuilder.compute_sigma(predicted, target, uncertainty)

        return (
            f"PMNS {name} from G2 geometry: {predicted:.2f}°. "
            f"{source}: {target}° ± {uncertainty}°. "
            f"Deviation: {sigma:.2f}σ."
        )

    @staticmethod
    def delta_cp_description(
        delta_cp: float,
        target: float = 278.0,
        uncertainty: float = 22.0,
        source: str = "NuFIT 6.0 IO",
        parity_offset: float = 45.9
    ) -> str:
        """
        Generate dynamic description for delta_CP with parity offset.

        Args:
            delta_cp: The computed delta_CP value in degrees
            target: Experimental target value
            uncertainty: Experimental uncertainty
            source: Source of experimental value
            parity_offset: The 13D parity offset applied

        Returns:
            Formatted description string
        """
        sigma = MetadataBuilder.compute_sigma(delta_cp, target, uncertainty)

        return (
            f"CP-violating phase from cycle intersection complex structure with "
            f"13D parity offset ({parity_offset}°): δ_CP = {delta_cp:.1f}°. "
            f"{source}: {target}° ± {uncertainty}°. "
            f"Deviation: {sigma:.2f}σ. "
            f"{'Excellent agreement.' if sigma < 1 else 'Good agreement.' if sigma < 2 else 'Moderate tension.'}"
        )

    @staticmethod
    def alpha_description(
        alpha_inv: float,
        target: float = 137.036,
        uncertainty: float = 0.001,
        source: str = "CODATA 2022"
    ) -> str:
        """
        Generate dynamic description for fine structure constant.

        Args:
            alpha_inv: The computed 1/α value
            target: Experimental target value
            uncertainty: Experimental uncertainty
            source: Source of experimental value

        Returns:
            Formatted description string
        """
        sigma = MetadataBuilder.compute_sigma(alpha_inv, target, uncertainty)
        deviation_ppm = abs(alpha_inv - target) / target * 1e6

        return (
            f"Fine structure constant from G2 geometry with RG running: "
            f"α⁻¹ = {alpha_inv:.6f}. "
            f"{source}: α⁻¹ = {target:.6f} ± {uncertainty}. "
            f"Deviation: {deviation_ppm:.1f} ppm ({sigma:.2f}σ)."
        )

    @staticmethod
    def validation_summary(
        param_name: str,
        predicted: float,
        target: float,
        uncertainty: float,
        source: str,
        units: str = ""
    ) -> Dict[str, Any]:
        """
        Generate a complete validation dictionary for a parameter.

        Args:
            param_name: Name of the parameter
            predicted: Computed value
            target: Experimental target
            uncertainty: Experimental uncertainty
            source: Data source
            units: Units string (optional)

        Returns:
            Dictionary with all validation fields
        """
        sigma = MetadataBuilder.compute_sigma(predicted, target, uncertainty)

        # Determine status based on sigma deviation
        if sigma < 1.0:
            status = "PASS"
        elif sigma < 2.0:
            status = "GOOD"
        elif sigma < 3.0:
            status = "MARGINAL"
        else:
            status = "TENSION"

        return {
            "param": param_name,
            "predicted": predicted,
            "target": target,
            "uncertainty": uncertainty,
            "sigma": sigma,
            "status": status,
            "source": source,
            "units": units,
            "description": f"{param_name}: {predicted:.6g}{units} vs {target:.6g} ± {uncertainty:.6g} ({sigma:.2f}σ)"
        }

    @staticmethod
    def format_formula_step(description: str, formula: str, value: Optional[float] = None) -> Dict[str, str]:
        """
        Generate a derivation step with optional computed value substitution.

        Args:
            description: Text description of the step
            formula: LaTeX formula (can contain {value} placeholder)
            value: Optional computed value to substitute

        Returns:
            Dictionary with description and formula
        """
        if value is not None:
            formula = formula.format(value=value)
        return {
            "description": description,
            "formula": formula
        }


class DynamicFormula:
    """
    Helper class for generating dynamic formula metadata.

    Wraps formula generation to include computed values in descriptions
    and derivation steps.
    """

    def __init__(
        self,
        formula_id: str,
        label: str,
        category: str = "DERIVED"
    ):
        """
        Initialize a dynamic formula builder.

        Args:
            formula_id: Unique identifier for the formula
            label: Display label like "(5.10)"
            category: Formula category (THEORY, DERIVED, PREDICTIONS)
        """
        self.formula_id = formula_id
        self.label = label
        self.category = category
        self._computed_values: Dict[str, float] = {}
        self._latex: Optional[str] = None
        self._plain_text: Optional[str] = None
        self._description: Optional[str] = None
        self._derivation_steps: list = []
        self._terms: Dict[str, str] = {}
        self._input_params: list = []
        self._output_params: list = []

    def set_computed(self, **values: float) -> 'DynamicFormula':
        """
        Set computed values for substitution.

        Args:
            **values: Keyword arguments of computed values

        Returns:
            Self for chaining
        """
        self._computed_values.update(values)
        return self

    def with_latex(self, template: str) -> 'DynamicFormula':
        """
        Set LaTeX template with computed value substitution.

        The template can use {key} placeholders for computed values.

        Args:
            template: LaTeX template string

        Returns:
            Self for chaining
        """
        self._latex = template.format(**self._computed_values)
        return self

    def with_plain_text(self, template: str) -> 'DynamicFormula':
        """
        Set plain text template with computed value substitution.

        Args:
            template: Plain text template string

        Returns:
            Self for chaining
        """
        self._plain_text = template.format(**self._computed_values)
        return self

    def with_description(self, template: str) -> 'DynamicFormula':
        """
        Set description template with computed value substitution.

        Args:
            template: Description template string

        Returns:
            Self for chaining
        """
        self._description = template.format(**self._computed_values)
        return self

    def add_derivation_step(self, description: str, formula_template: str) -> 'DynamicFormula':
        """
        Add a derivation step with value substitution.

        Args:
            description: Step description
            formula_template: LaTeX formula template

        Returns:
            Self for chaining
        """
        self._derivation_steps.append({
            "description": description.format(**self._computed_values),
            "formula": formula_template.format(**self._computed_values)
        })
        return self

    def with_terms(self, terms: Dict[str, str]) -> 'DynamicFormula':
        """
        Set term definitions.

        Args:
            terms: Dictionary mapping symbol to description

        Returns:
            Self for chaining
        """
        self._terms = {
            k: v.format(**self._computed_values) for k, v in terms.items()
        }
        return self

    def with_params(
        self,
        input_params: list,
        output_params: list
    ) -> 'DynamicFormula':
        """
        Set input and output parameter paths.

        Args:
            input_params: List of input parameter paths
            output_params: List of output parameter paths

        Returns:
            Self for chaining
        """
        self._input_params = input_params
        self._output_params = output_params
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build the formula dictionary for use in simulations.

        Returns:
            Dictionary with all formula fields
        """
        return {
            "id": self.formula_id,
            "label": self.label,
            "latex": self._latex,
            "plain_text": self._plain_text,
            "category": self.category,
            "description": self._description,
            "inputParams": self._input_params,
            "outputParams": self._output_params,
            "input_params": self._input_params,
            "output_params": self._output_params,
            "derivation": {
                "steps": self._derivation_steps
            },
            "terms": self._terms
        }


# Convenience functions for common PM values
def w0_from_b3(b3: int = 24) -> Tuple[float, str, str]:
    """
    Compute w0 from b3 with fraction and description.

    Args:
        b3: Number of associative 3-cycles

    Returns:
        Tuple of (value, fraction_str, full_description)
    """
    w0 = -1.0 + (1.0 / b3)
    numerator = b3 - 1
    frac_str = f"-{numerator}/{b3}"
    desc = f"w₀ = -1 + 1/b₃ = {frac_str} = {w0:.6f}"
    return w0, frac_str, desc


def wa_from_b3(b3: int = 24) -> Tuple[float, str]:
    """
    Compute wa from b3 with description.

    Args:
        b3: Number of associative 3-cycles

    Returns:
        Tuple of (value, description)
    """
    wa = -1.0 / np.sqrt(b3)
    desc = f"w_a = -1/√b₃ = -1/√{b3} = {wa:.6f}"
    return wa, desc


def delta_cp_with_parity(n_gen: int, b2: int, b3: int, parity_offset: float = 45.9) -> Tuple[float, str]:
    """
    Compute delta_CP with 13D parity offset.

    Args:
        n_gen: Number of fermion generations
        b2: Kahler moduli
        b3: Associative 3-cycles
        parity_offset: Parity offset in degrees

    Returns:
        Tuple of (value_degrees, description)
    """
    lepton_phase = (n_gen + b2) / (2 * n_gen)
    topology_phase = n_gen / b3
    phase_factor = lepton_phase + topology_phase

    delta_cp_bare = np.degrees(np.pi * phase_factor)
    delta_cp = (delta_cp_bare + parity_offset) % 360

    desc = (
        f"δ_CP = π×({n_gen}+{b2})/(2×{n_gen}) + π×{n_gen}/{b3} + {parity_offset}° = "
        f"{delta_cp_bare:.1f}° + {parity_offset}° = {delta_cp:.1f}°"
    )
    return delta_cp, desc


# Export all public symbols
__all__ = [
    'MetadataBuilder',
    'DynamicFormula',
    'w0_from_b3',
    'wa_from_b3',
    'delta_cp_with_parity',
]
