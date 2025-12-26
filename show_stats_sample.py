#!/usr/bin/env python3
import json

data = json.load(open('theory_output.json', 'r', encoding='utf-8'))
stats = data['framework_statistics']

print('=== FRAMEWORK STATISTICS SAMPLE ===\n')

# Show all fields except registry
for key in stats.keys():
    if key == 'registry':
        print(f'{key}: <Large object with {len(stats[key].get("parameters", {}))} parameters>')
    elif key == 'parameter_categories':
        print(f'{key}: {stats[key][:5]} ... ({len(stats[key])} total)')
    elif key == 'foundation_categories':
        print(f'{key}: {stats[key][:3]} ... ({len(stats[key])} total)')
    elif key == 'description':
        print(f'{key}: "{stats[key][:80]}..."')
    else:
        print(f'{key}: {stats[key]}')

print('\n=== VERIFICATION ===\n')
print(f'Total fields (excluding registry): {len([k for k in stats.keys() if k != "registry"])}')
print(f'All 3 critical missing fields now present: {all(f in stats for f in ["geometric_predictions", "total_formulas", "total_simulations"])}')
print(f'Success rate 2sigma matches calculation: {stats["success_rate_2sigma"]} == {round(55/56*100, 1)}')
print(f'Geometric predictions equals pure predictions: {stats["geometric_predictions"]} == {stats["pure_predictions"]}')
