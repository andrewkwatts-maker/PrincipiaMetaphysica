"""
proton_decay_rg.py - Two-Loop RG Running Analysis for Proton Decay

Agent 5: Renormalization Group Corrections to Yukawa Coupling

This module implements:
1. Two-loop beta functions for Yukawa coupling y(μ)
2. Gauge coupling unification (MSSM vs non-SUSY)
3. RG running from M_Pl -> M_GUT -> M_Z
4. Threshold corrections at each scale
5. Suppression factor calculation for proton decay

OBJECTIVE: Calculate suppression from RG running to resolve τ_p tension

Context:
- Current issue: τ_p = 2.36×10⁶ years (28 orders too short)
- Root cause: Formula uses Γ ∝ 1/Λ² instead of correct 1/Λ⁴
- This module: Additional RG suppression from y(M_Pl) -> y(M_Z)

Principia Metaphysica v6.1+
Date: 2025-11-26
"""

import numpy as np
from sympy import symbols, sqrt, exp, log, diff, dsolve, Function, Eq, N, pi, simplify
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Dict, Tuple, List

# ==============================================================================
# PHYSICAL CONSTANTS
# ==============================================================================

class Constants:
    """Physical constants for RG running"""

    # Energy scales (GeV)
    M_PLANCK = 1.2195e19        # Reduced Planck mass
    M_GUT_MSSM = 2.0e16         # MSSM unification scale
    M_GUT_NON_SUSY = 1.8e16     # Non-SUSY GUT scale (lower)
    M_Z = 91.1876               # Z boson mass
    M_PROTON = 0.938272         # Proton mass
    M_TOP = 173.0               # Top quark mass

    # Gauge couplings at M_Z (PDG 2024)
    ALPHA_1_INV_MZ = 59.0       # U(1)_Y inverse coupling
    ALPHA_2_INV_MZ = 29.6       # SU(2)_L inverse coupling
    ALPHA_3_INV_MZ = 8.5        # SU(3)_c inverse coupling

    # MSSM unification
    ALPHA_GUT_INV_MSSM = 24.0   # Unified coupling

    # Conversion factors
    HBAR_GEV_S = 6.582119569e-25    # GeV·s
    SECONDS_PER_YEAR = 3.154e7      # s/year

    # Yukawa initial condition
    Y_PLANCK_INITIAL = 0.1      # y(M_Pl) ~ 0.1


# ==============================================================================
# ONE-LOOP BETA FUNCTIONS (ANALYTICAL)
# ==============================================================================

def beta_yukawa_one_loop_symbolic():
    """
    One-loop beta function for Yukawa coupling (SymPy symbolic).

    β₁(y) = y³/(16π²)

    This is the standard Yukawa self-interaction contribution.

    Returns:
        SymPy expression for β₁(y)
    """
    y = symbols('y', real=True, positive=True)

    # One-loop: β₁(y) = y³/(16π²)
    beta_1 = y**3 / (16 * pi**2)

    return beta_1


def solve_yukawa_one_loop_exact():
    """
    Exact solution to one-loop Yukawa RG equation using SymPy dsolve.

    dy/dt = β₁(y) = y³/(16π²)

    where t = log(μ/μ₀)

    Solution:
        y(t) = y₀ / √(1 - y₀² t/(8π²))

    Returns:
        dict with SymPy solution and Landau pole location
    """
    print("Solving one-loop Yukawa RG equation with SymPy...")

    # Symbols
    t, y0 = symbols('t y0', real=True)
    y = Function('y')

    # Differential equation: dy/dt = y³/(16π²)
    ode = Eq(y(t).diff(t), y(t)**3 / (16 * pi**2))

    print(f"  ODE: {ode}")

    # Solve with initial condition y(0) = y0
    # SymPy general solution (warning: may be complex)
    # We'll use the known solution form instead

    # Known exact solution:
    # 1/y² - 1/y₀² = 2t/(8π²) = t/(4π²)
    # 1/y² = 1/y₀² + t/(4π²)
    # y = y₀ / √(1 + y₀² t/(4π²))

    # Landau pole: denominator -> 0
    # 1 - y₀² t/(8π²) = 0
    # t_pole = 8π² / y₀²

    t_pole = 8 * pi**2 / y0**2

    print(f"  Solution: y(t) = y0 / sqrt(1 - y0^2 * t/(8*pi^2))")
    print(f"  Landau pole: t_pole = 8*pi^2/y0^2 = {simplify(t_pole)}")

    return {
        'solution': 'y(t) = y0 / sqrt(1 - y0^2 * t / (8*pi^2))',
        't_pole': t_pole,
        't_pole_numeric': float(N(t_pole.subs(y0, 0.1)))
    }


