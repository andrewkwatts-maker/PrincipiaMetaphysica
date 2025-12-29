#!/usr/bin/env python3
"""
Test script for covariance matrix data validation.

Verifies that the covariance matrices in nufit_6_0_covariance.json are:
1. Properly formatted
2. Mathematically valid (symmetric, positive definite)
3. Consistent (covariance = correlation * sigma_i * sigma_j)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import numpy as np
from pathlib import Path


def test_covariance_data():
    """Test the covariance data file."""

    data_file = Path(__file__).parent.parent.parent / "data" / "experimental" / "nufit_6_0_covariance.json"

    print("=" * 75)
    print("COVARIANCE DATA VALIDATION TEST")
    print("=" * 75)
    print(f"\nData file: {data_file}")

    # Load data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"[OK] File loaded successfully")

    # Test Normal Ordering neutrino data
    print("\n--- Testing Normal Ordering Neutrino Data ---")
    no_data = data["normal_ordering"]
    test_sector(no_data, "Neutrino (NO)")

    # Test Inverted Ordering neutrino data
    print("\n--- Testing Inverted Ordering Neutrino Data ---")
    io_data = data["inverted_ordering"]
    test_sector(io_data, "Neutrino (IO)")

    # Test cosmology data
    print("\n--- Testing Cosmology Data ---")
    cosmo_data = data["cosmological_parameters"]
    test_sector(cosmo_data, "Cosmology")

    print("\n" + "=" * 75)
    print("ALL TESTS PASSED [OK]")
    print("=" * 75)


def test_sector(sector_data, sector_name):
    """Test a single sector's covariance data."""

    params = sector_data["parameters"]
    corr_data = sector_data["correlation_matrix"]
    cov_data = sector_data["covariance_matrix"]

    param_order = corr_data["parameters_order"]
    n = len(param_order)

    # Extract matrices
    corr_matrix = np.array(corr_data["matrix"])
    cov_matrix = np.array(cov_data["matrix"])

    # Extract uncertainties
    uncertainties = np.array([params[p]["uncertainty"] for p in param_order])

    print(f"\n{sector_name}:")
    print(f"  Parameters: {', '.join(param_order)}")
    print(f"  Dimension: {n}×{n}")

    # Test 1: Matrix shapes
    assert corr_matrix.shape == (n, n), f"Correlation matrix wrong shape: {corr_matrix.shape}"
    assert cov_matrix.shape == (n, n), f"Covariance matrix wrong shape: {cov_matrix.shape}"
    print(f"  [OK] Matrix shapes correct")

    # Test 2: Correlation matrix symmetry
    assert np.allclose(corr_matrix, corr_matrix.T), "Correlation matrix not symmetric"
    print(f"  [OK] Correlation matrix symmetric")

    # Test 3: Correlation diagonal = 1
    assert np.allclose(np.diag(corr_matrix), 1.0), "Correlation diagonal not 1.0"
    print(f"  [OK] Correlation diagonal = 1.0")

    # Test 4: Correlation bounds [-1, 1]
    assert np.all(corr_matrix >= -1.0) and np.all(corr_matrix <= 1.0), "Correlation out of bounds"
    print(f"  [OK] Correlation coefficients in [-1, 1]")

    # Test 5: Covariance matrix symmetry
    assert np.allclose(cov_matrix, cov_matrix.T), "Covariance matrix not symmetric"
    print(f"  [OK] Covariance matrix symmetric")

    # Test 6: Covariance positive definite (all eigenvalues > 0)
    eigvals = np.linalg.eigvalsh(cov_matrix)
    min_eigval = np.min(eigvals)
    assert min_eigval > 0, f"Covariance not positive definite: min eigenvalue = {min_eigval}"
    print(f"  [OK] Covariance positive definite (min eigenvalue = {min_eigval:.2e})")

    # Test 7: Consistency: Cov[i,j] = rho[i,j] * sigma[i] * sigma[j]
    reconstructed_cov = np.outer(uncertainties, uncertainties) * corr_matrix
    max_diff = np.max(np.abs(cov_matrix - reconstructed_cov))
    assert np.allclose(cov_matrix, reconstructed_cov, rtol=1e-3), \
        f"Covariance inconsistent with correlation: max diff = {max_diff}"
    print(f"  [OK] Covariance consistent with correlation (max diff = {max_diff:.2e})")

    # Test 8: Diagonal of covariance = variance
    expected_diag = uncertainties ** 2
    actual_diag = np.diag(cov_matrix)
    assert np.allclose(actual_diag, expected_diag, rtol=1e-3), \
        "Covariance diagonal not equal to variances"
    print(f"  [OK] Covariance diagonal = sigma^2")

    # Print correlation summary
    print(f"\n  Correlation summary:")
    for i in range(n):
        for j in range(i + 1, n):
            rho = corr_matrix[i, j]
            if abs(rho) > 0.05:  # Print significant correlations
                print(f"    rho({param_order[i]}, {param_order[j]}) = {rho:+.3f}")

    # Print eigenvalue spectrum
    print(f"\n  Eigenvalue spectrum:")
    for i, eigval in enumerate(sorted(eigvals)):
        print(f"    lambda_{i+1} = {eigval:.6f}")


if __name__ == "__main__":
    test_covariance_data()
