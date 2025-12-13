#!/usr/bin/env python3
"""Fix Appendix O with correct content from division-algebra-section.html"""

import re
from pathlib import Path

# Read the division algebra section
division_file = Path("h:/Github/PrincipiaMetaphysica/sections/division-algebra-section.html")
with open(division_file, 'r', encoding='utf-8') as f:
    div_content = f.read()

# Extract main content (everything is the content in this case, just the section)
# Remove comments at the start
div_content = re.sub(r'^<!--.*?-->\s*', '', div_content, flags=re.DOTALL)
div_content = re.sub(r'^<!--.*?-->\s*', '', div_content, flags=re.DOTALL)
div_content = div_content.strip()

# Read the main paper
paper_file = Path("h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html")
with open(paper_file, 'r', encoding='utf-8') as f:
    paper_html = f.read()

# Find and replace the placeholder Appendix O
old_appendix_o = '''<section id="appendix-o" class="appendix">
  <h2>Appendix O: Division Algebras</h2>
  <p><em>Content from division-algebras.html - See source file for details.</em></p>
</section>'''

new_appendix_o = f'''<section id="appendix-o" class="appendix">
  <h2>Appendix O: Division Algebras</h2>
  {div_content}
</section>'''

# Replace
if old_appendix_o in paper_html:
    paper_html = paper_html.replace(old_appendix_o, new_appendix_o)
    print("[OK] Replaced Appendix O placeholder with actual content")
else:
    print("[WARNING] Could not find exact placeholder match")
    # Try to find it differently
    start_marker = '<section id="appendix-o" class="appendix">'
    end_marker = '</section>'

    start_pos = paper_html.find(start_marker)
    if start_pos != -1:
        # Find the next </section> after this marker
        search_start = start_pos + len(start_marker)
        end_pos = paper_html.find(end_marker, search_start)
        if end_pos != -1:
            # Replace everything between the markers
            before = paper_html[:start_pos]
            after = paper_html[end_pos + len(end_marker):]
            paper_html = before + new_appendix_o + after
            print("[OK] Replaced Appendix O using alternative method")

# Write back
with open(paper_file, 'w', encoding='utf-8') as f:
    f.write(paper_html)

print(f"[OK] Updated paper file")
print(f"[OK] Added {len(div_content)} characters to Appendix O")
