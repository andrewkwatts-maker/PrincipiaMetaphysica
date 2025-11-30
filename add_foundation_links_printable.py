#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""

"""Add foundation links to beginners-guide-printable.html"""

import re

# Read the file
with open('beginners-guide-printable.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define replacements - only replace first occurrence in each section
replacements = [
    # G₂ manifolds
    (r'<strong>G<sub>2</sub> manifold</strong>',
     r'<strong><a href="foundations/g2-manifolds.html" style="color: #8b7fff; text-decoration: none; border-bottom: 1px solid #8b7fff;">G<sub>2</sub> manifold</a></strong>'),

    # Kaluza-Klein
    (r'Kaluza-Klein excitations',
     r'<a href="foundations/kaluza-klein.html" style="color: #8b7fff; text-decoration: none;">Kaluza-Klein</a> excitations'),

    # Entropy
    (r'connects time to <strong>entropy</strong>',
     r'connects time to <strong><a href="foundations/boltzmann-entropy.html" style="color: #8b7fff; text-decoration: none;">entropy</a></strong>'),

    # Gravity
    (r'gravity</strong> \(how planets',
     r'<a href="foundations/einstein-field-equations.html" style="color: #8b7fff; text-decoration: none;">gravity</a></strong> (how planets'),
]

# Apply replacements
for old, new in replacements:
    content = re.sub(old, new, content, count=1)

# Add foundation resources section with QR code
resources_section = '''
    <div class="section" style="page-break-before: always;">
        <h2 style="color: #51cf66; border-bottom: 3px solid #51cf66; padding-bottom: 0.5rem; margin-bottom: 1.5rem;">
            Learn the Physics Foundations
        </h2>

        <p style="margin-bottom: 1.5rem; line-height: 1.8;">
            Every concept in this theory builds on established physics. Explore detailed explanations with diagrams, videos, and practice problems:
        </p>

        <div style="display: flex; align-items: center; gap: 2rem; background: #f8f9fa; border: 2px solid #8b7fff; border-radius: 10px; padding: 2rem; margin: 1.5rem 0;">
            <div style="flex: 1;">
                <h3 style="color: #8b7fff; margin-bottom: 1rem; text-align: center;">Scan to Access Foundation Pages</h3>

                <!-- QR Code using Google Chart API -->
                <div style="text-align: center;">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://www.xn--metaphysic-97a.com/foundations/"
                         alt="QR Code for Foundations"
                         style="width: 200px; height: 200px; border: 3px solid #8b7fff; border-radius: 10px; padding: 10px; background: white;"/>
                    <p style="margin-top: 1rem; font-weight: 700; color: #8b7fff;">
                        www.metaphysicæ.com/foundations/
                    </p>
                </div>
            </div>

            <div style="flex: 1.5;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <h4 style="color: #8b7fff; margin-bottom: 0.5rem; font-size: 0.95rem;">Gravity & Spacetime</h4>
                        <ul style="list-style: none; margin: 0; padding: 0; line-height: 1.6; font-size: 0.85rem;">
                            <li>• Einstein Field Equations</li>
                            <li>• Einstein-Hilbert Action</li>
                            <li>• Ricci Tensor</li>
                        </ul>
                    </div>

                    <div>
                        <h4 style="color: #ff7eb6; margin-bottom: 0.5rem; font-size: 0.95rem;">Quantum Fields</h4>
                        <ul style="list-style: none; margin: 0; padding: 0; line-height: 1.6; font-size: 0.85rem;">
                            <li>• Dirac Equation</li>
                            <li>• Clifford Algebra</li>
                            <li>• Yang-Mills Theory</li>
                        </ul>
                    </div>

                    <div>
                        <h4 style="color: #4facfe; margin-bottom: 0.5rem; font-size: 0.95rem;">Extra Dimensions</h4>
                        <ul style="list-style: none; margin: 0; padding: 0; line-height: 1.6; font-size: 0.85rem;">
                            <li>• Kaluza-Klein Theory</li>
                            <li>• G₂ Manifolds</li>
                            <li>• Calabi-Yau Manifolds</li>
                        </ul>
                    </div>

                    <div>
                        <h4 style="color: #ffc107; margin-bottom: 0.5rem; font-size: 0.95rem;">Time & Entropy</h4>
                        <ul style="list-style: none; margin: 0; padding: 0; line-height: 1.6; font-size: 0.85rem;">
                            <li>• Boltzmann Entropy</li>
                            <li>• KMS Condition</li>
                            <li>• Tomita-Takesaki Theory</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <p style="margin-top: 1.5rem; text-align: center; font-style: italic; color: #666;">
            Each page includes SVG diagrams, YouTube videos, key terms glossary, and practice problems.
        </p>
    </div>
'''

# Insert before </main> tag
if '</main>' in content:
    content = content.replace('</main>', resources_section + '\n</main>')

# Write back
with open('beginners-guide-printable.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done: Added foundation links to beginners-guide-printable.html")
