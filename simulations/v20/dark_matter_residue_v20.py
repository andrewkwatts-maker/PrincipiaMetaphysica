#!/usr/bin/env python3
"""
Dark Matter Residue Module v20 - SPECULATIVE PHENOMENOLOGICAL MODEL
====================================================================

STATUS: SPECULATIVE NUMEROLOGY - NOT RIGOROUS PHYSICS
------------------------------------------------------
Per Gemini peer review (2026-01-11), this module presents a SPECULATIVE
phenomenological model with significant caveats:

1. THE 288 STRUCTURE: The 288 = b3 * 12 (24 * 12) represents an octonionic/
   24-dimensional basis structure. It also emerges from "Logic Closure"
   (135 + 153). This is an internal numerological pattern, not gauge theory.

2. KAPPA = 4.25 IS PURE FINE-TUNING: The calibration factor is explicitly
   chosen to match Planck 2018 data (DM/baryon ~ 5.37). This is curve-fitting,
   not derivation from first principles.

3. 125 = 5^3 IS ARBITRARY: The claim that the visible sector has 125 "roots"
   lacks any clear connection to a known gauge group or particle physics.

4. NO PHYSICAL MECHANISM: What particles constitute this "dark matter"? What
   are their masses? Cross-sections? Decay channels? None are specified.

This module should be treated as speculative numerology exploring whether
certain number patterns might correspond to cosmological observations, NOT
as a rigorous derivation of dark matter physics.

Original claims (preserved for context, but DISPUTED):
    The 288 roots partition into:
    - N_visible = 125 (5^3): Matter sector roots (observable particles)
    - N_hidden = 163 (O'Dowd Bulk): Hidden sector roots (dark matter)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import math
import numpy as np
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Import SSOT
try:
    from core.FormulasRegistry import FormulasRegistry as _REG_CLASS
    from core.FormulasRegistry import get_registry
    _REG = get_registry()
except ImportError:
    from ...core.FormulasRegistry import FormulasRegistry as _REG_CLASS
    from ...core.FormulasRegistry import get_registry
    _REG = get_registry()

try:
    from simulations.base import (
        SimulationBase, SimulationMetadata, PMRegistry,
        Formula, Parameter, SectionContent, ContentBlock
    )
except ImportError:
    from ..base import (
        SimulationBase, SimulationMetadata, PMRegistry,
        Formula, Parameter, SectionContent, ContentBlock
    )


@dataclass
class DarkMatterResult:
    """Result of dark matter residue derivation."""
    Omega_DM_derived: float
    Omega_DM_planck: float
    Omega_baryon_derived: float
    Omega_baryon_planck: float
    Omega_matter_total: float
    DM_to_baryon_ratio: float
    DM_to_baryon_planck: float
    volume_ratio_hidden: float  # N_hidden / N_total = 163/288
    volume_ratio_visible: float  # N_visible / N_total = 125/288
    sigma_deviation_DM: float
    sigma_deviation_baryon: float
    status: str  # PASS, MARGINAL, TENSION, FAIL


class DarkMatterResidueV20(SimulationBase):
    """
    v20 Dark Matter Derivation - SPECULATIVE PHENOMENOLOGICAL MODEL.

    WARNING: This is a SPECULATIVE phenomenological model, NOT rigorous physics.

    This module explores a numerological approach to dark matter density,
    using internal numbers (288 = b3 * 12 = 24 * 12, octonionic/24D basis).
    The 288 also emerges from "Logic Closure" (135 + 153). The calibration
    factor kappa = 4.25 is a PHENOMENOLOGICAL FIT to Planck 2018 data.

    Key Numbers (SPECULATIVE - NOT FROM GAUGE THEORY):
        N_total = 288 = b3 * 12 (24 * 12, octonionic/24D basis)
        N_visible = 125 = 5^3 (arbitrary assignment, no gauge theory basis)
        N_hidden = 163 (remainder, claimed as "dark sector")

    The ratio N_hidden/N_total ~ 0.566 is then FITTED via kappa = 4.25
    to approximately match Omega_DM/Omega_b ~ 5.4.

    Per Gemini peer review (2026-01-11): This should be treated as speculative
    numerology, not fundamental physics derivation.
    """

    # DISCLAIMER for runtime warning
    DISCLAIMER = (
        "WARNING: This module presents a SPECULATIVE phenomenological model. "
        "The 288 = b3 * 12 (24 * 12) represents an octonionic/24-dimensional structure. "
        "The calibration kappa = 4.25 is a PHENOMENOLOGICAL FIT "
        "to match Planck 2018 data, with no rigorous derivation. The dark matter "
        "interpretation lacks a concrete physical mechanism (particle type, mass, "
        "interactions). Per Gemini peer review 2026-01-11, this should be treated "
        "as speculative numerology, not fundamental physics."
    )

    # Topological constants from FormulasRegistry
    # NOTE: 288 = b3 * 12 (24 * 12, octonionic basis)
    N_TOTAL = 288      # b3 * 12 = 24 * 12 (octonionic/24D structure)
    N_VISIBLE = 125    # Arbitrary assignment (5^3, no gauge theory basis)
    N_HIDDEN = 163     # Remainder (claimed as "sterile sector")

    # Planck 2018 cosmological parameters
    OMEGA_M_PLANCK = 0.3111       # Total matter density
    OMEGA_M_UNCERTAINTY = 0.0056
    OMEGA_DM_PLANCK = 0.265       # Dark matter density (Omega_c h^2 / h^2)
    OMEGA_DM_UNCERTAINTY = 0.007
    OMEGA_B_PLANCK = 0.0493       # Baryon density
    OMEGA_B_UNCERTAINTY = 0.00033

    # Derived: DM/baryon ratio from Planck
    DM_BARYON_PLANCK = OMEGA_DM_PLANCK / OMEGA_B_PLANCK  # ~ 5.375

    def __init__(self):
        super().__init__()
        # Use SSOT values if available
        if hasattr(_REG, 'roots_total'):
            self.N_TOTAL = _REG.nitzotzin_roots
        if hasattr(_REG, 'visible_sector'):
            self.N_VISIBLE = _REG.sophian_registry
        if hasattr(_REG, 'sterile_sector'):
            self.N_HIDDEN = _REG.barbelo_modulus

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="dark-matter-residue-v20",
            version="20.0",
            domain="cosmology",
            title="Dark Matter from Hidden Sector Volume",
            description=(
                "SPECULATIVE: Derives dark matter density Omega_DM from the "
                "partition of 288 = b3 * 12 (octonionic/24D structure). The "
                "163/288 volume fraction of the hidden sector is fitted to DM abundance."
            ),
            section_id="B",
            subsection_id="B.2"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            "topology.roots_total",
            "topology.visible_sector",
            "topology.sterile_sector",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            "cosmology.Omega_DM_derived",
            "cosmology.Omega_baryon_derived",
            "cosmology.Omega_matter_derived",
            "cosmology.DM_to_baryon_ratio",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "dark-matter-volume-ratio-v20",
            "omega-dm-derivation-v20",
        ]

    def _ensure_inputs(self, registry: PMRegistry) -> None:
        """Ensure required topology inputs are available."""
        defaults = {
            "topology.roots_total": (self.N_TOTAL, "ESTABLISHED:FormulasRegistry"),
            "topology.visible_sector": (self.N_VISIBLE, "ESTABLISHED:FormulasRegistry"),
            "topology.sterile_sector": (self.N_HIDDEN, "ESTABLISHED:FormulasRegistry"),
            "topology.b3": (24, "ESTABLISHED:FormulasRegistry"),
        }

        for path, (value, source) in defaults.items():
            if not registry.has_param(path):
                registry.set_param(path, value, source=source, status="ESTABLISHED")

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute dark matter residue derivation from hidden sector geometry.

        WARNING: This is a SPECULATIVE phenomenological model. See DISCLAIMER.

        The derivation chain:
        1. Compute volume ratios from root partition (163/288, 125/288)
        2. Map hidden sector volume to dark matter fraction
        3. Derive Omega_DM, Omega_b, and DM/baryon ratio
        4. Validate against Planck 2018 measurements

        Returns:
            Dictionary with all derived dark matter quantities
        """
        # Print disclaimer at start of run
        print("\n" + "=" * 70)
        print("DARK MATTER RESIDUE v20 - SPECULATIVE MODEL")
        print("=" * 70)
        print(self.DISCLAIMER)
        print("=" * 70 + "\n")

        self._ensure_inputs(registry)

        # Get topological parameters from registry (or use defaults)
        N_total = registry.get("topology.roots_total", default=self.N_TOTAL)
        N_visible = registry.get("topology.visible_sector", default=self.N_VISIBLE)
        N_hidden = registry.get("topology.sterile_sector", default=self.N_HIDDEN)
        b3 = registry.get("topology.b3", default=24)

        # Step 1: Compute volume fractions
        # The hidden sector contains N_hidden/N_total of the total 7D volume
        f_hidden = N_hidden / N_total  # 163/288 ~ 0.5660
        f_visible = N_visible / N_total  # 125/288 ~ 0.4340

        # Step 2: Map 7D volume ratio to 3D matter density
        # The projection from 7D to 4D involves dimensional reduction
        # Dark matter fraction of total matter:
        # Omega_DM/Omega_m = f_hidden^(3/7) * correction_factor
        #
        # Physical interpretation:
        # - 7D hidden volume projects to 3D density via (V_7D)^(3/7)
        # - The 3/7 exponent comes from dimensional projection
        #
        # Alternative: Direct ratio approach
        # Omega_DM/Omega_m = N_hidden/(N_hidden + N_visible * projection_factor)

        # Use the simpler geometric mapping:
        # The hidden sector contributes to dark matter
        # The visible sector contributes to baryons
        # But the visible sector has stronger coupling (gauge localization)

        # Projection correction: gauge localization enhances visible sector
        # by factor ~ sqrt(b3/2) ~ 3.46
        gauge_enhancement = math.sqrt(b3 / 2.0)  # ~ 3.464

        # Effective contributions:
        # Hidden sector -> DM (no enhancement, bulk)
        # Visible sector -> baryons (enhanced by gauge localization)
        effective_hidden = N_hidden  # 163
        effective_visible = N_visible * gauge_enhancement  # 125 * 3.464 ~ 433

        # Dark matter fraction of total matter
        DM_fraction = effective_hidden / (effective_hidden + effective_visible)
        baryon_fraction = 1.0 - DM_fraction

        # Total matter density (use Planck value as anchor)
        Omega_m = self.OMEGA_M_PLANCK  # 0.3111

        # Derived densities
        Omega_DM_derived = Omega_m * DM_fraction
        Omega_b_derived = Omega_m * baryon_fraction

        # Step 3: Compute DM/baryon ratio
        DM_to_baryon_ratio = Omega_DM_derived / Omega_b_derived

        # Step 4: Alternative derivation using direct volume ratio
        # This provides a cross-check
        # Omega_DM/Omega_b = (N_hidden/N_visible)^(3/7)
        volume_ratio = N_hidden / N_visible  # 163/125 ~ 1.304
        alt_DM_baryon = volume_ratio ** (3.0 / 7.0)  # ~ 1.125

        # Weighted average of both approaches
        # Method 1: gauge enhancement gives DM/b ~ 0.377/0.733 ~ 0.514 * 5.4 adjustment
        # Method 2: volume ratio gives ~ 1.125 * Omega_b

        # Use empirical calibration to match Planck
        # The key insight: N_hidden/N_visible controls the ratio
        # Calibration factor accounts for projection details
        #
        # PHENOMENOLOGICAL FIT WARNING (per Gemini peer review 2026-01-11):
        # This kappa = 4.25 is a PURE PHENOMENOLOGICAL FIT chosen specifically
        # to reproduce the Planck 2018 DM/baryon ratio of ~5.37. There is NO
        # rigorous derivation of this value from first principles. It is
        # curve-fitting, not physics derivation. The value was adjusted until
        # the output matched observations - this is the definition of fine-tuning.
        calibration = 4.25  # PHENOMENOLOGICAL FIT - NOT DERIVED (gives DM/b ~ 5.37)

        Omega_DM_derived = self.OMEGA_B_PLANCK * volume_ratio * calibration
        Omega_b_derived = self.OMEGA_B_PLANCK

        # Clamp to physical range
        Omega_DM_derived = min(Omega_DM_derived, Omega_m - Omega_b_derived)

        # Recalculate ratio
        DM_to_baryon_ratio = Omega_DM_derived / Omega_b_derived

        # Total matter
        Omega_matter_total = Omega_DM_derived + Omega_b_derived

        # Step 5: Validate against Planck 2018
        DM_deviation = abs(Omega_DM_derived - self.OMEGA_DM_PLANCK)
        DM_sigma = DM_deviation / self.OMEGA_DM_UNCERTAINTY

        b_deviation = abs(Omega_b_derived - self.OMEGA_B_PLANCK)
        b_sigma = b_deviation / self.OMEGA_B_UNCERTAINTY

        # Determine status based on worst sigma
        max_sigma = max(DM_sigma, b_sigma)
        if max_sigma < 1.0:
            status = "PASS"
        elif max_sigma < 2.0:
            status = "MARGINAL"
        elif max_sigma < 3.0:
            status = "TENSION"
        else:
            status = "FAIL"

        # Store results
        result = DarkMatterResult(
            Omega_DM_derived=Omega_DM_derived,
            Omega_DM_planck=self.OMEGA_DM_PLANCK,
            Omega_baryon_derived=Omega_b_derived,
            Omega_baryon_planck=self.OMEGA_B_PLANCK,
            Omega_matter_total=Omega_matter_total,
            DM_to_baryon_ratio=DM_to_baryon_ratio,
            DM_to_baryon_planck=self.DM_BARYON_PLANCK,
            volume_ratio_hidden=f_hidden,
            volume_ratio_visible=f_visible,
            sigma_deviation_DM=DM_sigma,
            sigma_deviation_baryon=b_sigma,
            status=status
        )

        # Register derived parameters
        registry.set_param(
            "cosmology.Omega_DM_derived", Omega_DM_derived,
            source="dark-matter-residue-v20",
            status="DERIVED",
            experimental_value=self.OMEGA_DM_PLANCK,
            experimental_uncertainty=self.OMEGA_DM_UNCERTAINTY,
            experimental_source="Planck2018",
            bound_type="measured"
        )

        registry.set_param(
            "cosmology.Omega_baryon_derived", Omega_b_derived,
            source="dark-matter-residue-v20",
            status="DERIVED",
            experimental_value=self.OMEGA_B_PLANCK,
            experimental_uncertainty=self.OMEGA_B_UNCERTAINTY,
            experimental_source="Planck2018",
            bound_type="measured"
        )

        registry.set_param(
            "cosmology.Omega_matter_derived", Omega_matter_total,
            source="dark-matter-residue-v20",
            status="DERIVED",
            experimental_value=self.OMEGA_M_PLANCK,
            experimental_uncertainty=self.OMEGA_M_UNCERTAINTY,
            experimental_source="Planck2018",
            bound_type="measured"
        )

        registry.set_param(
            "cosmology.DM_to_baryon_ratio", DM_to_baryon_ratio,
            source="dark-matter-residue-v20",
            status="DERIVED",
            metadata={"explanation": "DM/baryon ratio from 163/125 volume partition"}
        )

        return {
            "cosmology.Omega_DM_derived": Omega_DM_derived,
            "cosmology.Omega_baryon_derived": Omega_b_derived,
            "cosmology.Omega_matter_derived": Omega_matter_total,
            "cosmology.DM_to_baryon_ratio": DM_to_baryon_ratio,
            "Omega_DM_planck": self.OMEGA_DM_PLANCK,
            "Omega_b_planck": self.OMEGA_B_PLANCK,
            "DM_to_baryon_planck": self.DM_BARYON_PLANCK,
            "volume_ratio_hidden": f_hidden,
            "volume_ratio_visible": f_visible,
            "N_hidden": N_hidden,
            "N_visible": N_visible,
            "N_total": N_total,
            "sigma_deviation_DM": DM_sigma,
            "sigma_deviation_baryon": b_sigma,
            "status": status,
        }

    def get_formulas(self) -> List[Formula]:
        """Return formulas for dark matter derivation."""
        return [
            Formula(
                id="dark-matter-volume-ratio-v20",
                label="(DM.1)",
                latex=r"\frac{V_{\text{hidden}}}{V_{\text{total}}} = \frac{N_{\text{hidden}}}{N_{\text{total}}} = \frac{163}{288} \approx 0.566",
                plain_text="V_hidden/V_total = N_hidden/N_total = 163/288 ~ 0.566",
                category="SPECULATIVE",
                description=(
                    "SPECULATIVE: Hidden sector volume fraction. The 288 = b3 * 12 "
                    "(24 * 12) represents an octonionic/24-dimensional structure. "
                    "The 125/163 partition is arbitrary, not from gauge theory."
                ),
                input_params=["topology.sterile_sector", "topology.roots_total"],
                output_params=["cosmology.volume_ratio_hidden"],
                derivation={
                    "steps": [
                        "1. 288 = b3 * 12 = 24 * 12 (octonionic/24D basis)",
                        "2. Visible sector: 5^3 = 125 (arbitrary, no gauge theory basis)",
                        "3. Hidden sector: 288 - 125 = 163 (remainder)",
                        "4. Volume ratio: 163/288 = 0.5660",
                        "NOTE: This is SPECULATIVE numerology, not physics derivation",
                    ],
                    "references": ["Appendix B.2 (Speculative Material)"]
                }
            ),
            Formula(
                id="omega-dm-derivation-v20",
                label="(DM.2)",
                latex=r"\Omega_{\text{DM}} = \Omega_b \cdot \frac{N_{\text{hidden}}}{N_{\text{visible}}} \cdot \kappa \approx 0.27",
                plain_text="Omega_DM = Omega_b * (N_hidden/N_visible) * kappa ~ 0.27",
                category="PHENOMENOLOGICAL_FIT",
                description=(
                    "PHENOMENOLOGICAL FIT: Dark matter density from hidden/visible ratio. "
                    "The kappa = 4.25 is a PURE FIT to Planck 2018 data, NOT derived. "
                    "This is curve-fitting, not physics derivation."
                ),
                input_params=[
                    "topology.sterile_sector",
                    "topology.visible_sector",
                    "cosmology.Omega_baryon_derived"
                ],
                output_params=["cosmology.Omega_DM_derived"],
                derivation={
                    "steps": [
                        "1. Volume ratio: N_hidden/N_visible = 163/125 ~ 1.304",
                        "2. kappa = 4.25 is PHENOMENOLOGICAL FIT (not derived!)",
                        "3. Omega_DM = 0.0493 * 1.304 * 4.25 ~ 0.27",
                        "4. This MATCHES Planck because kappa was FITTED to match",
                        "WARNING: This is curve-fitting, not derivation",
                    ],
                    "references": ["Appendix B.2 (Speculative Material)"]
                }
            ),
            Formula(
                id="dm-baryon-ratio-v20",
                label="(DM.3)",
                latex=r"\frac{\Omega_{\text{DM}}}{\Omega_b} = \frac{N_{\text{hidden}}}{N_{\text{visible}}} \cdot \kappa = \frac{163}{125} \cdot 4.25 \approx 5.54",
                plain_text="DM/baryon = (N_hidden/N_visible) * kappa = 163/125 * 4.25 ~ 5.54",
                category="PHENOMENOLOGICAL_FIT",
                description=(
                    "PHENOMENOLOGICAL FIT: DM/baryon ratio. The match to Planck 2018 "
                    "(~5.38) is achieved by FITTING kappa = 4.25. This is not a "
                    "prediction - it is a fit parameter chosen to match observation."
                ),
                input_params=["topology.sterile_sector", "topology.visible_sector"],
                output_params=["cosmology.DM_to_baryon_ratio"],
                derivation={
                    "steps": [
                        "1. Ratio: 163/125 = 1.304 (from arbitrary partition)",
                        "2. kappa = 4.25 (PHENOMENOLOGICAL FIT to Planck)",
                        "3. DM/baryon = 1.304 * 4.25 = 5.54",
                        "4. Planck 2018: 0.265/0.0493 = 5.38",
                        "5. Match achieved BY CONSTRUCTION (kappa was fitted)",
                    ],
                    "references": ["Appendix B.2 (Speculative Material)", "Planck 2018"]
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="cosmology.Omega_DM_derived",
                name="Dark Matter Density Parameter",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Dark matter density parameter derived from hidden sector volume. "
                    "Omega_DM = Omega_b * (163/125) * 4.25 ~ 0.27."
                ),
                derivation_formula="omega-dm-derivation-v20",
                experimental_bound=0.265,
                uncertainty=0.007,
                bound_type="measured",
                bound_source="Planck2018"
            ),
            Parameter(
                path="cosmology.Omega_baryon_derived",
                name="Baryon Density Parameter",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Baryon density from visible sector. Uses Planck 2018 anchor "
                    "value Omega_b = 0.0493."
                ),
                derivation_formula="omega-dm-derivation-v20",
                experimental_bound=0.0493,
                uncertainty=0.00033,
                bound_type="measured",
                bound_source="Planck2018"
            ),
            Parameter(
                path="cosmology.Omega_matter_derived",
                name="Total Matter Density",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Total matter density Omega_m = Omega_DM + Omega_b. "
                    "Derived value should match Planck 2018: 0.3111 +/- 0.0056."
                ),
                experimental_bound=0.3111,
                uncertainty=0.0056,
                bound_type="measured",
                bound_source="Planck2018"
            ),
            Parameter(
                path="cosmology.DM_to_baryon_ratio",
                name="DM to Baryon Ratio",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Dark matter to baryon density ratio. "
                    "Derived from 163/125 root partition with calibration."
                ),
                derivation_formula="dm-baryon-ratio-v20",
                experimental_bound=5.38,
                uncertainty=0.15,
                bound_type="measured",
                bound_source="Planck2018"
            ),
        ]

    def get_section_content(self) -> SectionContent:
        """Return paper section content for dark matter derivation."""
        return SectionContent(
            section_id="B.2",
            subsection_id=None,
            title="SPECULATIVE: Dark Matter as Geometric Residue",
            abstract=(
                "WARNING: This section presents SPECULATIVE phenomenological material. "
                "The 288 = b3 * 12 (24 * 12) represents an octonionic/24-dimensional structure. "
                "The calibration kappa = 4.25 is a phenomenological "
                "fit to Planck 2018 data, not a derived quantity. This approach lacks a "
                "concrete physical mechanism (particle type, mass, interactions). Per Gemini "
                "peer review 2026-01-11, this should be treated as speculative numerology.\n\n"
                "Original claim (DISPUTED): dark matter is a geometric residue - the portion "
                "of a 'root structure' residing in the hidden sector. The 288 total partitions "
                "into 125 visible and 163 hidden. This 163/288 ~ 0.566 volume "
                "fraction is then FITTED to match Omega_DM ~ 0.27."
            ),
            content_blocks=[
                ContentBlock(
                    type="callout",
                    callout_type="warning",
                    title="SPECULATIVE MATERIAL",
                    content=(
                        "This section presents a SPECULATIVE phenomenological model. "
                        "The 288 = b3 * 12 (octonionic/24D structure). The kappa = 4.25 calibration "
                        "is a PHENOMENOLOGICAL FIT, not derived. No concrete dark matter particle, "
                        "mass, or interaction mechanism is specified. Treat as exploratory numerology."
                    )
                ),
                ContentBlock(
                    type="heading",
                    level=2,
                    content="B.2 SPECULATIVE: Dark Matter as Geometric Residue"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "This section explores a SPECULATIVE numerological approach to dark matter. "
                        "The model uses 288 = b3 * 12 (24 * 12), representing an octonionic/24-dimensional "
                        "structure. The partition into 125 'visible' and 163 'hidden' lacks rigorous "
                        "gauge-theoretic justification."
                    )
                ),
                ContentBlock(
                    type="equation",
                    formula_id="dark-matter-volume-ratio-v20",
                    label="(DM.1)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The model assigns N_visible = 125 = 5^3 'roots' to the visible sector. "
                        "NOTE: This is an ARBITRARY assignment - 125 does not correspond to any "
                        "known gauge group dimension. The remaining N_hidden = 163 is claimed "
                        "to form a 'dark sector', but no physical mechanism is specified."
                    )
                ),
                ContentBlock(
                    type="callout",
                    callout_type="warning",
                    title="The 163 Assignment (SPECULATIVE)",
                    content=(
                        "The number 163 is mathematically interesting (Heegner number), but "
                        "its connection to dark matter physics is NUMEROLOGICAL, not physical. "
                        "No particle type, mass, cross-section, or interaction is specified. "
                        "This is pattern-matching, not physics derivation."
                    )
                ),
                ContentBlock(
                    type="equation",
                    formula_id="omega-dm-derivation-v20",
                    label="(DM.2)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The dark matter density is FITTED to match Planck 2018 via "
                        "the phenomenological calibration kappa = 4.25. This is NOT "
                        "a derivation - it is curve-fitting. The 'projection factor' "
                        "and 'dimensional reduction' claims lack rigorous justification."
                    )
                ),
                ContentBlock(
                    type="equation",
                    formula_id="dm-baryon-ratio-v20",
                    label="(DM.3)"
                ),
                ContentBlock(
                    type="table",
                    headers=["Quantity", "Derived", "Planck 2018", "Deviation"],
                    rows=[
                        ["Omega_DM", "0.273", "0.265 +/- 0.007", "~1.1 sigma"],
                        ["Omega_b", "0.0493", "0.0493 +/- 0.0003", "exact"],
                        ["DM/baryon", "5.54", "5.38 +/- 0.15", "~1.1 sigma"],
                    ]
                ),
            ],
            formula_refs=[
                "dark-matter-volume-ratio-v20",
                "omega-dm-derivation-v20",
                "dm-baryon-ratio-v20"
            ],
            param_refs=[
                "cosmology.Omega_DM_derived",
                "cosmology.Omega_baryon_derived",
                "cosmology.DM_to_baryon_ratio"
            ]
        )


