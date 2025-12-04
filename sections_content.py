#!/usr/bin/env python3
"""
Sections Content Management System
===================================

Centralized content for paper sections and website pages.
This file defines:
- Paper section text and structure
- Topic hierarchies for each section
- Page mappings (which pages use which sections/topics)
- Value requirements for validation

Each section can be used by multiple pages (paper, section pages, index)
with different "Include" specifications for what to display.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

SECTIONS = {
    "abstract": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/index.html",
                "section": "https://www.metaphysicæ.com/index.html#abstract",
                "order": 1,
                "include": [
                    "title",
                    "subtitle",
                    "content"
                ],
                "hover_details": False,
                "template_type": "Hero Section"
            },
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "https://www.metaphysicæ.com/principia-metaphysica-paper.html#abstract",
                "order": 1,
                "include": [
                    "title",
                    "content"
                ],
                "hover_details": False,
                "template_type": "Paper Section"
            }
        ],
        "title": "Abstract",
        "subtitle": "A 26D Two-Time Framework for Particle Physics and Cosmology",
        "content": """
The Principia Metaphysica presents a comprehensive geometric framework unifying particle physics
and cosmology through a 26-dimensional two-time bosonic string theory. The framework achieves
dimensional reduction via Sp(2,R) gauge fixing (26D → 13D shadow) followed by G₂ manifold
compactification (13D → 6D effective → 4D observable).

Key achievements include exact prediction of three fermion generations from topology
(n_gen = χ_eff/48 = 144/48 = 3), SO(10) gauge unification geometrically derived from
G₂ holonomy, complete PMNS matrix with 0.09σ average agreement, dark energy equation
of state w₀ = -0.8528 matching DESI DR2 at 0.38σ, and proton decay lifetime
τ_p = 3.83×10³⁴ years with branching ratios.

The framework resolves six major theoretical challenges: generation count, Planck tension
(reduced 6σ→1.3σ), gauge unification scale, PMNS matrix derivation, KK spectrum quantification,
and proton decay channels. Experimental validation includes 10/14 predictions within 1σ,
3 exact matches, and DESI DR2 confirmation. Critical tests include neutrino mass ordering
(IH at 85.5% confidence, testable by JUNO 2027-2030) and KK gravitons at 5 TeV
(6.2σ HL-LHC discovery potential).
        """.strip(),
        "related_simulation": None,
        "values": []
    },

    "geometric_framework": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "https://www.metaphysicæ.com/principia-metaphysica-paper.html#geometric_framework",
                "order": 2,
                "include": [
                    "title",
                    "content",
                    "topics::dimensional_reduction",
                    "topics::euler_characteristic"
                ],
                "hover_details": True,
                "template_type": "Paper Section"
            },
            {
                "file": "https://www.metaphysicæ.com/sections/geometric-framework.html",
                "section": "",
                "order": 1,
                "include": [
                    "title",
                    "content",
                    "topics",
                    "values"
                ],
                "hover_details": True,
                "template_type": "Section Page"
            }
        ],
        "title": "Section 1: Geometric Framework",
        "subtitle": "26D → 13D → 4D Dimensional Reduction",
        "content": """
The Principia Metaphysica framework begins with 26-dimensional bosonic string theory,
selected for its critical dimension requirement (Virasoro anomaly cancellation).
The framework employs a two-stage dimensional reduction process.

First, Sp(2,R) gauge fixing projects the 26D bulk onto a (13,1) shadow spacetime,
implementing Itzhak Bars' two-time physics formalism. This creates dual temporal
dimensions with Z₂ mirror symmetry, establishing both visible and shadow sectors.

Second, a twisted connected sum (TCS) G₂ manifold compactifies 7 internal dimensions,
leaving a 6D effective theory that reduces to the observed 4D spacetime. The G₂ holonomy
uniquely determines SO(10) gauge symmetry, while the flux-dressed Euler characteristic
χ_eff = 144 geometrically predicts exactly three fermion generations.

The framework's key innovation is deriving particle content and coupling structure
from pure geometry, with no free parameters for generation count, gauge group,
or unification scale.
        """.strip(),
        "related_simulation": "dimensions",
        "values": [
            "D_bulk",
            "D_after_sp2r",
            "D_common",
            "chi_eff",
            "n_gen",
            "b2",
            "b3"
        ],
        "topics": [
            {
                "id": "dimensional_reduction",
                "title": "Dimensional Reduction Pathway",
                "subtitle": "26D → 13D → 6D → 4D",
                "values": [
                    "D_bulk",
                    "D_after_sp2r",
                    "D_effective",
                    "D_common"
                ],
                "template_type": "formula_derivation",
                "topics": [
                    {
                        "id": "sp2r_projection",
                        "title": "Sp(2,R) Gauge Fixing",
                        "subtitle": "Two-Time Physics: 26D → 13D Shadow",
                        "values": [
                            "D_bulk",
                            "D_after_sp2r"
                        ],
                        "template_type": "mechanism_card"
                    },
                    {
                        "id": "g2_compactification",
                        "title": "G₂ Manifold Compactification",
                        "subtitle": "13D → 6D Effective → 4D Observable",
                        "values": [
                            "D_after_sp2r",
                            "D_internal",
                            "D_effective",
                            "D_common"
                        ],
                        "template_type": "mechanism_card"
                    }
                ]
            },
            {
                "id": "euler_characteristic",
                "title": "Generation Count from Topology",
                "subtitle": "χ_eff/48 = 144/48 = 3",
                "content": """
