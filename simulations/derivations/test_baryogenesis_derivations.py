#!/usr/bin/env python3
"""
Test Suite for Baryogenesis Derivations
========================================

Validates all derivation steps against known results and
ensures Wolfram validation strings are correctly formatted.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import json
import numpy as np
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from derivations.baryogenesis_derivations import BaryogenesisDerivations


class TestBaryogenesisDerivations:
    """Test suite for baryogenesis derivation chain."""

    def __init__(self):
        self.calc = BaryogenesisDerivations(
            delta_cp_deg=235.0,
            m_nu_lightest_eV=0.001,
            m_nu_middle_eV=0.009,
            m_nu_heaviest_eV=0.05
        )
        self.passed = 0
        self.failed = 0

    def assert_close(self, value, expected, rel_tol=0.01, name=""):
        """Assert two values are close within relative tolerance."""
        if abs(value - expected) / abs(expected) < rel_tol:
            print(f"  PASS {name}: {value:.4e} ~= {expected:.4e}")
            self.passed += 1
            return True
        else:
            print(f"  FAIL {name}: {value:.4e} != {expected:.4e}")
            self.failed += 1
            return False

    def assert_true(self, condition, name=""):
        """Assert condition is True."""
        if condition:
            print(f"  PASS {name}")
            self.passed += 1
            return True
        else:
            print(f"  FAIL {name}")
            self.failed += 1
            return False

    def test_sakharov_conditions(self):
        """Test Sakharov conditions verification."""
        print("\n1. Testing Sakharov Conditions...")

        result = self.calc.verify_sakharov_conditions()

        self.assert_true(
            result['all_conditions_satisfied'],
            "All Sakharov conditions satisfied"
        )

        self.assert_true(
            result['conditions']['condition_1_B_violation']['satisfied'],
            "B violation satisfied"
        )

        self.assert_true(
            result['conditions']['condition_2_CP_violation']['satisfied'],
            "CP violation satisfied"
        )

        # Check mechanism descriptions
        self.assert_true(
            'sphaleron' in result['conditions']['condition_1_B_violation']['mechanism'].lower(),
            "B violation via sphalerons"
        )

        self.assert_true(
            'G₂' in result['conditions']['condition_2_CP_violation']['mechanism'] or
            'G2' in result['conditions']['condition_2_CP_violation']['mechanism'],
            "CP violation from G2"
        )

    def test_cp_asymmetry(self):
        """Test CP asymmetry calculation."""
        print("\n2. Testing CP Asymmetry...")

        # Test at canonical mass
        M_N1 = 1e10  # GeV
        result = self.calc.derive_cp_asymmetry(M_N1)

        # Check formula structure
        self.assert_true(
            'epsilon_tree' in result,
            "CP asymmetry has tree-level component"
        )

        self.assert_true(
            'epsilon_with_CP' in result,
            "CP asymmetry includes CP phase"
        )

        # Check sign (should be negative for delta_CP = 235 degrees)
        self.assert_true(
            result['epsilon_final'] < 0,
            "CP asymmetry sign correct for delta_CP = 235 deg"
        )

        # Check CP phase
        self.assert_close(
            result['delta_CP_deg'],
            235.0,
            rel_tol=0.001,
            name="CP phase (degrees)"
        )

        # Check scaling with mass
        M_N1_low = 1e9
        M_N1_high = 1e11
        eps_low = self.calc.derive_cp_asymmetry(M_N1_low)['epsilon_final']
        eps_high = self.calc.derive_cp_asymmetry(M_N1_high)['epsilon_final']

        # Should scale linearly with M_N1
        ratio = abs(eps_high / eps_low)
        expected_ratio = M_N1_high / M_N1_low
        self.assert_close(
            ratio,
            expected_ratio,
            rel_tol=0.01,
            name="Linear scaling with M_N1"
        )

    def test_washout_factor(self):
        """Test washout factor calculation."""
        print("\n3. Testing Washout Factor...")

        # Weak washout regime (K < 1)
        M_weak = 1e8  # GeV
        result_weak = self.calc.calculate_washout_factor(M_weak)

        self.assert_true(
            result_weak['regime'] == 'weak',
            "Weak washout regime identified"
        )

        self.assert_close(
            result_weak['kappa'],
            0.3,
            rel_tol=0.01,
            name="Weak washout efficiency"
        )

        # Strong washout regime (K > 10)
        M_strong = 1e14  # GeV
        result_strong = self.calc.calculate_washout_factor(M_strong)

        self.assert_true(
            result_strong['regime'] == 'strong',
            "Strong washout regime identified"
        )

        self.assert_true(
            result_strong['kappa'] < 0.1,
            "Strong washout suppression"
        )

        # Check K parameter scaling
        # K should scale as M_N^2
        K_ratio = result_strong['K'] / result_weak['K']
        M_ratio = M_strong / M_weak
        self.assert_close(
            K_ratio,
            M_ratio**2,
            rel_tol=0.1,
            name="K scales as M_N^2"
        )

    def test_eta_B_derivation(self):
        """Test full baryon asymmetry derivation."""
        print("\n4. Testing eta_B Derivation...")

        # Use canonical mass
        M_N1 = 1e10  # GeV
        result = self.calc.derive_eta_B(M_N1)

        # Check sphaleron factor
        self.assert_close(
            result['c_sph'],
            28.0 / 79.0,
            rel_tol=0.001,
            name="Sphaleron factor"
        )

        # Check eta_B is positive (we take abs value)
        self.assert_true(
            result['eta_B_predicted'] > 0,
            "eta_B is positive"
        )

        # Check order of magnitude
        self.assert_true(
            1e-11 < result['eta_B_predicted'] < 1e-8,
            "eta_B in expected range"
        )

        # Check derivation chain structure
        self.assert_true(
            'derivation_chain' in result,
            "Derivation chain present"
        )

        self.assert_true(
            len(result['derivation_chain']) >= 3,
            "At least 3 derivation steps"
        )

    def test_davidson_ibarra_bound(self):
        """Test Davidson-Ibarra bound verification."""
        print("\n5. Testing Davidson-Ibarra Bound...")

        # Test mass above bound
        M_above = 1e10  # GeV
        result_above = self.calc.verify_davidson_ibarra_bound(M_above)

        self.assert_true(
            result_above['passes_standard_bound'],
            "M_N1 = 10^10 GeV passes standard bound"
        )

        # Test mass below bound
        M_below = 1e8  # GeV
        result_below = self.calc.verify_davidson_ibarra_bound(M_below)

        self.assert_true(
            not result_below['passes_standard_bound'],
            "M_N1 = 10^8 GeV fails standard bound"
        )

        # Check bound value
        self.assert_close(
            result_above['M_DI_standard_GeV'],
            1e9,
            rel_tol=0.01,
            name="Standard DI bound"
        )

    def test_find_required_mass(self):
        """Test finding required M_N1 for observed asymmetry."""
        print("\n6. Testing Required Mass Finder...")

        result = self.calc.find_required_M_N1(eta_target=6.1e-10)

        # Check convergence
        self.assert_true(
            result['iterations_to_converge'] < 50,
            "Converged in reasonable iterations"
        )

        # Check achieved asymmetry matches target
        self.assert_close(
            result['eta_B_achieved'],
            6.1e-10,
            rel_tol=0.01,
            name="Achieved eta_B matches target"
        )

        # Check M_N1 is positive
        self.assert_true(
            result['M_N1_required_GeV'] > 0,
            "Required M_N1 is positive"
        )

    def test_complete_derivation_chain(self):
        """Test complete derivation chain generation."""
        print("\n7. Testing Complete Derivation Chain...")

        chain = self.calc.generate_complete_derivation_chain()

        # Check metadata
        self.assert_true(
            'metadata' in chain,
            "Metadata present"
        )

        self.assert_true(
            'title' in chain['metadata'],
            "Title present"
        )

        # Check all derivation steps
        expected_steps = [
            'step_1_sakharov_conditions',
            'step_2_cp_asymmetry',
            'step_3_washout_factor',
            'step_4_baryon_asymmetry',
            'step_5_davidson_ibarra',
            'step_6_required_mass'
        ]

        for step in expected_steps:
            self.assert_true(
                step in chain,
                f"{step} in chain"
            )

        # Check Wolfram validation
        self.assert_true(
            'wolfram_master_validation' in chain,
            "Wolfram master validation present"
        )

        # Check references
        self.assert_true(
            'key_references' in chain,
            "Key references present"
        )

        self.assert_true(
            len(chain['key_references']) >= 5,
            "At least 5 references"
        )

    def test_wolfram_queries(self):
        """Test Wolfram query string formatting."""
        print("\n8. Testing Wolfram Query Strings...")

        M_N1 = 1e10
        cp_result = self.calc.derive_cp_asymmetry(M_N1)
        washout_result = self.calc.calculate_washout_factor(M_N1)
        eta_result = self.calc.derive_eta_B(M_N1)

        # Check CP asymmetry queries
        self.assert_true(
            'wolfram_queries' in cp_result,
            "CP asymmetry has Wolfram queries"
        )

        self.assert_true(
            'WolframAlpha' in cp_result['wolfram_queries']['full_asymmetry'],
            "Wolfram query uses WolframAlpha function"
        )

        # Check washout queries
        self.assert_true(
            'wolfram_queries' in washout_result,
            "Washout has Wolfram queries"
        )

        # Check eta_B queries
        self.assert_true(
            'wolfram_queries' in eta_result,
            "eta_B has Wolfram queries"
        )

        self.assert_true(
            'sphaleron_factor' in eta_result['wolfram_queries'],
            "Sphaleron factor query present"
        )

    def test_json_serialization(self):
        """Test JSON serialization of derivation chain."""
        print("\n9. Testing JSON Serialization...")

        chain = self.calc.generate_complete_derivation_chain()

        # Try to serialize to JSON
        try:
            from derivations.baryogenesis_derivations import NumpyEncoder
            json_str = json.dumps(chain, indent=2, cls=NumpyEncoder)
            self.assert_true(True, "JSON serialization successful")

            # Try to deserialize
            chain_reloaded = json.loads(json_str)
            self.assert_true(True, "JSON deserialization successful")

            # Check roundtrip
            self.assert_close(
                chain_reloaded['metadata']['derived_quantities']['eta_B'],
                chain['metadata']['derived_quantities']['eta_B'],
                rel_tol=1e-6,
                name="JSON roundtrip preserves values"
            )

        except Exception as e:
            self.assert_true(False, f"JSON serialization: {e}")

    def test_observational_agreement(self):
        """Test agreement with Planck 2018 observation."""
        print("\n10. Testing Observational Agreement...")

        result = self.calc.find_required_M_N1(eta_target=6.1e-10)

        # Check sigma deviation
        self.assert_true(
            result['full_eta_derivation']['sigma_deviation'] < 2.0,
            "Within 2sigma of Planck 2018"
        )

        # Check agreement flag
        self.assert_true(
            result['full_eta_derivation']['agreement'],
            "Agreement flag is True"
        )

        # Check eta_B in uncertainty range
        eta_pred = result['eta_B_achieved']
        eta_obs = 6.1e-10
        eta_unc = 0.04e-10

        self.assert_true(
            abs(eta_pred - eta_obs) < 2 * eta_unc,
            "eta_B within 2sigma uncertainty"
        )

    def run_all_tests(self):
        """Run all tests and print summary."""
        print("=" * 70)
        print("BARYOGENESIS DERIVATIONS - TEST SUITE")
        print("=" * 70)

        self.test_sakharov_conditions()
        self.test_cp_asymmetry()
        self.test_washout_factor()
        self.test_eta_B_derivation()
        self.test_davidson_ibarra_bound()
        self.test_find_required_mass()
        self.test_complete_derivation_chain()
        self.test_wolfram_queries()
        self.test_json_serialization()
        self.test_observational_agreement()

        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {self.passed + self.failed}")

        if self.failed == 0:
            print("\n*** ALL TESTS PASSED ***")
            return 0
        else:
            print(f"\n*** {self.failed} TESTS FAILED ***")
            return 1


def validate_json_file():
    """Validate the generated JSON file."""
    print("\n" + "=" * 70)
    print("VALIDATING GENERATED JSON FILE")
    print("=" * 70)

    json_path = Path(__file__).parent.parent.parent / "AutoGenerated" / "derivations" / "baryogenesis_chain.json"

    if not json_path.exists():
        print(f"FAIL JSON file not found: {json_path}")
        return False

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chain = json.load(f)

        print(f"PASS JSON file loaded: {json_path}")

        # Check structure
        required_keys = [
            'metadata',
            'step_1_sakharov_conditions',
            'step_2_cp_asymmetry',
            'step_3_washout_factor',
            'step_4_baryon_asymmetry',
            'step_5_davidson_ibarra',
            'step_6_required_mass',
            'wolfram_master_validation',
            'key_references'
        ]

        all_present = True
        for key in required_keys:
            if key in chain:
                print(f"  PASS {key}")
            else:
                print(f"  FAIL {key} MISSING")
                all_present = False

        if all_present:
            print("\nPASS All required sections present")
        else:
            print("\nFAIL Some sections missing")

        # Check key values
        print("\nKey Values:")
        print(f"  M_N1:  {chain['metadata']['derived_quantities']['M_N1_GeV']:.2e} GeV")
        print(f"  epsilon: {chain['metadata']['derived_quantities']['epsilon']:.2e}")
        print(f"  kappa:   {chain['metadata']['derived_quantities']['kappa']:.3f}")
        print(f"  eta_B:   {chain['metadata']['derived_quantities']['eta_B']:.2e}")
        print(f"  Agreement: {chain['metadata']['observational_comparison']['agreement']}")

        return all_present

    except Exception as e:
        print(f"FAIL Error loading JSON: {e}")
        return False


if __name__ == "__main__":
    # Run test suite
    tester = TestBaryogenesisDerivations()
    exit_code = tester.run_all_tests()

    # Validate JSON file
    json_valid = validate_json_file()

    # Final status
    if exit_code == 0 and json_valid:
        print("\n" + "=" * 70)
        print("*** COMPLETE - All tests passed and JSON validated ***")
        print("=" * 70)
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("*** FAILED - See errors above ***")
        print("=" * 70)
        sys.exit(1)
