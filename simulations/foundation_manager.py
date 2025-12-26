"""
Foundation Manager - Utility for managing foundations in theory_output.json

This script provides command-line tools for:
- Listing foundations
- Validating foundations
- Adding new foundations
- Exporting foundations to various formats
- Generating reports
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional

from foundation_schema import (
    FoundationEntry,
    FormulaEntry,
    load_foundations_from_theory_output,
    save_foundations_to_theory_output,
    get_foundations_by_category,
    get_foundation_by_id,
    validate_all_foundations,
    generate_html_template,
    generate_json_template,
    VALID_CATEGORIES,
    VALID_BADGE_TYPES,
    create_example_foundation,
)


class FoundationManager:
    """Manager class for foundation operations."""

    def __init__(self, theory_output_path: str):
        """
        Initialize the foundation manager.

        Args:
            theory_output_path: Path to theory_output.json
        """
        self.theory_output_path = Path(theory_output_path)
        self.foundations: List[FoundationEntry] = []

    def load(self) -> bool:
        """
        Load foundations from theory_output.json.

        Returns:
            True if successful, False otherwise
        """
        if not self.theory_output_path.exists():
            print(f"Warning: {self.theory_output_path} does not exist")
            return False

        try:
            self.foundations = load_foundations_from_theory_output(str(self.theory_output_path))
            print(f"Loaded {len(self.foundations)} foundations from {self.theory_output_path}")
            return True
        except Exception as e:
            print(f"Error loading foundations: {e}")
            return False

    def save(self) -> bool:
        """
        Save foundations to theory_output.json.

        Returns:
            True if successful, False otherwise
        """
        try:
            success = save_foundations_to_theory_output(
                self.foundations,
                str(self.theory_output_path),
                merge=True
            )
            if success:
                print(f"Saved {len(self.foundations)} foundations to {self.theory_output_path}")
            return success
        except Exception as e:
            print(f"Error saving foundations: {e}")
            return False

    def list_foundations(self, category: Optional[str] = None) -> None:
        """
        List all foundations (optionally filtered by category).

        Args:
            category: Optional category filter
        """
        foundations = self.foundations
        if category:
            foundations = get_foundations_by_category(foundations, category)

        if not foundations:
            print("No foundations found.")
            return

        print(f"\n{'=' * 80}")
        print(f"Foundations ({len(foundations)})")
        if category:
            print(f"Category: {category}")
        print(f"{'=' * 80}\n")

        for i, foundation in enumerate(foundations, 1):
            print(f"{i}. [{foundation.id}] {foundation.title}")
            print(f"   Category: {foundation.category} | Year: {foundation.year_established} | Badge: {foundation.badge_type}")
            print(f"   Formulas: {len(foundation.formulas)} | Tags: {', '.join(foundation.tags) if foundation.tags else 'none'}")
            print()

    def show_foundation(self, foundation_id: str) -> None:
        """
        Display detailed information about a specific foundation.

        Args:
            foundation_id: ID of the foundation to display
        """
        foundation = get_foundation_by_id(self.foundations, foundation_id)

        if not foundation:
            print(f"Foundation '{foundation_id}' not found.")
            return

        print(f"\n{'=' * 80}")
        print(f"Foundation: {foundation.title}")
        print(f"{'=' * 80}\n")

        print(f"ID: {foundation.id}")
        print(f"Category: {foundation.category}")
        print(f"Year Established: {foundation.year_established}")
        print(f"Badge Type: {foundation.badge_type}")
        print()

        print("Main Equation:")
        print(f"  {foundation.main_equation}")
        if foundation.main_equation_latex:
            print(f"  LaTeX: {foundation.main_equation_latex}")
        print()

        print("Summary:")
        print(f"  {foundation.summary}")
        print()

        print("Key Properties:")
        for i, prop in enumerate(foundation.key_properties, 1):
            print(f"  {i}. {prop}")
        print()

        print("PM Connection:")
        print(f"  {foundation.pm_connection}")
        print()

        if foundation.formulas:
            print(f"Formulas ({len(foundation.formulas)}):")
            for i, formula in enumerate(foundation.formulas, 1):
                print(f"  {i}. [{formula.id}] {formula.label}")
                print(f"     {formula.plain_text}")
                if formula.description:
                    print(f"     {formula.description}")
            print()

        if foundation.references:
            print(f"References ({len(foundation.references)}):")
            for i, ref in enumerate(foundation.references, 1):
                print(f"  {i}. {ref}")
            print()

        if foundation.tags:
            print(f"Tags: {', '.join(foundation.tags)}")
            print()

    def validate(self) -> None:
        """Validate all foundations and display report."""
        report = validate_all_foundations(self.foundations)

        print(f"\n{'=' * 80}")
        print("Validation Report")
        print(f"{'=' * 80}\n")

        print(f"Total Foundations: {report['total']}")
        print(f"Valid: {report['valid']}")
        print(f"Invalid: {report['invalid']}")
        print()

        if report['errors']:
            print("Validation Errors:")
            print("-" * 80)
            for error_info in report['errors']:
                print(f"\n[{error_info['id']}] {error_info['title']}")
                for error in error_info['errors']:
                    print(f"  - {error}")
            print()
        else:
            print("All foundations passed validation!")

    def export_html(self, output_dir: str) -> None:
        """
        Export foundations to HTML files.

        Args:
            output_dir: Directory to write HTML files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for foundation in self.foundations:
            html = generate_html_template(foundation)
            file_path = output_path / f"{foundation.id}.html"

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"Exported: {file_path}")

        print(f"\nExported {len(self.foundations)} foundations to {output_dir}")

    def export_json(self, output_file: str) -> None:
        """
        Export foundations to a JSON file.

        Args:
            output_file: Path to output JSON file
        """
        data = [f.to_dict() for f in self.foundations]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Exported {len(self.foundations)} foundations to {output_file}")

    def generate_report(self) -> None:
        """Generate a summary report of all foundations."""
        print(f"\n{'=' * 80}")
        print("Foundation Summary Report")
        print(f"{'=' * 80}\n")

        print(f"Total Foundations: {len(self.foundations)}")
        print()

        # Category breakdown
        print("By Category:")
        category_counts = {}
        for foundation in self.foundations:
            category_counts[foundation.category] = category_counts.get(foundation.category, 0) + 1

        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}")
        print()

        # Badge type breakdown
        print("By Badge Type:")
        badge_counts = {}
        for foundation in self.foundations:
            badge_counts[foundation.badge_type] = badge_counts.get(foundation.badge_type, 0) + 1

        for badge, count in sorted(badge_counts.items()):
            print(f"  {badge}: {count}")
        print()

        # Time period breakdown
        print("By Time Period:")
        periods = {
            "Pre-1900": 0,
            "1900-1950": 0,
            "1950-2000": 0,
            "Post-2000": 0
        }
        for foundation in self.foundations:
            year = foundation.year_established
            if year < 1900:
                periods["Pre-1900"] += 1
            elif year < 1950:
                periods["1900-1950"] += 1
            elif year < 2000:
                periods["1950-2000"] += 1
            else:
                periods["Post-2000"] += 1

        for period, count in periods.items():
            print(f"  {period}: {count}")
        print()

        # Formula statistics
        total_formulas = sum(len(f.formulas) for f in self.foundations)
        avg_formulas = total_formulas / len(self.foundations) if self.foundations else 0
        print(f"Total Formulas: {total_formulas}")
        print(f"Average Formulas per Foundation: {avg_formulas:.1f}")
        print()

    def add_example(self) -> None:
        """Add the example foundation to the collection."""
        example = create_example_foundation()

        # Check if it already exists
        existing = get_foundation_by_id(self.foundations, example.id)
        if existing:
            print(f"Foundation '{example.id}' already exists. Skipping.")
            return

        self.foundations.append(example)
        print(f"Added example foundation: {example.title}")


