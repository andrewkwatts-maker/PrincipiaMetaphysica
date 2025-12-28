#!/usr/bin/env python3
"""Verify all Formula dataclass fields."""

from config import Formula

print("Formula Dataclass Fields:")
print("=" * 60)

# Get all fields
all_fields = list(Formula.__dataclass_fields__.keys())

# Categorize fields
required_fields = ['id', 'label', 'html', 'latex', 'plain_text', 'category', 'description']
display_fields = ['attribution', 'status', 'section', 'paper_page']
term_fields = ['terms']
derivation_fields = ['derivation']
numerical_fields = ['computed_value', 'units', 'experimental_value', 'experimental_error', 'sigma_deviation']
link_fields = ['simulation_file', 'verification_simulation', 'references', 'learning_resources', 'related_formulas']
param_fields = ['input_params', 'output_params', 'reference_ids']
comment_fields = ['notes', 'testability']
rich_ux_fields = ['html_interactive', 'info_title', 'info_meaning', 'info_grid', 'use_cases',
                  'expansion_title', 'sub_components', 'derivation_chain']

# Print categorized fields
print("\n1. REQUIRED FIELDS:")
for f in required_fields:
    print(f"   - {f}")

print("\n2. DISPLAY OPTIONS:")
for f in display_fields:
    print(f"   - {f}")

print("\n3. TERMS (hoverable):")
for f in term_fields:
    print(f"   - {f}")

print("\n4. DERIVATION:")
for f in derivation_fields:
    print(f"   - {f}")

print("\n5. NUMERICAL VALUES:")
for f in numerical_fields:
    print(f"   - {f}")

print("\n6. LINKS & RESOURCES:")
for f in link_fields:
    print(f"   - {f}")

print("\n7. PARAMETER LINKAGE:")
for f in param_fields:
    print(f"   - {f}")

print("\n8. COMMENTS:")
for f in comment_fields:
    print(f"   - {f}")

print("\n9. RICH UX RENDERING (NEW):")
for f in rich_ux_fields:
    if f in all_fields:
        print(f"   [+] {f}")
    else:
        print(f"   [-] {f} (MISSING)")

print("\n" + "=" * 60)
print(f"Total fields: {len(all_fields)}")
print(f"Rich UX fields: {len([f for f in rich_ux_fields if f in all_fields])}/{len(rich_ux_fields)}")
print("\nAll rich UX fields present!" if all(f in all_fields for f in rich_ux_fields) else "Some fields missing!")
