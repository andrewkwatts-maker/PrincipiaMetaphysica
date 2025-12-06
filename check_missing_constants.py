"""
Check which PM constants from formula_definitions.py are missing from theory_output.json

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
from formula_definitions import ALL_FORMULAS

# Load theory_output.json to see simulation values
with open('theory_output.json', 'r') as f:
    simulation = json.load(f)

# Extract all PM values referenced in formulas
formula_pm_values = set()
for formula in ALL_FORMULAS.values():
    for pm_value in formula.get('pm_values', []):
        formula_pm_values.add(pm_value)

print('Checking Formula PM References Against Simulation Output')
print('=' * 80)
print()

# Parse category.parameter format
missing_from_simulation = []
found_in_simulation = []

for pm_value in sorted(formula_pm_values):
    if not pm_value:
        continue
    parts = pm_value.split('.')
    if len(parts) == 2:
        category, param = parts
        if category in simulation and param in simulation[category]:
            found_in_simulation.append(pm_value)
            value = simulation[category][param]
            # Format large numbers
            if isinstance(value, (int, float)) and abs(value) > 1000:
                print(f'✓ {pm_value} = {value:.3e}')
            else:
                print(f'✓ {pm_value} = {value}')
        else:
            missing_from_simulation.append(pm_value)
            print(f'✗ MISSING: {pm_value}')

print()
print(f'Summary: {len(found_in_simulation)}/{len(formula_pm_values)} in theory_output.json')
print(f'Missing: {len(missing_from_simulation)}')
print()

if missing_from_simulation:
    print('Missing from theory_output.json (need to add to simulation):')
    for pm in missing_from_simulation:
        print(f'  - {pm}')

    # Save for later use
    with open('missing_constants.json', 'w') as f:
        json.dump({
            'missing': missing_from_simulation,
            'found': found_in_simulation,
            'total': len(formula_pm_values)
        }, f, indent=2)

    print()
    print('✅ Missing constants list saved to: missing_constants.json')
