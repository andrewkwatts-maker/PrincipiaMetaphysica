"""
HTML to Section JSON Converter
==============================

Converts section HTML files to JSON format following the section schema.
Used by agents to process each section file.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Any, Optional


class SectionHTMLParser(HTMLParser):
    """Parse section HTML and extract content blocks."""

    def __init__(self):
        super().__init__()
        self.content_blocks = []
        self.current_block = None
        self.in_content = False
        self.current_text = ""
        self.subsections = []
        self.current_subsection = None
        self.formula_refs = set()
        self.param_refs = set()
        self.cross_refs = {"sections": set(), "appendices": set(), "formulas": set()}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Track formula references
        if attrs_dict.get("data-formula-id"):
            self.formula_refs.add(attrs_dict["data-formula-id"])

        # Track parameter references
        if "pm-param" in attrs_dict.get("class", ""):
            param_id = attrs_dict.get("data-id", attrs_dict.get("data-param"))
            if param_id:
                self.param_refs.add(param_id)

        # Track subsections
        if tag in ["h2", "h3", "h4"] and "subsection" in attrs_dict.get("class", ""):
            self.current_subsection = {
                "id": attrs_dict.get("id", ""),
                "title": "",
                "contentBlocks": []
            }

        # Track content blocks
        if tag == "div" and "subsection" in attrs_dict.get("class", ""):
            self.in_content = True

        if tag == "p":
            self.current_block = {"type": "paragraph", "content": ""}

        if tag == "div" and "derivation-box" in attrs_dict.get("class", ""):
            self.current_block = {"type": "derivation", "content": ""}

    def handle_endtag(self, tag):
        if tag == "p" and self.current_block:
            self.current_block["content"] = self.current_text.strip()
            if self.current_block["content"]:
                if self.current_subsection:
                    self.current_subsection["contentBlocks"].append(self.current_block)
                else:
                    self.content_blocks.append(self.current_block)
            self.current_block = None
            self.current_text = ""

        if tag in ["h2", "h3", "h4"] and self.current_subsection:
            self.current_subsection["title"] = self.current_text.strip()
            self.current_text = ""

        if tag == "div" and self.current_subsection and self.in_content:
            self.subsections.append(self.current_subsection)
            self.current_subsection = None
            self.in_content = False

    def handle_data(self, data):
        self.current_text += data

        # Extract cross-references
        section_refs = re.findall(r"Section\s+(\d+(?:\.\d+)?[a-z]?)", data)
        for ref in section_refs:
            self.cross_refs["sections"].add(f"Section {ref}")

        appendix_refs = re.findall(r"Appendix\s+([A-Z])", data)
        for ref in appendix_refs:
            self.cross_refs["appendices"].add(f"Appendix {ref}")


def extract_section_metadata(html_content: str) -> Dict[str, Any]:
    """Extract metadata from section HTML."""
    metadata = {}

    # Extract title
    title_match = re.search(r"<title>([^<]+)</title>", html_content)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    # Extract section number from title
    section_match = re.search(r"Section\s+(\d+)", metadata.get("title", ""))
    if section_match:
        metadata["id"] = section_match.group(1)
        metadata["type"] = "section"
    elif "Appendix" in metadata.get("title", ""):
        appendix_match = re.search(r"Appendix\s+([A-Z])", metadata["title"])
        if appendix_match:
            metadata["id"] = appendix_match.group(1)
            metadata["type"] = "appendix"

    # Extract description
    desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html_content)
    if desc_match:
        metadata["abstract"] = desc_match.group(1)

    return metadata


def html_to_section_json(html_path: Path) -> Dict[str, Any]:
    """Convert HTML section file to JSON structure."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract metadata
    section = extract_section_metadata(html_content)

    # Parse content
    parser = SectionHTMLParser()
    parser.feed(html_content)

    section["contentBlocks"] = parser.content_blocks
    section["subsections"] = parser.subsections
    section["formulaRefs"] = list(parser.formula_refs)
    section["paramRefs"] = list(parser.param_refs)
    section["crossRefs"] = {
        "sections": list(parser.cross_refs["sections"]),
        "appendices": list(parser.cross_refs["appendices"]),
        "formulas": list(parser.formula_refs)
    }
    section["sectionFile"] = f"sections/{html_path.name}"

    return section


def save_section_json(section: Dict[str, Any], output_dir: Path):
    """Save section to JSON file."""
    section_id = section.get("id", "unknown")
    section_type = section.get("type", "section")

    if section_type == "appendix":
        filename = f"appendix-{section_id.lower()}.json"
    else:
        filename = f"section-{section_id}.json"

    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(section, f, indent=2, ensure_ascii=False)

    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python html_to_section_json.py <html_file>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"File not found: {html_path}")
        sys.exit(1)

    section = html_to_section_json(html_path)
    print(json.dumps(section, indent=2, ensure_ascii=False))
