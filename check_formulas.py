#!/usr/bin/env python3
import json

data = json.load(open(r'h:\Github\PrincipiaMetaphysica\theory_output.json', 'r', encoding='utf-8'))
founds = {f['id']: f for f in data['foundations']}

print('BOLTZMANN-ENTROPY FORMULAS (last 4 are new):')
boltz = founds['boltzmann-entropy']
for i, f in enumerate(boltz['formulas'], 1):
    print(f"{i}. {f['id']}: {f['label']}")

print('\nCALABI-YAU FORMULAS (last 2 are new):')
cy = founds['calabi-yau']
for i, f in enumerate(cy['formulas'], 1):
    print(f"{i}. {f['id']}: {f['label']}")

print('\nCLIFFORD-ALGEBRA FORMULAS (last 2 are new):')
cliff = founds['clifford-algebra']
for i, f in enumerate(cliff['formulas'], 1):
    print(f"{i}. {f['id']}: {f['label']}")
