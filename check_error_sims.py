#!/usr/bin/env python3
"""Check ERROR simulations"""

import json

with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sims = data['simulations']

error_sims = [
    'hebrew_physics',
    'kk_spectrum_v14_2',
    'yukawa_textures',
    'cp_phase',
    'pneuma_bridge_v15_1'
]

for key in error_sims:
    sim = sims.get(key)
    if sim:
        print(f'\n{"="*60}')
        print(f'Simulation: {key}')
        print("="*60)
        print(json.dumps(sim, indent=2))
    else:
        print(f'\nSimulation {key}: NOT FOUND')
