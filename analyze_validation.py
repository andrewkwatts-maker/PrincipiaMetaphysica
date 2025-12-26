#!/usr/bin/env python3
"""
Analyze validation_summary section of theory_output.json
"""

import json
from pathlib import Path
from collections import defaultdict

def analyze_validation_summary():
    """Analyze the validation_summary section for completeness."""

    # Load the theory output
    theory_file = Path(r'h:\Github\PrincipiaMetaphysica\theory_output.json')
    with open(theory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get validation summary
    validation_summary = data.get('validation_summary', [])

    # Initialize counters
    total_entries = len(validation_summary)
    status_counts = defaultdict(int)
    missing_computed = []
    missing_expected = []
    missing_sigma = []
    missing_id_name = []
    missing_units = []

    # Analyze each entry
    for i, entry in enumerate(validation_summary):
        # Check for name/id
        has_name = 'name' in entry or 'id' in entry
        if not has_name:
            missing_id_name.append(i)

        # Count status
        status = entry.get('status', 'UNKNOWN')
        status_counts[status] += 1

        # Check for computed value
        if 'computed' not in entry and 'computed_value' not in entry and 'value' not in entry:
            missing_computed.append({
                'index': i,
                'name': entry.get('name', entry.get('id', f'Entry {i}'))
            })

        # Check for expected/experimental value
        if 'expected' not in entry and 'experimental' not in entry and 'experimental_value' not in entry:
            missing_expected.append({
                'index': i,
                'name': entry.get('name', entry.get('id', f'Entry {i}'))
            })

        # Check for sigma deviation
        if 'sigma' not in entry and 'sigma_deviation' not in entry and 'sigmas' not in entry:
            missing_sigma.append({
                'index': i,
                'name': entry.get('name', entry.get('id', f'Entry {i}'))
            })

        # Check for units
        if 'units' not in entry and 'unit' not in entry:
            missing_units.append({
                'index': i,
                'name': entry.get('name', entry.get('id', f'Entry {i}'))
            })

    # Generate report
    report = []
    report.append("# Validation Summary Audit Report\n")
    report.append(f"Generated: 2025-12-26\n")
    report.append(f"Source: `h:\\Github\\PrincipiaMetaphysica\\theory_output.json`\n\n")

    report.append("## Overview\n\n")
    report.append(f"**Total validation entries:** {total_entries}\n\n")

    report.append("## Status Breakdown\n\n")
    for status in ['PASS', 'FAIL', 'CHECK', 'UNKNOWN']:
        count = status_counts.get(status, 0)
        percentage = (count / total_entries * 100) if total_entries > 0 else 0
        report.append(f"- **{status}:** {count} ({percentage:.1f}%)\n")

    # Check for other status values
    other_statuses = {k: v for k, v in status_counts.items()
                     if k not in ['PASS', 'FAIL', 'CHECK', 'UNKNOWN']}
    if other_statuses:
        report.append(f"\nOther statuses found:\n")
        for status, count in other_statuses.items():
            report.append(f"- **{status}:** {count}\n")

    report.append("\n## Completeness Analysis\n\n")

    report.append(f"### Missing ID/Name\n")
    report.append(f"**Count:** {len(missing_id_name)}\n")
    if missing_id_name:
        report.append(f"Entries at indices: {missing_id_name}\n")
    report.append("\n")

    report.append(f"### Missing Computed Values\n")
    report.append(f"**Count:** {len(missing_computed)}\n")
    if missing_computed:
        report.append("```\n")
        for item in missing_computed[:10]:  # Show first 10
            report.append(f"  [{item['index']}] {item['name']}\n")
        if len(missing_computed) > 10:
            report.append(f"  ... and {len(missing_computed) - 10} more\n")
        report.append("```\n")
    report.append("\n")

    report.append(f"### Missing Expected/Experimental Values\n")
    report.append(f"**Count:** {len(missing_expected)}\n")
    if missing_expected:
        report.append("```\n")
        for item in missing_expected[:10]:
            report.append(f"  [{item['index']}] {item['name']}\n")
        if len(missing_expected) > 10:
            report.append(f"  ... and {len(missing_expected) - 10} more\n")
        report.append("```\n")
    report.append("\n")

    report.append(f"### Missing Sigma Deviations\n")
    report.append(f"**Count:** {len(missing_sigma)}\n")
    if missing_sigma:
        report.append("```\n")
        for item in missing_sigma[:10]:
            report.append(f"  [{item['index']}] {item['name']}\n")
        if len(missing_sigma) > 10:
            report.append(f"  ... and {len(missing_sigma) - 10} more\n")
        report.append("```\n")
    report.append("\n")

    report.append(f"### Missing Units\n")
    report.append(f"**Count:** {len(missing_units)}\n")
    if missing_units:
        report.append("```\n")
        for item in missing_units[:10]:
            report.append(f"  [{item['index']}] {item['name']}\n")
        if len(missing_units) > 10:
            report.append(f"  ... and {len(missing_units) - 10} more\n")
        report.append("```\n")
    report.append("\n")

    report.append("## Validation Health Summary\n\n")

    # Calculate health metrics
    if total_entries > 0:
        pass_rate = (status_counts.get('PASS', 0) / total_entries * 100)
        fail_rate = (status_counts.get('FAIL', 0) / total_entries * 100)
        check_rate = (status_counts.get('CHECK', 0) / total_entries * 100)

        completeness_score = 100 - (
            (len(missing_computed) / total_entries * 100 * 0.3) +
            (len(missing_expected) / total_entries * 100 * 0.3) +
            (len(missing_sigma) / total_entries * 100 * 0.25) +
            (len(missing_units) / total_entries * 100 * 0.15)
        )

        report.append(f"- **Pass Rate:** {pass_rate:.1f}%\n")
        report.append(f"- **Fail Rate:** {fail_rate:.1f}%\n")
        report.append(f"- **Check Rate:** {check_rate:.1f}%\n")
        report.append(f"- **Data Completeness Score:** {completeness_score:.1f}%\n\n")

        # Overall health assessment
        if pass_rate >= 80 and completeness_score >= 90:
            health = "EXCELLENT"
        elif pass_rate >= 60 and completeness_score >= 75:
            health = "GOOD"
        elif pass_rate >= 40 and completeness_score >= 60:
            health = "FAIR"
        else:
            health = "NEEDS IMPROVEMENT"

        report.append(f"**Overall Health:** {health}\n\n")

        # Recommendations
        report.append("## Recommendations\n\n")

        if len(missing_computed) > 0:
            report.append(f"1. Add computed values for {len(missing_computed)} entries\n")

        if len(missing_expected) > 0:
            report.append(f"2. Add expected/experimental values for {len(missing_expected)} entries\n")

        if len(missing_sigma) > 0:
            report.append(f"3. Calculate sigma deviations for {len(missing_sigma)} entries\n")

        if len(missing_units) > 0:
            report.append(f"4. Specify units for {len(missing_units)} entries\n")

        if status_counts.get('CHECK', 0) > 0:
            report.append(f"5. Review {status_counts.get('CHECK')} entries marked as CHECK\n")

        if status_counts.get('FAIL', 0) > 0:
            report.append(f"6. Investigate {status_counts.get('FAIL')} entries marked as FAIL\n")

    # Write report
    report_file = Path(r'h:\Github\PrincipiaMetaphysica\reports\VALIDATION_SUMMARY_AUDIT.md')
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(''.join(report))

    print(f"Report written to: {report_file}")
    print(f"\nQuick Summary:")
    print(f"  Total entries: {total_entries}")
    print(f"  PASS: {status_counts.get('PASS', 0)}")
    print(f"  FAIL: {status_counts.get('FAIL', 0)}")
    print(f"  CHECK: {status_counts.get('CHECK', 0)}")
    print(f"  Missing computed: {len(missing_computed)}")
    print(f"  Missing expected: {len(missing_expected)}")
    print(f"  Missing sigma: {len(missing_sigma)}")
    print(f"  Missing units: {len(missing_units)}")

if __name__ == '__main__':
    analyze_validation_summary()
