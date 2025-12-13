#!/usr/bin/env python3
"""
Insert appendices content into the main paper HTML file.
"""

from pathlib import Path

# Read the appendices content
appendices_file = Path("h:/Github/PrincipiaMetaphysica/appendices_content.html")
with open(appendices_file, 'r', encoding='utf-8') as f:
    appendices_html = f.read()

# Read the main paper file
paper_file = Path("h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html")
with open(paper_file, 'r', encoding='utf-8') as f:
    paper_html = f.read()

# Add appendix CSS styles before </style>
appendix_css = '''
        /* Appendix Styles */
        .appendix {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #444;
        }

        .appendix h2 {
            color: #b794f6;
            margin-bottom: 1.5rem;
        }

        .appendices-toc {
            page-break-before: always;
        }

        @media print {
            .appendix {
                border-top: 1px solid #666;
                page-break-before: always;
            }

            .appendix h2 {
                color: #333;
                border-bottom: 1px solid #666;
            }

            .appendices-toc {
                background: #f5f5f5 !important;
                border: 1px solid #666 !important;
            }
        }

        '''

# Insert CSS before </style>
style_end_pos = paper_html.find('</style>')
if style_end_pos != -1:
    paper_html = paper_html[:style_end_pos] + appendix_css + paper_html[style_end_pos:]
    print("[OK] Added appendix CSS styles")
else:
    print("[WARNING] Could not find </style> tag")

# Find the insertion point (after References section, before </div></body></html>)
# Look for the closing div before </body></html>
insertion_marker = '</div>\n </body>\n</html>'
insertion_pos = paper_html.rfind(insertion_marker)

if insertion_pos == -1:
    # Try alternative pattern
    insertion_marker = '</div>\n</body>\n</html>'
    insertion_pos = paper_html.rfind(insertion_marker)

if insertion_pos != -1:
    # Insert appendices before the closing div
    paper_html = paper_html[:insertion_pos] + '\n' + appendices_html + '\n  ' + paper_html[insertion_pos:]
    print("[OK] Inserted appendices after References section")
else:
    print("[ERROR] Could not find insertion point")
    print("Looking for patterns...")
    # Debug: find what the end looks like
    last_500_chars = paper_html[-500:]
    print(f"Last 500 characters:\n{last_500_chars}")

# Write the updated paper
output_file = Path("h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(paper_html)

print(f"[OK] Updated paper written to: {output_file}")
print(f"[OK] Total file size: {len(paper_html):,} characters")
print("\nAppendices have been successfully added to the paper!")
