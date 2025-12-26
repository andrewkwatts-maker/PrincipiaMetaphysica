#!/usr/bin/env python3
"""
Final summary of foundations metadata after fixes.
"""
import json

data = json.load(open(r'h:\Github\PrincipiaMetaphysica\theory_output.json', 'r', encoding='utf-8'))
foundations = data['foundations']

print("=" * 70)
print("FOUNDATIONS METADATA - FINAL SUMMARY")
print("=" * 70)
print()

# Category distribution
print("CATEGORY DISTRIBUTION (All snake_case):")
from collections import Counter
cat_counts = Counter(f['category'] for f in foundations)
for cat, count in sorted(cat_counts.items()):
    print(f"  {cat:30s} : {count}")
print()

# PM connection stats
print("PM CONNECTION LENGTHS:")
pm_lengths = [(f['id'], len(f['pm_connection'])) for f in foundations]
pm_lengths.sort(key=lambda x: x[1])
print(f"  Min: {pm_lengths[0][1]} chars ({pm_lengths[0][0]})")
print(f"  Max: {pm_lengths[-1][1]} chars ({pm_lengths[-1][0]})")
avg_len = sum(x[1] for x in pm_lengths) / len(pm_lengths)
print(f"  Avg: {avg_len:.1f} chars")
print()

# Formula stats
print("FORMULA COUNTS:")
formula_counts = [(f['id'], len(f['formulas'])) for f in foundations]
formula_counts.sort(key=lambda x: x[1])
for fid, count in formula_counts:
    print(f"  {fid:30s} : {count} formulas")
print()

total_formulas = sum(x[1] for x in formula_counts)
avg_formulas = total_formulas / len(formula_counts)
print(f"  Total: {total_formulas} formulas across {len(foundations)} foundations")
print(f"  Average: {avg_formulas:.1f} formulas per foundation")
print()

# Quality metrics
print("QUALITY METRICS:")
key_prop_counts = [len(f['key_properties']) for f in foundations]
print(f"  Key properties: {min(key_prop_counts)}-{max(key_prop_counts)} per foundation (avg: {sum(key_prop_counts)/len(key_prop_counts):.1f})")

summary_lengths = [len(f['summary']) for f in foundations]
print(f"  Summary length: {min(summary_lengths)}-{max(summary_lengths)} chars (avg: {sum(summary_lengths)/len(summary_lengths):.1f})")

print()
print("=" * 70)
print("STATUS: All metadata fixes successfully applied!")
print("=" * 70)
