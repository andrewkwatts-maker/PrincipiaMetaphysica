#!/usr/bin/env python3
"""Extract available data from simulations to build validation summary"""

import json

with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sims = data['simulations']

# Check a few simulations without validation key
test_sims = [
    'kk_graviton', 'doublet_triplet', 'breaking_chain',
    'fermion_chirality', 'pneuma_stability'
]

for key in test_sims:
    if key in sims:
        print(f'\n{"="*60}')
        print(f'Simulation: {key}')
        print("="*60)
        sim = sims[key]
        print(json.dumps(sim, indent=2))
