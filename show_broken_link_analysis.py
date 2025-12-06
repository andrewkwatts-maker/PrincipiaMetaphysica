#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper script to display the broken link analysis report in a readable format.
"""

import json
import sys
from collections import defaultdict

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def load_report(filename='broken_links_fix_report.json'):
    """Load the analysis report."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def show_summary(report):
    """Display summary statistics."""
    print('='*80)
    print('BROKEN LINKS ANALYSIS SUMMARY')
    print('='*80)
    print()
    print(f"Analysis timestamp: {report['timestamp']}")
    print(f"Dry run mode: {report['dry_run']}")
    print()
    print(f"Total broken links: {report['summary']['total_analyzed']}")
    print(f"Fixes applied: {report['summary']['total_fixes_applied']}")
    print(f"Manual needed: {report['summary']['total_manual_needed']}")
    print(f"Pending: {report['summary']['total_pending']}")
    print()


def show_by_strategy(report):
    """Group and display fixes by strategy."""
    print('='*80)
    print('FIXES BY STRATEGY')
    print('='*80)
    print()

    by_strategy = defaultdict(list)
    for fix in report['all_fixes_analyzed']:
        by_strategy[fix['strategy']].append(fix)

    strategy_descriptions = {
        'update_path': 'Files moved to new locations',
        'remove_link': 'Dead links to be removed',
        'fix_typo': 'Typos in filenames or anchors',
        'create_page': 'Missing pages that should exist',
        'add_anchor': 'Missing anchor IDs in existing files',
        'manual': 'Requires manual review (likely false positives)'
    }

    for strategy in ['update_path', 'remove_link', 'fix_typo', 'create_page', 'add_anchor', 'manual']:
        fixes = by_strategy.get(strategy, [])
        if not fixes:
            continue

        print(f"\n{strategy.upper()}: {len(fixes)} links")
        print(f"  {strategy_descriptions.get(strategy, '')}")
        print()

        for i, fix in enumerate(fixes, 1):
            print(f"  [{i}] File: {fix['source_file']}")
            print(f"      Link: {fix['broken_link']}")
            if fix.get('new_link'):
                print(f"      Fix:  {fix['new_link']}")
            print(f"      Confidence: {fix['confidence']:.0%}")
            print(f"      Reason: {fix['reason']}")

            # Show metadata for interesting cases
            if fix['strategy'] in ['create_page', 'add_anchor', 'fix_typo']:
                if fix['metadata']:
                    print(f"      Metadata: {json.dumps(fix['metadata'], indent=14)[:200]}")
            print()


def show_by_file(report):
    """Group and display fixes by source file."""
    print('='*80)
    print('FIXES BY SOURCE FILE')
    print('='*80)
    print()

    by_file = defaultdict(list)
    for fix in report['all_fixes_analyzed']:
        by_file[fix['source_file']].append(fix)

    for filename in sorted(by_file.keys()):
        fixes = by_file[filename]
        print(f"\n{filename}: {len(fixes)} broken link(s)")
        print('-' * 80)

        for fix in fixes:
            print(f"  Link: {fix['broken_link']}")
            print(f"  Strategy: {fix['strategy']} (confidence: {fix['confidence']:.0%})")
            if fix.get('new_link'):
                print(f"  New link: {fix['new_link']}")
            print(f"  Reason: {fix['reason']}")
            print()


def show_auto_fixable(report):
    """Show only auto-fixable items."""
    print('='*80)
    print('AUTO-FIXABLE ITEMS (Confidence >= 90%)')
    print('='*80)
    print()

    auto_fixes = [f for f in report['all_fixes_analyzed'] if f['confidence'] >= 0.9]

    if not auto_fixes:
        print("No auto-fixable items found.")
        return

    print(f"Total: {len(auto_fixes)} links\n")

    by_file = defaultdict(list)
    for fix in auto_fixes:
        by_file[fix['source_file']].append(fix)

    for filename in sorted(by_file.keys()):
        fixes = by_file[filename]
        print(f"{filename}: {len(fixes)} fix(es)")
        for fix in fixes:
            print(f"  - {fix['strategy']}: {fix['broken_link']}")
            if fix.get('new_link'):
                print(f"    -> {fix['new_link']}")
        print()

    print(f"\nRun with: python fix_broken_links.py --auto-only --no-dry-run")


def show_needs_confirmation(report):
    """Show items that need user confirmation."""
    print('='*80)
    print('NEEDS CONFIRMATION (50% <= Confidence < 90%)')
    print('='*80)
    print()

    confirm_fixes = [f for f in report['all_fixes_analyzed']
                     if 0.5 <= f['confidence'] < 0.9]

    if not confirm_fixes:
        print("No items need confirmation.")
        return

    print(f"Total: {len(confirm_fixes)} links\n")

    for i, fix in enumerate(confirm_fixes, 1):
        print(f"[{i}] {fix['source_file']}")
        print(f"    Link: {fix['broken_link']}")
        print(f"    Strategy: {fix['strategy']}")
        print(f"    Reason: {fix['reason']}")
        print(f"    Confidence: {fix['confidence']:.0%}")

        if fix['strategy'] == 'create_page':
            print(f"    Suggested: {fix['metadata'].get('suggested_location', 'N/A')}")
        elif fix['strategy'] == 'add_anchor':
            print(f"    Required anchor: {fix['metadata'].get('required_anchor', 'N/A')}")
            avail = fix['metadata'].get('available_anchors', [])
            if avail:
                print(f"    Similar anchors: {', '.join(avail[:5])}")
        elif fix['strategy'] == 'fix_typo':
            if 'similar_anchor' in fix['metadata']:
                print(f"    Suggested: {fix['metadata']['similar_anchor']}")
            if 'corrected_filename' in fix['metadata']:
                print(f"    Corrected: {fix['metadata']['corrected_filename']}")

        print()

    print(f"\nRun with: python fix_broken_links.py --interactive --no-dry-run")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Display broken link analysis report')
    parser.add_argument('--report', default='broken_links_fix_report.json',
                       help='Report file to display')
    parser.add_argument('--summary', action='store_true',
                       help='Show summary only')
    parser.add_argument('--by-strategy', action='store_true',
                       help='Group by fix strategy')
    parser.add_argument('--by-file', action='store_true',
                       help='Group by source file')
    parser.add_argument('--auto-only', action='store_true',
                       help='Show only auto-fixable items')
    parser.add_argument('--confirm-only', action='store_true',
                       help='Show only items needing confirmation')

    args = parser.parse_args()

    try:
        report = load_report(args.report)
    except FileNotFoundError:
        print(f"Error: Report file '{args.report}' not found.")
        print("Run 'python fix_broken_links.py --dry-run' first to generate it.")
        return 1

    # If no specific view requested, show all
    if not any([args.summary, args.by_strategy, args.by_file,
                args.auto_only, args.confirm_only]):
        show_summary(report)
        show_auto_fixable(report)
        print()
        show_needs_confirmation(report)
    else:
        if args.summary:
            show_summary(report)
        if args.by_strategy:
            show_by_strategy(report)
        if args.by_file:
            show_by_file(report)
        if args.auto_only:
            show_auto_fixable(report)
        if args.confirm_only:
            show_needs_confirmation(report)

    return 0


if __name__ == '__main__':
    exit(main())
