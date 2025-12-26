#!/usr/bin/env python3
import json

data = json.load(open(r'h:\Github\PrincipiaMetaphysica\theory_output.json', 'r', encoding='utf-8'))
stats = data['framework_statistics']

print('Framework Statistics Fields:')
fields = [k for k in stats.keys() if k != 'registry']
print(f'Total fields (excluding registry): {len(fields)}')

print('\nNew/Updated fields:')
for field in ['geometric_predictions', 'total_formulas', 'total_simulations', 'total_sections',
              'success_rate_2sigma', 'simulation_pass_rate', 'parameter_categories', 'validation_timestamp']:
    value = stats.get(field)
    if field == 'parameter_categories':
        print(f'  {field}: {len(value)} categories - {value[:3]}...')
    elif field == 'validation_timestamp':
        print(f'  {field}: {value[:19]}...')
    else:
        print(f'  {field}: {value}')

print('\nVerified existing fields:')
print(f'  total_sm_parameters: {stats["total_sm_parameters"]}')
print(f'  within_1_sigma: {stats["within_1_sigma"]}')
print(f'  within_2_sigma: {stats["within_2_sigma"]}')
print(f'  success_rate_1sigma: {stats["success_rate_1sigma"]}%')
print(f'  pure_predictions: {stats["pure_predictions"]}')

print(f'\nAll expected fields present: {all(field in stats for field in ["geometric_predictions", "total_formulas", "total_simulations"])}')
