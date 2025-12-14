#!/usr/bin/env python3
"""
Comprehensive mojibake fix for principia-metaphysica-paper.html
Fixes all corrupted UTF-8 subscript/superscript patterns
"""

import re

# Read file as bytes to handle mojibake
with open('principia-metaphysica-paper.html', 'rb') as f:
    content = f.read()

# Define replacement patterns (old bytes -> new bytes)
replacements = [
    # Pneuma variations
    (b'P\xe2\x82\x81\xe2\x84\xa2\xe2\x82\x81\xe2\x80\x99u\xe2\x82\x81\xcb\x9c\xe2\x82\x81', b'Pneuma'),
    (b'P\xe2\x82\x81\xe2\x84\xa2\xe2\x82\x81\xe2\x80\x99\xc3\xa1\xc2\xb5\xa4\xe2\x82\x81\xcb\x9c\xe2\x82\x81', b'Pneuma'),
    (b'P\xe2\x82\x81\xe2\x84\xa2\xe2\x82\x81', b'Pneuma'),

    # thermal variations
    (b't<sub>t</sub>\xe2\x82\x81\xe2\x80\xa2\xe2\x82\x81\xe2\x80\x99\xc3\xa1\xc2\xb5\xa3\xe2\x82\x81\xcb\x9c', b'thermal'),
    (b't<sub>t</sub>\xe2\x82\x81\xe2\x80\xa2\xe2\x82\x81\xe2\x80\x99r\xe2\x82\x81\xcb\x9c', b'thermal'),
    (b'<sub>t</sub>\xe2\x82\x81\xe2\x80\xa2\xe2\x82\x81\xe2\x80\x99\xc3\xa1\xc2\xb5\xa3\xe2\x82\x81\xcb\x9c', b'thermal'),

    # c_matter variations
    (b'c \xe2\x82\x81\xcb\x9c\xe2\x82\x81<sub>t</sub><sub>t</sub>\xe2\x82\x81\xe2\x80\x99r', b'c<sub>matter</sub>'),
    (b'c<sub>t</sub>\xe2\x82\x81\xe2\x80\x99<sub>t</sub>\xe2\x82\x81\xe2\x82\x81\xe2\x80\x94', b'c<sub>total</sub>'),
    (b'\xe2\x82\x81\xcb\x9c\xe2\x82\x81<sub>t</sub><sub>t</sub>\xe2\x82\x81\xe2\x80\x99r', b'<sub>matter</sub>'),

    # ghost variations
    (b'g\xe2\x82\x81\xe2\x80\x99\xe2\x82\x81\xe2\x84\xa2', b'ghost'),
    (b'g\xe2\x82\x81\xe2\x80\xa2\xe2\x82\x81\xe2\x80\x99\xe2\x82\x81\xe2\x80\xba<sub>t</sub>', b'ghost'),

    # interaction
    (b'i\xe2\x82\x81\xe2\x84\xa2<sub>t</sub>', b'interaction'),
    (b'<sub>i</sub>\xe2\x82\x81\xe2\x84\xa2<sub>t</sub>', b'<sub>int</sub>'),

    # Simple pattern cleanup
    (b'\xe2\x82\x81\xcb\x9c\xe2\x82\x81\xe2\x84\xa2', b''),
    (b'\xe2\x82\x81\xe2\x80\x99', b''),
    (b'\xe2\x82\x81\xe2\x80\xa2', b''),
    (b'\xe2\x82\x81\xe2\x80\xba', b''),
    (b'\xe2\x82\x81\xe2\x80\x94', b''),
    (b'\xe2\x82\x81\xe2\x84\xa2', b''),
    (b'\xe2\x82\x81\xcb\x9c', b''),

    # Superscript/subscript number fixes
    (b'\xc2\xb3<sup>4</sup>', b'<sup>34</sup>'),
    (b'\xc2\xb9<sup>6</sup>', b'<sup>16</sup>'),
    (b'\xc2\xb3 \xe2\x8a\x95', b'<sup>3</sup> &oplus;'),
    (b'\xe2\x82\x84 \xc2\xb3', b'<sub>4</sub><sup>3</sup>'),

    # Fix broken Sigma subscripts
    (b'\xce\xa3 \xe2\x82\x84', b'&Sigma;<sub>4</sub>'),

    # Fix M^13_eff pattern
    (b'M \xc2\xb9\xc2\xb3 <sub>eff</sub>', b'M<sup>13</sup><sub>eff</sub>'),

    # Fix broken math operators
    (b'\xe2\x84\x9d', b'&real;'),  # Real part symbol
    (b'\xe2\x8a\x83', b'&sup;'),   # Superset symbol fix
]

count = 0
for old, new in replacements:
    occurrences = content.count(old)
    if occurrences > 0:
        content = content.replace(old, new)
        count += occurrences

# Write back
with open('principia-metaphysica-paper.html', 'wb') as f:
    f.write(content)

print(f"Fixed {count} mojibake instances")
