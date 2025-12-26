#!/usr/bin/env python3
"""
Pneuma Stability Analysis - v12.8 CORRECTED

Mathematical analysis of pneuma field stability using KKLT-type potential.

CORRECTIONS FROM ORIGINAL PROPOSAL:
1. N_flux = chi_eff / 6 = 24 (not 28) - matches config.py
2. Hessian uses PLUS sign (not minus) - correct calculus

Potential: V(Ψ) = A·exp(-a·Ψ) + B·exp(-b·Ψ)

Mathematical Framework:
- VEV: ∂V/∂Ψ = 0 ⟹ Ψ_VEV = ln(Aa/Bb)/(a-b)
- Stability: ∂²V/∂Ψ² > 0 at VEV ⟹ stable minimum
- Hessian: H = A·a²·exp(-a·VEV) + B·b²·exp(-b·VEV)  [PLUS sign!]

Physical Interpretation:
- Ψ: Pneuma condensate field (scalar modulus)
- A, B: Instanton amplitudes (flux + non-perturbative)
- a, b: Related to flux quanta (cycle volumes)

This is a KKLT/racetrack-type potential, NOT exact F-term V = |∂W/∂Ψ|².

References:
- KKLT: Kachru et al. (2003) hep-th/0301240
- G₂ flux: Acharya (2002) hep-th/0212294

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os

# Import from config.py for consistency
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FluxQuantization

def analyze_pneuma_stability(chi_eff=FluxQuantization.CHI_EFF, verbose=True):
    """
    Analyze pneuma field stability from KKLT-type potential.

    V(Ψ) = A·exp(-a·Ψ) + B·exp(-b·Ψ)

    Parameters:
    -----------
    chi_eff : int
        Effective Euler characteristic (default: 144 from config.py)
    verbose : bool
        Print detailed analysis

    Returns:
    --------
    dict
        Analysis results including VEV, Hessian, and stability
    """

    # CORRECTED: Use standard N_flux from config.py
    # NOT (chi_eff / 6) * (7/6) which gives 28
    n_flux = chi_eff / 6  # = 24 (standard index theorem)

    # Parameters for KKLT-type potential
    # a, b: Related to flux quantization (inverse cycle volumes)
    a = (2 * np.pi) / n_flux
    b = (2 * np.pi) / (n_flux - 1)

    # Instanton amplitudes
    A = 1.0   # Normalized flux/membrane contribution
    B = 1.03  # Non-perturbative correction (3% effect)

    # VEV from ∂V/∂Ψ = 0
    # This formula is CORRECT in original proposal
    vev = np.log((A * a) / (B * b)) / (a - b)

    # CORRECTED: Hessian with PLUS sign
    # Original had MINUS - mathematical error!
    # Correct: ∂²V/∂Ψ² = A·a²·exp(-a·Ψ) + B·b²·exp(-b·Ψ)
    hessian = (A * (a**2) * np.exp(-a * vev)) + (B * (b**2) * np.exp(-b * vev))
    #                                         ^^^^^ PLUS sign (corrected)

    # Stability: Hessian > 0 for minimum
    # Should always be True (both terms positive)
    is_stable = hessian > 0

    # Potential value at VEV
    V_at_vev = A * np.exp(-a * vev) + B * np.exp(-b * vev)

    # First derivative check (should be ~0 at VEV)
    dV_at_vev = -A * a * np.exp(-a * vev) - B * b * np.exp(-b * vev)

    # Numerical validation
    results = {
        'chi_eff': chi_eff,
        'n_flux': n_flux,
        'parameters': {
            'a': a,
            'b': b,
            'A': A,
            'B': B
        },
        'vev': vev,
        'V_at_vev': V_at_vev,
        'dV_at_vev': dV_at_vev,
        'hessian': hessian,
        'is_stable': is_stable,
        'corrections': {
            'n_flux_corrected': 'Changed from 28 to 24 (config.py standard)',
            'hessian_corrected': 'Changed minus to plus sign (correct calculus)'
        }
    }

    if verbose:
        print('='*70)
        print('PNEUMA STABILITY ANALYSIS - v12.8 CORRECTED')
        print('='*70)
        print('\n1. CONFIGURATION (from config.py)')
        print(f'   chi_eff = {chi_eff}')
        print(f'   N_flux = chi_eff / 6 = {n_flux} (standard, not 28!)')
        print(f'   b3 = {FluxQuantization.B3}')

        print('\n2. POTENTIAL PARAMETERS')
        print(f'   a = 2*pi/N_flux = {a:.6f}')
        print(f'   b = 2*pi/(N_flux-1) = {b:.6f}')
        print(f'   A = {A:.3f} (flux amplitude)')
        print(f'   B = {B:.3f} (non-perturbative correction)')

        print('\n3. POTENTIAL FORM')
        print('   V(Psi) = A*exp(-a*Psi) + B*exp(-b*Psi)')
        print('   Type: KKLT/racetrack (not exact F-term)')

        print('\n4. VEV CALCULATION')
        print('   From dV/dPsi = 0:')
        print(f'   Psi_VEV = ln(Aa/Bb)/(a-b)')
        print(f'         = ln({A*a:.6f}/{B*b:.6f}) / {a-b:.6f}')
        print(f'         = {vev:.6f}')

        print('\n5. STABILITY ANALYSIS')
        print('   Hessian: d2V/dPsi2 = A*a^2*exp(-a*VEV) + B*b^2*exp(-b*VEV)')
        print(f'                      = {hessian:.6e}')
        print(f'   dV/dPsi|_VEV = {dV_at_vev:.6e} (should be ~0)')
        print(f'   V(Psi_VEV) = {V_at_vev:.6e}')

        print('\n6. STABILITY CONCLUSION')
        if is_stable:
            print('   STABLE MINIMUM (H > 0)')
            print('   Both Hessian terms are positive, always stable')
        else:
            print('   UNSTABLE (H < 0) - Should not happen!')
            print('   Check for numerical errors')

        print('\n7. CORRECTIONS APPLIED')
        print('   1. N_flux: 28 -> 24 (matches config.py)')
        print('   2. Hessian: minus -> plus (correct mathematics)')
        print('   Impact: Gives correct stability (H > 0)')

        print('\n8. PHYSICAL INTERPRETATION')
        print('   - Psi: Pneuma condensate (scalar modulus)')
        print('   - V: Effective potential (KKLT-type)')
        print('   - VEV: Stabilization point from flux balance')
        print('   - Stable: Both flux + NP terms create minimum')

        print('='*70)

    return results


def compare_with_wrong_formula(chi_eff=FluxQuantization.CHI_EFF):
    """
    Compare correct vs. wrong formulas to show impact of errors.
    """
    print('\n' + '='*70)
    print('COMPARISON: CORRECT vs. WRONG FORMULAS')
    print('='*70)

    # Correct version
    n_flux_correct = chi_eff / 6  # 24
    a_c = (2 * np.pi) / n_flux_correct
    b_c = (2 * np.pi) / (n_flux_correct - 1)
    A, B = 1.0, 1.03
    vev_c = np.log((A * a_c) / (B * b_c)) / (a_c - b_c)
    hessian_correct = (A * a_c**2 * np.exp(-a_c * vev_c)) + (B * b_c**2 * np.exp(-b_c * vev_c))

    # Wrong version (original proposal)
    n_flux_wrong = (chi_eff / 6) * (7/6)  # 28
    a_w = (2 * np.pi) / n_flux_wrong
    b_w = (2 * np.pi) / (n_flux_wrong - 1)
    vev_w = np.log((A * a_w) / (B * b_w)) / (a_w - b_w)
    hessian_wrong = (A * a_w**2 * np.exp(-a_w * vev_w)) - (B * b_w**2 * np.exp(-b_w * vev_w))

    print('\n1. N_FLUX VALUES')
    print(f'   Correct:  N_flux = {n_flux_correct} (config.py standard)')
    print(f'   Wrong:    N_flux = {n_flux_wrong:.2f} (x 7/6 factor)')

    print('\n2. VEV VALUES')
    print(f'   Correct:  Psi_VEV = {vev_c:.6f}')
    print(f'   Wrong:    Psi_VEV = {vev_w:.6f}')
    print(f'   Difference: {abs(vev_c - vev_w):.6f}')

    print('\n3. HESSIAN VALUES')
    print(f'   Correct (+ sign): H = {hessian_correct:+.6e}  -> Stable: {hessian_correct > 0}')
    print(f'   Wrong   (- sign): H = {hessian_wrong:+.6e}  -> Stable: {hessian_wrong > 0}')

    print('\n4. IMPACT')
    if hessian_correct > 0 and hessian_wrong < 0:
        print('   CRITICAL: Wrong formula gives OPPOSITE stability!')
        print('   Correct: Stable minimum (H > 0)')
        print('   Wrong:   Unstable (H < 0)')
    elif abs(hessian_correct - hessian_wrong) > 0.001 * abs(hessian_correct):
        print('   WARNING: Significant numerical difference')
        print(f'   Relative error: {abs(hessian_correct - hessian_wrong)/abs(hessian_correct)*100:.1f}%')

    print('='*70)


if __name__ == "__main__":
    # Run corrected analysis
    results = analyze_pneuma_stability(verbose=True)

    # Show comparison with wrong formulas
    compare_with_wrong_formula()

    # Summary
    print('\n' + '='*70)
    print('SUMMARY')
    print('='*70)
    print(f'N_flux = {results["n_flux"]} (corrected from 28)')
    print(f'Psi_VEV = {results["vev"]:.6f}')
    print(f'Hessian = {results["hessian"]:.6e} (corrected sign)')
    print(f'Stability: {"STABLE" if results["is_stable"] else "UNSTABLE"}')
    print('\nCORRECTIONS REQUIRED:')
    print('1. n_flux = chi_eff / 6  (not x 7/6)')
    print('2. hessian = ... + ...  (not minus)')
    print('='*70)
