#!/usr/bin/env python3
"""
Section Registry for Principia Metaphysica
===========================================

Defines all paper sections with metadata for dynamic rendering.
This file is imported by config.py and exported to theory_output.json.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

from config import SectionMetadata

# ==============================================================================
# SECTION REGISTRY
# ==============================================================================

SECTION_REGISTRY = {
    "1": SectionMetadata(
        id="1",
        title="Introduction",
        section_type="section",
        abstract="The Principia Metaphysica framework unifies quantum mechanics, general relativity, and particle physics through a 26D bulk geometry with (24,2) signature. We propose that observable reality emerges from dimensional reduction through Sp(2,R) gauge fixing and G₂ holonomy compactification, yielding three fermion generations and precise predictions for particle masses and lifetimes.",
        section_file="sections/introduction.html",
        beginner_summary="This theory starts with 26 dimensions and uses geometric symmetries to derive the Standard Model of particle physics. Think of it like origami: we fold higher dimensions to create the 3D space and particles we observe.",
        key_takeaways=[
            "The framework begins with 26D spacetime with signature (24,2)",
            "Dimensional reduction via Sp(2,R) gauge fixing projects to 13D",
            "G₂ holonomy compactification yields 4D observable + 3 shadow branes",
            "Three fermion generations arise from χ_eff = 144 (Euler characteristic)",
            "All Standard Model parameters derive from geometric topology"
        ],
        next_section="2",
    ),

    "2": SectionMetadata(
        id="2",
        title="Geometric Framework",
        section_type="section",
        abstract="We establish the dimensional structure through successive reductions: 26D → 13D (Sp(2,R) gauge fixing) → 6D (G₂ compactification) → 4D + 3 shadow branes. The G₂ manifold TCS #187 with χ_eff = 144, b₂ = 4, b₃ = 24 determines all topological observables.",
        section_file="sections/geometric-framework.html",
        beginner_summary="The math behind the dimensional reduction. Like how a 3D object casts a 2D shadow, our 26D space projects down to create the 4D universe we experience.",
        key_takeaways=[
            "Dimensional reduction: 26D → 13D → 6D → 4D",
            "G₂ holonomy preserves exactly 1 supersymmetry (needed for stability)",
            "Euler characteristic χ_eff = 144 fixes n_gen = 3",
            "Betti numbers (b₂=4, b₃=24) control gauge sector and CP violation",
            "TCS manifold #187 selected by flux quantization and tadpole cancellation"
        ],
        prev_section="1",
        next_section="3",
    ),

    "3": SectionMetadata(
        id="3",
        title="Fermion Sector",
        section_type="section",
        abstract="Fermion masses and mixings arise from G₂ cycle intersections and Yukawa overlaps. The geometric Froggatt-Nielsen mechanism with ε = exp(-λ) ≈ 0.223 reproduces the observed mass hierarchies. CP violation emerges from H₃(G₂,Z) cycle orientations.",
        section_file="sections/fermion-sector.html",
        beginner_summary="How particle masses (electron, quark masses) come from geometry. Different particles 'live' at different positions in the folded dimensions, which determines their mass.",
        key_takeaways=[
            "Three generations from χ_eff/48 = 144/48 = 3",
            "Mass hierarchies from geometric Froggatt-Nielsen: Y_f ∝ ε^Q_f",
            "Cabibbo angle ε ≈ 0.223 derived from G₂ curvature scale λ = 1.5",
            "Neutrino masses from G₂ volume modulus: m_ν ∝ exp(-b₃/(8π)) ≈ 0.05 eV",
            "CP phases from cycle orientations: δ_CP ∝ π × (orientation sum) / b₃"
        ],
        prev_section="2",
        next_section="4",
    ),

    "4": SectionMetadata(
        id="4",
        title="Gauge Unification",
        section_type="section",
        abstract="The Standard Model gauge group SU(3)×SU(2)×U(1) unifies into SO(10) at M_GUT = 2.118×10¹⁶ GeV via G₂ discrete torsion. Doublet-triplet splitting arises from TCS cycle topology, and proton decay lifetime τ_p = 8.15×10³⁴ years satisfies Super-Kamiokande bounds.",
        section_file="sections/gauge-unification.html",
        beginner_summary="At very high energies, the three fundamental forces (strong, weak, electromagnetic) merge into one. We calculate when and how this happens from pure geometry.",
        key_takeaways=[
            "GUT scale M_GUT = 2.118×10¹⁶ GeV from G₂ torsion class Z₂×Z₂",
            "Gauge coupling unification: α_GUT⁻¹ = 23.54 at M_GUT",
            "Doublet-triplet splitting via TCS discrete torsion (b₂=4 cycles)",
            "Proton lifetime τ_p = 8.15×10³⁴ years (4.9× Super-K bound)",
            "Breaking chain: SO(10) → Pati-Salam SU(4)×SU(2)×SU(2) → SM"
        ],
        prev_section="3",
        next_section="5",
    ),

    "5": SectionMetadata(
        id="5",
        title="Cosmology and Predictions",
        section_type="section",
        abstract="The Pneuma field φ_P provides dark energy with equation of state w = -0.998, matching DESI DR2 data. KK gravitons with M_KK = 5.0 TeV are accessible at HL-LHC. Testable signatures include modified gravitational wave dispersion and CMB bubble collision imprints.",
        section_file="sections/predictions.html",
        beginner_summary="What experiments can test this theory. We predict specific particle masses and subtle effects in gravitational waves that future telescopes and colliders can detect.",
        key_takeaways=[
            "Dark energy from Pneuma field: w₀ = -0.998 ± 0.002 (matches DESI)",
            "KK graviton mass M_KK = 5.0 TeV (HL-LHC reach: 7 TeV)",
            "Modified GW dispersion: v_gw/c - 1 ∝ (E/M_Pl)² × O(10⁻²)",
            "Neutrino mass sum Σm_ν = 0.060 eV (within Planck+DESI bound)",
            "CMB bubble collisions from pre-inflation multiverse structure"
        ],
        prev_section="4",
        next_section="6",
    ),

    "6": SectionMetadata(
        id="6",
        title="Conclusion",
        section_type="section",
        abstract="The Principia Metaphysica framework demonstrates that Standard Model parameters and beyond-SM predictions can emerge from pure geometry. With 14 predictions vs 6 input parameters, the framework achieves a 2.3:1 prediction-to-input ratio and is testable at HL-LHC and next-generation gravitational wave observatories.",
        section_file="sections/conclusion.html",
        beginner_summary="Summary of results and what comes next. The framework makes concrete predictions that can be tested in the next 5-10 years.",
        key_takeaways=[
            "14 predictions from 6 input parameters (2.3:1 ratio)",
            "Zero tunable parameters - all observables from topology",
            "Testable at HL-LHC (2027+) and LISA/Einstein Telescope (2030s)",
            "Resolves gauge hierarchy, strong CP, and cosmological constant problems",
            "Provides geometric unification without supersymmetry at low scales"
        ],
        prev_section="5",
    ),
}


def get_section_dict():
    """Export section registry as dictionary for JSON serialization."""
    return {
        section_id: section.to_dict()
        for section_id, section in SECTION_REGISTRY.items()
    }