def yukawa_one_loop(y, t):
    """
    Numerical one-loop Yukawa RG equation for scipy.integrate.

    dy/dt = y³/(16π²)

    Args:
        y: Yukawa coupling
        t: RG time t = log(μ/μ₀)

    Returns:
        dy/dt
    """
    return y**3 / (16 * np.pi**2)


# ==============================================================================
# TWO-LOOP BETA FUNCTIONS
# ==============================================================================

def beta_yukawa_two_loop_symbolic(model='MSSM'):
    """
    Two-loop beta function for Yukawa coupling (SymPy symbolic).

    β(y) = β₁(y) + β₂(y)

    where:
        β₁(y) = y³/(16π²)
        β₂(y) = y³/(16π²)² [c₁ y² + c₂ λ - c₃ g_s²]

    MSSM coefficients (top Yukawa in MSSM):
        c₁ = -3      (Yukawa self-interaction)
        c₂ = 1       (Higgs quartic coupling)
        c₃ = 16/3    (QCD gauge coupling)

    Non-SUSY SM coefficients:
        c₁ = -3/2
        c₂ = 3/2
        c₃ = 8

    Args:
        model: 'MSSM' or 'SM'

    Returns:
        dict: {
            'beta_1': One-loop term,
            'beta_2': Two-loop term,
            'beta_total': β₁ + β₂,
            'coefficients': (c₁, c₂, c₃)
        }
    """
    print(f"Deriving two-loop Yukawa beta function ({model})...")

    # Symbols
    y, lam, g_s = symbols('y lambda g_s', real=True, positive=True)

    # Coefficients
    if model == 'MSSM':
        c1 = -3
        c2 = 1
        c3 = 16/3
    elif model == 'SM':
        c1 = -3/2
        c2 = 3/2
        c3 = 8
    else:
        raise ValueError(f"Unknown model: {model}")

    # One-loop
    beta_1 = y**3 / (16 * pi**2)

    # Two-loop
    beta_2 = (y**3 / (16 * pi**2)**2) * (c1 * y**2 + c2 * lam - c3 * g_s**2)

    # Total
    beta_total = beta_1 + beta_2

    print(f"  Coefficients: c1={c1}, c2={c2}, c3={c3}")
    print(f"  beta_1(y) = {beta_1}")
    print(f"  beta_2(y) = {simplify(beta_2)}")

    return {
        'beta_1': beta_1,
        'beta_2': beta_2,
        'beta_total': beta_total,
        'coefficients': (c1, c2, c3)
    }


def yukawa_two_loop(y, t, g_s, lam, model='MSSM'):
    """
    Numerical two-loop Yukawa RG equation.

    dy/dt = β₁(y) + β₂(y, g_s, λ)

    Args:
        y: Yukawa coupling
        t: RG time
        g_s: Strong coupling g_s = √(4π α_s)
        lam: Higgs quartic coupling
        model: 'MSSM' or 'SM'

    Returns:
        dy/dt
    """
    # Coefficients
    if model == 'MSSM':
        c1, c2, c3 = -3, 1, 16/3
    else:  # SM
        c1, c2, c3 = -3/2, 3/2, 8

    # One-loop
    beta_1 = y**3 / (16 * np.pi**2)

    # Two-loop
    beta_2 = (y**3 / (16 * np.pi**2)**2) * (c1 * y**2 + c2 * lam - c3 * g_s**2)

    return beta_1 + beta_2


