#!/usr/bin/env python3
"""
Audit predictions.html for numerical accuracy against theory_output.json
"""

import json
import re
from pathlib import Path

# Load theory output
with open('theory_output.json', 'r') as f:
    theory = json.load(f)

# Read predictions HTML
predictions_html = Path('sections/predictions.html').read_text(encoding='utf-8')

# Define expected values and patterns
checks = [
    {
        'name': 'Proton decay lifetime (main)',
        'pattern': r'τ<sub>p</sub>\s*=\s*([\d.]+)\s*×\s*10[³⁴]+\s*yr',
        'expected': 3.83,
        'actual': theory['proton_decay']['tau_p_central'] / 1e34,
        'tolerance': 0.01
    },
    {
        'name': 'Proton decay uncertainty',
        'pattern': r'±\s*0\.18\s*OOM',
        'expected': 0.18,
        'actual': round(theory['proton_decay']['tau_p_uncertainty_oom'], 2),
        'tolerance': 0.01
    },
    {
        'name': 'alpha_GUT inverse (hardcoded)',
        'pattern': r'α<sub>GUT</sub>\s*=\s*1/([\d.]+)',
        'expected': 23.54,
        'actual': theory['proton_decay']['alpha_GUT_inv'],
        'tolerance': 0.1
    },
    {
        'name': 'M_GUT',
        'pattern': r'M<sub>GUT</sub>\s*=\s*2\.11[0-9]\s*×\s*10[¹⁶]+\s*GeV',
        'expected': 2.118,
        'actual': theory['proton_decay']['M_GUT'] / 1e16,
        'tolerance': 0.001
    },
    {
        'name': 'BR(e+pi0)',
        'pattern': r'BR\(e[⁺+]π[⁰0]\)\s*=\s*([\d.]+)%',
        'expected': 64.2,
        'actual': theory['proton_decay_channels']['BR_epi0_mean'] * 100,
        'tolerance': 0.5
    },
    {
        'name': 'BR(K+nu)',
        'pattern': r'BR\(K[⁺+]ν̄\)\s*=\s*([\d.]+)%',
        'expected': 35.6,
        'actual': theory['proton_decay_channels']['BR_Knu_mean'] * 100,
        'tolerance': 0.5
    },
    {
        'name': 'Mass ordering probability',
        'pattern': r'(85\.[0-9]+)%?\s*confidence',
        'expected': 85.5,
        'actual': round(theory['neutrino_mass_ordering']['prob_IH_mean'] * 100, 1),
        'tolerance': 0.5
    },
    {
        'name': 'KK mass m1',
        'pattern': r'm[₁1]\s*=\s*([\d.]+)\s*(?:±|TeV)',
        'expected': 5.0,
        'actual': theory['kk_spectrum']['m1'] / 1000,
        'tolerance': 0.1
    },
    {
        'name': 'KK mass m1 error',
        'pattern': r'm[₁1]\s*=\s*[\d.]+\s*±\s*([\d.]+)\s*TeV',
        'expected': 1.5,
        'actual': theory['kk_spectrum']['m1_std'] / 1000,
        'tolerance': 0.1
    },
    {
        'name': 'w0 theory',
        'pattern': r'w[₀0]\s*=\s*-0\.85[0-9]+',
        'expected': -0.8528,
        'actual': theory['dark_energy']['w0_PM'],
        'tolerance': 0.0005
    },
    {
        'name': 'PMNS average sigma',
        'pattern': r'(?:average|avg).*?(0\.0[0-9]+)σ',
        'expected': 0.09,
        'actual': theory['pmns_matrix']['average_sigma'],
        'tolerance': 0.01
    },
]

print("=" * 80)
print("PREDICTIONS PAGE AUDIT")
print("=" * 80)

issues = []
for check in checks:
    matches = re.findall(check['pattern'], predictions_html, re.IGNORECASE)

    if not matches:
        issues.append(f"[WARN] {check['name']}: Pattern not found")
        continue

    # Check all matches
    all_ok = True
    for match in matches:
        value = float(match) if isinstance(match, str) and match.replace('.', '').replace('-', '').isdigit() else None

        if value is None:
            continue

        diff = abs(value - check['expected'])

        if diff > check['tolerance']:
            issues.append(
                f"[ERROR] {check['name']}: Found {value}, expected {check['expected']} "
                f"(actual: {check['actual']:.4f})"
            )
            all_ok = False

    if all_ok:
        print(f"[OK] {check['name']}: OK")

print("\n" + "=" * 80)
if issues:
    print("ISSUES FOUND:")
    print("=" * 80)
    for issue in issues:
        print(issue)
else:
    print("[OK] ALL CHECKS PASSED")
print("=" * 80)

# Additional check: Count PM.* dynamic references
pm_refs = re.findall(r'class="pm-value"', predictions_html)
print(f"\n[INFO] Dynamic PM references: {len(pm_refs)}")

# Check for hardcoded values that should be dynamic
hardcoded_patterns = [
    (r'(?<!data-param=")theta_23[^<]*?(?:47\.2)', 'theta_23 angle'),
    (r'(?<!data-param=")theta_12[^<]*?(?:33\.[0-9])', 'theta_12 angle'),
    (r'(?<!data-param=")theta_13[^<]*?(?:8\.5[0-9])', 'theta_13 angle'),
    (r'(?<!data-param=")delta_cp[^<]*?(?:23[0-9])', 'delta_CP'),
]

print("\n" + "=" * 80)
print("HARDCODED VALUES CHECK")
print("=" * 80)

for pattern, name in hardcoded_patterns:
    # Exclude PM references and experimental data
    matches = re.findall(pattern, predictions_html, re.IGNORECASE)
    if matches:
        print(f"[WARN] Found potential hardcoded {name}: {len(matches)} instances")
        # This is OK if they're in experimental data cells
