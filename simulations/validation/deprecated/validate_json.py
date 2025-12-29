#!/usr/bin/env python3
"""
Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json

try:
    data = json.load(open('theory_output.json', 'r', encoding='utf-8'))
    print('JSON is valid')
    print(f'Top-level keys: {list(data.keys())}')
    stats = data['framework_statistics']
    field_count = len([k for k in stats.keys() if k != 'registry'])
    print(f'Framework statistics field count: {field_count}')
    print('\nAll framework_statistics fields:')
    for i, key in enumerate([k for k in stats.keys() if k != 'registry'], 1):
        print(f'  {i}. {key}')
except Exception as e:
    print(f'ERROR: {e}')
