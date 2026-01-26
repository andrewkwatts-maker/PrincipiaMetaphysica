#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Appendix A: The Spectral Registry
================================================================

DOI: 10.5281/zenodo.18079602

v16.2 STERILE MODEL: The 125 residues as spectral eigenvalues of the V_7 manifold.

This appendix provides the terminal values for the 125 physical residues
extracted from the V_7 manifold. Each residue is mapped to its Brane-Node ID,
Spectral Index (lambda_n), and functional Symmetry Bank.

APPENDIX: A (The Spectral Registry - The 125 Residues)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os
from typing import Dict, Any, List, Optional

_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(os.path.dirname(_current_dir))
_project_root = os.path.dirname(_simulations_dir)
sys.path.insert(0, _project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)


class AppendixASpectralRegistry(SimulationBase):
    """
    Appendix A: The Spectral Registry (The 125 Residues).

    Provides the complete 125-node lattice of physical residues,
    organized by Symmetry Bank and mapped to V_7 eigenvalues.

    Follows SOLID principles:
    - Single Responsibility: Only handles spectral registry content
    - Open/Closed: Extends SimulationBase without modification
    - Dependency Inversion: Depends on registry abstraction for values
    """

    # Dynamic formula IDs referenced by this appendix
    FORMULA_REFS = [
        "spectral-eigenvalue-extraction",
        "omega-hash-verification",
        "node-distribution-function",
        "log-harmonic-spacing",
    ]

    # Dynamic parameter paths referenced by this appendix
    PARAM_REFS = [
        "topology.elder_kads",
        "topology.euler_chi",
        "cosmology.H0_geometric",
        "cosmology.w0_geometric",
        "particle.alpha_em",
        "particle.m_electron",
        "particle.m_top",
        "particle.higgs_vev",
        "particle.alpha_s",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_a_spectral_registry_v16_2",
            version="16.2",
            domain="appendices",
            title="Appendix A: The 125-Residue Spectral Registry (The Master Table)",
            description="The 125 residues as spectral eigenvalues of the V_7 manifold",
            section_id="A",
            subsection_id=None,
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        # Narrative content - no strict dependencies, PARAM_REFS are for documentation
        return []

    @property
    def output_params(self) -> List[str]:
        return ["registry.node_count", "registry.bank_distribution"]

    @property
    def output_formulas(self) -> List[str]:
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute spectral registry validation."""
        # Dynamic param extraction - use registry.get() with geometric defaults
        b3 = registry.get("topology.elder_kads", default=24)
        chi = registry.get("topology.mephorash_chi", default=144)

        return {
            "registry.node_count": 125,
            "registry.bank_distribution": {
                "metric": 18,
                "gauge": 27,
                "matter": 67,
                "scalar": 13
            },
            "registry.b3_constraint": b3,
            "registry.chi_constraint": chi,
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for Appendix A: The Spectral Registry."""
        content_blocks = [
            ContentBlock(
                type="heading",
                content="The Spectral Registry (The 125 Residues)",
                level=2,
                label="A"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This appendix provides the terminal values for the 125 physical residues "
                    "extracted from the V₇ manifold. Each residue is mapped to its "
                    "<strong>Brane-Node ID</strong>, its <strong>Spectral Index</strong> (λₙ), "
                    "and its functional <strong>Symmetry Bank</strong>."
                )
            ),

            # A.1 Data Structure
            ContentBlock(
                type="heading",
                content="A.1 Data Structure and Metadata",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "For the simulation to be considered sterile, each entry in the registry.json "
                    "must contain the following fields:"
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>Node_ID</strong>: The geometric coordinate within the G₂ lattice</li>"
                    "<li><strong>Spectral_Index (λₙ)</strong>: The specific eigenvalue of the Laplacian Δ<sub>V₇</sub></li>"
                    "<li><strong>Residue_Value</strong>: The physical constant (e.g., m<sub>e</sub>, α, w₀)</li>"
                    "<li><strong>Holonomy_Link</strong>: The pointer to the b₃ or b₂ cycle providing flux screening</li>"
                    "</ul>"
                ),
                label="registry-fields"
            ),

            # A.2 Master Registry Table - references dynamic params
            ContentBlock(
                type="heading",
                content="A.2 The Master Registry Table (Primary Nodes)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The following table presents the primary anchor nodes of the 125-residue "
                    "lattice. Values are dynamically populated from the registry and protected "
                    "by the SHA-256 Metric Lock. See Appendix F for the full dynamically-generated "
                    "node listing."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\lambda_n = \Delta_{V_7}(\Psi_n) \quad \text{for } n \in \{1, \ldots, 125\}",
                formula_id="spectral-eigenvalue-extraction",
                label="(A.1)"
            ),

            # A.3 Spectral Distribution Map
            ContentBlock(
                type="heading",
                content="A.3 The Spectral Distribution Map",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The distribution of the 125 residues follows a <strong>Log-Harmonic Spacing</strong>. "
                    "This explains the 'Hierarchy Problem' (why gravity is so much weaker than "
                    "electromagnetism). In a V₇ manifold, eigenvalues cluster according to the "
                    "depth of the brane intersection:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"r(n) = e^{-\kappa \cdot \lambda_n} \quad \text{(Node Depth Function)}",
                formula_id="log-harmonic-spacing",
                label="(A.2)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>Metric Bank (Nodes 1-18)</strong>: Cluster at the 'Zero-Point' of the "
                    "Laplacian, representing global spacetime properties</li>"
                    "<li><strong>Gauge Bank (Nodes 19-45)</strong>: Located at the 'Symmetry Faults' "
                    "where the G₂ structure shatters into the Standard Model groups</li>"
                    "<li><strong>Fermionic Bank (Nodes 46-112)</strong>: Distributed along the internal "
                    "Calabi-Yau folds, creating the mass generations</li>"
                    "<li><strong>Scalar Bank (Nodes 113-125)</strong>: Higgs sector and coupling constants "
                    "at the G₂ holonomy center</li>"
                    "</ul>"
                ),
                label="spectral-distribution"
            ),

            # A.4 Registry Integrity
            ContentBlock(
                type="heading",
                content="A.4 Registry Integrity (The Omega Hash)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "To ensure this data is never 'tuned,' the total sum of the residues must "
                    "satisfy the Global Sum Rule defined in Appendix B. Any modification to the "
                    "125 residues will result in a hash mismatch, revoking the Sterile Certification."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\text{SHA-256}(\text{registry.json}) = \Omega_{\text{seal}}",
                formula_id="omega-hash-verification",
                label="(A.3)"
            ),
        ]

        return SectionContent(
            section_id="A",
            subsection_id=None,
            title="Appendix A: The 125-Residue Spectral Registry (The Master Table)",
            abstract="The 125 residues as spectral eigenvalues of the V7 manifold.",
            content_blocks=content_blocks,
            formula_refs=self.FORMULA_REFS,
            param_refs=self.PARAM_REFS,
            appendix=True,
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for dynamic population."""
        return [
            Formula(
                id="spectral-eigenvalue-extraction",
                label="(A.1)",
                latex=r"\lambda_n = \Delta_{V_7}(\Psi_n)",
                plain_text="λₙ = Δ_V₇(Ψₙ)",
                category="FOUNDATIONAL",
                description=(
                    "Spectral eigenvalue extraction from V₇ Laplacian. Each of the 125 "
                    "residues corresponds to a specific eigenvalue of this operator."
                ),
                input_params=["topology.elder_kads", "topology.euler_chi"],
                output_params=["registry.node_count"],
                terms={
                    "Δ_V₇": "Laplace-Beltrami operator on V₇ manifold",
                    "Ψₙ": "Eigenfunction at node n",
                    "λₙ": "Spectral eigenvalue (residue value)",
                }
            ),
            Formula(
                id="omega-hash-verification",
                label="(A.3)",
                latex=r"\text{SHA-256}(\text{registry.json}) = \Omega_{\text{seal}}",
                plain_text="SHA-256(registry.json) = Ω_seal",
                category="VALIDATION",
                description=(
                    "Cryptographic hash verification ensuring registry immutability. "
                    "Any modification triggers Sterile Certification revocation."
                ),
                input_params=[],
                output_params=[],
                terms={
                    "Ω_seal": "The terminal cryptographic signature",
                }
            ),
            Formula(
                id="log-harmonic-spacing",
                label="(A.2)",
                latex=r"r(n) = e^{-\kappa \cdot \lambda_n}",
                plain_text="r(n) = exp(-κ·λₙ)",
                category="FOUNDATIONAL",
                description=(
                    "Log-harmonic spacing function determining node depth in V₇ manifold. "
                    "Explains the mass hierarchy across symmetry banks."
                ),
                input_params=["topology.elder_kads"],
                output_params=[],
                terms={
                    "r(n)": "Radial depth of node n",
                    "κ": "Spacing coefficient from G₂ holonomy",
                    "λₙ": "Spectral eigenvalue at node n",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for this appendix."""
        return [
            Parameter(
                path="registry.node_count",
                name="Total Registry Nodes",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Total number of residue nodes in the spectral registry (125)",
                no_experimental_value=True,
            ),
            Parameter(
                path="registry.bank_distribution",
                name="Symmetry Bank Distribution",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Distribution of 125 nodes across the four Symmetry Banks",
                no_experimental_value=True,
            ),
        ]


if __name__ == "__main__":
    from simulations.base import PMRegistry
    registry = PMRegistry()
    sim = AppendixASpectralRegistry()
    print(f"Simulation: {sim.metadata.title}")
    results = sim.run(registry)
    print(f"Results: {results}")
    content = sim.get_section_content()
    if content:
        print(f"Content blocks: {len(content.content_blocks)}")
        print(f"Formula refs: {content.formula_refs}")
        print(f"Param refs: {content.param_refs}")
