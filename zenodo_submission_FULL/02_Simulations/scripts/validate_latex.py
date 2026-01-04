#!/usr/bin/env python3
"""
validate_latex.py - Validate LaTeX/MathJax expressions in HTML files

This script scans all HTML files for LaTeX expressions and detects common issues:
- Unmatched $ delimiters
- $\times$ used alone (should be inside larger expression)
- Superscripts $^{...}$ without base
- Subscripts $_{...}$ without base
- Text adjacent to math without spaces
- Known problematic patterns (empty math, malformed commands)

Usage:
    python scripts/validate_latex.py                    # Scan and report issues
    python scripts/validate_latex.py --fix             # Auto-fix common issues
    python scripts/validate_latex.py --verbose         # Show all matches
    python scripts/validate_latex.py --file FILE       # Check specific file
    python scripts/validate_latex.py --exclude-dirs X  # Exclude directories (comma-separated)

Author: Andrew Keith Watts
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, NamedTuple
from dataclasses import dataclass, field
from enum import Enum, auto


class IssueSeverity(Enum):
    """Severity levels for issues."""
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


@dataclass
class LatexIssue:
    """Represents a LaTeX issue found in a file."""
    file: str
    line: int
    column: int
    severity: IssueSeverity
    code: str
    message: str
    context: str
    fix: Optional[str] = None

    def __str__(self) -> str:
        severity_str = {
            IssueSeverity.ERROR: "ERROR",
            IssueSeverity.WARNING: "WARN",
            IssueSeverity.INFO: "INFO"
        }[self.severity]
        return f"{self.file}:{self.line}:{self.column}: [{severity_str}] {self.code}: {self.message}"


@dataclass
class ValidationStats:
    """Statistics from validation run."""
    files_scanned: int = 0
    files_with_issues: int = 0
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    issues_fixed: int = 0


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


# Issue codes
class IssueCodes:
    UNMATCHED_DOLLAR = "LTX001"
    LONE_TIMES = "LTX002"
    SUPERSCRIPT_NO_BASE = "LTX003"
    SUBSCRIPT_NO_BASE = "LTX004"
    NO_SPACE_BEFORE_MATH = "LTX005"
    NO_SPACE_AFTER_MATH = "LTX006"
    EMPTY_MATH = "LTX007"
    UNCLOSED_BRACE = "LTX008"
    NESTED_DOLLARS = "LTX009"
    INVALID_ESCAPE = "LTX010"
    DISPLAY_MATH_INLINE = "LTX011"
    LONE_OPERATOR = "LTX012"
    MISMATCHED_DELIMITERS = "LTX013"
    DOUBLE_SUPERSCRIPT = "LTX014"
    DOUBLE_SUBSCRIPT = "LTX015"


# Patterns for detecting issues
class LatexPatterns:
    """Compiled regex patterns for LaTeX detection."""

    # Match inline math: $...$
    INLINE_MATH = re.compile(r'(?<!\$)\$(?!\$)([^$]*?)(?<!\$)\$(?!\$)')

    # Match display math: $$...$$
    DISPLAY_MATH = re.compile(r'\$\$([^$]*?)\$\$', re.DOTALL)

    # Match \(...\) inline math
    PAREN_INLINE = re.compile(r'\\\(([^)]*?)\\\)')

    # Match \[...\] display math
    BRACKET_DISPLAY = re.compile(r'\\\[([^\]]*?)\\\]', re.DOTALL)

    # Lone times: $\times$ by itself
    LONE_TIMES = re.compile(r'\$\\times\$')

    # Superscript without base: $^{...}$
    SUPERSCRIPT_NO_BASE = re.compile(r'\$\s*\^')

    # Subscript without base: $_{...}$
    SUBSCRIPT_NO_BASE = re.compile(r'\$\s*_')

    # Empty math: $$ or $   $
    EMPTY_MATH = re.compile(r'\$\s*\$')

    # Text immediately before math (no space)
    NO_SPACE_BEFORE = re.compile(r'[a-zA-Z0-9)}\]]\$[^$]')

    # Text immediately after math (no space)
    NO_SPACE_AFTER = re.compile(r'[^$]\$[a-zA-Z0-9({[\[]')

    # Double superscript: ^{...}^{...}
    DOUBLE_SUPERSCRIPT = re.compile(r'\^{[^}]*}\s*\^')

    # Double subscript: _{...}_{...}
    DOUBLE_SUBSCRIPT = re.compile(r'_{[^}]*}\s*_')

    # Nested dollars: $$$ or more
    NESTED_DOLLARS = re.compile(r'\${3,}')

    # Lone operators that should be in larger expressions
    LONE_OPERATORS = re.compile(r'\$\\(pm|mp|cdot|div|ast)\$')

    # Common malformed commands
    MALFORMED_COMMANDS = [
        (re.compile(r'\\frac\s*{[^}]*}\s*$'), "Incomplete \\frac - missing second argument"),
        (re.compile(r'\\sqrt\s*\['), "\\sqrt with optional argument but no main argument"),
        (re.compile(r'\\begin{[^}]*}(?:(?!\\end{).)*$', re.DOTALL), "Unclosed \\begin environment"),
    ]


class LatexValidator:
    """Validates LaTeX expressions in HTML files."""

    def __init__(self, verbose: bool = False, fix_mode: bool = False):
        self.verbose = verbose
        self.fix_mode = fix_mode
        self.stats = ValidationStats()

    def find_all_dollar_positions(self, content: str) -> List[Tuple[int, bool]]:
        """Find all $ positions with their type (single or double)."""
        positions = []
        i = 0
        while i < len(content):
            if content[i] == '$':
                if i + 1 < len(content) and content[i + 1] == '$':
                    positions.append((i, True))  # Double dollar
                    i += 2
                else:
                    positions.append((i, False))  # Single dollar
                    i += 1
            else:
                i += 1
        return positions

    def check_balanced_delimiters(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for balanced $ and $$ delimiters."""
        issues = []
        positions = self.find_all_dollar_positions(content)

        single_stack = []
        double_stack = []

        for pos, is_double in positions:
            # Skip positions inside script/style tags or template literals
            if self.is_in_script_or_style(content, pos):
                continue
            if self.is_in_template_literal(content, pos):
                continue

            if is_double:
                if double_stack:
                    double_stack.pop()
                else:
                    double_stack.append(pos)
            else:
                if single_stack:
                    single_stack.pop()
                else:
                    single_stack.append(pos)

        # Report unmatched delimiters
        for pos in single_stack:
            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 20):pos + 20]
            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.ERROR,
                code=IssueCodes.UNMATCHED_DOLLAR,
                message="Unmatched single $ delimiter",
                context=context.replace('\n', ' ')
            ))

        for pos in double_stack:
            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 20):pos + 20]
            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.ERROR,
                code=IssueCodes.UNMATCHED_DOLLAR,
                message="Unmatched display $$ delimiter",
                context=context.replace('\n', ' ')
            ))

        return issues

    def pos_to_line_col(self, pos: int, line_offsets: List[int]) -> Tuple[int, int]:
        """Convert character position to line and column."""
        for i, offset in enumerate(line_offsets):
            if offset > pos:
                line = i
                col = pos - line_offsets[i - 1] + 1 if i > 0 else pos + 1
                return line, col
        return len(line_offsets), pos - line_offsets[-1] + 1 if line_offsets else pos + 1

    def get_line_offsets(self, content: str) -> List[int]:
        """Get character offsets for each line start."""
        offsets = [0]
        for i, char in enumerate(content):
            if char == '\n':
                offsets.append(i + 1)
        return offsets

    def is_in_script_or_style(self, content: str, pos: int) -> bool:
        """Check if position is inside a script or style tag."""
        # Find nearest opening and closing tags
        script_open = content.rfind('<script', 0, pos)
        script_close = content.rfind('</script>', 0, pos)
        style_open = content.rfind('<style', 0, pos)
        style_close = content.rfind('</style>', 0, pos)

        in_script = script_open > script_close if script_open != -1 else False
        in_style = style_open > style_close if style_open != -1 else False

        return in_script or in_style

    def is_in_template_literal(self, content: str, pos: int) -> bool:
        """Check if position is inside a JavaScript template literal."""
        # Look for backtick template literals
        backtick_count = 0
        for i in range(pos):
            if content[i] == '`' and (i == 0 or content[i-1] != '\\'):
                backtick_count += 1
        return backtick_count % 2 == 1

    def check_lone_times(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for $\\times$ used alone."""
        issues = []
        for match in LatexPatterns.LONE_TIMES.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue
            if self.is_in_template_literal(content, pos):
                continue

            # Check context - is this truly alone or part of something like "14D$\times$2"
            before = content[max(0, pos - 10):pos]
            after = content[pos + len(match.group()):min(len(content), pos + 20)]

            # If it's between alphanumerics like "14D$\times$2", it's probably intentional inline
            # But should still be in a larger expression like $14D \times 2$
            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 30):pos + 40].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.WARNING,
                code=IssueCodes.LONE_TIMES,
                message="$\\times$ should be part of a larger math expression",
                context=context,
                fix="Consider: $a \\times b$ instead of a$\\times$b"
            ))
        return issues

    def check_superscript_no_base(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for superscripts without a base."""
        issues = []
        for match in LatexPatterns.SUPERSCRIPT_NO_BASE.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue
            if self.is_in_template_literal(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 10):pos + 30].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.WARNING,
                code=IssueCodes.SUPERSCRIPT_NO_BASE,
                message="Superscript ^ without base - may render incorrectly",
                context=context,
                fix="Add base: $x^{...}$ or use ${}^{...}$ for explicit empty base"
            ))
        return issues

    def check_subscript_no_base(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for subscripts without a base."""
        issues = []
        for match in LatexPatterns.SUBSCRIPT_NO_BASE.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue
            if self.is_in_template_literal(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 10):pos + 30].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.WARNING,
                code=IssueCodes.SUBSCRIPT_NO_BASE,
                message="Subscript _ without base - may render incorrectly",
                context=context,
                fix="Add base: $x_{...}$ or use ${}_{...}$ for explicit empty base"
            ))
        return issues

    def check_empty_math(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for empty math expressions."""
        issues = []
        for match in LatexPatterns.EMPTY_MATH.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue
            if self.is_in_template_literal(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 10):pos + 20].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.ERROR,
                code=IssueCodes.EMPTY_MATH,
                message="Empty math expression",
                context=context,
                fix="Remove empty $$ or add content"
            ))
        return issues

    def check_spacing_issues(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for missing spaces around math expressions."""
        issues = []

        # Check for text immediately before math
        for match in LatexPatterns.NO_SPACE_BEFORE.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue
            if self.is_in_template_literal(content, pos):
                continue

            # Skip if inside HTML attributes or common patterns
            before_context = content[max(0, pos - 50):pos + 5]
            if '="' in before_context or "='" in before_context:
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 20):pos + 30].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.INFO,
                code=IssueCodes.NO_SPACE_BEFORE_MATH,
                message="Consider adding space before math expression",
                context=context,
                fix="Add space before $"
            ))

        return issues

    def check_nested_dollars(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for nested dollar signs ($$$ or more)."""
        issues = []
        for match in LatexPatterns.NESTED_DOLLARS.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 10):pos + 30].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.ERROR,
                code=IssueCodes.NESTED_DOLLARS,
                message=f"Invalid nested dollar signs: {match.group()}",
                context=context,
                fix="Use only $ for inline or $$ for display math"
            ))
        return issues

    def check_lone_operators(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for lone operators that should be in larger expressions."""
        issues = []
        for match in LatexPatterns.LONE_OPERATORS.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 20):pos + 30].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.WARNING,
                code=IssueCodes.LONE_OPERATOR,
                message=f"Lone operator {match.group()} - should be part of larger expression",
                context=context,
                fix="Include in larger math expression"
            ))
        return issues

    def check_double_scripts(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for double superscripts/subscripts."""
        issues = []

        for match in LatexPatterns.DOUBLE_SUPERSCRIPT.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 10):pos + 40].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.WARNING,
                code=IssueCodes.DOUBLE_SUPERSCRIPT,
                message="Double superscript - may not render as intended",
                context=context,
                fix="Use x^{a^b} for nested superscripts"
            ))

        for match in LatexPatterns.DOUBLE_SUBSCRIPT.finditer(content):
            pos = match.start()
            if self.is_in_script_or_style(content, pos):
                continue

            line, col = self.pos_to_line_col(pos, line_offsets)
            context = content[max(0, pos - 10):pos + 40].replace('\n', ' ')

            issues.append(LatexIssue(
                file="",
                line=line,
                column=col,
                severity=IssueSeverity.WARNING,
                code=IssueCodes.DOUBLE_SUBSCRIPT,
                message="Double subscript - may not render as intended",
                context=context,
                fix="Use x_{a_b} for nested subscripts"
            ))

        return issues

    def check_unclosed_braces(self, content: str, line_offsets: List[int]) -> List[LatexIssue]:
        """Check for unclosed braces in math expressions."""
        issues = []

        # Find all math expressions
        for pattern in [LatexPatterns.INLINE_MATH, LatexPatterns.DISPLAY_MATH]:
            for match in pattern.finditer(content):
                math_content = match.group(1) if match.lastindex else match.group()
                pos = match.start()

                if self.is_in_script_or_style(content, pos):
                    continue

                # Count braces
                open_braces = math_content.count('{')
                close_braces = math_content.count('}')

                if open_braces != close_braces:
                    line, col = self.pos_to_line_col(pos, line_offsets)
                    context = content[pos:pos + 60].replace('\n', ' ')

                    issues.append(LatexIssue(
                        file="",
                        line=line,
                        column=col,
                        severity=IssueSeverity.ERROR,
                        code=IssueCodes.UNCLOSED_BRACE,
                        message=f"Mismatched braces: {open_braces} open, {close_braces} close",
                        context=context,
                        fix="Balance { and } in math expression"
                    ))

        return issues

    def validate_file(self, file_path: Path) -> List[LatexIssue]:
        """Validate a single HTML file."""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  Warning: Could not read {file_path}: {e}")
            return issues

        line_offsets = self.get_line_offsets(content)

        # Run all checks
        checks = [
            self.check_balanced_delimiters,
            self.check_lone_times,
            self.check_superscript_no_base,
            self.check_subscript_no_base,
            self.check_empty_math,
            self.check_nested_dollars,
            self.check_lone_operators,
            self.check_double_scripts,
            self.check_unclosed_braces,
            # Spacing checks can be noisy, only include in verbose mode
        ]

        if self.verbose:
            checks.append(self.check_spacing_issues)

        for check in checks:
            found_issues = check(content, line_offsets)
            for issue in found_issues:
                issue.file = str(file_path)
            issues.extend(found_issues)

        return issues

    def fix_file(self, file_path: Path, issues: List[LatexIssue]) -> int:
        """Apply automatic fixes to a file."""
        if not issues:
            return 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  Warning: Could not read {file_path} for fixing: {e}")
            return 0

        original_content = content
        fixes_applied = 0

        # Apply fixes for specific issue types
        # Fix lone $\times$ -> merge with adjacent text
        # This is complex and context-dependent, so we'll do simple fixes

        # Fix empty math expressions by removing them
        content = re.sub(r'\$\s*\$', '', content)
        if content != original_content:
            fixes_applied += 1

        # Fix triple+ dollars
        content = re.sub(r'\${3,}', '$$', content)

        if content != original_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixes_applied = sum(1 for i in issues if i.code in [IssueCodes.EMPTY_MATH, IssueCodes.NESTED_DOLLARS])
            except Exception as e:
                print(f"  Warning: Could not write fixes to {file_path}: {e}")
                return 0

        return fixes_applied