# Standalone execution for testing
if __name__ == "__main__":
    print("=" * 70)
    print("DARK MATTER RESIDUE v20 - Test Run")
    print("=" * 70)

    registry = PMRegistry.get_instance()
    sim = DarkMatterResidueV20()
    result = sim.run(registry)

    print(f"\n--- Topological Parameters ---")
    print(f"N_total (roots):    {result['N_total']}")
    print(f"N_visible (matter): {result['N_visible']}")
    print(f"N_hidden (bulk):    {result['N_hidden']}")
    print(f"Volume ratio hidden: {result['volume_ratio_hidden']:.4f}")
    print(f"Volume ratio visible: {result['volume_ratio_visible']:.4f}")

    print(f"\n--- Dark Matter Derivation ---")
    print(f"Omega_DM derived:   {result['cosmology.Omega_DM_derived']:.4f}")
    print(f"Omega_DM Planck:    {result['Omega_DM_planck']:.4f}")
    print(f"Sigma deviation:    {result['sigma_deviation_DM']:.2f}")

    print(f"\n--- Baryon Derivation ---")
    print(f"Omega_b derived:    {result['cosmology.Omega_baryon_derived']:.4f}")
    print(f"Omega_b Planck:     {result['Omega_b_planck']:.4f}")
    print(f"Sigma deviation:    {result['sigma_deviation_baryon']:.2f}")

    print(f"\n--- Matter Totals ---")
    print(f"Omega_m derived:    {result['cosmology.Omega_matter_derived']:.4f}")
    print(f"DM/baryon derived:  {result['cosmology.DM_to_baryon_ratio']:.2f}")
    print(f"DM/baryon Planck:   {result['DM_to_baryon_planck']:.2f}")

    print(f"\n--- Validation ---")
    print(f"Status:             {result['status']}")
    print("=" * 70)
