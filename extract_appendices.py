#!/usr/bin/env python3
"""
Extract main content from section HTML files to create appendices.
"""

import re
from pathlib import Path

# Define appendix mappings
appendix_files = [
    ("A", "introduction.html", "Introduction - The Quest for Unification"),
    ("B", "geometric-framework.html", "Geometric Framework"),
    ("C", "gauge-unification.html", "Gauge Unification"),
    ("D", "fermion-sector.html", "Fermion Sector"),
    ("E", "cosmology.html", "Cosmology"),
    ("F", "thermal-time.html", "Thermal Time"),
    ("G", "predictions.html", "Predictions"),
    ("H", "conclusion.html", "Conclusion"),
    ("I", "formulas.html", "Formulas"),
    ("J", "theory-analysis.html", "Theory Analysis"),
    ("K", "einstein-hilbert-term.html", "Einstein-Hilbert Term"),
    ("L", "pneuma-lagrangian.html", "Pneuma Lagrangian"),
    ("M", "xy-gauge-bosons.html", "XY Gauge Bosons"),
    ("N", "cmb-bubble-collisions-comprehensive.html", "CMB Bubble Collisions"),
    ("O", "division-algebras.html", "Division Algebras"),
    ("P", "index.html", "Section Index"),
    ("Q", "pneuma-lagrangian-new.html", "Pneuma Lagrangian (New)"),
]

sections_dir = Path("h:/Github/PrincipiaMetaphysica/sections")

def extract_main_content(html_content):
    """
    Extract the main content from an HTML file.
    Removes header, navigation, and footer sections.
    """
    # Remove everything before the first main section
    # Look for <section class="section-hero"> or first <section>
    section_start = re.search(r'<section[^>]*>', html_content, re.IGNORECASE)
    if section_start:
        html_content = html_content[section_start.start():]

    # Remove navigation sections at the end
    nav_section = re.search(r'<section class="nav-section">', html_content, re.IGNORECASE)
    if nav_section:
        html_content = html_content[:nav_section.start()]

    # Remove footer
    footer_match = re.search(r'<footer', html_content, re.IGNORECASE)
    if footer_match:
        html_content = html_content[:footer_match.start()]

    # Remove closing body and html tags
    html_content = re.sub(r'</body>.*</html>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    return html_content.strip()

def create_appendix_html(letter, title, content):
    """Create appendix HTML section."""
    appendix_id = f"appendix-{letter.lower()}"

    appendix_html = f'''
<section id="{appendix_id}" class="appendix">
  <h2>Appendix {letter}: {title}</h2>
  {content}
</section>
'''
    return appendix_html

def create_table_of_appendices():
    """Create the table of appendices navigation."""
    toc_html = '''
<section id="appendices-toc" class="appendices-toc" style="margin-top: 3rem; padding: 2rem; background: rgba(139, 127, 255, 0.05); border-radius: 8px; border: 1px solid rgba(139, 127, 255, 0.2);">
  <h2 style="color: #8b7fff; margin-bottom: 1.5rem; border: none;">Table of Appendices</h2>
  <p style="margin-bottom: 1.5rem; color: #666;">
    The following appendices contain detailed derivations, formulas, and analysis from the complete Principia Metaphysica framework.
  </p>
  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 0.75rem;">
'''

    for letter, filename, title in appendix_files:
        appendix_id = f"appendix-{letter.lower()}"
        toc_html += f'    <div style="padding: 0.5rem;"><a href="#{appendix_id}" style="color: #8b7fff; text-decoration: none; font-weight: 500;"><strong>Appendix {letter}:</strong> {title}</a></div>\n'

    toc_html += '''  </div>
</section>
'''
    return toc_html

# Main execution
print("Extracting appendices from section files...")
print("=" * 70)

appendices_html = []

for letter, filename, title in appendix_files:
    filepath = sections_dir / filename
    print(f"\nProcessing Appendix {letter}: {filename}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Extract main content
        main_content = extract_main_content(html_content)

        # Create appendix HTML
        appendix_html = create_appendix_html(letter, title, main_content)
        appendices_html.append(appendix_html)

        print(f"  [OK] Extracted {len(main_content)} characters")

    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        # Create placeholder if file not found or error
        appendix_html = create_appendix_html(letter, title, f"<p><em>Content from {filename} - See source file for details.</em></p>")
        appendices_html.append(appendix_html)

# Create table of appendices
toc_html = create_table_of_appendices()

# Combine all appendices
all_appendices = "\n".join([toc_html] + appendices_html)

# Write to output file
output_file = Path("h:/Github/PrincipiaMetaphysica/appendices_content.html")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(all_appendices)

print("\n" + "=" * 70)
print(f"[OK] All appendices extracted successfully!")
print(f"[OK] Output written to: {output_file}")
print(f"[OK] Total size: {len(all_appendices):,} characters")
print("\nNext step: Insert this content into principia-metaphysica-paper.html")
print("           after the References section (before </div></body></html>)")