def collect_html_files(root: Path, exclude_dirs: Set[str]) -> List[Path]:
    """Collect all HTML files, excluding specified directories."""
    html_files = []

    # Standard directories to check
    dirs_to_scan = [
        root,
        root / 'Pages',
        root / 'foundations',
        root / 'components',
        root / 'sections',
        root / 'examples',
        root / 'docs',
        root / 'diagrams',
    ]

    for scan_dir in dirs_to_scan:
        if not scan_dir.exists():
            continue

        for html_file in scan_dir.glob('*.html'):
            # Check exclusions
            rel_path = html_file.relative_to(root)
            skip = False
            for exclude in exclude_dirs:
                if exclude in str(rel_path):
                    skip = True
                    break
            if not skip:
                html_files.append(html_file)

    return html_files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate LaTeX/MathJax expressions in HTML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Issue Codes:
  LTX001 - Unmatched $ delimiter
  LTX002 - $\\times$ used alone (should be in larger expression)
  LTX003 - Superscript ^ without base
  LTX004 - Subscript _ without base
  LTX005 - No space before math expression
  LTX006 - No space after math expression
  LTX007 - Empty math expression
  LTX008 - Unclosed/mismatched braces
  LTX009 - Nested dollar signs ($$$)
  LTX010 - Invalid escape sequence
  LTX011 - Display math used inline
  LTX012 - Lone operator ($\\pm$, $\\cdot$, etc.)
  LTX013 - Mismatched delimiters
  LTX014 - Double superscript
  LTX015 - Double subscript