# ==============================================================================
# GAUGE COUPLING UNIFICATION
# ==============================================================================

def gauge_coupling_running_mssm(mu_gev):
    """
    MSSM gauge coupling running with one-loop beta functions.

    dα_i⁻¹/dt = -b_i/(2π)

    where t = log(μ/M_Z) and MSSM beta coefficients:
        b₁ = 33/5   (U(1)_Y)
        b₂ = 1      (SU(2)_L)
        b₃ = -3     (SU(3)_c)

    Args:
        mu_gev: Energy scale in GeV

    Returns:
        dict: {
            'alpha_1': α₁(μ),
            'alpha_2': α₂(μ),
            'alpha_3': α₃(μ),
            'alpha_1_inv': α₁⁻¹(μ),
            'alpha_2_inv': α₂⁻¹(μ),
            'alpha_3_inv': α₃⁻¹(μ)
        }
    """
    # MSSM beta coefficients
    b1 = 33/5
    b2 = 1
    b3 = -3

    # RG time
    t = np.log(mu_gev / Constants.M_Z)

    # Running inverse couplings
    alpha_1_inv = Constants.ALPHA_1_INV_MZ - (b1 / (2*np.pi)) * t
    alpha_2_inv = Constants.ALPHA_2_INV_MZ - (b2 / (2*np.pi)) * t
    alpha_3_inv = Constants.ALPHA_3_INV_MZ - (b3 / (2*np.pi)) * t

    return {
        'alpha_1_inv': alpha_1_inv,
        'alpha_2_inv': alpha_2_inv,
        'alpha_3_inv': alpha_3_inv,
        'alpha_1': 1/alpha_1_inv,
        'alpha_2': 1/alpha_2_inv,
        'alpha_3': 1/alpha_3_inv
    }


def check_mssm_unification():
    """
    Check MSSM gauge coupling unification at M_GUT.

    Returns:
        dict: {
            'M_GUT': Unification scale (GeV),
            'alpha_GUT_inv': Unified α⁻¹,
            'alpha_1_inv': α₁⁻¹(M_GUT),
            'alpha_2_inv': α₂⁻¹(M_GUT),
            'alpha_3_inv': α₃⁻¹(M_GUT),
            'unification_quality': Max deviation,
            'unified': True if within 5%
        }
    """
    print("Checking MSSM gauge coupling unification...")

    M_GUT = Constants.M_GUT_MSSM
    couplings = gauge_coupling_running_mssm(M_GUT)

    # Average
    alpha_inv_avg = (couplings['alpha_1_inv'] +
                     couplings['alpha_2_inv'] +
                     couplings['alpha_3_inv']) / 3

    # Deviations
    dev_1 = abs(couplings['alpha_1_inv'] - alpha_inv_avg) / alpha_inv_avg
    dev_2 = abs(couplings['alpha_2_inv'] - alpha_inv_avg) / alpha_inv_avg
    dev_3 = abs(couplings['alpha_3_inv'] - alpha_inv_avg) / alpha_inv_avg

    max_dev = max(dev_1, dev_2, dev_3)
    unified = max_dev < 0.05  # 5% tolerance

    print(f"  M_GUT = {M_GUT:.2e} GeV")
    print(f"  alpha_1_inv(M_GUT) = {couplings['alpha_1_inv']:.2f}")
    print(f"  alpha_2_inv(M_GUT) = {couplings['alpha_2_inv']:.2f}")
    print(f"  alpha_3_inv(M_GUT) = {couplings['alpha_3_inv']:.2f}")
    print(f"  Average: {alpha_inv_avg:.2f}")
    print(f"  Max deviation: {max_dev*100:.2f}%")
    print(f"  Unified: {unified}")

    return {
        'M_GUT': M_GUT,
        'alpha_GUT_inv': alpha_inv_avg,
        'alpha_1_inv': couplings['alpha_1_inv'],
        'alpha_2_inv': couplings['alpha_2_inv'],
        'alpha_3_inv': couplings['alpha_3_inv'],
        'unification_quality': max_dev,
        'unified': unified
    }


