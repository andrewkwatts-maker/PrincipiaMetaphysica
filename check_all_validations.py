#!/usr/bin/env python3
"""Check validation data availability in all simulations"""

import json

with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sims = data['simulations']

count_with = 0
count_without = 0

for k, v in sims.items():
    has_val = 'validation' in v
    if has_val:
        count_with += 1
        status = "HAS"
    else:
        count_without += 1
        status = "NO"
    print(f'{k}: {status} validation')

print(f'\nTotal: {count_with} with validation, {count_without} without')
