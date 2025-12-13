#!/usr/bin/env python3
"""
Fix formatting issues in principia-metaphysica-paper.html
"""

import re

def fix_paper_formatting(file_path):
    """Apply all formatting fixes to the paper"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track changes
    changes = []

    # 1. Remove version references
    # Fix "V12.8 Final Transparency Statement"
    old = r'<strong>V12\.8 Final Transparency Statement:</strong>'
    new = r'<strong>Transparency Statement:</strong>'
    if re.search(old, content):
        content = re.sub(old, new, content)
        changes.append("Removed 'V12.8' from Transparency Statement")

    # Fix "V12.8 Final Transparency Report"
    old = r'V12\.8 Final Transparency Report'
    new = r'Final Transparency Report'
    count = len(re.findall(old, content))
    if count > 0:
        content = re.sub(old, new, content)
        changes.append(f"Removed 'V12.8' from Transparency Report ({count} instances)")

    # Fix "v12.7+ achieves"
    old = r'\(v12\.7\+ achieves ~100% geometric rigor with minimal phenomenological inputs\)'
    new = r'(achieves ~100% geometric rigor with minimal phenomenological inputs)'
    if re.search(old, content):
        content = re.sub(old, new, content)
        changes.append("Removed 'v12.7+' version reference")

    # Remove other V12.8 references from main body (before appendices ~line 9500)
    # Line 2455: "V12.8 Fix:"
    old = r'\(V12\.8 Fix: Z2 parity from Sp\(2,R\) gauge fixing doubles the F-theory divisor 24 to 48; see <code>simulations/zero_modes_gen_v12_8\.py</code>\)'
    new = r'(Z2 parity from Sp(2,R) gauge fixing doubles the F-theory divisor 24 to 48)'
    count = len(re.findall(old, content))
    if count > 0:
        content = re.sub(old, new, content)
        changes.append(f"Removed V12.8 Fix reference from generation formula ({count} instances)")

    # Line 4500: "[V12.8 Note:"
    old = r'\[V12\.8 Note: TCS G₂ manifolds are Ricci-flat, so T_omega is an effective torsion from G-flux contributions, not geometric torsion\. The value T_omega_eff = -b₃/27\.2 ≈ -0\.882 comes from flux quantization via b₃ = 24; see <code>simulations/torsion_effective_v12_8\.py</code>\.\]'
    new = r'[Note: TCS G₂ manifolds are Ricci-flat, so T_omega is an effective torsion from G-flux contributions, not geometric torsion. The value T_omega_eff = -b₃/27.2 ≈ -0.882 comes from flux quantization via b₃ = 24.]'
    count = len(re.findall(old, content))
    if count > 0:
        content = re.sub(old, new, content)
        changes.append(f"Removed V12.8 Note reference from torsion section ({count} instances)")

    # Line 6340: "V12.8 Fix" in heading
    old = r'Maximal Mixing from G2 Holonomy Symmetry \(V12\.8 Fix\)'
    new = r'Maximal Mixing from G2 Holonomy Symmetry'
    count = len(re.findall(old, content))
    if count > 0:
        content = re.sub(old, new, content)
        changes.append(f"Removed V12.8 Fix from section heading ({count} instances)")

    # Line 7636: "V12.8 transparency update"
    old = r'\(V12\.8 transparency update\)'
    new = r''
    count = len(re.findall(old, content))
    if count > 0:
        content = re.sub(old, new, content)
        changes.append(f"Removed V12.8 transparency update reference ({count} instances)")

    # 2. Fix Master Action formula card - broken category label
    # The problem is at line ~46302 where it shows:
    # ( <span class="pm-value" data-category="proton_decay" ... data-param="s_parameter"> ) Master Action
    # This should just be "Master 13D Action" with proper styling

    old_pattern = '''    <div class="formula-card">
     <div class="formula-header">
      <span class="formula-label">
       (
       <span class="pm-value" data-category="proton_decay" data-format="fixed:1" data-param="s_parameter">
       </span>
       ) Master Action
      </span>
      <span class="formula-status status-established">
       FOUNDATIONAL
      </span>
     </div>'''

    new_pattern = '''    <div class="formula-card" style="background: rgba(139, 127, 255, 0.08); backdrop-filter: blur(10px); border: 1px solid rgba(139, 127, 255, 0.3); border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
     <div class="formula-header" style="margin-bottom: 1rem;">
      <h4 style="color: #8b7fff; margin: 0;">
       Master 13D Action <span style="background: rgba(81, 207, 102, 0.2); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 0.5rem;">FOUNDATIONAL</span>
      </h4>
     </div>'''

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        changes.append("Fixed Master Action formula card header with frosted glass styling")

    # 3. Fix Full Lagrangian F(R,T,tau) formula card - also has broken category label
    old_pattern2 = '''    <div class="formula-card">
     <div class="formula-header">
      <span class="formula-label">
       (
       <span class="pm-value" data-category="pmns_matrix" data-format="fixed:1" data-param="theta_12_error">
       </span>
       ) Full Lagrangian F(R,T,tau)
      </span>
      <span class="formula-status status-established">
       FOUNDATIONAL
      </span>
     </div>'''

    new_pattern2 = '''    <div class="formula-card" style="background: rgba(139, 127, 255, 0.08); backdrop-filter: blur(10px); border: 1px solid rgba(139, 127, 255, 0.3); border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
     <div class="formula-header" style="margin-bottom: 1rem;">
      <h4 style="color: #8b7fff; margin: 0;">
       Full Lagrangian F(R,T,τ) <span style="background: rgba(81, 207, 102, 0.2); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 0.5rem;">FOUNDATIONAL</span>
      </h4>
     </div>'''

    if old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern2)
        changes.append("Fixed Full Lagrangian F(R,T,τ) formula card header with frosted glass styling")

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return changes

if __name__ == '__main__':
    file_path = 'H:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html'
    changes = fix_paper_formatting(file_path)

    print("Applied fixes:")
    for i, change in enumerate(changes, 1):
        # Replace Greek characters with ASCII for console output
        change_ascii = change.replace('τ', 'tau')
        print(f"  {i}. {change_ascii}")

    if not changes:
        print("  No changes needed.")