# ==============================================================================
# YUKAWA RG RUNNING
# ==============================================================================

def run_yukawa_one_loop(y_initial, mu_initial_gev, mu_final_gev):
    """
    Run Yukawa coupling from μ_initial to μ_final using one-loop RG.

    Args:
        y_initial: y(μ_initial)
        mu_initial_gev: Initial scale (GeV)
        mu_final_gev: Final scale (GeV)

    Returns:
        dict: {
            'y_final': y(μ_final),
            'suppression': y_final / y_initial,
            't_total': Total RG time log(μ_f/μ_i),
            'evolution': (t_array, y_array) for plotting
        }
    """
    # RG time
    t_total = np.log(mu_final_gev / mu_initial_gev)

    # Time array for evolution
    t_array = np.linspace(0, t_total, 1000)

    # Solve ODE
    y_array = odeint(yukawa_one_loop, y_initial, t_array)
    y_array = y_array.flatten()

    y_final = y_array[-1]
    suppression = y_final / y_initial

    return {
        'y_final': y_final,
        'suppression': suppression,
        't_total': t_total,
        'evolution': (t_array, y_array)
    }


def run_yukawa_two_loop(y_initial, mu_initial_gev, mu_final_gev,
                        model='MSSM', use_running_gs=True):
    """
    Run Yukawa coupling from μ_initial to μ_final using two-loop RG.

    Args:
        y_initial: y(μ_initial)
        mu_initial_gev: Initial scale (GeV)
        mu_final_gev: Final scale (GeV)
        model: 'MSSM' or 'SM'
        use_running_gs: Use running α_s(μ) if True

    Returns:
        dict: Same as run_yukawa_one_loop
    """
    # RG time
    t_total = np.log(mu_final_gev / mu_initial_gev)

    # Time array
    t_array = np.linspace(0, t_total, 1000)

    # Solve with running g_s(t)
    def dydt_wrapper(y, t):
        # Current scale
        mu_current = mu_initial_gev * np.exp(t)

        # Running strong coupling
        if use_running_gs:
            couplings = gauge_coupling_running_mssm(mu_current)
            alpha_s = couplings['alpha_3']
            g_s = np.sqrt(4 * np.pi * alpha_s)
        else:
            # Fixed at initial scale
            couplings_init = gauge_coupling_running_mssm(mu_initial_gev)
            alpha_s_init = couplings_init['alpha_3']
            g_s = np.sqrt(4 * np.pi * alpha_s_init)

        # Higgs quartic (rough estimate: λ ~ y²)
        lam = y**2

        return yukawa_two_loop(y, t, g_s, lam, model)

    # Solve ODE
    y_array = odeint(dydt_wrapper, y_initial, t_array)
    y_array = y_array.flatten()

    y_final = y_array[-1]
    suppression = y_final / y_initial

    return {
        'y_final': y_final,
        'suppression': suppression,
        't_total': t_total,
        'evolution': (t_array, y_array)
    }


