#!/usr/bin/env python3
"""
PM Values Paper Audit Script
============================
Audits which PM values from theory_output.json are present in the paper
and identifies missing values that need derivation chains.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Define all critical PM values that MUST be in the paper with derivation chains
CRITICAL_PM_VALUES = {
    # === TOPOLOGY (Exact, from geometry) ===
    "topology": {
        "D_bulk": {"value": 26, "patterns": ["D.*=.*26", "26-[Dd]imensional", "26D"], "section": "2", "derivation": "Virasoro anomaly c_total = D - 26 = 0"},
        "D_shadow": {"value": 13, "patterns": ["13-[Dd]imensional", "13D", "\\(12,1\\)"], "section": "3", "derivation": "Sp(2,R) gauge fixing of (24,2) -> (12,1)"},
        "D_G2": {"value": 7, "patterns": ["G.?2.*7", "7-[Dd]imensional.*G.?2", "G_2\\(7D\\)"], "section": "4", "derivation": "G2 holonomy manifold"},
        "b2": {"value": 4, "patterns": ["b_2.*=.*4", "b2.*=.*4"], "section": "4", "derivation": "TCS Mayer-Vietoris: b2 = rank(H^2(X,Z))"},
        "b3": {"value": 24, "patterns": ["b_3.*=.*24", "b3.*=.*24"], "section": "4", "derivation": "Associative 3-cycles count"},
        "chi_eff": {"value": 144, "patterns": ["chi.*=.*144", "\\\\chi.*144"], "section": "4", "derivation": "Flux-dressed Euler characteristic"},
        "n_gen": {"value": 3, "patterns": ["n.*gen.*=.*3", "three.*generation", "3.*generation"], "section": "4", "derivation": "n_gen = |chi_eff|/48 = 144/48 = 3"},
    },

    # === GAUGE UNIFICATION ===
    "gauge": {
        "M_GUT": {"value": 2.118e16, "patterns": ["M.*GUT.*10.*16", "2\\.118.*10.*16", "M_GUT"], "section": "5", "derivation": "Geometric hierarchy from G2 torsion"},
        "alpha_GUT": {"value": 0.0425, "patterns": ["alpha.*GUT.*0\\.04", "1/alpha.*GUT.*23\\.5"], "section": "5", "derivation": "1/alpha_GUT = 10*pi * Vol(Sigma_sing)/Vol(G2) * exp(|T_omega|/h11)"},
        "alpha_GUT_inv": {"value": 23.54, "patterns": ["1/.*alpha.*GUT.*23", "23\\.5"], "section": "5", "derivation": "SO(10) Casimir + D5 singularities"},
        "sin2_theta_W": {"value": 0.23121, "patterns": ["sin.*theta.*W.*0\\.231", "\\\\sin.*2.*theta"], "section": "5", "derivation": "SM gauge coupling from SO(10) breaking"},
    },

    # === PMNS MATRIX ===
    "pmns": {
        "theta_23": {"value": 45.0, "patterns": ["theta.*23.*=.*45", "\\\\theta.*23.*45", "maximal.*mixing"], "section": "6", "derivation": "G2 holonomy SU(3) symmetry => shadow_kuf = shadow_chet => theta_23 = pi/4"},
        "theta_12": {"value": 33.59, "patterns": ["theta.*12.*33", "\\\\theta.*12"], "section": "6", "derivation": "Tri-bimaximal base + perturbation from cycle volumes"},
        "theta_13": {"value": 8.57, "patterns": ["theta.*13.*8\\.5", "\\\\theta.*13"], "section": "6", "derivation": "CALIBRATED (pending Yukawa intersection)"},
        "delta_CP": {"value": 235, "patterns": ["delta.*CP.*235", "\\\\delta.*CP"], "section": "6", "derivation": "CALIBRATED (pending phase calculation)"},
    },

    # === DARK ENERGY ===
    "dark_energy": {
        "w0": {"value": -0.8528, "patterns": ["w.*0.*=.*-0\\.85", "w_0.*-0\\.85", "-0\\.8528"], "section": "7", "derivation": "w0 = -(d_eff - 1)/(d_eff + 1) from MEP"},
        "d_eff": {"value": 12.576, "patterns": ["d.*eff.*=.*12\\.5", "12\\.576"], "section": "7", "derivation": "d_eff = 12 + 0.5*(shadow_kuf + shadow_chet), ghost coeff = |c_ghost|/(2*c_matter)"},
        "wa": {"value": -0.95, "patterns": ["w.*a.*=.*-0\\.9", "w_a.*-"], "section": "7", "derivation": "Thermal friction from Tomita-Takesaki modular flow"},
        "alpha_T": {"value": 2.7, "patterns": ["alpha.*T.*2\\.7", "\\\\alpha.*T"], "section": "7", "derivation": "From two-time thermodynamic framework"},
    },

    # === PROTON DECAY ===
    "proton_decay": {
        "tau_p": {"value": 3.9e34, "patterns": ["tau.*p.*10.*34", "3\\.9.*10.*34", "proton.*lifetime"], "section": "8", "derivation": "tau_p from M_GUT^4 / alpha_GUT^2"},
        "BR_e_pi0": {"value": 0.25, "patterns": ["BR.*0\\.25", "branching.*0\\.25"], "section": "8", "derivation": "BR = (orientation_sum/b3)^2 = (12/24)^2 = 0.25"},
        "T_omega": {"value": -0.884, "patterns": ["T.*omega.*-0\\.88", "T_\\\\omega.*-0\\.88"], "section": "4", "derivation": "Effective torsion from G-flux: T_omega = -b3/N_flux"},
    },

    # === KK SPECTRUM ===
    "kk_graviton": {
        "m_KK": {"value": 5.0, "patterns": ["m.*KK.*5.*TeV", "KK.*graviton.*5", "5.*TeV"], "section": "8", "derivation": "m_KK = R_c^-1 from G2 cycle volumes"},
    },

    # === GW DISPERSION ===
    "gw_dispersion": {
        "eta": {"value": 0.101, "patterns": ["eta.*0\\.10", "\\\\eta.*0\\.1", "GW.*dispersion"], "section": "8", "derivation": "eta = exp(|T_omega|)/b3"},
    },

    # === NEUTRINO MASSES ===
    "neutrino_mass": {
        "m1_eV": {"value": 0.00083, "patterns": ["m.*1.*0\\.0008", "m_1.*eV"], "section": "6", "derivation": "Seesaw from G2 triple intersections"},
        "m2_eV": {"value": 0.00897, "patterns": ["m.*2.*0\\.008", "m_2.*eV"], "section": "6", "derivation": "Seesaw mechanism"},
        "m3_eV": {"value": 0.0503, "patterns": ["m.*3.*0\\.05", "m_3.*eV"], "section": "6", "derivation": "Seesaw mechanism"},
        "sum_masses": {"value": 0.060, "patterns": ["sum.*0\\.06", "\\\\sum.*m.*0\\.06"], "section": "6", "derivation": "Sum < 0.12 eV Planck bound"},
        "delta_m21_sq": {"value": 7.97e-5, "patterns": ["delta.*m.*21.*7\\.9", "\\\\Delta.*m.*21"], "section": "6", "derivation": "Solar mass splitting"},
        "delta_m31_sq": {"value": 2.525e-3, "patterns": ["delta.*m.*31.*2\\.5", "\\\\Delta.*m.*31"], "section": "6", "derivation": "Atmospheric mass splitting"},
        "ordering": {"value": "NH", "patterns": ["Normal.*[Hh]ierarchy", "NH"], "section": "8", "derivation": "76% confidence from flux cycle bias"},
    },

    # === HIGGS & VEV ===
    "higgs_vev": {
        "m_h": {"value": 125.10, "patterns": ["m.*h.*125\\.1", "Higgs.*125", "125\\.1.*GeV"], "section": "5", "derivation": "From Re(T) = 7.086 modulus stabilization"},
        "v_EW": {"value": 174, "patterns": ["v.*EW.*174", "VEV.*174", "174.*GeV"], "section": "5", "derivation": "v = M_Pl * exp(-h21/b3) * exp(|T_omega|)"},
        "Re_T": {"value": 7.086, "patterns": ["Re.*T.*7\\.08", "Re\\(T\\).*7"], "section": "5", "derivation": "Kahler modulus from superpotential minimization"},
    },

    # === FERMION MASSES ===
    "fermion_masses": {
        "m_t": {"value": 172.7, "patterns": ["m.*t.*172", "top.*172"], "section": "6", "derivation": "Yukawa from G2 cycle intersections"},
        "m_b": {"value": 4.18, "patterns": ["m.*b.*4\\.18", "bottom.*4"], "section": "6", "derivation": "Yukawa hierarchy"},
        "m_tau": {"value": 1.777, "patterns": ["m.*tau.*1\\.77", "tau.*1\\.77"], "section": "6", "derivation": "Lepton Yukawa"},
    },

    # === XY BOSONS ===
    "xy_bosons": {
        "M_X": {"value": 2.118e16, "patterns": ["M.*X.*10.*16", "XY.*boson"], "section": "5", "derivation": "GUT scale gauge bosons"},
        "charge_X": {"value": 4/3, "patterns": ["4/3", "\\\\pm.*4/3"], "section": "5", "derivation": "SO(10) quantum numbers"},
        "charge_Y": {"value": 1/3, "patterns": ["1/3", "\\\\pm.*1/3"], "section": "5", "derivation": "SO(10) quantum numbers"},
    },

    # === GAUGE COUPLINGS ===
    "gauge_couplings": {
        "alpha_s": {"value": 0.1179, "patterns": ["alpha.*s.*0\\.117", "\\\\alpha.*s"], "section": "5", "derivation": "Strong coupling at M_Z"},
        "alpha_em": {"value": 1/128, "patterns": ["alpha.*em.*1/128", "1/128"], "section": "5", "derivation": "EM coupling at M_Z"},
    },
}


def search_paper_for_value(paper_content: str, patterns: List[str]) -> Tuple[bool, List[str]]:
    """Search paper content for value patterns, return (found, matched_lines)."""
    found = False
    matched_lines = []

    for pattern in patterns:
        matches = re.finditer(pattern, paper_content, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            found = True
            # Get line context
            start = max(0, match.start() - 50)
            end = min(len(paper_content), match.end() + 50)
            context = paper_content[start:end].replace('\n', ' ')
            matched_lines.append(f"...{context}...")

    return found, matched_lines[:3]  # Return max 3 examples


def audit_paper(paper_path: str) -> Dict:
    """Audit paper for PM value coverage."""

    with open(paper_path, 'r', encoding='utf-8') as f:
        paper_content = f.read()

    results = {
        "total_values": 0,
        "found_values": 0,
        "missing_values": [],
        "found_details": {},
        "missing_details": {},
        "by_category": {},
        "coverage_pct": 0.0
    }

    for category, values in CRITICAL_PM_VALUES.items():
        results["by_category"][category] = {"found": [], "missing": []}

        for param_name, param_info in values.items():
            results["total_values"] += 1

            found, matched_lines = search_paper_for_value(paper_content, param_info["patterns"])

            if found:
                results["found_values"] += 1
                results["found_details"][f"{category}.{param_name}"] = {
                    "value": param_info["value"],
                    "section": param_info["section"],
                    "examples": matched_lines
                }
                results["by_category"][category]["found"].append(param_name)
            else:
                results["missing_values"].append(f"{category}.{param_name}")
                results["missing_details"][f"{category}.{param_name}"] = {
                    "value": param_info["value"],
                    "required_section": param_info["section"],
                    "derivation_chain": param_info["derivation"],
                    "search_patterns": param_info["patterns"]
                }
                results["by_category"][category]["missing"].append(param_name)

    results["coverage_pct"] = 100 * results["found_values"] / results["total_values"]

    return results


def generate_report(results: Dict) -> str:
    """Generate human-readable report."""

    report = []
    report.append("=" * 70)
    report.append("PM VALUES PAPER AUDIT REPORT")
    report.append("=" * 70)
    report.append("")
    report.append(f"COVERAGE: {results['found_values']}/{results['total_values']} ({results['coverage_pct']:.1f}%)")
    report.append("")

    # Summary by category
    report.append("-" * 70)
    report.append("COVERAGE BY CATEGORY:")
    report.append("-" * 70)
    for category, data in results["by_category"].items():
        total = len(data["found"]) + len(data["missing"])
        found = len(data["found"])
        pct = 100 * found / total if total > 0 else 0
        status = "✓" if pct == 100 else "⚠" if pct >= 50 else "✗"
        report.append(f"  {status} {category}: {found}/{total} ({pct:.0f}%)")
        if data["missing"]:
            report.append(f"      Missing: {', '.join(data['missing'])}")

    # Missing values detail
    if results["missing_values"]:
        report.append("")
        report.append("-" * 70)
        report.append(f"MISSING VALUES ({len(results['missing_values'])} total):")
        report.append("-" * 70)
        for key, detail in results["missing_details"].items():
            report.append(f"\n  {key}:")
            report.append(f"    Value: {detail['value']}")
            report.append(f"    Should be in Section: {detail['required_section']}")
            report.append(f"    Derivation: {detail['derivation_chain']}")

    # Found values summary
    report.append("")
    report.append("-" * 70)
    report.append(f"FOUND VALUES ({results['found_values']} total):")
    report.append("-" * 70)
    for key, detail in list(results["found_details"].items())[:10]:  # Show first 10
        report.append(f"  ✓ {key} = {detail['value']} (Section {detail['section']})")
    if len(results["found_details"]) > 10:
        report.append(f"  ... and {len(results['found_details']) - 10} more")

    return "\n".join(report)


def generate_missing_values_plan(results: Dict) -> str:
    """Generate plan for adding missing values."""

    plan = []
    plan.append("=" * 70)
    plan.append("PLAN: ADD MISSING PM VALUES TO PAPER")
    plan.append("=" * 70)
    plan.append("")

    # Group by section
    by_section = {}
    for key, detail in results["missing_details"].items():
        section = detail["required_section"]
        if section not in by_section:
            by_section[section] = []
        by_section[section].append((key, detail))

    for section in sorted(by_section.keys()):
        plan.append(f"\n## Section {section}")
        plan.append("-" * 40)

        for key, detail in by_section[section]:
            plan.append(f"\n### {key}")
            plan.append(f"Value: {detail['value']}")
            plan.append(f"Derivation Chain:")
            plan.append(f"  {detail['derivation_chain']}")
            plan.append("")

    # Appendix table suggestion
    plan.append("\n" + "=" * 70)
    plan.append("SUGGESTED: Add Appendix L - Complete PM Values Table")
    plan.append("=" * 70)
    plan.append("""
Include a comprehensive table with ALL PM values:
| Parameter | Value | Status | Derivation | Experimental |
|-----------|-------|--------|------------|--------------|
| D_bulk    | 26    | Exact  | Virasoro   | N/A          |
| n_gen     | 3     | Exact  | chi/48     | 3            |
| ... all 58 parameters ...
""")

    return "\n".join(plan)


if __name__ == "__main__":
    # Find paper
    script_dir = Path(__file__).parent.parent
    paper_path = script_dir / "principia-metaphysica-paper.html"

    if not paper_path.exists():
        print(f"ERROR: Paper not found at {paper_path}")
        exit(1)

    print(f"Auditing: {paper_path}")
    print("")

    # Run audit
    results = audit_paper(str(paper_path))

    # Generate and print report
    report = generate_report(results)
    print(report)

    # Save detailed results
    output_dir = script_dir / "reports"
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "pm_values_audit.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    # Generate and save plan
    plan = generate_missing_values_plan(results)
    with open(output_dir / "pm_values_missing_plan.md", "w") as f:
        f.write(plan)

    print(f"\n\nDetailed results saved to: {output_dir / 'pm_values_audit.json'}")
    print(f"Missing values plan saved to: {output_dir / 'pm_values_missing_plan.md'}")
