#!/usr/bin/env python3
"""Fix em-dash mojibake"""

with open('principia-metaphysica-paper.html', 'rb') as f:
    content = f.read()

# Fix em-dash mojibake
replacements = [
    (b'\xe2\x80\x94', b'&mdash;'),  # em-dash
    (b'\xe2\x80\x93', b'&ndash;'),  # en-dash
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9c', b'&ndash;'),  # corrupted en-dash
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x94', b'&mdash;'),  # corrupted em-dash
]

count = 0
for old, new in replacements:
    occurrences = content.count(old)
    if occurrences > 0:
        content = content.replace(old, new)
        count += occurrences

with open('principia-metaphysica-paper.html', 'wb') as f:
    f.write(content)

print(f"Fixed {count} dash instances")
