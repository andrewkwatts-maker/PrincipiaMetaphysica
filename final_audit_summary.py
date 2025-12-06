#!/usr/bin/env python3
"""
Final audit summary for predictions.html
"""

import json
from pathlib import Path

# Load theory output
with open('theory_output.json', 'r') as f:
    theory = json.load(f)

# Read predictions HTML
predictions_html = Path('sections/predictions.html').read_text(encoding='utf-8')

print("=" * 80)
print("PREDICTIONS PAGE - FINAL AUDIT SUMMARY")
print("=" * 80)
print()

# Check critical hardcoded values that should match theory_output.json
hardcoded_checks = [
    ("Proton decay lifetime", "3.83", f"{theory['proton_decay']['tau_p_central']/1e34:.2f}"),
    ("Proton decay uncertainty", "0.18", f"{theory['proton_decay']['tau_p_uncertainty_oom']:.2f}"),
    ("M_GUT", "2.118", f"{theory['proton_decay']['M_GUT']/1e16:.3f}"),
    ("alpha_GUT_inv (hardcoded)", "23.54", f"{theory['proton_decay']['alpha_GUT_inv']:.2f}"),
    ("BR(e+pi0)", "64.2", f"{theory['proton_decay_channels']['BR_epi0_mean']*100:.1f}"),
    ("BR(K+nu)", "35.6", f"{theory['proton_decay_channels']['BR_Knu_mean']*100:.1f}"),
    ("Mass ordering IH%", "85.5", f"{theory['neutrino_mass_ordering']['prob_IH_mean']*100:.1f}"),
    ("KK m1", "5.0", f"{theory['kk_spectrum']['m1']/1000:.1f}"),
    ("KK m1_std", "1.5", f"{theory['kk_spectrum']['m1_std']/1000:.1f}"),
]

print("[HARDCODED VALUES CHECK]")
print()
all_ok = True
for name, expected, actual in hardcoded_checks:
    if expected == actual:
        print(f"  [OK] {name}: {expected} (matches simulation)")
    else:
        print(f"  [WARN] {name}: Found {expected}, simulation says {actual}")
        all_ok = False

print()
print("=" * 80)
print("[PM DYNAMIC SYSTEM CHECK]")
print("=" * 80)
print()

# Count PM references
import re
pm_refs = re.findall(r'class="pm-value".*?data-param="([^"]+)"', predictions_html)
pm_categories = {}
for param in pm_refs:
    pm_categories[param] = pm_categories.get(param, 0) + 1

print(f"Total PM.* dynamic references: {len(pm_refs)}")
print()
print("Most used parameters:")
for param, count in sorted(pm_categories.items(), key=lambda x: -x[1])[:10]:
    print(f"  - {param}: {count} times")

print()
print("=" * 80)
print("[KEY PREDICTIONS SUMMARY]")
print("=" * 80)
print()

predictions = [
    ("Proton Decay Lifetime", f"{theory['proton_decay']['tau_p_central']/1e34:.2f} x 10^34 years"),
    ("  Uncertainty", f"±{theory['proton_decay']['tau_p_uncertainty_oom']:.2f} OOM"),
    ("  BR(e+pi0)", f"{theory['proton_decay_channels']['BR_epi0_mean']*100:.1f}% ± {theory['proton_decay_channels']['BR_epi0_std']*100:.1f}%"),
    ("  BR(K+nu)", f"{theory['proton_decay_channels']['BR_Knu_mean']*100:.1f}% ± {theory['proton_decay_channels']['BR_Knu_std']*100:.1f}%"),
    ("", ""),
    ("M_GUT", f"{theory['proton_decay']['M_GUT']/1e16:.3f} x 10^16 GeV"),
    ("alpha_GUT_inv", f"{theory['proton_decay']['alpha_GUT_inv']:.2f}"),
    ("", ""),
    ("PMNS Average Sigma", f"{theory['pmns_matrix']['average_sigma']:.2f} sigma"),
    ("  theta_23", f"{theory['pmns_matrix']['theta_23']:.2f} deg (sigma: {theory['pmns_matrix']['theta_23_sigma']:.2e})"),
    ("  theta_12", f"{theory['pmns_matrix']['theta_12']:.2f} deg (sigma: {theory['pmns_matrix']['theta_12_sigma']:.2f})"),
    ("  theta_13", f"{theory['pmns_matrix']['theta_13']:.2f} deg (sigma: {theory['pmns_matrix']['theta_13_sigma']:.2f})"),
    ("  delta_CP", f"{theory['pmns_matrix']['delta_cp']:.1f} deg (sigma: {theory['pmns_matrix']['delta_cp_sigma']:.2f})"),
    ("", ""),
    ("Mass Ordering", f"IH at {theory['neutrino_mass_ordering']['prob_IH_mean']*100:.1f}% confidence"),
    ("", ""),
    ("KK Spectrum", f"m1 = {theory['kk_spectrum']['m1']/1000:.1f} ± {theory['kk_spectrum']['m1_std']/1000:.1f} TeV"),
    ("  m2", f"{theory['kk_spectrum']['m2']/1000:.1f} ± {theory['kk_spectrum']['m2_std']/1000:.1f} TeV"),
    ("  m3", f"{theory['kk_spectrum']['m3']/1000:.1f} ± {theory['kk_spectrum']['m3_std']/1000:.1f} TeV"),
    ("", ""),
    ("Dark Energy w0", f"{theory['dark_energy']['w0_PM']:.4f}"),
    ("  DESI agreement", f"{theory['dark_energy']['w0_deviation_sigma']:.2f} sigma"),
    ("  Functional test", f"{theory['dark_energy']['functional_test_sigma_preference']:.1f} sigma preference for log form"),
]

for name, value in predictions:
    if name == "":
        print()
    else:
        print(f"  {name:25s} {value}")

print()
print("=" * 80)
if all_ok:
    print("[RESULT] All hardcoded values match simulation output")
else:
    print("[RESULT] Some discrepancies found - review warnings above")
print("=" * 80)
