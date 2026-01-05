#!/usr/bin/env python3
"""
Validate Variable Names and Check for Outdated References.

This script scans the project for:
1. Outdated variable names that should use Gnostic naming
2. Hardcoded values that should be dynamic
3. Invalid variable references in HTML/JS files
4. Mismatched parameter names between SSoT and website

Run this script after making changes to ensure consistency.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

PROJECT_ROOT = Path(__file__).parent.parent

# Files to scan
SCAN_EXTENSIONS = {'.html', '.js', '.py', '.json', '.md'}
EXCLUDE_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.venv'}

# Known Gnostic mappings (variable name -> Gnostic name)
GNOSTIC_MAP = {
    "watts_constant": "The Monad",
    "reid_invariant": "The Pneuma",
    "weinstein_scale": "The Aeon",
    "hossenfelder_root": "The Nous",
    "odowd_bulk_pressure": "The Barbelo",
    "penrose_hameroff_bridge": "The Ogdoad",
    "christ_constant": "The Christos",
    "delta_jc": "The Christos",
    "sophian_drag": "The Sophian Breath",
    "demiurgic_coupling": "The Demiurgic Gear",
    "tzimtzum_pressure": "The Tzimtzum Seal",
    "b3": "The Pleroma",
    "chi_eff": "The Demiurge",
    "shadow_sector": "The Sophia",
    "roots_total": "The Ennoia",
    "visible_sector": "The Visible",
    "sterile_sector": "The Barbelo",
    "syzygy_gap": "The Syzygy",
    "horos": "The Horos",
}

# Known values that should NOT be hardcoded
HARDCODED_VALUES = {
    # Sovereign Integers
    "= 24": "B3 (The Pleroma)",
    "= 135": "shadow_sector (The Sophia)",
    "= 144": "chi_eff (The Demiurge)",
    "= 153": "christ_constant (The Christos)",
    "= 163": "sterile_sector (The Barbelo)",
    "= 288": "roots_total (The Ennoia)",
    # Other important values
    "= 125": "visible_sector (The Visible)",
    "= 18": "syzygy_gap (The Syzygy)",
    "= 26": "horos (The Horos)",
    "= 12": "weinstein_scale (The Aeon) - check context",
    "= 13": "penrose_hameroff_bridge (The Ogdoad) - check context",
}

# Deprecated/outdated variable patterns
# These are checked in HTML/JS files only (not Python source files which define values)
DEPRECATED_PATTERNS = [
    # Old variable names that should use Gnostic naming
    (r'(?<![_a-zA-Z])visible_gates(?![_a-zA-Z])', 'shadow_sector or VISIBLE_GATES'),
    (r'(?<![_a-zA-Z])shadow_gates(?![_a-zA-Z])', 'shadow_sector'),
    (r'(?<![_a-zA-Z])logic_gates(?![_a-zA-Z])', 'roots_total or LOGIC_CLOSURE'),
    (r'(?<!odowd_)bulk_pressure(?![_a-zA-Z])', 'odowd_bulk_pressure or BULK_PRESSURE'),
    (r'(?<![_a-zA-Z])sterile_count(?![_a-zA-Z])', 'sterile_sector'),
]

# Patterns only checked in consumer files (HTML/JS), not SSoT sources
CONSUMER_DEPRECATED_PATTERNS = [
    # Hardcoded counts that should come from statistics.json
    (r'\bpass_count\s*[:=]\s*\d+', 'Should use framework_statistics.pass_count from statistics.json'),
    (r'\bpending_count\s*[:=]\s*\d+', 'Should use framework_statistics.pending_count from statistics.json'),
    (r'\bnot_testable_count\s*[:=]\s*\d+', 'Should use framework_statistics.not_testable_count'),
]

# Files that define SSoT values (exclude from deprecated checks)
SSOT_SOURCE_FILES = {
    # Core SSoT generators
    'FormulasRegistry.py',
    'generate_72_certificates.py',
    'generate_statistics.py',
    'zenodo_pack_v16.py',
    # Validation/verification scripts
    'rigorous_validator_v16_1.py',
    'verify_sterility_report.py',
    'validate_variable_names.py',
    # Legacy bridges and derivations
    'legacy_bridge.py',
    'root_derivation.py',
    'add_gnostic_naming.py',
    # Config/manifest files
    'MANIFEST.json',
    'config.py',
}

# Valid parameter paths in the SSoT
VALID_PARAM_PATHS = set()

# Known JS aliases that map HTML paths to actual parameters
# These are defined in pm-constants-loader.js
# This comprehensive list ensures validation recognizes all valid aliased paths
JS_PARAMETER_ALIASES = {
    # ================================================================
    # DIMENSION PARAMETERS (map dimensions.X → geometry.X)
    # ================================================================
    'dimensions.D_bulk': 'geometry.D_bulk',
    'dimensions.d_bulk': 'geometry.D_bulk',
    'dimensions.D_after_sp2r': 'geometry.D_eff',
    'dimensions.d_after_sp2r': 'geometry.D_eff',
    'dimensions.D_observable': '_hardcoded',  # 4D spacetime
    'dimensions.d_observable': '_hardcoded',
    'dimensions.D_G2': 'geometry.D_G2',
    'dimensions.d_g2': 'geometry.D_G2',
    'dimensions.D_compact': 'geometry.D_compact',
    'dimensions.D_shadow': 'geometry.D_shadow',
    'dimensions.d_spin8': 'dimensions.D_SPIN8',
    'dimensions.bulk_signature': '_hardcoded',

    # ================================================================
    # PMNS / Neutrino mixing
    # ================================================================
    'pmns_matrix.theta_23': 'neutrino.theta_23_pred',
    'pmns_matrix.theta_12': 'neutrino.theta_12_pred',
    'pmns_matrix.theta_13': 'neutrino.theta_13_pred',
    'pmns_matrix.delta_cp': 'neutrino.delta_CP_pred',
    'parameters.pmns.theta_23': 'neutrino.theta_23_pred',
    'parameters.pmns.theta_12': 'neutrino.theta_12_pred',
    'parameters.pmns.theta_13': 'neutrino.theta_13_pred',
    'parameters.pmns.delta_CP': 'neutrino.delta_CP_pred',
    # Nested paths for neutrino (JS handles .value/.sigma_deviation internally)
    'neutrino.theta_23_pred.value': 'neutrino.theta_23_pred',
    'neutrino.theta_23_pred.sigma_deviation': '_dynamic',
    'neutrino.theta_13_pred.value': 'neutrino.theta_13_pred',
    'neutrino.theta_13_pred.sigma_deviation': '_dynamic',
    'neutrino.delta_CP_pred.value': 'neutrino.delta_CP_pred',
    'neutrino.delta_CP_pred.sigma_deviation': '_dynamic',

    # ================================================================
    # VALIDATION / FRAMEWORK STATISTICS
    # ================================================================
    'validation.calibrated_count': '_dynamic',
    'validation.constraints_count': '_dynamic',
    'validation.predictions_within_1sigma': '_dynamic',
    'validation.predictions_within_2sigma': '_dynamic',
    'validation.exact_matches': '_dynamic',
    'validation.success_rate': '_dynamic',
    'framework_statistics.within_1_sigma': '_dynamic',
    'framework_statistics.total_sm_parameters': '_dynamic',
    'framework_statistics.calibrated_parameters': '_dynamic',
    'framework_statistics.success_rate_1sigma': '_dynamic',
    'statistics.certificates_total': '_dynamic',
    'statistics.certificates_verified': '_dynamic',

    # ================================================================
    # DARK ENERGY
    # ================================================================
    'dark_energy.w0': 'cosmology.w0_derived',
    'dark_energy.w0_PM': 'cosmology.w0_derived',
    'dark_energy.w0_DESI_central': 'desi.w0',
    'dark_energy.w0_DESI_error': '_uncertainty',
    'dark_energy.w0_sigma': 'cosmology.w0_deviation',
    'parameters.dark_energy.w0': 'cosmology.w0_derived',
    'parameters.dark_energy.w0.value': 'cosmology.w0_derived',
    'parameters.dark_energy.w0.experimental.value': 'desi.w0',
    'parameters.dark_energy.w0.experimental.uncertainty': '_uncertainty',

    # ================================================================
    # HUBBLE CONSTANT / COSMOLOGY
    # ================================================================
    'cosmology.H0_local': '_hardcoded',  # 71.55 (O'Dowd formula)
    'cosmology.H0_early': 'cosmology.H0_early_normalized',
    'cosmology.H0': 'cosmology.H0_late_evolved',
    'cosmology.alpha_T': '_hardcoded',  # Tensor-to-scalar ratio
    'hubble.H0_local': 'cosmology.H0_late_evolved',
    'hubble.H0_early': 'cosmology.H0_early_normalized',
    'hubble.H0_SH0ES': 'cosmology.H0_late_evolved',
    'hubble.H0_Planck': 'cosmology.H0_early_normalized',
    'parameters.cosmology.H0': 'cosmology.H0_late_evolved',
    'parameters.cosmology.H0_local': 'cosmology.H0_late_evolved',
    'parameters.cosmology.H0_early': 'cosmology.H0_early_normalized',
    'seeds.k_gimel': 'constants.demiurgic_coupling',
    'cosmology.w0_dark_energy': 'cosmology.w0_derived',

    # ================================================================
    # GAUGE PARAMETERS
    # ================================================================
    'parameters.gauge.ALPHA_GUT_INV': 'gauge.ALPHA_GUT_INV',
    'parameters.gauge.alpha_gut_inv': 'gauge.ALPHA_GUT_INV',
    'parameters.gauge.m_ps': 'simulations.breaking_chain.m_ps',
    'parameters.gauge.M_GUT': 'gauge.M_GUT',
    'gauge_couplings.alpha_s_MZ': 'pdg.alpha_s_MZ',

    # ================================================================
    # HIGGS MASS
    # ================================================================
    'simulations.higgs_mass.m_h_GeV': 'pdg.m_higgs',
    'simulations.higgs_mass.m_h_gev': 'pdg.m_higgs',
    'simulations.higgs_mass.validation.sigma': '_dynamic',
    'higgs_mass.m_h_GeV': 'pdg.m_higgs',
    'v11_final_observables.higgs_mass.m_h_gev': 'pdg.m_higgs',
    'v11_final_observables.higgs_mass.m_h_GeV': 'pdg.m_higgs',

    # ================================================================
    # PROTON DECAY
    # ================================================================
    'simulations.proton_decay.tau_p_years': 'proton_decay.tau_p_years',
    'simulations.proton_decay.alpha_gut_inv': 'gauge.ALPHA_GUT_INV',
    'simulations.proton_decay.m_gut': 'gauge.M_GUT',
    'proton_decay.tau_p_years': 'proton_decay.tau_p_years',
    'proton_decay.alpha_GUT_inv': 'gauge.ALPHA_GUT_INV',
    'proton_decay.m_gut': 'gauge.M_GUT',
    'parameters.proton_decay.BR_epi0': '_hardcoded',

    # ================================================================
    # KK GRAVITON
    # ================================================================
    'simulations.kk_graviton.m_KK_TeV': '_hardcoded',
    'simulations.kk_graviton.hl_lhc_discovery': '_hardcoded',
    'kk_spectrum.m1': '_hardcoded',
    'kk_spectrum.m1_central': '_hardcoded',
    'kk_spectrum.m1_TeV': '_hardcoded',
    'kk_spectrum.hl_lhc_significance': '_hardcoded',
    'kk_graviton.mass_tev': '_hardcoded',

    # ================================================================
    # NEUTRINO MASSES
    # ================================================================
    'neutrino_mass.delta_m_sq': 'neutrino.dm2_21',
    'neutrino_masses.delta_m21_sq': 'neutrino.dm2_21',
    'neutrino_masses.delta_m3l_sq': 'neutrino.dm2_32',
    'simulations.neutrino_masses.delta_m21_sq': 'neutrino.dm2_21',
    'simulations.neutrino_masses.delta_m3l_sq': 'neutrino.dm2_32',

    # ================================================================
    # ELECTROWEAK / VEV
    # ================================================================
    'electroweak.v_higgs': 'higgs.vev',
    'parameters.electroweak.v_higgs': 'higgs.vev',
    'parameters.electroweak.v_higgs.value': 'geometry.higgs_vev',
    'v12_6_geometric_derivations.vev_pneuma.v_ew': 'higgs.vev',

    # ================================================================
    # FITTED PARAMETERS
    # ================================================================
    'fitted_parameters.shadow_kuf': '_dynamic',
    'fitted_parameters.shadow_chet': '_dynamic',  # Typo alias for shadow_kuf

    # ================================================================
    # TOPOLOGY (map legacy names to SSoT names)
    # ================================================================
    'topology.roots_total': '_named.roots',
    'topology.sterile_sector': '_named.sterile',
    'topology.shadow_sector': '_named.shadow_sector',
    'topology.visible_sector': '_named.visible',
    'topology.b3': '_named.b3',
    'topology.chi_eff': '_named.chi_eff',
    'topology.roots': '_named.roots',
    'topology.visible': '_named.visible',
    'topology.sterile': '_named.sterile',
    'topology.n_gen': '_hardcoded',  # 3 fermion generations
    'parameters.topology.roots_total': '_named.roots',
    'parameters.topology.sterile_sector': '_named.sterile',
    'parameters.topology.b2': '_named.b3',
    'parameters.topology.b3': '_named.b3',
    'parameters.topology.B2': '_named.b3',
    'parameters.topology.B3': '_named.b3',
    'parameters.topology.h11': 'parameters.topology.HODGE_H11',
    'parameters.topology.h21': 'parameters.topology.HODGE_H21',
    'parameters.topology.h31': 'parameters.topology.HODGE_H31',
    'parameters.topology.nu': '_hardcoded',  # alias for n_gen
    'parameters.topology.CHI_EFF': '_named.chi_eff',
    'parameters.topology.n_gen': '_hardcoded',

    # ================================================================
    # SACRED HEPTAGON CONSTANTS (from named_constants.json)
    # ================================================================
    'constants.watts_constant': '_named',
    'constants.omega_W': '_named',
    'constants.reid_invariant': '_named',
    'constants.chi_R': '_named',
    'constants.weinstein_scale': '_named',
    'constants.kappa_E': '_named',
    'constants.hossenfelder_root': '_named',
    'constants.hossenfelder_constant': '_named',
    'constants.lambda_S': '_named',
    'constants.odowd_bulk_pressure': '_named',
    'constants.odowd_constant': '_named',
    'constants.P_O': '_named',
    'constants.penrose_hameroff_bridge': '_named',
    'constants.penrose_hameroff': '_named',
    'constants.phi_PH': '_named',
    'constants.christ_constant': '_named',
    'constants.lambda_JC': '_named',
    'constants.phi': '_hardcoded',  # Golden ratio

    # ================================================================
    # MECHANICAL TRIAD CONSTANTS
    # ================================================================
    'constants.sophian_drag': '_named',
    'constants.eta_S': '_named',
    'cosmology.eta_S': '_named',
    'constants.demiurgic_coupling': '_named',
    'constants.kappa_Delta': '_named',
    'constants.k_gimel': '_named',
    'constants.tzimtzum_pressure': '_named',
    'constants.sigma_T': '_named',
    'cosmology.sigma_T': '_named',
    'cosmology.w0_magnitude': '_named',

    # ================================================================
    # DERIVED VALUES
    # ================================================================
    'derived.hubble_constant': '_named',
    'derived.dark_energy_w0': '_named',
    'derived.parity_product': '_named',

    # ================================================================
    # QED CONSTANTS
    # ================================================================
    'qed.alpha_inverse': '_named.alpha_inverse',

    # ================================================================
    # HEPTAGON ALIASES
    # ================================================================
    'heptagon.watts_constant': '_named',
    'heptagon.reid_invariant': '_named',
    'heptagon.weinstein_scale': '_named',
    'heptagon.hossenfelder_root': '_named',
    'heptagon.odowd_bulk_pressure': '_named',
    'heptagon.penrose_hameroff_bridge': '_named',
    'heptagon.christ_constant': '_named',
    'mechanical.sophian_drag': '_named',
    'mechanical.demiurgic_coupling': '_named',
    'mechanical.tzimtzum_pressure': '_named',
}

def load_ssot_params():
    """Load valid parameter paths from SSoT files."""
    global VALID_PARAM_PATHS

    # Add all known aliases as valid paths
    VALID_PARAM_PATHS.update(JS_PARAMETER_ALIASES.keys())

    # Load from parameters.json
    params_file = PROJECT_ROOT / "AutoGenerated" / "parameters.json"
    if params_file.exists():
        with open(params_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'parameters' in data:
                VALID_PARAM_PATHS.update(data['parameters'].keys())

    # Load from named_constants.json
    constants_file = PROJECT_ROOT / "AutoGenerated" / "named_constants.json"
    if constants_file.exists():
        with open(constants_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'constants' in data:
                for key, val in data['constants'].items():
                    if 'pm_path' in val:
                        VALID_PARAM_PATHS.add(val['pm_path'])
                    VALID_PARAM_PATHS.add(f"constants.{key}")

def scan_file(filepath: Path) -> List[Tuple[int, str, str]]:
    """Scan a file for issues. Returns list of (line_num, issue_type, message)."""
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [(0, 'ERROR', f"Could not read file: {e}")]

    # Check if this is an SSoT source file (exclude from deprecated checks)
    is_ssot_source = filepath.name in SSOT_SOURCE_FILES

    for line_num, line in enumerate(lines, 1):
        # Skip comments in Python files
        stripped = line.strip()
        if filepath.suffix == '.py' and stripped.startswith('#'):
            continue

        # Check deprecated patterns (only in non-SSoT files)
        if not is_ssot_source:
            for pattern, suggestion in DEPRECATED_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append((line_num, 'DEPRECATED', f"Found deprecated pattern. Use: {suggestion}"))

            # Check consumer-only patterns (HTML/JS files)
            if filepath.suffix in {'.js', '.html'}:
                for pattern, suggestion in CONSUMER_DEPRECATED_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append((line_num, 'DEPRECATED', f"Found deprecated pattern. Use: {suggestion}"))

        # Check for hardcoded sovereign integers in JS/HTML (not in Python SSoT)
        if filepath.suffix in {'.js', '.html'}:
            for hardcoded, should_be in HARDCODED_VALUES.items():
                if hardcoded in line:
                    # Check if it's not in a comment or string literal that's OK
                    if not re.search(r'//.*' + re.escape(hardcoded), line):
                        if not re.search(r'data-pm-value', line):  # Allow data attributes
                            issues.append((line_num, 'HARDCODED', f"Hardcoded value {hardcoded} found. Consider using: {should_be}"))

        # Check for data-pm-value with invalid paths in HTML
        if filepath.suffix == '.html':
            matches = re.findall(r'data-pm-value=["\']([^"\']+)["\']', line)
            for match in matches:
                if match not in VALID_PARAM_PATHS and not match.startswith('framework_statistics.'):
                    # Check if it's a simple constant name
                    if '.' not in match and match not in GNOSTIC_MAP:
                        issues.append((line_num, 'INVALID_PATH', f"data-pm-value='{match}' may be invalid"))

    return issues

def scan_project() -> Dict[str, List[Tuple[int, str, str]]]:
    """Scan entire project for issues."""
    all_issues = {}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for filename in files:
            filepath = Path(root) / filename

            # Skip non-scannable files
            if filepath.suffix not in SCAN_EXTENSIONS:
                continue

            # Skip AutoGenerated JSON files (they're the source, not consumers)
            if 'AutoGenerated' in str(filepath) and filepath.suffix == '.json':
                continue

            issues = scan_file(filepath)
            if issues:
                rel_path = filepath.relative_to(PROJECT_ROOT)
                all_issues[str(rel_path)] = issues

    return all_issues

def check_html_param_references():
    """Check all HTML files for invalid parameter references."""
    issues = []

    for html_file in PROJECT_ROOT.glob("**/*.html"):
        if 'node_modules' in str(html_file):
            continue

        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find all data-pm-value attributes
        for match in re.finditer(r'data-pm-value=["\']([^"\']+)["\']', content):
            param_path = match.group(1)
            line_num = content[:match.start()].count('\n') + 1

            # Check if param path is valid
            if param_path not in VALID_PARAM_PATHS:
                # Allow framework_statistics.* paths
                if not param_path.startswith('framework_statistics.'):
                    rel_path = html_file.relative_to(PROJECT_ROOT)
                    issues.append((str(rel_path), line_num, param_path))

    return issues

def main():
    print("=" * 70)
    print("VARIABLE NAME VALIDATION SCRIPT")
    print("=" * 70)

    # Load SSoT parameters
    print("\n[1] Loading SSoT parameter paths...")
    load_ssot_params()
    print(f"    Loaded {len(VALID_PARAM_PATHS)} valid parameter paths")

    # Scan project
    print("\n[2] Scanning project for issues...")
    all_issues = scan_project()

    # Separate critical errors from advisory warnings
    critical_errors = 0
    warnings = 0

    for filepath, issues in all_issues.items():
        for line_num, issue_type, message in issues:
            if issue_type in {'INVALID_PATH', 'ERROR'}:
                critical_errors += 1
            elif issue_type == 'DEPRECATED':
                # DEPRECATED in validation script itself is expected (self-referential)
                if 'validate_variable_names.py' not in filepath:
                    critical_errors += 1
                else:
                    warnings += 1
            else:  # HARDCODED is advisory
                warnings += 1

    total_issues = critical_errors + warnings

    if total_issues == 0:
        print("\n[OK] No issues found!")
    else:
        print(f"\n[!] Found {critical_errors} error(s) and {warnings} warning(s) in {len(all_issues)} file(s):")

        for filepath, issues in sorted(all_issues.items()):
            print(f"\n  {filepath}:")
            for line_num, issue_type, message in issues:
                print(f"    Line {line_num} [{issue_type}]: {message}")

    # Check HTML parameter references
    print("\n[3] Checking HTML parameter references...")
    html_issues = check_html_param_references()

    if not html_issues:
        print("    [OK] All HTML data-pm-value references are valid")
    else:
        critical_errors += len(html_issues)
        print(f"    [!] Found {len(html_issues)} invalid parameter reference(s):")
        for filepath, line_num, param_path in html_issues:
            print(f"      {filepath}:{line_num} - Invalid: {param_path}")

    print("\n" + "=" * 70)

    # Return exit code - only fail on critical errors, not warnings
    if critical_errors > 0:
        print(f"VALIDATION FAILED - {critical_errors} critical error(s), {warnings} warning(s)")
        return 1
    elif warnings > 0:
        print(f"VALIDATION PASSED WITH WARNINGS - {warnings} advisory warning(s)")
        print("(Hardcoded sovereign integers in formulas are expected)")
        return 0
    else:
        print("VALIDATION PASSED")
        return 0

if __name__ == "__main__":
    exit(main())
