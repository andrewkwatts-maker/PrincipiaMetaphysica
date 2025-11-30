#!/usr/bin/env python3
"""Update principia-metaphysica-paper.html to current 26D→13D→6D→4D framework"""

import re

# Read the paper
with open('principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define systematic replacements
replacements = [
    # Core framework updates
    (r'14D×2', '13D shadow'),
    (r'14-dimensional', '13-dimensional shadow'),
    (r'two coupled 14-dimensional "halves"', 'a 13-dimensional shadow manifold with signature (12,1)'),
    (r'two 14D halves', '13D shadow (from 26D bulk)'),
    (r'M¹⁴_A ⊗ M¹⁴_B', '13D shadow with signature (12,1)'),

    # Signature updates
    (r'signature \(12,2\)', 'signature (12,1)'),
    (r'\(12,2\) with <strong>2 shared timelike dimensions</strong>', '(12,1) with 1 effective timelike dimension after Sp(2,R) gauge fixing'),

    # χ_eff derivation updates - ALL instances
    (r'13D shadow mirror symmetry: 72 \+ 72',
     'flux-dressed G₂ topology'),
    (r'mirror symmetry: 72 \+ 72',
     'flux-dressed G₂ compactification'),
    (r'χ<sub>eff</sub> = 144 \(from flux-dressed G₂ topology\)',
     'χ<sub>eff</sub> = 144 (from flux-dressed G₂ topology)'),
    (r'from the 14D×2 decomposition',
     'from G₂ compactification with flux dressing'),
    (r'14D×2 mirror structure: χ<sub>A</sub> \+ χ<sub>B</sub> = 72 \+ 72',
     'flux-dressed G₂ topology: χ<sub>eff</sub> = 144'),
    (r'χ<sub>A</sub> \+ χ<sub>B</sub> = 72 \+ 72 = 144',
     'χ<sub>eff</sub> = 144 from G₂ manifold with flux contributions'),
    (r'χ<sub>eff</sub> = 144 from 14D×2 mirror symmetry',
     'χ<sub>eff</sub> = 144 from flux-dressed G₂ compactification'),
    (r'arises from the 13D shadow decomposition with appropriate flux dressing',
     'arises from the G₂ manifold topology with flux dressing'),
    (r'flux-dressed topology from flux-dressed G₂ compactification',
     'flux-dressed G₂ topology'),

    # Action and structure updates
    (r'S<sub>A,B</sub> are 14D Einstein-Hilbert actions',
     'the action includes the 13D Einstein-Hilbert term with Sp(2,R) gauge structure'),
    (r'14D×2 structure preserves anomaly cancellation',
     '13D shadow structure from Sp(2,R) gauge fixing preserves unitarity and anomaly cancellation'),

    # TOC update
    (r'The 26D→14D×2 Two-Time Structure',
     'The 26D→13D Shadow via Sp(2,R) Gauge Fixing'),
    (r'14D×2 Decomposition \(Shared Time Framework\)',
     '26D→13D Projection via Sp(2,R) Gauge Symmetry'),

    # Section heading
    (r'<h4 id="14d-halves">2\.1\.3 The 26D→14D×2 Two-Time Structure \(Enhanced Framework\)</h4>',
     '<h4 id="13d-shadow">2.1.3 The 26D→13D Shadow via Sp(2,R) Gauge Fixing</h4>'),
]

# Apply all replacements
for old, new in replacements:
    content = re.sub(old, new, content, flags=re.IGNORECASE if '14D' in old else 0)

# Update the main framework description paragraph
old_framework = r'''Building on Bars' two-time \(2T\) physics framework, the 26D bulk decomposes into <strong>a 13-dimensional shadow manifold with signature \(12,1\)</strong>,
            each with signature \(12,1\) and sharing <strong>2 timelike dimensions</strong> \(thermal time t<sub>therm</sub> and orthogonal time t<sub>ortho</sub>\)\.
            This "dimensional democracy" provides gauge redundancy that stabilizes the higher-dimensional theory while allowing
            dimensional reduction to observable 4D spacetime through <strong>G<sub>2</sub> compactification</strong>\.'''

new_framework = '''Building on Bars' two-time (2T) physics framework, the 26D bulk with signature (24,2) undergoes
            <strong>Sp(2,R) gauge fixing</strong> to project to a <strong>13D shadow manifold with signature (12,1)</strong>.
            This gauge symmetry removes ghost states that would arise from having 2 timelike dimensions in the bulk,
            leaving 1 effective timelike dimension in the shadow. The 13D manifold then undergoes
            <strong>G₂ compactification</strong> (7D compact manifold) to yield a 6D bulk with signature (5,1),
            which further reduces to our observable 4D spacetime (3,1) plus 3 shadow 4D branes.'''

content = re.sub(old_framework, new_framework, content, flags=re.DOTALL)

# Update the formula box
old_formula_box = r'''<div class="formula-def-title">26D→13D Projection via Sp\(2,R\) Gauge Symmetry</div>
            <div class="math-block">
                <div class="formula-line">
                    M<sup>26</sup> = 13D shadow with signature \(12,1\)
                </div>'''

new_formula_box = '''<div class="formula-def-title">26D→13D Projection via Sp(2,R) Gauge Symmetry</div>
            <div class="math-block">
                <div class="formula-line">
                    M<sup>26</sup> (24,2) → Sp(2,R) gauge fixing → M<sup>13</sup> (12,1)
                </div>'''

content = re.sub(old_formula_box, new_formula_box, content, flags=re.DOTALL)

# Update shared time explanation
old_shared = r'''<strong>Shared timelike dimensions:</strong> Both halves share 2 times: thermal time t<sub>therm</sub> \(entropy-driven\) and t<sub>ortho</sub> \(gauge freedom\)\. The Sp\(2,R\) symmetry rotates these times, providing gauge redundancy that eliminates ghosts\.'''

new_shared = '''<strong>Gauge fixing to 1 time:</strong> The 26D bulk has 2 timelike dimensions (signature 24,2), but
                    Sp(2,R) gauge symmetry projects this to 1 effective timelike dimension in the 13D shadow (signature 12,1).
                    This gauge fixing eliminates ghost states while preserving unitarity.'''

content = re.sub(old_shared, new_shared, content)

# Update the action description
old_action = r'''where the action includes the 13D Einstein-Hilbert term with Sp\(2,R\) gauge structure couples the halves
            via G<sub>2</sub> holonomy-preserving terms\.'''

new_action = '''where S₁₃D is the 13D Einstein-Hilbert action with Sp(2,R) gauge structure,
            and S_G₂ describes the compactification on the 7D G₂ manifold.'''

content = re.sub(old_action, new_action, content)

# Write the updated paper
with open('principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done: Updated paper to current framework")
print("- Removed all 14D x 2 references")
print("- Updated to 26D -> Sp(2,R) -> 13D -> G2 -> 6D -> 4D")
print("- Fixed chi_eff = 144 derivation (flux-dressed G2, not mirror symmetry)")
print("- Updated signatures: (24,2) -> (12,1) -> (5,1) -> (3,1)")
