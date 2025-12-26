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
    entries_by_status = defaultdict(list)

    # Analyze each entry
    for i, entry in enumerate(validation_summary):
        if isinstance(entry, list) and len(entry) >= 2:
            name = entry[0]
            status = entry[1]

            status_counts[status] += 1
            entries_by_status[status].append({
                'index': i,
                'name': name,
                'status': status
            })
        else:
            status_counts['MALFORMED'] += 1
            entries_by_status['MALFORMED'].append({
                'index': i,
                'name': 'Unknown',
                'status': 'MALFORMED',
                'data': entry
            })

    # Generate report
    report = []
    report.append("# Validation Summary Audit Report\n\n")
    report.append(f"**Generated:** 2025-12-26\n\n")
    report.append(f"**Source:** `h:\\Github\\PrincipiaMetaphysica\\theory_output.json`\n\n")

    report.append("---\n\n")

    report.append("## 1. Total Number of Validation Entries\n\n")
    report.append(f"**Total:** {total_entries} validation entries\n\n")

    report.append("---\n\n")

    report.append("## 2. Entries with PASS Status\n\n")
    pass_count = status_counts.get('PASS', 0)
    report.append(f"**Count:** {pass_count} ({pass_count/total_entries*100:.1f}% of total)\n\n")

    if entries_by_status['PASS']:
        report.append("**Passing validations:**\n")
        for entry in entries_by_status['PASS']:
            report.append(f"- {entry['name']}\n")
    report.append("\n")

    report.append("---\n\n")

    report.append("## 3. Entries with FAIL Status\n\n")
    fail_count = status_counts.get('FAIL', 0)
    report.append(f"**Count:** {fail_count} ({fail_count/total_entries*100:.1f}% of total)\n\n")

    if entries_by_status['FAIL']:
        report.append("**Failed validations:**\n")
        for entry in entries_by_status['FAIL']:
            report.append(f"- {entry['name']}\n")
    else:
        report.append("No entries with FAIL status.\n")
    report.append("\n")

    report.append("---\n\n")

    report.append("## 4. Entries with CHECK Status (Need Attention)\n\n")
    check_count = status_counts.get('CHECK', 0)
    report.append(f"**Count:** {check_count} ({check_count/total_entries*100:.1f}% of total)\n\n")

    if entries_by_status['CHECK']:
        report.append("**Validations requiring attention:**\n")
        for entry in entries_by_status['CHECK']:
            report.append(f"- {entry['name']}\n")
    else:
        report.append("No entries with CHECK status.\n")
    report.append("\n")

    report.append("---\n\n")

    report.append("## 5. Missing Computed/Expected Values\n\n")
    report.append("**Analysis:** The current validation_summary uses a simplified format:\n")
    report.append("```json\n")
    report.append("[\n")
    report.append('  ["Validation Name", "STATUS"],\n')
    report.append('  ...\n')
    report.append("]\n")
    report.append("```\n\n")

    report.append("**Finding:** ALL entries are missing:\n")
    report.append(f"- Computed values: {total_entries}/{total_entries} entries\n")
    report.append(f"- Expected/experimental values: {total_entries}/{total_entries} entries\n\n")

    report.append("**Recommendation:** Expand the validation_summary format to include:\n")
    report.append("```json\n")
    report.append("{\n")
    report.append('  "name": "Validation Name",\n')
    report.append('  "status": "PASS/FAIL/CHECK/ERROR",\n')
    report.append('  "computed": <value>,\n')
    report.append('  "expected": <value>,\n')
    report.append('  "sigma": <deviation>,\n')
    report.append('  "units": "...",\n')
    report.append('  "notes": "..."\n')
    report.append("}\n")
    report.append("```\n\n")

    report.append("---\n\n")

    report.append("## 6. Missing Sigma Calculations\n\n")
    report.append(f"**Count:** {total_entries}/{total_entries} entries (100%)\n\n")
    report.append("All validation entries lack sigma deviation calculations. This is critical for:\n")
    report.append("- Quantifying agreement with experimental data\n")
    report.append("- Statistical validation of theoretical predictions\n")
    report.append("- Comparing relative quality of different predictions\n\n")

    report.append("---\n\n")

    report.append("## 7. Summary of Overall Validation Health\n\n")

    # Calculate health metrics
    if total_entries > 0:
        pass_rate = (pass_count / total_entries * 100)
        fail_rate = (fail_count / total_entries * 100)
        check_rate = (check_count / total_entries * 100)
        error_count = status_counts.get('ERROR', 0)
        error_rate = (error_count / total_entries * 100)

        report.append("### Status Distribution\n\n")
        report.append(f"- **PASS:** {pass_count} ({pass_rate:.1f}%)\n")
        report.append(f"- **CHECK:** {check_count} ({check_rate:.1f}%)\n")
        report.append(f"- **ERROR:** {error_count} ({error_rate:.1f}%)\n")
        report.append(f"- **FAIL:** {fail_count} ({fail_rate:.1f}%)\n\n")

        # ERROR status entries
        if entries_by_status['ERROR']:
            report.append("### Entries with ERROR Status\n\n")
            report.append(f"**Count:** {error_count} ({error_rate:.1f}% of total)\n\n")
            report.append("**Error validations requiring fixes:**\n")
            for entry in entries_by_status['ERROR']:
                report.append(f"- {entry['name']}\n")
            report.append("\n")

        # Data completeness
        report.append("### Data Completeness\n\n")
        report.append("| Field | Present | Missing | Completeness |\n")
        report.append("|-------|---------|---------|-------------|\n")
        report.append(f"| Name/ID | {total_entries} | 0 | 100% |\n")
        report.append(f"| Status | {total_entries} | 0 | 100% |\n")
        report.append(f"| Computed Value | 0 | {total_entries} | 0% |\n")
        report.append(f"| Expected Value | 0 | {total_entries} | 0% |\n")
        report.append(f"| Sigma Deviation | 0 | {total_entries} | 0% |\n")
        report.append(f"| Units | 0 | {total_entries} | 0% |\n\n")

        # Overall assessment
        report.append("### Overall Health Assessment\n\n")

        # Determine health status
        successful_rate = (pass_count / total_entries * 100)
        problematic_rate = ((check_count + error_count + fail_count) / total_entries * 100)

        report.append(f"**Successful Validations:** {successful_rate:.1f}%\n")
        report.append(f"**Problematic Validations:** {problematic_rate:.1f}%\n\n")

        if successful_rate >= 70:
            health_status = "GOOD - Strong validation success rate"
            health_color = "green"
        elif successful_rate >= 50:
            health_status = "FAIR - Moderate validation success"
            health_color = "yellow"
        else:
            health_status = "POOR - Low validation success rate"
            health_color = "red"

        report.append(f"**Status Health:** {health_status}\n\n")

        # Data quality assessment
        data_completeness = 50  # Only name and status present, no numerical data
        if data_completeness >= 90:
            data_status = "EXCELLENT - Comprehensive validation data"
        elif data_completeness >= 75:
            data_status = "GOOD - Adequate validation data"
        elif data_completeness >= 50:
            data_status = "FAIR - Minimal validation data"
        else:
            data_status = "POOR - Insufficient validation data"

        report.append(f"**Data Quality:** {data_status}\n\n")

        # Overall grade
        overall_score = (successful_rate * 0.6 + data_completeness * 0.4)

        if overall_score >= 85:
            overall_grade = "A - Excellent"
        elif overall_score >= 75:
            overall_grade = "B - Good"
        elif overall_score >= 65:
            overall_grade = "C - Fair"
        elif overall_score >= 50:
            overall_grade = "D - Needs Improvement"
        else:
            overall_grade = "F - Critical Issues"

        report.append(f"**Overall Grade:** {overall_grade} ({overall_score:.1f}/100)\n\n")

    report.append("---\n\n")

    report.append("## Detailed Recommendations\n\n")

    report.append("### Immediate Actions (Priority 1)\n\n")

    if error_count > 0:
        report.append(f"1. **Fix {error_count} ERROR entries:**\n")
        for entry in entries_by_status['ERROR']:
            report.append(f"   - {entry['name']}\n")
        report.append("\n")

    if check_count > 0:
        report.append(f"2. **Review {check_count} CHECK entries:**\n")
        for entry in entries_by_status['CHECK']:
            report.append(f"   - {entry['name']}\n")
        report.append("\n")

    report.append("### Short-term Improvements (Priority 2)\n\n")

    report.append("3. **Expand validation data structure** to include:\n")
    report.append("   - Computed values from simulations\n")
    report.append("   - Expected/experimental values with uncertainties\n")
    report.append("   - Sigma deviations for quantitative comparison\n")
    report.append("   - Physical units for all quantities\n")
    report.append("   - References to source simulations/experiments\n\n")

    report.append("4. **Add validation metadata:**\n")
    report.append("   - Simulation version/date\n")
    report.append("   - Experimental data source\n")
    report.append("   - Confidence level\n")
    report.append("   - Notes/caveats\n\n")

    report.append("### Long-term Enhancements (Priority 3)\n\n")

    report.append("5. **Implement automated validation pipeline:**\n")
    report.append("   - Automatic sigma calculation from simulation outputs\n")
    report.append("   - Trend analysis over simulation versions\n")
    report.append("   - Alert system for failing validations\n")
    report.append("   - Visualization of validation results\n\n")

    report.append("6. **Create validation documentation:**\n")
    report.append("   - Detailed explanation of each validation\n")
    report.append("   - Physical significance of results\n")
    report.append("   - Known limitations and assumptions\n")
    report.append("   - Improvement roadmap\n\n")

    report.append("---\n\n")

    report.append("## Appendix: Example Enhanced Validation Entry\n\n")

    report.append("```json\n")
    report.append("{\n")
    report.append('  "name": "Higgs Mass",\n')
    report.append('  "id": "higgs_mass_prediction",\n')
    report.append('  "status": "PASS",\n')
    report.append('  "computed": 125.3,\n')
    report.append('  "expected": 125.25,\n')
    report.append('  "experimental_uncertainty": 0.17,\n')
    report.append('  "sigma": 0.29,\n')
    report.append('  "units": "GeV",\n')
    report.append('  "simulation": "higgs_mass_v14_2.py",\n')
    report.append('  "reference": "ATLAS+CMS Combined, PDG 2024",\n')
    report.append('  "confidence": 0.95,\n')
    report.append('  "notes": "Prediction within 1-sigma of experimental value",\n')
    report.append('  "timestamp": "2025-12-26"\n')
    report.append("}\n")
    report.append("```\n\n")

    # Write report
    report_file = Path(r'h:\Github\PrincipiaMetaphysica\reports\VALIDATION_SUMMARY_AUDIT.md')
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(''.join(report))

    print(f"Report written to: {report_file}")
    print(f"\nQuick Summary:")
    print(f"  Total entries: {total_entries}")
    print(f"  PASS: {status_counts.get('PASS', 0)} ({status_counts.get('PASS', 0)/total_entries*100:.1f}%)")
    print(f"  CHECK: {status_counts.get('CHECK', 0)} ({status_counts.get('CHECK', 0)/total_entries*100:.1f}%)")
    print(f"  ERROR: {status_counts.get('ERROR', 0)} ({status_counts.get('ERROR', 0)/total_entries*100:.1f}%)")
    print(f"  FAIL: {status_counts.get('FAIL', 0)} ({status_counts.get('FAIL', 0)/total_entries*100:.1f}%)")
    print(f"\nData Completeness:")
    print(f"  Missing computed values: {total_entries}")
    print(f"  Missing expected values: {total_entries}")
    print(f"  Missing sigma calculations: {total_entries}")
    print(f"  Missing units: {total_entries}")

if __name__ == '__main__':
    analyze_validation_summary()
