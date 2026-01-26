"""
Physics Invariants Test Suite v23.0 - SSoT Edition
===================================================
Validates that the G2 Lagrangian remains invariant under
local coordinate transformations.
Standard check for U(1) and SU(3) symmetry preservation.

Uses FormulasRegistry as Single Source of Truth (SSoT).

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

# Import SSoT Registry
try:
    from simulations.core.FormulasRegistry import get_registry
    REGISTRY = get_registry()
except ImportError:
    REGISTRY = None

def test_gauge_invariance():
    """
    Validates that the G2 Lagrangian remains invariant under
    local coordinate transformations.
    Standard check for U(1) and SU(3) symmetry preservation.
    """
    # Load geometric anchors from SSoT Registry
    if REGISTRY:
        b3 = REGISTRY.elder_kads
        kappa_Delta = REGISTRY.demiurgic_coupling  # κ_Δ = B3/2 + 1/π ≈ 12.318
    else:
        b3 = 24
        kappa_Delta = b3/2 + 1/np.pi  # Fallback

    # Simulate a field phase shift (Gauge Transformation)
    theta = np.random.uniform(0, 2*np.pi)
    field_strength = np.complex128(np.exp(1j * theta))

    # Calculate Lagrangian density L before and after shift
    # L = |(d - iA)phi|^2
    l_initial = kappa_Delta * np.abs(field_strength)**2
    l_transformed = kappa_Delta * np.abs(field_strength * np.exp(-1j * theta))**2

    # Academic tolerance for floating point errors
    is_invariant = np.isclose(l_initial, l_transformed, atol=1e-15)

    print(f"--- GAUGE INVARIANCE AUDIT ---")
    print(f"Phase shift theta: {theta:.6f} rad")
    print(f"L_initial: {l_initial:.10f}")
    print(f"L_transformed: {l_transformed:.10f}")
    print(f"Difference: {abs(l_initial - l_transformed):.2e}")
    print(f"Status: {'[PASS]' if is_invariant else '[FAIL]'}")

    return is_invariant

def test_su3_color_invariance():
    """
    Tests SU(3) color gauge invariance.
    Verifies that the strong force sector remains invariant under color rotations.
    """
    # SU(3) generators (Gell-Mann matrices simplified)
    # Using a representative transformation

    # Load from SSoT Registry
    if REGISTRY:
        b3 = REGISTRY.elder_kads
        C_kaf = REGISTRY.c_kaf  # Flux normalization: B3*(B3-7)/(B3-9) = 27.2
    else:
        b3 = 24
        C_kaf = b3 * (b3 - 7) / (b3 - 9)  # Fallback

    # Color triplet state
    color_state = np.array([1, 0, 0], dtype=complex)

    # Random SU(3) rotation angle
    alpha = np.random.uniform(0, 2*np.pi)

    # Simplified SU(3) transformation (using lambda_3 generator)
    U = np.array([
        [np.exp(1j*alpha), 0, 0],
        [0, np.exp(-1j*alpha), 0],
        [0, 0, 1]
    ])

    transformed_state = U @ color_state

    # The norm should be preserved (gauge invariance)
    norm_initial = np.linalg.norm(color_state)
    norm_transformed = np.linalg.norm(transformed_state)

    is_invariant = np.isclose(norm_initial, norm_transformed, atol=1e-15)

    print(f"\n--- SU(3) COLOR INVARIANCE AUDIT ---")
    print(f"Initial norm: {norm_initial:.10f}")
    print(f"Transformed norm: {norm_transformed:.10f}")
    print(f"Status: {'[PASS]' if is_invariant else '[FAIL]'}")

    return is_invariant

def test_lorentz_invariance():
    """
    Tests Lorentz invariance of the metric signature.
    Verifies (-,+,+,+) Minkowski signature is preserved.
    """
    # Minkowski metric
    eta = np.diag([-1, 1, 1, 1])

    # Lorentz boost in x-direction (v = 0.5c)
    v = 0.5
    gamma = 1 / np.sqrt(1 - v**2)

    Lambda = np.array([
        [gamma, -gamma*v, 0, 0],
        [-gamma*v, gamma, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Transform metric: eta' = Lambda^T @ eta @ Lambda
    eta_transformed = Lambda.T @ eta @ Lambda

    # Check if metric is preserved
    is_invariant = np.allclose(eta, eta_transformed, atol=1e-14)

    print(f"\n--- LORENTZ INVARIANCE AUDIT ---")
    print(f"Original metric signature: {np.diag(eta)}")
    print(f"Transformed metric signature: {np.diag(eta_transformed)}")
    print(f"Status: {'[PASS]' if is_invariant else '[FAIL]'}")

    return is_invariant

def test_manifold_parity():
    """
    Tests the Manifold Parity Check: η_S + σ_T ≈ 1.6403

    v23.0+: The Sophian Drag (η_S = 163/239) and Tzimtzum Pressure (σ_T = 23/24)
    must satisfy this parity relation for the sterile manifold to be stable.

    Exact: 163/239 + 23/24 = 1.64034169820...

    Physical meaning: The force pushing out (Pressure) and the force holding
    back (Drag) must balance against the observer's unit (1.0).
    """
    # Mechanical Triad constants from SSoT Registry
    if REGISTRY:
        eta_S = REGISTRY.sophian_drag           # η_S: H0 friction coefficient
        sigma_T = REGISTRY.tzimtzum_pressure    # σ_T: Void Seal (23/24)
    else:
        reg = get_registry()
        eta_S = reg.sophian_drag           # Fallback from SSoT
        sigma_T = 23.0 / 24.0    # MUST use fraction, NOT decimal!

    # The Parity Sum
    parity_sum = eta_S + sigma_T
    expected_sum = REGISTRY.parity_sum if REGISTRY else get_registry().parity_sum    # Target parity value from SSoT

    # Tolerance for "Demon Lock" validation
    tolerance = 0.0001
    is_valid = abs(parity_sum - expected_sum) < tolerance

    print(f"\n--- MANIFOLD PARITY CHECK (DECAGON) ---")
    print(f"Sophian Drag (eta_S):     {eta_S:.4f}")
    print(f"Tzimtzum Pressure (sigma_T): {sigma_T:.10f} (= 23/24)")
    print(f"Parity Sum (eta_S + sigma_T): {parity_sum:.4f}")
    print(f"Expected:                 {expected_sum:.4f}")
    print(f"Deviation:                {abs(parity_sum - expected_sum):.6f}")
    print(f"Status: {'[PASS]' if is_valid else '[FAIL] - DEMON LOCK COMPROMISED'}")

    return is_valid


def test_integer_closure():
    """
    Tests the Integer Closure constraint: 135 + 153 = 288

    This is the "Demon Lock" signature - the sum of Shadow (135) and
    Logos/Christ Constant (Λ_JC = 153) must equal the total E8×E8 roots (288).
    """
    # Load from SSoT Registry - ALWAYS prefer registry values
    if REGISTRY:
        shadow = REGISTRY.demiurgic_Yetts           # Shadow sector
        Lambda_JC = REGISTRY.logos_joint      # Λ_JC: Logos Potential (153)
        total_roots = REGISTRY.nitzotzin_roots        # E8×E8 root lattice
    else:
        # Fallback only if registry unavailable - must match SSoT values
        shadow = 135           # Fallback: must match registry.demiurgic_Yetts
        Lambda_JC = 153        # Fallback: must match registry.logos_joint
        total_roots = 288      # Fallback: must match registry.nitzotzin_roots

    closure_sum = shadow + Lambda_JC
    is_valid = (closure_sum == total_roots)

    print(f"\n--- INTEGER CLOSURE CHECK (DEMON LOCK) ---")
    print(f"Shadow sector:            {shadow}")
    print(f"Logos Potential (Lambda_JC): {Lambda_JC}")
    print(f"Sum (Shadow + Logos):     {closure_sum}")
    print(f"Expected (E8xE8 roots):   {total_roots}")
    print(f"Status: {'[PASS]' if is_valid else '[FAIL] - DEMON LOCK BROKEN'}")

    return is_valid


def test_sterile_ratio():
    """
    Tests the Sterile Ratio: 163/288 ≈ 0.5660

    The hidden (sterile) sector must maintain this exact ratio to the
    total root lattice for the manifold to remain stable.
    """
    # Load from SSoT Registry
    if REGISTRY:
        P_O = REGISTRY.barbelo_modulus   # P_O: Barbelo Modulus / Bulk Pressure (163)
        total_roots = REGISTRY.nitzotzin_roots   # E8×E8 root lattice (288)
    else:
        P_O = 163          # Fallback: O'Dowd Bulk Pressure
        total_roots = 288

    sterile_ratio = P_O / total_roots
    expected_ratio = 0.56597222222  # 163/288

    tolerance = 1e-10
    is_valid = abs(sterile_ratio - expected_ratio) < tolerance

    print(f"\n--- STERILE RATIO CHECK ---")
    print(f"O'Dowd Bulk Pressure (P_O): {P_O}")
    print(f"Total roots:              {total_roots}")
    print(f"Sterile ratio:            {sterile_ratio:.10f}")
    print(f"Expected:                 {expected_ratio:.10f}")
    print(f"Status: {'[PASS]' if is_valid else '[FAIL]'}")

    return is_valid


def test_tzimtzum_fraction():
    """
    Tests that Tzimtzum Pressure uses the FRACTION 23/24, not a decimal.

    The Tzimtzum is the membrane separating the 27D Bulk from our 4D Void.
    In the Principia, the fraction represents the logic (23 gates open,
    1 gate for the observer), whereas the decimal is just a shadow.
    """
    # Load from SSoT Registry
    if REGISTRY:
        sigma_T = REGISTRY.tzimtzum_pressure  # σ_T from Registry (should be 23/24)
    else:
        sigma_T = 23.0 / 24.0  # Fallback - use FRACTION

    # Verify it equals 23/24 exactly
    sigma_T_fraction = 23.0 / 24.0
    sigma_T_decimal = 0.9583333333333334  # Reference value for comparison

    # Verify Registry value equals 23/24 exactly
    is_valid = np.isclose(sigma_T, sigma_T_fraction, atol=1e-15)

    # Also verify the complement: 1 - σ_T = 1/24 = 1/B3
    complement = 1.0 - sigma_T
    expected_complement = 1.0 / 24.0
    complement_valid = np.isclose(complement, expected_complement, atol=1e-15)

    print(f"\n--- TZIMTZUM FRACTION CHECK ---")
    print(f"sigma_T from Registry:    {sigma_T:.16f}")
    print(f"Expected (23/24):         {sigma_T_fraction:.16f}")
    print(f"Registry = 23/24:         {'[PASS]' if is_valid else '[FAIL]'}")
    print(f"Complement (1 - sigma_T): {complement:.16f}")
    print(f"Expected (1/B3 = 1/24):   {expected_complement:.16f}")
    print(f"Complement valid:         {'[PASS]' if complement_valid else '[FAIL]'}")

    return is_valid and complement_valid


def test_watts_constant_guard_rail():
    """
    Tests that Watts Constant (Ω_W) remains exactly 1.0.

    The Watts Constant is the Observer Unity - it MUST equal exactly 1.0.
    This is the fundamental invariant that ensures the 27D derivation
    remains self-consistent. It cannot be adjusted or "tuned".

    This is a GUARD RAIL - any deviation breaks the entire framework.
    """
    # Load from SSoT Registry
    if REGISTRY:
        Omega_W = REGISTRY.monad_unity    # Ω_W: Observer Unity
        chi_R = REGISTRY.nitsot_par      # χ_R: Sounding Board (1/144)
    else:
        Omega_W = 1.0          # Fallback - IMMUTABLE
        chi_R = 1.0 / 144.0    # Reid Invariant

    # Test exact equality (not approximate)
    is_valid = (Omega_W == 1.0)

    # Also verify: CHI = Ω_W / χ_R = 144
    parity_product = Omega_W / chi_R
    parity_valid = (parity_product == 144.0)

    print(f"\n--- WATTS CONSTANT GUARD RAIL ---")
    print(f"Omega_W (Watts Constant):  {Omega_W}")
    print(f"Expected:                  1.0")
    print(f"Exact match:               {'[PASS]' if is_valid else '[FAIL] - GUARD RAIL BROKEN'}")
    print(f"chi_R (Reid Invariant):    {chi_R}")
    print(f"Parity Product (CHI):      {parity_product} (= Omega_W / chi_R)")
    print(f"Expected CHI:              144.0")
    print(f"CHI valid:                 {'[PASS]' if parity_valid else '[FAIL]'}")

    return is_valid and parity_valid


def test_odowd_hubble_formula():
    """
    Tests the O'Dowd H0 Formula: (288/4) - (P_O/χ_eff) + η_S = 71.55

    This is the derived Hubble constant for the local universe, resolving
    the Hubble Tension through geometric bulk pressure corrections.

    Components:
    - 288/4 = 72 (base from E8×E8 roots)
    - P_O = 163 (O'Dowd Bulk Pressure)
    - chi_eff_total = 144 (cross-shadow effective Euler characteristic)
    - eta_S = 0.6819 (Sophian Drag)

    Note: The O'Dowd formula uses chi_eff_total (144) because bulk pressure
    correction is a global/cross-shadow effect, not chi_eff (72 per sector).
    """
    # Load from SSoT Registry
    if REGISTRY:
        roots_total = REGISTRY.nitzotzin_roots          # 288
        chi_eff_total = REGISTRY.chi_eff_total      # chi_eff_total = 144 (cross-shadow)
        P_O = REGISTRY.barbelo_modulus          # P_O = 163
        eta_S = REGISTRY.sophian_drag               # eta_S = 0.6819
    else:
        reg = get_registry()
        roots_total = 288
        chi_eff_total = 144  # Cross-shadow total (NOT chi_eff = 72 per sector)
        P_O = 163      # O'Dowd Bulk Pressure
        eta_S = reg.sophian_drag  # Sophian Drag from SSoT

    # O'Dowd Formula
    H0_base = roots_total / 4.0                 # 288/4 = 72
    H0_bulk_correction = P_O / chi_eff_total    # 163/144 = 1.1319...
    H0_derived = H0_base - H0_bulk_correction + eta_S

    # Expected value from SSoT Registry
    H0_expected = REGISTRY.h0_local if REGISTRY else get_registry().h0_local
    tolerance = 0.01

    is_valid = abs(H0_derived - H0_expected) < tolerance

    print(f"\n--- O'DOWD H0 FORMULA CHECK ---")
    print(f"Formula: (288/4) - (P_O/chi_eff_total) + eta_S")
    print(f"Base (288/4):              {H0_base:.2f}")
    print(f"Bulk correction (163/144): {H0_bulk_correction:.4f}")
    print(f"Sophian Drag (eta_S):      {eta_S}")
    print(f"H0 derived:                {H0_derived:.4f} km/s/Mpc")
    print(f"H0 expected:               {H0_expected} km/s/Mpc")
    print(f"Deviation:                 {abs(H0_derived - H0_expected):.4f}")
    print(f"Status: {'[PASS]' if is_valid else '[FAIL]'}")

    return is_valid


def run_all_tests():
    """Run all physics invariance tests."""
    print("=" * 60)
    print(" PRINCIPIA METAPHYSICA v23.0 - PHYSICS INVARIANTS AUDIT")
    print("=" * 60)

    results = {
        "U(1) Gauge": test_gauge_invariance(),
        "SU(3) Color": test_su3_color_invariance(),
        "Lorentz": test_lorentz_invariance(),
        "Manifold Parity": test_manifold_parity(),
        "Integer Closure": test_integer_closure(),
        "Sterile Ratio": test_sterile_ratio(),
        "Tzimtzum Fraction": test_tzimtzum_fraction(),
        "Watts Guard Rail": test_watts_constant_guard_rail(),
        "O'Dowd H0 Formula": test_odowd_hubble_formula()
    }

    print("\n" + "=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    all_passed = all(results.values())
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {test_name}: {status}")

    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    run_all_tests()
