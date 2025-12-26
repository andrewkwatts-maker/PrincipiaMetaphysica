#!/usr/bin/env python3
"""Insert PNEUMA_STRESS_ENERGY formula into config.py"""

# Read the config file
with open(r"h:\Github\PrincipiaMetaphysica\config.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Read the formula to insert
with open(r"h:\Github\PrincipiaMetaphysica\pneuma_stress_energy_formula.txt", "r", encoding="utf-8") as f:
    formula_text = f.read()

# Find the line with BEKENSTEIN_HAWKING
insert_line = None
for i, line in enumerate(lines):
    if "BEKENSTEIN_HAWKING = Formula(" in line:
        insert_line = i
        break

if insert_line is None:
    print("ERROR: Could not find BEKENSTEIN_HAWKING in config.py")
    exit(1)

# Insert the formula before BEKENSTEIN_HAWKING
lines.insert(insert_line, formula_text)

# Write back to config.py
with open(r"h:\Github\PrincipiaMetaphysica\config.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Successfully inserted PNEUMA_STRESS_ENERGY at line {insert_line}")
print("Formula added before BEKENSTEIN_HAWKING")