def run_yukawa_cascade(y_planck=0.1, model='MSSM', use_two_loop=True):
    """
    Run Yukawa coupling through cascade: M_Pl -> M_GUT -> M_Z.

    Args:
        y_planck: y(M_Pl) initial value
        model: 'MSSM' or 'SM'
        use_two_loop: Use two-loop beta function if True

    Returns:
        dict: {
            'y_Planck': y(M_Pl),
            'y_GUT': y(M_GUT),
            'y_Z': y(M_Z),
            'suppression_total': y(M_Z) / y(M_Pl),
            'suppression_Pl_to_GUT': y(M_GUT) / y(M_Pl),
            'suppression_GUT_to_Z': y(M_Z) / y(M_GUT),
            'evolution_Pl_to_GUT': (t, y) arrays,
            'evolution_GUT_to_Z': (t, y) arrays
        }
    """
    print(f"Running Yukawa cascade with {model} ({'two-loop' if use_two_loop else 'one-loop'})...")
    print(f"  Initial: y(M_Pl) = {y_planck}")

    # Choose RG function
    if use_two_loop:
        rg_func = run_yukawa_two_loop
    else:
        rg_func = run_yukawa_one_loop

    # M_Pl -> M_GUT
    M_GUT = Constants.M_GUT_MSSM if model == 'MSSM' else Constants.M_GUT_NON_SUSY

    result_Pl_to_GUT = rg_func(y_planck, Constants.M_PLANCK, M_GUT, model=model)
    y_GUT = result_Pl_to_GUT['y_final']

    print(f"  After M_Pl -> M_GUT: y(M_GUT) = {y_GUT:.6e}")
    print(f"    Suppression: {result_Pl_to_GUT['suppression']:.6e}")

    # M_GUT -> M_Z
    result_GUT_to_Z = rg_func(y_GUT, M_GUT, Constants.M_Z, model=model)
    y_Z = result_GUT_to_Z['y_final']

    print(f"  After M_GUT -> M_Z: y(M_Z) = {y_Z:.6e}")
    print(f"    Suppression: {result_GUT_to_Z['suppression']:.6e}")

    # Total suppression
    suppression_total = y_Z / y_planck

    print(f"  Total suppression: y(M_Z)/y(M_Pl) = {suppression_total:.6e}")
    print(f"  Decay rate suppression: [y(M_Z)/y(M_Pl)]^4 = {suppression_total**4:.6e}")

    return {
        'y_Planck': y_planck,
        'y_GUT': y_GUT,
        'y_Z': y_Z,
        'M_GUT': M_GUT,
        'suppression_total': suppression_total,
        'suppression_Pl_to_GUT': result_Pl_to_GUT['suppression'],
        'suppression_GUT_to_Z': result_GUT_to_Z['suppression'],
        'suppression_decay_rate': suppression_total**4,
        'evolution_Pl_to_GUT': result_Pl_to_GUT['evolution'],
        'evolution_GUT_to_Z': result_GUT_to_Z['evolution']
    }


# ==============================================================================
# THRESHOLD CORRECTIONS
# ==============================================================================

def threshold_correction_at_scale(mu_gev, mu_threshold_gev, alpha_threshold):
    """
    Threshold correction at heavy particle mass scale.

    Δλ/λ ~ α log(μ/μ_threshold)

    This represents the finite correction when integrating out heavy states.

    Args:
        mu_gev: Current scale (GeV)
        mu_threshold_gev: Threshold scale (heavy mass)
        alpha_threshold: Coupling at threshold

    Returns:
        Δλ/λ (relative correction)
    """
    return alpha_threshold * np.log(mu_gev / mu_threshold_gev)


