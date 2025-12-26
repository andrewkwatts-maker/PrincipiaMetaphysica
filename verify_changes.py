#!/usr/bin/env python3
"""Verify validation_summary changes"""

import json

with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

vs = data['validation_summary']

print('Sample entries from different categories:\n')
print('='*60)

# Sample PASS with data
print('\n1. PASS with full data (Proton Decay):')
print(json.dumps(vs[0], indent=2))

# Sample PASS without full validation key
print('\n2. PASS without validation key (Fermion Chirality):')
fc = [e for e in vs if e['name'] == 'Fermion Chirality'][0]
print(json.dumps(fc, indent=2))

# Sample ERROR
print('\n3. ERROR (Hebrew Physics):')
error_entry = [e for e in vs if e['status'] == 'ERROR'][0]
print(json.dumps(error_entry, indent=2))

# Sample CHECK
print('\n4. CHECK (Multi-Sector Sampling):')
check_entry = [e for e in vs if e['status'] == 'CHECK'][0]
print(json.dumps(check_entry, indent=2))

print('\n' + '='*60)
print('\nVerification complete!')
