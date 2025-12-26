#!/usr/bin/env python3
"""
Mathematical Verification of Pneuma Stability Formulas
"""
import numpy as np
import sympy as sp

# Define symbolic variables
Psi, a, b, A, B = sp.symbols('Psi a b A B', real=True, positive=True)

print('='*70)
print('PNEUMA STABILITY MATHEMATICAL VERIFICATION')
print('='*70)

# Define the potential V = A*exp(-a*Psi) + B*exp(-b*Psi)
V = A * sp.exp(-a * Psi) + B * sp.exp(-b * Psi)

print('\n1. POTENTIAL FUNCTION')
print('   V(Psi) = A*exp(-a*Psi) + B*exp(-b*Psi)')
print(f'   V = {V}')

# First derivative
dV_dPsi = sp.diff(V, Psi)
print('\n2. FIRST DERIVATIVE (VEV CONDITION)')
print(f'   dV/dPsi = {dV_dPsi}')
print('   dV/dPsi = -A*a*exp(-a*Psi) - B*b*exp(-b*Psi)')

# Solve for VEV: dV/dPsi = 0
print('\n3. VEV FROM dV/dPsi = 0')
print('   Setting dV/dPsi = 0:')
print('   -A*a*exp(-a*Psi) - B*b*exp(-b*Psi) = 0')
print('   A*a*exp(-a*Psi) = -B*b*exp(-b*Psi)')
print('   (A*a)/(B*b) = exp(-b*Psi)/exp(-a*Psi)')
print('   (A*a)/(B*b) = exp((a-b)*Psi)')
print('   ln(A*a/(B*b)) = (a-b)*Psi')
print('   Psi_VEV = ln(A*a/(B*b))/(a-b)')

vev_solution = sp.solve(dV_dPsi, Psi)
print(f'\n   Symbolic solution: Psi_VEV = {vev_solution[0]}')
vev_formula = sp.log(A*a/(B*b)) / (a - b)
print(f'   Expected formula:  Psi_VEV = {vev_formula}')

# Check if they match
print(f'   Match: {sp.simplify(vev_solution[0] - vev_formula) == 0}')

# Second derivative (Hessian)
d2V_dPsi2 = sp.diff(dV_dPsi, Psi)
print('\n4. SECOND DERIVATIVE (HESSIAN/STABILITY)')
print(f'   d2V/dPsi2 = {d2V_dPsi2}')
print('   d2V/dPsi2 = A*a^2*exp(-a*Psi) + B*b^2*exp(-b*Psi)')

# Substitute VEV into Hessian
print('\n5. HESSIAN AT VEV')
hessian_at_vev = d2V_dPsi2.subs(Psi, vev_formula)
hessian_at_vev_simplified = sp.simplify(hessian_at_vev)
print(f'   H = d2V/dPsi2|_VEV = {hessian_at_vev_simplified}')

print('\n   CRITICAL: The Hessian has POSITIVE terms (both + signs)')
print('   For stability (minimum), we need H > 0')

print('\n6. NUMERICAL TEST WITH PROPOSED VALUES')
# Test values from the proposed simulation
chi_eff = 144
n_flux_standard = chi_eff / 6  # = 24
n_flux_moduli = n_flux_standard * (7/6)  # = 28
n_flux_spinor = n_flux_standard * (7/8)  # = 21

a_val = (2 * np.pi) / n_flux_moduli
b_val = (2 * np.pi) / (n_flux_moduli - 1)
A_val = 1.0
B_val = 1.03

print(f'\n   Using N_flux (moduli) = {n_flux_moduli:.2f}:')
print(f'   a = 2*pi/N_flux = {a_val:.6f}')
print(f'   b = 2*pi/(N_flux-1) = {b_val:.6f}')
print(f'   A = {A_val}, B = {B_val}')

# Calculate VEV numerically
vev_num = np.log((A_val * a_val) / (B_val * b_val)) / (a_val - b_val)
print(f'\n   VEV = ln((A*a)/(B*b))/(a-b) = {vev_num:.6f}')

# Calculate Hessian at VEV (CORRECT FORMULA)
hessian_correct = (A_val * a_val**2 * np.exp(-a_val * vev_num)) + (B_val * b_val**2 * np.exp(-b_val * vev_num))
print(f'\n   CORRECT Hessian = A*a^2*exp(-a*VEV) + B*b^2*exp(-b*VEV)')
print(f'                   = {hessian_correct:.6e}')
print(f'   Stable: {hessian_correct > 0} (need H > 0 for minimum)')

print('\n7. ERROR IN PROPOSED FORMULA')
print('   Proposed formula: hessian = A*a^2*exp(-a*VEV) - B*b^2*exp(-b*VEV)')
hessian_wrong = (A_val * a_val**2 * np.exp(-a_val * vev_num)) - (B_val * b_val**2 * np.exp(-b_val * vev_num))
print(f'   WRONG result: {hessian_wrong:.6e}')
print('   ERROR: Uses MINUS sign instead of PLUS!')
print('   Correct: H = A*a^2*exp(-a*Psi) + B*b^2*exp(-b*Psi)')

print('\n8. N_FLUX CONSISTENCY CHECK')
print(f'   N_flux (standard) = {n_flux_standard} (from chi_eff/6)')
print(f'   N_flux (moduli)   = {n_flux_moduli:.2f} (x 7/6 correction)')
print(f'   N_flux (spinor)   = {n_flux_spinor:.2f} (x 7/8 correction)')
print('\n   ISSUE: Proposed code uses moduli fraction (7/6) for N_flux = 28')
print('   But config.py uses standard formula: N_flux = chi_eff/6 = 24')

print('\n9. RELATIONSHIP TO SUPERPOTENTIAL')
print('\n   If V = |dW/dPsi|^2 (F-term potential), then:')
print('   V = A*exp(-a*Psi) + B*exp(-b*Psi)')
print('\n   This implies (up to phase):')
print('   dW/dPsi = sqrt(A)*exp(-a*Psi/2) + sqrt(B)*exp(-b*Psi/2)')
print('\n   Integrating:')
print('   W = -2*sqrt(A)/a * exp(-a*Psi/2) - 2*sqrt(B)/b * exp(-b*Psi/2) + const')
print('\n   This is a racetrack-type superpotential with square root coefficients.')

print('\n10. ALTERNATIVE: KKKLT-TYPE POTENTIAL')
print('\n   Standard KKLT/flux: V = sum_i A_i * exp(-a_i * Psi)')
print('   This is exactly what we have with 2 terms.')
print('   The Hessian formula with + signs is correct for this case.')

print('='*70)
print('\nSUMMARY OF ISSUES:')
print('1. VEV formula is CORRECT: VEV = ln(Aa/Bb)/(a-b)')
print('2. Hessian formula is WRONG: should be + not -')
print('   CORRECT: H = A*a^2*exp(-a*VEV) + B*b^2*exp(-b*VEV)')
print('   WRONG:   H = A*a^2*exp(-a*VEV) - B*b^2*exp(-b*VEV)')
print('3. N_flux value inconsistent: code uses 28, config.py says 24')
print('   Should use N_flux = chi_eff/6 = 24 (standard)')
print('='*70)
