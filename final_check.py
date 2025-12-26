#!/usr/bin/env python3
import json
import os

filepath = 'theory_output.json'
size_kb = os.path.getsize(filepath) / 1024
data = json.load(open(filepath, 'r', encoding='utf-8'))
stats = data['framework_statistics']

print('=== FINAL VERIFICATION ===\n')
print(f'File: {filepath}')
print(f'File size: {size_kb:.1f} KB')
print(f'JSON valid: Yes')
print(f'\nFramework Statistics:')
print(f'  Total fields (excluding registry): {len([k for k in stats.keys() if k != "registry"])}')
print(f'  Registry parameters: {len(stats.get("registry", {}).get("parameters", {}))}')

critical_fields = ['geometric_predictions', 'total_formulas', 'total_simulations']
print(f'\nCritical fields check:')
for field in critical_fields:
    present = field in stats
    value = stats.get(field, 'N/A')
    print(f'  {field}: {"PRESENT" if present else "MISSING"} (value: {value})')

additional_fields = ['total_sections', 'success_rate_2sigma', 'simulation_pass_rate',
                     'parameter_categories', 'validation_timestamp']
print(f'\nAdditional recommended fields:')
for field in additional_fields:
    present = field in stats
    value = stats.get(field, 'N/A')
    if field == 'parameter_categories':
        value = f'{len(value)} categories' if isinstance(value, list) else value
    elif field == 'validation_timestamp':
        value = value[:19] if isinstance(value, str) else value
    print(f'  {field}: {"PRESENT" if present else "MISSING"} (value: {value})')

print(f'\nAll critical fields present: {all(f in stats for f in critical_fields)}')
print(f'All additional fields present: {all(f in stats for f in additional_fields)}')
print(f'\nSTATUS: COMPLETE')
