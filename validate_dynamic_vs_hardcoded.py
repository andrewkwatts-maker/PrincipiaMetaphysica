#!/usr/bin/env python3
"""
Validation script to compare dynamic content from theory_output.json
against hardcoded values in HTML files.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# Key predictions to track
KEY_PREDICTIONS = {
    'proton_lifetime': {
        'json_path': ['simulations', 'proton_decay', 'tau_p_years'],
        'expected': 8.15e34,
        'pattern': r'8\.1[45]\s*[×x]\s*10\s*[³³⁴4]\s*[⁴4]|8\.1[45]e[+]?34',
        'unit': 'years'
    },
    'dark_energy_w0': {
        'json_path': ['parameters', 'dark_energy', 'w0'],
        'expected': -0.8528,
        'pattern': r'-0\.852[0-9]|w[_₀0]\s*=\s*-0\.85',
        'unit': ''
    },
    'theta_23': {
        'json_path': ['parameters', 'neutrino', 'pmns_angles', 'theta_23', 'predicted'],
        'expected': 45.0,
        'pattern': r'θ[_₂2][_₃3]\s*=\s*45°?|theta[_]?23\s*=\s*45',
        'unit': 'degrees'
    },
    'm_gut': {
        'json_path': ['simulations', 'proton_decay', 'm_gut'],
        'expected': 2.118e16,
        'pattern': r'2\.11[0-9]\s*[×x]\s*10\s*[¹1][⁶6]|2\.11[0-9]e[+]?16|M[_]?GUT.*2\.11',
        'unit': 'GeV'
    },
    'kk_mass': {
        'json_path': ['simulations', 'kk_spectrum_v14_2', 'm_kk_tev'],
        'expected': 5.0,  # Target is 5.0 TeV
        'pattern': r'[45]\.[0-9]+\s*TeV|m[_]?KK.*[45]\.[0-9]',
        'unit': 'TeV'
    },
    'generation_count': {
        'json_path': ['simulations', 'zero_modes_v12_8', 'n_gen'],
        'expected': 3,
        'pattern': r'(?:n|N)[_]?(?:gen|generations?)\s*=\s*3|three\s+generations|3\s+fermion\s+generations',
        'unit': ''
    }
}

class ValidationReport:
    def __init__(self):
        self.matches = []
        self.mismatches = []
        self.hardcoded_only = []
        self.json_only = []
        self.json_values = {}

    def load_json_values(self, json_path):
        """Load theory_output.json and extract key values."""
        with open(json_path, 'r') as f:
            data = json.load(f)

        for key, config in KEY_PREDICTIONS.items():
            path = config['json_path']
            value = data
            try:
                for p in path:
                    value = value[p]
                self.json_values[key] = value
                print(f"✓ Found {key}: {value} {config['unit']}")
            except (KeyError, TypeError):
                print(f"✗ Missing {key} in JSON")
                self.json_values[key] = None
                self.json_only.append({
                    'key': key,
                    'expected': config['expected'],
                    'reason': 'Value defined in JSON but path not found'
                })

    def scan_html_file(self, filepath):
        """Scan an HTML file for hardcoded values."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return

        lines = content.split('\n')

        for key, config in KEY_PREDICTIONS.items():
            pattern = config['pattern']
            json_value = self.json_values.get(key)
            expected = config['expected']

            for i, line in enumerate(lines, 1):
                # Skip comments
                if '<!--' in line:
                    continue

                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    matched_text = match.group(0)

                    # Extract numerical value from matched text
                    hardcoded_value = self.extract_number(matched_text, key)

                    if json_value is not None:
                        # Compare with JSON value
                        if self.values_match(hardcoded_value, json_value, key):
                            self.matches.append({
                                'file': str(filepath),
                                'line': i,
                                'key': key,
                                'value': matched_text,
                                'json_value': json_value
                            })
                        else:
                            self.mismatches.append({
                                'file': str(filepath),
                                'line': i,
                                'key': key,
                                'hardcoded': matched_text,
                                'hardcoded_number': hardcoded_value,
                                'json_value': json_value,
                                'difference': self.calculate_difference(hardcoded_value, json_value)
                            })
                    else:
                        # Found in HTML but not in JSON
                        self.hardcoded_only.append({
                            'file': str(filepath),
                            'line': i,
                            'key': key,
                            'value': matched_text
                        })

    def extract_number(self, text, key):
        """Extract numerical value from matched text."""
        # Remove HTML entities and unicode
        text = text.replace('&times;', 'x').replace('×', 'x')

        # Handle different formats
        if key == 'proton_lifetime':
            # Look for 8.15 × 10^34
            match = re.search(r'8\.1[45]\d*', text)
            if match:
                base = float(match.group(0))
                return base * 1e34

        elif key == 'dark_energy_w0':
            match = re.search(r'-0\.85\d+', text)
            if match:
                return float(match.group(0))

        elif key == 'theta_23':
            match = re.search(r'45\.?\d*', text)
            if match:
                return float(match.group(0))

        elif key == 'm_gut':
            match = re.search(r'2\.11\d*', text)
            if match:
                base = float(match.group(0))
                return base * 1e16

        elif key == 'kk_mass':
            match = re.search(r'[45]\.\d+', text)
            if match:
                return float(match.group(0))

        elif key == 'generation_count':
            return 3

        return None

    def values_match(self, hardcoded, json_val, key):
        """Check if values match within tolerance."""
        if hardcoded is None:
            return False

        if key == 'generation_count':
            return hardcoded == json_val

        # For floating point, allow small differences
        if isinstance(json_val, float):
            tolerance = abs(json_val * 0.01)  # 1% tolerance
            return abs(hardcoded - json_val) <= tolerance

        return hardcoded == json_val

    def calculate_difference(self, hardcoded, json_val):
        """Calculate percentage difference."""
        if hardcoded is None or json_val is None:
            return None
        try:
            return abs((hardcoded - json_val) / json_val * 100)
        except:
            return None

    def generate_report(self, output_path):
        """Generate markdown report."""
        report = []
        report.append("# Dynamic vs Hardcoded Content Validation Report\n")
        report.append(f"**Generated:** 2025-12-25\n")
        report.append(f"**Source:** theory_output.json vs HTML section files\n\n")

        # Summary
        report.append("## Executive Summary\n")
        report.append(f"- ✓ **Matches:** {len(self.matches)}\n")
        report.append(f"- ⚠ **Mismatches:** {len(self.mismatches)}\n")
        report.append(f"- 📝 **Hardcoded only:** {len(self.hardcoded_only)}\n")
        report.append(f"- 🔍 **JSON only:** {len(self.json_only)}\n\n")

        # Key predictions summary
        report.append("## Key Predictions from JSON\n")
        report.append("| Prediction | JSON Value | Expected | Unit |\n")
        report.append("|------------|------------|----------|------|\n")
        for key, value in self.json_values.items():
            config = KEY_PREDICTIONS[key]
            expected = config['expected']
            unit = config['unit']
            if value is not None:
                report.append(f"| {key} | {value:.4g} | {expected:.4g} | {unit} |\n")
            else:
                report.append(f"| {key} | NOT FOUND | {expected:.4g} | {unit} |\n")
        report.append("\n")

        # Matches
        if self.matches:
            report.append("## ✓ Matching Values (Good)\n")
            report.append("These hardcoded values match the JSON values correctly:\n\n")

            by_key = defaultdict(list)
            for match in self.matches:
                by_key[match['key']].append(match)

            for key in sorted(by_key.keys()):
                report.append(f"### {key}\n")
                for match in by_key[key]:
                    filepath = Path(match['file']).relative_to(Path('H:/Github/PrincipiaMetaphysica'))
                    report.append(f"- `{filepath}:{match['line']}` - `{match['value']}`\n")
                report.append("\n")

        # Mismatches
        if self.mismatches:
            report.append("## ⚠ Mismatches (Need Fixing)\n")
            report.append("These hardcoded values differ from JSON values:\n\n")

            by_key = defaultdict(list)
            for mismatch in self.mismatches:
                by_key[mismatch['key']].append(mismatch)

            for key in sorted(by_key.keys()):
                report.append(f"### {key}\n")
                report.append("| File:Line | Hardcoded | JSON Value | Difference |\n")
                report.append("|-----------|-----------|------------|------------|\n")
                for mm in by_key[key]:
                    filepath = Path(mm['file']).relative_to(Path('H:/Github/PrincipiaMetaphysica'))
                    hardcoded = mm['hardcoded']
                    json_val = mm['json_value']
                    diff = mm['difference']
                    if diff is not None:
                        report.append(f"| `{filepath}:{mm['line']}` | `{hardcoded}` | {json_val:.4g} | {diff:.2f}% |\n")
                    else:
                        report.append(f"| `{filepath}:{mm['line']}` | `{hardcoded}` | {json_val} | N/A |\n")
                report.append("\n")

        # Hardcoded only
        if self.hardcoded_only:
            report.append("## 📝 Hardcoded Values Not in JSON (Need Migration)\n")
            report.append("These values are hardcoded in HTML but not found in JSON:\n\n")

            by_key = defaultdict(list)
            for item in self.hardcoded_only:
                by_key[item['key']].append(item)

            for key in sorted(by_key.keys()):
                report.append(f"### {key}\n")
                for item in by_key[key]:
                    filepath = Path(item['file']).relative_to(Path('H:/Github/PrincipiaMetaphysica'))
                    report.append(f"- `{filepath}:{item['line']}` - `{item['value']}`\n")
                report.append("\n")

        # JSON only
        if self.json_only:
            report.append("## 🔍 JSON Values Not in HTML (Coverage Gap)\n")
            report.append("These values exist in JSON but are not used in HTML:\n\n")

            for item in self.json_only:
                report.append(f"### {item['key']}\n")
                report.append(f"Expected value: {item['expected']}\n")
                report.append(f"Reason: {item['reason']}\n\n")

        # Recommendations
        report.append("## Recommendations\n\n")
        if self.mismatches:
            report.append("### High Priority\n")
            report.append("1. **Fix mismatches:** Update hardcoded values in HTML to match JSON values\n")
            report.append("2. **Use dynamic loading:** Replace hardcoded values with data-formula or data-param attributes\n\n")

        if self.hardcoded_only:
            report.append("### Medium Priority\n")
            report.append("3. **Migrate hardcoded values:** Move remaining hardcoded values to theory_output.json\n")
            report.append("4. **Add validation:** Ensure all predictions are in JSON and loaded dynamically\n\n")

        report.append("### Best Practices\n")
        report.append("- Use `data-formula=\"FORMULA_ID\"` for equations\n")
        report.append("- Use `data-param=\"param.path\"` for numerical values\n")
        report.append("- Use `<span class=\"pm-value\" data-source=\"simulations.name.field\"></span>` for predictions\n")
        report.append("- Avoid hardcoding numerical values in HTML content\n\n")

        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(report))

        print(f"\n✓ Report written to {output_path}")