def calculate_threshold_corrections(M_GUT_gev, M_KK_tev=5.0):
    """
    Calculate threshold corrections at M_GUT and M_KK.

    At M_GUT: Heavy GUT states integrated out
        Δλ/λ ~ α_GUT log(M_Pl / M_GUT)

    At M_KK: Kaluza-Klein tower integrated out
        Δλ/λ ~ α_KK log(M_GUT / M_KK)

    Args:
        M_GUT_gev: GUT scale (GeV)
        M_KK_tev: KK scale (TeV)

    Returns:
        dict: {
            'Delta_at_GUT': Δλ/λ at M_GUT,
            'Delta_at_KK': Δλ/λ at M_KK,
            'total_correction': Sum,
            'exponential_suppression': exp(-Δλ/λ)
        }
    """
    print("Calculating threshold corrections...")

    # At M_GUT
    alpha_GUT = 1 / Constants.ALPHA_GUT_INV_MSSM
    Delta_GUT = threshold_correction_at_scale(
        Constants.M_PLANCK, M_GUT_gev, alpha_GUT
    )

    print(f"  At M_GUT = {M_GUT_gev:.2e} GeV:")
    print(f"    alpha_GUT = {alpha_GUT:.4f}")
    print(f"    log(M_Pl/M_GUT) = {np.log(Constants.M_PLANCK/M_GUT_gev):.2f}")
    print(f"    Delta_lambda/lambda = {Delta_GUT:.4f}")

    # At M_KK
    M_KK_gev = M_KK_tev * 1e3
    couplings_KK = gauge_coupling_running_mssm(M_KK_gev)
    alpha_KK = couplings_KK['alpha_3']  # Use strong coupling

    Delta_KK = threshold_correction_at_scale(M_GUT_gev, M_KK_gev, alpha_KK)

    print(f"  At M_KK = {M_KK_tev} TeV:")
    print(f"    alpha_s(M_KK) = {alpha_KK:.4f}")
    print(f"    log(M_GUT/M_KK) = {np.log(M_GUT_gev/M_KK_gev):.2f}")
    print(f"    Delta_lambda/lambda = {Delta_KK:.4f}")

    # Total
    total = Delta_GUT + Delta_KK
    exp_suppression = np.exp(-total)

    print(f"  Total: Delta_lambda/lambda = {total:.4f}")
    print(f"  Exponential suppression: exp(-Delta_lambda/lambda) = {exp_suppression:.6e}")

    return {
        'Delta_at_GUT': Delta_GUT,
        'Delta_at_KK': Delta_KK,
        'total_correction': total,
        'exponential_suppression': exp_suppression
    }


# ==============================================================================
# COMBINED PROTON DECAY SUPPRESSION
# ==============================================================================

def calculate_total_suppression(y_planck=0.1, M_KK_tev=5.0, model='MSSM'):
    """
    Calculate total suppression factor for proton decay from:
    1. RG running y(M_Pl) -> y(M_Z)
    2. Threshold corrections

    Total suppression = (y(M_Z)/y(M_Pl))^4 x exp(-Sum Delta_lambda/lambda)

    Args:
        y_planck: Initial Yukawa at M_Pl
        M_KK_tev: KK scale (TeV)
        model: 'MSSM' or 'SM'

    Returns:
        dict: Full analysis results
    """
    print("\n" + "="*80)
    print("PROTON DECAY SUPPRESSION - FULL RG + THRESHOLD ANALYSIS")
    print("="*80)

    # RG running
    rg_results = run_yukawa_cascade(y_planck, model=model, use_two_loop=True)

    # Threshold corrections
    threshold_results = calculate_threshold_corrections(
        rg_results['M_GUT'], M_KK_tev
    )

    # Combined suppression
    RG_suppression = rg_results['suppression_decay_rate']
    threshold_suppression = threshold_results['exponential_suppression']
    total_suppression = RG_suppression * threshold_suppression

    print("\n" + "-"*80)
    print("COMBINED SUPPRESSION FACTORS:")
    print("-"*80)
    print(f"  RG running: [y(M_Z)/y(M_Pl)]^4 = {RG_suppression:.6e}")
    print(f"  Threshold: exp(-Delta_lambda/lambda) = {threshold_suppression:.6e}")
    print(f"  TOTAL SUPPRESSION: {total_suppression:.6e}")

    # New proton lifetime estimate
    # Original (with bug): τ_p ~ 2.36×10⁶ years
    # With correct formula (Λ⁴): τ_p ~ 10^40 years
    # With RG suppression: τ_p -> τ_p / suppression (rate increases!)

    # Wait - RG running makes y smaller, which INCREASES lifetime (good!)
    # Γ ∝ y⁴, so Γ_new = Γ_old × (y_Z/y_Pl)⁴
    # τ_new = τ_old / (y_Z/y_Pl)⁴ = τ_old × (y_Pl/y_Z)⁴

    enhancement_factor = 1 / total_suppression

    # Base lifetime with CORRECTED formula (from Agent 8 analysis)
    # Γ₆ = (y⁴ M_p⁵) / (32π Λ⁴)
    # For Λ = 1.8×10^16 GeV, y = 0.1, M_p = 0.938 GeV:

    y_eff = rg_results['y_Z']
    Lambda_GUT = rg_results['M_GUT']
    M_p = Constants.M_PROTON

    # Decay rate (GeV units)
    Gamma_GeV = (y_eff**4 * M_p**5) / (32 * np.pi * Lambda_GUT**4)

    # Lifetime (years)
    tau_p_years = (1 / Gamma_GeV) * Constants.HBAR_GEV_S / Constants.SECONDS_PER_YEAR

    print("\n" + "-"*80)
    print("NEW PROTON LIFETIME ESTIMATE:")
    print("-"*80)
    print(f"  y_eff = y(M_Z) = {y_eff:.6e}")
    print(f"  Lambda = M_GUT = {Lambda_GUT:.2e} GeV")
    print(f"  Gamma_p = {Gamma_GeV:.6e} GeV")
    print(f"  tau_p = {tau_p_years:.2e} years")
    print(f"  Super-K bound: 2.4x10^34 years")
    print(f"  Status: {'PASS' if tau_p_years > 2.4e34 else 'FAIL'}")

    return {
        'rg_results': rg_results,
        'threshold_results': threshold_results,
        'RG_suppression': RG_suppression,
        'threshold_suppression': threshold_suppression,
        'total_suppression': total_suppression,
        'enhancement_factor': enhancement_factor,
        'y_effective': y_eff,
        'Lambda_GUT': Lambda_GUT,
        'Gamma_proton_GeV': Gamma_GeV,
        'tau_proton_years': tau_p_years,
        'passes_superK': tau_p_years > 2.4e34
    }


