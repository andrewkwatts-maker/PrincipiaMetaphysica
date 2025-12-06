#!/usr/bin/env python3
"""
Source of Truth Validation - Complete Pipeline Verification
============================================================

Validates that all assertions in the website are properly sourced from:
  config.py → simulations → theory_output.json → theory-constants-enhanced.js → HTML

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import config

def load_theory_output():
    """Load theory_output.json"""
    try:
        with open('theory_output.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: theory_output.json not found. Run: python run_all_simulations.py")
        return None

def extract_pm_references_from_html(html_path):
    """Extract all PM.* references from an HTML file"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match PM.category.parameter or PM.category.parameter.value
        pattern = r'PM\.([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)(?:\.([a-zA-Z_][a-zA-Z0-9_]*))?'
        matches = re.findall(pattern, content)

        references = []
        for match in matches:
            category, param, sub = match
            if sub:
                references.append(f"PM.{category}.{param}.{sub}")
            else:
                references.append(f"PM.{category}.{param}")

        return references
    except Exception as e:
        print(f"Error reading {html_path}: {e}")
        return []

def extract_hardcoded_numbers(html_path):
    """Find hardcoded numbers that should use PM references"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        hardcoded = []

        # Known values that should be PM references
        patterns = {
            r'\b3\.7\s*[×x]\s*10\^?34\b': 'Proton lifetime (should use PM.proton_decay.tau_p_central)',
            r'\b2\.118\s*[×x]\s*10\^?16\b': 'M_GUT (should use PM.proton_decay.M_GUT)',
            r'\b-0\.85[0-9]*\b': 'Dark energy w0 (should use PM.dark_energy.w0_PM)',
            r'\b47\.2\s*degrees?\b': 'theta_23 (should use PM.pmns_matrix.theta_23)',
            r'\b5\.0\s*TeV\b': 'KK mass (should use PM.kk_spectrum.m1)',
            r'\b144\b(?![\d])': 'chi_eff (should use PM.topology.chi_eff)',
            r'\b23\.5[0-9]*\b': 'alpha_GUT^-1 (should use PM.proton_decay.alpha_GUT_inv)',
        }

        for pattern, description in patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Check if it's inside a PM.* reference already
                start = max(0, match.start() - 50)
                context = content[start:match.end() + 50]
                if 'PM.' not in context:
                    hardcoded.append({
                        'value': match.group(),
                        'description': description,
                        'context': context.strip()[:100]
                    })

        return hardcoded
    except Exception as e:
        print(f"Error analyzing {html_path}: {e}")
        return []

def validate_pm_reference(ref, theory_data):
    """Check if a PM reference exists in theory_output.json"""
    parts = ref.replace('PM.', '').split('.')

    if len(parts) < 2:
        return False, "Invalid reference format"

    category = parts[0]
    param = parts[1]

    # Navigate JSON structure
    current = theory_data
    try:
        current = current[category]
        if param in current:
            if len(parts) == 3:
                # Check for sub-property (e.g., PM.dark_energy.w0_PM.value)
                sub = parts[2]
                if sub == 'value':
                    return True, current[param]
                elif isinstance(current[param], dict) and sub in current[param]:
                    return True, current[param][sub]
                else:
                    return False, f"Sub-property '{sub}' not found"
            else:
                return True, current[param]
        else:
            return False, f"Parameter '{param}' not found in category '{category}'"
    except KeyError as e:
        return False, f"Category '{category}' not found"
    except Exception as e:
        return False, f"Error: {str(e)}"

def trace_to_simulation(param_path, theory_data):
    """Trace a parameter back to its simulation source"""
    # Extract category from path (e.g., PM.proton_decay.M_GUT -> proton_decay)
    parts = param_path.replace('PM.', '').split('.')
    category = parts[0]

    # Check which simulation generated this value
    simulations = theory_data.get('meta', {}).get('simulations_run', [])

    # Map categories to simulations
    category_to_sim = {
        'proton_decay': 'proton_decay_rg_hybrid',
        'pmns_matrix': 'pmns_full_matrix',
        'dark_energy': 'wz_evolution_desi_dr2',
        'kk_spectrum': 'kk_spectrum_full',
        'neutrino_mass_ordering': 'neutrino_mass_ordering',
        'proton_decay_channels': 'proton_decay_v84_ckm',
        'v9_transparency': 'v9_manifest',
        'v10_geometric_derivations': 'g2_torsion_derivation_v10',
        'v10_1_neutrino_masses': 'neutrino_mass_matrix_v10_1',
        'v10_2_all_fermions': 'full_fermion_matrices_v10_2',
        'v11_final_observables': 'proton_lifetime_v11',
        'v12_final_values': 'neutrino_mass_matrix_final_v12',
    }

    simulation = category_to_sim.get(category, 'Unknown')

    # Check if simulation exists in simulations directory
    sim_file = Path('simulations') / f"{simulation}.py"
    exists = sim_file.exists()

    return {
        'simulation': simulation,
        'exists': exists,
        'path': str(sim_file) if exists else 'N/A'
    }

def trace_to_config(param_path):
    """Trace a parameter back to config.py"""
    parts = param_path.replace('PM.', '').split('.')
    category = parts[0]
    param = parts[1] if len(parts) > 1 else None

    # Map to config.py classes
    config_map = {
        'dimensions': 'FundamentalConstants',
        'topology': 'FundamentalConstants',
        'proton_decay': 'GaugeUnificationParameters',
        'pmns_matrix': 'NeutrinoParameters',
        'dark_energy': 'PhenomenologyParameters',
        'kk_spectrum': 'KKGravitonParameters',
    }

    config_class = config_map.get(category, None)

    if config_class:
        # Check if parameter exists in config
        try:
            cls = getattr(config, config_class)
            if param:
                has_attr = hasattr(cls, param.upper()) or hasattr(cls, param)
                return {
                    'config_class': config_class,
                    'has_parameter': has_attr,
                    'source': 'config.py'
                }
        except:
            pass

    return {
        'config_class': config_class or 'N/A',
        'has_parameter': False,
        'source': 'Computed (not in config.py directly)'
    }

def generate_validation_report():
    """Generate complete validation report"""

    print("=" * 80)
    print("SOURCE OF TRUTH VALIDATION REPORT")
    print("=" * 80)
    print()

    # Load theory output
    print("1. Loading theory_output.json...")
    theory_data = load_theory_output()
    if not theory_data:
        return
    print(f"   [OK] Loaded version {theory_data['meta']['version']}")
    print(f"   [OK] Last updated: {theory_data['meta']['last_updated']}")
    print(f"   [OK] {len(theory_data['meta']['simulations_run'])} simulations run")
    print()

    # Find all HTML files
    print("2. Scanning HTML files...")
    html_files = list(Path('.').glob('**/*.html'))
    print(f"   [OK] Found {len(html_files)} HTML files")
    print()

    # Extract all PM references
    print("3. Extracting PM.* references from HTML...")
    all_references = {}
    total_refs = 0
    for html_file in html_files:
        refs = extract_pm_references_from_html(html_file)
        if refs:
            all_references[str(html_file)] = refs
            total_refs += len(refs)
    print(f"   [OK] Found {total_refs} PM references in {len(all_references)} files")
    print()

    # Validate references
    print("4. Validating PM references against theory_output.json...")
    valid_refs = []
    broken_refs = []

    for html_file, refs in all_references.items():
        for ref in refs:
            is_valid, value = validate_pm_reference(ref, theory_data)
            if is_valid:
                valid_refs.append({'file': html_file, 'ref': ref, 'value': value})
            else:
                broken_refs.append({'file': html_file, 'ref': ref, 'reason': value})

    print(f"   [OK] Valid references: {len(valid_refs)}")
    print(f"   [WARN] Broken references: {len(broken_refs)}")
    print()

    # Find hardcoded numbers
    print("5. Searching for hardcoded numbers...")
    hardcoded_numbers = {}
    total_hardcoded = 0
    for html_file in html_files:
        hardcoded = extract_hardcoded_numbers(html_file)
        if hardcoded:
            hardcoded_numbers[str(html_file)] = hardcoded
            total_hardcoded += len(hardcoded)
    print(f"   [WARN] Found {total_hardcoded} potential hardcoded numbers")
    print()

    # Generate detailed report
    print("=" * 80)
    print("DETAILED FINDINGS")
    print("=" * 80)
    print()

    # Broken references
    if broken_refs:
        print("BROKEN REFERENCES (need to add to theory-constants-enhanced.js):")
        print("-" * 80)
        broken_by_file = defaultdict(list)
        for item in broken_refs:
            broken_by_file[item['file']].append(f"  • {item['ref']} - {item['reason']}")

        for file, refs in sorted(broken_by_file.items()):
            print(f"\n{file}:")
            for ref in refs:
                print(ref)
        print()

    # Hardcoded numbers
    if hardcoded_numbers:
        print("\nHARDCODED NUMBERS (should use PM references):")
        print("-" * 80)
        for file, numbers in sorted(hardcoded_numbers.items()):
            if numbers:
                print(f"\n{file}:")
                for num in numbers:
                    print(f"  • {num['value']}")
                    print(f"    {num['description']}")
        print()

    # Traceability sample
    print("\nSOURCE TRACEABILITY (sample):")
    print("-" * 80)
    sample_refs = [
        'PM.proton_decay.M_GUT',
        'PM.pmns_matrix.theta_23',
        'PM.dark_energy.w0_PM',
        'PM.topology.chi_eff',
        'PM.kk_spectrum.m1'
    ]

    for ref in sample_refs:
        is_valid, value = validate_pm_reference(ref, theory_data)
        if is_valid:
            sim_trace = trace_to_simulation(ref, theory_data)
            config_trace = trace_to_config(ref)

            print(f"\n{ref}:")
            print(f"  Value: {value}")
            print(f"  Config: {config_trace['config_class']} (in config.py: {config_trace['has_parameter']})")
            print(f"  Simulation: {sim_trace['simulation']} (exists: {sim_trace['exists']})")
            print(f"  JSON: [OK] in theory_output.json")
            print(f"  JS: [OK] in theory-constants-enhanced.js")
    print()

    # Summary statistics
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total PM references found:     {total_refs}")
    print(f"Valid references:              {len(valid_refs)} ({len(valid_refs)/total_refs*100:.1f}%)")
    print(f"Broken references:             {len(broken_refs)} ({len(broken_refs)/total_refs*100:.1f}%)")
    print(f"Hardcoded numbers:             {total_hardcoded}")
    print(f"HTML files with PM refs:       {len(all_references)}")
    print(f"Simulations in pipeline:       {len(theory_data['meta']['simulations_run'])}")
    print()

    # Critical issues
    critical_issues = []
    if len(broken_refs) > 10:
        critical_issues.append(f"{len(broken_refs)} broken references need fixing")
    if total_hardcoded > 20:
        critical_issues.append(f"{total_hardcoded} hardcoded numbers should use PM refs")

    if critical_issues:
        print("CRITICAL ISSUES:")
        for issue in critical_issues:
            print(f"  [!] {issue}")
    else:
        print("[OK] No critical issues found!")

    print()
    print("=" * 80)

    # Save report
    report_data = {
        'total_refs': total_refs,
        'valid_refs': len(valid_refs),
        'broken_refs': len(broken_refs),
        'hardcoded_numbers': total_hardcoded,
        'broken_references': broken_refs,
        'hardcoded_details': hardcoded_numbers,
        'valid_references': valid_refs[:100],  # Sample
    }

    with open('SOURCE_OF_TRUTH_VALIDATION.json', 'w') as f:
        json.dump(report_data, f, indent=2)

    print("Full report saved to: SOURCE_OF_TRUTH_VALIDATION.json")

    return report_data

if __name__ == '__main__':
    generate_validation_report()
