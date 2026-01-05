"""
Section Registry for Principia Metaphysica
============================================

Defines the paper structure with sections, subsections, and appendices.
Each section tracks which formulas and parameters it contains.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json
import os


@dataclass
class SubsectionInfo:
    """Information about a subsection."""
    id: str
    title: str


@dataclass
class SectionInfo:
    """Complete information about a paper section."""
    id: str
    title: str
    description: str
    section_type: str = "section"  # "section" or "appendix"
    subsections: List[SubsectionInfo] = field(default_factory=list)
    formula_refs: List[str] = field(default_factory=list)
    param_refs: List[str] = field(default_factory=list)
    simulation_source: Optional[str] = None


# Define the complete paper structure
PAPER_SECTIONS: Dict[str, SectionInfo] = {
    # Abstract (Section 0)
    "0": SectionInfo(
        id="0",
        title="Abstract",
        description="The 26D(24,2) ancestral bulk, S_PR(2) gauge filter, G2 manifold, and 6D→4D projection.",
        section_type="abstract",
        simulation_source="foundations_v16_2"  # Abstract content from foundations
    ),
    # Main Sections
    "1": SectionInfo(
        id="1",
        title="Introduction",
        description="Overview of M-theory compactification and the unified framework",
        section_type="section",
        simulation_source=None  # Manual content
    ),
    "2": SectionInfo(
        id="2",
        title="Geometric Framework",
        description="The Pneuma mechanism and G2 manifold construction",
        section_type="section",
        subsections=[
            SubsectionInfo("2.1", "The Pneuma Mechanism"),
            SubsectionInfo("2.2", "G2 Holonomy Manifolds"),
            SubsectionInfo("2.3", "TCS Construction"),
            SubsectionInfo("2.4", "Effective Field Theory"),
        ],
        simulation_source="pneuma_mechanism_v16_0"
    ),
    "3": SectionInfo(
        id="3",
        title="Gauge Unification",
        description="Symmetry breaking chain from E8 to Standard Model",
        section_type="section",
        subsections=[
            SubsectionInfo("3.1", "The E8 Embedding"),
            SubsectionInfo("3.2", "Breaking Chain"),
            SubsectionInfo("3.3", "Coupling Unification"),
            SubsectionInfo("3.4", "GUT Scale"),
        ],
        simulation_source="gauge_unification_v16_0"
    ),
    "4": SectionInfo(
        id="4",
        title="Fermion Sector",
        description="Three generations and flavor structure from G2 topology",
        section_type="section",
        subsections=[
            SubsectionInfo("4.1", "Generation Structure"),
            SubsectionInfo("4.2", "Yukawa Textures"),
            SubsectionInfo("4.3", "CKM Matrix"),
            SubsectionInfo("4.4", "Higgs Mechanism"),
            SubsectionInfo("4.5", "Neutrino Physics"),
            SubsectionInfo("4.6", "Proton Decay"),
        ],
        simulation_source="fermion_generations_v16_0"
    ),
    "5": SectionInfo(
        id="5",
        title="Cosmology",
        description="Multi-sector cosmology and dark energy from moduli dynamics",
        section_type="section",
        subsections=[
            SubsectionInfo("5.1", "Moduli Stabilization"),
            SubsectionInfo("5.2", "Multi-Sector Dynamics"),
            SubsectionInfo("5.3", "Dark Energy"),
            SubsectionInfo("5.4", "Dark Matter"),
            SubsectionInfo("5.5", "Thermal History"),
        ],
        simulation_source="multi_sector_v16_0"
    ),
    "6": SectionInfo(
        id="6",
        title="Predictions",
        description="Testable predictions and experimental signatures",
        section_type="section",
        subsections=[
            SubsectionInfo("6.1", "Proton Decay"),
            SubsectionInfo("6.2", "Gravitational Waves"),
            SubsectionInfo("6.3", "Collider Signatures"),
        ],
        simulation_source="predictions_v16_0"
    ),
    "7": SectionInfo(
        id="7",
        title="Discussion",
        description="Interpretation and open questions",
        section_type="section",
        simulation_source=None
    ),
    "8": SectionInfo(
        id="8",
        title="Conclusion",
        description="Summary and future directions",
        section_type="section",
        simulation_source=None
    ),

    # Appendices
    "A": SectionInfo(
        id="A",
        title="Virasoro Anomaly Cancellation",
        description="Central charge calculation and anomaly freedom",
        section_type="appendix"
    ),
    "B": SectionInfo(
        id="B",
        title="Generation Number Derivation",
        description="Three generations from Euler characteristic",
        section_type="appendix"
    ),
    "C": SectionInfo(
        id="C",
        title="Atmospheric Mixing Angle",
        description="Derivation of theta_23 near maximal",
        section_type="appendix"
    ),
    "D": SectionInfo(
        id="D",
        title="Dark Energy Equation of State",
        description="w(z) from moduli dynamics",
        section_type="appendix"
    ),
    "E": SectionInfo(
        id="E",
        title="Proton Decay Calculation",
        description="Detailed lifetime calculation",
        section_type="appendix"
    ),
    "F": SectionInfo(
        id="F",
        title="Dimensional Decomposition",
        description="26D to 4D reduction via 13D shadow (PM chain: 26D→13D→6D→4D)",
        section_type="appendix"
    ),
    "G": SectionInfo(
        id="G",
        title="Effective Torsion from Flux",
        description="G-flux and torsion classes",
        section_type="appendix"
    ),
    "H": SectionInfo(
        id="H",
        title="Proton Decay Branching Ratios",
        description="Channel-by-channel predictions",
        section_type="appendix"
    ),
    "I": SectionInfo(
        id="I",
        title="Gravitational Wave Dispersion",
        description="Modified dispersion relation",
        section_type="appendix"
    ),
    "J": SectionInfo(
        id="J",
        title="Monte Carlo Methods",
        description="Numerical simulation techniques",
        section_type="appendix"
    ),
    "K": SectionInfo(
        id="K",
        title="Transparency Statement",
        description="AI assistance disclosure",
        section_type="appendix"
    ),
    "L": SectionInfo(
        id="L",
        title="PM Values Table",
        description="Complete parameter table",
        section_type="appendix"
    ),
}


class SectionRegistry:
    """
    Registry for paper sections with content tracking.

    Usage:
        registry = SectionRegistry()
        section = registry.get_section("4.6")
        subsections = registry.get_subsections("4")
        registry.register_content("4.6", content, "proton_decay_v16_0")
    """

    def __init__(self, load_from_json: bool = True):
        """Initialize the section registry."""
        self._sections = dict(PAPER_SECTIONS)
        self._content: Dict[str, Any] = {}

        if load_from_json:
            self._load_from_theory_output()

    def _load_from_theory_output(self) -> None:
        """Load section data from theory_output.json if available."""
        json_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "AutoGenerated", "theory_output.json"
        )

        if not os.path.exists(json_path):
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            sections_data = data.get('sections', {})
            for section_id, section_info in sections_data.items():
                if section_id in self._sections:
                    # Update formula and param refs from JSON
                    self._sections[section_id].formula_refs = section_info.get('formulaRefs', [])
                    self._sections[section_id].param_refs = section_info.get('paramRefs', [])
        except Exception as e:
            import warnings
            warnings.warn(f"Could not load theory_output.json: {e}")

    def get_section(self, section_id: str) -> Optional[SectionInfo]:
        """Get section metadata by ID."""
        # Handle subsection IDs like "4.6"
        if '.' in section_id:
            parent_id = section_id.split('.')[0]
            return self._sections.get(parent_id)
        return self._sections.get(section_id)

    def get_subsections(self, section_id: str) -> List[SubsectionInfo]:
        """Get all subsections for a section."""
        section = self._sections.get(section_id)
        if section:
            return section.subsections
        return []

    def register_content(
        self,
        section_id: str,
        content: Any,
        source: str
    ) -> None:
        """Add content from a simulation to a section."""
        self._content[section_id] = {
            'content': content,
            'source': source
        }

    def get_content(self, section_id: str) -> Optional[Any]:
        """Get registered content for a section."""
        entry = self._content.get(section_id)
        return entry['content'] if entry else None

    def get_all_sections(self) -> Dict[str, SectionInfo]:
        """Return all sections."""
        return dict(self._sections)

    def get_main_sections(self) -> Dict[str, SectionInfo]:
        """Return only main sections (not appendices)."""
        return {
            k: v for k, v in self._sections.items()
            if v.section_type == "section"
        }

    def get_appendices(self) -> Dict[str, SectionInfo]:
        """Return only appendices."""
        return {
            k: v for k, v in self._sections.items()
            if v.section_type == "appendix"
        }

    def validate_coverage(self) -> Dict[str, List[str]]:
        """Check which sections have content and which don't."""
        with_content = []
        without_content = []

        for section_id, section in self._sections.items():
            if section_id in self._content or section.simulation_source is None:
                with_content.append(section_id)
            else:
                without_content.append(section_id)

        return {
            'with_content': with_content,
            'without_content': without_content
        }


# Helper functions
def section_id_to_title(section_id: str) -> str:
    """Convert section ID to title."""
    registry = SectionRegistry(load_from_json=False)

    if '.' in section_id:
        parent_id, sub_num = section_id.split('.', 1)
        section = registry.get_section(parent_id)
        if section:
            for sub in section.subsections:
                if sub.id == section_id:
                    return sub.title
    else:
        section = registry.get_section(section_id)
        if section:
            return section.title

    return section_id


def get_section_path(section_id: str) -> List[str]:
    """Get breadcrumb path for a section ID."""
    registry = SectionRegistry(load_from_json=False)

    if '.' in section_id:
        parent_id = section_id.split('.')[0]
        section = registry.get_section(parent_id)
        if section:
            for sub in section.subsections:
                if sub.id == section_id:
                    return [section.title, sub.title]
    else:
        section = registry.get_section(section_id)
        if section:
            return [section.title]

    return [section_id]


def is_appendix(section_id: str) -> bool:
    """Check if a section ID is an appendix."""
    return section_id.upper() in "ABCDEFGHIJKLMN"
