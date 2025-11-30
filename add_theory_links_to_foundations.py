#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""

"""Add theory section links to foundation pages"""

import os

# Define which theory sections use each foundation topic
foundation_to_sections = {
    'einstein-field-equations.html': {
        'sections': [
            ('sections/geometric-framework.html', 'Geometric Framework', 'How Einstein\'s equations generalize to 26D'),
            ('sections/cosmology.html', 'Cosmology', 'Dark energy and universe expansion'),
            ('sections/einstein-hilbert-term.html', '13D Einstein-Hilbert', 'Extension to higher dimensions'),
        ],
        'title': 'Where Einstein Field Equations Are Used in PM'
    },
    'ricci-tensor.html': {
        'sections': [
            ('sections/geometric-framework.html', 'Geometric Framework', 'Curvature in higher dimensions'),
            ('sections/cosmology.html', 'Cosmology', 'Spacetime curvature evolution'),
        ],
        'title': 'Where Ricci Curvature Is Used in PM'
    },
    'clifford-algebra.html': {
        'sections': [
            ('sections/fermion-sector.html', 'Fermion Sector', 'Spinor representations and chirality'),
            ('sections/pneuma-lagrangian.html', 'Pneuma Lagrangian', '8192-component bulk spinor'),
            ('sections/geometric-framework.html', 'Geometric Framework', 'Cl(24,2) → Cl(12,1) reduction'),
        ],
        'title': 'Where Clifford Algebra Is Used in PM'
    },
    'yang-mills.html': {
        'sections': [
            ('sections/gauge-unification.html', 'Gauge Unification', 'SO(10) and Standard Model forces'),
            ('sections/geometric-framework.html', 'Geometric Framework', 'Gauge fields in bulk'),
        ],
        'title': 'Where Yang-Mills Theory Is Used in PM'
    },
    'kaluza-klein.html': {
        'sections': [
            ('sections/geometric-framework.html', 'Geometric Framework', '26D → 13D → 6D → 4D reduction'),
            ('sections/predictions.html', 'Predictions', 'KK particles at 5 TeV'),
            ('sections/fermion-sector.html', 'Fermion Sector', 'KK tower decomposition'),
        ],
        'title': 'Where Kaluza-Klein Theory Is Used in PM'
    },
    'g2-manifolds.html': {
        'sections': [
            ('sections/geometric-framework.html', 'Geometric Framework', 'G₂ compactification from 13D → 6D'),
            ('sections/fermion-sector.html', 'Fermion Sector', '3 generations from χ_eff = 144'),
            ('sections/gauge-unification.html', 'Gauge Unification', 'SO(10) emergence'),
        ],
        'title': 'Where G₂ Manifolds Are Used in PM'
    },
    'calabi-yau.html': {
        'sections': [
            ('sections/geometric-framework.html', 'Geometric Framework', 'Comparison with G₂ compactification'),
        ],
        'title': 'Connection to PM Framework'
    },
    'so10-gut.html': {
        'sections': [
            ('sections/gauge-unification.html', 'Gauge Unification', 'SO(10) from G₂ compactification'),
            ('sections/fermion-sector.html', 'Fermion Sector', '16-spinor and 3 generations'),
        ],
        'title': 'Where SO(10) GUT Is Used in PM'
    },
    'boltzmann-entropy.html': {
        'sections': [
            ('sections/thermal-time.html', 'Thermal Time', 'Entropy and time emergence'),
            ('sections/cosmology.html', 'Cosmology', 'Thermodynamic arrow of time'),
        ],
        'title': 'Where Boltzmann Entropy Is Used in PM'
    },
    'kms-condition.html': {
        'sections': [
            ('sections/thermal-time.html', 'Thermal Time', 'KMS states and modular flow'),
        ],
        'title': 'Where KMS Condition Is Used in PM'
    },
    'tomita-takesaki.html': {
        'sections': [
            ('sections/thermal-time.html', 'Thermal Time', 'Modular automorphisms and time emergence'),
        ],
        'title': 'Where Tomita-Takesaki Theory Is Used in PM'
    },
    'dirac-equation.html': {
        'sections': [
            ('sections/pneuma-lagrangian.html', 'Pneuma Lagrangian', '26D generalization of Dirac equation'),
            ('sections/fermion-sector.html', 'Fermion Sector', 'Spinor fields'),
        ],
        'title': 'Where Dirac Equation Is Used in PM'
    },
    'einstein-hilbert-action.html': {
        'sections': [
            ('sections/einstein-hilbert-term.html', '13D Einstein-Hilbert', 'Extension to 13D shadow'),
            ('sections/geometric-framework.html', 'Geometric Framework', 'Action principle in higher D'),
        ],
        'title': 'Where Einstein-Hilbert Action Is Used in PM'
    },
}

# Template for the theory links section
theory_section_template = '''
        <!-- Where This Is Used in PM -->
        <section class="subsection" style="background: linear-gradient(135deg, rgba(139, 127, 255, 0.05), rgba(255, 126, 182, 0.05)); border: 2px solid rgba(139, 127, 255, 0.3);">
            <h2 style="color: #8b7fff;">{title}</h2>
            <p>
                This foundational physics appears in the following sections of Principia Metaphysica:
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
{cards}
            </div>

            <div style="text-align: center; margin-top: 2rem;">
                <a href="../sections/index.html" style="display: inline-block; padding: 1rem 2rem; background: linear-gradient(135deg, #8b7fff, #ff7eb6); color: white; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 1.05rem;">
                    Browse All Theory Sections &rarr;
                </a>
            </div>
        </section>
'''

card_template = '''                <div class="resource-card" style="border-left: 4px solid #8b7fff;">
                    <h4 style="color: #8b7fff;">{section_name}</h4>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin: 0.75rem 0;">
                        {description}
                    </p>
                    <a href="../{section_url}" class="resource-link" style="color: var(--accent-primary);">
                        Read More &rarr;
                    </a>
                </div>
'''

# Process each foundation file
for foundation_file, info in foundation_to_sections.items():
    filepath = os.path.join('foundations', foundation_file)

    if not os.path.exists(filepath):
        print(f"Skipping {foundation_file} (not found)")
        continue

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build the cards
    cards = []
    for section_url, section_name, description in info['sections']:
        card = card_template.format(
            section_name=section_name,
            description=description,
            section_url=section_url
        )
        cards.append(card)

    # Build the full section
    theory_section = theory_section_template.format(
        title=info['title'],
        cards='\n'.join(cards)
    )

    # Insert before the navigation links at the bottom (try multiple markers)
    nav_markers = ['<div class="nav-links"', '<div class="section-nav-links"', '</main>']
    inserted = False

    for nav_marker in nav_markers:
        if nav_marker in content:
            content = content.replace(nav_marker, theory_section + '\n        ' + nav_marker, 1)
            inserted = True
            break

    if not inserted:
        print(f"Warning: Could not find insertion point in {foundation_file}")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Done: {foundation_file}")

print("\nAll foundation pages updated with theory section links!")
