#!/usr/bin/env python3
r"""
LaTeX/MathJax Validation Script for Principia Metaphysica

This script detects rendering issues in LaTeX expressions within HTML files.

Features:
1. Extracts all LaTeX expressions from HTML files
2. Checks for balanced delimiters ($, \[, \], etc.)
3. Checks for common mistakes:
   - T$^{n}$ should be $T^{n}$
   - 24$\times$2 should be $24 \times 2$
   - Stray $\times$ between text
   - Hebrew letters that may not render (\gimel, \heth, \aleph, etc.)
   - Missing spaces around math blocks
4. Generates a report of all issues
5. Provides suggested fixes

Usage:
    python latex_checker.py [--path PATH] [--fix] [--verbose] [--json]

Examples:
    python latex_checker.py
    python latex_checker.py --path ../Pages
    python latex_checker.py --verbose --json > report.json

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from enum import Enum


class IssueSeverity(Enum):
    ERROR = "error"      # Will definitely break rendering
    WARNING = "warning"  # May cause rendering issues
    INFO = "info"        # Style suggestion


@dataclass
class LatexIssue:
    """Represents a single LaTeX issue found in the codebase."""
    file_path: str
    line_number: int
    column: int
    issue_type: str
    severity: IssueSeverity
    message: str
    context: str
    suggestion: Optional[str] = None
    original: Optional[str] = None
    fixed: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result['severity'] = self.severity.value
        return result


@dataclass
class LatexExpression:
    """Represents an extracted LaTeX expression."""
    content: str
    delimiter_type: str  # 'inline_dollar', 'inline_paren', 'display_dollar', 'display_bracket'
    start_pos: int
    end_pos: int
    line_number: int


@dataclass
class FileReport:
    """Report for a single file."""
    file_path: str
    expressions_found: int = 0
    issues: List[LatexIssue] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Complete validation report."""
    files_scanned: int = 0
    total_expressions: int = 0
    total_issues: int = 0
    issues_by_severity: Dict[str, int] = field(default_factory=lambda: {"error": 0, "warning": 0, "info": 0})
    issues_by_type: Dict[str, int] = field(default_factory=dict)
    file_reports: List[FileReport] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "summary": {
                "files_scanned": self.files_scanned,
                "total_expressions": self.total_expressions,
                "total_issues": self.total_issues,
                "issues_by_severity": self.issues_by_severity,
                "issues_by_type": self.issues_by_type
            },
            "files": [
                {
                    "file_path": fr.file_path,
                    "expressions_found": fr.expressions_found,
                    "issues": [issue.to_dict() for issue in fr.issues]
                }
                for fr in self.file_reports if fr.issues
            ]
        }


