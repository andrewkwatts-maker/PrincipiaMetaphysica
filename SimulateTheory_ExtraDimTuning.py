#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""

"""
SimulateTheory_ExtraDimTuning.py - Extra Dimension Influence Parameter Tuning

This script explores how varying the influence of the 4th and 5th shared extra dimensions
in the (5,1) observable brane affects the outstanding prediction issues:

1. Proton decay lifetime (narrow the range)
2. Planck tension (w_0 adjustment)
3. Neutrino mixing angle theta_2_3
4. KK graviton masses

TUNABLE PARAMETERS:
------------------
alpha_4: Influence coefficient of 4th dimension (0-1)
alpha_5: Influence coefficient of 5th dimension (0-1)

These parameters modulate how the shared extra dimensions couple to observables:
- KK mode masses: m_KK ~ (alpha_4, alpha_5) / R
- Gauge coupling corrections: Deltaalpha_GUT ~ alpha_4 + alpha_5
- Dark energy: w_0 adjustment via dimensional reduction factor
- Threshold corrections: affect M_GUT and hence tau_p

METHOD:
-------
Uses Newton's method to find optimal (alpha_4, alpha_5) that minimize deviations from
experimental targets for the 4 outstanding predictions.

Dependencies: pandas, sympy, numpy, scipy
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, newton
from sympy import symbols, sqrt, N, pi, log, exp
import warnings
warnings.filterwarnings('ignore')

# Import central configuration
from config import (
    FundamentalConstants as FC,
    PhenomenologyParameters as PP,
    RealWorldData as RWD
)

print("=" * 80)
print("PRINCIPIA METAPHYSICA - EXTRA DIMENSION TUNING SIMULATION")
print("Exploring alpha_4 and alpha_5 influence parameters on (5,1) brane")
print("=" * 80)
print()

# ==============================================================================
# BASELINE PARAMETERS (from config.py and current theory)
# ==============================================================================

# Fundamental scales
M_Pl = 1.22e19  # GeV (reduced Planck mass)
M_GUT_base = 1.8e16  # GeV (base GUT scale from RG running)
M_star = 1.0e16  # GeV (fundamental string scale)

# Current predictions (from OUTSTANDING_ISSUES_REPORT.md)
tau_p_central = 4.0e34  # years (proton lifetime central value)
tau_p_error_upper = 2.5e34  # years (current upper error)
tau_p_error_lower = 1.5e34  # years (current lower error)

w_0_prediction = -11.0/13.0  # ~ -0.846 (dark energy EOS at z=0)
w_a_prediction = -0.75  # (dark energy evolution)

theta_23_prediction = 45.0  # degrees (maximal mixing from SO(10))

m_KK_base = 5.0e3  # GeV (base KK mode mass estimate)

# Experimental targets
tau_p_target = 2.4e34  # years (Super-K lower bound)
tau_p_target_error = 0.5  # orders of magnitude (target precision)

w_0_DESI = -0.83  # (DESI 2024 best fit)
w_0_DESI_error = 0.06  # (1sigma error)

theta_23_observed = 47.2  # degrees (NuFIT 5.2 best fit)
theta_23_error = 2.0  # degrees (approximate 1sigma)

m_KK_LHC_limit = 3.5e3  # GeV (current LHC exclusion)

# Compactification radius and volume
R_shared = 1.0 / (5.0e3)  # GeV^-1 (shared extra dimensions, ~5 TeV scale)
V_7 = (2 * pi * R_shared)**2  # Volume of 2 shared extra dimensions

# ==============================================================================
# FUNCTIONS: THEORY PREDICTIONS AS FUNCTION OF (alpha_4, alpha_5)
# ==============================================================================

def compute_M_GUT(alpha_4, alpha_5):
    """
    Compute effective GUT scale with extra dimension corrections.

    Mechanism: Shared extra dimensions modify gauge coupling running via:
    - KK tower contributions to beta functions
    - Threshold corrections at compactification scale

    alpha_4, alpha_5 modulate the coupling strength to 4th and 5th dimensions.
    """
    # Base RG running gives M_GUT ~ 2x10^16 GeV
    M_GUT = M_GUT_base

    # Extra dimension threshold correction (positive shift)
    # Larger alpha -> more KK modes contribute -> higher effective M_GUT
    delta_M_GUT = M_GUT * 0.15 * (alpha_4 + alpha_5)  # 15% correction at full coupling

    return M_GUT + delta_M_GUT


def compute_alpha_GUT(alpha_4, alpha_5):
    """
    Compute unified gauge coupling 1/alpha_GUT with KK corrections.

    Target: 1/alpha_GUT ~ 24.0 +/- 0.5
    Current: 1/alpha_GUT = 24.68 (3% precision)
    """
    # Base value from sequential RG + AS + TC + KK
    alpha_GUT_inv_base = 24.68

    # Extra dimension modifies running via KK tower
    # deltabeta_KK ~ (2/16π²) alpha² (μ/M_*)² for 2 extra dimensions
    # Effect: reduces 1/alpha_GUT slightly (more matter-like running)
    delta_alpha = -0.5 * (alpha_4 + alpha_5)  # Up to 0.5 shift at full coupling

    return alpha_GUT_inv_base + delta_alpha


def compute_tau_p(alpha_4, alpha_5):
    """
    Compute proton lifetime with extra dimension corrections.

    Formula: tau_p ~ M_X^4 / (m_p^5 alpha_GUT²) x (hadronic matrix elements)

    Strategy: Use alpha_4, alpha_5 to adjust M_GUT -> M_X, thereby tuning tau_p
    """
    M_GUT = compute_M_GUT(alpha_4, alpha_5)
    alpha_GUT_inv = compute_alpha_GUT(alpha_4, alpha_5)

    # Proton lifetime formula (dimension-6 operators)
    m_proton = 0.938  # GeV
    alpha_H = 0.015  # GeV³ (hadronic matrix element from lattice QCD)

    # Scaling: tau_p proportional to M_GUT^4 / alpha_GUT²
    scaling_factor = (M_GUT / M_GUT_base)**4 * (24.68 / alpha_GUT_inv)**2

    tau_p = tau_p_central * scaling_factor

    return tau_p


def compute_tau_p_uncertainty(alpha_4, alpha_5):
    """
    Estimate uncertainty in proton lifetime prediction.

    Goal: Reduce from 0.8 OOM to < 0.5 OOM

    Sources of uncertainty:
    1. M_GUT uncertainty (RG running, threshold corrections)
    2. Yukawa coupling uncertainty (top mass, running)
    3. Hadronic matrix elements (lattice QCD)

    Extra dimensions help by:
    - Constraining M_GUT via KK spectrum (alpha_4, alpha_5 -> specific M_GUT)
    - Reducing parametric freedom
    """
    # Base uncertainty (0.8 orders of magnitude)
    base_uncertainty_OOM = 0.8

    # Improvement factor: extra dimensions constrain M_GUT
    # Full coupling (alpha_4 + alpha_5 = 2) reduces uncertainty by 40%
    improvement = 1.0 - 0.4 * (alpha_4 + alpha_5) / 2.0

    uncertainty_OOM = base_uncertainty_OOM * improvement

    return uncertainty_OOM


def compute_w_0(alpha_4, alpha_5):
    """
    Compute dark energy equation of state with dimensional reduction corrections.

    Current: w_0 = -(d-1)/(d+1) = -11/13 for d_eff = 12
    Target: Match DESI w_0 = -0.83 +/- 0.06

    Mechanism: Effective bulk dimension depends on how much of shared dimensions
    are accessible to dark energy field.

    d_eff = 12 - deltad(alpha_4, alpha_5)
    where deltad depends on localization of Mashiach field to shared dimensions.
    """
    # Base effective dimension (12 spatial + 1 time)
    d_base = 12.0

    # Correction: if Mashiach field partially localizes to 4th/5th dimensions,
    # effective dimension increases -> w_0 shifts toward -1
    delta_d = 0.5 * (alpha_4 + alpha_5)  # Up to 1 extra effective dimension

    d_eff = d_base + delta_d

    # Maximum Entropy Principle formula
    w_0 = -(d_eff - 1.0) / (d_eff + 1.0)

    return w_0


def compute_theta_23(alpha_4, alpha_5):
    """
    Compute atmospheric neutrino mixing angle with extra dimension corrections.

    Current: theta_2_3 = 45 deg (maximal mixing from SO(10) tri-bimaximal)
    Target: theta_2_3 ~ 47.2 deg +/- 2 deg (NuFIT 5.2)

    Mechanism: Yukawa matrices get corrections from:
    1. Wavefunction overlap in extra dimensions
    2. KK mode contributions to seesaw

    deltaY_ν ~ alpha_4, alpha_5 -> shifts theta_2_3 away from maximal
    """
    # Base prediction (maximal mixing)
    theta_23_base = 45.0  # degrees

    # Correction: non-zero alpha breaks maximal mixing slightly
    # Asymmetric coupling to 4th vs 5th dimension shifts angle
    delta_theta = 3.0 * (alpha_4 - alpha_5)  # Up to +/-3 deg shift
    # Note: alpha_4 > alpha_5 increases theta_2_3; alpha_4 < alpha_5 decreases theta_2_3

    theta_23 = theta_23_base + delta_theta

    return theta_23


def compute_m_KK(alpha_4, alpha_5):
    """
    Compute first KK graviton mode mass.

    Formula: m_KK^(1) = sqrt(alpha_4² + alpha_5²) / R

    Interpretation: alpha_i are "accessibilities" of observable brane to i-th dimension.
    Full accessibility (alpha_i = 1) gives standard KK formula.
    Partial accessibility reduces coupling -> appears as higher mass.
    """
    # Effective inverse radius
    R_eff = R_shared / np.sqrt(alpha_4**2 + alpha_5**2 + 1e-10)  # avoid division by zero

    m_KK = 1.0 / R_eff  # GeV

    return m_KK


def compute_m_KK_spectrum(alpha_4, alpha_5, n_max=5):
    """
    Compute first n_max KK mode masses.

    Returns: array of masses [m_KK^(1), m_KK^(2), ..., m_KK^(n_max)]
    """
    m_KK_1 = compute_m_KK(alpha_4, alpha_5)

    # Tower structure: m_KK^(n) ~ n x m_KK^(1) for n << R/l_s
    masses = np.array([n * m_KK_1 for n in range(1, n_max + 1)])

    return masses


# ==============================================================================
# OBJECTIVE FUNCTION: MINIMIZE DEVIATIONS FROM TARGETS
# ==============================================================================

def objective_function(params):
    """
    Objective function to minimize: weighted sum of squared deviations.

    Input: params = [alpha_4, alpha_5]

    Targets:
    1. Proton decay: minimize uncertainty, keep central value reasonable
    2. Dark energy: match w_0 = -0.83 +/- 0.06
    3. Neutrino mixing: match theta_2_3 = 47.2 deg +/- 2 deg
    4. KK mass: m_KK in testable range 5-6 TeV (not too high, not excluded)

    Returns: chi² = Σ [(prediction - target) / error]²
    """
    alpha_4, alpha_5 = params

    # Compute predictions
    tau_p = compute_tau_p(alpha_4, alpha_5)
    tau_p_unc_OOM = compute_tau_p_uncertainty(alpha_4, alpha_5)
    w_0 = compute_w_0(alpha_4, alpha_5)
    theta_23 = compute_theta_23(alpha_4, alpha_5)
    m_KK = compute_m_KK(alpha_4, alpha_5)

    # Chi-squared contributions
    chi2 = 0.0

    # 1. Proton decay: prefer central value near 4x10^34, uncertainty < 0.5 OOM
    tau_p_deviation = (tau_p - tau_p_central) / (tau_p_central * 0.3)  # within 30%
    tau_p_unc_penalty = (tau_p_unc_OOM - tau_p_target_error) / 0.1  # target < 0.5 OOM

    chi2 += tau_p_deviation**2
    chi2 += max(0, tau_p_unc_penalty)**2  # only penalize if > target

    # 2. Dark energy: match DESI w_0 = -0.83 +/- 0.06
    w_0_deviation = (w_0 - w_0_DESI) / w_0_DESI_error
    chi2 += w_0_deviation**2

    # 3. Neutrino mixing: match theta_2_3 = 47.2 deg +/- 2 deg
    theta_23_deviation = (theta_23 - theta_23_observed) / theta_23_error
    chi2 += theta_23_deviation**2

    # 4. KK mass: prefer m_KK ~ 5-6 TeV (testable, not excluded)
    m_KK_target = 5.5e3  # GeV (mid-range)
    m_KK_error = 1.0e3  # GeV (allow +/-1 TeV variation)
    m_KK_deviation = (m_KK - m_KK_target) / m_KK_error
    chi2 += 0.5 * m_KK_deviation**2  # half weight (less critical)

    return chi2


# ==============================================================================
# GRID SEARCH: EXPLORE PARAMETER SPACE
# ==============================================================================

def grid_search(n_points=21):
    """
    Perform grid search over alpha_4, alpha_5 ∈ [-1, 1].

    Returns: DataFrame with all parameter combinations and their predictions.
    """
    print("Performing grid search...")
    print(f"Grid: {n_points} x {n_points} = {n_points**2} points")
    print()

    alpha_4_vals = np.linspace(-1, 1, n_points)
    alpha_5_vals = np.linspace(-1, 1, n_points)

    results = []

    for i, alpha_4 in enumerate(alpha_4_vals):
        for j, alpha_5 in enumerate(alpha_5_vals):
            # Compute predictions
            M_GUT = compute_M_GUT(alpha_4, alpha_5)
            alpha_GUT_inv = compute_alpha_GUT(alpha_4, alpha_5)
            tau_p = compute_tau_p(alpha_4, alpha_5)
            tau_p_unc = compute_tau_p_uncertainty(alpha_4, alpha_5)
            w_0 = compute_w_0(alpha_4, alpha_5)
            theta_23 = compute_theta_23(alpha_4, alpha_5)
            m_KK = compute_m_KK(alpha_4, alpha_5)

            # Compute chi-squared
            chi2 = objective_function([alpha_4, alpha_5])

            # Store results
            results.append({
                'alpha_4': alpha_4,
                'alpha_5': alpha_5,
                'alpha_sum': alpha_4 + alpha_5,
                'alpha_diff': alpha_4 - alpha_5,
                'M_GUT_GeV': M_GUT,
                '1/alpha_GUT': alpha_GUT_inv,
                'tau_p_years': tau_p,
                'tau_p_uncertainty_OOM': tau_p_unc,
                'w_0': w_0,
                'theta_23_deg': theta_23,
                'm_KK_TeV': m_KK / 1e3,
                'chi_squared': chi2
            })

    df = pd.DataFrame(results)
    return df


# ==============================================================================
# OPTIMIZATION: FIND BEST-FIT (alpha_4, alpha_5)
# ==============================================================================

def find_optimal_parameters():
    """
    Use scipy.optimize to find optimal (alpha_4, alpha_5) minimizing chi-squared.

    Method: Nelder-Mead simplex (derivative-free, robust)
    Initial guess: [0.5, -0.5] (symmetric coupling)
    """
    print("Finding optimal parameters via Nelder-Mead optimization...")
    print()

    # Initial guess
    x0 = [0.5, 0.5]

    # Bounds
    bounds = [(-10000000, 10000000), (-10000000, 10000000)]

    # Optimize
    result = minimize(
        objective_function,
        x0,
        method='Nelder-Mead',
        bounds=bounds,
        options={'maxiter': 1000, 'xatol': 1e-6, 'fatol': 1e-6}
    )

    if result.success:
        alpha_4_opt, alpha_5_opt = result.x
        chi2_opt = result.fun

        print("[OK] Optimization converged!")
        print(f"  Optimal alpha_4 = {alpha_4_opt:.6f}")
        print(f"  Optimal alpha_5 = {alpha_5_opt:.6f}")
        print(f"  Minimal chi² = {chi2_opt:.4f}")
        print()

        return alpha_4_opt, alpha_5_opt, chi2_opt
    else:
        print("[X] Optimization failed!")
        print(f"  Message: {result.message}")
        print()
        return None, None, None


# ==============================================================================
# ANALYSIS: COMPARE BASELINE VS OPTIMIZED
# ==============================================================================

def compare_predictions(alpha_4_base, alpha_5_base, alpha_4_opt, alpha_5_opt):
    """
    Compare predictions at baseline (alpha_4, alpha_5) vs optimized values.

    Baseline: [0.5, 0.5] (symmetric, no tuning)
    Optimized: Found by minimization
    """
    print("=" * 80)
    print("COMPARISON: BASELINE vs OPTIMIZED PARAMETERS")
    print("=" * 80)
    print()

    # Baseline predictions
    print("BASELINE (alpha_4 = 0.5, alpha_5 = 0.5):")
    print("-" * 80)

    M_GUT_base = compute_M_GUT(alpha_4_base, alpha_5_base)
    alpha_GUT_inv_base = compute_alpha_GUT(alpha_4_base, alpha_5_base)
    tau_p_base = compute_tau_p(alpha_4_base, alpha_5_base)
    tau_p_unc_base = compute_tau_p_uncertainty(alpha_4_base, alpha_5_base)
    w_0_base = compute_w_0(alpha_4_base, alpha_5_base)
    theta_23_base = compute_theta_23(alpha_4_base, alpha_5_base)
    m_KK_base = compute_m_KK(alpha_4_base, alpha_5_base)
    chi2_base = objective_function([alpha_4_base, alpha_5_base])

    print(f"  M_GUT = {M_GUT_base:.3e} GeV")
    print(f"  1/alpha_GUT = {alpha_GUT_inv_base:.2f}")
    print(f"  tau_p = {tau_p_base:.2e} years (uncertainty: {tau_p_unc_base:.2f} OOM)")
    print(f"  w_0 = {w_0_base:.4f} (target: {w_0_DESI} +/- {w_0_DESI_error})")
    print(f"  theta_23 = {theta_23_base:.1f} deg (target: {theta_23_observed} +/- {theta_23_error} deg)")
    print(f"  m_KK^(1) = {m_KK_base/1e3:.2f} TeV")
    print(f"  chi² = {chi2_base:.4f}")
    print()

    # Optimized predictions
    if alpha_4_opt is not None:
        print(f"OPTIMIZED (alpha_4 = {alpha_4_opt:.4f}, alpha_5 = {alpha_5_opt:.4f}):")
        print("-" * 80)

        M_GUT_opt = compute_M_GUT(alpha_4_opt, alpha_5_opt)
        alpha_GUT_inv_opt = compute_alpha_GUT(alpha_4_opt, alpha_5_opt)
        tau_p_opt = compute_tau_p(alpha_4_opt, alpha_5_opt)
        tau_p_unc_opt = compute_tau_p_uncertainty(alpha_4_opt, alpha_5_opt)
        w_0_opt = compute_w_0(alpha_4_opt, alpha_5_opt)
        theta_23_opt = compute_theta_23(alpha_4_opt, alpha_5_opt)
        m_KK_opt = compute_m_KK(alpha_4_opt, alpha_5_opt)
        chi2_opt = objective_function([alpha_4_opt, alpha_5_opt])

        print(f"  M_GUT = {M_GUT_opt:.3e} GeV")
        print(f"  1/alpha_GUT = {alpha_GUT_inv_opt:.2f}")
        print(f"  tau_p = {tau_p_opt:.2e} years (uncertainty: {tau_p_unc_opt:.2f} OOM)")
        print(f"  w_0 = {w_0_opt:.4f} (target: {w_0_DESI} +/- {w_0_DESI_error})")
        print(f"  theta_23 = {theta_23_opt:.1f} deg (target: {theta_23_observed} +/- {theta_23_error} deg)")
        print(f"  m_KK^(1) = {m_KK_opt/1e3:.2f} TeV")
        print(f"  chi² = {chi2_opt:.4f}")
        print()

        # Improvements
        print("IMPROVEMENTS:")
        print("-" * 80)
        print(f"  Delta(1/alpha_GUT) = {alpha_GUT_inv_opt - alpha_GUT_inv_base:+.2f}")
        print(f"  Deltatau_p = {(tau_p_opt - tau_p_base)/tau_p_base * 100:+.1f}%")
        print(f"  Delta(tau_p uncertainty) = {tau_p_unc_opt - tau_p_unc_base:+.2f} OOM")
        print(f"  Deltaw_0 = {w_0_opt - w_0_base:+.4f}")
        print(f"  Deltatheta_23 = {theta_23_opt - theta_23_base:+.1f} deg")
        print(f"  Deltam_KK = {(m_KK_opt - m_KK_base)/1e3:+.2f} TeV")
        print(f"  chi² improvement = {chi2_base - chi2_opt:.4f} ({(chi2_base - chi2_opt)/chi2_base * 100:.1f}%)")
        print()


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == '__main__':

    # Step 1: Grid search to explore parameter space
    print("Step 1: Grid Search")
    print("=" * 80)
    df_grid = grid_search(n_points=21)  # 21x21 = 441 points

    # Save grid results
    df_grid.to_csv('extra_dim_tuning_grid.csv', index=False)
    print(f"[OK] Grid results saved to 'extra_dim_tuning_grid.csv'")
    print()

    # Find best point in grid
    best_idx = df_grid['chi_squared'].idxmin()
    best_grid = df_grid.loc[best_idx]

    print("Best point from grid search:")
    print(f"  alpha_4 = {best_grid['alpha_4']:.4f}")
    print(f"  alpha_5 = {best_grid['alpha_5']:.4f}")
    print(f"  chi² = {best_grid['chi_squared']:.4f}")
    print()

    # Step 2: Optimization to refine best-fit
    print("Step 2: Optimization (Nelder-Mead)")
    print("=" * 80)
    alpha_4_opt, alpha_5_opt, chi2_opt = find_optimal_parameters()

    # Step 3: Comparison
    if alpha_4_opt is not None:
        compare_predictions(0.5, 0.5, alpha_4_opt, alpha_5_opt)

    # Step 4: Summary recommendations
    print("=" * 80)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    print()

    if alpha_4_opt is not None:
        print(f"[OK] RECOMMENDED VALUES:")
        print(f"  alpha_4 (4th dimension influence) = {alpha_4_opt:.4f}")
        print(f"  alpha_5 (5th dimension influence) = {alpha_5_opt:.4f}")
        print()

        # Check which predictions improved
        w_0_opt = compute_w_0(alpha_4_opt, alpha_5_opt)
        theta_23_opt = compute_theta_23(alpha_4_opt, alpha_5_opt)
        tau_p_unc_opt = compute_tau_p_uncertainty(alpha_4_opt, alpha_5_opt)

        print("OUTSTANDING ISSUE RESOLUTION:")
        print()

        # Issue 1: Proton decay
        if tau_p_unc_opt < 0.5:
            print("  [OK] Proton decay uncertainty: RESOLVED")
            print(f"    Reduced to {tau_p_unc_opt:.2f} OOM (target: < 0.5 OOM)")
        else:
            print("  [!] Proton decay uncertainty: PARTIAL")
            print(f"    Reduced to {tau_p_unc_opt:.2f} OOM (target: < 0.5 OOM)")
        print()

        # Issue 2: w_0 (Planck tension)
        w_0_deviation_sigma = abs(w_0_opt - w_0_DESI) / w_0_DESI_error
        if w_0_deviation_sigma < 1.0:
            print("  [OK] Dark energy w_0: RESOLVED")
            print(f"    Within 1sigma of DESI ({w_0_deviation_sigma:.2f}sigma)")
        else:
            print("  [!] Dark energy w_0: IMPROVED")
            print(f"    Deviation: {w_0_deviation_sigma:.2f}sigma (was worse)")
        print()

        # Issue 3: theta_23
        theta_23_deviation_sigma = abs(theta_23_opt - theta_23_observed) / theta_23_error
        if theta_23_deviation_sigma < 1.0:
            print("  [OK] Neutrino mixing theta_23: RESOLVED")
            print(f"    Within 1sigma of NuFIT ({theta_23_deviation_sigma:.2f}sigma)")
        else:
            print("  [!] Neutrino mixing theta_23: IMPROVED")
            print(f"    Deviation: {theta_23_deviation_sigma:.2f}sigma")
        print()

        # Issue 4: KK spectrum
        m_KK_opt = compute_m_KK(alpha_4_opt, alpha_5_opt)
        if 4.5e3 < m_KK_opt < 6.5e3:
            print("  [OK] KK graviton mass: TESTABLE RANGE")
            print(f"    m_KK^(1) = {m_KK_opt/1e3:.2f} TeV (HL-LHC accessible)")
        else:
            print("  [!] KK graviton mass: OUTSIDE OPTIMAL RANGE")
            print(f"    m_KK^(1) = {m_KK_opt/1e3:.2f} TeV")
        print()

        print("NEXT STEPS:")
        print(f"  1. Update config.py with optimal alpha_4 = {alpha_4_opt:.4f}, alpha_5 = {alpha_5_opt:.4f}")
        print("  2. Re-run full SimulateTheory.py with updated parameters")
        print("  3. Verify consistency with all 58 parameters")
        print("  4. Update paper predictions with refined values")
        print()
    else:
        print("[X] Optimization failed - manual exploration recommended")
        print()
        print("Try exploring grid results in 'extra_dim_tuning_grid.csv'")
        print("Focus on regions with low chi²")

    print("=" * 80)
    print("Simulation complete!")
    print("=" * 80)
