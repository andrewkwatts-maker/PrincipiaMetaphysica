#!/usr/bin/env python3
"""Test script for ParameterCategory implementation."""

from config import ParameterCategory, FittedParameters

print('ParameterCategory values:')
print(f'  GEOMETRIC: {ParameterCategory.GEOMETRIC}')
print(f'  DERIVED: {ParameterCategory.DERIVED}')
print(f'  PHENOMENOLOGICAL: {ParameterCategory.PHENOMENOLOGICAL}')
print(f'  CALIBRATED: {ParameterCategory.CALIBRATED}')
print(f'  PREDICTED: {ParameterCategory.PREDICTED}')
print(f'  EXPERIMENTAL: {ParameterCategory.EXPERIMENTAL}')
print()

print('FittedParameters STATUS flags:')
print(f'  STATUS_SHADOW_KUF: {FittedParameters.STATUS_SHADOW_KUF}')
print(f'  STATUS_SHADOW_CHET: {FittedParameters.STATUS_SHADOW_CHET}')
print(f'  STATUS_THETA_13: {FittedParameters.STATUS_THETA_13}')
print(f'  STATUS_DELTA_CP: {FittedParameters.STATUS_DELTA_CP}')
print()

print('Category counts:')
counts = FittedParameters.get_category_counts()
for category, count in counts.items():
    print(f'  {category}: {count}')
print()

total = sum(counts.values())
print(f'Total categorized parameters: {total}')
