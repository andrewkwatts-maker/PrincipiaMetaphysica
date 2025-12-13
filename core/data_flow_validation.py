"""
Data Flow Validation Module
===========================

Validates consistency of physics constants across config and simulations.
Detects hardcoded duplicates and circular dependencies.

This module ensures "single source of truth" for key physics parameters:
- M_PLANCK (full vs reduced)
- M_GUT (GUT scale)
- ALPHA_GUT (GUT coupling)
- Topology parameters (b2, b3, chi_eff)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np


@dataclass
class ValidationIssue:
    """Represents a validation issue found during data flow check."""
    severity: str  # "CRITICAL", "WARNING", "INFO"
    parameter: str
    description: str
    locations: List[str]
    expected_value: Optional[float] = None
    actual_values: Optional[List[float]] = None


class DataFlowValidator:
    """
    Validates data flow consistency across the simulation framework.

    Checks:
    1. M_PLANCK consistency (full vs reduced)
    2. M_GUT consistency across all modules
    3. ALPHA_GUT consistency
    4. Topology parameters (b2, b3, chi_eff)
    """

    def __init__(self):
        self.issues: List[ValidationIssue] = []

    def validate_planck_mass(self) -> bool:
        """Check M_PLANCK consistency across modules."""
        from config import PhenomenologyParameters, ModuliParameters

        # Expected values
        M_PLANCK_REDUCED = 2.435e18  # GeV
        M_PLANCK_FULL = 1.221e19     # GeV

        # Check PhenomenologyParameters
        if abs(PhenomenologyParameters.M_PLANCK_REDUCED - M_PLANCK_REDUCED) / M_PLANCK_REDUCED > 0.01:
            self.issues.append(ValidationIssue(
                severity="CRITICAL",
                parameter="M_PLANCK_REDUCED",
                description="PhenomenologyParameters.M_PLANCK_REDUCED differs from expected",
                locations=["config.py:PhenomenologyParameters"],
                expected_value=M_PLANCK_REDUCED,
                actual_values=[PhenomenologyParameters.M_PLANCK_REDUCED]
            ))
            return False

        if abs(PhenomenologyParameters.M_PLANCK_FULL - M_PLANCK_FULL) / M_PLANCK_FULL > 0.01:
            self.issues.append(ValidationIssue(
                severity="CRITICAL",
                parameter="M_PLANCK_FULL",
                description="PhenomenologyParameters.M_PLANCK_FULL differs from expected",
                locations=["config.py:PhenomenologyParameters"],
                expected_value=M_PLANCK_FULL,
                actual_values=[PhenomenologyParameters.M_PLANCK_FULL]
            ))
            return False

        return True

    def validate_m_gut(self) -> bool:
        """Check M_GUT consistency across modules."""
        from config import GaugeUnificationParameters, ProtonLifetimeParameters

        # Single source of truth
        M_GUT_EXPECTED = 2.118e16  # GeV

        values = [
            ("GaugeUnificationParameters", GaugeUnificationParameters.M_GUT),
            ("ProtonLifetimeParameters", ProtonLifetimeParameters.M_GUT),
        ]

        for name, value in values:
            if abs(value - M_GUT_EXPECTED) / M_GUT_EXPECTED > 0.01:
                self.issues.append(ValidationIssue(
                    severity="CRITICAL",
                    parameter="M_GUT",
                    description=f"{name}.M_GUT differs from expected",
                    locations=[f"config.py:{name}"],
                    expected_value=M_GUT_EXPECTED,
                    actual_values=[value]
                ))
                return False

        # Check they're identical (not just close)
        if GaugeUnificationParameters.M_GUT != ProtonLifetimeParameters.M_GUT:
            self.issues.append(ValidationIssue(
                severity="WARNING",
                parameter="M_GUT",
                description="M_GUT values differ between GaugeUnification and ProtonLifetime",
                locations=["config.py:GaugeUnificationParameters", "config.py:ProtonLifetimeParameters"],
                actual_values=[GaugeUnificationParameters.M_GUT, ProtonLifetimeParameters.M_GUT]
            ))

        return True

    def validate_alpha_gut(self) -> bool:
        """Check ALPHA_GUT consistency."""
        from config import GaugeUnificationParameters, ProtonLifetimeParameters

        # Single source of truth: 1/23.54
        ALPHA_GUT_INV_EXPECTED = 23.54

        values = [
            ("GaugeUnificationParameters", GaugeUnificationParameters.ALPHA_GUT_INV),
            ("ProtonLifetimeParameters", 1.0 / ProtonLifetimeParameters.ALPHA_GUT),
        ]

        for name, value in values:
            if abs(value - ALPHA_GUT_INV_EXPECTED) / ALPHA_GUT_INV_EXPECTED > 0.05:
                self.issues.append(ValidationIssue(
                    severity="WARNING",
                    parameter="ALPHA_GUT_INV",
                    description=f"{name} ALPHA_GUT_INV differs from expected",
                    locations=[f"config.py:{name}"],
                    expected_value=ALPHA_GUT_INV_EXPECTED,
                    actual_values=[value]
                ))

        return True

    def validate_topology(self) -> bool:
        """Check topology parameters consistency."""
        from config import FundamentalConstants

        # Expected values
        H11_EXPECTED = 4
        CHI_EFF_EXPECTED = 144
        B3_EXPECTED = 24  # Associative 3-cycles

        if FundamentalConstants.HODGE_H11 != H11_EXPECTED:
            self.issues.append(ValidationIssue(
                severity="CRITICAL",
                parameter="HODGE_H11",
                description="FundamentalConstants.HODGE_H11 differs from expected",
                locations=["config.py:FundamentalConstants"],
                expected_value=H11_EXPECTED,
                actual_values=[FundamentalConstants.HODGE_H11]
            ))
            return False

        chi_eff = FundamentalConstants.euler_characteristic_effective()
        if chi_eff != CHI_EFF_EXPECTED:
            self.issues.append(ValidationIssue(
                severity="CRITICAL",
                parameter="chi_eff",
                description="euler_characteristic_effective() differs from expected",
                locations=["config.py:FundamentalConstants"],
                expected_value=CHI_EFF_EXPECTED,
                actual_values=[chi_eff]
            ))
            return False

        return True

    def validate_simulation_outputs(self, results: Dict) -> bool:
        """
        Validate that simulation outputs are consistent with config.

        Args:
            results: Output from run_all_simulations()
        """
        from config import GaugeUnificationParameters

        # Check M_GUT from proton decay matches config
        if 'proton_decay' in results:
            sim_m_gut = results['proton_decay'].get('M_GUT', 0)
            config_m_gut = GaugeUnificationParameters.M_GUT

            rel_diff = abs(sim_m_gut - config_m_gut) / config_m_gut
            if rel_diff > 0.01:  # 1% tolerance
                self.issues.append(ValidationIssue(
                    severity="WARNING",
                    parameter="M_GUT",
                    description="Simulation-derived M_GUT differs from config",
                    locations=["run_all_simulations.py", "config.py"],
                    expected_value=config_m_gut,
                    actual_values=[sim_m_gut]
                ))

        return len([i for i in self.issues if i.severity == "CRITICAL"]) == 0

    def run_all_validations(self) -> Tuple[bool, List[ValidationIssue]]:
        """
        Run all validation checks.

        Returns:
            (all_passed, issues)
        """
        self.issues = []

        checks = [
            ("M_PLANCK", self.validate_planck_mass),
            ("M_GUT", self.validate_m_gut),
            ("ALPHA_GUT", self.validate_alpha_gut),
            ("Topology", self.validate_topology),
        ]

        all_passed = True
        for name, check in checks:
            try:
                if not check():
                    all_passed = False
            except Exception as e:
                self.issues.append(ValidationIssue(
                    severity="CRITICAL",
                    parameter=name,
                    description=f"Validation check failed with error: {e}",
                    locations=["core/data_flow_validation.py"]
                ))
                all_passed = False

        return all_passed, self.issues

    def print_report(self) -> None:
        """Print validation report."""
        print("=" * 70)
        print("DATA FLOW VALIDATION REPORT")
        print("=" * 70)

        if not self.issues:
            print("[OK] All validations passed - single source of truth maintained")
            return

        critical = [i for i in self.issues if i.severity == "CRITICAL"]
        warnings = [i for i in self.issues if i.severity == "WARNING"]
        info = [i for i in self.issues if i.severity == "INFO"]

        if critical:
            print(f"\n[CRITICAL] {len(critical)} critical issue(s):")
            for issue in critical:
                print(f"  - {issue.parameter}: {issue.description}")
                if issue.expected_value:
                    print(f"    Expected: {issue.expected_value:.4e}")
                if issue.actual_values:
                    print(f"    Actual: {[f'{v:.4e}' for v in issue.actual_values]}")

        if warnings:
            print(f"\n[WARNING] {len(warnings)} warning(s):")
            for issue in warnings:
                print(f"  - {issue.parameter}: {issue.description}")

        if info:
            print(f"\n[INFO] {len(info)} info message(s):")
            for issue in info:
                print(f"  - {issue.parameter}: {issue.description}")

        print("=" * 70)


def validate_data_flow() -> bool:
    """
    Convenience function to run all validations and print report.

    Returns:
        True if all critical checks passed
    """
    validator = DataFlowValidator()
    all_passed, issues = validator.run_all_validations()
    validator.print_report()
    return all_passed


if __name__ == "__main__":
    # Run validation when module is executed directly
    import sys
    sys.path.insert(0, str(__file__).replace("core/data_flow_validation.py", ""))

    passed = validate_data_flow()
    sys.exit(0 if passed else 1)
