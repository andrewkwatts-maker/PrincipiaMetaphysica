#!/usr/bin/env python3
"""
Systematic update script for converting theory sections from CY4 to G₂ manifold framework.
Updates all HTML files in sections/ folder to reflect the new dimensional structure:
26D (24,2) → 13D (12,1) → 7D G₂ → 6D (5,1) effective
"""

import re
import os
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).parent
SECTIONS_DIR = BASE_DIR / "sections"

# Track all changes for logging
changes_log = []

def log_change(filename, line_num, old_text, new_text, reason):
    """Log a change for the update report"""
    changes_log.append({
        'file': filename,
        'line': line_num,
        'old': old_text[:100],  # Truncate for readability
        'new': new_text[:100],
        'reason': reason
    })

def update_toc_references(content, filename):
    """Update table of contents references from CY4 to G₂"""
    replacements = [
        (r'The Pneuma Manifold: CY4 with F-Theory Structure',
         'The Pneuma Manifold: G₂ Manifold with F-Theory Connection',
         'Update TOC - main heading'),
        (r'Corrected CY4 Construction \(χ = 72\)',
         'G₂ Topology (χ_eff = 72)',
         'Update TOC - construction section'),
        (r'D<sub>5</sub> Singularity and SO\(10\)',
         'D<sub>5</sub> Singularity from G₂ and SO(10)',
         'Update TOC - SO(10) origin'),
    ]

    for old, new, reason in replacements:
        if re.search(old, content):
            content = re.sub(old, new, content)
            log_change(filename, 0, old, new, reason)

    return content

def update_dimensional_structure(content, filename):
    """Update dimensional reduction pathway"""
    replacements = [
        # Compactification pathway
        (r'26D.*?→.*?13D.*?→.*?4D',
         '26D (24,2) → 13D (12,1) → 7D G₂ → 6D (5,1) effective → 4D',
         'Update compactification pathway'),

        # 8D to 7D manifold references
        (r'8-dimensional internal Calabi-Yau four-fold',
         '7-dimensional G₂ manifold',
         'Replace CY4 with G₂'),
        (r'8D Internal Manifold',
         '7D G₂ Manifold',
         'Update diagram labels'),
        (r'8D internal manifold',
         '7D G₂ manifold',
         'Update text references'),

        # Specific CY4 replacements (but not all - keep some historical context)
        (r'Calabi-Yau four-fold K<sub>Pneuma</sub>',
         'G₂ manifold K<sub>Pneuma</sub>',
         'Update manifold type'),
        (r'The Calabi-Yau four-fold K<sub>Pneuma</sub>',
         'The G₂ manifold K<sub>Pneuma</sub>',
         'Update manifold type'),

        # 5D to 6D effective bulk
        (r'5D effective bulk',
         '6D effective bulk',
         'Update effective dimension'),
        (r'5D bulk',
         '6D bulk',
         'Update bulk dimension'),

        # Octonion dimension (8D remains for division algebra, but manifold changes)
        (r'8-dimensional internal Calabi-Yau',
         '7-dimensional G₂',
         'Update internal manifold'),
    ]

    for old, new, reason in replacements:
        if re.search(old, content, re.IGNORECASE):
            content = re.sub(old, new, content, flags=re.IGNORECASE)
            log_change(filename, 0, old, new, reason)

    return content

def update_euler_characteristic(content, filename):
    """Update Euler characteristic formulas for G₂"""
    replacements = [
        # Update generation count formula
        (r'n<sub>gen</sub> = χ\(CY4\) / 24',
         'n<sub>gen</sub> = χ_eff(G₂) / (24 × Z₂) = 144 / 48 = 3',
         'Update generation formula for G₂'),
        (r'χ\(CY4\) / 24 = 72 / 24 = 3',
         'χ_eff(G₂) / (24 × Z₂) = 144 / 48 = 3',
         'Update specific calculation'),

        # Update Euler characteristic discussion
        (r'Euler characteristic of the Calabi-Yau four-fold',
         'Effective Euler characteristic of the G₂ manifold (flux-dressed)',
         'Update χ description'),
    ]

    for old, new, reason in replacements:
        if re.search(old, content):
            content = re.sub(old, new, content)
            log_change(filename, 0, old, new, reason)

    return content