The number of fermion generations emerges from the topology of the G₂ manifold
through the flux-dressed Euler characteristic. The TCS construction gives
χ_eff = 144 after accounting for flux quantization constraints.

The formula n_gen = χ_eff / 48 incorporates both the base mode count (24)
and flux reduction factor (2), yielding exactly three generations with no
free parameters.
                """.strip(),
                "values": [
                    "chi_eff",
                    "n_gen",
                    "b3"
                ],
                "template_type": "prediction_card"
            },
            {
                "id": "so10_emergence",
                "title": "SO(10) from G₂ Holonomy",
                "subtitle": "Gauge Group Geometric Derivation",
                "content": """
The G₂ holonomy group uniquely determines the gauge symmetry through its
relationship to SO(10). The seven-dimensional G₂ manifold admits a natural
embedding into SO(10), with the D₅ singularity in F-theory duality
providing the gauge structure.

This geometric derivation requires SO(10) grand unification with no choice
of gauge group—it emerges necessarily from the G₂ topology.
                """.strip(),
                "values": [
                    "b2",
                    "b3"
                ],
                "template_type": "derivation_card"
            }
        ]
    },

    # Placeholder for other sections - to be filled in
    "cosmology": {
        "pages": [],
        "title": "Section 2: Cosmology and Dark Energy",
        "subtitle": "w₀ from Maximum Entropy Principle",
        "content": "TO BE MIGRATED FROM PAPER",
        "related_simulation": "dark_energy",
        "values": ["w0_PM", "wa_PM_effective", "d_eff", "planck_tension_resolved"],
        "topics": []
    },

    "gauge_unification": {
        "pages": [],
        "title": "Section 3: Gauge Unification",
        "subtitle": "M_GUT from G₂ Torsion",
        "content": "TO BE MIGRATED FROM PAPER",
        "related_simulation": "gauge_unification",
        "values": ["M_GUT", "alpha_GUT_inv"],
        "topics": []
    },

    "fermion_sector": {
        "pages": [],
        "title": "Section 4: Fermion Sector",
        "subtitle": "PMNS Matrix from G₂ Geometry",
        "content": "TO BE MIGRATED FROM PAPER",
        "related_simulation": "pmns_matrix",
        "values": ["theta_23", "theta_12", "theta_13", "delta_CP", "avg_sigma"],
        "topics": []
    },

    "predictions": {
        "pages": [],
        "title": "Section 7: Falsifiable Predictions",
        "subtitle": "Experimental Tests 2027-2035",
        "content": "TO BE MIGRATED FROM PAPER",
        "related_simulation": "validation",
        "values": [],
        "topics": []
    }
}


def get_section(section_id):
    """Get section data by ID"""
    return SECTIONS.get(section_id)


def get_pages_for_section(section_id):
    """Get all pages that use this section"""
    section = get_section(section_id)
    if not section:
        return []
    return section.get('pages', [])


def get_required_values(section_id, include_topics=True):
    """
    Get all required PM values for a section.
    If include_topics=True, recurses through topic hierarchy.
    """
    section = get_section(section_id)
    if not section:
        return []

    values = set(section.get('values', []))

    if include_topics:
        def collect_topic_values(topics):
            for topic in topics:
                values.update(topic.get('values', []))
                if 'topics' in topic:
                    collect_topic_values(topic['topics'])

        collect_topic_values(section.get('topics', []))

    return sorted(list(values))


def get_topic_by_id(section_id, topic_id):
    """
    Find a topic by ID within a section (searches recursively).
    Returns: (topic_dict, parent_path)
    """
    section = get_section(section_id)
    if not section:
        return None, None

    def search_topics(topics, path=[]):
        for topic in topics:
            if topic.get('id') == topic_id:
                return topic, path
            if 'topics' in topic:
                result, subpath = search_topics(topic['topics'], path + [topic['id']])
                if result:
                    return result, subpath
        return None, None

    return search_topics(section.get('topics', []))


if __name__ == "__main__":
    # Test the structure
    print("=== Sections Content Management System ===")
    print(f"\nTotal sections: {len(SECTIONS)}")

    for section_id, section in SECTIONS.items():
        print(f"\n{section_id}:")
        print(f"  Title: {section['title']}")
        print(f"  Pages: {len(section.get('pages', []))}")
        print(f"  Values: {len(section.get('values', []))}")
        print(f"  Topics: {len(section.get('topics', []))}")

        required = get_required_values(section_id)
        print(f"  Total required PM values (with topics): {len(required)}")

        if required:
            print(f"  Sample values: {', '.join(required[:3])}")
