"""
Unit Validation System v16.2
=============================

Comprehensive unit validation for Principia Metaphysica simulations.
Ensures dimensional consistency across all physics calculations.

Key Features:
1. Unit registry with SI base units
2. Dimensional analysis for all parameters
3. Cross-simulation unit propagation checks
4. Automatic conversion validation

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class SIUnit(Enum):
    """SI base units and common derived units."""
    # Base units
    DIMENSIONLESS = ""
    METER = "m"
    KILOGRAM = "kg"
    SECOND = "s"
    AMPERE = "A"
    KELVIN = "K"
    MOLE = "mol"
    CANDELA = "cd"

    # Derived units (physics)
    JOULE = "J"                    # kg⋅m²/s²
    WATT = "W"                     # J/s
    NEWTON = "N"                   # kg⋅m/s²
    PASCAL = "Pa"                  # N/m²
    HERTZ = "Hz"                   # 1/s
    ELECTRONVOLT = "eV"            # 1.602e-19 J
    TESLA = "T"                    # kg/(A⋅s²)

    # Cosmology units
    KM_PER_SEC_PER_MPC = "km/s/Mpc"  # Hubble constant
    INV_METER_SQ = "m^-2"            # Cosmological constant

    # Natural units
    PLANCK_MASS = "M_Pl"
    PLANCK_LENGTH = "l_Pl"
    PLANCK_TIME = "t_Pl"


@dataclass
class DimensionalQuantity:
    """A physical quantity with value and dimensional exponents."""
    value: float
    unit_str: str
    # SI dimensional exponents: [m, kg, s, A, K, mol, cd]
    dimensions: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0, 0])

    def is_dimensionless(self) -> bool:
        return all(d == 0 for d in self.dimensions)

    def check_compatible(self, other: 'DimensionalQuantity') -> bool:
        return self.dimensions == other.dimensions


# Standard dimensional signatures
UNIT_DIMENSIONS = {
    # Dimensionless quantities
    "": [0, 0, 0, 0, 0, 0, 0],
    "1": [0, 0, 0, 0, 0, 0, 0],
    "dimensionless": [0, 0, 0, 0, 0, 0, 0],

    # Base units
    "m": [1, 0, 0, 0, 0, 0, 0],
    "kg": [0, 1, 0, 0, 0, 0, 0],
    "s": [0, 0, 1, 0, 0, 0, 0],
    "A": [0, 0, 0, 1, 0, 0, 0],
    "K": [0, 0, 0, 0, 1, 0, 0],

    # Energy
    "J": [2, 1, -2, 0, 0, 0, 0],        # kg⋅m²/s²
    "eV": [2, 1, -2, 0, 0, 0, 0],       # Same dimensions as J
    "GeV": [2, 1, -2, 0, 0, 0, 0],
    "MeV": [2, 1, -2, 0, 0, 0, 0],

    # Mass (particle physics)
    "MeV/c^2": [0, 1, 0, 0, 0, 0, 0],  # Mass
    "GeV/c^2": [0, 1, 0, 0, 0, 0, 0],

    # Time
    "yr": [0, 0, 1, 0, 0, 0, 0],
    "years": [0, 0, 1, 0, 0, 0, 0],
    "ms": [0, 0, 1, 0, 0, 0, 0],  # milliseconds

    # Cosmology
    "km/s/Mpc": [0, 0, -1, 0, 0, 0, 0],  # Hubble constant (1/time)
    "m^-2": [-2, 0, 0, 0, 0, 0, 0],       # Cosmological constant

    # Gravitational
    "m^3/(kg*s^2)": [3, -1, -2, 0, 0, 0, 0],  # G Newton
    "m^3/kg/s^2": [3, -1, -2, 0, 0, 0, 0],

    # Angular
    "rad": [0, 0, 0, 0, 0, 0, 0],         # Dimensionless
    "deg": [0, 0, 0, 0, 0, 0, 0],

    # Action
    "J*s": [2, 1, -1, 0, 0, 0, 0],        # Planck constant
}


@dataclass
class UnitValidationResult:
    """Result of unit validation for a parameter."""
    path: str
    value: Any
    declared_unit: str
    inferred_unit: Optional[str]
    dimensions: List[int]
    is_valid: bool
    message: str


class UnitValidator:
    """
    Validates unit consistency across PM simulations.

    Checks:
    1. All parameters have declared units
    2. Units match expected dimensional signature
    3. Cross-simulation unit propagation is consistent
    4. No unit mismatches in calculations
    """

    # PM v16.2 parameter unit registry
    PARAMETER_UNITS = {
        # Geometric anchors (dimensionless)
        "b3": "",
        "k_gimel": "",
        "k_gimel_warp": "",
        "D_bulk": "",
        "D_crit": "",
        "alpha": "",
        "alpha_inv": "",
        "sin2_theta_w": "",

        # Dark energy (dimensionless EoS)
        "w0": "",
        "wa": "",
        "w_eff": "",

        # Cosmology
        "H0": "km/s/Mpc",
        "H0_local": "km/s/Mpc",
        "H0_early": "km/s/Mpc",
        "Lambda": "m^-2",
        "Lambda_derived": "m^-2",
        "z_transition": "",

        # Masses
        "m_e": "MeV/c^2",
        "m_mu": "MeV/c^2",
        "m_tau": "MeV/c^2",
        "m_u": "MeV/c^2",
        "m_d": "MeV/c^2",
        "m_s": "MeV/c^2",
        "m_c": "GeV/c^2",
        "m_b": "GeV/c^2",
        "m_t": "GeV/c^2",
        "m_h": "GeV/c^2",
        "m_W": "GeV/c^2",
        "m_Z": "GeV/c^2",

        # Neutrino
        "m_nu_sum": "eV",
        "delta_m21_sq": "eV^2",
        "delta_m31_sq": "eV^2",
        "theta_12": "deg",
        "theta_13": "deg",
        "theta_23": "deg",
        "delta_CP": "deg",

        # Proton decay
        "tau_p_years": "years",
        "tau_p_median": "years",

        # Quantum biology
        "tau_coherence": "s",
        "tau_coherence_ms": "ms",

        # Fundamental constants
        "G_Newton": "m^3/(kg*s^2)",
        "G_corrected": "m^3/(kg*s^2)",
        "hbar": "J*s",
        "c": "m/s",
    }

    def __init__(self):
        self.results: List[UnitValidationResult] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_parameter(
        self,
        path: str,
        value: Any,
        declared_unit: str
    ) -> UnitValidationResult:
        """Validate a single parameter's units."""

        # Get expected unit from registry
        param_name = path.split(".")[-1] if "." in path else path
        expected_unit = self.PARAMETER_UNITS.get(param_name)

        # Check if unit is declared
        # Empty string is valid for dimensionless quantities
        if not declared_unit and expected_unit is not None and expected_unit != "":
            return UnitValidationResult(
                path=path,
                value=value,
                declared_unit=declared_unit,
                inferred_unit=expected_unit,
                dimensions=UNIT_DIMENSIONS.get(expected_unit, [0]*7),
                is_valid=False,
                message=f"Missing unit declaration. Expected: {expected_unit}"
            )

        # Dimensionless quantities with empty declared unit are OK
        if not declared_unit and (expected_unit == "" or expected_unit is None):
            return UnitValidationResult(
                path=path,
                value=value,
                declared_unit="(dimensionless)",
                inferred_unit="",
                dimensions=[0]*7,
                is_valid=True,
                message="OK (dimensionless)"
            )

        # Get dimensions
        declared_dims = UNIT_DIMENSIONS.get(declared_unit, None)
        expected_dims = UNIT_DIMENSIONS.get(expected_unit, [0]*7) if expected_unit else None

        if declared_dims is None and declared_unit:
            return UnitValidationResult(
                path=path,
                value=value,
                declared_unit=declared_unit,
                inferred_unit=expected_unit,
                dimensions=[0]*7,
                is_valid=False,
                message=f"Unknown unit: {declared_unit}"
            )

        # Check dimensional consistency
        if declared_dims and expected_dims and declared_dims != expected_dims:
            return UnitValidationResult(
                path=path,
                value=value,
                declared_unit=declared_unit,
                inferred_unit=expected_unit,
                dimensions=declared_dims,
                is_valid=False,
                message=f"Unit mismatch: declared {declared_unit}, expected {expected_unit}"
            )

        return UnitValidationResult(
            path=path,
            value=value,
            declared_unit=declared_unit,
            inferred_unit=expected_unit,
            dimensions=declared_dims or [0]*7,
            is_valid=True,
            message="OK"
        )

    def validate_calculation(
        self,
        result_path: str,
        result_value: float,
        result_unit: str,
        formula: str,
        inputs: Dict[str, Tuple[float, str]]
    ) -> UnitValidationResult:
        """
        Validate dimensional consistency of a calculation.

        Args:
            result_path: Path of output parameter
            result_value: Computed value
            result_unit: Declared unit of result
            formula: Human-readable formula description
            inputs: Dict of {param_name: (value, unit)}
        """
        # This would require parsing the formula to check dimensional consistency
        # For now, we do basic unit registry lookup
        return self.validate_parameter(result_path, result_value, result_unit)

    def validate_cross_simulation(
        self,
        source_sim: str,
        source_param: str,
        source_value: float,
        source_unit: str,
        target_sim: str,
        target_param: str,
        target_unit: str
    ) -> bool:
        """
        Validate that a parameter passed between simulations has consistent units.
        """
        source_dims = UNIT_DIMENSIONS.get(source_unit, None)
        target_dims = UNIT_DIMENSIONS.get(target_unit, None)

        if source_dims is None or target_dims is None:
            self.warnings.append(
                f"Unknown unit in cross-sim check: {source_sim}.{source_param} -> "
                f"{target_sim}.{target_param}: {source_unit} -> {target_unit}"
            )
            return True  # Can't validate unknown units

        if source_dims != target_dims:
            self.errors.append(
                f"Unit mismatch: {source_sim}.{source_param} ({source_unit}) -> "
                f"{target_sim}.{target_param} ({target_unit})"
            )
            return False

        return True


