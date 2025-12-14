#!/usr/bin/env python3
"""
Strip tooltip divs from the paper HTML.
These hover tooltips are for the website but clutter the paper.
"""

import sys
import re

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    paper_path = 'principia-metaphysica-paper.html'

    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # Count tooltips before removal
    tooltip_count_before = content.count('<div class="var-tooltip">')
    print(f"Found {tooltip_count_before} var-tooltip divs to remove")

    # Pattern to match entire var-tooltip div blocks (including nested content)
    # This handles multi-line tooltip divs
    pattern = r'<div class="var-tooltip">.*?</div>\s*</div>\s*</div>'

    # More precise pattern - match the var-tooltip and its children
    # The structure is: <div class="var-tooltip"><div>...</div>...<div>...</div></div>

    # Use a more careful approach - find and remove tooltip blocks
    def remove_tooltips(html):
        # Pattern for simple single-level tooltips
        simple_pattern = r'\s*<div class="var-tooltip">\s*<div class="var-name">[^<]*</div>\s*<div class="var-desc(?:ription)?">[^<]*</div>\s*(?:<div class="var-units">[^<]*</div>\s*)?(?:<div class="var-contribution">[^<]*</div>\s*)?</div>'

        # Count and remove
        count = 0
        while True:
            new_html = re.sub(simple_pattern, '', html, count=1)
            if new_html == html:
                break
            html = new_html
            count += 1

        return html, count

    # Try a more robust approach - remove everything between <div class="var-tooltip"> and its matching </div>
    def remove_tooltip_blocks(html):
        result = []
        i = 0
        removed = 0

        while i < len(html):
            # Look for start of var-tooltip
            tooltip_start = html.find('<div class="var-tooltip">', i)

            if tooltip_start == -1:
                # No more tooltips, add rest of content
                result.append(html[i:])
                break

            # Add content before the tooltip
            result.append(html[i:tooltip_start])

            # Find matching closing </div> by counting nesting
            pos = tooltip_start + len('<div class="var-tooltip">')
            depth = 1

            while depth > 0 and pos < len(html):
                next_open = html.find('<div', pos)
                next_close = html.find('</div>', pos)

                if next_close == -1:
                    break

                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + 4
                else:
                    depth -= 1
                    if depth == 0:
                        # Found the matching close
                        pos = next_close + len('</div>')
                        break
                    else:
                        pos = next_close + len('</div>')

            i = pos
            removed += 1

        return ''.join(result), removed

    content, removed = remove_tooltip_blocks(content)

    # Also strip empty whitespace that might be left
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    print(f"Removed {removed} tooltip blocks")

    new_len = len(content)
    reduction = original_len - new_len
    print(f"File size reduction: {reduction:,} bytes ({reduction/1024:.1f} KB)")

    # Save
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Verify
    with open(paper_path, 'r', encoding='utf-8') as f:
        verify = f.read()

    remaining = verify.count('<div class="var-tooltip">')
    print(f"Remaining tooltips: {remaining}")

    if remaining == 0:
        print("SUCCESS: All tooltips removed from paper")
        return 0
    else:
        print(f"WARNING: {remaining} tooltips still present")
        return 1

if __name__ == '__main__':
    sys.exit(main())
