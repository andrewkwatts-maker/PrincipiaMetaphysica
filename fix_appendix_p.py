#!/usr/bin/env python3
"""
Fix Appendix P by removing duplicate sections/index.html content
"""

with open('principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the marker we just added
marker = '<!-- REMOVED: Duplicate sections/index.html content that was incorrectly embedded here -->'
appendix_q_start = '<section id="appendix-q" class="appendix">'

if marker in content and appendix_q_start in content:
    # Find positions
    marker_pos = content.find(marker)
    appendix_q_pos = content.find(appendix_q_start)

    # Extract content before marker, then add clean transition to Appendix Q
    before_marker = content[:marker_pos + len(marker)]
    after_appendix_q = content[appendix_q_pos:]

    # Combine with clean transition
    new_content = before_marker + '\n\n' + after_appendix_q

    with open('principia-metaphysica-paper.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Removed {appendix_q_pos - marker_pos - len(marker)} characters of duplicate content")
    print("Successfully cleaned up Appendix P")
else:
    print(f"Marker found: {marker in content}")
    print(f"Appendix Q found: {appendix_q_start in content}")
    print("Could not find markers to clean up")
