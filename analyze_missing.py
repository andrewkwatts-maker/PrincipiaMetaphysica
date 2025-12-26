#!/usr/bin/env python3
import json
import sys

# Use UTF-8 for output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

formulas = data.get('formulas', {}).get('formulas', {})

# Find formulas without params
missing = [fid for fid, f in formulas.items() if not f.get('inputParams') and not f.get('outputParams')]

print(f"Formulas still missing params: {len(missing)}\n")

# Analyze each one
for fid in sorted(missing):
    f = formulas[fid]
    print(f"=== {fid} ===")
    print(f"Label: {f.get('label', '')}")
    print(f"Category: {f.get('category', '')}")
    html = f.get('html', '')
    print(f"HTML: {html[:100] if html else 'None'}")
    print(f"LaTeX: {f.get('latex', 'None')[:100]}")
    print(f"Terms: {list(f.get('terms', {}).keys())}")
    print(f"Simulation: {f.get('simulationFile', 'None')}")
    print()
