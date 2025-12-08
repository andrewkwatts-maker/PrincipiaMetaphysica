#!/usr/bin/env python3
"""
Convert ALL remaining <sup> and <sub> tags to Unicode throughout the paper.
This handles inline text, paragraphs, tables, etc.
"""

import re
from pathlib import Path

def convert_sup_sub_to_unicode(text):
    """Convert <sup> and <sub> HTML tags to Unicode superscripts/subscripts."""

    # Superscript mappings
    sup_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', 'i': 'ⁱ',
        'A': 'ᴬ', 'B': 'ᴮ', 'D': 'ᴰ', 'E': 'ᴱ', 'G': 'ᴳ',
        'H': 'ᴴ', 'I': 'ᴵ', 'J': 'ᴶ', 'K': 'ᴷ', 'L': 'ᴸ',
        'M': 'ᴹ', 'N': 'ᴺ', 'O': 'ᴼ', 'P': 'ᴾ', 'R': 'ᴿ',
        'T': 'ᵀ', 'U': 'ᵁ', 'V': 'ⱽ', 'W': 'ᵂ',
    }

    # Subscript mappings
    sub_map = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ', 'h': 'ₕ',
        'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'p': 'ₚ',
        's': 'ₛ', 't': 'ₜ', 'r': 'ᵣ', 'v': 'ᵥ', 'i': 'ᵢ', 'j': 'ⱼ', 'u': 'ᵤ',
    }

    # Convert superscripts
    def replace_sup(match):
        content = match.group(1).strip()
        result = ''
        for char in content:
            result += sup_map.get(char, char)
        return result

    # Convert subscripts
    def replace_sub(match):
        content = match.group(1).strip()
        result = ''
        for char in content:
            result += sub_map.get(char, char)
        return result

    # Replace <sup>...</sup> (handle multi-line)
    text = re.sub(r'<sup>\s*([^<]+?)\s*</sup>', replace_sup, text, flags=re.DOTALL)

    # Replace <sub>...</sub> (handle multi-line)
    text = re.sub(r'<sub>\s*([^<]+?)\s*</sub>', replace_sub, text, flags=re.DOTALL)

    return text

def process_file(file_path):
    """Process the HTML file and convert ALL remaining sup/sub tags."""

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    # Count before
    sup_count_before = len(re.findall(r'<sup>', content))
    sub_count_before = len(re.findall(r'<sub>', content))

    print(f"Found {sup_count_before} <sup> tags and {sub_count_before} <sub> tags")

    # Convert all remaining sup/sub tags
    content = convert_sup_sub_to_unicode(content)

    # Count after
    sup_count_after = len(re.findall(r'<sup>', content))
    sub_count_after = len(re.findall(r'<sub>', content))

    print(f"After conversion: {sup_count_after} <sup> tags and {sub_count_after} <sub> tags remain")

    # Save the modified file
    print(f"\nWriting modified file...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    final_size = len(content)

    return {
        'sup_before': sup_count_before,
        'sub_before': sub_count_before,
        'sup_after': sup_count_after,
        'sub_after': sub_count_after,
        'converted': (sup_count_before - sup_count_after) + (sub_count_before - sub_count_after),
        'original_size': original_size,
        'final_size': final_size,
        'size_change': final_size - original_size
    }

if __name__ == '__main__':
    paper_path = Path(__file__).parent.parent / 'principia-metaphysica-paper.html'

    print("="*80)
    print("CONVERTING REMAINING SUP/SUB TAGS")
    print("="*80)

    results = process_file(paper_path)

    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
    print(f"Converted {results['converted']} tags to Unicode")
    print(f"Remaining: {results['sup_after']} <sup> + {results['sub_after']} <sub>")
    print(f"Size change: {results['size_change']:+,} bytes")