# ==============================================================================
# PLOTTING FUNCTIONS
# ==============================================================================

def plot_yukawa_running(results, save_path=None):
    """
    Plot Yukawa coupling evolution y(μ) from M_Pl to M_Z.

    Args:
        results: Output from run_yukawa_cascade
        save_path: Optional path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: M_Pl -> M_GUT
    t1, y1 = results['evolution_Pl_to_GUT']
    mu1 = Constants.M_PLANCK * np.exp(t1)

    ax1.plot(mu1, y1, 'b-', linewidth=2, label='y(mu)')
    ax1.axvline(results['M_GUT'], color='r', linestyle='--',
                label=f"M_GUT = {results['M_GUT']:.2e} GeV")
    ax1.set_xscale('log')
    ax1.set_xlabel('Energy Scale mu (GeV)', fontsize=12)
    ax1.set_ylabel('Yukawa Coupling y(mu)', fontsize=12)
    ax1.set_title('RG Running: M_Pl -> M_GUT', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

    # Right: M_GUT -> M_Z
    t2, y2 = results['evolution_GUT_to_Z']
    mu2 = results['M_GUT'] * np.exp(t2)

    ax2.plot(mu2, y2, 'g-', linewidth=2, label='y(mu)')
    ax2.axvline(Constants.M_Z, color='orange', linestyle='--',
                label=f"M_Z = {Constants.M_Z:.1f} GeV")
    ax2.set_xscale('log')
    ax2.set_xlabel('Energy Scale mu (GeV)', fontsize=12)
    ax2.set_ylabel('Yukawa Coupling y(mu)', fontsize=12)
    ax2.set_title('RG Running: M_GUT -> M_Z', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  Plot saved to: {save_path}")

    plt.show()


def plot_gauge_unification(save_path=None):
    """
    Plot MSSM gauge coupling unification.

    Args:
        save_path: Optional path to save figure
    """
    # Energy range
    mu_array = np.logspace(np.log10(Constants.M_Z), np.log10(Constants.M_PLANCK), 500)

    alpha_1_inv = np.zeros_like(mu_array)
    alpha_2_inv = np.zeros_like(mu_array)
    alpha_3_inv = np.zeros_like(mu_array)

    for i, mu in enumerate(mu_array):
        couplings = gauge_coupling_running_mssm(mu)
        alpha_1_inv[i] = couplings['alpha_1_inv']
        alpha_2_inv[i] = couplings['alpha_2_inv']
        alpha_3_inv[i] = couplings['alpha_3_inv']

    plt.figure(figsize=(10, 6))
    plt.plot(mu_array, alpha_1_inv, 'b-', linewidth=2, label='alpha_1_inv (U(1)_Y)')
    plt.plot(mu_array, alpha_2_inv, 'g-', linewidth=2, label='alpha_2_inv (SU(2)_L)')
    plt.plot(mu_array, alpha_3_inv, 'r-', linewidth=2, label='alpha_3_inv (SU(3)_c)')

    plt.axvline(Constants.M_GUT_MSSM, color='k', linestyle='--', alpha=0.5,
                label=f'M_GUT = {Constants.M_GUT_MSSM:.2e} GeV')

    plt.xscale('log')
    plt.xlabel('Energy Scale mu (GeV)', fontsize=12)
    plt.ylabel('Inverse Coupling alpha_inv', fontsize=12)
    plt.title('MSSM Gauge Coupling Unification', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  Plot saved to: {save_path}")

    plt.show()


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def main():
    """
    Run complete RG analysis for proton decay.
    """
    print("proton_decay_rg.py - Two-Loop RG Running Analysis")

    # 1. Symbolic beta functions
    print("\n" + "="*80)
    print("STEP 1: SYMBOLIC BETA FUNCTIONS")
    print("="*80)

    beta_1 = beta_yukawa_one_loop_symbolic()
    print(f"  beta_1(y) = {beta_1}")

    beta_2_mssm = beta_yukawa_two_loop_symbolic('MSSM')
    print(f"  beta_2(y) [MSSM] = {simplify(beta_2_mssm['beta_2'])}")

    # 2. Exact solution (one-loop)
    print("\n" + "="*80)
    print("STEP 2: EXACT ONE-LOOP SOLUTION")
    print("="*80)

    exact_solution = solve_yukawa_one_loop_exact()
    print(f"  Landau pole at t = {exact_solution['t_pole_numeric']:.2f}")
    print(f"  (For y0 = 0.1, this is t ~ 790 >> log(M_Pl/M_Z) ~ 42)")

    # 3. Gauge unification
    print("\n" + "="*80)
    print("STEP 3: GAUGE COUPLING UNIFICATION")
    print("="*80)

    unification = check_mssm_unification()

    # 4. Full RG cascade + thresholds
    print("\n" + "="*80)
    print("STEP 4: YUKAWA CASCADE M_Pl -> M_GUT -> M_Z")
    print("="*80)

    full_results = calculate_total_suppression(
        y_planck=0.1,
        M_KK_tev=5.0,
        model='MSSM'
    )

    # 5. Plots (disabled for batch mode)
    print("\n" + "="*80)
    print("STEP 5: PLOTS (SKIPPED IN BATCH MODE)")
    print("="*80)
    print("  To generate plots, call plot_gauge_unification() and plot_yukawa_running()")

    # print("\nPlot 1: Gauge Unification")
    # plot_gauge_unification()

    # print("\nPlot 2: Yukawa Running")
    # plot_yukawa_running(full_results['rg_results'])

    # 6. Summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"  y(M_Pl) = {full_results['rg_results']['y_Planck']:.6e}")
    print(f"  y(M_GUT) = {full_results['rg_results']['y_GUT']:.6e}")
    print(f"  y(M_Z) = {full_results['y_effective']:.6e}")
    print(f"  Total suppression: {full_results['total_suppression']:.6e}")
    print(f"  tau_p (corrected) = {full_results['tau_proton_years']:.2e} years")
    print(f"  Super-K bound: 2.4x10^34 years")
    print(f"  Status: {'PASS' if full_results['passes_superK'] else 'FAIL'}")

    return full_results


if __name__ == '__main__':
    results = main()
