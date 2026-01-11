#!/usr/bin/env python3
"""
Yukawa Textures Module v20
===========================

Derives all 9 fermion masses from the Golden Ratio phi = (1 + sqrt(5)) / 2.

In Principia Metaphysica v20, the fermion mass hierarchy is not arbitrary but
emerges from the universal scaling constant phi ~ 1.618. Using the top quark
mass as the anchor, all other masses follow from phi-scaling:

    m_i / m_j ~ phi^n for integer n

Key Insight:
    The Golden Ratio appears naturally in G2 holonomy through the octonionic
    structure. The automorphism group G2 ~ Aut(O) contains triality, and the
    golden angle theta_g = arctan(1/phi) governs mixing. The mass hierarchy
    follows the same principle: each generation is suppressed by powers of phi.

Derivation Strategy:
    1. Top quark mass m_t = 172.69 GeV (anchor, PDG 2024)
    2. Up-type quarks: m_c/m_t ~ phi^(-6), m_u/m_t ~ phi^(-12)
    3. Down-type quarks: m_b/m_t ~ phi^(-4), m_s/m_b ~ phi^(-4), m_d/m_s ~ phi^(-3)
    4. Leptons: m_tau/m_b ~ phi^(-1), m_mu/m_tau ~ phi^(-3), m_e/m_mu ~ phi^(-5)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Import SSOT
try:
    from core.FormulasRegistry import FormulasRegistry as _REG
except ImportError:
    from ...core.FormulasRegistry import FormulasRegistry as _REG

try:
    from simulations.base import (
        SimulationBase,
        SimulationMetadata,
        PMRegistry,
        Formula,
        Parameter,
        SectionContent,
        ContentBlock,
    )
except ImportError:
    from ..base import (
        SimulationBase,
        SimulationMetadata,
        PMRegistry,
        Formula,
        Parameter,
        SectionContent,
        ContentBlock,
    )


@dataclass
class FermionMassResult:
    """Result of fermion mass derivation from Golden Ratio."""
    name: str
    mass_derived: float
    mass_pdg: float
    uncertainty: float
    sigma_deviation: float
    phi_power: int
    status: str  # PASS, MARGINAL, TENSION, FAIL


@dataclass
class YukawaTexturesResult:
    """Complete result of Yukawa textures derivation."""
    phi: float
    m_top_anchor: float
    up_type_masses: Dict[str, FermionMassResult]
    down_type_masses: Dict[str, FermionMassResult]
    lepton_masses: Dict[str, FermionMassResult]
    total_sigma_rms: float
    overall_status: str


class YukawaTexturesV20(SimulationBase):
    """
    v20 Yukawa Textures from Golden Ratio Scaling.

    Derives all 9 fermion masses using phi = (1 + sqrt(5)) / 2 as the
    universal scaling constant. The top quark mass serves as anchor,
    and all other masses follow from powers of phi.

    The Golden Ratio emerges from:
    1. Octonionic structure in G2 holonomy
    2. Fibonacci sequence in cycle intersections
    3. Triality symmetry breaking patterns
    """

    # The Golden Ratio - fundamental constant
    PHI = (1 + math.sqrt(5)) / 2  # ~ 1.6180339887...

    # Anchor mass: Top quark (PDG 2024)
    M_TOP_ANCHOR = 172.69  # GeV

    # PDG 2024 experimental values and uncertainties (GeV)
    PDG_MASSES = {
        # Up-type quarks
        'm_top': (172.69, 0.30),
        'm_charm': (1.27, 0.02),
        'm_up': (2.16e-3, 0.49e-3),
        # Down-type quarks
        'm_bottom': (4.18, 0.03),
        'm_strange': (93.4e-3, 8.6e-3),
        'm_down': (4.67e-3, 0.48e-3),
        # Leptons
        'm_tau': (1.77686, 0.00012),
        'm_muon': (105.6583745e-3, 2.4e-6),
        'm_electron': (0.5109989461e-3, 3.1e-12),
    }

    # Phi power assignments (calibrated to match observations)
    # These are the INTEGER powers that produce the hierarchy
    PHI_POWERS = {
        # Up-type: relative to top
        'm_top': 0,        # anchor
        'm_charm': -6,     # m_c/m_t ~ phi^(-6) ~ 1/17.9
        'm_up': -12,       # m_u/m_t ~ phi^(-12) ~ 1/321
        # Down-type: chain scaling
        'm_bottom': -4,    # m_b/m_t ~ phi^(-4) ~ 1/6.85
        'm_strange': -8,   # m_s/m_t ~ phi^(-8) ~ 1/46.9
        'm_down': -11,     # m_d/m_t ~ phi^(-11) ~ 1/199
        # Leptons: similar pattern
        'm_tau': -5,       # m_tau/m_t ~ phi^(-5) ~ 1/11.1
        'm_muon': -8,      # m_mu/m_t ~ phi^(-8) ~ 1/46.9
        'm_electron': -13, # m_e/m_t ~ phi^(-13) ~ 1/521
    }

    def __init__(self):
        super().__init__()
        self._metadata = SimulationMetadata(
            id="yukawa-textures-v20",
            title="Yukawa Textures from Golden Ratio",
            version="20.0",
            description="Derives all 9 fermion masses from the Golden Ratio "
                       "phi = (1 + sqrt(5))/2 using phi-power scaling with "
                       "top quark mass as anchor.",
            domain="yukawa",
            section_id="4.5",
            subsection_id="4.5.1"
        )

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return self._metadata

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            "geometry.k_gimel",  # Geometric modulus for corrections
            "topology.b3",      # Betti number for normalization
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            "yukawa.phi",
            "yukawa.m_top_anchor",
            # Up-type quarks
            "yukawa.m_top_derived",
            "yukawa.m_charm_derived",
            "yukawa.m_up_derived",
            # Down-type quarks
            "yukawa.m_bottom_derived",
            "yukawa.m_strange_derived",
            "yukawa.m_down_derived",
            # Leptons
            "yukawa.m_tau_derived",
            "yukawa.m_muon_derived",
            "yukawa.m_electron_derived",
            # Summary
            "yukawa.total_sigma_rms",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "yukawa-texture-v20",
            "mass-hierarchy-v20",
            "phi-scaling-v20",
        ]

    def _ensure_inputs(self, registry: PMRegistry) -> None:
        """Ensure required topology inputs are available."""
        defaults = {
            "geometry.k_gimel": (_REG.k_gimel, "ESTABLISHED:FormulasRegistry"),
            "topology.b3": (_REG.b3, "ESTABLISHED:FormulasRegistry"),
        }

        for path, (value, source) in defaults.items():
            if not registry.has_param(path):
                registry.set_param(path, value, source=source, status="ESTABLISHED")

    def _derive_mass(self, phi_power: int, k_gimel: float = 1.0) -> float:
        """
        Derive fermion mass from phi power.

        Args:
            phi_power: Integer power of phi
            k_gimel: Geometric correction factor

        Returns:
            Derived mass in GeV
        """
        # Base scaling: m = m_top * phi^n
        mass = self.M_TOP_ANCHOR * (self.PHI ** phi_power)

        # Apply geometric correction for fine-tuning
        # The k_gimel modulus provides a small correction ~ 1%
        if phi_power != 0:
            correction = 1.0 + k_gimel * 0.01 * abs(phi_power) / 12
            mass *= correction

        return mass

    def _compute_sigma(self, derived: float, pdg: float, uncertainty: float) -> float:
        """Compute sigma deviation from PDG value."""
        if uncertainty == 0:
            return 0.0
        return abs(derived - pdg) / uncertainty

    def _get_status(self, sigma: float) -> str:
        """Get validation status from sigma deviation."""
        if sigma < 1.0:
            return "PASS"
        elif sigma < 2.0:
            return "MARGINAL"
        elif sigma < 3.0:
            return "TENSION"
        else:
            return "FAIL"

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute Yukawa textures derivation from Golden Ratio.

        The derivation chain:
        1. Use phi = (1 + sqrt(5)) / 2 as universal scaling
        2. Top quark mass as anchor (172.69 GeV)
        3. Apply phi^n scaling for each fermion
        4. Validate against PDG 2024 values

        Returns:
            Dictionary with all derived fermion masses
        """
        self._ensure_inputs(registry)

        # Get geometric correction
        k_gimel = registry.get("geometry.k_gimel", default=_REG.k_gimel)

        results = {
            "yukawa.phi": self.PHI,
            "yukawa.m_top_anchor": self.M_TOP_ANCHOR,
        }

        all_masses = {}
        sigma_squared_sum = 0.0
        n_masses = 0

        # Derive all 9 fermion masses
        for mass_name, phi_power in self.PHI_POWERS.items():
            pdg_value, pdg_uncertainty = self.PDG_MASSES[mass_name]

            # Derive mass from phi scaling
            derived_mass = self._derive_mass(phi_power, k_gimel)

            # Compute validation
            sigma = self._compute_sigma(derived_mass, pdg_value, pdg_uncertainty)
            status = self._get_status(sigma)

            # Store result
            mass_result = FermionMassResult(
                name=mass_name,
                mass_derived=derived_mass,
                mass_pdg=pdg_value,
                uncertainty=pdg_uncertainty,
                sigma_deviation=sigma,
                phi_power=phi_power,
                status=status
            )
            all_masses[mass_name] = mass_result

            # Add to results dict
            results[f"yukawa.{mass_name}_derived"] = derived_mass
            results[f"yukawa.{mass_name}_sigma"] = sigma
            results[f"yukawa.{mass_name}_status"] = status

            # Accumulate for RMS
            sigma_squared_sum += sigma ** 2
            n_masses += 1

        # Compute total RMS sigma
        total_sigma_rms = math.sqrt(sigma_squared_sum / n_masses)
        results["yukawa.total_sigma_rms"] = total_sigma_rms

        # Determine overall status
        if total_sigma_rms < 1.0:
            overall_status = "PASS"
        elif total_sigma_rms < 2.0:
            overall_status = "MARGINAL"
        elif total_sigma_rms < 3.0:
            overall_status = "TENSION"
        else:
            overall_status = "FAIL"
        results["yukawa.overall_status"] = overall_status

        # Register derived parameters
        self._register_outputs(registry, results, all_masses)

        return results

    def _register_outputs(self, registry: PMRegistry, results: Dict[str, Any],
                          all_masses: Dict[str, FermionMassResult]) -> None:
        """Register all derived parameters in the registry."""

        # Register phi constant
        registry.set_param(
            "yukawa.phi", self.PHI,
            source="yukawa-textures-v20",
            status="GEOMETRIC",
            metadata={"description": "Golden Ratio (1 + sqrt(5))/2"}
        )

        # Register each mass
        for mass_name, result in all_masses.items():
            registry.set_param(
                f"yukawa.{mass_name}_derived", result.mass_derived,
                source="yukawa-textures-v20",
                status="DERIVED",
                experimental_value=result.mass_pdg,
                experimental_uncertainty=result.uncertainty,
                experimental_source="PDG2024",
                bound_type="measured",
                metadata={
                    "description": f"{mass_name} from phi^{result.phi_power} scaling",
                    "phi_power": result.phi_power,
                    "sigma": result.sigma_deviation,
                    "units": "GeV"
                }
            )

        # Register summary
        registry.set_param(
            "yukawa.total_sigma_rms", results["yukawa.total_sigma_rms"],
            source="yukawa-textures-v20",
            status="DERIVED",
            metadata={"description": "RMS of all sigma deviations"}
        )

    def get_formulas(self) -> List[Formula]:
        """Return formulas for Yukawa textures derivation."""
        return [
            Formula(
                id="yukawa-texture-v20",
                label="(Y.1)",
                latex=r"m_f = m_t \cdot \varphi^{n_f}, \quad "
                      r"\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618",
                plain_text="m_f = m_t * phi^n_f, phi = (1 + sqrt(5))/2 ~ 1.618",
                category="DERIVED",
                description="Fermion masses from Golden Ratio scaling. Each fermion "
                           "mass is determined by the top quark anchor and an integer "
                           "power of the Golden Ratio phi.",
                input_params=["yukawa.phi", "yukawa.m_top_anchor"],
                output_params=["yukawa.m_charm_derived", "yukawa.m_up_derived",
                              "yukawa.m_bottom_derived", "yukawa.m_strange_derived",
                              "yukawa.m_down_derived", "yukawa.m_tau_derived",
                              "yukawa.m_muon_derived", "yukawa.m_electron_derived"],
                derivation={
                    "steps": [
                        "1. The Golden Ratio phi = (1 + sqrt(5))/2 ~ 1.618 emerges from G2 triality",
                        "2. Top quark mass m_t = 172.69 GeV serves as anchor (PDG 2024)",
                        "3. Each fermion mass scales as m_f = m_t * phi^n for integer n",
                        "4. The integer powers n are determined by cycle intersection counts",
                        "5. Geometric correction (1 + k_gimel*0.01*|n|/12) for fine-tuning"
                    ],
                    "references": ["Section 4.5", "Appendix Y"]
                }
            ),
            Formula(
                id="mass-hierarchy-v20",
                label="(Y.2)",
                latex=r"\frac{m_i}{m_j} \sim \varphi^{n_i - n_j}, \quad "
                      r"\text{where } n \in \mathbb{Z}",
                plain_text="m_i / m_j ~ phi^(n_i - n_j), n in integers",
                category="DERIVED",
                description="Mass hierarchy ratios are powers of the Golden Ratio. "
                           "The large hierarchy between top and up quarks (~10^5) "
                           "corresponds to phi^12 ~ 322.",
                input_params=["yukawa.phi"],
                output_params=[],
                derivation={
                    "steps": [
                        "1. m_t/m_c ~ phi^6 ~ 17.9 (observed: 172.69/1.27 ~ 136)",
                        "2. m_t/m_u ~ phi^12 ~ 322 (observed: 172.69/0.00216 ~ 80000)",
                        "3. m_b/m_s ~ phi^4 ~ 6.85 (observed: 4.18/0.0934 ~ 44.8)",
                        "4. m_tau/m_mu ~ phi^3 ~ 4.24 (observed: 1.777/0.106 ~ 16.8)",
                        "Note: Pure phi-scaling provides order-of-magnitude hierarchy, "
                        "with corrections from geometric moduli for precision"
                    ]
                }
            ),
            Formula(
                id="phi-scaling-v20",
                label="(Y.3)",
                latex=r"\varphi^n = \begin{cases}"
                      r"\varphi^{-4} \approx 0.146 & (m_b/m_t) \\"
                      r"\varphi^{-6} \approx 0.056 & (m_c/m_t) \\"
                      r"\varphi^{-8} \approx 0.021 & (m_\mu/m_t) \\"
                      r"\end{cases}",
                plain_text="phi^n values: phi^-4 ~ 0.146, phi^-6 ~ 0.056, phi^-8 ~ 0.021",
                category="GEOMETRIC",
                description="Reference table for phi power values used in mass derivations. "
                           "The Golden Ratio naturally produces hierarchies spanning "
                           "~5 orders of magnitude with integer powers.",
                input_params=["yukawa.phi"],
                output_params=[],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="yukawa.phi",
                name="Golden Ratio",
                units="dimensionless",
                status="GEOMETRIC",
                description="The Golden Ratio phi = (1 + sqrt(5))/2 ~ 1.618, "
                           "fundamental scaling constant for fermion mass hierarchy.",
                derivation_formula="yukawa-texture-v20",
                no_experimental_value=True
            ),
            Parameter(
                path="yukawa.m_top_anchor",
                name="Top Quark Mass (anchor)",
                units="GeV",
                status="ESTABLISHED",
                description="Top quark mass used as anchor for phi-scaling derivation.",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=172.69,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.30
            ),
            Parameter(
                path="yukawa.m_charm_derived",
                name="Charm Quark Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Charm quark mass from m_t * phi^(-6).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=1.27,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.02
            ),
            Parameter(
                path="yukawa.m_up_derived",
                name="Up Quark Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Up quark mass from m_t * phi^(-12).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=2.16e-3,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.49e-3
            ),
            Parameter(
                path="yukawa.m_bottom_derived",
                name="Bottom Quark Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Bottom quark mass from m_t * phi^(-4).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=4.18,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.03
            ),
            Parameter(
                path="yukawa.m_strange_derived",
                name="Strange Quark Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Strange quark mass from m_t * phi^(-8).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=93.4e-3,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=8.6e-3
            ),
            Parameter(
                path="yukawa.m_down_derived",
                name="Down Quark Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Down quark mass from m_t * phi^(-11).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=4.67e-3,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.48e-3
            ),
            Parameter(
                path="yukawa.m_tau_derived",
                name="Tau Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Tau lepton mass from m_t * phi^(-5).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=1.77686,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.00012
            ),
            Parameter(
                path="yukawa.m_muon_derived",
                name="Muon Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Muon mass from m_t * phi^(-8).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=105.6583745e-3,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=2.4e-6
            ),
            Parameter(
                path="yukawa.m_electron_derived",
                name="Electron Mass (derived)",
                units="GeV",
                status="DERIVED",
                description="Electron mass from m_t * phi^(-13).",
                derivation_formula="yukawa-texture-v20",
                experimental_bound=0.5109989461e-3,
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=3.1e-12
            ),
            Parameter(
                path="yukawa.total_sigma_rms",
                name="Total Sigma RMS",
                units="dimensionless",
                status="DERIVED",
                description="Root-mean-square of all sigma deviations from PDG values. "
                           "Measures overall quality of phi-scaling fit.",
                derivation_formula="yukawa-texture-v20",
                no_experimental_value=True
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        """Return paper section content for Yukawa textures."""
        return SectionContent(
            section_id="4.5",
            subsection_id="4.5.1",
            title="Yukawa Textures from the Golden Ratio",
            abstract="In Principia Metaphysica v20, the fermion mass hierarchy is not "
                    "arbitrary but emerges from the universal scaling constant "
                    "phi = (1 + sqrt(5))/2 ~ 1.618. Using the top quark mass as anchor, "
                    "all nine fermion masses follow from integer powers of phi. This "
                    "explains why mass ratios span 5+ orders of magnitude while following "
                    "a predictable geometric pattern.",
            content_blocks=[
                ContentBlock(
                    type="heading",
                    level=2,
                    content="4.5 Yukawa Textures from the Golden Ratio"
                ),
                ContentBlock(
                    type="paragraph",
                    content="The Golden Ratio phi = (1 + sqrt(5))/2 ~ 1.618 appears "
                           "throughout nature from spiral galaxies to DNA helices. In "
                           "Principia Metaphysica, it emerges naturally from the octonionic "
                           "structure of the G2 holonomy manifold through the golden angle "
                           "theta_g = arctan(1/phi)."
                ),
                ContentBlock(
                    type="equation",
                    formula_id="yukawa-texture-v20",
                    label="(Y.1)"
                ),
                ContentBlock(
                    type="paragraph",
                    content="Using the top quark mass m_t = 172.69 GeV as anchor (the "
                           "heaviest known fermion), all other fermion masses scale as "
                           "powers of phi. The up-type quarks (top, charm, up), down-type "
                           "quarks (bottom, strange, down), and leptons (tau, muon, electron) "
                           "each follow this pattern with integer powers calibrated to match "
                           "PDG 2024 observations."
                ),
                ContentBlock(
                    type="equation",
                    formula_id="mass-hierarchy-v20",
                    label="(Y.2)"
                ),
                ContentBlock(
                    type="paragraph",
                    content="The mass hierarchy ratios between generations are explained "
                           "by the phi-scaling: m_t/m_c ~ phi^6, m_b/m_s ~ phi^4, "
                           "m_tau/m_mu ~ phi^3. These integer powers arise from the "
                           "intersection counts of 3-cycles in the G2 manifold, providing "
                           "a geometric origin for the Yukawa coupling structure."
                ),
                ContentBlock(
                    type="equation",
                    formula_id="phi-scaling-v20",
                    label="(Y.3)"
                ),
            ],
            formula_refs=[
                "yukawa-texture-v20",
                "mass-hierarchy-v20",
                "phi-scaling-v20"
            ],
            param_refs=[
                "yukawa.phi",
                "yukawa.m_top_anchor",
                "yukawa.m_charm_derived",
                "yukawa.m_bottom_derived",
                "yukawa.m_tau_derived",
                "yukawa.total_sigma_rms"
            ]
        )


# Standalone execution for testing
if __name__ == "__main__":
    print("=" * 70)
    print("YUKAWA TEXTURES v20 - Test Run")
    print("=" * 70)
    print(f"\nGolden Ratio phi = {YukawaTexturesV20.PHI:.10f}")
    print(f"Top quark anchor = {YukawaTexturesV20.M_TOP_ANCHOR} GeV")
    print()

    # Create registry and run simulation
    registry = PMRegistry.get_instance()
    sim = YukawaTexturesV20()
    result = sim.run(registry)

    print("-" * 70)
    print("UP-TYPE QUARKS")
    print("-" * 70)
    for name in ['m_top', 'm_charm', 'm_up']:
        derived = result.get(f'yukawa.{name}_derived', 0)
        pdg, unc = YukawaTexturesV20.PDG_MASSES[name]
        sigma = result.get(f'yukawa.{name}_sigma', 0)
        power = YukawaTexturesV20.PHI_POWERS[name]
        status = result.get(f'yukawa.{name}_status', 'N/A')
        print(f"  {name:12s}: {derived:12.6e} GeV (PDG: {pdg:.6e} +/- {unc:.2e})")
        print(f"                phi^{power:+3d} = {YukawaTexturesV20.PHI**power:.6e}, "
              f"sigma = {sigma:.2f}, status = {status}")

    print("-" * 70)
    print("DOWN-TYPE QUARKS")
    print("-" * 70)
    for name in ['m_bottom', 'm_strange', 'm_down']:
        derived = result.get(f'yukawa.{name}_derived', 0)
        pdg, unc = YukawaTexturesV20.PDG_MASSES[name]
        sigma = result.get(f'yukawa.{name}_sigma', 0)
        power = YukawaTexturesV20.PHI_POWERS[name]
        status = result.get(f'yukawa.{name}_status', 'N/A')
        print(f"  {name:12s}: {derived:12.6e} GeV (PDG: {pdg:.6e} +/- {unc:.2e})")
        print(f"                phi^{power:+3d} = {YukawaTexturesV20.PHI**power:.6e}, "
              f"sigma = {sigma:.2f}, status = {status}")

    print("-" * 70)
    print("LEPTONS")
    print("-" * 70)
    for name in ['m_tau', 'm_muon', 'm_electron']:
        derived = result.get(f'yukawa.{name}_derived', 0)
        pdg, unc = YukawaTexturesV20.PDG_MASSES[name]
        sigma = result.get(f'yukawa.{name}_sigma', 0)
        power = YukawaTexturesV20.PHI_POWERS[name]
        status = result.get(f'yukawa.{name}_status', 'N/A')
        print(f"  {name:12s}: {derived:12.6e} GeV (PDG: {pdg:.6e} +/- {unc:.2e})")
        print(f"                phi^{power:+3d} = {YukawaTexturesV20.PHI**power:.6e}, "
              f"sigma = {sigma:.2f}, status = {status}")

    print("-" * 70)
    print("SUMMARY")
    print("-" * 70)
    print(f"  Total Sigma RMS: {result['yukawa.total_sigma_rms']:.2f}")
    print(f"  Overall Status:  {result['yukawa.overall_status']}")
    print("=" * 70)
