#!/usr/bin/env python3
"""Update cosmology.html for Update1-8 integration"""

import re

# Read the file
with open('h:/Github/PrincipiaMetaphysica/sections/cosmology.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the old section to replace (simplified potential)
old_section = '''        <div class="equation-box numbered">
          <span class="eq-content">
            V(&sigma;, &chi;) = V<sub>flux</sub>(&sigma;) + V<sub>Casimir</sub>(&sigma;) +
            V<sub>np</sub>(&chi;)e<sup>-a&sigma;</sup>
          </span>
          <span class="eq-number">(6.10)</span>
        </div>

        <p>
          While &sigma; is stabilized at high mass, the Mashiach field &chi; acquires a very flat
          potential, allowing it to remain dynamical and drive late-time acceleration.
        </p>'''

# Define the new section (full Update1-8 potential)
new_section = '''        <div class="interactive-formula" style="background: rgba(139, 127, 255, 0.1); border: 1px solid rgba(139, 127, 255, 0.2); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;">
          <span class="formula-hint">Hover for variable definitions</span>
          <div class="formula-display" style="justify-content: center; gap: 0.5rem; flex-wrap: wrap; font-size: 1.2rem;">
            <span class="formula-var">V(&phi;)
              <div class="var-tooltip">
                <div class="var-name">V(&phi;) — Moduli Potential</div>
                <div class="var-description">Full moduli potential including flux, non-perturbative, and orthogonal sector contributions</div>
                <div class="var-units">Energy<sup>4</sup></div>
              </div>
            </span>
            <span class="formula-op">=</span>
            <span class="formula-var" style="color: #ff7eb6;">|F|<sup>2</sup>e<sup>-a&phi;</sup>
              <div class="var-tooltip">
                <div class="var-name">|F|<sup>2</sup>e<sup>-a&phi;</sup> — Flux Term</div>
                <div class="var-description">KKLT-type flux compactification contribution with swampland parameter a</div>
                <div class="var-contribution">Stabilizes volume modulus at large &phi;; F is the flux superpotential</div>
              </div>
            </span>
            <span class="formula-op">+</span>
            <span class="formula-var" style="color: #51cf66;">&kappa;e<sup>-b/&phi;</sup>
              <div class="var-tooltip">
                <div class="var-name">&kappa;e<sup>-b/&phi;</sup> — Non-Perturbative Term</div>
                <div class="var-description">Gaugino condensation or D-brane instantons from SO(10) sector</div>
                <div class="var-contribution">Lifts flat directions; &kappa; ~ M<sub>Planck</sub><sup>4</sup>, b ~ 8&pi;<sup>2</sup>/g<sup>2</sup></div>
              </div>
            </span>
            <span class="formula-op">+</span>
            <span class="formula-var" style="color: #4facfe;">&mu;cos(&phi;/R<sub>ortho</sub>)
              <div class="var-tooltip">
                <div class="var-name">&mu;cos(&phi;/R<sub>ortho</sub>) — Orthogonal Sector</div>
                <div class="var-description">Periodic contribution from orthogonal time sector in 26D framework</div>
                <div class="var-contribution">R<sub>ortho</sub> is the compactification radius of the mirror sector</div>
              </div>
            </span>
          </div>
          <div class="formula-label" style="text-align: center; margin-top: 0.75rem; color: var(--text-muted);">(6.10) Full Moduli Potential (Update1-8)</div>
        </div>

        <p>
          This is the <strong>complete moduli potential</strong> combining three fundamental contributions:
        </p>

        <ul>
          <li><strong>Flux term:</strong> The factor e<sup>-a&phi;</sup> with <strong>swampland parameter a = &radic;(26/13) &asymp; 1.414</strong> arises from the dimensional structure: 26 total dimensions with 13 spacetime dimensions per sector</li>
          <li><strong>Non-perturbative term:</strong> Exponentially suppressed at large &phi;, dominates at small field values</li>
          <li><strong>Orthogonal sector:</strong> The periodic term reflects the discrete symmetries of the mirror sector compactification</li>
        </ul>

        <div class="theorem-box" style="background: rgba(81, 207, 102, 0.1); border-left: 4px solid #51cf66;">
          <h5>Moduli Minimization</h5>
          <p>The vacuum of the theory is determined by minimizing the potential:</p>
          <div class="equation-box">
            <span class="eq-content">
              dV/d&phi; = 0 &nbsp;&nbsp;&nbsp;and&nbsp;&nbsp;&nbsp; d<sup>2</sup>V/d&phi;<sup>2</sup> &gt; 0
            </span>
          </div>
          <p>
            <strong>Numerical solution:</strong> &phi;<sub>min</sub> &asymp; 0.781 (in Planck units)
          </p>
          <p>
            The Hessian stability condition ensures the minimum is stable against small perturbations.
            The mass of fluctuations around the minimum is m<sup>2</sup> = d<sup>2</sup>V/d&phi;<sup>2</sup>|<sub>&phi;=&phi;<sub>min</sub></sub>.
          </p>
        </div>

        <p>
          While the heavy modulus &sigma; is stabilized at high mass (m<sub>&sigma;</sub> ~ M<sub>GUT</sub>), the Mashiach field &chi; acquires a very flat
          potential along a particular direction in moduli space, allowing it to remain dynamical and drive late-time acceleration.
          This hierarchical stabilization naturally explains why one modulus remains light while others are heavy.
        </p>'''

# Replace the section
if old_section in content:
    content = content.replace(old_section, new_section)
    print("[OK] Replaced moduli potential section")
else:
    print("[ERROR] Could not find old section to replace")
    exit(1)

# Now add CMB bubble nucleation and landscape statistics references
# Find the section after moduli minimization to add these

# Add CMB connection near the Mashiach evolution diagram caption
old_caption = '''        <div class="diagram-caption">
          The Mashiach field &phi;<sub>M</sub> evolves through cosmic history, starting frozen during inflation,
          oscillating in radiation era, and finally slow-rolling toward a late-time attractor with w &rarr; -1.
          This provides a dynamical explanation for dark energy consistent with DESI 2024 observations.
        </div>'''

new_caption = '''        <div class="diagram-caption">
          The Mashiach field &phi;<sub>M</sub> evolves through cosmic history, starting frozen during inflation,
          oscillating in radiation era, and finally slow-rolling toward a late-time attractor with w &rarr; -1.
          This provides a dynamical explanation for dark energy consistent with DESI 2024 observations.
          The initial conditions for &phi;<sub>M</sub> are set by <strong>CMB bubble nucleation</strong> during the early universe phase transition.
        </div>'''

if old_caption in content:
    content = content.replace(old_caption, new_caption)
    print("[OK] Added CMB bubble nucleation reference")
else:
    print("[WARN] Could not find diagram caption to update")

# Add landscape statistics reference in the modulus stabilization section
# Find "Stabilization Mechanisms" and add landscape info
old_stabilization_end = '''          </ul>
        </div>

        <p>
          The combined potential has the form:
        </p>'''

new_stabilization_end = '''          </ul>
          <p style="margin-top: 1rem; font-size: 0.95rem; color: var(--text-secondary);">
            <strong>Landscape statistics:</strong> The string landscape contains approximately <strong>~10<sup>500</sup> metastable vacua</strong>
            arising from different flux configurations. The observed vacuum is selected by anthropic considerations
            (see Section 8 for detailed statistical analysis).
          </p>
        </div>

        <p>
          The combined potential has the form:
        </p>'''

if old_stabilization_end in content:
    content = content.replace(old_stabilization_end, new_stabilization_end)
    print("[OK] Added landscape statistics reference")
else:
    print("[WARN] Could not find stabilization section to update")

# Add QuTiP reference in open questions
old_question = '''          <li>How does the Mashiach potential connect to fundamental parameters of K<sub>Pneuma</sub>?</li>'''

new_question = '''          <li>How does the Mashiach potential connect to fundamental parameters of K<sub>Pneuma</sub>?</li>
          <li><strong>Computational:</strong> See Appendix D for QuTiP-based numerical simulation of moduli dynamics and stabilization</li>'''

if old_question in content:
    content = content.replace(old_question, new_question)
    print("[OK] Added QuTiP simulation reference")
else:
    print("[WARN] Could not find open questions section to update")

# Write the updated content
with open('h:/Github/PrincipiaMetaphysica/sections/cosmology.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("
[OK] cosmology.html updated successfully with Update1-8 integration")
