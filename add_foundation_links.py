#!/usr/bin/env python3
"""Add foundation links to beginners-guide.html"""

import re

# Read the file
with open('beginners-guide.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define replacements - only replace first occurrence in each section to avoid over-linking
replacements = [
    # G₂ manifolds
    (r'<strong>G<sub>2</sub> manifold</strong>',
     r'<strong><a href="foundations/g2-manifolds.html" style="color: var(--accent-primary); text-decoration: none; border-bottom: 2px solid var(--accent-primary);">G<sub>2</sub> manifold</a></strong>'),

    # Kaluza-Klein (only link first mention)
    (r'Kaluza-Klein excitations',
     r'<a href="foundations/kaluza-klein.html" style="color: var(--accent-primary); text-decoration: none;">Kaluza-Klein</a> excitations'),

    # Entropy and thermal time
    (r'connects time to <strong>entropy</strong>',
     r'connects time to <strong><a href="foundations/boltzmann-entropy.html" style="color: var(--accent-primary); text-decoration: none;">entropy</a></strong>'),

    # Einstein Field Equations
    (r'gravity</strong> \(how planets orbit',
     r'<a href="foundations/einstein-field-equations.html" style="color: var(--accent-primary); text-decoration: none;">gravity</a></strong> (how planets orbit'),
]

# Apply replacements (only first occurrence of each)
for old, new in replacements:
    content = re.sub(old, new, content, count=1)

# Add a "Learn More" section before "Download This Guide"
learn_more_section = '''
        <!-- Learn More Section -->
        <div class="concept-card" style="border: 2px solid rgba(81, 207, 102, 0.4); background: linear-gradient(135deg, rgba(81, 207, 102, 0.05), rgba(79, 172, 254, 0.05));">
            <h2 style="color: #51cf66;">📚 Want to Go Deeper? Learn the Physics!</h2>

            <p class="simple-explanation">
                Every concept in this theory builds on established physics. Explore the foundations with diagrams,
                YouTube videos, and practice problems:
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: var(--bg-card); border: 2px solid rgba(139, 127, 255, 0.3); border-radius: 10px; padding: 1.25rem;">
                    <h4 style="color: var(--accent-primary); margin-bottom: 0.75rem;">🌌 Gravity & Spacetime</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin: 0.5rem 0;"><a href="foundations/einstein-field-equations.html" style="color: var(--text-primary); text-decoration: none;">→ Einstein Field Equations</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/einstein-hilbert-action.html" style="color: var(--text-primary); text-decoration: none;">→ Einstein-Hilbert Action</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/ricci-tensor.html" style="color: var(--text-primary); text-decoration: none;">→ Ricci Tensor & Curvature</a></li>
                    </ul>
                </div>

                <div style="background: var(--bg-card); border: 2px solid rgba(255, 126, 182, 0.3); border-radius: 10px; padding: 1.25rem;">
                    <h4 style="color: #ff7eb6; margin-bottom: 0.75rem;">⚛️ Quantum Fields & Matter</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin: 0.5rem 0;"><a href="foundations/dirac-equation.html" style="color: var(--text-primary); text-decoration: none;">→ Dirac Equation (Fermions)</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/clifford-algebra.html" style="color: var(--text-primary); text-decoration: none;">→ Clifford Algebra (Spinors)</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/yang-mills.html" style="color: var(--text-primary); text-decoration: none;">→ Yang-Mills (Gauge Theory)</a></li>
                    </ul>
                </div>

                <div style="background: var(--bg-card); border: 2px solid rgba(79, 172, 254, 0.3); border-radius: 10px; padding: 1.25rem;">
                    <h4 style="color: #4facfe; margin-bottom: 0.75rem;">🔄 Extra Dimensions</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin: 0.5rem 0;"><a href="foundations/kaluza-klein.html" style="color: var(--text-primary); text-decoration: none;">→ Kaluza-Klein Theory</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/g2-manifolds.html" style="color: var(--text-primary); text-decoration: none;">→ G₂ Manifolds</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/calabi-yau.html" style="color: var(--text-primary); text-decoration: none;">→ Calabi-Yau Manifolds</a></li>
                    </ul>
                </div>

                <div style="background: var(--bg-card); border: 2px solid rgba(255, 193, 7, 0.3); border-radius: 10px; padding: 1.25rem;">
                    <h4 style="color: #ffc107; margin-bottom: 0.75rem;">🔬 Unification</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin: 0.5rem 0;"><a href="foundations/so10-gut.html" style="color: var(--text-primary); text-decoration: none;">→ SO(10) Grand Unification</a></li>
                    </ul>
                </div>

                <div style="background: var(--bg-card); border: 2px solid rgba(255, 126, 182, 0.3); border-radius: 10px; padding: 1.25rem;">
                    <h4 style="color: #ff7eb6; margin-bottom: 0.75rem;">⏰ Time & Entropy</h4>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin: 0.5rem 0;"><a href="foundations/boltzmann-entropy.html" style="color: var(--text-primary); text-decoration: none;">→ Boltzmann Entropy</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/kms-condition.html" style="color: var(--text-primary); text-decoration: none;">→ KMS Condition (Thermal States)</a></li>
                        <li style="margin: 0.5rem 0;"><a href="foundations/tomita-takesaki.html" style="color: var(--text-primary); text-decoration: none;">→ Tomita-Takesaki (Modular Time)</a></li>
                    </ul>
                </div>
            </div>

            <div style="text-align: center; margin-top: 2rem;">
                <a href="foundations/index.html" style="display: inline-block; padding: 1rem 2rem; background: linear-gradient(135deg, #51cf66, #4facfe); color: white; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 1.1rem;">
                    Browse All Foundation Topics →
                </a>
            </div>
        </div>
'''

# Insert before "Download This Guide"
download_section_marker = '<h2 style="margin-bottom: 1rem;">Download This Guide</h2>'
if download_section_marker in content:
    content = content.replace(download_section_marker, learn_more_section + '\n        ' + download_section_marker)

# Write back
with open('beginners-guide.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done: Added foundation links to beginners-guide.html")
