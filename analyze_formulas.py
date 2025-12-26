#!/usr/bin/env python3
import json
import re

# Load data
with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

formulas = data.get('formulas', {}).get('formulas', {})

# Find formulas without params
missing = [fid for fid, f in formulas.items() if not f.get('inputParams') and not f.get('outputParams')]

print(f"Formulas missing params: {len(missing)}\n")

# Analyze a few
for fid in missing[:5]:
    f = formulas[fid]
    print(f"=== {fid} ===")
    print(f"Label: {f.get('label', '')}")
    print(f"HTML: {f.get('html', '')}")
    print(f"Terms: {list(f.get('terms', {}).keys())}")
    print(f"Simulation: {f.get('simulationFile', 'None')}")
    print()
