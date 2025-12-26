#!/usr/bin/env python3
"""Inspect simulation validation structures"""

import json

with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sims = data['simulations']

# Check a few key simulations
test_keys = ['neutrino_masses', 'higgs_mass', 'kk_graviton', 'hebrew_physics',
             'kk_spectrum_v14_2', 'yukawa_textures', 'cp_phase']

for key in test_keys:
    if key in sims:
        print(f'\n=== {key} ===')
        sim = sims[key]
        val = sim.get('validation')
        if val:
            print(json.dumps(val, indent=2))
        else:
            print('No validation key')
            print('Available keys:', list(sim.keys())[:10])
    else:
        print(f'\n=== {key} === NOT FOUND')
