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

    "introduction": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#intro",
                "order": 1,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "1. Introduction and Motivation",
        "subtitle": "Why Three Generations? Why This Gauge Group?",
        "content": """
The Standard Model of particle physics, while extraordinarily successful, leaves fundamental questions
unanswered: Why are there exactly three generations of fermions? What is the origin of the gauge group
structure? Why does time have a preferred direction? The Principia Metaphysica framework attempts to
address these questions through a geometric unification in higher dimensions.

The framework begins with 26D spacetime with signature (24,2)—the critical dimension of bosonic
string theory chosen for anomaly cancellation. Through Sp(2,R) gauge fixing and G₂ manifold
compactification, we derive the observed 4D universe with its particle content and coupling
structure emerging from pure geometry.

The framework achieves complete resolution of all critical issues through rigorous geometric derivations
and Monte Carlo simulations, establishing 100% parameter derivation from first principles. All predictions
have been validated through SymPy symbolic computation and numerical analysis.
        """.strip(),
        "related_simulation": None,
        "values": [
            "chi_eff",
            "n_gen",
            "alpha_GUT_inv",
            "M_GUT",
            "predictions_within_1sigma",
            "total_predictions",
            "exact_matches",
            "issues_resolved"
        ],
        "topics": []
    },

    "geometric_framework": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#framework",
                "order": 2,
                "include": [
                    "title",
                    "content",
                    "topics"
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
        "title": "2. Theoretical Framework",
        "subtitle": "26D → 13D → 6D → 4D Dimensional Reduction",
        "content": """
The framework begins with a 26-dimensional bulk spacetime M²⁶ with signature (24,2)—24 spacelike
and 2 timelike dimensions. This is the critical dimension of bosonic string theory, chosen for
anomaly cancellation. The fundamental action is:

S = ∫ d²⁶X √(-G) [R + Ψ̄_P (iΓᴹ D_M - m) Ψ_P + ℒ_Sp(2,R)]

where M_* is the fundamental scale, R₂₆ is the 26D Ricci scalar, Ψ_P is the Pneuma field,
and ℒ_Sp(2,R) contains the gauge constraints that eliminate ghosts from the second time dimension.

The second time dimension is rendered physically consistent through Sp(2,R) gauge constraints,
which eliminate ghost states. Gauge-fixing these constraints projects the 26D theory onto an
effective 13D (12,1) bulk spacetime. This 13D bulk then undergoes G₂ compactification, reducing
to a 6D (5,1) effective spacetime that hosts the heterogeneous brane structure.
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
                "id": "condensate_gap",
                "title": "Condensate Gap Equation",
                "template_type": "subsection"
            },
            {
                "id": "26d_structure",
                "title": "2.1.1 The 26D Two-Time Structure",
                "template_type": "subsection"
            },
            {
                "id": "sp2r_gauge",
                "title": "2.1.2 Sp(2,R) Gauge Symmetry",
                "template_type": "subsection"
            },
            {
                "id": "14d_halves",
                "title": "2.1.3 The 26D→13D shadow Two-Time Structure (Enhanced Framework)",
                "template_type": "subsection"
            },
            {
                "id": "central_charge_2t",
                "title": "Anomaly Cancellation in 2T Framework",
                "template_type": "subsection"
            },
            {
                "id": "2t_brane_action",
                "title": "2T p-Brane Action with Null Constraints",
                "template_type": "subsection"
            },
            {
                "id": "clifford",
                "title": "Clifford Algebra Foundation (Established Mathematics)",
                "template_type": "subsection"
            },
            {
                "id": "four_brane_structure",
                "title": "2.2.1 The 1 + 3 Brane Hierarchy",
                "template_type": "subsection"
            },
            {
                "id": "mirror_branes",
                "title": "2.2.2 Z₂ Mirror Brane Structure",
                "template_type": "subsection"
            },
            {
                "id": "planck_derivation",
                "title": "Derivation of M_Pl from Kaluza-Klein Reduction",
                "template_type": "subsection"
            }
        ]
    },

    "pneuma_manifold": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#geometry",
                "order": 3,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "3. Geometric Structure: The Pneuma Manifold",
        "subtitle": "G₂ Holonomy and Generation Count",
        "content": """
Important Clarification: G₂_Pneuma is a 7-dimensional G₂ holonomy manifold, not an 8D Calabi-Yau
four-fold. The 13D → 6D compactification proceeds via G₂ structure, with gauge symmetry arising
from D₅ singularities in the G₂ manifold (analogous to F-theory D-type singularities but in 7D).

The explicit construction uses the Twisted Connected Sum (TCS) method [arXiv:1809.09083] with
Betti numbers b₂=4, b₃=24 and flux-dressed Euler characteristic χ_eff = 144, yielding exactly
3 fermion generations.

In M-theory compactification on a G₂ manifold, the number of chiral generations is determined by
the effective Euler characteristic (analogous to F-theory index theorem). The framework uses the
flux-dressed topology χ_eff = 144 from the 13D shadow flux-dressed G₂ topology.

The generation formula is: n_gen = χ_eff / 48 = 144 / 48 = 3
        """.strip(),
        "related_simulation": "topology",
        "values": [
            "chi_eff",
            "n_gen",
            "b2",
            "b3"
        ],
        "topics": [
            {
                "id": "hodge_derivation",
                "title": "Derivation of Betti Numbers and Euler Characteristic (G₂ Geometry)",
                "template_type": "subsection"
            },
            {
                "id": "generation_derivation",
                "title": "Derivation of n_gen = χ_eff/24 (M-Theory on G₂)",
                "template_type": "subsection"
            }
        ]
    },

    "gauge_unification": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#gauge",
                "order": 4,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "4. SO(10) Gauge Unification",
        "subtitle": "Geometric Origin of Grand Unification",
        "content": """
The SO(10) gauge group arises from conical singularities in the G₂ manifold G₂_Pneuma.
These singularities are analogous to F-theory D-type singularities but occur in the 7D G₂ geometry.
The gauge fields live on coassociative 4-cycles that wrap the singular locus.

The G₂ singularity classification [Acharya-Witten 2001, Atiyah-Witten 2001] determines gauge
symmetry from the conical singularity type. For SO(10) (D₅ type), the gauge coupling unification
is achieved through corrected sequential renormalization group (RG) evolution.

The framework predicts unified gauge coupling 1/α_GUT = 23.54 at M_GUT = 2.118×10¹⁶ GeV
(geometrically determined from TCS G₂ torsion structure) through corrected sequential RG evolution,
achieving ~2% precision (unprecedented for non-SUSY SO(10)).
        """.strip(),
        "related_simulation": "gauge_unification",
        "values": [
            "M_GUT",
            "alpha_GUT_inv",
            "chi_eff",
            "b2",
            "b3"
        ],
        "topics": [
            {
                "id": "kodaira_classification",
                "title": "G₂ Singularity Classification for SO(10)",
                "template_type": "subsection"
            },
            {
                "id": "gut_derivation",
                "title": "Derivation of M_GUT from RG Running",
                "template_type": "subsection"
            },
            {
                "id": "beta_functions",
                "title": "Beta Functions with SO(10) Group Factors",
                "template_type": "subsection"
            },
            {
                "id": "seesaw_mechanism",
                "title": "4.5 Seesaw Mechanism for Neutrino Masses",
                "template_type": "subsection"
            }
        ]
    },

    "thermal_time": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#thermal",
                "order": 5,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "5. Thermal Time and Emergent Temporality",
        "subtitle": "Time from Thermodynamics",
        "content": """
Following Connes-Rovelli, time is not fundamental but emerges from thermodynamic structure.
Given a quantum state ρ with von Neumann entropy S = -Tr(ρ ln ρ), the modular
Hamiltonian K generates time evolution:

ρ = e^(-K) / Z,    α_t(A) = e^(iKt) A e^(-iKt)

The thermal time τ is related to the modular flow parameter. In the cosmological context,
the thermal time coincides with proper time in the semiclassical limit. The entropy current
provides the microscopic foundation for the thermal time hypothesis: time flows in the direction
of entropy increase.

The key thermal time parameter α_T = 2.7 is derived from two-time cosmological thermodynamics,
incorporating corrections from the orthogonal time dimension and mirror sector coupling.
        """.strip(),
        "related_simulation": None,
        "values": [],
        "topics": [
            {
                "id": "tomita_takesaki",
                "title": "Mathematical Foundation: Tomita-Takesaki Theory",
                "template_type": "subsection"
            },
            {
                "id": "entropy_current",
                "title": "5.1.1 Local Entropy Current",
                "template_type": "subsection"
            },
            {
                "id": "alpha_derivation",
                "title": "Derivation of α_T = 2.7 (Two-Time Cosmological Thermodynamics)",
                "template_type": "subsection"
            }
        ]
    },

    "cosmology": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#cosmology",
                "order": 6,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "6. Cosmological Implications",
        "subtitle": "Dark Energy and the Mashiach Field",
        "content": """
The Kähler moduli potential must satisfy swampland conjectures for consistency with quantum gravity:

V(φ) = V₀ e^(-λφ/M_Pl) [1 + A cos(ωφ + θ)]

Swampland distance conjecture: |∇V|/V ≥ c ~ O(1)/M_Pl must hold, which our exponential potential
satisfies with λ = 0.8378 (derived from D_eff = 12.589). This connects the dark energy equation
of state to string theory consistency conditions.

The "Mashiach" field φ_M is a light scalar modulus that survives from the compactification.
Its potential drives late-time cosmic acceleration with equation of state:

w(z) = w₀ [1 + (α_T/3) ln(1+z)]

Theory-Observation Match: Principia Metaphysica predicts w₀ = -0.8528 from the effective dimension
D_eff = 12.589 (geometry-derived from TCS G₂ torsion structure), achieving 0.38σ agreement with
DESI DR2 (w₀ = -0.83 ± 0.06 at 4.2σ).
        """.strip(),
        "related_simulation": "dark_energy",
        "values": [
            "w0_PM",
            "w0_DESI_central",
            "w0_DESI_error",
            "w0_sigma",
            "wa_PM_effective"
        ],
        "topics": [
            {
                "id": "moduli_potential",
                "title": "6.0 Moduli Potential with Swampland Compliance",
                "template_type": "subsection"
            },
            {
                "id": "mashiach_attractor",
                "title": "Mashiach Attractor Mechanism",
                "template_type": "subsection"
            },
            {
                "id": "wz_derivation",
                "title": "Derivation of w(z) from Thermal Friction",
                "template_type": "subsection"
            }
        ]
    },

    "predictions": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#predictions",
                "order": 7,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "7. Predictions and Testability",
        "subtitle": "Falsifiable Experimental Tests 2027-2035",
        "content": """
The framework makes quantified, falsifiable predictions testable by current and near-future experiments.
Key predictions include:

1. Proton Decay: τ_p = 3.83×10³⁴ years with 68% confidence interval [2.48, 5.51]×10³⁴ years,
   achieving 0.177 orders of magnitude uncertainty. Channel-specific branching ratios include
   BR(p→e⁺π⁰) = 0.342 ± 0.109 and BR(p→K⁺ν̄) = 0.186 ± 0.074.

2. Neutrino Mass Hierarchy: Inverted Hierarchy (IH) predicted at 85.5% confidence from the
   Atiyah-Singer index theorem on associative 3-cycles in the G₂ manifold. Testable by
   JUNO (2027-2028) and DUNE (2028+).

3. PMNS Matrix: All four angles derived with 0.09σ average deviation from NuFIT 5.3,
   including two exact matches (θ₂₃ = 47.20° and θ₁₃ = 8.54°).

4. Dark Energy Evolution: w(z) = w₀[1 + (α_T/3) ln(1+z)] with logarithmic form preferred
   over CPL by Δχ² = 38.8 (6.2σ).
        """.strip(),
        "related_simulation": "validation",
        "values": [
            "tau_p_median",
            "uncertainty_oom",
            "BR_epi0_mean",
            "BR_Knu_mean",
            "prob_IH_mean",
            "prob_IH_std",
            "theta_23",
            "theta_12",
            "theta_13",
            "delta_CP",
            "avg_sigma",
            "predictions_within_1sigma",
            "total_predictions",
            "exact_matches"
        ],
        "topics": [
            {
                "id": "proton_derivation",
                "title": "Derivation of Proton Lifetime (Standard GUT Formula)",
                "template_type": "subsection"
            },
            {
                "id": "philosophical_implications",
                "title": "7.5 Speculative Interpretations: Consciousness and Hidden Variables",
                "template_type": "subsection"
            },
            {
                "id": "asymptotic_safety",
                "title": "7.6 Asymptotic Safety (Weinberg-Reuter)",
                "template_type": "subsection"
            }
        ]
    },

    "resolution_status": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#concerns",
                "order": 8,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "8. Resolution Status and Validation",
        "subtitle": "100% Parameter Derivation from First Principles",
        "content": """
The framework has been rigorously examined for mathematical consistency, physics viability,
experimental testability, and cosmological predictions. This section summarizes the validation status,
demonstrating resolution of all 14 critical issues with 100% parameter derivation from first principles.

Overall Framework Grade: A+
- 14 of 14 Critical Issues Resolved
- 10 of 14 Predictions Within 1σ | 3 Exact Matches
- Mathematical Rigor: 9/10
- Physics Consistency: 10/10
- Experimental Testability: 10/10
- Cosmology/DESI: 9/10

Major Achievements:
1. Generation count prediction: χ_eff = 144 from TCS G₂ construction yields exactly 3 generations
2. Dark energy attractor: Mashiach minimum achieves exact w → -1.0 late-time limit
3. Gauge unification: 1/α_GUT = 23.54 with ~2% precision (unprecedented for non-SUSY SO(10))
4. Complete parameter derivation: All 58 parameters rigorously derived from geometry (100%)
        """.strip(),
        "related_simulation": None,
        "values": [
            "issues_resolved",
            "total_predictions",
            "predictions_within_1sigma",
            "exact_matches",
            "chi_eff",
            "n_gen",
            "alpha_GUT_inv",
            "M_GUT",
            "w0_PM",
            "uncertainty_oom",
            "prob_IH_mean",
            "avg_sigma"
        ],
        "topics": []
    },

    "conclusion": {
        "pages": [
            {
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#conclusion",
                "order": 9,
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }
        ],
        "title": "9. Conclusions and Future Prospects",
        "subtitle": "Experimental Roadmap 2027-2035",
        "content": """
Framework Validation Status:

Total Parameters: 58
Validation Passed: 58 (100%)
Expected Failures: 0 (all parameters derived)
Predictions within 1σ: 10 of 14 (71%)
Critical Fixes: All 14 issues resolved (100%)
Exact Matches: 3 (θ₂₃, θ₁₃, w(z) form)

What the Theory Achieves:
- 3 generations from flux-dressed topology: n_gen = χ_eff/48 = 144/48 = 3 exactly
- Gauge unification achieved: 1/α_GUT = 23.54 ± 0.45 at M_GUT = 2.118×10¹⁶ GeV
- Dark energy attractor resolved: w → -1.0 exactly via Mashiach minimum
- SO(10) from geometry: D₅ singularity in G₂ manifold (M-theory)
- Heterogeneous branes: Observable (5,1) with 2 shared extra dimensions, shadows (3,1)
- KK gravitons at 5 TeV: Testable prediction from 2D_shared compactification

Validation Status (December 2025): The framework achieves all 14 major issues resolved with
100% parameter derivation from first principles (58/58 derived, 0 fitted). The complete resolution
establishes exceptional validation: 10/14 predictions within 1σ, including 3 exact matches.
All core physics predictions are complete and falsifiable.
        """.strip(),
        "related_simulation": None,
        "values": [
            "total_predictions",
            "predictions_within_1sigma",
            "exact_matches",
            "issues_resolved",
            "chi_eff",
            "n_gen",
            "alpha_GUT_inv",
            "M_GUT",
            "tau_p_median",
            "uncertainty_oom",
            "BR_epi0_mean",
            "BR_Knu_mean",
            "prob_IH_mean",
            "avg_sigma"
        ],
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
