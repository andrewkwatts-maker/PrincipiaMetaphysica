"""
Principia Metaphysica - Section JSON Schema
============================================

This module defines the schema for section JSON files that will be
merged into theory_output.json. Each section file follows this structure.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

SECTION_SCHEMA = {
    # ============================================
    # CORE METADATA
    # ============================================
    "id": "string",               # e.g., "1", "2", "A", "B" (sections are numbers, appendices are letters)
    "type": "string",             # "section" | "appendix" | "conclusion"
    "title": "string",            # Full section title
    "shortTitle": "string",       # Short title for navigation
    "order": "number",            # Display order (1, 2, 3... or 100, 101 for appendices)
    "category": "string",         # "theoretical" | "mathematical" | "phenomenological" | "supplementary"

    # ============================================
    # NAVIGATION & CROSS-REFERENCES
    # ============================================
    "prevSection": "string|null", # ID of previous section
    "nextSection": "string|null", # ID of next section
    "parentId": "string|null",    # Parent section ID (for subsections)
    "sectionFile": "string",      # HTML file path: "sections/introduction.html"

    # Cross-references by name (for dynamic linking)
    "crossRefs": {
        "sections": ["string"],   # ["Section 2", "Section 5.3"]
        "appendices": ["string"], # ["Appendix A", "Appendix H"]
        "formulas": ["string"],   # ["vev-electroweak", "alpha-gut"]
        "parameters": ["string"], # ["alpha_GUT", "M_GUT"]
        "simulations": ["string"] # ["derive_vev_pneuma.py"]
    },

    # ============================================
    # PAPER CONTENT (Academic/Formal)
    # ============================================
    "abstract": "string",         # Section abstract
    "paperLineStart": "number",   # Line number in paper HTML
    "paperLineEnd": "number",     # End line number

    "contentBlocks": [            # Main section content
        {
            "type": "string",     # "paragraph" | "equation" | "derivation" | "figure" | "list" | "quote" | "note"
            "content": "string",  # Raw content (HTML or LaTeX)
            "label": "string|null", # Optional label for reference
            "equationNumber": "string|null",  # For equations: "(1.1)"
            "caption": "string|null",  # For figures
            "className": "string|null" # CSS class for styling
        }
    ],

    "subsections": [              # Nested subsections
        {
            "id": "string",       # "1.1", "1.2", "1.2a"
            "title": "string",
            "contentBlocks": [],  # Same structure as parent
            "formulaRefs": [],
            "paramRefs": []
        }
    ],

    # ============================================
    # WEBSITE-ONLY CONTENT (Non-academic)
    # ============================================
    "websiteOnlyContent": [
        {
            "type": "string",     # "explainer" | "analogy" | "interactive" | "visualization"
            "title": "string",
            "content": "string",
            "targetAudience": "string"  # "beginner" | "intermediate" | "expert"
        }
    ],

    "beginnerSummary": "string",   # Plain-language summary
    "keyTakeaways": ["string"],    # Bullet points
    "learningObjectives": ["string"],
    "relatedConcepts": ["string"], # Links to foundations page concepts

    # ============================================
    # REFERENCES (by name for dynamic lookup)
    # ============================================
    "formulaRefs": ["string"],     # Formula IDs: ["vev-electroweak", "alpha-gut"]
    "paramRefs": ["string"],       # Parameter IDs: ["alpha_GUT", "M_GUT", "v_EW"]
    "figureRefs": ["string"],      # Figure IDs
    "citationRefs": ["string"],    # Citation keys: ["Bars2006", "Witten1995"]

    # ============================================
    # APPENDIX-SPECIFIC (for type="appendix")
    # ============================================
    "appendices": ["string"],      # Related appendix IDs this section references
    "simulationFile": "string",    # Primary simulation file
    "derivationSteps": [           # Formal derivation steps
        {
            "step": "number",
            "description": "string",
            "equation": "string",
            "notes": "string|null"
        }
    ],

    # ============================================
    # METADATA FOR DISPLAY
    # ============================================
    "estimatedReadTime": "number", # Minutes
    "difficulty": "string",        # "introductory" | "intermediate" | "advanced"
    "lastUpdated": "string",       # ISO date
    "version": "string"            # Content version
}

# Section ID to HTML file mapping
SECTION_FILE_MAP = {
    # Main Sections
    "1": "introduction.html",
    "2": "geometric-framework.html",
    "3": "fermion-sector.html",
    "4": "gauge-unification.html",
    "5": "cosmology.html",
    "6": "predictions.html",
    "7": "conclusion.html",

    # Supplementary sections (website-only)
    "thermal-time": "thermal-time.html",
    "pneuma-lagrangian": "pneuma-lagrangian.html",
    "cmb-bubble": "cmb-bubble-collisions-comprehensive.html",
    "division-algebra": "division-algebra-section.html",
    "einstein-hilbert": "einstein-hilbert-term.html",
    "xy-gauge": "xy-gauge-bosons.html",
    "theory-analysis": "theory-analysis.html",

    # Appendices
    "A": "appendix-a-virasoro.html",
    "B": "appendix-b-generations.html",
    "C": "appendix-c-theta23.html",
    "D": "appendix-d-dark-energy.html",
    "E": "appendix-e-delta-lat-probes.html",
    "F": "appendix-f-subleading-dispersion.html",
    "G": "appendix-g-torsion.html",
    "H": "appendix-h-proton-decay-br.html",
    "I": "appendix-i-gw-dispersion.html",
    "J": "appendix-j-monte-carlo.html",
    "K": "appendix-k-transparency.html",
    "L": "appendix-l-values-summary.html"
}

# Cross-reference name patterns for validation
CROSS_REF_PATTERNS = {
    "section": r"Section\s+(\d+(?:\.\d+)?[a-z]?)",
    "appendix": r"Appendix\s+([A-Z])",
    "equation": r"(?:Eq\.|Equation)\s*\(?([\d.]+)\)?",
    "figure": r"(?:Fig\.|Figure)\s+(\d+(?:\.\d+)?)",
    "table": r"Table\s+(\d+(?:\.\d+)?)"
}
