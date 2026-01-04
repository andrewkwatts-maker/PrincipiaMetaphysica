"""
PM Visualization Generators
===========================

Python scripts to generate publication-quality diagrams for the
Principia Metaphysica paper and website.

Output Directory: ../../images/  (project root images folder)

Usage:
    python -m simulations.visualizations.brane_diagrams
    python -m simulations.visualizations.two_time_structure
    etc.

Or run all visualizations:
    python -m simulations.visualizations.generate_all

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from pathlib import Path

# Output directory for generated images
OUTPUT_DIR = Path(__file__).parent.parent.parent / "images"

# PM color palette
PM_COLORS = {
    "purple": "#8b7fff",
    "pink": "#ff7eb6",
    "blue": "#60a5fa",
    "orange": "#fb923c",
    "green": "#4ade80",
    "gold": "#ffd43b",
    "red": "#ef4444",
    "text": "#f8f9fa",
    "bg_dark": "#1a1f3a",
    "bg_card": "#2a2f4a",
}

# Common figure settings
FIGURE_DEFAULTS = {
    "dpi": 300,
    "figsize": (10, 8),
    "facecolor": PM_COLORS["bg_dark"],
    "edgecolor": "none",
}