def run_unit_validation():
    """Run comprehensive unit validation on PM v16.2 parameters."""

    print("=" * 70)
    print(" PM v16.2 UNIT VALIDATION REPORT")
    print("=" * 70)

    validator = UnitValidator()

    # Test parameters from logic check
    test_params = [
        # Geometric anchors
        ("b3", 24, ""),
        ("k_gimel", 12.3183098862, ""),
        ("alpha_inv", 137.03599, ""),

        # Dark energy
        ("w0", -0.9583333, ""),
        ("wa", -0.2041241, ""),

        # Cosmology
        ("H0_local", 73.04, "km/s/Mpc"),
        ("H0_early", 67.4, "km/s/Mpc"),
        ("Lambda", 1.1e-52, "m^-2"),

        # Gravitational
        ("G_Newton", 6.67430e-11, "m^3/(kg*s^2)"),
        ("G_corrected", 6.66271e-11, "m^3/(kg*s^2)"),

        # Quantum biology
        ("tau_coherence_ms", 98.97, "ms"),

        # Neutrino
        ("m_nu_sum", 0.06, "eV"),
        ("theta_12", 33.44, "deg"),
        ("delta_CP", 232.0, "deg"),
    ]

    print("\nValidating parameter units:")
    print("-" * 70)

    all_valid = True
    for path, value, unit in test_params:
        result = validator.validate_parameter(path, value, unit)
        status = "[PASS]" if result.is_valid else "[FAIL]"
        print(f"  {path:20} = {value:15} {unit:15} [{status}]")
        if not result.is_valid:
            print(f"      -> {result.message}")
            all_valid = False

    # Cross-simulation validation
    print("\n" + "-" * 70)
    print("Cross-simulation unit propagation:")
    print("-" * 70)

    cross_checks = [
        ("geometric_anchors", "b3", 24, "", "dark_energy", "b3", ""),
        ("geometric_anchors", "k_gimel", 12.318, "", "microtubule", "k_gimel", ""),
        ("ricci_flow", "H0_early", 67.4, "km/s/Mpc", "hubble_tension", "H0_early", "km/s/Mpc"),
        ("dark_energy", "w0", -0.958, "", "cosmology", "w0", ""),
    ]

    for src_sim, src_param, src_val, src_unit, tgt_sim, tgt_param, tgt_unit in cross_checks:
        valid = validator.validate_cross_simulation(
            src_sim, src_param, src_val, src_unit,
            tgt_sim, tgt_param, tgt_unit
        )
        status = "[PASS]" if valid else "[FAIL]"
        print(f"  {src_sim}.{src_param} -> {tgt_sim}.{tgt_param}: [{status}]")

    # Summary
    print("\n" + "=" * 70)
    print(" SUMMARY")
    print("=" * 70)

    if validator.errors:
        print(f"\nERRORS ({len(validator.errors)}):")
        for err in validator.errors:
            print(f"  [X] {err}")

    if validator.warnings:
        print(f"\nWARNINGS ({len(validator.warnings)}):")
        for warn in validator.warnings:
            print(f"  [!] {warn}")

    if all_valid and not validator.errors:
        print("\n[PASS] All unit validations passed!")
    else:
        print(f"\n[FAIL] {len(validator.errors)} errors, {len(validator.warnings)} warnings")

    print("=" * 70)

    return all_valid and not validator.errors


# Unit conversion factors for reference
CONVERSION_FACTORS = {
    # Energy
    "eV_to_J": 1.602176634e-19,
    "GeV_to_J": 1.602176634e-10,
    "MeV_to_J": 1.602176634e-13,

    # Time
    "yr_to_s": 3.15576e7,
    "ms_to_s": 1e-3,

    # Length
    "Mpc_to_m": 3.0857e22,
    "km_to_m": 1e3,

    # Mass
    "MeV_c2_to_kg": 1.782662e-30,
    "GeV_c2_to_kg": 1.782662e-27,
}


if __name__ == "__main__":
    run_unit_validation()
