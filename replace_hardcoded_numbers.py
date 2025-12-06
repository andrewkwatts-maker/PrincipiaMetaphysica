#!/usr/bin/env python3
"""
replace_hardcoded_numbers.py

Automated replacement of hardcoded numbers in HTML files with proper PM value references.

This script:
1. Loads theory_output.json and extracts all numeric values with their PM paths
2. Scans HTML files for hardcoded numbers (excluding years, DOIs, arXiv IDs, etc.)
3. Matches hardcoded numbers to PM values using fuzzy matching
4. Generates replacement HTML with <span data-category="X" data-param="Y">VALUE</span>
5. Creates diff preview and applies changes with user confirmation
6. Handles formulas, tables, and edge cases intelligently

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import shutil
import math
from bs4 import BeautifulSoup, NavigableString, Tag
from difflib import unified_diff

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('replace_hardcoded_numbers.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class PMValue:
    """Represents a value from theory_output.json with its PM path"""
    category: str
    parameter: str
    value: float
    path: str  # e.g., "PM.proton_decay.M_GUT"
    display: str = ""
    unit: str = ""

    def __post_init__(self):
        """Initialize display representation"""
        if not self.display:
            if abs(self.value) >= 1e4 or (abs(self.value) < 0.01 and self.value != 0):
                self.display = f"{self.value:.3e}"
            else:
                self.display = f"{self.value:.4g}"


@dataclass
class Match:
    """Represents a match between a hardcoded number and a PM value"""
    hardcoded_value: float
    pm_value: PMValue
    match_type: str  # 'exact', 'scientific', 'magnitude', 'rounded'
    confidence: float  # 0-1
    context: str = ""  # Surrounding text for disambiguation

    def __str__(self):
        return (f"Match({self.hardcoded_value} → {self.pm_value.path}, "
                f"type={self.match_type}, conf={self.confidence:.2f})")


@dataclass
class Replacement:
    """Represents a proposed replacement"""
    original_text: str
    replacement_text: str
    match: Match
    file_path: str
    line_number: int = 0
    context_before: str = ""
    context_after: str = ""
    applied: bool = False


@dataclass
class ChangeAudit:
    """Audit trail for all changes"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    replacements: List[Dict[str, Any]] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    statistics: Dict[str, int] = field(default_factory=dict)


