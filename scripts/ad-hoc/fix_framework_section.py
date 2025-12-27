#!/usr/bin/env python3
"""Fix broken Early Framework -> Current Framework -> Framework Status section."""

import sys
import re

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    paper_path = 'principia-metaphysica-paper.html'

    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The broken pattern - regex to match the orphaned divs without proper flex container
    # Note: \u2192 is the right arrow →
    broken_pattern = re.compile(
        r'</table>\s*</div>\s*\n\s*<div style="color: var\(--text-muted\); font-size: 0\.9rem;">\s*Early Framework\s*</div>\s*'
        r'<div style="color: var\(--text-secondary\); font-size: 0\.8rem; margin-top: 0\.25rem;">\s*\(Fitted parameters\)\s*</div>\s*'
        r'</div>\s*'
        r'<div style="font-size: 2rem; color: var\(--accent-primary\);">\s*[\u2192→]\s*</div>\s*'
        r'<div style="text-align: center;">\s*'
        r'<div style="color: var\(--text-muted\); font-size: 0\.9rem;">\s*Current Framework\s*</div>\s*'
        r'<div style="color: var\(--text-secondary\); font-size: 0\.8rem; margin-top: 0\.25rem;">\s*\(Geometric derivations\)\s*</div>\s*'
        r'</div>\s*'
        r'<div style="font-size: 2rem; color: var\(--accent-primary\);">\s*[\u2192→]\s*</div>\s*'
        r'<div style="text-align: center;">\s*'
        r'<div style="color: var\(--text-muted\); font-size: 0\.9rem;">\s*Framework Status\s*</div>\s*'
        r'<div style="color: var\(--text-secondary\); font-size: 0\.8rem; margin-top: 0\.25rem;">\s*\(Current status\)\s*</div>\s*'
        r'</div>\s*'
        r'</div>',
        re.MULTILINE
    )

    # The fixed replacement
    fixed_html = '''</table>
    </div>

    <!-- Framework Evolution Summary -->
    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap; padding: 1.5rem; background: rgba(139, 127, 255, 0.05); border-radius: 12px; border: 1px solid rgba(139, 127, 255, 0.2);">
      <div style="text-align: center;">
        <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">
          Early Framework
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
          (Fitted parameters)
        </div>
      </div>
      <div style="font-size: 2rem; color: var(--accent-primary);">
        →
      </div>
      <div style="text-align: center;">
        <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">
          Current Framework
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
          (Geometric derivations)
        </div>
      </div>
      <div style="font-size: 2rem; color: var(--accent-primary);">
        →
      </div>
      <div style="text-align: center;">
        <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">
          Framework Status
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
          (All 15 issues resolved)
        </div>
      </div>
    </div>'''

    match = broken_pattern.search(content)
    if match:
        content = broken_pattern.sub(fixed_html, content)
        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed: Framework Evolution section now has proper flex container")
        return 0
    else:
        print("Pattern not found with regex - trying simple string match...")

        # Try a simpler approach - find and replace the specific area
        marker = 'Early Framework'
        idx = content.find(marker)
        if idx > 0:
            # Find the start of the broken section (after </div> from the table)
            search_start = idx - 200
            table_end = content.rfind('</table>', 0, idx)
            div_end = content.find('</div>', table_end)

            # Find the end of the broken section (the Assessment paragraph)
            assessment_start = content.find('<p style="color: var(--text-secondary); margin-top: 1rem;', idx)

            if table_end > 0 and assessment_start > 0:
                broken_section = content[div_end:assessment_start]
                print(f"Found broken section ({len(broken_section)} chars)")

                # Replace it
                new_section = '''</div>

    <!-- Framework Evolution Summary -->
    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap; padding: 1.5rem; background: rgba(139, 127, 255, 0.05); border-radius: 12px; border: 1px solid rgba(139, 127, 255, 0.2);">
      <div style="text-align: center;">
        <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">
          Early Framework
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
          (Fitted parameters)
        </div>
      </div>
      <div style="font-size: 2rem; color: var(--accent-primary);">
        →
      </div>
      <div style="text-align: center;">
        <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">
          Current Framework
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
          (Geometric derivations)
        </div>
      </div>
      <div style="font-size: 2rem; color: var(--accent-primary);">
        →
      </div>
      <div style="text-align: center;">
        <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">
          Framework Status
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.25rem;">
          (All 15 issues resolved)
        </div>
      </div>
    </div>

    '''

                content = content[:div_end] + new_section + content[assessment_start:]
                with open(paper_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("Fixed with simple string replacement!")
                return 0

        print("Could not locate the broken section")
        return 1

if __name__ == '__main__':
    sys.exit(main())
