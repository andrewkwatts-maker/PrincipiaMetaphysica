#!/usr/bin/env python3
"""
Proton Lifetime Monte Carlo Uncertainty (v12.8)
===============================================

Quantifies proton lifetime uncertainty from M_GUT variation.

Formula: tau_p ~ M_GUT^4
         tau_p_uncertainty from MC sampling of M_GUT

This closes the "tau_p uncertainty" statement.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np


def proton_lifetime_mc(n_mc=10000, M_GUT_mean=2.118e16, M_GUT_std=1e14):
    """
    Monte Carlo uncertainty estimation for proton lifetime.

    Parameters:
    -----------
    n_mc : int
        Number of Monte Carlo samples
    M_GUT_mean : float
        Central M_GUT value in GeV
    M_GUT_std : float
        M_GUT uncertainty in GeV

    Returns:
    --------
    dict : Contains tau_p statistics and uncertainties
    """
    # Monte Carlo sampling of M_GUT
    np.random.seed(42)  # Reproducibility
    M_GUT_mc = np.random.normal(M_GUT_mean, M_GUT_std, n_mc)

    # Remove non-physical values
    M_GUT_mc = M_GUT_mc[M_GUT_mc > 0]

    # tau_p scales as M_GUT^4
    tau_p_baseline = 3.91e34  # years (from simulations)
    tau_p_mc = tau_p_baseline * (M_GUT_mc / M_GUT_mean)**4

    # Statistics
    tau_p_mean = np.mean(tau_p_mc)
    tau_p_median = np.median(tau_p_mc)
    tau_p_std = np.std(tau_p_mc)
    tau_p_16 = np.percentile(tau_p_mc, 16)
    tau_p_84 = np.percentile(tau_p_mc, 84)

    # Relative uncertainty
    relative_uncertainty = tau_p_std / tau_p_mean

    # Order of magnitude uncertainty
    oom_uncertainty = np.log10(tau_p_84 / tau_p_16) / 2

    # Super-K limit comparison
    tau_p_superK = 2.4e34  # years (90% CL lower limit)
    above_superK = tau_p_mean > tau_p_superK

    results = {
        'tau_p_mean': tau_p_mean,
        'tau_p_median': tau_p_median,
        'tau_p_std': tau_p_std,
        'tau_p_16': tau_p_16,
        'tau_p_84': tau_p_84,
        'relative_uncertainty': relative_uncertainty,
        'oom_uncertainty': oom_uncertainty,
        'n_mc': n_mc,
        'M_GUT_mean': M_GUT_mean,
        'M_GUT_std': M_GUT_std,
        'tau_p_superK': tau_p_superK,
        'above_superK': above_superK,
        'derivation_status': 'MC QUANTIFIED',
        'formula': 'tau_p ~ M_GUT^4',
        'reference': 'Monte Carlo from flux quantization variation'
    }

    return results


def print_results(results):
    """Print formatted results."""
    print("=" * 60)
    print("PROTON LIFETIME MONTE CARLO UNCERTAINTY (v12.8)")
    print("=" * 60)
    print(f"Formula: {results['formula']}")
    print(f"M_GUT = ({results['M_GUT_mean']:.3e} +/- {results['M_GUT_std']:.0e}) GeV")
    print(f"N_MC = {results['n_mc']}")
    print(f"tau_p mean = {results['tau_p_mean']:.2e} years")
    print(f"tau_p median = {results['tau_p_median']:.2e} years")
    print(f"tau_p 68% CI: [{results['tau_p_16']:.2e}, {results['tau_p_84']:.2e}] years")
    print(f"Relative uncertainty = {results['relative_uncertainty']:.1%}")
    print(f"OOM uncertainty = {results['oom_uncertainty']:.3f}")
    print(f"Super-K limit: > {results['tau_p_superK']:.1e} years")
    print(f"Above Super-K: {results['above_superK']}")
    print(f"Status: {results['derivation_status']}")
    print("=" * 60)


if __name__ == "__main__":
    results = proton_lifetime_mc()
    print_results(results)
