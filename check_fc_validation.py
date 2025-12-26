#!/usr/bin/env python3
"""Check fermion_chirality validation structure"""

import json

with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fc = data['simulations']['fermion_chirality']
print('Keys:', list(fc.keys()))
print('\nValidation key exists:', 'validation' in fc)

if 'validation' in fc:
    print('Validation:', json.dumps(fc['validation'], indent=2))
else:
    print('\nNo validation key - showing full simulation:')
    print(json.dumps(fc, indent=2))
