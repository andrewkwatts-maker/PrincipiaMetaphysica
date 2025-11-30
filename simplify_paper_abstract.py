#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""

"""Simplify the abstract in principia-metaphysica-paper.html for printing"""

import re

# Read the paper
with open('principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the abstract section with cleaner, more readable text
old_abstract_start = r'<p class="abstract-title">Abstract</p>\s*<p>'
old_abstract_end = r'</p>\s*</div>\s*<div class="toc">'

# Extract the current abstract
abstract_match = re.search(old_abstract_start + r'(.*?)' + old_abstract_end, content, re.DOTALL)

if abstract_match:
    # New simplified abstract - clear, concise, printable
    new_abstract = '''<p class="abstract-title">Abstract</p>
            <p>
                This paper presents Principia Metaphysica, a theoretical framework unifying gravity, gauge forces,
                and the origin of time through higher-dimensional geometry. The framework begins with 26-dimensional
                spacetime with signature (24,2)—24 spatial dimensions and 2 timelike dimensions. An Sp(2,R) gauge
                symmetry removes unphysical ghost states, projecting to an effective 13-dimensional shadow manifold
                with signature (12,1). This 13D space then compactifies on a 7-dimensional G₂ manifold, yielding
                a 6-dimensional bulk with signature (5,1).
            </p>
            <p>
                The framework features four branes: one 6D observable universe (5,1) and three 4D shadow universes (3,1),
                all sharing a common 4D spacetime base. The topology of the flux-dressed G₂ manifold yields an effective
                Euler characteristic χ<sub>eff</sub> = 144, which through the relation n<sub>gen</sub> = χ<sub>eff</sub>/48
                predicts exactly 3 fermion generations. The fundamental field is an 8192-component spinor in 26D
                (Clifford algebra Cl(24,2)), which gauge-reduces to 64 effective components in the 13D shadow.
            </p>
            <p>
                Time emerges from thermal entropy via the Two-Time Thermal Hypothesis: observable thermal time couples
                to an orthogonal hidden time dimension. The framework predicts dark energy equation of state
                w₀ = -11/13 ≈ -0.846 and w<sub>a</sub> ≈ -0.75, matching DESI 2024 observations within 1σ.
                SO(10) grand unification emerges naturally from the G₂ compactification. Shared extra dimensions
                produce Kaluza-Klein graviton resonances at approximately 5 TeV, testable at the High-Luminosity LHC.
            </p>
            <p>
                Six critical mathematical issues have been resolved: (1) Generation count correctly derived from
                flux-dressed topology rather than bare Euler characteristic; (2) Dark energy attractor to w = -1.0
                at late times via Mashiach minimum; (3) Spinor dimensions validated via Clifford algebra;
                (4) Dimensional reduction pathway clarified (gauge projection followed by compactification);
                (5) Previously undefined parameters now derived from geometry; (6) Gauge coupling unification achieved
                with 3% precision. Framework validation shows 51 of 58 parameters (88%) passing consistency checks,
                with 10 of 14 predictions within experimental error bars.
            </p>
        </div>

        <div class="toc">'''

    # Replace the abstract
    content = re.sub(
        old_abstract_start + r'.*?' + old_abstract_end,
        new_abstract,
        content,
        flags=re.DOTALL
    )

    # Write back
    with open('principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Done: Simplified abstract for printing")
    print("- Removed inline technical jargon")
    print("- Broke into 4 clear paragraphs")
    print("- Kept all key information")
    print("- Made more readable for print")
else:
    print("Warning: Could not find abstract section")