def main():
    """Main validation routine."""
    base_path = Path('H:/Github/PrincipiaMetaphysica')
    json_path = base_path / 'theory_output.json'
    sections_path = base_path / 'sections'
    report_path = base_path / 'reports' / 'DYNAMIC_VS_HARDCODED_VALIDATION.md'

    print("=" * 70)
    print("Dynamic vs Hardcoded Content Validation")
    print("=" * 70)
    print()

    # Create report
    report = ValidationReport()

    # Load JSON values
    print("Loading theory_output.json...")
    report.load_json_values(json_path)
    print()

    # Scan HTML files
    print("Scanning HTML section files...")
    html_files = list(sections_path.glob('*.html'))

    for i, filepath in enumerate(html_files, 1):
        print(f"[{i}/{len(html_files)}] Scanning {filepath.name}...")
        report.scan_html_file(filepath)

    print()

    # Generate report
    print("Generating validation report...")
    report.generate_report(report_path)

    print()
    print("=" * 70)
    print("Validation Summary:")
    print(f"  Matches:        {len(report.matches)}")
    print(f"  Mismatches:     {len(report.mismatches)}")
    print(f"  Hardcoded only: {len(report.hardcoded_only)}")
    print(f"  JSON only:      {len(report.json_only)}")
    print("=" * 70)

if __name__ == '__main__':
    main()