class LatexChecker:
    """Main class for checking LaTeX expressions in HTML files."""

    # Regex to match script and style blocks (including their content)
    SCRIPT_STYLE_PATTERN = re.compile(
        r'<script[^>]*>.*?</script>|<style[^>]*>.*?</style>',
        re.DOTALL | re.IGNORECASE
    )

    # Regex to match HTML comments
    COMMENT_PATTERN = re.compile(r'<!--.*?-->', re.DOTALL)

    # Regex to match code blocks and pre tags
    CODE_PATTERN = re.compile(
        r'<code[^>]*>.*?</code>|<pre[^>]*>.*?</pre>',
        re.DOTALL | re.IGNORECASE
    )

    # Hebrew letters that may not render in all MathJax configurations
    HEBREW_LETTERS = {
        r'\gimel': 'gimel (may need \\text{} or amssymb)',
        r'\heth': 'heth (non-standard, use Unicode or custom macro)',
        r'\aleph': 'aleph (standard, but verify MathJax config)',
        r'\beth': 'beth (may need amssymb)',
        r'\daleth': 'daleth (may need amssymb)',
    }

    # Common LaTeX mistakes patterns
    MISTAKE_PATTERNS = [
        # Text followed by $^{...}$ - superscript should be inside math
        (r'([A-Za-z0-9])\$\^(\{[^}]+\})\$',
         r'$\1^{\2}$',
         'Superscript outside math mode',
         'Move text inside math expression'),

        # Text followed by $_{...}$ - subscript should be inside math
        (r'([A-Za-z0-9])\$_(\{[^}]+\})\$',
         r'$\1_{\2}$',
         'Subscript outside math mode',
         'Move text inside math expression'),

        # Number$\times$Number pattern - multiplication should be in math mode
        (r'(\d+)\$\\times\$(\d+)',
         r'$\1 \\times \2$',
         'Multiplication between text numbers',
         'Put entire expression in math mode'),

        # D$\times$2 pattern
        (r'([A-Za-z]+)\$\\times\$(\d+)',
         r'$\1 \\times \2$',
         'Mixed text/math multiplication',
         'Put entire expression in math mode'),
    ]

    # Patterns that indicate stray math operators
    STRAY_OPERATOR_PATTERNS = [
        (r'\$\\times\$', 'Isolated \\times in separate math blocks'),
        (r'\$\\cdot\$', 'Isolated \\cdot in separate math blocks'),
        (r'\$\\pm\$', 'Isolated \\pm in separate math blocks'),
        (r'\$\\div\$', 'Isolated \\div in separate math blocks'),
    ]

    # Delimiter pairs for balance checking
    DELIMITER_PAIRS = {
        '{': '}',
        '[': ']',
        '(': ')',
        '\\{': '\\}',
        '\\[': '\\]',
        '\\(': '\\)',
        '\\left(': '\\right)',
        '\\left[': '\\right]',
        '\\left\\{': '\\right\\}',
        '\\left|': '\\right|',
        '\\left.': '\\right.',
        '\\begin{': '\\end{',
    }

    def __init__(self, base_path: str, verbose: bool = False):
        self.base_path = Path(base_path)
        self.verbose = verbose
        self.report = ValidationReport()

    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def strip_non_content(self, content: str) -> Tuple[str, List[Tuple[int, int]]]:
        """
        Strip script, style, code, and comment blocks from content.
        Returns the cleaned content and a list of (start, end) ranges that were removed.
        This prevents false positives from JavaScript template literals like ${...}.
        """
        removed_ranges = []

        # Find all ranges to remove
        for pattern in [self.SCRIPT_STYLE_PATTERN, self.COMMENT_PATTERN, self.CODE_PATTERN]:
            for match in pattern.finditer(content):
                removed_ranges.append((match.start(), match.end()))

        # Sort and merge overlapping ranges
        removed_ranges.sort()
        merged_ranges = []
        for start, end in removed_ranges:
            if merged_ranges and start <= merged_ranges[-1][1]:
                merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))
            else:
                merged_ranges.append((start, end))

        # Create cleaned content by replacing removed sections with spaces
        # (to preserve line numbers and positions)
        cleaned = list(content)
        for start, end in merged_ranges:
            for i in range(start, end):
                if i < len(cleaned) and cleaned[i] != '\n':
                    cleaned[i] = ' '

        return ''.join(cleaned), merged_ranges

    def is_in_removed_range(self, pos: int, removed_ranges: List[Tuple[int, int]]) -> bool:
        """Check if a position is within any removed range."""
        for start, end in removed_ranges:
            if start <= pos < end:
                return True
        return False

    def find_html_files(self) -> List[Path]:
        """Find all HTML files in the base path, excluding node_modules and other directories."""
        exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__', 'venv'}
        html_files = []

        # If base_path is a file, just return it
        if self.base_path.is_file():
            if str(self.base_path).endswith('.html'):
                return [self.base_path]
            else:
                return []

        for root, dirs, files in os.walk(self.base_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.html'):
                    html_files.append(Path(root) / file)

        return html_files

    def extract_latex_expressions(self, content: str) -> List[LatexExpression]:
        """Extract all LaTeX expressions from HTML content."""
        expressions = []

        # Track line numbers
        line_starts = [0]
        for i, char in enumerate(content):
            if char == '\n':
                line_starts.append(i + 1)

        def get_line_number(pos: int) -> int:
            for i, start in enumerate(line_starts):
                if start > pos:
                    return i
            return len(line_starts)

        # Pattern for display math $$...$$
        for match in re.finditer(r'\$\$(.+?)\$\$', content, re.DOTALL):
            expressions.append(LatexExpression(
                content=match.group(1),
                delimiter_type='display_dollar',
                start_pos=match.start(),
                end_pos=match.end(),
                line_number=get_line_number(match.start())
            ))

        # Pattern for display math \[...\]
        for match in re.finditer(r'\\\[(.+?)\\\]', content, re.DOTALL):
            expressions.append(LatexExpression(
                content=match.group(1),
                delimiter_type='display_bracket',
                start_pos=match.start(),
                end_pos=match.end(),
                line_number=get_line_number(match.start())
            ))

        # Pattern for inline math $...$ (not $$)
        # Need to be careful not to match inside $$...$$ blocks
        display_ranges = [(e.start_pos, e.end_pos) for e in expressions if e.delimiter_type == 'display_dollar']

        for match in re.finditer(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', content):
            # Check if this match is inside a display math block
            in_display = any(start <= match.start() < end for start, end in display_ranges)
            if not in_display:
                expressions.append(LatexExpression(
                    content=match.group(1),
                    delimiter_type='inline_dollar',
                    start_pos=match.start(),
                    end_pos=match.end(),
                    line_number=get_line_number(match.start())
                ))

        # Pattern for inline math \(...\)
        for match in re.finditer(r'\\\((.+?)\\\)', content, re.DOTALL):
            expressions.append(LatexExpression(
                content=match.group(1),
                delimiter_type='inline_paren',
                start_pos=match.start(),
                end_pos=match.end(),
                line_number=get_line_number(match.start())
            ))

        return sorted(expressions, key=lambda x: x.start_pos)

    def check_delimiter_balance(self, latex: str, line_number: int, file_path: str) -> List[LatexIssue]:
        """Check for balanced delimiters in a LaTeX expression."""
        issues = []

        # Simple brace counting
        brace_count = 0
        bracket_count = 0
        paren_count = 0

        i = 0
        while i < len(latex):
            # Handle escaped characters
            if latex[i] == '\\' and i + 1 < len(latex):
                next_char = latex[i + 1]
                if next_char in '{}[]()':
                    i += 2
                    continue
                elif latex[i:].startswith('\\left') or latex[i:].startswith('\\right'):
                    # Skip \left and \right commands
                    if latex[i:].startswith('\\left'):
                        i += 5
                    else:
                        i += 6
                    continue

            if latex[i] == '{':
                brace_count += 1
            elif latex[i] == '}':
                brace_count -= 1
                if brace_count < 0:
                    issues.append(LatexIssue(
                        file_path=file_path,
                        line_number=line_number,
                        column=i,
                        issue_type='unbalanced_braces',
                        severity=IssueSeverity.ERROR,
                        message='Unmatched closing brace }',
                        context=latex[max(0, i-20):i+20],
                        suggestion='Add matching opening brace or remove extra closing brace'
                    ))
            elif latex[i] == '[':
                bracket_count += 1
            elif latex[i] == ']':
                bracket_count -= 1
            elif latex[i] == '(':
                paren_count += 1
            elif latex[i] == ')':
                paren_count -= 1

            i += 1

        if brace_count > 0:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=line_number,
                column=0,
                issue_type='unbalanced_braces',
                severity=IssueSeverity.ERROR,
                message=f'Unclosed braces: {brace_count} opening brace(s) without matching closing brace',
                context=latex[:100] + ('...' if len(latex) > 100 else ''),
                suggestion='Add matching closing brace(s)'
            ))

        if bracket_count != 0:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=line_number,
                column=0,
                issue_type='unbalanced_brackets',
                severity=IssueSeverity.WARNING,
                message=f'Unbalanced brackets: difference of {bracket_count}',
                context=latex[:100] + ('...' if len(latex) > 100 else ''),
                suggestion='Check bracket pairs'
            ))

        # Check for \left without \right and vice versa
        left_count = len(re.findall(r'\\left[^a-zA-Z]', latex))
        right_count = len(re.findall(r'\\right[^a-zA-Z]', latex))

        if left_count != right_count:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=line_number,
                column=0,
                issue_type='unbalanced_left_right',
                severity=IssueSeverity.ERROR,
                message=f'Unbalanced \\left/\\right: {left_count} \\left vs {right_count} \\right',
                context=latex[:100] + ('...' if len(latex) > 100 else ''),
                suggestion='Each \\left must have a matching \\right'
            ))

        # Check for \begin without \end
        begin_envs = re.findall(r'\\begin\{([^}]+)\}', latex)
        end_envs = re.findall(r'\\end\{([^}]+)\}', latex)

        begin_counts = defaultdict(int)
        end_counts = defaultdict(int)

        for env in begin_envs:
            begin_counts[env] += 1
        for env in end_envs:
            end_counts[env] += 1

        all_envs = set(begin_counts.keys()) | set(end_counts.keys())
        for env in all_envs:
            if begin_counts[env] != end_counts[env]:
                issues.append(LatexIssue(
                    file_path=file_path,
                    line_number=line_number,
                    column=0,
                    issue_type='unbalanced_environment',
                    severity=IssueSeverity.ERROR,
                    message=f'Unbalanced environment "{env}": {begin_counts[env]} \\begin vs {end_counts[env]} \\end',
                    context=latex[:100] + ('...' if len(latex) > 100 else ''),
                    suggestion=f'Each \\begin{{{env}}} must have a matching \\end{{{env}}}'
                ))

        return issues

    def check_hebrew_letters(self, latex: str, line_number: int, file_path: str) -> List[LatexIssue]:
        """Check for Hebrew letters that may not render correctly."""
        issues = []

        for letter, description in self.HEBREW_LETTERS.items():
            if letter in latex:
                # Find all occurrences
                for match in re.finditer(re.escape(letter), latex):
                    issues.append(LatexIssue(
                        file_path=file_path,
                        line_number=line_number,
                        column=match.start(),
                        issue_type='hebrew_letter',
                        severity=IssueSeverity.WARNING,
                        message=f'Hebrew letter {letter} found - {description}',
                        context=latex[max(0, match.start()-20):match.end()+20],
                        suggestion='Verify MathJax configuration supports this letter or use Unicode'
                    ))

        return issues

    def check_spacing_issues(self, content: str, file_path: str) -> List[LatexIssue]:
        """Check for spacing issues around math blocks."""
        issues = []

        # Track line numbers
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Check for missing space before $ (but not after < or " or other valid chars)
            for match in re.finditer(r'([a-zA-Z0-9])\$(?!\$)', line):
                if match.group(1).isalpha():
                    # This might be intentional, like x$y$ or variable$
                    pass  # Don't flag as these are often valid

            # Check for missing space after $ (but not before < or " or other valid chars)
            for match in re.finditer(r'(?<!\$)\$(?!\$)([^$]+?)\$([a-zA-Z])', line):
                # Pattern like $x$word - might be intentional
                pass  # Don't flag these

            # Check for word$\times$ patterns more specifically
            for match in re.finditer(r'(\w+)\$\\times\$(\w+)', line):
                issues.append(LatexIssue(
                    file_path=file_path,
                    line_number=line_num,
                    column=match.start(),
                    issue_type='fragmented_math',
                    severity=IssueSeverity.WARNING,
                    message='Multiplication operator in isolated math block between words',
                    context=match.group(0),
                    original=match.group(0),
                    fixed=f'${match.group(1)} \\times {match.group(2)}$',
                    suggestion='Combine into single math expression'
                ))

        return issues

    def check_common_mistakes(self, content: str, file_path: str) -> List[LatexIssue]:
        """Check for common LaTeX mistakes in HTML content."""
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern, replacement, issue_desc, suggestion in self.MISTAKE_PATTERNS:
                for match in re.finditer(pattern, line):
                    # Generate the fixed version
                    fixed = re.sub(pattern, replacement, match.group(0))

                    issues.append(LatexIssue(
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start(),
                        issue_type='common_mistake',
                        severity=IssueSeverity.WARNING,
                        message=issue_desc,
                        context=line[max(0, match.start()-10):match.end()+10],
                        original=match.group(0),
                        fixed=fixed,
                        suggestion=suggestion
                    ))

            # Check for stray operators
            for pattern, description in self.STRAY_OPERATOR_PATTERNS:
                for match in re.finditer(pattern, line):
                    # Check if this is actually isolated (not part of a larger expression)
                    before = line[max(0, match.start()-5):match.start()]
                    after = line[match.end():match.end()+5]

                    # If there's a $ right before or after, it might be part of an expression
                    if not (before.endswith('$') or after.startswith('$')):
                        issues.append(LatexIssue(
                            file_path=file_path,
                            line_number=line_num,
                            column=match.start(),
                            issue_type='stray_operator',
                            severity=IssueSeverity.INFO,
                            message=description,
                            context=line[max(0, match.start()-15):match.end()+15],
                            suggestion='Consider combining with surrounding content in one math block'
                        ))

        return issues

    def check_unmatched_delimiters(self, content: str, file_path: str) -> List[LatexIssue]:
        """Check for unmatched math delimiters at the file level."""
        issues = []
        lines = content.split('\n')

        # Count dollar signs (excluding $$ and escaped \$)
        single_dollar_pattern = r'(?<!\$)(?<!\\)\$(?!\$)'

        for line_num, line in enumerate(lines, 1):
            # Skip lines that are likely in script or style blocks
            if '<script' in line.lower() or '<style' in line.lower():
                continue

            dollars = list(re.finditer(single_dollar_pattern, line))
            if len(dollars) % 2 != 0:
                issues.append(LatexIssue(
                    file_path=file_path,
                    line_number=line_num,
                    column=dollars[-1].start() if dollars else 0,
                    issue_type='unmatched_delimiter',
                    severity=IssueSeverity.ERROR,
                    message=f'Odd number of $ delimiters on line ({len(dollars)} found)',
                    context=line[:100] + ('...' if len(line) > 100 else ''),
                    suggestion='Check for missing or extra $ delimiter'
                ))

        # Check for unmatched \[ and \]
        open_display = content.count('\\[')
        close_display = content.count('\\]')

        if open_display != close_display:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=0,
                column=0,
                issue_type='unmatched_display_delimiters',
                severity=IssueSeverity.ERROR,
                message=f'Unmatched display math delimiters: {open_display} \\[ vs {close_display} \\]',
                context='File-level check',
                suggestion='Check for missing or extra \\[ or \\] delimiter'
            ))

        # Check for unmatched \( and \)
        open_inline = content.count('\\(')
        close_inline = content.count('\\)')

        if open_inline != close_inline:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=0,
                column=0,
                issue_type='unmatched_inline_delimiters',
                severity=IssueSeverity.WARNING,
                message=f'Unmatched inline math delimiters: {open_inline} \\( vs {close_inline} \\)',
                context='File-level check',
                suggestion='Check for missing or extra \\( or \\) delimiter'
            ))

        return issues

    def check_double_subscript_superscript(self, latex: str, line_number: int, file_path: str) -> List[LatexIssue]:
        """Check for double subscripts or superscripts which cause errors."""
        issues = []

        # Pattern for double subscript like x_a_b (should be x_{a_b} or x_a{}^b)
        double_sub = re.search(r'([^_])_([^{])_', latex)
        if double_sub:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=line_number,
                column=double_sub.start(),
                issue_type='double_subscript',
                severity=IssueSeverity.ERROR,
                message='Double subscript detected - will cause LaTeX error',
                context=latex[max(0, double_sub.start()-10):double_sub.end()+10],
                suggestion='Use braces: x_{a_b} or separate scripts: x_a{}_{b}'
            ))

        # Pattern for double superscript like x^a^b
        double_sup = re.search(r'([^^])\^([^{])\^', latex)
        if double_sup:
            issues.append(LatexIssue(
                file_path=file_path,
                line_number=line_number,
                column=double_sup.start(),
                issue_type='double_superscript',
                severity=IssueSeverity.ERROR,
                message='Double superscript detected - will cause LaTeX error',
                context=latex[max(0, double_sup.start()-10):double_sup.end()+10],
                suggestion='Use braces: x^{a^b} or separate scripts: x^a{}^{b}'
            ))

        return issues

    def check_file(self, file_path: Path) -> FileReport:
        """Check a single HTML file for LaTeX issues."""
        self.log(f"Checking: {file_path}")

        file_report = FileReport(file_path=str(file_path))

        try:
            original_content = file_path.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            file_report.issues.append(LatexIssue(
                file_path=str(file_path),
                line_number=0,
                column=0,
                issue_type='file_read_error',
                severity=IssueSeverity.ERROR,
                message=f'Could not read file: {e}',
                context='',
                suggestion='Check file encoding and permissions'
            ))
            return file_report

        # Strip script, style, code blocks, and comments to avoid false positives
        # from JavaScript template literals like ${...}
        cleaned_content, removed_ranges = self.strip_non_content(original_content)

        # Extract LaTeX expressions from cleaned content
        expressions = self.extract_latex_expressions(cleaned_content)
        file_report.expressions_found = len(expressions)

        # Check each expression
        for expr in expressions:
            # Check delimiter balance
            file_report.issues.extend(
                self.check_delimiter_balance(expr.content, expr.line_number, str(file_path))
            )

            # Check Hebrew letters
            file_report.issues.extend(
                self.check_hebrew_letters(expr.content, expr.line_number, str(file_path))
            )

            # Check for double subscripts/superscripts
            file_report.issues.extend(
                self.check_double_subscript_superscript(expr.content, expr.line_number, str(file_path))
            )

        # File-level checks (on cleaned content)
        file_report.issues.extend(self.check_unmatched_delimiters(cleaned_content, str(file_path)))
        file_report.issues.extend(self.check_common_mistakes(cleaned_content, str(file_path)))
        file_report.issues.extend(self.check_spacing_issues(cleaned_content, str(file_path)))

        return file_report

    def run(self) -> ValidationReport:
        """Run the validation on all HTML files."""
        html_files = self.find_html_files()
        self.log(f"Found {len(html_files)} HTML files to check")

        self.report.files_scanned = len(html_files)

        for file_path in html_files:
            file_report = self.check_file(file_path)
            self.report.file_reports.append(file_report)
            self.report.total_expressions += file_report.expressions_found

            for issue in file_report.issues:
                self.report.total_issues += 1
                self.report.issues_by_severity[issue.severity.value] += 1

                if issue.issue_type not in self.report.issues_by_type:
                    self.report.issues_by_type[issue.issue_type] = 0
                self.report.issues_by_type[issue.issue_type] += 1

        return self.report

    def print_report(self, use_json: bool = False):
        """Print the validation report."""
        if use_json:
            print(json.dumps(self.report.to_dict(), indent=2))
            return

        print("\n" + "=" * 70)
        print("LATEX/MATHJAX VALIDATION REPORT")
        print("=" * 70)

        print(f"\nFiles scanned: {self.report.files_scanned}")
        print(f"Total LaTeX expressions found: {self.report.total_expressions}")
        print(f"Total issues found: {self.report.total_issues}")

        print("\nIssues by severity:")
        for severity, count in self.report.issues_by_severity.items():
            if count > 0:
                print(f"  {severity.upper()}: {count}")

        print("\nIssues by type:")
        for issue_type, count in sorted(self.report.issues_by_type.items(), key=lambda x: -x[1]):
            print(f"  {issue_type}: {count}")

        # Print detailed issues
        files_with_issues = [fr for fr in self.report.file_reports if fr.issues]

        if files_with_issues:
            print("\n" + "-" * 70)
            print("DETAILED ISSUES")
            print("-" * 70)

            for file_report in files_with_issues:
                rel_path = os.path.relpath(file_report.file_path, self.base_path)
                print(f"\n{rel_path} ({len(file_report.issues)} issues):")

                for issue in sorted(file_report.issues, key=lambda x: (x.line_number, x.column)):
                    severity_indicator = {
                        IssueSeverity.ERROR: "[ERROR]  ",
                        IssueSeverity.WARNING: "[WARN]   ",
                        IssueSeverity.INFO: "[INFO]   "
                    }[issue.severity]

                    print(f"  Line {issue.line_number}: {severity_indicator}{issue.message}")
                    print(f"    Context: {issue.context[:60]}{'...' if len(issue.context) > 60 else ''}")

                    if issue.original and issue.fixed:
                        print(f"    Original: {issue.original}")
                        print(f"    Suggested: {issue.fixed}")
                    elif issue.suggestion:
                        print(f"    Suggestion: {issue.suggestion}")
                    print()
        else:
            print("\nNo issues found! All LaTeX expressions appear valid.")

        print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Validate LaTeX/MathJax expressions in HTML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python latex_checker.py                    # Check current directory
  python latex_checker.py --path ../Pages    # Check specific directory
  python latex_checker.py --verbose          # Show progress
  python latex_checker.py --json             # Output as JSON
  python latex_checker.py --json > report.json  # Save JSON report
        """
    )

    parser.add_argument(
        '--path', '-p',
        default='.',
        help='Path to check (default: current directory)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output report as JSON'
    )

    parser.add_argument(
        '--exclude', '-e',
        nargs='*',
        default=[],
        help='Additional directories to exclude'
    )

    args = parser.parse_args()

    # Resolve the path
    base_path = Path(args.path).resolve()

    if not base_path.exists():
        print(f"Error: Path does not exist: {base_path}", file=sys.stderr)
        sys.exit(1)

    checker = LatexChecker(str(base_path), verbose=args.verbose)
    checker.run()
    checker.print_report(use_json=args.json)

    # Exit with error code if there are errors
    if checker.report.issues_by_severity.get('error', 0) > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
