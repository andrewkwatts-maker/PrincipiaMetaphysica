#!/usr/bin/env python3
"""
Cleanup script for v12.1 - Remove obsolete files

Removes old documentation, utility scripts, and temporary files
that are no longer needed after v12.0 completion.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import os
from pathlib import Path

# Files to remove (obsolete documentation and utilities)
OBSOLETE_MD_FILES = [
    # Agent reports (keep only comprehensive summary in reports/)
    "AGENT_3_SUMMARY.md",
    "AGENT_C_README.md",
    "AGENT_C_REPORT.md",
    "AGENT_C_SUMMARY.md",
    "AGENT_D_FIX_REPORT.md",
    "AGENT_E_REPORT.md",
    "AGENT_F_COMPLETION_REPORT.md",
    "AGENT_F_SUMMARY.md",

    # Old version summaries (superseded by V12_COMPLETION_SUMMARY.md)
    "V7_ISSUES_REPORT.md",
    "V7_PUBLICATION_SUMMARY.md",
    "V8_1_IMPROVEMENT_SUMMARY.md",
    "V8_2_IMPROVEMENT_SUMMARY.md",
    "V8_4_BREAKTHROUGH_SUMMARY.md",
    "V8_4_FINAL_INTEGRATION_SUMMARY.md",
    "V8_4_IMPLEMENTATION_COMPLETE.md",
    "V8_IMPLEMENTATION_SUMMARY.md",
    "V8_SIMULATION_VALIDATION_REPORT.md",
    "V9_TO_V12_SIMULATION_IMPLEMENTATION.md",

    # Migration/implementation process docs (complete, no longer needed)
    "CENTRALIZATION_ACTION_PLAN.md",
    "CENTRALIZATION_COMPLETION_REPORT.md",
    "CENTRALIZATION_PROGRESS_REPORT.md",
    "CENTRALIZATION_VALIDATION_REPORT.md",
    "COMPLETE_MIGRATION_FINAL_SUMMARY.md",
    "MIGRATION_COMPLETE_SUMMARY.md",
    "MISSION_ACCOMPLISHED.md",
    "SECTIONS_CONTENT_UPDATE_SUMMARY.md",

    # Build/fix process docs (completed)
    "BROKEN_LINKS_SOLUTION.md",
    "FIX_BROKEN_LINKS_README.md",
    "REPLACE_HARDCODED_NUMBERS_README.md",
    "REPLACE_NUMBERS_QUICKSTART.md",
    "REPLACE_NUMBERS_SUMMARY.md",
    "CLEANUP_SUMMARY.md",
    "FINAL_POLISH_REPORT.md",

    # Audit reports (completed, issues resolved)
    "PM_VALUES_AUDIT.md",
    "FORMULA_AUDIT_INDEX.md",
    "FORMULA_AUDIT_REPORT.md",
    "FORMULA_CENTRALIZATION_SUMMARY.md",
    "FORMULA_DATABASE_EXECUTIVE_SUMMARY.md",
    "FORMULA_PRIORITY_TABLE.md",
    "ORPHANED_BLOCKS_DETAILED.md",
    "OUTSTANDING_WORK_ASSESSMENT.md",
    "DIAGRAM_FORMULA_AUDIT_V12.md",

    # Integration reports (completed)
    "ACKNOWLEDGMENTS_ADDED.md",
    "BEGINNERS_GUIDE_V12_UPDATE.md",
    "CALABI_YAU_INTEGRATION_REPORT.md",
    "CONFIG_V12_UPDATES.md",
    "FOUNDATIONAL_ATTRIBUTION.md",
    "HARDCODED_NUMBERS_AGENT4.md",
    "IMPLEMENTATION_GUIDE.md",
    "MARKETING_LANGUAGE_REMOVAL.md",
    "PAPER_A4_FORMATTING.md",
    "PAPER_V12_UPDATE.md",
    "PHD_REVIEW_EXPERIMENTAL.md",
    "PHD_REVIEW_MATHEMATICS.md",
    "PHD_REVIEW_PHYSICS.md",
    "PROTON_DECAY_ANALYSIS.md",
    "SECTION_POLISH_V12.md",
    "SECTIONS_CONTENT_V12_UPDATE.md",
    "SIMULATION_FILES_INVENTORY.md",
    "SIMULATION_RUNNER_V12_FINAL.md",
    "WEBSITE_V12_POLISH.md",
    "XY_BOSONS_SPEC.md",
]

OBSOLETE_PY_FILES = [
    # Audit/validation scripts (completed tasks)
    "analyze_orphaned_formulas.py",
    "apply_equation_fixes.py",
    "assess_formula_relevance.py",
    "audit_formulas.py",
    "audit_predictions_page.py",
    "check_broken_links.py",
    "check_missing_constants.py",
    "check_topic_implementation.py",
    "extract_equations.py",
    "extract_paper_sections.py",
    "final_audit_summary.py",

    # Fix scripts (tasks completed)
    "fix_all_equation_labels.py",
    "fix_all_equation_labels_final.py",
    "fix_all_equation_labels_v2.py",
    "fix_broken_links.py",
    "fix_cross_references.py",
    "fix_cross_refs_simple.py",
    "fix_diagrams_v12.py",
    "fix_remaining_equations.py",
    "fix_unicode.py",

    # Utility scripts (tasks completed)
    "remove_consciousness_from_paper.py",
    "remove_marketing_language.py",
    "replace_hardcoded_numbers.py",
    "replace_orphaned_formulas.py",
    "show_broken_link_analysis.py",
    "update_acknowledgments.py",
    "update_pending_peer_review.py",

    # Old validation scripts (superseded)
    "validate_agent_f_work.py",
    "validate_magic_numbers.py",
    "validate_topic_implementation.py",

    # Malformed filenames
    "h:GithubPrincipiaMetaphysicaaudit_config_conflicts.py",
    "h:GithubPrincipiaMetaphysicaaudit_formulas.py",
    "PAPER_SECTIONS_EXTRACT.py",

    # Old simulation runners (superseded by run_all_simulations.py)
    "run_all_v9_to_v12_simulations.py",
    "test_v8_simulations.py",
]

# Keep these essential files
KEEP_MD_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "CONFIG_README.md",
    "BUILD_README.md",
    "SimulateTheory_README.md",
    "ENHANCED_CONSTANTS_README.md",
    "SINGLE_SOURCE_OF_TRUTH.md",
    "V12_COMPLETION_SUMMARY.md",
    "V12_IMPLEMENTATION_SUMMARY.md",
    "VALIDATION_COMPLETE.md",
    "ROOT_STRUCTURE.md",
    "SOURCE_OF_TRUTH_VALIDATION.md",
    "CENTRALIZED_CONTENT_SYSTEM_README.md",
]

KEEP_PY_FILES = [
    "config.py",
    "run_all_simulations.py",
    "generate_enhanced_constants.py",
    "validate_pm_values.py",
    "validate_v12_consistency.py",
    "validate_centralization.py",
    "validate_source_of_truth.py",
    "formula_definitions.py",
    "sections_content.py",
]

def cleanup_files(file_list, file_type="file"):
    """Remove files from list if they exist"""
    removed = []
    skipped = []

    for filename in file_list:
        filepath = Path(filename)
        if filepath.exists():
            try:
                os.remove(filepath)
                removed.append(filename)
                print(f"[OK] Removed: {filename}")
            except Exception as e:
                print(f"[ERROR] Removing {filename}: {e}")
                skipped.append(filename)
        else:
            skipped.append(filename)

    return removed, skipped

def main():
    print("=" * 80)
    print("Principia Metaphysica v12.1 - File Cleanup")
    print("=" * 80)
    print()

    # Cleanup MD files
    print("Cleaning up obsolete documentation files...")
    print("-" * 80)
    removed_md, skipped_md = cleanup_files(OBSOLETE_MD_FILES, "MD")
    print(f"\nRemoved {len(removed_md)} MD files, {len(skipped_md)} not found")

    print()

    # Cleanup PY files
    print("Cleaning up obsolete Python utility scripts...")
    print("-" * 80)
    removed_py, skipped_py = cleanup_files(OBSOLETE_PY_FILES, "PY")
    print(f"\nRemoved {len(removed_py)} PY files, {len(skipped_py)} not found")

    print()
    print("=" * 80)
    print(f"Cleanup Complete")
    print(f"Total removed: {len(removed_md) + len(removed_py)} files")
    print("=" * 80)
    print()
    print("Essential files preserved:")
    print(f"  - {len(KEEP_MD_FILES)} documentation files")
    print(f"  - {len(KEEP_PY_FILES)} Python scripts")
    print()

if __name__ == "__main__":
    main()
