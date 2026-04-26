#!/usr/bin/env python3
"""
Appendix T: QEC Golay Bridge — Stabilizer Table & Syndrome Extraction
======================================================================

CLASSIFICATION: DERIVED (CSS construction) + MOTIVATED_IDENTIFICATION (PM mapping)

This appendix expands on the QEC Golay Bridge (qec_golay_bridge.py) with:
1. The full 12×24 stabilizer generator matrix (explicit binary display)
2. A worked syndrome extraction example for single-qubit errors
3. The complete PM-to-QEC mapping table with honest classifications

The CSS [[24,12,8]] code from the self-dual Golay code [24,12,8] is standard
quantum error correction theory. The PM mapping is a MOTIVATED_IDENTIFICATION:
the numerical coincidences (b3=24 → n=24, 12 pairs → k=12) share a common
mathematical root in the Leech lattice but connect different mathematical objects.

References:
- Calderbank, Shor (1996) "Good quantum error-correcting codes exist"
- Steane (1996) "Multiple particle interference and quantum error correction"
- Grassl, Beth, Pellizzari (1997) "Codes for the quantum erasure channel"
- Conway, Sloane (1999) "Sphere Packings, Lattices and Groups"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)
from simulations.PM.algebra.qec_golay_bridge import QECGolayBridge


class AppendixTQECBridge(SimulationBase):
    """
    Appendix T: Expanded QEC bridge with stabilizer table and syndrome extraction.

    Imports the QECGolayBridge and presents:
    - Full 12×24 stabilizer generator matrix
    - Syndrome extraction for single-qubit X, Z, and Y errors
    - Complete mapping table between PM and QEC concepts
    """

    def __init__(self):
        self._bridge = QECGolayBridge()
        self._params = None
        self._stabilizers = None

    # =========================================================================
    # METADATA
    # =========================================================================

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_t_qec_bridge_v24",
            version="24.0",
            domain="appendix",
            title="Appendix T: QEC Bridge Stabilizer Table and Syndrome Extraction",
            description=(
                "Expanded presentation of the CSS [[24,12,8]] quantum error-correcting "
                "code from the self-dual Golay code. Includes explicit stabilizer matrix, "
                "worked syndrome extraction example, and honest PM-to-QEC mapping table."
            ),
            section_id="appendix-T",
            subsection_id=None,
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.elder_kads"]

    @property
    def output_params(self) -> List[str]:
        return [
            "appendix_t.stabilizer_weight_mean",
            "appendix_t.syndrome_example_valid",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return ["syndrome-extraction-formula"]

    # =========================================================================
    # CORE COMPUTATION
    # =========================================================================

    def _ensure_computed(self):
        """Compute stabilizers and parameters if not already done."""
        if self._params is None:
            self._params = self._bridge.compute_code_parameters()
            self._stabilizers = self._bridge.construct_css_stabilizers()

    def format_stabilizer_table(self) -> str:
        """
        Format the 12×24 stabilizer generator matrix as a readable string.

        Each row is a stabilizer generator. A '1' indicates the generator
        acts on that qubit position; '0' means it does not.

        Returns:
            Formatted string representation of the stabilizer matrix.
        """
        self._ensure_computed()
        lines = []
        lines.append("12x24 CSS Stabilizer Generator Matrix (X-type):")
        lines.append("=" * 52)
        lines.append("Gen  |  Qubits 1-12 (parity)  |  Qubits 13-24 (identity)")
        lines.append("-" * 52)

        for i, row in enumerate(self._stabilizers):
            left = "".join(str(int(b)) for b in row[:12])
            right = "".join(str(int(b)) for b in row[12:])
            weight = int(np.sum(row))
            lines.append(f" g{i+1:02d} |  {left}  |  {right}   wt={weight}")

        lines.append("-" * 52)
        weights = [int(np.sum(row)) for row in self._stabilizers]
        lines.append(f"Mean weight: {np.mean(weights):.1f}, All weights: {weights}")

        return "\n".join(lines)

    def syndrome_extraction_example(self, error_qubit: int = 3) -> Dict[str, Any]:
        """
        Demonstrate syndrome extraction for a single-qubit X error.

        For a CSS code, an X error on qubit j produces a Z-syndrome
        that is the j-th column of the Z-stabilizer matrix (= parity check H).

        Args:
            error_qubit: Which qubit has the error (0-indexed, 0-23).

        Returns:
            Dict with error details, syndrome vector, and correction info.
        """
        self._ensure_computed()
        H = self._stabilizers  # 12 x 24

        # Syndrome = H * e_j = j-th column of H
        syndrome = H[:, error_qubit].astype(int)
        syndrome_weight = int(np.sum(syndrome))

        # Check if syndrome is non-zero (error is detectable)
        detectable = syndrome_weight > 0

        # For a distance-8 code, any pattern of <=3 errors has a unique syndrome
        return {
            "error_type": "X",
            "error_qubit": error_qubit,
            "syndrome": syndrome.tolist(),
            "syndrome_weight": syndrome_weight,
            "detectable": detectable,
            "syndrome_binary": "".join(str(b) for b in syndrome),
            "explanation": (
                f"An X error on qubit {error_qubit} produces Z-syndrome "
                f"{''.join(str(b) for b in syndrome)} (weight {syndrome_weight}). "
                f"{'Detectable and correctable.' if detectable else 'NOT detectable (identity column).'} "
                f"The distance d=8 guarantees unique syndromes for all "
                f"error patterns of weight <= 3."
            ),
        }

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute appendix computation."""
        self._ensure_computed()

        weights = [float(np.sum(row)) for row in self._stabilizers]
        syndrome_result = self.syndrome_extraction_example(error_qubit=3)

        return {
            "appendix_t.stabilizer_weight_mean": float(np.mean(weights)),
            "appendix_t.syndrome_example_valid": syndrome_result["detectable"],
        }

    # =========================================================================
    # SECTION CONTENT
    # =========================================================================


    def run_eml(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        EML Math computation path.

        This simulation produces paper outputs. The EML Math representation
        for this module is in the section text via <EML>...</EML> blocks in
        get_section_content(). The computed parameter values are identical
        between Normal Math and EML Math modes.
        """
        return self.run(registry)

    def get_section_content(self) -> Optional[SectionContent]:
        self._ensure_computed()
        stab_table = self.format_stabilizer_table()
        syndrome = self.syndrome_extraction_example(error_qubit=3)
        mapping = self._bridge.get_mapping_table()

        # Format mapping table as text
        mapping_lines = ["PM Concept → QEC Concept [Classification]"]
        mapping_lines.append("-" * 60)
        for m in mapping:
            mapping_lines.append(
                f"  {m['pm_concept']}\n"
                f"    → {m['qec_concept']} [{m['classification']}]\n"
                f"    {m['note'][:120]}..."
            )

        return SectionContent(
            section_id="appendix-T",
            subsection_id=None,
            title="Appendix T: QEC Bridge — Stabilizer Table and Syndrome Extraction",
            abstract=(
                "This appendix presents the full stabilizer generator matrix of the "
                "CSS [[24,12,8]] quantum code constructed from the self-dual extended "
                "Golay code. A worked syndrome extraction example demonstrates error "
                "detection for single-qubit errors. The PM-to-QEC mapping table "
                "documents both motivated identifications and honest mismatches."
            ),
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The CSS [[24,12,8]] code has 12 independent stabilizer generators, "
                        "each acting on a subset of the 24 physical qubits. For the self-dual "
                        "Golay code in systematic form G = [I|B], the stabilizer generators "
                        "are the rows of H = [B^T|I]. The X-type and Z-type stabilizers share "
                        "the same structure due to self-duality, and they commute because "
                        "H * H^T = 0 mod 2."
                    ),
                ),
                ContentBlock(
                    type="paragraph",
                    content=stab_table,
                ),
                ContentBlock(
                    type="formula",
                    content=r"s_i = \langle g_i | e \rangle = H_{ij} \quad \text{(syndrome of X-error on qubit } j\text{)}",
                    formula_id="syndrome-extraction-formula",
                    label="(T.1)",
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        f"Worked Example: {syndrome['explanation']} "
                        f"Syndrome vector: [{syndrome['syndrome_binary']}]."
                    ),
                ),
                ContentBlock(
                    type="callout",
                    callout_type="info",
                    title="PM-to-QEC Mapping Assessment",
                    content=(
                        "The CSS construction is DERIVED (standard mathematics). "
                        "The identification b3=24 -> 24 qubits and 12 pairs -> 12 logical qubits "
                        "is a MOTIVATED_IDENTIFICATION sharing the Leech lattice root. "
                        "Honest MISMATCHES: 42 certificates != 12 stabilizers; "
                        "288 roots != 4096 codewords."
                    ),
                ),
            ],
            formula_refs=["syndrome-extraction-formula"],
            param_refs=["appendix_t.stabilizer_weight_mean", "appendix_t.syndrome_example_valid"],
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="syndrome-extraction-formula",
                label="(T.1)",
                latex=r"s_i = \langle g_i | e \rangle = H_{ij}",
                plain_text="s_i = <g_i | e> = H[i,j] for X-error on qubit j",
                category="DERIVED",
                description=(
                    "Syndrome extraction for CSS code. The syndrome of a single-qubit "
                    "X error on qubit j is the j-th column of the parity check matrix H. "
                    "For the [[24,12,8]] code, all single-qubit errors produce unique "
                    "non-zero syndromes (detectable and correctable up to weight 3)."
                ),
                eml_tree_str="ops.mod(ops.mul(H_row_i, error_vec_j), eml_scalar(2.0))",
                eml_description=(
                    "EML syndrome: s_i = ops.mod(ops.dot(H_row_i, e_j), 2). "
                    "Inner product of i-th stabilizer generator with error vector, mod 2. "
                    "For single-qubit X-error on qubit j, result is j-th column of H."
                ),
                inputParams=["qec.code_n", "qec.code_d"],
                outputParams=["appendix_t.syndrome_example_valid"],
                input_params=["qec.code_n", "qec.code_d"],
                output_params=["appendix_t.syndrome_example_valid"],
                derivation={
                    "method": "css_syndrome_extraction",
                    "steps": [
                        "Construct parity check matrix H = [B^T | I] from Golay generator",
                        "For X-error on qubit j, Z-syndrome is column j of H",
                        "Distance d=8 guarantees unique syndromes for weight <= 3 errors",
                    ],
                },
                terms={
                    "s_i": "i-th syndrome bit (0 or 1)",
                    "g_i": "i-th stabilizer generator",
                    "e": "Error vector (single-qubit X error)",
                    "H": "12x24 parity check matrix",
                },
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="appendix_t.stabilizer_weight_mean",
                name="Mean Stabilizer Weight",
                units="dimensionless",
                status="DERIVED",
                description="Mean Hamming weight of stabilizer generators",
                derivation_formula="syndrome-extraction-formula",
                no_experimental_value=True,
            ),
            Parameter(
                path="appendix_t.syndrome_example_valid",
                name="Syndrome Example Valid",
                units="boolean",
                status="DERIVED",
                description="True if worked syndrome example detects the error",
                derivation_formula="syndrome-extraction-formula",
                no_experimental_value=True,
            ),
        ]

    def get_certificates(self) -> List[Dict[str, Any]]:
        self._ensure_computed()
        syndrome = self.syndrome_extraction_example(error_qubit=3)
        return [
            {
                "id": "CERT_APPENDIX_T_SYNDROME",
                "assertion": f"Single-qubit X error on qubit 3 is detectable: {syndrome['detectable']}",
                "condition": f"syndrome weight = {syndrome['syndrome_weight']} > 0",
                "status": "PASS" if syndrome["detectable"] else "FAIL",
            },
        ]

    def validate_self(self):
        self._ensure_computed()
        syndrome = self.syndrome_extraction_example(error_qubit=3)
        return {
            "checks": [
                {"name": "syndrome_detectable", "passed": syndrome["detectable"], "log_level": "INFO"},
                {"name": "stabilizer_count_12", "passed": len(self._stabilizers) == 12, "log_level": "INFO"},
            ]
        }

    def get_references(self):
        return [
            {
                "id": "calderbank1996",
                "authors": "Calderbank, A.R. and Shor, P.W.",
                "title": "Good quantum error-correcting codes exist",
                "year": 1996,
                "doi": "10.1103/PhysRevA.54.1098",
            },
            {
                "id": "steane1996",
                "authors": "Steane, A.M.",
                "title": "Multiple particle interference and quantum error correction",
                "year": 1996,
                "doi": "10.1098/rspa.1996.0136",
            },
        ]

    def get_learning_materials(self):
        return [
            {
                "topic": "CSS quantum error-correcting codes",
                "url": "https://en.wikipedia.org/wiki/CSS_code",
                "relevance": "Foundation for the [[24,12,8]] code construction",
            },
        ]