Examples:
  python scripts/validate_latex.py
  python scripts/validate_latex.py --fix
  python scripts/validate_latex.py --verbose --file Pages/formulas.html
  python scripts/validate_latex.py --exclude-dirs "node_modules,Demon_Lock"
        """
    )

    parser.add_argument('--fix', action='store_true',
                        help='Attempt to auto-fix common issues')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all issues including minor ones')
    parser.add_argument('--file', '-f', type=str,
                        help='Check a specific file only')
    parser.add_argument('--exclude-dirs', type=str,
                        default='node_modules,Demon_Lock,Principia_Metaphysica_v16',
                        help='Comma-separated directories to exclude')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    parser.add_argument('--summary-only', action='store_true',
                        help='Only show summary, not individual issues')

    args = parser.parse_args()

    project_root = get_project_root()
    exclude_dirs = set(args.exclude_dirs.split(',')) if args.exclude_dirs else set()

    print("=" * 70)
    print(" LATEX/MATHJAX VALIDATION")
    print("=" * 70)
    print(f"Project root: {project_root}")
    print(f"Exclude dirs: {', '.join(exclude_dirs) if exclude_dirs else 'none'}")
    print()

    validator = LatexValidator(verbose=args.verbose, fix_mode=args.fix)

    # Collect files to check
    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = project_root / file_path
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return 1
        html_files = [file_path]
    else:
        html_files = collect_html_files(project_root, exclude_dirs)

    print(f"Scanning {len(html_files)} HTML files...")
    print()

    all_issues: List[LatexIssue] = []
    files_with_issues: Set[str] = set()

    for html_file in html_files:
        issues = validator.validate_file(html_file)
        if issues:
            files_with_issues.add(str(html_file))
            all_issues.extend(issues)

        validator.stats.files_scanned += 1

    # Update stats
    validator.stats.files_with_issues = len(files_with_issues)
    validator.stats.total_issues = len(all_issues)
    validator.stats.errors = sum(1 for i in all_issues if i.severity == IssueSeverity.ERROR)
    validator.stats.warnings = sum(1 for i in all_issues if i.severity == IssueSeverity.WARNING)
    validator.stats.info = sum(1 for i in all_issues if i.severity == IssueSeverity.INFO)

    # Apply fixes if requested
    if args.fix and all_issues:
        print("Applying fixes...")
        for file_path in files_with_issues:
            file_issues = [i for i in all_issues if i.file == file_path]
            fixed = validator.fix_file(Path(file_path), file_issues)
            validator.stats.issues_fixed += fixed

    # Report issues
    if not args.summary_only and all_issues:
        print("=" * 70)
        print(" ISSUES FOUND")
        print("=" * 70)

        # Group by file
        by_file: Dict[str, List[LatexIssue]] = {}
        for issue in all_issues:
            rel_path = os.path.relpath(issue.file, project_root)
            if rel_path not in by_file:
                by_file[rel_path] = []
            by_file[rel_path].append(issue)

        for file_path, issues in sorted(by_file.items()):
            print(f"\n{file_path}:")
            for issue in sorted(issues, key=lambda x: (x.line, x.column)):
                severity_color = {
                    IssueSeverity.ERROR: "\033[91m",  # Red
                    IssueSeverity.WARNING: "\033[93m",  # Yellow
                    IssueSeverity.INFO: "\033[94m"  # Blue
                }
                reset = "\033[0m"

                severity_str = {
                    IssueSeverity.ERROR: "ERROR",
                    IssueSeverity.WARNING: "WARN",
                    IssueSeverity.INFO: "INFO"
                }[issue.severity]

                # Print without colors for Windows compatibility
                # Sanitize context for safe printing (remove non-ASCII chars)
                safe_context = issue.context.encode('ascii', 'replace').decode('ascii')
                print(f"  Line {issue.line}:{issue.column} [{severity_str}] {issue.code}: {issue.message}")
                print(f"    Context: ...{safe_context}...")
                if issue.fix:
                    print(f"    Fix: {issue.fix}")

    # Summary
    print()
    print("=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    print(f"  Files scanned: {validator.stats.files_scanned}")
    print(f"  Files with issues: {validator.stats.files_with_issues}")
    print(f"  Total issues: {validator.stats.total_issues}")
    print(f"    Errors: {validator.stats.errors}")
    print(f"    Warnings: {validator.stats.warnings}")
    print(f"    Info: {validator.stats.info}")
    if args.fix:
        print(f"  Issues fixed: {validator.stats.issues_fixed}")
    print()

    if validator.stats.errors > 0:
        print("=" * 70)
        print(f" VERDICT: {validator.stats.errors} ERRORS FOUND")
        print("=" * 70)
        return 1
    elif validator.stats.warnings > 0:
        print("=" * 70)
        print(f" VERDICT: {validator.stats.warnings} WARNINGS (no errors)")
        print("=" * 70)
        return 0
    else:
        print("=" * 70)
        print(" VERDICT: ALL CHECKS PASSED")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    sys.exit(main())
