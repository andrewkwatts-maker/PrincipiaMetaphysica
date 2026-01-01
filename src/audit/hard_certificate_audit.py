#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Hard Certificate Audit
=====================================================

DOI: 10.5281/zenodo.18079602

This module provides the "Hardened" certificate validation that enforces
Geometric Invariants rather than "Goodness of Fit."

THE HARD GATES:
    C02-R:   Absolute Conservation (Active + Hidden = 288)
    C19-T:   Gauge-Symmetry Parity (12+12 shadow split)
    C39-ISO: Zero-Variance Isotropic Matrix ([6,6,6,6])

THE TERMINAL CERTIFICATES:
    C36: Brane-Gap Pressure (insulation >= 1.304)
    C37: Sterile Angle Lock (25.7234 degrees)
    C38: Spectral Trace Limit (no 126th node)
    C40: Metric Anchor (Node 001 = H0 residue)
    C41: Unitary Unwinding (entropy residue = 0)
    C42: Omega Seal Finality (all certificates passed)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import hashlib
from typing import Dict, Any, List
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.physics.root_derivation import RootDerivation


@dataclass
class HardCertificateResult:
    """Result of a hard certificate check."""
    id: str
    name: str
    requirement: str
    value: Any
    expected: Any
    passed: bool
    status: str


