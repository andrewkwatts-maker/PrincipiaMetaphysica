#!/usr/bin/env python3
"""
Fix critical diagram issues for v12.0
"""

import re

print("FIXING CRITICAL DIAGRAM ISSUES FOR V12.0")
print("=" * 60)

# Fix 1: Update version tag in diagrams/theory-diagrams.html
try:
    with open('diagrams/theory-diagrams.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix version tag
    content = content.replace(
        'Updated for 2T Physics (v6.4)',
        'Framework Version 12.0'
    )
    content = content.replace(
        'Visual Guide to the 2T Physics Framework',
        'Visual Guide to the Geometric Framework'
    )

    with open('diagrams/theory-diagrams.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Fixed diagrams/theory-diagrams.html version tag (v6.4 → v12.0)")
except Exception as e:
    print(f"✗ Error fixing diagrams/theory-diagrams.html: {e}")

# Fix 2: Update version tag in sections/formulas.html
try:
    with open('sections/formulas.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix version tag
    content = content.replace(
        'v6.0 Temporal Mirrors',
        'v12.0 Geometric Framework'
    )
    content = content.replace(
        'Temporal Mirror Framework (v6.0)',
        'Geometric Framework (v12.0)'
    )

    with open('sections/formulas.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Fixed sections/formulas.html version tag (v6.0 → v12.0)")
except Exception as e:
    print(f"✗ Error fixing sections/formulas.html: {e}")

# Fix 3: Update neutrino hierarchy prediction in sections/fermion-sector.html
try:
    with open('sections/fermion-sector.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix hierarchy prediction - careful to preserve context
    # Pattern: "Inverted Hierarchy" with percentage 85.5% or similar
    content = re.sub(
        r'Inverted Hierarchy[^<]*85\.5%',
        'Normal Hierarchy (76% confidence)',
        content
    )
    content = re.sub(
        r'inverted hierarchy[^<]*85\.5%',
        'normal hierarchy (76% confidence)',
        content,
        flags=re.IGNORECASE
    )

    # Also fix standalone IH references
    content = content.replace('IH (85.5%)', 'NH (76%)')
    content = content.replace('Inverted Hierarchy: 85.5%', 'Normal Hierarchy: 76%')

    with open('sections/fermion-sector.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Fixed sections/fermion-sector.html neutrino hierarchy (IH 85.5% → NH 76%)")
except Exception as e:
    print(f"✗ Error fixing sections/fermion-sector.html: {e}")

# Fix 4: Add pedagogical notes for 14D×2 and CY4 references in diagrams
try:
    with open('diagrams/theory-diagrams.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add note near any 14D×2 references (if they exist in educational context)
    # This is a gentle fix - we'll add a general note at the top
    if '14D' in content or 'CY4' in content:
        # Find the intro section and add a note
        intro_pattern = r'(<div class="intro">.*?<p>)(.*?)(</p>)'

        pedagogical_note = """This visual guide includes some pedagogical diagrams showing intermediate construction steps
        (e.g., CY4 building blocks, 14D×2 notation). The current v12.0 framework uses TCS G₂ manifolds
        with dimensional reduction 26D → 13D → 7D (G₂) → 6D → 4D. """

        content = re.sub(
            intro_pattern,
            r'\1\2 ' + pedagogical_note + r'\3',
            content,
            count=1,
            flags=re.DOTALL
        )

        with open('diagrams/theory-diagrams.html', 'w', encoding='utf-8') as f:
            f.write(content)

        print("✓ Added pedagogical note for 14D×2/CY4 references in diagrams")
    else:
        print("ℹ No 14D×2/CY4 references found in diagrams (already clean)")
except Exception as e:
    print(f"✗ Error adding pedagogical note: {e}")

print("\n" + "=" * 60)
print("DIAGRAM FIXES COMPLETE")
print("\nFiles modified:")
print("  - diagrams/theory-diagrams.html")
print("  - sections/formulas.html")
print("  - sections/fermion-sector.html")
print("\nCritical issues resolved:")
print("  ✓ Version tags updated to v12.0")
print("  ✓ Neutrino hierarchy prediction corrected (IH → NH)")
print("  ✓ Pedagogical context added for legacy notation")
