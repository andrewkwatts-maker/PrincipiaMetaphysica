#!/usr/bin/env python3
"""
Example usage of ParameterCategory standardization framework.

This demonstrates how to use the new ParameterCategory class to categorize
parameters throughout the Principia Metaphysica codebase.
"""

from config import ParameterCategory, FittedParameters

# Example 1: Using ParameterCategory for new parameter classes
class ExampleParameters:
    """Example showing how to use ParameterCategory in new parameter classes."""

    # Geometric parameters (pure topology)
    CHI_EFF = 144
    CATEGORY_CHI_EFF = ParameterCategory.GEOMETRIC

    # Derived parameters (computed from geometry)
    M_GUT = 2.118e16  # GeV
    CATEGORY_M_GUT = ParameterCategory.DERIVED

    # Phenomenological parameters (measured inputs)
    M_PLANCK = 2.435e18  # GeV
    CATEGORY_M_PLANCK = ParameterCategory.PHENOMENOLOGICAL

    # Predicted parameters (testable predictions)
    M_KK = 5000  # GeV
    CATEGORY_M_KK = ParameterCategory.PREDICTED

# Example 2: Checking parameter categories
print("Parameter Category Framework")
print("=" * 60)
print()
print("Available Categories:")
print(f"  - {ParameterCategory.GEOMETRIC}: Pure topology (chi_eff, b2, b3, n_gen)")
print(f"  - {ParameterCategory.DERIVED}: Computed from geometry (M_GUT, tau_p, alpha_GUT)")
print(f"  - {ParameterCategory.PHENOMENOLOGICAL}: Measured inputs (M_Planck, m_H)")
print(f"  - {ParameterCategory.CALIBRATED}: Fitted to data (theta_13, delta_CP)")
print(f"  - {ParameterCategory.PREDICTED}: Testable predictions (M_KK, GW)")
print(f"  - {ParameterCategory.EXPERIMENTAL}: PDG/NuFIT reference values")
print()

# Example 3: Current category distribution
print("Current FittedParameters Category Distribution:")
print("-" * 60)
counts = FittedParameters.get_category_counts()
total = sum(counts.values())

for category, count in counts.items():
    percentage = (count / total * 100) if total > 0 else 0
    print(f"  {category:20s}: {count:3d} ({percentage:5.1f}%)")

print(f"  {'TOTAL':20s}: {total:3d}")
print()
print("Note: As parameters are categorized, this distribution will evolve.")
print("      The goal is to categorize all 200+ parameters in config.py.")