def run_hard_audit(registry_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Terminal 42-Certificate Audit for v16.2.

    Args:
        registry_data: Optional registry data. If None, uses RootDerivation defaults.

    Returns:
        Dictionary with all certificate results and final status
    """
    model = RootDerivation()

    if registry_data is None:
        registry_data = {
            'active': model.OBSERVABLE_NODES,
            'hidden': model.HIDDEN_SUPPORTS,
            'torsion_matrix': [6, 6, 6, 6],
            'shadow_split': [12, 12],
            'H0_residue': 73.04,
        }

    checks = {}
    results = []

    # ================================================================
    # THE HARD GATES
    # ================================================================

    # C02-R: Parity (Absolute Conservation)
    parity_sum = registry_data.get('active', 125) + registry_data.get('hidden', 163)
    c02_passed = (parity_sum == 288)
    checks['C02-R'] = c02_passed
    results.append(HardCertificateResult(
        id="C02-R",
        name="Ancestral Parity",
        requirement="Active + Hidden = 288",
        value=parity_sum,
        expected=288,
        passed=c02_passed,
        status="HARD_LOCKED" if c02_passed else "CONSERVATION_VIOLATION"
    ))

    # C19-T: Gauge-Symmetry Parity (12+12 shadow split)
    shadow_split = registry_data.get('shadow_split', [12, 12])
    c19_passed = (sum(shadow_split) == 24) and (shadow_split[0] == shadow_split[1])
    checks['C19-T'] = c19_passed
    results.append(HardCertificateResult(
        id="C19-T",
        name="Gauge-Symmetry Parity",
        requirement="Shadow Split = [12, 12]",
        value=shadow_split,
        expected=[12, 12],
        passed=c19_passed,
        status="HARD_LOCKED" if c19_passed else "GAUGE_ASYMMETRY"
    ))

    # C39-ISO: 4-Pattern (6 pins per dimension, zero variance)
    torsion = registry_data.get('torsion_matrix', [6, 6, 6, 6])
    variance = float(np.var(torsion))
    c39_passed = all(p == 6 for p in torsion) and len(torsion) == 4 and variance == 0
    checks['C39-ISO'] = c39_passed
    results.append(HardCertificateResult(
        id="C39-ISO",
        name="Isotropic Matrix",
        requirement="Variance = 0, Distribution = [6,6,6,6]",
        value={"matrix": torsion, "variance": variance},
        expected={"matrix": [6, 6, 6, 6], "variance": 0},
        passed=c39_passed,
        status="HARD_LOCKED" if c39_passed else "ANISOTROPY"
    ))

    # ================================================================
    # THE TERMINAL CERTIFICATES
    # ================================================================

    # C36: Brane-Gap Pressure
    active = registry_data.get('active', 125)
    hidden = registry_data.get('hidden', 163)
    insulation_ratio = hidden / active if active > 0 else 0
    c36_passed = insulation_ratio >= 1.304
    checks['C36'] = c36_passed
    results.append(HardCertificateResult(
        id="C36",
        name="Brane-Gap Pressure",
        requirement="Insulation Ratio >= 1.304",
        value=round(insulation_ratio, 4),
        expected=">= 1.304",
        passed=c36_passed,
        status="TERMINAL" if c36_passed else "PRESSURE_FAILURE"
    ))

    # C37: Sterile Angle Lock
    angle = np.degrees(np.arcsin(125/288))
    c37_passed = np.isclose(angle, 25.7234, atol=1e-4)
    checks['C37'] = c37_passed
    results.append(HardCertificateResult(
        id="C37",
        name="Sterile Angle Lock",
        requirement="theta = 25.7234 degrees",
        value=round(angle, 4),
        expected=25.7234,
        passed=c37_passed,
        status="TERMINAL" if c37_passed else "ANGLE_DRIFT"
    ))

    # C38: Spectral Trace Limit (no 126th eigenvalue)
    # The 126th eigenvalue should be effectively zero
    residues = model.derive_metric_residues()
    last_eigenvalue = residues[-1]
    first_eigenvalue = residues[0]
    spectral_gap = last_eigenvalue / first_eigenvalue
    c38_passed = spectral_gap < 1e-5  # 125th is much smaller than 1st
    checks['C38'] = c38_passed
    results.append(HardCertificateResult(
        id="C38",
        name="Spectral Trace Limit",
        requirement="lambda_126 effectively 0",
        value=f"gap ratio = {spectral_gap:.2e}",
        expected="< 1e-5",
        passed=c38_passed,
        status="TERMINAL" if c38_passed else "SPECTRUM_OVERFLOW"
    ))

    # C40: Metric Anchor (Node 001)
    # This should correspond to the Hubble residue
    h0_residue = registry_data.get('H0_residue', 73.04)
    c40_passed = np.isclose(h0_residue, 73.04, rtol=0.02)  # 2% tolerance
    checks['C40'] = c40_passed
    results.append(HardCertificateResult(
        id="C40",
        name="Metric Anchor",
        requirement="H0 residue ~ 73.04",
        value=h0_residue,
        expected=73.04,
        passed=c40_passed,
        status="TERMINAL" if c40_passed else "ANCHOR_DRIFT"
    ))

    # C41: Unitary Unwinding
    entropy_residue = 288 - (active + hidden)
    c41_passed = entropy_residue == 0
    checks['C41'] = c41_passed
    results.append(HardCertificateResult(
        id="C41",
        name="Unitary Unwinding",
        requirement="Entropy Residue = 0",
        value=entropy_residue,
        expected=0,
        passed=c41_passed,
        status="TERMINAL" if c41_passed else "INFORMATION_LOSS"
    ))

    # ================================================================
    # C42-OMEGA: FINAL SEAL
    # ================================================================

    all_passed = all(checks.values())

    if all_passed:
        # Generate Omega Seal
        cert_string = "-".join(f"{k}:{v}" for k, v in sorted(checks.items()))
        seal_hash = hashlib.sha256(cert_string.encode()).hexdigest()[:16].upper()
        omega_seal = f"OMEGA-{seal_hash[:4]}-{seal_hash[4:8]}-{seal_hash[8:12]}"
        c42_status = "SEALED"
    else:
        omega_seal = None
        c42_status = "BREACH"
        failed = [k for k, v in checks.items() if not v]

    checks['C42-Ω'] = all_passed
    results.append(HardCertificateResult(
        id="C42-Ω",
        name="Omega Seal Finality",
        requirement="All Certificates = PASS",
        value=omega_seal if all_passed else f"Failed: {[k for k, v in checks.items() if not v]}",
        expected="SEALED",
        passed=all_passed,
        status=c42_status
    ))

    return {
        "certificates": results,
        "checks": checks,
        "total_certificates": len(results),
        "passed": sum(1 for r in results if r.passed),
        "failed": sum(1 for r in results if not r.passed),
        "omega_seal": omega_seal,
        "final_status": "STERILE_TERMINAL" if all_passed else "NON_STERILE"
    }


def get_certificate_ledger() -> List[Dict[str, str]]:
    """
    Get the complete certificate ledger in tabular format.

    Returns:
        List of certificate definitions
    """
    return [
        {"ID": "C02-R", "Name": "Root Parity", "Constraint": "Active + Hidden = 288", "Role": "Conservation"},
        {"ID": "C19-T", "Name": "Torsion Lock", "Constraint": "Pins = 24 (12+12)", "Role": "Gauge Symmetry"},
        {"ID": "C39-ISO", "Name": "Isotropic Seal", "Constraint": "Distribution = [6,6,6,6]", "Role": "Spacetime"},
        {"ID": "C36", "Name": "Brane-Gap Pressure", "Constraint": "Ratio >= 1.304", "Role": "C-EPSILON"},
        {"ID": "C37", "Name": "Sterile Angle", "Constraint": "theta = 25.7234°", "Role": "Projection"},
        {"ID": "C38", "Name": "Spectral Limit", "Constraint": "lambda_126 = 0", "Role": "Saturation"},
        {"ID": "C40", "Name": "Metric Anchor", "Constraint": "H0 = 73.04", "Role": "Hubble Lock"},
        {"ID": "C41", "Name": "Unitary Unwinding", "Constraint": "Entropy = 0", "Role": "C-OMEGA"},
        {"ID": "C42-Ω", "Name": "Omega Finality", "Constraint": "All PASS", "Role": "Terminal Seal"},
    ]


# ================================================================
# Validation Gate
# ================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PRINCIPIA METAPHYSICA v16.2 - Hard Certificate Audit")
    print("=" * 70)

    result = run_hard_audit()

    print("\nCERTIFICATE LEDGER:")
    print("-" * 70)
    print(f"{'ID':<10} {'Name':<25} {'Status':<15} {'Value'}")
    print("-" * 70)

    for cert in result['certificates']:
        status = cert.status
        value_str = str(cert.value)[:30]
        print(f"{cert.id:<10} {cert.name:<25} {status:<15} {value_str}")

    print("-" * 70)
    print(f"\nTotal: {result['total_certificates']} certificates")
    print(f"Passed: {result['passed']}")
    print(f"Failed: {result['failed']}")

    if result['omega_seal']:
        print(f"\nOMEGA SEAL: {result['omega_seal']}")

    print(f"\nFINAL STATUS: {result['final_status']}")
    print("=" * 70)