def update_so10_origin(content, filename):
    """Update SO(10) origin from CY4 D5 singularity to G₂ singularity"""
    replacements = [
        (r'SO\(10\) gauge symmetry from CY4 D₅ singularities',
         'SO(10) gauge symmetry from G₂ ADE singularities (D₅-type)',
         'Update SO(10) origin'),
        (r'D₅ singularity in the CY4',
         'D₅-type singularity in the G₂ manifold',
         'Update singularity location'),
        (r'7-branes wrap the singular locus',
         'G₂ singularities enhance gauge symmetry',
         'Update mechanism'),
    ]

    for old, new, reason in replacements:
        if re.search(old, content):
            content = re.sub(old, new, content)
            log_change(filename, 0, old, new, reason)

    return content

def add_g2_properties_section(content, filename):
    """Add a new section explaining G₂ manifold properties"""
    # Look for the section after the Pneuma Manifold heading
    g2_section = """
            <div class="highlight-box">
                <h4>G₂ Manifold Properties</h4>
                <p>
                    The 7-dimensional G₂ manifold is characterized by:
                </p>
                <ul class="concept-list">
                    <li><strong>Holonomy group:</strong> G₂ ⊂ SO(7) - exceptional holonomy preserving one Majorana spinor</li>
                    <li><strong>Euler characteristic:</strong> χ(G₂) = 0 generically, but flux dressing yields χ_eff = 72</li>
                    <li><strong>Singularities:</strong> Can develop ADE-type singularities → gauge enhancement (SO(10) from D₅-type)</li>
                    <li><strong>Spinor content:</strong> Exactly one Majorana spinor (8 real components) - connects naturally to Pneuma</li>
                    <li><strong>Metric:</strong> Ricci-flat with special 3-form structure φ, satisfying dφ = 0 and d*φ = 0</li>
                </ul>
            </div>
"""

    # Insert after the main Pneuma Manifold section header
    pattern = r'(<h2>The Pneuma Manifold:.*?</h2>)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1\n' + g2_section, content, count=1)
        log_change(filename, 0, '[Section header]', '[Added G₂ properties]', 'Add G₂ manifold properties')

    return content

def add_warping_discussion(content, filename):
    """Add Randall-Sundrum warping mechanism"""
    warping_section = """
            <div class="subsection">
                <h3>Warping and Hierarchy Generation</h3>
                <p>
                    The 6D effective spacetime exhibits <strong>Randall-Sundrum type warping</strong> in the shared extra dimensions:
                </p>
                <div class="equation-box">
                    ds²<sub>6</sub> = e<sup>-2ky</sup> η<sub>μν</sub> dx<sup>μ</sup> dx<sup>ν</sup> + dy² + dz²
                    <span class="equation-label">Warped 6D metric</span>
                </div>
                <p>
                    where k ~ 35 is the curvature scale. The exponential warping factor e<sup>-kπR</sup> ~ 10<sup>-16</sup>
                    naturally generates the Planck-TeV hierarchy. The φ_M (Mashiach) field propagates in this 6D bulk,
                    with KK modes at M_KK ~ 5 TeV.
                </p>
            </div>
"""

    # Insert before the Kaluza-Klein Decomposition section
    pattern = r'(<section id="kk-decomposition")'
    if re.search(pattern, content):
        content = re.sub(pattern, warping_section + r'\n\1', content, count=1)
        log_change(filename, 0, '[Before KK section]', '[Added warping]', 'Add warping mechanism')

    return content

def add_heterogeneous_branes(content, filename):
    """Add section on heterogeneous brane structure"""
    brane_section = """
            <div class="highlight-box">
                <h4>Heterogeneous Brane Structure</h4>
                <p>
                    The dimensional structure explains why our 4D brane sees <strong>(5,1) = 4D_common + 2D_shared</strong>
                    while shadow branes see only <strong>(3,1) = 4D_common</strong>:
                </p>
                <ul class="concept-list">
                    <li><strong>Observable brane:</strong> Couples to all 6D bulk dimensions → sees (5,1) effective</li>
                    <li><strong>Shadow branes (×3):</strong> Localized on domain walls → see only 4D_common</li>
                    <li><strong>KK gravitons:</strong> Propagate in 6D bulk → universally coupled (testable at 5 TeV!)</li>
                    <li><strong>φ_M field:</strong> 6D bulk scalar → generates dark energy</li>
                </ul>
            </div>
"""

    # Insert after the brane hierarchy discussion
    pattern = r'(1 \+ 3 brane structure provides)'
    if re.search(pattern, content):
        content = re.sub(pattern, brane_section + r'\n\1', content, count=1)
        log_change(filename, 0, '[Before brane structure]', '[Added heterogeneous branes]', 'Add heterogeneous brane explanation')

    return content

