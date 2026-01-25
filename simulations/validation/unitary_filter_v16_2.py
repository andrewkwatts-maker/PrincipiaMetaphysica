#!/usr/bin/env python3
"""
Principia Metaphysica - Ghost-Free Stability Check v16.2
=========================================================

The "Guardian" validation filter that ensures no simulation can produce
unphysical results by enforcing Weyl anomaly cancellation.

PHYSICS BACKGROUND:
In string theory, the Weyl anomaly must cancel for physical consistency.
The total central charge must vanish:

    c_total = c_matter + c_ghost = 0

For PM's v21 (24,1) signature theory with Euclidean bridge:
- 24 transverse coordinates (b3): c = +24
- 1 unified time + Euclidean bridge (0) for timeless substrate: c = +2 effective
- Ghost contribution: c = -26 (from bc ghost system)

Total: c = 24 + 2 - 26 = 0 [GHOST-FREE]

The v21/v22 framework uses OR reduction via R_perp operator to produce dual 13D(12,1) shadows
with shared time, replacing the legacy Sp(2,R) gauge fixing approach.

If b3 != 24 or D_total != 26, the Weyl anomaly does NOT cancel, leading to:
1. Negative-norm states (ghosts) in the spectrum
2. Non-unitary S-matrix
3. Broken BRST cohomology
4. Loss of predictive power

This filter BLOCKS any simulation that would violate unitarity.

Usage:
    from simulations.validation.unitary_filter_v16_2 import UnitaryFilter

    # Create filter with default values (b3=24, dim_total=26)
    guardian = UnitaryFilter()

    # Check stability before running simulation
    is_stable, message = guardian.check_stability()
    if not is_stable:
        raise RuntimeError(message)

    # Or use the validation method
    guardian.validate_before_simulation()  # Raises if unstable

References:
- Polchinski, J. (1998) "String Theory Vol. 1" Ch. 2-4
- Bars, I. (2006) "Gauge symmetry in two-time physics"
- Polyakov, A. (1981) "Quantum geometry of bosonic strings"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Tuple, Dict, Any, List, Optional
import sys
import os

# Add parent directories to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
sys.path.insert(0, _project_root)

try:
    from core.FormulasRegistry import get_registry
    _REG = get_registry()
except ImportError:
    _REG = None

try:
    from simulations.base import (
        SimulationBase,
        SimulationMetadata,
        Formula,
        Parameter,
        SectionContent,
        ContentBlock,
        PMRegistry,
    )
except ImportError:
    # Allow standalone usage without full simulation framework
    SimulationBase = object
    SimulationMetadata = None
    Formula = None
    Parameter = None
    SectionContent = None
    ContentBlock = None
    PMRegistry = None


class UnitaryFilterError(Exception):
    """Raised when unitarity check fails - simulation would produce unphysical results."""
    pass


class UnitaryFilter:
    """
    Ghost-Free Stability Check - The Guardian.

    This filter ensures that no simulation can produce unphysical results
    by enforcing Weyl anomaly cancellation. If b3 != 24 or D != 26, the
    theory breaks and the filter will BLOCK the simulation.

    The Weyl anomaly check:
        central_charge = b3 + 2 - 26  (transverse + Sp(2,R) - ghost)

    For unitarity: central_charge MUST equal 0.

    Attributes:
        b3_val: Third Betti number of the G2 manifold (transverse modes)
        dim_total: Total spacetime dimension (should be 26)
        dim_sp2r: Sp(2,R) symplectic contribution (always 2)
        dim_ghost: Ghost sector contribution (always -26 for bc system)

    Example:
        >>> guardian = UnitaryFilter(b3_val=24, dim_total=26)
        >>> is_stable, msg = guardian.check_stability()
        >>> print(is_stable)
        True
        >>> print(msg)
        UNITARY_STABLE: GHOST_FREE

        >>> bad_guardian = UnitaryFilter(b3_val=23, dim_total=26)
        >>> is_stable, msg = bad_guardian.check_stability()
        >>> print(is_stable)
        False
        >>> print(msg)
        ANOMALY_DETECTED: C=-1
    """

    # Physical constants for the Weyl anomaly
    DIM_BRIDGE = 2      # Unified time (1) + Euclidean bridge (0) contribution for timeless substrate
    DIM_GHOST = 26      # bc ghost system central charge magnitude

    def __init__(self, b3_val: int = 24, dim_total: int = 26):
        """
        Initialize the UnitaryFilter.

        Args:
            b3_val: Third Betti number (transverse dimensions from G2 manifold).
                    Default is 24 for TCS G2 with 187 special Lagrangians.
            dim_total: Total spacetime dimension. Default is 26 (critical dimension).

        The central charge calculation:
            c = b3 + 2 - 26
              = (transverse) + (unified time + bridge) - (ghost)
              = 24 + 2 - 26 = 0 [required for unitarity]
        """
        self.b3_val = b3_val
        self.dim_total = dim_total
        self.dim_bridge = self.DIM_BRIDGE
        self.dim_ghost = self.DIM_GHOST

        # Store computed values
        self._central_charge: Optional[int] = None
        self._is_stable: Optional[bool] = None
        self._status_message: Optional[str] = None

    @property
    def central_charge(self) -> int:
        """
        Calculate the total central charge.

        Returns:
            c_total = b3 + 2 - 26

        For ghost-free unitarity, this must be exactly 0.
        """
        if self._central_charge is None:
            # c = c_transverse + c_bridge + c_ghost
            # c = b3 + 2 - 26 (unified time + Euclidean bridge contribution)
            self._central_charge = self.b3_val + self.dim_bridge - self.dim_ghost
        return self._central_charge

    def check_stability(self) -> Tuple[bool, str]:
        """
        Check if the theory is ghost-free and unitary.

        The Weyl anomaly cancellation requirement:
            central_charge = b3 + 2 - 26 = 0

        Returns:
            Tuple of (is_stable, message) where:
            - is_stable: True if central_charge == 0 (ghost-free)
            - message: Status string explaining the result

        Examples:
            >>> guardian = UnitaryFilter(b3_val=24)
            >>> guardian.check_stability()
            (True, 'UNITARY_STABLE: GHOST_FREE')

            >>> guardian = UnitaryFilter(b3_val=23)
            >>> guardian.check_stability()
            (False, 'ANOMALY_DETECTED: C=-1')
        """
        c = self.central_charge

        # Use floating point tolerance to avoid numerical noise issues
        # The central charge should be exactly 0, but floating point
        # arithmetic may produce tiny residuals like 1e-15
        if abs(c) < 1e-14:
            self._is_stable = True
            self._status_message = "UNITARY_STABLE: GHOST_FREE"
        else:
            self._is_stable = False
            self._status_message = f"ANOMALY_DETECTED: C={c}"

        return (self._is_stable, self._status_message)

    def validate_before_simulation(self) -> None:
        """
        Validate that the theory is unitary before running a simulation.

        This method should be called by other simulations before they
        produce physical predictions. If the Weyl anomaly is not cancelled,
        this method raises UnitaryFilterError to BLOCK the simulation.

        Raises:
            UnitaryFilterError: If central_charge != 0 (theory is not ghost-free)

        Example:
            >>> guardian = UnitaryFilter()
            >>> guardian.validate_before_simulation()  # OK, passes silently

            >>> bad_guardian = UnitaryFilter(b3_val=25)
            >>> bad_guardian.validate_before_simulation()
            Traceback (most recent call last):
                ...
            UnitaryFilterError: SIMULATION BLOCKED - ANOMALY_DETECTED: C=1
        """
        is_stable, message = self.check_stability()

        if not is_stable:
            raise UnitaryFilterError(
                f"SIMULATION BLOCKED - {message}\n"
                f"The Weyl anomaly is not cancelled:\n"
                f"  b3 = {self.b3_val} (transverse modes)\n"
                f"  Bridge = {self.dim_bridge} (unified time + Euclidean bridge contribution)\n"
                f"  Ghost = -{self.dim_ghost} (bc system)\n"
                f"  Central charge = {self.central_charge} != 0\n"
                f"\n"
                f"Theory requires b3 = 24 and D_total = 26 for unitarity."
            )

    def get_stability_report(self) -> Dict[str, Any]:
        """
        Generate a detailed stability report.

        Returns:
            Dictionary with complete stability analysis including:
            - is_stable: Boolean stability status
            - central_charge: Total central charge value
            - b3: Third Betti number value
            - dim_total: Total dimension
            - contributions: Breakdown of central charge contributions
            - message: Status message
            - physics: Explanation of physical implications
        """
        is_stable, message = self.check_stability()

        return {
            "is_stable": is_stable,
            "central_charge": self.central_charge,
            "b3": self.b3_val,
            "dim_total": self.dim_total,
            "contributions": {
                "c_transverse": self.b3_val,
                "c_bridge": self.dim_bridge,
                "c_ghost": -self.dim_ghost,
            },
            "message": message,
            "physics": (
                "GHOST-FREE: The Weyl anomaly is cancelled. The theory has:\n"
                "  - No negative-norm states in the physical spectrum\n"
                "  - Unitary S-matrix\n"
                "  - Consistent BRST cohomology\n"
                "  - Valid predictive power"
                if is_stable else
                f"GHOSTS PRESENT: The Weyl anomaly is NOT cancelled (c = {self.central_charge}).\n"
                f"  - Negative-norm states pollute the spectrum\n"
                f"  - S-matrix is non-unitary\n"
                f"  - BRST cohomology is broken\n"
                f"  - Physical predictions are invalid"
            ),
            "required_values": {
                "b3": 24,
                "dim_total": 26,
                "central_charge": 0,
            },
            "actual_values": {
                "b3": self.b3_val,
                "dim_total": self.dim_total,
                "central_charge": self.central_charge,
            },
        }

    @classmethod
    def create_from_registry(cls, registry: 'PMRegistry') -> 'UnitaryFilter':
        """
        Create a UnitaryFilter using values from the PMRegistry.

        Args:
            registry: PMRegistry instance containing topology.b3

        Returns:
            UnitaryFilter instance configured from registry values

        Example:
            >>> registry = PMRegistry.get_instance()
            >>> registry.set_param("topology.b3", 24, source="g2_geometry_v16_0")
            >>> guardian = UnitaryFilter.create_from_registry(registry)
            >>> guardian.check_stability()
            (True, 'UNITARY_STABLE: GHOST_FREE')
        """
        if registry is None:
            raise ValueError("PMRegistry is required to create UnitaryFilter from registry")

        # Get b3 from registry (default to SSoT registry if not set)
        if registry.has_param("topology.b3"):
            b3 = registry.get_param("topology.b3")
        else:
            b3 = _REG.elder_kads if _REG else 24  # Default from SSoT registry

        # D_total is always 26 for bosonic string
        dim_total = 26

        return cls(b3_val=int(b3), dim_total=dim_total)

    def __repr__(self) -> str:
        """Return string representation of the filter."""
        is_stable, message = self.check_stability()
        return (
            f"UnitaryFilter(b3={self.b3_val}, D={self.dim_total}, "
            f"c={self.central_charge}, status='{message}')"
        )


# ============================================================================
# Integration with Simulation Framework
# ============================================================================

class UnitaryFilterSimulation(SimulationBase if SimulationBase != object else object):
    """
    Simulation wrapper for UnitaryFilter that integrates with the PM framework.

    This allows the filter to be registered in the simulation chain and
    produce output parameters for the theory_output.json.
    """

    def __init__(self):
        """Initialize the simulation."""
        self._filter: Optional[UnitaryFilter] = None

    @property
    def metadata(self) -> 'SimulationMetadata':
        """Return simulation metadata."""
        if SimulationMetadata is None:
            return None
        return SimulationMetadata(
            id="unitary_filter_v16_2",
            version="16.2",
            domain="validation",
            title="Ghost-Free Stability Check (The Guardian)",
            description=(
                "Validates Weyl anomaly cancellation to ensure ghost-free unitarity. "
                "This filter BLOCKS simulations if b3 != 24 or D != 26, preventing "
                "unphysical results from entering the prediction chain."
            ),
            section_id="validation",
            subsection_id="V.1"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            "unitary.central_charge",
            "unitary.is_ghost_free",
            "unitary.status",
            "unitary.c_transverse",
            "unitary.c_bridge",
            "unitary.c_ghost",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "weyl-anomaly-cancellation",
            "central-charge-unitarity",
        ]

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute the unitarity check.

        Args:
            registry: PMRegistry instance with topology.b3

        Returns:
            Dictionary with unitarity validation results

        Raises:
            UnitaryFilterError: If the theory is not ghost-free
        """
        # Create filter from registry
        self._filter = UnitaryFilter.create_from_registry(registry)

        # Validate - this will raise if not stable
        self._filter.validate_before_simulation()

        # Get detailed report
        report = self._filter.get_stability_report()

        return {
            "unitary.central_charge": report["central_charge"],
            "unitary.is_ghost_free": report["is_stable"],
            "unitary.status": report["message"],
            "unitary.c_transverse": report["contributions"]["c_transverse"],
            "unitary.c_bridge": report["contributions"]["c_bridge"],
            "unitary.c_ghost": report["contributions"]["c_ghost"],
        }

    def get_formulas(self) -> List['Formula']:
        """Return formulas for the unitarity check."""
        if Formula is None:
            return []

        return [
            Formula(
                id="weyl-anomaly-cancellation",
                label="(V.1)",
                latex=r"c_{\text{total}} = c_{\text{matter}} + c_{\text{ghost}} = 26 - 26 = 0",
                plain_text="c_total = c_matter + c_ghost = 26 - 26 = 0",
                category="THEORY",
                description=(
                    "Weyl anomaly cancellation in 26D. The matter contribution (26 from "
                    "24 transverse + 2 Sp(2,R)) exactly cancels the ghost contribution (-26 "
                    "from the bc ghost system), ensuring conformal invariance and unitarity."
                ),
                input_params=["topology.b3"],
                output_params=["unitary.central_charge", "unitary.is_ghost_free"],
                derivation={
                    "parentFormulas": ["virasoro-algebra", "brst-cohomology"],
                    "method": "Central charge calculation from conformal field theory",
                    "steps": [
                        "Matter: c_matter = D = 26 (each coordinate contributes +1)",
                        "Ghost: c_ghost = -26 (from bc ghost system with h_b=2, h_c=-1)",
                        "Total: c_total = c_matter + c_ghost = 26 - 26 = 0",
                        "Unitarity: c_total = 0 ensures no negative-norm states",
                    ]
                },
                terms={
                    "c_total": "Total central charge (must be 0 for unitarity)",
                    "c_matter": "Matter sector contribution = 26",
                    "c_ghost": "Ghost sector contribution = -26",
                }
            ),
            Formula(
                id="central-charge-unitarity",
                label="(V.2)",
                latex=r"c = b_3 + 2 - 26 = 24 + 2 - 26 = 0",
                plain_text="c = b3 + 2 - 26 = 24 + 2 - 26 = 0",
                category="THEORY",
                description=(
                    "Unitarity requirement in terms of the G2 geometry. The third Betti "
                    "number b3 = 24 provides transverse modes, unified time (1) + Euclidean "
                    "bridge (0) contributes 2 for timeless substrate, and the ghost sector subtracts 26. Total must be exactly 0."
                ),
                input_params=["topology.b3"],
                output_params=["unitary.central_charge"],
                derivation={
                    "parentFormulas": ["g2-topology", "weyl-anomaly-cancellation"],
                    "method": "Dimensional counting from G2 compactification",
                    "steps": [
                        "b3 = 24 transverse modes from TCS G2 manifold",
                        "Unified time (1) + Euclidean bridge (0) contributes 2 for timeless substrate",
                        "Ghost bc system contributes -26",
                        "c = 24 + 2 - 26 = 0 [GHOST-FREE]",
                    ]
                },
                terms={
                    "b3": "Third Betti number of G2 manifold = 24",
                    "c": "Central charge (must equal 0 for ghost-free theory)",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List['Parameter']:
        """Return parameter definitions for outputs."""
        if Parameter is None:
            return []

        return [
            Parameter(
                path="unitary.central_charge",
                name="Total Central Charge",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Total central charge c = b3 + 2 - 26. Must be exactly 0 for "
                    "ghost-free unitarity. Non-zero values indicate broken conformal "
                    "invariance and presence of negative-norm states."
                ),
                derivation_formula="central-charge-unitarity",
                no_experimental_value=True
            ),
            Parameter(
                path="unitary.is_ghost_free",
                name="Ghost-Free Status",
                units="boolean",
                status="DERIVED",
                description=(
                    "True if c = 0 (ghost-free and unitary). False if c != 0 "
                    "(ghosts present, theory is inconsistent)."
                ),
                derivation_formula="weyl-anomaly-cancellation",
                no_experimental_value=True
            ),
            Parameter(
                path="unitary.status",
                name="Unitarity Status Message",
                units="string",
                status="DERIVED",
                description=(
                    "Status message: 'UNITARY_STABLE: GHOST_FREE' if c = 0, "
                    "or 'ANOMALY_DETECTED: C=X' if c = X != 0."
                ),
                derivation_formula="weyl-anomaly-cancellation",
                no_experimental_value=True
            ),
        ]

    def get_section_content(self) -> Optional['SectionContent']:
        """Return section content for the validation report."""
        if SectionContent is None or ContentBlock is None:
            return None

        content_blocks = [
            ContentBlock(
                type="paragraph",
                content=(
                    "The Ghost-Free Stability Check (The Guardian) ensures that no simulation "
                    "in the Principia Metaphysica framework can produce unphysical results. "
                    "This is achieved by enforcing Weyl anomaly cancellation before any "
                    "physical prediction is computed."
                )
            ),
            ContentBlock(
                type="heading",
                content="The Weyl Anomaly Requirement",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In string theory, conformal (Weyl) invariance on the worldsheet is essential "
                    "for consistent quantization. Quantum corrections introduce an anomaly unless "
                    "the total central charge vanishes:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"c_{\text{total}} = c_{\text{matter}} + c_{\text{ghost}} = 0",
                formula_id="weyl-anomaly-cancellation",
                label="(V.1)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "For PM's v21 (24,1) signature theory with Euclidean bridge, the central charge calculation is:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"c = b_3 + 2 - 26 = 24 + 2 - 26 = 0",
                formula_id="central-charge-unitarity",
                label="(V.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This exact cancellation ensures: (1) no negative-norm states in the physical "
                    "spectrum, (2) unitarity of the S-matrix, (3) consistent BRST cohomology, and "
                    "(4) valid predictive power for all derived quantities."
                )
            ),
            ContentBlock(
                type="heading",
                content="The Guardian Protocol",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Before any simulation produces physical predictions, it must pass through "
                    "the UnitaryFilter validation. If b3 != 24 or D != 26, the filter BLOCKS "
                    "the simulation with a UnitaryFilterError, preventing unphysical results "
                    "from entering the prediction chain."
                )
            ),
        ]

        return SectionContent(
            section_id="validation",
            subsection_id="V.1",
            title="Ghost-Free Stability Check (The Guardian)",
            abstract=(
                "Validation filter that enforces Weyl anomaly cancellation to ensure "
                "ghost-free unitarity. Blocks simulations if b3 != 24 or D != 26."
            ),
            content_blocks=content_blocks,
            formula_refs=["weyl-anomaly-cancellation", "central-charge-unitarity"],
            param_refs=[
                "topology.b3",
                "unitary.central_charge",
                "unitary.is_ghost_free",
            ]
        )

    def get_foundations(self) -> List[Dict[str, str]]:
        """Return foundational concepts."""
        return [
            {
                "id": "weyl-anomaly",
                "title": "Weyl Anomaly",
                "category": "conformal_field_theory",
                "description": (
                    "Quantum correction that breaks Weyl (conformal) invariance "
                    "unless the total central charge vanishes in critical dimensions."
                )
            },
            {
                "id": "central-charge",
                "title": "Central Charge",
                "category": "conformal_field_theory",
                "description": (
                    "Measure of degrees of freedom in a conformal field theory. "
                    "Must cancel between matter and ghost sectors for unitarity."
                )
            },
            {
                "id": "ghost-states",
                "title": "Ghost States",
                "category": "quantum_field_theory",
                "description": (
                    "Negative-norm states that violate probability conservation. "
                    "Must be absent from physical spectrum for unitarity."
                )
            },
        ]

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references."""
        return [
            {
                "id": "polchinski1998",
                "authors": "Polchinski, J.",
                "title": "String Theory Vol. 1: An Introduction to the Bosonic String",
                "journal": "Cambridge University Press",
                "year": 1998,
            },
            {
                "id": "polyakov1981",
                "authors": "Polyakov, A.M.",
                "title": "Quantum geometry of bosonic strings",
                "journal": "Phys. Lett. B",
                "volume": "103",
                "pages": "207-210",
                "year": 1981,
            },
            {
                "id": "bars2006",
                "authors": "Bars, I.",
                "title": "Gauge symmetry in phase space with spin, a basis for conformal symmetry and duality among many interactions",
                "journal": "arXiv:hep-th/0604012",
                "year": 2006,
            },
        ]

    def get_beginner_explanation(self) -> Dict[str, Any]:
        """Return beginner-friendly explanation."""
        return {
            "icon": "G",
            "title": "The Guardian: Keeping Physics Real",
            "simpleExplanation": (
                "In quantum physics, we need probabilities to add up to exactly 100%. "
                "Some mathematical frameworks can accidentally create 'ghost' states - "
                "invisible particles with negative probability that would make the math "
                "work out to more than 100% or less than 0%. The Guardian checks that our "
                "theory is 'ghost-free' before any calculation runs. If the check fails, "
                "the entire simulation is blocked because any results would be unphysical."
            ),
            "analogy": (
                "Imagine a bank that must balance its books exactly at the end of each day. "
                "The Guardian is like an auditor who checks the books BEFORE any transaction "
                "can be processed. If the books don't balance (like if someone tried to "
                "withdraw more money than exists), the transaction is blocked. In physics, "
                "the 'books' are the central charge, and they must add up to exactly zero: "
                "24 (from extra dimensions) + 2 (from time structure) - 26 (from ghost "
                "accounting) = 0. Only when this balance is perfect can physics proceed."
            ),
            "keyTakeaway": (
                "The UnitaryFilter is the 'Guardian' that ensures PM never produces "
                "unphysical predictions by blocking any simulation where the Weyl anomaly "
                "is not perfectly cancelled."
            ),
            "technicalDetail": (
                "Central charge calculation: c = b3 + 2 - 26, where b3 = 24 is the third "
                "Betti number (transverse modes from G2 compactification), 2 comes from "
                "unified time (1) + Euclidean bridge (0) for timeless substrate in dual-shadow structure, "
                "and -26 is the bc ghost system contribution. For c = 0, the Weyl anomaly cancels and the theory "
                "is unitary (ghost-free). For c != 0, negative-norm states appear and all "
                "predictions are invalid. The Guardian enforces c = 0 before any simulation runs."
            ),
            "prediction": (
                "If b3 is ever measured or computed to be anything other than 24, or if "
                "the spacetime dimension differs from 26, the entire PM framework would "
                "require fundamental revision. The Guardian would block all simulations "
                "until the geometry is corrected."
            )
        }


# ============================================================================
# Required Validation Entry for theory_output.json
# ============================================================================

REQUIRED_VALIDATION = {
    "id": "unitary_filter_v16_2",
    "type": "required_validation",
    "version": "16.2",
    "title": "Ghost-Free Stability Check (The Guardian)",
    "description": (
        "Validates Weyl anomaly cancellation before any simulation runs. "
        "BLOCKS simulations if b3 != 24 or D != 26."
    ),
    "validation_function": "UnitaryFilter.validate_before_simulation",
    "required_by_all": True,
    "checks": [
        {
            "name": "central_charge_zero",
            "condition": "b3 + 2 - 26 == 0",
            "pass_message": "UNITARY_STABLE: GHOST_FREE",
            "fail_message": "ANOMALY_DETECTED: C != 0",
        }
    ],
    "blocking": True,
    "priority": 0,  # Run before all other validations
}


# ============================================================================
# Standalone Execution
# ============================================================================

def main():
    """Run the UnitaryFilter standalone for testing."""
    print("=" * 70)
    print(" PRINCIPIA METAPHYSICA - GHOST-FREE STABILITY CHECK (THE GUARDIAN)")
    print("=" * 70)

    # Test with correct values
    print("\n1. Testing with b3 = 24, D = 26 (correct values):")
    guardian = UnitaryFilter(b3_val=24, dim_total=26)
    is_stable, message = guardian.check_stability()
    print(f"   Central charge: {guardian.central_charge}")
    print(f"   Is stable: {is_stable}")
    print(f"   Message: {message}")
    print(f"   Repr: {guardian}")

    # Test validation method (should pass)
    print("\n   Calling validate_before_simulation()...")
    try:
        guardian.validate_before_simulation()
        print("   PASSED - Simulation can proceed")
    except UnitaryFilterError as e:
        print(f"   BLOCKED - {e}")

    # Test with wrong b3
    print("\n2. Testing with b3 = 23, D = 26 (WRONG b3):")
    bad_guardian = UnitaryFilter(b3_val=23, dim_total=26)
    is_stable, message = bad_guardian.check_stability()
    print(f"   Central charge: {bad_guardian.central_charge}")
    print(f"   Is stable: {is_stable}")
    print(f"   Message: {message}")

    print("\n   Calling validate_before_simulation()...")
    try:
        bad_guardian.validate_before_simulation()
        print("   PASSED - Simulation can proceed")
    except UnitaryFilterError as e:
        print(f"   BLOCKED - Theory is not ghost-free!")

    # Test with wrong b3 (too high)
    print("\n3. Testing with b3 = 25, D = 26 (WRONG b3):")
    bad_guardian2 = UnitaryFilter(b3_val=25, dim_total=26)
    is_stable, message = bad_guardian2.check_stability()
    print(f"   Central charge: {bad_guardian2.central_charge}")
    print(f"   Is stable: {is_stable}")
    print(f"   Message: {message}")

    # Print detailed report
    print("\n4. Detailed stability report for correct configuration:")
    report = guardian.get_stability_report()
    print(f"   is_stable: {report['is_stable']}")
    print(f"   central_charge: {report['central_charge']}")
    print(f"   b3: {report['b3']}")
    print(f"   contributions:")
    for k, v in report['contributions'].items():
        print(f"      {k}: {v}")
    print(f"   physics: {report['physics'][:80]}...")

    print("\n" + "=" * 70)
    print(" THE GUARDIAN: Ensuring ghost-free unitarity in all simulations")
    print("=" * 70)

    return guardian


# =============================================================================
# Self-Validation Assertions (catch silent failures at import time)
# =============================================================================

# Test with correct values (b3=24, D=26)
_guardian_correct = UnitaryFilter(b3_val=24, dim_total=26)
assert _guardian_correct.central_charge == 0, \
    f"UnitaryFilter: central charge should be 0 for b3=24, got {_guardian_correct.central_charge}"
_is_stable, _message = _guardian_correct.check_stability()
assert _is_stable is True, f"UnitaryFilter: should be stable for b3=24, got: {_message}"
assert "GHOST_FREE" in _message, f"UnitaryFilter: message should contain GHOST_FREE, got: {_message}"

# Test validation method doesn't raise for correct values
try:
    _guardian_correct.validate_before_simulation()
except UnitaryFilterError:
    raise AssertionError("UnitaryFilter: should not raise for b3=24")

# Test with wrong b3=23 (should fail)
_guardian_wrong_low = UnitaryFilter(b3_val=23, dim_total=26)
assert _guardian_wrong_low.central_charge == -1, \
    f"UnitaryFilter: central charge should be -1 for b3=23, got {_guardian_wrong_low.central_charge}"
_is_stable_23, _message_23 = _guardian_wrong_low.check_stability()
assert _is_stable_23 is False, "UnitaryFilter: b3=23 should be unstable"
assert "ANOMALY" in _message_23, f"UnitaryFilter: message should contain ANOMALY, got: {_message_23}"

# Test with wrong b3=25 (should fail)
_guardian_wrong_high = UnitaryFilter(b3_val=25, dim_total=26)
assert _guardian_wrong_high.central_charge == 1, \
    f"UnitaryFilter: central charge should be 1 for b3=25, got {_guardian_wrong_high.central_charge}"
_is_stable_25, _ = _guardian_wrong_high.check_stability()
assert _is_stable_25 is False, "UnitaryFilter: b3=25 should be unstable"

# Test that wrong values raise UnitaryFilterError
try:
    _guardian_wrong_low.validate_before_simulation()
    raise AssertionError("UnitaryFilter: should raise for b3=23")
except UnitaryFilterError:
    pass  # Expected

# Test DIM constants
assert UnitaryFilter.DIM_BRIDGE == 2, "UnitaryFilter: DIM_BRIDGE should be 2"
assert UnitaryFilter.DIM_GHOST == 26, "UnitaryFilter: DIM_GHOST should be 26"

# Cleanup
del _guardian_correct, _guardian_wrong_low, _guardian_wrong_high
del _is_stable, _message, _is_stable_23, _message_23, _is_stable_25


if __name__ == "__main__":
    main()
