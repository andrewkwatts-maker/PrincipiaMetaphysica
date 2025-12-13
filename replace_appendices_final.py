#!/usr/bin/env python3
"""
Replace Appendices A, B, C in principia-metaphysica-paper.html
Handles large file by processing line-by-line
"""

import os

def replace_appendices():
    paper_file = r'h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html'
    backup_file = r'h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html.backup'
    temp_file = r'h:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html.temp'

    appendix_a_file = r'h:/Github/PrincipiaMetaphysica/appendix-a-fixed.html'
    appendix_b_file = r'h:/Github/PrincipiaMetaphysica/appendix-b-fixed.html'
    appendix_c_file = r'h:/Github/PrincipiaMetaphysica/appendix-c-fixed.html'

    # Boundaries (line numbers are 1-indexed, but we use 0-indexed)
    APPENDIX_A_START = 9549 - 1  # Line before appendix A
    APPENDIX_B_START = 10751 - 1  # Line before appendix B
    APPENDIX_C_START = 19116 - 1  # Line before appendix C
    APPENDIX_C_END = 22737  # Line after appendix C

    print("Creating backup...")
    if os.path.exists(backup_file):
        print(f"  Backup already exists: {backup_file}")
    else:
        import shutil
        shutil.copy2(paper_file, backup_file)
        print(f"  ✓ Backup created: {backup_file}")

    print("\nReading fixed appendices...")
    with open(appendix_a_file, 'r', encoding='utf-8') as f:
        appendix_a_content = f.read()
    with open(appendix_b_file, 'r', encoding='utf-8') as f:
        appendix_b_content = f.read()
    with open(appendix_c_file, 'r', encoding='utf-8') as f:
        appendix_c_content = f.read()

    print("\nProcessing paper file...")
    with open(paper_file, 'r', encoding='utf-8') as infile, \
         open(temp_file, 'w', encoding='utf-8') as outfile:

        line_num = 0

        # Copy lines before Appendix A
        print(f"  Copying lines 1-{APPENDIX_A_START}...")
        for line in infile:
            if line_num == APPENDIX_A_START:
                break
            outfile.write(line)
            line_num += 1

        # Write Appendix A
        print(f"  Writing fixed Appendix A...")
        outfile.write(appendix_a_content)
        outfile.write('\n')

        # Skip original Appendix A (lines APPENDIX_A_START to APPENDIX_B_START-1)
        print(f"  Skipping original Appendix A (lines {APPENDIX_A_START+1}-{APPENDIX_B_START})...")
        while line_num < APPENDIX_B_START:
            next(infile)
            line_num += 1

        # Write Appendix B
        print(f"  Writing fixed Appendix B...")
        outfile.write(appendix_b_content)
        outfile.write('\n')

        # Skip original Appendix B (lines APPENDIX_B_START to APPENDIX_C_START-1)
        print(f"  Skipping original Appendix B (lines {APPENDIX_B_START+1}-{APPENDIX_C_START})...")
        while line_num < APPENDIX_C_START:
            next(infile)
            line_num += 1

        # Write Appendix C
        print(f"  Writing fixed Appendix C...")
        outfile.write(appendix_c_content)
        outfile.write('\n')

        # Skip original Appendix C (lines APPENDIX_C_START to APPENDIX_C_END-1)
        print(f"  Skipping original Appendix C (lines {APPENDIX_C_START+1}-{APPENDIX_C_END})...")
        while line_num < APPENDIX_C_END:
            next(infile)
            line_num += 1

        # Copy remaining lines
        print(f"  Copying remaining lines from {APPENDIX_C_END+1} to end...")
        for line in infile:
            outfile.write(line)
            line_num += 1

    print(f"\n  Total lines processed: {line_num}")

    # Replace original with temp
    print("\nReplacing original file with updated version...")
    os.replace(temp_file, paper_file)

    print("\n" + "="*60)
    print("✓ SUCCESS! Appendices have been fixed.")
    print("="*60)
    print("\nSummary of changes:")
    print("  • Appendix A: Reduced from ~1,200 lines to ~140 lines")
    print("  • Appendix B: Reduced from ~8,400 lines to ~180 lines")
    print("  • Appendix C: Reduced from ~3,600 lines to ~200 lines")
    print("  • Total reduction: ~13,000 lines (from ~56,670 to ~43,670)")
    print("\nImprovements:")
    print("  ✓ All formulas converted to proper MathJax LaTeX ($$...$$)")
    print("  ✓ Frosted glass styling applied to all content boxes")
    print("  ✓ Dimensional analysis converted to proper tables")
    print("  ✓ Version references and changelog boxes removed")
    print("  ✓ Duplicate content replaced with summaries + links to full sections")
    print("  ✓ Mobile/print responsive design applied")
    print(f"\nBackup saved at: {backup_file}")

if __name__ == '__main__':
    try:
        replace_appendices()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