def update_file(filepath):
    """Update a single HTML file"""
    print(f"Processing {filepath.name}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply all transformations
        content = update_toc_references(content, filepath.name)
        content = update_dimensional_structure(content, filepath.name)
        content = update_euler_characteristic(content, filepath.name)
        content = update_so10_origin(content, filepath.name)

        # Add new sections (only for geometric-framework.html)
        if filepath.name == 'geometric-framework.html':
            content = add_g2_properties_section(content, filepath.name)
            content = add_warping_discussion(content, filepath.name)
            content = add_heterogeneous_branes(content, filepath.name)

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [OK] Updated {filepath.name}")
            return True
        else:
            print(f"  [-] No changes needed for {filepath.name}")
            return False

    except Exception as e:
        print(f"  [ERROR] Error processing {filepath.name}: {e}")
        return False

def generate_log():
    """Generate the update log markdown file"""
    log_path = BASE_DIR / "SECTIONS_UPDATE_LOG.md"

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("# Sections Update Log: CY4 -> G2 Framework\n\n")
        f.write("## Summary\n\n")
        f.write("Systematic updates to convert theory sections from 8D Calabi-Yau four-fold (CY4) ")
        f.write("to 7D G2 manifold framework.\n\n")
        f.write("### Dimensional Structure Update\n\n")
        f.write("```\n")
        f.write("OLD: 26D (24,2) -> 13D (12,1) -> 8D CY4 -> 5D effective -> 4D\n")
        f.write("NEW: 26D (24,2) -> 13D (12,1) -> 7D G2 -> 6D (5,1) effective -> 4D\n")
        f.write("```\n\n")
        f.write("### Key Changes\n\n")
        f.write("1. **Internal manifold**: 8D Calabi-Yau four-fold -> 7D G2 manifold\n")
        f.write("2. **Effective bulk**: 5D -> 6D with warping\n")
        f.write("3. **SO(10) origin**: CY4 D5 singularities -> G2 ADE singularities (D5-type)\n")
        f.write("4. **Generation count**: chi(CY4)/24 -> chi_eff(G2)/(24xZ2) = 144/48 = 3\n")
        f.write("5. **Heterogeneous branes**: Observable (5,1) vs Shadows (3,1)\n")
        f.write("6. **Warping added**: Randall-Sundrum mechanism in 6D bulk\n\n")
        f.write("## Detailed Changes\n\n")

        # Group changes by file
        by_file = {}
        for change in changes_log:
            fname = change['file']
            if fname not in by_file:
                by_file[fname] = []
            by_file[fname].append(change)

        for fname in sorted(by_file.keys()):
            f.write(f"### {fname}\n\n")
            for change in by_file[fname]:
                f.write(f"**{change['reason']}**\n\n")
                f.write(f"- Old: `{change['old']}`\n")
                f.write(f"- New: `{change['new']}`\n\n")

    print(f"\n[OK] Generated update log: {log_path}")

def main():
    """Main update process"""
    print("=" * 60)
    print("SECTIONS UPDATE: CY4 -> G2 Framework")
    print("=" * 60)
    print()

    # Get all HTML files in sections/
    html_files = sorted(SECTIONS_DIR.glob("*.html"))

    # Priority order
    priority_files = [
        'geometric-framework.html',
        'cosmology.html',
        'gauge-unification.html',
        'fermion-sector.html',
        'thermal-time.html',
        'pneuma-lagrangian.html',
        'pneuma-lagrangian-new.html',
        'predictions.html',
        'conclusion.html',
    ]

    updated_count = 0

    # Process priority files first
    for fname in priority_files:
        fpath = SECTIONS_DIR / fname
        if fpath.exists():
            if update_file(fpath):
                updated_count += 1

    # Process remaining files
    for fpath in html_files:
        if fpath.name not in priority_files:
            if update_file(fpath):
                updated_count += 1

    print()
    print("=" * 60)
    print(f"Update complete: {updated_count} files modified")
    print("=" * 60)

    # Generate log
    if changes_log:
        generate_log()

if __name__ == '__main__':
    main()
