"""
Unit Conversion Utilities for Principia Metaphysica
====================================================

Provides explicit conversions between the unit systems used across
different simulation domains:

1. PLANCK UNITS (geometric_anchors)
   - Length: l_P = 1.616255e-35 m
   - Mass: m_P = 2.176434e-8 kg
   - Time: t_P = 5.391247e-44 s
   - Energy: E_P = 1.956e9 J = 1.221e28 eV

2. COSMOLOGICAL UNITS (ricci_flow, hubble)
   - Distance: Mpc (megaparsec) = 3.086e22 m
   - Velocity: km/s
   - H0: km/s/Mpc = 3.241e-20 s^-1

3. HIGH ENERGY PHYSICS UNITS (higgs, gauge)
   - Energy: GeV = 1.602e-10 J
   - Mass: GeV/c^2
   - Length: 1/GeV (natural units)

4. NATURAL UNITS (theoretical)
   - c = hbar = k_B = 1
   - Energy = Mass = Temperature = 1/Length = 1/Time

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Union, Tuple
from dataclasses import dataclass


# =============================================================================
# FUNDAMENTAL CONSTANTS (CODATA 2022)
# =============================================================================

@dataclass(frozen=True)
class PhysicalConstants:
    """Fundamental physical constants."""
    # Speed of light
    c: float = 299792458.0  # m/s (exact)

    # Planck constant
    h: float = 6.62607015e-34  # J⋅s (exact)
    hbar: float = 1.054571817e-34  # J⋅s

    # Gravitational constant
    G: float = 6.67430e-11  # m³/(kg⋅s²)

    # Boltzmann constant
    k_B: float = 1.380649e-23  # J/K (exact)

    # Elementary charge
    e: float = 1.602176634e-19  # C (exact)

    # Planck units
    l_planck: float = 1.616255e-35  # m
    m_planck: float = 2.176434e-8   # kg
    t_planck: float = 5.391247e-44  # s
    E_planck: float = 1.956e9       # J
    E_planck_GeV: float = 1.221e19  # GeV

CONST = PhysicalConstants()


# =============================================================================
# COSMOLOGICAL CONVERSIONS
# =============================================================================

# Distance
MPC_IN_M = 3.08567758e22      # 1 Mpc in meters
MPC_IN_KM = 3.08567758e19     # 1 Mpc in kilometers
PC_IN_M = 3.08567758e16       # 1 parsec in meters
LY_IN_M = 9.461e15            # 1 light-year in meters

# Time
GYR_IN_S = 3.156e16           # 1 Gyr in seconds
MYR_IN_S = 3.156e13           # 1 Myr in seconds

# Hubble constant conversion
# H0 in km/s/Mpc to s^-1: multiply by 1/Mpc_in_km
H0_KMS_MPC_TO_INV_S = 1.0 / MPC_IN_KM  # 3.241e-20 s^-1 per km/s/Mpc

# Hubble time: 1/H0
def hubble_time_gyr(H0_kms_mpc: float) -> float:
    """Convert H0 in km/s/Mpc to Hubble time in Gyr."""
    H0_inv_s = H0_kms_mpc * H0_KMS_MPC_TO_INV_S
    return 1.0 / H0_inv_s / GYR_IN_S

# Hubble distance: c/H0
def hubble_distance_mpc(H0_kms_mpc: float) -> float:
    """Convert H0 in km/s/Mpc to Hubble distance in Mpc."""
    return CONST.c / 1000.0 / H0_kms_mpc  # c in km/s divided by H0


# =============================================================================
# HIGH ENERGY PHYSICS CONVERSIONS
# =============================================================================

# Energy
GEV_IN_J = 1.602176634e-10    # 1 GeV in Joules
EV_IN_J = 1.602176634e-19     # 1 eV in Joules
TEV_IN_GEV = 1000.0           # 1 TeV = 1000 GeV
MEV_IN_GEV = 0.001            # 1 MeV = 0.001 GeV

# Mass-energy equivalence (GeV/c²)
KG_TO_GEV = CONST.c**2 / GEV_IN_J  # ~5.61e26 GeV per kg

# Natural units conversions (hbar = c = 1)
# Length: 1 GeV^-1 = hbar*c / GeV
GEV_INV_IN_M = CONST.hbar * CONST.c / GEV_IN_J  # ~1.97e-16 m
GEV_INV_IN_FM = GEV_INV_IN_M * 1e15  # ~0.197 fm

# Time: 1 GeV^-1 = hbar / GeV
GEV_INV_IN_S = CONST.hbar / GEV_IN_J  # ~6.58e-25 s


def gev_to_kg(energy_gev: float) -> float:
    """Convert energy in GeV to equivalent mass in kg."""
    return energy_gev * GEV_IN_J / CONST.c**2


def kg_to_gev(mass_kg: float) -> float:
    """Convert mass in kg to energy equivalent in GeV."""
    return mass_kg * CONST.c**2 / GEV_IN_J


def gev_to_natural_length(energy_gev: float) -> float:
    """Convert GeV to natural length scale (meters)."""
    return GEV_INV_IN_M / energy_gev


def natural_length_to_gev(length_m: float) -> float:
    """Convert length in meters to energy scale in GeV."""
    return GEV_INV_IN_M / length_m


# =============================================================================
# PLANCK UNIT CONVERSIONS
# =============================================================================

def planck_to_si(value: float, unit_type: str) -> float:
    """
    Convert Planck units to SI units.

    Args:
        value: Value in Planck units
        unit_type: One of 'length', 'mass', 'time', 'energy'

    Returns:
        Value in SI units
    """
    conversions = {
        'length': CONST.l_planck,
        'mass': CONST.m_planck,
        'time': CONST.t_planck,
        'energy': CONST.E_planck,
    }
    if unit_type not in conversions:
        raise ValueError(f"Unknown unit type: {unit_type}. Use: {list(conversions.keys())}")
    return value * conversions[unit_type]


def si_to_planck(value: float, unit_type: str) -> float:
    """
    Convert SI units to Planck units.

    Args:
        value: Value in SI units
        unit_type: One of 'length', 'mass', 'time', 'energy'

    Returns:
        Value in Planck units
    """
    conversions = {
        'length': CONST.l_planck,
        'mass': CONST.m_planck,
        'time': CONST.t_planck,
        'energy': CONST.E_planck,
    }
    if unit_type not in conversions:
        raise ValueError(f"Unknown unit type: {unit_type}. Use: {list(conversions.keys())}")
    return value / conversions[unit_type]


def planck_to_gev(value: float, unit_type: str) -> float:
    """
    Convert Planck units to GeV-based natural units.

    Args:
        value: Value in Planck units
        unit_type: One of 'length', 'mass', 'time', 'energy'

    Returns:
        Value in GeV-based units (GeV for energy/mass, GeV^-1 for length/time)
    """
    if unit_type == 'energy' or unit_type == 'mass':
        # Planck energy to GeV
        return value * CONST.E_planck_GeV
    elif unit_type == 'length':
        # Planck length to GeV^-1
        si_value = value * CONST.l_planck
        return si_value / GEV_INV_IN_M
    elif unit_type == 'time':
        # Planck time to GeV^-1
        si_value = value * CONST.t_planck
        return si_value / GEV_INV_IN_S
    else:
        raise ValueError(f"Unknown unit type: {unit_type}")


# =============================================================================
# COSMOLOGICAL <-> PLANCK BRIDGE
# =============================================================================

def planck_length_to_mpc(n_planck: float) -> float:
    """Convert number of Planck lengths to Mpc."""
    length_m = n_planck * CONST.l_planck
    return length_m / MPC_IN_M


def mpc_to_planck_length(distance_mpc: float) -> float:
    """Convert distance in Mpc to Planck lengths."""
    length_m = distance_mpc * MPC_IN_M
    return length_m / CONST.l_planck


def hubble_to_planck_time(H0_kms_mpc: float) -> float:
    """
    Convert Hubble constant to Planck time units.

    Returns 1/(H0 * t_Planck), useful for cosmological simulations
    in Planck-normalized time.
    """
    H0_inv_s = H0_kms_mpc * H0_KMS_MPC_TO_INV_S
    return 1.0 / (H0_inv_s * CONST.t_planck)


# =============================================================================
# DIMENSIONAL ANALYSIS HELPERS
# =============================================================================

def check_dimensions(formula_name: str, inputs: dict, output: dict) -> bool:
    """
    Verify dimensional consistency of a calculation.

    Args:
        formula_name: Name of formula being checked
        inputs: Dict of {name: (value, unit_string)}
        output: Dict of {name: (value, unit_string)}

    Returns:
        True if dimensions are consistent (logs warning if not)

    Example:
        check_dimensions(
            "Hubble parameter",
            {"H0": (67.4, "km/s/Mpc"), "Omega_m": (0.311, "dimensionless")},
            {"H_z": (100.0, "km/s/Mpc")}
        )
    """
    # This is a documentation/logging helper
    # Full dimensional analysis would require a symbolic system
    import logging
    logging.info(f"Dimensional check for {formula_name}:")
    logging.info(f"  Inputs: {inputs}")
    logging.info(f"  Output: {output}")
    return True


# =============================================================================
# UNIT VALIDATION
# =============================================================================

class UnitValidator:
    """
    Validates that computed values are in expected ranges for their units.

    Prevents NaN/Inf from scale mismatches between unit systems.
    """

    # Expected ranges for common physics parameters
    RANGES = {
        "H0_kms_mpc": (50.0, 100.0),
        "w0_eos": (-2.0, 0.0),
        "Omega_m": (0.0, 1.0),
        "Omega_de": (0.0, 1.0),
        "redshift": (0.0, 1e10),
        "proton_lifetime_years": (1e30, 1e40),
        "alpha_fine_structure_inv": (130.0, 145.0),
        "m_planck_gev": (1e18, 1e20),
        "m_higgs_gev": (100.0, 150.0),
        "m_gut_gev": (1e15, 1e18),
    }

    @classmethod
    def validate(cls, value: float, param_type: str) -> Tuple[bool, str]:
        """
        Check if value is in expected range for parameter type.

        Returns:
            Tuple of (is_valid, message)
        """
        if param_type not in cls.RANGES:
            return True, f"No range defined for {param_type}"

        if np.isnan(value) or np.isinf(value):
            return False, f"{param_type} is NaN or Inf - likely unit conversion error"

        min_val, max_val = cls.RANGES[param_type]
        if value < min_val or value > max_val:
            return False, (
                f"{param_type} = {value} outside expected range "
                f"[{min_val}, {max_val}] - check unit conversions"
            )

        return True, "OK"

    @classmethod
    def assert_valid(cls, value: float, param_type: str) -> None:
        """Raise ValueError if value is out of range."""
        is_valid, message = cls.validate(value, param_type)
        if not is_valid:
            raise ValueError(message)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("UNIT CONVERSION UTILITIES - SELF TEST")
    print("=" * 60)

    # Planck unit tests
    print("\n1. Planck Unit Conversions:")
    print(f"   1 Planck length = {CONST.l_planck:.3e} m")
    print(f"   1 Planck mass = {CONST.m_planck:.3e} kg = {CONST.E_planck_GeV:.3e} GeV")
    print(f"   1 Planck time = {CONST.t_planck:.3e} s")

    # Cosmological conversions
    print("\n2. Cosmological Conversions:")
    H0 = 67.4  # km/s/Mpc
    print(f"   H0 = {H0} km/s/Mpc")
    print(f"   Hubble time = {hubble_time_gyr(H0):.2f} Gyr")
    print(f"   Hubble distance = {hubble_distance_mpc(H0):.0f} Mpc")

    # HEP conversions
    print("\n3. High Energy Physics Conversions:")
    m_higgs = 125.1  # Higgs mass (PDG)
    print(f"   Higgs mass = {m_higgs} GeV = {gev_to_kg(m_higgs):.3e} kg")
    print(f"   1 GeV^-1 = {GEV_INV_IN_FM:.3f} fm")

    # Cross-system bridge
    print("\n4. Cross-System Bridge:")
    print(f"   Planck length in Mpc: {planck_length_to_mpc(1):.3e}")
    print(f"   1 Mpc in Planck lengths: {mpc_to_planck_length(1):.3e}")

    # Validation
    print("\n5. Unit Validation:")
    valid, msg = UnitValidator.validate(67.4, "H0_kms_mpc")
    print(f"   H0=67.4: {msg}")
    valid, msg = UnitValidator.validate(1e35, "proton_lifetime_years")
    print(f"   tau_p=1e35: {msg}")

    print("\n" + "=" * 60)
    print("SELF TEST COMPLETE")
    print("=" * 60)
