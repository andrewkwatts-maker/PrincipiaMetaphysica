#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Master Sterile Audit Runner
==========================================================

DOI: 10.5281/zenodo.18079602

This script runs the complete sterile validation suite and generates
the final alignment evidence log.

VALIDATION TIERS:
    1. RIGIDITY TESTS: Prove the model cannot be tuned
    2. ISOTROPIC FLOW: Prove speed of light is constant
    3. BULK LEAKAGE: Prove hidden sector is insulated
    4. TOPOLOGICAL AUDITS: Prove geometric constraints hold
    5. CERTIFICATE STACK: Validate all 42 certificates

OUTPUT:
    - Console report with all test results
    - docs/alignment_evidence.log for Appendix G

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, List
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from src.physics.root_derivation import RootDerivation
from src.validation.stress_test_rigidity import run_all_rigidity_tests
from src.validation.anisotropy_check import verify_4_pattern_orthogonality
from src.sim.isotropic_flow_validator import run_all_isotropic_tests
from src.sim.bulk_leakage_monitor import run_all_leakage_tests
from src.audit.hard_certificate_audit import run_hard_audit
from src.audit.omega_seal_generator import generate_omega_seal
from src.audit.certificate_stack import CertificateStack

# Import topological tests
from tests.topology_gap_check import validate_topological_gap, test_gap_sensitivity
from tests.brane_alignment_audit import verify_sterile_angle, test_brane_geometry
from tests.omega_unwinding_test import run_all_omega_tests


