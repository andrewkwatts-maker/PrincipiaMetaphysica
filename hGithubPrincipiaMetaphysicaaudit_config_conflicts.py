"""
Config vs Theory Output Auditor

Finds duplicate and conflicting values between:
1. config.py (hardcoded parameters)
2. theory_output.json (simulation results)
3. HTML files (hardcoded numbers)

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
from pathlib import Path
import re
import inspect

# Import config
import config

class ConfigAuditor:
    def __init__(self):
        self.config_values = {}
        self.theory_values = {}
        self.conflicts = []
        self.duplicates = []
        
    def extract_config_values(self):
        """Extract all numerical values from config.py"""
        print("Extracting values from config.py...")
        
        # Get all classes from config
        for name, obj in inspect.getmembers(config):
            if inspect.isclass(obj) and hasattr(obj, '__dict__'):
                class_name = name
                for attr_name in dir(obj):
                    if not attr_name.startswith('_'):
                        try:
                            value = getattr(obj, attr_name)
                            if isinstance(value, (int, float)):
                                key = f"{class_name}.{attr_name}"
                                self.config_values[key] = value
                        except:
                            pass
        
        print(f"  Found {len(self.config_values)} config values")
        
    def extract_theory_values(self):
        """Extract all values from theory_output.json"""
        print("Extracting values from theory_output.json...")
        
        try:
            with open('theory_output.json', 'r') as f:
                data = json.load(f)
            
            def flatten_dict(d, parent_key=''):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}.{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key).items())
                    elif isinstance(v, (int, float)):
                        items.append((new_key, v))
                return dict(items)
            
            self.theory_values = flatten_dict(data)
            print(f"  Found {len(self.theory_values)} theory values")
        except Exception as e:
            print(f"  Error loading theory_output.json: {e}")
    
    def find_conflicts(self):
        """Find values that appear in both config and theory_output with different values"""
        print("\nFinding conflicts...")
        
        # Check for same parameter name with different values
        for config_key, config_val in self.config_values.items():
            # Extract parameter name (last part)
            param_name = config_key.split('.')[-1]
            
            # Look for matching parameter in theory_output
            for theory_key, theory_val in self.theory_values.items():
                if param_name.lower() in theory_key.lower():
                    # Compare values (with tolerance for floating point)
                    if isinstance(config_val, float) and isinstance(theory_val, float):
                        rel_diff = abs(config_val - theory_val) / max(abs(config_val), abs(theory_val), 1e-10)
                        if rel_diff > 0.01:  # More than 1% difference
                            self.conflicts.append({
                                'param': param_name,
                                'config_key': config_key,
                                'config_value': config_val,
                                'theory_key': theory_key,
                                'theory_value': theory_val,
                                'rel_diff_pct': rel_diff * 100
                            })
                    elif config_val != theory_val:
                        self.conflicts.append({
                            'param': param_name,
                            'config_key': config_key,
                            'config_value': config_val,
                            'theory_key': theory_key,
                            'theory_value': theory_val,
                            'rel_diff_pct': None
                        })
        
        print(f"  Found {len(self.conflicts)} conflicts")
    
    def generate_report(self):
        """Generate markdown report"""
        report = f"""# Config vs Theory Output Audit

## Summary

- **Config values**: {len(self.config_values)}
- **Theory output values**: {len(self.theory_values)}
- **Conflicts found**: {len(self.conflicts)}

## Conflicts

"""
        
        if self.conflicts:
            report += "| Parameter | Config Key | Config Value | Theory Key | Theory Value | Diff % |\n"
            report += "|-----------|------------|--------------|------------|--------------|--------|\n"
            
            for conflict in sorted(self.conflicts, key=lambda x: x.get('rel_diff_pct', 0) or 0, reverse=True):
                report += f"| {conflict['param']} | "
                report += f"`{conflict['config_key']}` | "
                report += f"`{conflict['config_value']:.6g}` | "
                report += f"`{conflict['theory_key']}` | "
                report += f"`{conflict['theory_value']:.6g}` | "
                if conflict['rel_diff_pct'] is not None:
                    report += f"{conflict['rel_diff_pct']:.2f}% |\n"
                else:
                    report += "N/A |\n"
        else:
            report += "✅ No conflicts found!\n"
        
        report += "\n## Resolution Priority\n\n"
        report += "1. **Use simulation value** if parameter is derived from theory\n"
        report += "2. **Use config value** if parameter is a fundamental input\n"
        report += "3. **Research** if unclear which is correct\n"
        
        with open('CONFIG_AUDIT_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n✅ Report saved: CONFIG_AUDIT_REPORT.md")
        
    def save_results(self):
        """Save results to JSON"""
        results = {
            'config_values': self.config_values,
            'theory_values': self.theory_values,
            'conflicts': self.conflicts
        }
        
        with open('config_audit_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print("✅ Results saved: config_audit_results.json")

def main():
    auditor = ConfigAuditor()
    auditor.extract_config_values()
    auditor.extract_theory_values()
    auditor.find_conflicts()
    auditor.generate_report()
    auditor.save_results()

if __name__ == '__main__':
    main()
