#!/usr/bin/env python3
"""
Analyze simulation file links in config.py formulas
"""
import re
import os

# Read config.py
with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all formulas and their simulation_file attributes
formula_pattern = r'(\w+)\s*=\s*Formula\('
simulation_pattern = r'simulation_file="([^"]*)"'

# Split content into formula blocks
formulas_data = {}
current_formula = None

lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]

    # Check if this is a formula definition
    formula_match = re.search(r'^\s+(\w+)\s*=\s*Formula\(', line)
    if formula_match:
        current_formula = formula_match.group(1)
        formulas_data[current_formula] = {
            'line': i + 1,
            'simulation_file': None,
            'id': None,
            'label': None
        }

        # Look ahead to find simulation_file, id, and label in the next 50 lines
        for j in range(i, min(i + 100, len(lines))):
            if 'simulation_file=' in lines[j]:
                sim_match = re.search(r'simulation_file="([^"]*)"', lines[j])
                if sim_match:
                    formulas_data[current_formula]['simulation_file'] = sim_match.group(1)
            if 'id=' in lines[j] and formulas_data[current_formula]['id'] is None:
                id_match = re.search(r'id="([^"]*)"', lines[j])
                if id_match:
                    formulas_data[current_formula]['id'] = id_match.group(1)
            if 'label=' in lines[j] and formulas_data[current_formula]['label'] is None:
                label_match = re.search(r'label="([^"]*)"', lines[j])
                if label_match:
                    formulas_data[current_formula]['label'] = label_match.group(1)
            # Stop when we hit the next formula or closing parenthesis
            if j > i and re.match(r'^\s+\w+\s*=\s*Formula\(', lines[j]):
                break
    i += 1

# Get list of simulation files
sim_dir = 'simulations'
sim_files = []
if os.path.exists(sim_dir):
    sim_files = [f for f in os.listdir(sim_dir) if f.endswith('.py') and not f.startswith('__')]
    sim_files.sort()

# Categorize formulas
with_sim = {k: v for k, v in formulas_data.items() if v['simulation_file']}
without_sim = {k: v for k, v in formulas_data.items() if not v['simulation_file']}

print("=" * 80)
print(f"SIMULATION FILE LINK ANALYSIS")
print("=" * 80)
print(f"\nTotal Formulas: {len(formulas_data)}")
print(f"With simulation_file: {len(with_sim)} ({100*len(with_sim)/len(formulas_data):.1f}%)")
print(f"Without simulation_file: {len(without_sim)} ({100*len(without_sim)/len(formulas_data):.1f}%)")
print(f"\nAvailable simulation files: {len(sim_files)}")

print("\n" + "=" * 80)
print("FORMULAS WITH SIMULATION FILES")
print("=" * 80)
for name, data in sorted(with_sim.items()):
    print(f"\n{name}")
    print(f"  ID: {data['id']}")
    print(f"  Label: {data['label']}")
    print(f"  Simulation: {data['simulation_file']}")

print("\n" + "=" * 80)
print("FORMULAS WITHOUT SIMULATION FILES")
print("=" * 80)
for name, data in sorted(without_sim.items()):
    print(f"\n{name}")
    print(f"  ID: {data['id']}")
    print(f"  Label: {data['label']}")

print("\n" + "=" * 80)
print("AVAILABLE SIMULATION FILES")
print("=" * 80)
for i, f in enumerate(sim_files, 1):
    print(f"{i:3}. {f}")

# Save detailed report
with open('simulation_link_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("SIMULATION FILE LINK ANALYSIS\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total Formulas: {len(formulas_data)}\n")
    f.write(f"With simulation_file: {len(with_sim)} ({100*len(with_sim)/len(formulas_data):.1f}%)\n")
    f.write(f"Without simulation_file: {len(without_sim)} ({100*len(without_sim)/len(formulas_data):.1f}%)\n\n")

    f.write("FORMULAS WITH SIMULATION FILES\n")
    f.write("=" * 80 + "\n")
    for name, data in sorted(with_sim.items()):
        f.write(f"\n{name}\n")
        f.write(f"  ID: {data['id']}\n")
        f.write(f"  Label: {data['label']}\n")
        f.write(f"  Simulation: {data['simulation_file']}\n")

    f.write("\n\nFORMULAS WITHOUT SIMULATION FILES\n")
    f.write("=" * 80 + "\n")
    for name, data in sorted(without_sim.items()):
        f.write(f"\n{name}\n")
        f.write(f"  ID: {data['id']}\n")
        f.write(f"  Label: {data['label']}\n")

    f.write("\n\nAVAILABLE SIMULATION FILES\n")
    f.write("=" * 80 + "\n")
    for f_name in sim_files:
        f.write(f"{f_name}\n")

print(f"\nDetailed report saved to: simulation_link_analysis.txt")