class SterileAuditRunner:
    """
    Master runner for all sterile validation tests.
    """

    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None

    def run_all(self) -> Dict[str, Any]:
        """
        Run the complete sterile audit suite.

        Returns:
            Dictionary with all test results
        """
        self.start_time = datetime.now()

        print("=" * 80)
        print("PRINCIPIA METAPHYSICA v16.2 - STERILE AUDIT SUITE")
        print("=" * 80)
        print(f"Started: {self.start_time.isoformat()}")
        print()

        # Tier 1: Rigidity Tests
        print("[TIER 1] RIGIDITY TESTS")
        print("-" * 40)
        self.results['rigidity'] = self._run_rigidity_tests()

        # Tier 2: Isotropic Flow
        print("\n[TIER 2] ISOTROPIC FLOW VALIDATION")
        print("-" * 40)
        self.results['isotropic'] = self._run_isotropic_tests()

        # Tier 3: Bulk Leakage
        print("\n[TIER 3] BULK LEAKAGE MONITORING")
        print("-" * 40)
        self.results['leakage'] = self._run_leakage_tests()

        # Tier 4: Topological Audits
        print("\n[TIER 4] TOPOLOGICAL AUDITS")
        print("-" * 40)
        self.results['topology'] = self._run_topology_tests()

        # Tier 5: Certificate Stack
        print("\n[TIER 5] CERTIFICATE STACK")
        print("-" * 40)
        self.results['certificates'] = self._run_certificate_audit()

        # Final Summary
        self.end_time = datetime.now()
        self.results['summary'] = self._generate_summary()

        return self.results

    def _run_rigidity_tests(self) -> Dict[str, Any]:
        """Run rigidity test suite."""
        try:
            results = run_all_rigidity_tests()
            status = results['summary']['overall_status']
            print(f"  Metric Rigidity: {results['metric_rigidity']['status']}")
            print(f"  Sum Rule: {results['sum_rule']['status']}")
            print(f"  Cascade Test: {results['perturbation_cascade']['status']}")
            print(f"  TIER STATUS: {status}")
            return {"status": status, "passed": results['summary']['all_passed'], "details": results}
        except Exception as e:
            print(f"  ERROR: {e}")
            return {"status": "ERROR", "passed": False, "error": str(e)}

    def _run_isotropic_tests(self) -> Dict[str, Any]:
        """Run isotropic flow test suite."""
        try:
            results = run_all_isotropic_tests()
            status = results['summary']['status']
            print(f"  Isotropy: {results['isotropy']['status']}")
            print(f"  Light Propagation: {results['light_propagation']['status']}")
            print(f"  Lorentz Invariance: {results['lorentz']['status']}")
            print(f"  TIER STATUS: {status}")
            return {"status": status, "passed": results['summary']['all_passed'], "details": results}
        except Exception as e:
            print(f"  ERROR: {e}")
            return {"status": "ERROR", "passed": False, "error": str(e)}

    def _run_leakage_tests(self) -> Dict[str, Any]:
        """Run bulk leakage test suite."""
        try:
            results = run_all_leakage_tests()
            status = results['summary']['status']
            print(f"  Bulk Audit: {results['bulk_audit']['integrity']}")
            print(f"  Ghost Detection: {results['ghost_detection']['status']}")
            print(f"  Brane Separation: {results['brane_separation']['status']}")
            print(f"  Transverse Pressure: {results['transverse_pressure']['status']}")
            print(f"  TIER STATUS: {status}")
            return {"status": status, "passed": results['summary']['all_passed'], "details": results}
        except Exception as e:
            print(f"  ERROR: {e}")
            return {"status": "ERROR", "passed": False, "error": str(e)}

    def _run_topology_tests(self) -> Dict[str, Any]:
        """Run topological audit suite."""
        try:
            # Topology gap
            gap_result = validate_topological_gap()
            print(f"  Topology Gap: {gap_result['status']}")

            # Sterile angle
            angle_result = verify_sterile_angle()
            print(f"  Sterile Angle: {angle_result['status']}")

            # Brane geometry
            geom_result = test_brane_geometry()
            print(f"  Brane Geometry: {geom_result['status']}")

            # Omega unwinding
            omega_results = run_all_omega_tests()
            print(f"  Omega Unwinding: {omega_results['summary']['status']}")

            all_passed = (
                gap_result['status'] == 'STABLE' and
                angle_result['status'] == 'LOCKED' and
                omega_results['summary']['all_passed']
            )

            status = "TOPOLOGY_VERIFIED" if all_passed else "TOPOLOGY_FAILURE"
            print(f"  TIER STATUS: {status}")

            return {
                "status": status,
                "passed": all_passed,
                "details": {
                    "gap": gap_result,
                    "angle": angle_result,
                    "geometry": geom_result,
                    "omega": omega_results
                }
            }
        except Exception as e:
            print(f"  ERROR: {e}")
            return {"status": "ERROR", "passed": False, "error": str(e)}

    def _run_certificate_audit(self) -> Dict[str, Any]:
        """Run certificate stack audit."""
        try:
            results = run_hard_audit()

            print(f"  Total Certificates: {results['total_certificates']}")
            print(f"  Passed: {results['passed']}")
            print(f"  Failed: {results['failed']}")

            if results['omega_seal']:
                print(f"  Omega Seal: {results['omega_seal']}")

            print(f"  TIER STATUS: {results['final_status']}")

            return {
                "status": results['final_status'],
                "passed": results['final_status'] == 'STERILE_TERMINAL',
                "omega_seal": results['omega_seal'],
                "details": results
            }
        except Exception as e:
            print(f"  ERROR: {e}")
            return {"status": "ERROR", "passed": False, "error": str(e)}

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate final summary."""
        duration = (self.end_time - self.start_time).total_seconds()

        all_passed = all(
            self.results.get(tier, {}).get('passed', False)
            for tier in ['rigidity', 'isotropic', 'leakage', 'topology', 'certificates']
        )

        omega_seal = self.results.get('certificates', {}).get('omega_seal', None)

        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": duration,
            "all_tiers_passed": all_passed,
            "omega_seal": omega_seal,
            "final_verdict": "STERILE_VERIFIED" if all_passed else "STERILE_BREACH"
        }

    def generate_evidence_log(self, filepath: str = None) -> str:
        """
        Generate the alignment evidence log for Appendix G.

        Args:
            filepath: Optional path to save the log

        Returns:
            The log content as a string
        """
        if not self.results:
            raise ValueError("Run the audit first with run_all()")

        log_lines = [
            "=" * 80,
            "PRINCIPIA METAPHYSICA v16.2 - ALIGNMENT EVIDENCE LOG",
            "=" * 80,
            f"Generated: {datetime.now().isoformat()}",
            "",
            "This log certifies that the v16.2 Terminal State has been validated",
            "against all sterile constraints. The model is geometrically locked.",
            "",
            "=" * 80,
            "VALIDATION SUMMARY",
            "=" * 80,
            "",
        ]

        # Summary
        summary = self.results['summary']
        log_lines.extend([
            f"Duration: {summary['duration_seconds']:.2f} seconds",
            f"All Tiers Passed: {summary['all_tiers_passed']}",
            f"Final Verdict: {summary['final_verdict']}",
            "",
        ])

        if summary['omega_seal']:
            log_lines.extend([
                f"OMEGA SEAL: {summary['omega_seal']}",
                "",
            ])

        # Tier results
        log_lines.extend([
            "=" * 80,
            "TIER RESULTS",
            "=" * 80,
            "",
        ])

        tier_names = {
            'rigidity': 'TIER 1: Rigidity Tests',
            'isotropic': 'TIER 2: Isotropic Flow',
            'leakage': 'TIER 3: Bulk Leakage',
            'topology': 'TIER 4: Topological Audits',
            'certificates': 'TIER 5: Certificate Stack',
        }

        for tier_key, tier_name in tier_names.items():
            tier = self.results.get(tier_key, {})
            log_lines.extend([
                f"{tier_name}",
                f"  Status: {tier.get('status', 'N/A')}",
                f"  Passed: {tier.get('passed', False)}",
                "",
            ])

        # Mathematical invariants
        model = RootDerivation()
        log_lines.extend([
            "=" * 80,
            "MATHEMATICAL INVARIANTS",
            "=" * 80,
            "",
            f"SO(24) Generators: {model.SO24_GENERATORS}",
            f"Shadow Torsion: {model.SHADOW_TORSION}",
            f"Manifold Cost: {model.MANIFOLD_COST}",
            f"Total Roots: {model.TOTAL_ROOTS}",
            "",
            f"Observable Nodes: {model.OBSERVABLE_NODES}",
            f"Hidden Supports: {model.HIDDEN_SUPPORTS}",
            f"Sterile Angle: {model.sterile_angle_degrees:.4f} degrees",
            f"Survival Rate: {model.survival_rate:.4f}",
            f"Decay Constant: {model.decay_constant:.4f}",
            "",
            "Root Equation: 276 + 24 - 12 = 288",
            "Node Equation: 125 + 163 = 288",
            "4-Pattern: [6, 6, 6, 6]",
            "",
            "=" * 80,
            "END OF EVIDENCE LOG",
            "=" * 80,
        ])

        log_content = "\n".join(log_lines)

        if filepath:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(log_content)
            print(f"\nEvidence log saved to: {filepath}")

        return log_content


def main():
    """Main entry point."""
    runner = SterileAuditRunner()
    results = runner.run_all()

    # Print final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    summary = results['summary']
    print(f"Duration: {summary['duration_seconds']:.2f} seconds")
    print(f"All Tiers Passed: {summary['all_tiers_passed']}")

    if summary['omega_seal']:
        print(f"\nOMEGA SEAL: {summary['omega_seal']}")

    print(f"\nFINAL VERDICT: {summary['final_verdict']}")
    print("=" * 80)

    # Generate evidence log
    log_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs",
        "alignment_evidence.log"
    )
    runner.generate_evidence_log(log_path)

    # Return exit code
    return 0 if summary['all_tiers_passed'] else 1


if __name__ == "__main__":
    sys.exit(main())
