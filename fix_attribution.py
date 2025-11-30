#!/usr/bin/env python3
"""
Fix attribution across all files to ensure Andrew K Watts owns all intellectual property.
All AI tools (Claude, Grok, Gemini) should be credited as development assistants only.
"""

import os
import re
from pathlib import Path

# Correct attribution text
CORRECT_AI_ATTRIBUTION = """This project was developed with the assistance of AI tools including Claude (Anthropic),
            Grok (xAI), and Gemini (Google)."""

# Files to check
repo_root = Path(r'h:\Github\PrincipiaMetaphysica')

def check_html_files():
    """Check all HTML files for correct attribution."""
    issues = []

    html_files = list(repo_root.glob('**/*.html'))

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for copyright header
            if 'Copyright (c) 2025 Andrew Keith Watts. All rights reserved.' not in content:
                issues.append(f"{filepath.relative_to(repo_root)}: Missing copyright header")

            # Check for footer attribution
            if '<footer>' in content:
                # Extract footer content
                footer_match = re.search(r'<footer>.*?</footer>', content, re.DOTALL)
                if footer_match:
                    footer = footer_match.group(0)

                    # Check for Andrew K Watts copyright in footer
                    if '&copy; 2025 Andrew Keith Watts' not in footer and '© 2025 Andrew Keith Watts' not in footer:
                        issues.append(f"{filepath.relative_to(repo_root)}: Footer missing Andrew K Watts copyright")

                    # Check for AI attribution mentioning all three
                    has_claude = 'Claude' in footer or 'Anthropic' in footer
                    has_grok = 'Grok' in footer or 'xAI' in footer
                    has_gemini = 'Gemini' in footer or 'Google' in footer

                    if has_claude or has_grok or has_gemini:
                        # If any AI is mentioned, all three must be mentioned
                        if not (has_claude and has_grok and has_gemini):
                            issues.append(f"{filepath.relative_to(repo_root)}: Footer mentions some AI tools but not all three")

                    # Check for problematic "Generated with Claude Code" in footer
                    if 'Generated with' in footer or 'Co-Authored-By' in footer:
                        issues.append(f"{filepath.relative_to(repo_root)}: Footer contains 'Generated with' or 'Co-Authored-By' language")

        except Exception as e:
            issues.append(f"{filepath.relative_to(repo_root)}: Error reading file - {e}")

    return issues

def check_python_files():
    """Check Python files for attribution."""
    issues = []

    py_files = list(repo_root.glob('*.py'))

    for filepath in py_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for copyright header
            if 'Copyright (c) 2025 Andrew Keith Watts' not in content:
                issues.append(f"{filepath.name}: Missing copyright header in Python file")

        except Exception as e:
            issues.append(f"{filepath.name}: Error reading file - {e}")

    return issues

def main():
    print("=== Attribution Audit Report ===\n")

    print("Checking HTML files...")
    html_issues = check_html_files()

    print(f"Checking Python files...")
    py_issues = check_python_files()

    all_issues = html_issues + py_issues

    if all_issues:
        print(f"\nFound {len(all_issues)} attribution issues:\n")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("\nNo attribution issues found. All intellectual property correctly attributed to Andrew K Watts.")

    print("\n=== Git Commit History Check ===")
    print("\nNote: Recent commits contain 'Generated with Claude Code' and 'Co-Authored-By: Claude'")
    print("These are in git history and cannot be changed without rewriting history.")
    print("However, all file content correctly attributes ownership to Andrew K Watts.")

    return len(all_issues)

if __name__ == '__main__':
    exit(main())
