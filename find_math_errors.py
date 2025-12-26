#!/usr/bin/env python3
"""
Script to identify potential MathJax/LaTeX errors in HTML files.
Looks for common issues like:
- Unbalanced delimiters
- Invalid LaTeX commands
- Missing escape characters
- Broken variable references
"""

import re
import os
from pathlib import Path

def find_math_blocks(content, filename):
    """Find all math blocks (inline $...$ and display $$...$$)"""
    errors = []

    # Find display math blocks $$...$$
    display_pattern = r'\$\$(.*?)\$\$'
    display_matches = re.finditer(display_pattern, content, re.DOTALL)

    for match in display_matches:
        math_content = match.group(1)
        line_num = content[:match.start()].count('\n') + 1
        issues = check_math_content(math_content, 'display')
        if issues:
            errors.append({
                'file': filename,
                'line': line_num,
                'type': 'display',
                'content': math_content[:100] + '...' if len(math_content) > 100 else math_content,
                'issues': issues
            })

    # Find inline math blocks $...$  (but not $$)
    # First remove display blocks to avoid double-matching
    content_no_display = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
    inline_pattern = r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)'
    inline_matches = re.finditer(inline_pattern, content_no_display, re.DOTALL)

    for match in inline_matches:
        math_content = match.group(1)
        # Find actual line in original content
        line_num = content_no_display[:match.start()].count('\n') + 1
        issues = check_math_content(math_content, 'inline')
        if issues:
            errors.append({
                'file': filename,
                'line': line_num,
                'type': 'inline',
                'content': math_content[:100] + '...' if len(math_content) > 100 else math_content,
                'issues': issues
            })

    return errors

def check_math_content(content, math_type):
    """Check math content for common issues"""
    issues = []

    # Check for unbalanced braces
    brace_count = content.count('{') - content.count('}')
    if brace_count != 0:
        issues.append(f"Unbalanced braces: {'+' if brace_count > 0 else ''}{brace_count}")

    # Check for unbalanced parentheses in \left \right
    left_count = content.count('\\left')
    right_count = content.count('\\right')
    if left_count != right_count:
        issues.append(f"Unbalanced \\left/\\right: {left_count} left, {right_count} right")

    # Check for common typos in LaTeX commands
    typo_patterns = [
        (r'\\textt(?!ext)', 'Possible typo: \\textt (should be \\text?)'),
        (r'\\textm(?!athrm)', 'Possible typo: \\textm'),
        (r'\\frc(?!ac)', 'Possible typo: \\frc (should be \\frac?)'),
        (r'\\sqt(?!rt)', 'Possible typo: \\sqt (should be \\sqrt?)'),
        (r'\\bgin(?!in)', 'Possible typo: \\bgin (should be \\begin?)'),
        (r'\\edn(?!d)', 'Possible typo: \\edn (should be \\end?)'),
        (r'\\lamda', 'Possible typo: \\lamda (should be \\lambda?)'),
        (r'\\apha', 'Possible typo: \\apha (should be \\alpha?)'),
        (r'\\bera', 'Possible typo: \\bera (should be \\beta?)'),
        (r'\\gama', 'Possible typo: \\gama (should be \\gamma?)'),
        (r'\\deta', 'Possible typo: \\deta (should be \\delta?)'),
        (r'\\epsion', 'Possible typo: \\epsion (should be \\epsilon?)'),
        (r'\\simga', 'Possible typo: \\simga (should be \\sigma?)'),
        (r'\\omgea', 'Possible typo: \\omgea (should be \\omega?)'),
    ]

    for pattern, msg in typo_patterns:
        if re.search(pattern, content):
            issues.append(msg)

    # Check for broken \text{} commands (common issue)
    text_pattern = r'\\text\{([^}]*)\}'
    text_matches = re.findall(text_pattern, content)
    for text_match in text_matches:
        if '\\' in text_match and not text_match.startswith('\\'):
            issues.append(f"Possible broken \\text{{}} content: {text_match[:50]}")

    # Check for HTML entities inside math (common error)
    if '&' in content and not '\\&' in content:
        html_entities = re.findall(r'&[a-zA-Z]+;', content)
        if html_entities:
            issues.append(f"HTML entities in math: {html_entities[:3]}")

    # Check for unescaped special characters
    if '<' in content or '>' in content:
        # Check if they're part of valid LaTeX
        if not re.search(r'\\[lg]eq?', content):
            issues.append("Unescaped < or > (use \\lt, \\gt or \\leq, \\geq)")

    # Check for empty subscripts/superscripts
    if '_{}'in content or '^{}' in content:
        issues.append("Empty subscript or superscript")

    # Check for common undefined commands
    undefined_cmds = [
        r'\\mathbb\{[A-Z]\}',  # This is valid, but check context
        r'\\textbf\{',  # Should use \mathbf in math mode
        r'\\textit\{',  # Should use \mathit in math mode
    ]

    # Check for potential variable reference issues (PM.xxx patterns in math)
    if 'PM.' in content or 'pm-value' in content:
        issues.append("JavaScript variable reference inside math block")

    # Check for \\ at end of inline math (invalid in inline)
    if math_type == 'inline' and content.strip().endswith('\\\\'):
        issues.append("Line break \\\\ at end of inline math")

    # Check for missing closing in begin/end blocks
    begins = re.findall(r'\\begin\{(\w+)\}', content)
    ends = re.findall(r'\\end\{(\w+)\}', content)
    if begins != ends:
        issues.append(f"Mismatched begin/end: begins={begins}, ends={ends}")

    return issues

def scan_file(filepath):
    """Scan a single file for math errors"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return find_math_blocks(content, str(filepath))
    except Exception as e:
        return [{'file': str(filepath), 'error': str(e)}]

def main():
    """Main function to scan all HTML files"""
    base_path = Path('.')

    # Files to scan
    html_files = list(base_path.glob('*.html')) + list(base_path.glob('sections/*.html')) + list(base_path.glob('foundations/*.html'))

    all_errors = []

    for filepath in html_files:
        errors = scan_file(filepath)
        all_errors.extend(errors)

    # Print results
    print("=" * 80)
    print("MATH ERROR SCAN RESULTS")
    print("=" * 80)

    if not all_errors:
        print("\nNo potential math errors found!")
    else:
        print(f"\nFound {len(all_errors)} potential issues:\n")

        # Group by file
        by_file = {}
        for err in all_errors:
            fname = err.get('file', 'unknown')
            if fname not in by_file:
                by_file[fname] = []
            by_file[fname].append(err)

        for fname, errors in sorted(by_file.items()):
            print(f"\n{'='*60}")
            print(f"FILE: {fname}")
            print(f"{'='*60}")
            for err in errors:
                if 'error' in err:
                    print(f"  ERROR: {err['error']}")
                else:
                    print(f"\n  Line ~{err['line']} ({err['type']} math):")
                    print(f"  Content: {err['content']}")
                    for issue in err['issues']:
                        print(f"    - {issue}")

    return all_errors

if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    main()
