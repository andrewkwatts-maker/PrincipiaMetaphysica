"""
Injection Utilities
====================

Utilities for injecting computed results into the PMRegistry.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Any, Optional, Dict

# Import types for type hints (avoid circular imports)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .registry import PMRegistry
    from .simulation_base import Formula, SectionContent


def inject_param(
    registry: 'PMRegistry',
    path: str,
    value: Any,
    source: str,
    uncertainty: Optional[float] = None,
    status: str = "DERIVED",
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Inject a parameter into the registry.

    Args:
        registry: PMRegistry instance
        path: Parameter path (e.g., "proton_decay.tau_p_years")
        value: Parameter value
        source: Source identifier (simulation ID or "ESTABLISHED:SOURCE")
        uncertainty: Optional uncertainty
        status: Status ("ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED")
        metadata: Optional additional metadata

    Example:
        inject_param(
            registry,
            "proton_decay.tau_p_years",
            8.15e34,
            "proton_decay_v16_0",
            uncertainty=0.15e34,
            status="DERIVED"
        )
    """
    registry.set_param(
        path=path,
        value=value,
        source=source,
        uncertainty=uncertainty,
        status=status,
        metadata=metadata
    )


def inject_formula(
    registry: 'PMRegistry',
    formula: 'Formula',
    source: str = ""
) -> None:
    """
    Inject a formula into the registry.

    Args:
        registry: PMRegistry instance
        formula: Formula instance to inject
        source: Source simulation file identifier

    Example:
        from simulations.base import Formula

        formula = Formula(
            id="proton-lifetime",
            label="(4.12)",
            latex=r"\tau_p = \frac{M_{GUT}^4}{\alpha_{GUT}^2 m_p^5} \times S^2",
            plain_text="tau_p = M_GUT^4 / (alpha_GUT^2 * m_p^5) * S^2",
            category="DERIVED",
            description="Proton decay lifetime with geometric suppression",
            input_params=["gauge.M_GUT", "gauge.ALPHA_GUT", "constants.m_proton"],
            output_params=["proton_decay.tau_p_years"]
        )
        inject_formula(registry, formula)
    """
    registry.add_formula(formula, source=source)


def inject_section(
    registry: 'PMRegistry',
    content: 'SectionContent'
) -> None:
    """
    Inject section content into the registry.

    Args:
        registry: PMRegistry instance
        content: SectionContent instance to inject

    Example:
        from simulations.base import SectionContent, ContentBlock

        section = SectionContent(
            section_id="4",
            subsection_id="4.6",
            title="Proton Decay",
            abstract="The proton lifetime emerges from TCS G2 cycle separation.",
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content="The grand unification of forces at M_GUT..."
                ),
                ContentBlock(
                    type="formula",
                    formula_id="proton-lifetime",
                    label="(4.12)"
                ),
            ],
            formula_refs=["proton-lifetime"],
            param_refs=["proton_decay.tau_p_years"]
        )
        inject_section(registry, section)
    """
    registry.add_section_content(content.section_id, content)


def inject_established(
    registry: 'PMRegistry',
    path: str,
    value: Any,
    source_name: str,
    uncertainty: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Inject an ESTABLISHED physics parameter (cannot be overridden).

    Args:
        registry: PMRegistry instance
        path: Parameter path (e.g., "constants.M_PLANCK")
        value: Parameter value
        source_name: Source name (e.g., "PDG2024", "NuFIT6.0")
        uncertainty: Optional uncertainty
        metadata: Optional additional metadata

    Example:
        inject_established(
            registry,
            "constants.M_PLANCK",
            2.435e18,
            "PDG2024",
            uncertainty=0.003e18
        )
    """
    registry.set_param(
        path=path,
        value=value,
        source=f"ESTABLISHED:{source_name}",
        uncertainty=uncertainty,
        status="ESTABLISHED",
        metadata=metadata
    )


def inject_geometric(
    registry: 'PMRegistry',
    path: str,
    value: Any,
    source: str,
    uncertainty: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Inject a GEOMETRIC parameter (from G2 topology, cannot be overridden).

    Args:
        registry: PMRegistry instance
        path: Parameter path (e.g., "topology.elder_kads", "topology.CHI_EFF")
        value: Parameter value
        source: Source simulation ID
        uncertainty: Optional uncertainty
        metadata: Optional additional metadata

    Example:
        inject_geometric(
            registry,
            "topology.elder_kads",
            24,
            "g2_geometry_v16_0"
        )
    """
    registry.set_param(
        path=path,
        value=value,
        source=source,
        uncertainty=uncertainty,
        status="GEOMETRIC",
        metadata=metadata
    )


def inject_prediction(
    registry: 'PMRegistry',
    path: str,
    value: Any,
    source: str,
    uncertainty: Optional[float] = None,
    experimental_bound: Optional[float] = None,
    bound_type: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Inject a PREDICTED parameter (testable prediction).

    Args:
        registry: PMRegistry instance
        path: Parameter path
        value: Predicted value
        source: Source simulation ID
        uncertainty: Theoretical uncertainty
        experimental_bound: Current experimental bound if any
        bound_type: Type of bound ("upper", "lower", "range")
        metadata: Optional additional metadata

    Example:
        inject_prediction(
            registry,
            "proton_decay.tau_p_years",
            8.15e34,
            "proton_decay_v16_0",
            uncertainty=0.5e34,
            experimental_bound=1.67e34,
            bound_type="lower"
        )
    """
    meta = metadata or {}
    if experimental_bound is not None:
        meta['experimental_bound'] = experimental_bound
    if bound_type is not None:
        meta['bound_type'] = bound_type

    registry.set_param(
        path=path,
        value=value,
        source=source,
        uncertainty=uncertainty,
        status="PREDICTED",
        metadata=meta
    )
