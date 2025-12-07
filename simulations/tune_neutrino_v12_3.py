# simulations/tune_neutrino_v12_3.py
"""
PRINCIPIA METAPHYSICA v12.3 - Neutrino Mass Tuning
Find optimal geometric_localization factor to match NuFIT 6.0 data
"""

import numpy as np

def calculate_masses(geometric_localization):
    """Calculate neutrino masses for given localization factor"""

    # Intersection numbers from Braun-Del Zotto-Halverson
    intersections = np.array([
        [ 0,  8,  3],
        [ 8,  0, 12],
        [ 3, 12,  0]
    ])

    # Wilson line phases
    phases = np.array([
        [0.000, 2.813, 1.107],
        [2.813, 0.000, 0.911],
        [1.107, 0.911, 0.000]
    ])

    # M_R quadratic hierarchy (Agent 4 recommendation)
    M_R_diag = np.array([5.1e13, 2.3e13, 5.7e12])  # GeV

    # Yukawa raw
    Y_D_raw = intersections * np.exp(1j * phases)

    # Hybrid suppression
    b3 = 24
    Vol_sigma = np.exp(b3 / (8 * np.pi))
    wavefunction_norm = np.sqrt(Vol_sigma)

    M_Pl = 1.22e19
    M_string = 2.0e16
    planck_suppression = np.sqrt(M_Pl / M_string)

    base_suppression = wavefunction_norm * planck_suppression

    N_flux = 3
    flux_factor = N_flux**(2.0/3.0)
    flux_enhancement = flux_factor * geometric_localization

    effective_suppression = base_suppression * flux_enhancement

    Y_D = Y_D_raw / effective_suppression

    # Seesaw
    M_R = np.diag(M_R_diag)
    v_EW = 246
    m_nu_gev = -Y_D @ np.linalg.inv(M_R) @ Y_D.T * (v_EW**2 / 2)

    # Diagonalize
    vals, U = np.linalg.eig(m_nu_gev)
    masses_gev = np.sort(np.abs(vals))
    masses_ev = masses_gev * 1e9

    # Mass squared differences
    delta_m21_2 = masses_ev[1]**2 - masses_ev[0]**2
    delta_m3l_2 = masses_ev[2]**2 - masses_ev[0]**2

    return {
        'delta_m21_2': delta_m21_2,
        'delta_m3l_2': delta_m3l_2,
        'masses': masses_ev,
        'suppression': effective_suppression
    }

# Target values from NuFIT 6.0 NO
target_delta21 = 7.42e-5  # eV^2
target_delta3l = 2.515e-3  # eV^2

print("="*70)
print("TUNING GEOMETRIC LOCALIZATION FACTOR TO MATCH NuFIT 6.0")
print("="*70)
print()

# Scan localization factors
best_localization = None
best_error = 1e10

for loc in np.linspace(0.5, 3.5, 31):
    result = calculate_masses(loc)

    error_21 = abs(result['delta_m21_2'] - target_delta21) / target_delta21 * 100
    error_3l = abs(result['delta_m3l_2'] - target_delta3l) / target_delta3l * 100
    avg_error = (error_21 + error_3l) / 2

    if error_21 < best_error:
        best_error = error_21
        best_localization = loc
        best_result = result

    if loc in [1.0, 1.5, 2.0, 2.5, 3.0]:
        print(f"localization = {loc:.2f}:")
        print(f"  Suppression: {result['suppression']:.2f}")
        print(f"  Delta_m21^2 = {result['delta_m21_2']:.4e} eV^2 (error: {error_21:.1f}%)")
        print(f"  Delta_m3l^2 = {result['delta_m3l_2']:.4e} eV^2 (error: {error_3l:.1f}%)")
        print(f"  Sum_m_nu = {np.sum(result['masses']):.5f} eV")
        print()

print("="*70)
print(f"OPTIMAL: localization = {best_localization:.3f}")
print(f"  Suppression: {best_result['suppression']:.2f}")
print(f"  Delta_m21^2 error: {best_error:.2f}%")
print(f"  Sum_m_nu = {np.sum(best_result['masses']):.5f} eV")
print("="*70)