def main():
    """Main entry point for the foundation manager CLI."""
    parser = argparse.ArgumentParser(
        description="Foundation Manager - Manage theoretical foundations in theory_output.json"
    )

    parser.add_argument(
        '--theory-output',
        default='theory_output.json',
        help='Path to theory_output.json (default: theory_output.json)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List foundations')
    list_parser.add_argument(
        '--category',
        choices=list(VALID_CATEGORIES),
        help='Filter by category'
    )

    # Show command
    show_parser = subparsers.add_parser('show', help='Show foundation details')
    show_parser.add_argument('id', help='Foundation ID')

    # Validate command
    subparsers.add_parser('validate', help='Validate all foundations')

    # Report command
    subparsers.add_parser('report', help='Generate summary report')

    # Export HTML command
    export_html_parser = subparsers.add_parser('export-html', help='Export foundations to HTML')
    export_html_parser.add_argument(
        '--output-dir',
        default='output/foundations',
        help='Output directory for HTML files (default: output/foundations)'
    )

    # Export JSON command
    export_json_parser = subparsers.add_parser('export-json', help='Export foundations to JSON')
    export_json_parser.add_argument(
        '--output-file',
        default='foundations_export.json',
        help='Output JSON file (default: foundations_export.json)'
    )

    # Add example command
    subparsers.add_parser('add-example', help='Add example foundation')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize manager
    manager = FoundationManager(args.theory_output)

    # Load foundations (except for add-example which creates new)
    if args.command != 'add-example':
        if not manager.load():
            print("Failed to load foundations.")
            sys.exit(1)

    # Execute command
    try:
        if args.command == 'list':
            manager.list_foundations(category=args.category)

        elif args.command == 'show':
            manager.show_foundation(args.id)

        elif args.command == 'validate':
            manager.validate()

        elif args.command == 'report':
            manager.generate_report()

        elif args.command == 'export-html':
            manager.export_html(args.output_dir)

        elif args.command == 'export-json':
            manager.export_json(args.output_file)

        elif args.command == 'add-example':
            manager.load()  # Load existing first
            manager.add_example()
            manager.save()

    except Exception as e:
        print(f"Error executing command: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