class PMValueExtractor:
    """Extracts all numeric values from theory_output.json"""

    def __init__(self, json_path: str):
        self.json_path = json_path
        self.values: List[PMValue] = []

    def load(self) -> List[PMValue]:
        """Load and extract all numeric values from JSON"""
        logger.info(f"Loading theory values from {self.json_path}")

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {self.json_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {self.json_path}: {e}")
            sys.exit(1)

        self.values = []
        self._extract_values(data, "PM")

        logger.info(f"Extracted {len(self.values)} numeric values from theory_output.json")
        return self.values

    def _extract_values(self, obj: Any, path: str):
        """Recursively extract numeric values from nested JSON structure"""
        if isinstance(obj, dict):
            # Check if this is a leaf node with a value
            if 'value' in obj and isinstance(obj.get('value'), (int, float)):
                # Extract the category and parameter from path
                parts = path.split('.')
                if len(parts) >= 3:  # PM.category.parameter
                    category = parts[1]
                    parameter = parts[2]
                    value = obj['value']

                    # Skip NaN values
                    if isinstance(value, float) and math.isnan(value):
                        return

                    pm_value = PMValue(
                        category=category,
                        parameter=parameter,
                        value=float(value),
                        path=path,
                        display=obj.get('display', ''),
                        unit=obj.get('unit', '')
                    )
                    self.values.append(pm_value)

            # Recurse into nested dictionaries
            for key, value in obj.items():
                if key in ['meta', 'sections']:  # Skip metadata sections
                    continue
                self._extract_values(value, f"{path}.{key}")

        elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
            # Direct numeric value
            parts = path.split('.')
            if len(parts) >= 3:
                category = parts[1]
                parameter = parts[-1]

                # Skip NaN
                if isinstance(obj, float) and math.isnan(obj):
                    return

                pm_value = PMValue(
                    category=category,
                    parameter=parameter,
                    value=float(obj),
                    path=path
                )
                self.values.append(pm_value)


class NumberMatcher:
    """Matches hardcoded numbers to PM values using fuzzy matching"""

    # Relative tolerance for floating point comparison
    EXACT_TOLERANCE = 1e-6
    ROUNDED_TOLERANCE = 0.01  # 1% for rounded values
    MAGNITUDE_TOLERANCE = 0.1  # Order of magnitude matching

    def __init__(self, pm_values: List[PMValue]):
        self.pm_values = pm_values
        self.value_index = self._build_index()

    def _build_index(self) -> Dict[int, List[PMValue]]:
        """Build an index of PM values by order of magnitude for fast lookup"""
        index = {}
        for pm_val in self.pm_values:
            if pm_val.value == 0:
                oom = 0
            else:
                oom = int(math.floor(math.log10(abs(pm_val.value))))

            if oom not in index:
                index[oom] = []
            index[oom].append(pm_val)

        return index

    def find_matches(self, number: float, context: str = "") -> List[Match]:
        """Find all possible PM value matches for a given number"""
        matches = []

        # Try exact match
        for pm_val in self.pm_values:
            match = self._try_exact_match(number, pm_val, context)
            if match:
                matches.append(match)

        # Try scientific notation match
        if not matches or matches[0].confidence < 0.99:
            sci_matches = self._try_scientific_match(number, context)
            matches.extend(sci_matches)

        # Try rounded match
        if not matches or matches[0].confidence < 0.95:
            rounded_matches = self._try_rounded_match(number, context)
            matches.extend(rounded_matches)

        # Try order of magnitude match (lower priority)
        if not matches or matches[0].confidence < 0.8:
            magnitude_matches = self._try_magnitude_match(number, context)
            matches.extend(magnitude_matches)

        # Sort by confidence
        matches.sort(key=lambda m: m.confidence, reverse=True)

        return matches

    def _try_exact_match(self, number: float, pm_val: PMValue, context: str) -> Optional[Match]:
        """Try exact match with floating point tolerance"""
        if abs(pm_val.value) < 1e-10:  # Avoid division by zero
            if abs(number) < 1e-10:
                return Match(
                    hardcoded_value=number,
                    pm_value=pm_val,
                    match_type='exact',
                    confidence=1.0,
                    context=context
                )
            return None

        relative_error = abs(number - pm_val.value) / abs(pm_val.value)

        if relative_error < self.EXACT_TOLERANCE:
            return Match(
                hardcoded_value=number,
                pm_value=pm_val,
                match_type='exact',
                confidence=1.0 - relative_error,
                context=context
            )

        return None

    def _try_scientific_match(self, number: float, context: str) -> List[Match]:
        """Match numbers in scientific notation (e.g., 2.118e16 matches 2.1180954...e16)"""
        matches = []

        if number == 0:
            return matches

        # Get order of magnitude
        oom = int(math.floor(math.log10(abs(number))))

        # Check nearby orders of magnitude
        for check_oom in range(oom - 1, oom + 2):
            if check_oom in self.value_index:
                for pm_val in self.value_index[check_oom]:
                    # Check if mantissas match
                    mantissa_num = number / (10 ** oom)
                    mantissa_pm = pm_val.value / (10 ** check_oom)

                    if abs(mantissa_num - mantissa_pm) < 0.1:  # Mantissa tolerance
                        relative_error = abs(number - pm_val.value) / abs(pm_val.value)
                        if relative_error < 0.1:  # 10% tolerance for scientific notation
                            matches.append(Match(
                                hardcoded_value=number,
                                pm_value=pm_val,
                                match_type='scientific',
                                confidence=0.95 - relative_error,
                                context=context
                            ))

        return matches

    def _try_rounded_match(self, number: float, context: str) -> List[Match]:
        """Match rounded versions of numbers (e.g., 12.59 matches 12.5890655)"""
        matches = []

        for pm_val in self.pm_values:
            if abs(pm_val.value) < 1e-10:  # Skip zero values
                continue

            # Try different rounding precisions
            for precision in range(0, 6):
                rounded_pm = round(pm_val.value, precision)
                if abs(number - rounded_pm) < 10 ** (-precision) * 0.5:
                    relative_error = abs(number - pm_val.value) / abs(pm_val.value)
                    if relative_error < self.ROUNDED_TOLERANCE:
                        matches.append(Match(
                            hardcoded_value=number,
                            pm_value=pm_val,
                            match_type='rounded',
                            confidence=0.90 - relative_error - (precision * 0.02),
                            context=context
                        ))
                        break

        return matches

    def _try_magnitude_match(self, number: float, context: str) -> List[Match]:
        """Match by order of magnitude (lowest confidence)"""
        matches = []

        if number == 0:
            return matches

        oom = int(math.floor(math.log10(abs(number))))

        if oom in self.value_index:
            for pm_val in self.value_index[oom]:
                if abs(pm_val.value) < 1e-10:  # Avoid division by zero
                    continue

                relative_error = abs(number - pm_val.value) / abs(pm_val.value)
                if relative_error < self.MAGNITUDE_TOLERANCE:
                    matches.append(Match(
                        hardcoded_value=number,
                        pm_value=pm_val,
                        match_type='magnitude',
                        confidence=0.75 - relative_error,
                        context=context
                    ))

        return matches


class HTMLNumberScanner:
    """Scans HTML files for hardcoded numbers"""

    # Patterns to exclude
    YEAR_PATTERN = re.compile(r'\b(19|20)\d{2}\b')
    DOI_PATTERN = re.compile(r'10\.\d{4,}/[\w\-.]+')
    ARXIV_PATTERN = re.compile(r'\d{4}\.\d{4,5}')
    PAGE_PATTERN = re.compile(r'\b(pp?\.?\s*\d+|\d+\s*-\s*\d+)\b', re.IGNORECASE)

    # Number patterns
    # Matches: integers, decimals, scientific notation, negative numbers
    NUMBER_PATTERN = re.compile(
        r'-?\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?'
    )

    # Tags to skip entirely
    SKIP_TAGS = {'script', 'style', 'code', 'pre'}

    def __init__(self, matcher: NumberMatcher):
        self.matcher = matcher

    def scan_file(self, file_path: str) -> List[Tuple[float, str, Tag]]:
        """Scan HTML file for hardcoded numbers

        Returns:
            List of (number, context, element) tuples
        """
        logger.info(f"Scanning {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return []

        soup = BeautifulSoup(content, 'html.parser')
        found_numbers = []

        # Find all text nodes
        for element in soup.find_all(string=True):
            # Skip if in excluded tag
            if element.parent.name in self.SKIP_TAGS:
                continue

            # Skip if already has PM reference
            if self._has_pm_reference(element):
                continue

            # Extract numbers from text
            text = str(element)
            for match in self.NUMBER_PATTERN.finditer(text):
                number_str = match.group()

                # Parse number
                try:
                    number = float(number_str)
                except ValueError:
                    continue

                # Apply exclusion rules
                if self._should_exclude(number, text):
                    continue

                # Get context
                context = self._get_context(element, match.start(), match.end())

                found_numbers.append((number, context, element))

        logger.info(f"Found {len(found_numbers)} potential numbers in {file_path}")
        return found_numbers

    def _has_pm_reference(self, element) -> bool:
        """Check if element or its parent already has PM reference"""
        # Check parent chain for data-category attribute
        current = element.parent
        depth = 0
        while current and depth < 5:
            if hasattr(current, 'get') and current.get('data-category'):
                return True
            current = current.parent
            depth += 1

        return False

    def _should_exclude(self, number: float, text: str) -> bool:
        """Check if number should be excluded from replacement"""
        # Skip small integers (likely not physics values)
        if number == int(number) and -10 < number < 10:
            return True

        # Skip years
        if 1900 <= number <= 2100:
            return True

        # Check for DOI
        if self.DOI_PATTERN.search(text):
            return True

        # Check for arXiv ID
        if self.ARXIV_PATTERN.search(text):
            return True

        # Check for page numbers
        if self.PAGE_PATTERN.search(text):
            return True

        return False

    def _get_context(self, element, start: int, end: int, window: int = 50) -> str:
        """Get surrounding context for a number"""
        text = str(element)
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end]


class HTMLReplacer:
    """Handles HTML replacement with proper structure"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.replacements: List[Replacement] = []

    def propose_replacement(self, file_path: str, number: float,
                          matches: List[Match], element) -> Optional[Replacement]:
        """Propose a replacement for a hardcoded number"""
        if not matches:
            return None

        # Use best match (highest confidence)
        best_match = matches[0]

        # Generate replacement HTML
        original_text = str(number)
        replacement_text = self._generate_span(best_match.pm_value, number)

        # Get context
        parent_text = element.parent.get_text() if element.parent else ""

        replacement = Replacement(
            original_text=original_text,
            replacement_text=replacement_text,
            match=best_match,
            file_path=file_path,
            context_before=parent_text[:100],
            context_after=parent_text[-100:]
        )

        self.replacements.append(replacement)
        return replacement

    def _generate_span(self, pm_value: PMValue, original_number: float) -> str:
        """Generate replacement span HTML"""
        # Determine display format
        if abs(original_number - int(original_number)) < 1e-10:
            # Integer display
            data_format = "display"
        elif abs(original_number) >= 1e4 or (abs(original_number) < 0.01 and original_number != 0):
            # Scientific notation
            data_format = "display"
        else:
            # Fixed decimal - count decimal places in original
            decimal_places = len(str(original_number).split('.')[-1]) if '.' in str(original_number) else 0
            data_format = f"fixed:{min(decimal_places, 4)}"

        span = (f'<span class="pm-value" '
                f'data-category="{pm_value.category}" '
                f'data-param="{pm_value.parameter}" '
                f'data-format="{data_format}">'
                f'</span>')

        return span

    def apply_replacements(self, file_path: str, auto_apply: bool = False) -> bool:
        """Apply all replacements to a file"""
        file_replacements = [r for r in self.replacements if r.file_path == file_path]

        if not file_replacements:
            return True

        logger.info(f"Applying {len(file_replacements)} replacements to {file_path}")

        # Create backup
        if not self.dry_run:
            backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(file_path, backup_path)
            logger.info(f"Created backup: {backup_path}")

        # Load file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return False

        # Apply replacements
        changes_made = 0
        for replacement in file_replacements:
            if self._apply_single_replacement(soup, replacement):
                replacement.applied = True
                changes_made += 1

        # Write back
        if not self.dry_run and changes_made > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup.prettify()))
                logger.info(f"Applied {changes_made} changes to {file_path}")
            except Exception as e:
                logger.error(f"Error writing {file_path}: {e}")
                return False

        return True

    def _apply_single_replacement(self, soup: BeautifulSoup, replacement: Replacement) -> bool:
        """Apply a single replacement to the soup"""
        # This is a simplified version - in production you'd need more sophisticated
        # text node finding and replacement
        # For now, we'll use string replacement with context checking

        # Find all text nodes containing the number
        for element in soup.find_all(string=True):
            text = str(element)
            if replacement.original_text in text:
                # Replace the text
                new_text = text.replace(
                    replacement.original_text,
                    replacement.replacement_text,
                    1  # Replace only first occurrence
                )
                element.replace_with(BeautifulSoup(new_text, 'html.parser'))
                return True

        return False


class DiffGenerator:
    """Generates diff previews of changes"""

    @staticmethod
    def generate_diff(file_path: str, replacements: List[Replacement]) -> str:
        """Generate unified diff for a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
        except Exception as e:
            logger.error(f"Error reading {file_path} for diff: {e}")
            return ""

        # Create modified version
        modified_text = ''.join(original_lines)
        for replacement in replacements:
            modified_text = modified_text.replace(
                replacement.original_text,
                replacement.replacement_text,
                1
            )

        modified_lines = modified_text.splitlines(keepends=True)

        # Generate diff
        diff = unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"{file_path} (original)",
            tofile=f"{file_path} (modified)",
            lineterm=''
        )

        return '\n'.join(diff)

    @staticmethod
    def print_summary(replacements: List[Replacement]):
        """Print summary of proposed replacements"""
        print("\n" + "="*80)
        print("REPLACEMENT SUMMARY")
        print("="*80)

        # Group by file
        files = {}
        for r in replacements:
            if r.file_path not in files:
                files[r.file_path] = []
            files[r.file_path].append(r)

        for file_path, file_replacements in files.items():
            print(f"\n{file_path}: {len(file_replacements)} replacements")
            for i, r in enumerate(file_replacements[:10], 1):  # Show first 10
                print(f"  {i}. {r.original_text} -> {r.match.pm_value.path}")
                print(f"     Type: {r.match.match_type}, Confidence: {r.match.confidence:.2f}")

            if len(file_replacements) > 10:
                print(f"  ... and {len(file_replacements) - 10} more")

        print("\n" + "="*80)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Replace hardcoded numbers in HTML with PM value references',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview only)
  python replace_hardcoded_numbers.py --dry-run

  # Apply changes with confirmation
  python replace_hardcoded_numbers.py --files index.html paper.html

  # Auto-apply all changes
  python replace_hardcoded_numbers.py --auto-apply --all-html

  # Generate report only
  python replace_hardcoded_numbers.py --dry-run --report report.json
        """
    )

    parser.add_argument(
        '--json',
        default='theory_output.json',
        help='Path to theory_output.json (default: theory_output.json)'
    )

    parser.add_argument(
        '--files',
        nargs='+',
        help='HTML files to process'
    )

    parser.add_argument(
        '--all-html',
        action='store_true',
        help='Process all HTML files in current directory'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Preview changes without applying (default: True)'
    )

    parser.add_argument(
        '--auto-apply',
        action='store_true',
        help='Automatically apply changes without confirmation'
    )

    parser.add_argument(
        '--report',
        help='Output report to JSON file'
    )

    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.85,
        help='Minimum confidence threshold (0-1, default: 0.85)'
    )

    parser.add_argument(
        '--show-diff',
        action='store_true',
        help='Show unified diff of changes'
    )

    args = parser.parse_args()

    # Determine files to process
    if args.all_html:
        html_files = list(Path('.').glob('*.html'))
    elif args.files:
        html_files = [Path(f) for f in args.files]
    else:
        print("Error: Specify --files or --all-html")
        parser.print_help()
        sys.exit(1)

    # Load PM values
    extractor = PMValueExtractor(args.json)
    pm_values = extractor.load()

    # Initialize matcher
    matcher = NumberMatcher(pm_values)

    # Initialize scanner
    scanner = HTMLNumberScanner(matcher)

    # Initialize replacer
    dry_run = args.dry_run and not args.auto_apply
    replacer = HTMLReplacer(dry_run=dry_run)

    # Process each file
    all_replacements = []

    for html_file in html_files:
        if not html_file.exists():
            logger.warning(f"File not found: {html_file}")
            continue

        # Scan for numbers
        numbers = scanner.scan_file(str(html_file))

        # Find matches
        for number, context, element in numbers:
            matches = matcher.find_matches(number, context)

            # Filter by confidence
            matches = [m for m in matches if m.confidence >= args.min_confidence]

            if matches:
                replacement = replacer.propose_replacement(
                    str(html_file), number, matches, element
                )
                if replacement:
                    all_replacements.append(replacement)

    # Print summary
    DiffGenerator.print_summary(all_replacements)

    # Show diffs
    if args.show_diff:
        print("\n" + "="*80)
        print("UNIFIED DIFFS")
        print("="*80)
        files_to_diff = set(r.file_path for r in all_replacements)
        for file_path in files_to_diff:
            file_replacements = [r for r in all_replacements if r.file_path == file_path]
            diff = DiffGenerator.generate_diff(file_path, file_replacements)
            print(f"\n{diff}")

    # Apply changes
    if not dry_run:
        if args.auto_apply:
            apply = True
        else:
            response = input("\nApply these changes? (yes/no): ")
            apply = response.lower() in ['yes', 'y']

        if apply:
            files_to_process = set(r.file_path for r in all_replacements)
            for file_path in files_to_process:
                replacer.apply_replacements(file_path, auto_apply=args.auto_apply)

            logger.info("All changes applied successfully")
        else:
            logger.info("Changes cancelled by user")
    else:
        logger.info("Dry run complete - no changes applied")

    # Generate report
    if args.report:
        audit = ChangeAudit()
        audit.replacements = [
            {
                'file': r.file_path,
                'original': r.original_text,
                'replacement': r.replacement_text,
                'pm_path': r.match.pm_value.path,
                'match_type': r.match.match_type,
                'confidence': r.match.confidence,
                'applied': r.applied
            }
            for r in all_replacements
        ]
        audit.files_modified = list(set(r.file_path for r in all_replacements if r.applied))
        audit.statistics = {
            'total_replacements': len(all_replacements),
            'applied': sum(1 for r in all_replacements if r.applied),
            'files_scanned': len(html_files),
            'files_modified': len(audit.files_modified)
        }

        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(audit.__dict__, f, indent=2, default=str)

        logger.info(f"Report saved to {args.report}")

    # Print statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Files scanned: {len(html_files)}")
    print(f"Total replacements proposed: {len(all_replacements)}")
    if not dry_run:
        print(f"Replacements applied: {sum(1 for r in all_replacements if r.applied)}")
    print("="*80)


if __name__ == '__main__':
    main()
