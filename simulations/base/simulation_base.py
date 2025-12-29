"""
Simulation Base Classes
========================

Abstract base class and data structures for Principia Metaphysica simulations.

This module defines:
- SimulationMetadata: Metadata about a simulation
- SimulationBase: Abstract base class that all simulations must extend
- Data structures: ContentBlock, SectionContent, Formula, Parameter

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class SimulationMetadata:
    """
    Metadata describing a simulation.

    Attributes:
        id: Unique identifier for the simulation (e.g., "proton_decay_v16_0")
        version: Version string (e.g., "16.0")
        domain: Domain category (e.g., "proton", "neutrino", "gauge")
        title: Human-readable title
        description: Detailed description of what the simulation computes
        section_id: Paper section ID this content relates to (e.g., "2", "4", "5")
        subsection_id: Optional subsection ID (e.g., "A", "B" for appendices)
        appendix: If True, render at end of paper as appendix (default False)
        parent_section_id: Optional parent section (deprecated, use appendix instead)
        section_type: Optional type hint (deprecated, use appendix instead)
    """
    id: str
    version: str
    domain: str
    title: str
    description: str
    section_id: str
    subsection_id: Optional[str] = None
    appendix: bool = False
    parent_section_id: Optional[str] = None
    section_type: Optional[str] = None


@dataclass
class ContentBlock:
    """
    A block of content in a section.

    Attributes:
        type: Content type ("paragraph", "formula", "list", "table", "heading",
              "note", "callout", "equation", "code", "definition", "theorem",
              "concept_highlight")
        content: The actual content (text, LaTeX, etc.)
        formula_id: Optional reference to a formula ID
        label: Optional label for equations/figures
        level: Optional heading level (for type="heading")
        items: Optional list items (for type="list")
        headers: Optional table headers (for type="table")
        rows: Optional table rows (for type="table")
        callout_type: Callout style ("info", "warning", "success", "error")
        title: Optional title for callouts, definitions, theorems
        language: Programming language for code blocks ("python", "javascript", etc.)
    """
    type: str  # "paragraph", "formula", "list", "table", "heading", "callout", etc.
    content: Optional[str] = None
    formula_id: Optional[str] = None
    label: Optional[str] = None
    level: Optional[int] = None
    items: Optional[List[str]] = None
    headers: Optional[List[str]] = None
    rows: Optional[List[List[str]]] = None
    callout_type: Optional[str] = None  # "info", "warning", "success", "error"
    title: Optional[str] = None  # For callouts, definitions, theorems
    language: Optional[str] = None  # For code blocks: "python", "javascript", etc.


@dataclass
class SectionContent:
    """
    Complete content for a paper section.

    Attributes:
        section_id: Section number this content relates to (e.g., "2", "4", "5")
        subsection_id: Subsection identifier (e.g., "A", "B" for appendices)
        title: Section title
        abstract: Brief summary of the section
        content_blocks: List of content blocks in order
        formula_refs: List of formula IDs referenced in this section
        param_refs: List of parameter paths referenced in this section
        appendix: If True, render at end of paper as appendix (default False)
        parent_section_id: Optional parent section (deprecated, use appendix instead)
        section_type: Optional type hint (deprecated, use appendix instead)
    """
    section_id: str
    subsection_id: Optional[str]
    title: str
    abstract: str
    content_blocks: List[ContentBlock] = field(default_factory=list)
    formula_refs: List[str] = field(default_factory=list)
    param_refs: List[str] = field(default_factory=list)
    appendix: bool = False
    parent_section_id: Optional[str] = None
    section_type: Optional[str] = None


@dataclass
class Formula:
    """
    A mathematical formula with metadata.

    Attributes:
        id: Unique formula identifier (e.g., "proton-lifetime")
        label: Display label (e.g., "(4.12)")
        latex: LaTeX representation of the formula
        plain_text: Plain text representation
        category: Category ("ESTABLISHED", "THEORY", "DERIVED", "PREDICTIONS")
        description: What the formula computes
        inputParams: List of input parameter paths (camelCase for JSON)
        outputParams: List of output parameter paths (camelCase for JSON)
        input_params: List of input parameter paths (snake_case for Python - legacy)
        output_params: List of output parameter paths (snake_case for Python - legacy)
        derivation: Optional derivation dict with steps
        terms: Dictionary of term definitions
    """
    id: str
    label: str
    latex: str
    plain_text: str
    category: str
    description: str
    inputParams: List[str] = field(default_factory=list)
    outputParams: List[str] = field(default_factory=list)
    input_params: List[str] = field(default_factory=list)
    output_params: List[str] = field(default_factory=list)
    derivation: Optional[Dict[str, Any]] = None
    terms: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Parameter:
    """
    A parameter definition with required experimental value metadata.

    SCHEMA REQUIREMENT: All parameters MUST have either:
    1. experimental_bound + bound_source (from PDG 2024, NuFIT 6.0, DESI 2025, etc.)
    2. no_experimental_value=True with justification in description

    Attributes:
        path: Dot-notation path (e.g., "proton_decay.tau_p_years")
        name: Display name (e.g., "Proton Lifetime")
        units: Units string (e.g., "years", "GeV", "dimensionless")
        status: Status ("ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED")
        description: What the parameter represents (static text)
        description_template: Optional template with {value} placeholder for dynamic descriptions
        derivation_formula: Optional formula ID that derives this parameter
        experimental_bound: Experimental constraint value (REQUIRED unless no_experimental_value=True)
        bound_type: Type of bound ("upper", "lower", "range", "measured", "central_value")
        bound_source: Citation for bound (e.g., "PDG2024", "NuFIT6.0", "DESI2025", "Super-K")
        uncertainty: Experimental uncertainty (1-sigma)
        no_experimental_value: Set True if no experimental measurement exists (e.g., topological params)
        validation: Optional validation metadata dict

    Dynamic Descriptions:
        Use description_template with {value} placeholder for descriptions that reference
        the parameter's computed value. Example:
            description_template="Total number of parameters in summary tables ({value})"
        The template is resolved at export time using the actual computed value.
    """
    path: str
    name: str
    units: str
    status: str
    description: str
    description_template: Optional[str] = None  # Template with {value} placeholder
    derivation_formula: Optional[str] = None
    experimental_bound: Optional[float] = None
    bound_type: Optional[str] = None
    bound_source: Optional[str] = None
    uncertainty: Optional[float] = None
    no_experimental_value: bool = False
    validation: Optional[Dict[str, Any]] = None


class SimulationBase(ABC):
    """
    Abstract base class for all Principia Metaphysica simulations.

    All simulations must:
    1. Define metadata (id, version, domain, etc.)
    2. Specify required inputs (parameter paths)
    3. Specify outputs (parameter paths and formula IDs)
    4. Implement run() to perform the computation
    5. Provide section content, formulas, and parameter definitions

    Example Usage:
        class ProtonDecaySimulation(SimulationBase):
            @property
            def metadata(self) -> SimulationMetadata:
                return SimulationMetadata(
                    id="proton_decay_v16_0",
                    version="16.0",
                    domain="proton",
                    title="Proton Decay Lifetime",
                    description="Compute proton decay lifetime from G2 geometry",
                    section_id="4",
                    subsection_id="4.6"
                )

            @property
            def required_inputs(self) -> List[str]:
                return ["gauge.M_GUT", "gauge.ALPHA_GUT", "topology.K_MATCHING"]

            @property
            def output_params(self) -> List[str]:
                return ["proton_decay.tau_p_years"]

            def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
                # Computation logic
                return {"proton_decay.tau_p_years": 8.15e34}
    """

    @property
    @abstractmethod
    def metadata(self) -> SimulationMetadata:
        """
        Return metadata about this simulation.

        Returns:
            SimulationMetadata instance
        """
        pass

    @property
    @abstractmethod
    def required_inputs(self) -> List[str]:
        """
        Return list of required input parameter paths.

        Returns:
            List of parameter paths (e.g., ["gauge.M_GUT", "topology.CHI_EFF"])
        """
        pass

    @property
    @abstractmethod
    def output_params(self) -> List[str]:
        """
        Return list of output parameter paths.

        Returns:
            List of parameter paths this simulation computes
        """
        pass

    @property
    @abstractmethod
    def output_formulas(self) -> List[str]:
        """
        Return list of formula IDs this simulation provides.

        Returns:
            List of formula IDs (e.g., ["proton-lifetime", "cycle-separation"])
        """
        pass

    def validate_inputs(self, registry: 'PMRegistry') -> bool:
        """
        Validate that all required inputs are present in the registry.

        Args:
            registry: PMRegistry instance to check

        Returns:
            True if all inputs are available

        Raises:
            ValueError: If any required inputs are missing
        """
        missing = []
        for param_path in self.required_inputs:
            if not registry.has_param(param_path):
                missing.append(param_path)

        if missing:
            raise ValueError(f"Missing required inputs for {self.metadata.id}: {missing}")

        return True

    @abstractmethod
    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute the simulation.

        Args:
            registry: PMRegistry instance to read inputs from

        Returns:
            Dictionary mapping parameter paths to computed values
        """
        pass

    def inject_outputs(self, registry: 'PMRegistry', results: Dict[str, Any]) -> None:
        """
        Inject computed outputs into the registry.

        Args:
            registry: PMRegistry instance to inject into
            results: Dictionary of computed results from run()
        """
        # Get parameter definitions to extract units and other metadata
        param_defs = {p.path: p for p in self.get_output_param_definitions()}

        for param_path in self.output_params:
            if param_path in results:
                param_def = param_defs.get(param_path)
                computed_value = results[param_path]

                # Build metadata dictionary with units
                metadata = {}
                if param_def:
                    if param_def.units:
                        metadata['units'] = param_def.units

                    # Handle dynamic description templates
                    if param_def.description_template:
                        # Resolve {value} placeholder with computed value
                        try:
                            # Format value appropriately
                            if isinstance(computed_value, float):
                                if computed_value >= 1e4 or (computed_value != 0 and abs(computed_value) < 0.01):
                                    formatted_value = f"{computed_value:.2e}"
                                else:
                                    formatted_value = f"{computed_value:.4g}"
                            elif isinstance(computed_value, int):
                                formatted_value = str(computed_value)
                            else:
                                formatted_value = str(computed_value)

                            metadata['description'] = param_def.description_template.format(
                                value=formatted_value
                            )
                        except (KeyError, ValueError):
                            # Fallback to template as-is if formatting fails
                            metadata['description'] = param_def.description_template
                    elif param_def.description:
                        metadata['description'] = param_def.description

                # Extract experimental comparison data from parameter definition
                exp_value = None
                exp_uncertainty = None
                exp_source = None
                bound_type = None

                if param_def:
                    exp_value = param_def.experimental_bound
                    exp_uncertainty = param_def.uncertainty
                    exp_source = param_def.bound_source
                    bound_type = param_def.bound_type

                registry.set_param(
                    path=param_path,
                    value=results[param_path],
                    source=self.metadata.id,
                    status=param_def.status if param_def else "DERIVED",
                    metadata=metadata if metadata else None,
                    experimental_value=exp_value,
                    experimental_uncertainty=exp_uncertainty,
                    experimental_source=exp_source,
                    bound_type=bound_type
                )

    def inject_section(self, registry: 'PMRegistry') -> None:
        """
        Inject section content into the registry.

        Args:
            registry: PMRegistry instance to inject into
        """
        section_content = self.get_section_content()
        if section_content:
            registry.add_section_content(section_content.section_id, section_content)

        # Also inject formulas
        for formula in self.get_formulas():
            registry.add_formula(formula)

    @abstractmethod
    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for the paper.

        Returns:
            SectionContent instance or None if not applicable
        """
        pass

    @abstractmethod
    def get_formulas(self) -> List[Formula]:
        """
        Return list of formulas this simulation provides.

        Returns:
            List of Formula instances
        """
        pass

    @abstractmethod
    def get_output_param_definitions(self) -> List[Parameter]:
        """
        Return parameter definitions for outputs.

        Returns:
            List of Parameter instances describing outputs
        """
        pass

    def execute(self, registry: 'PMRegistry', verbose: bool = True) -> Dict[str, Any]:
        """
        Template method for executing the simulation with validation and injection.

        Args:
            registry: PMRegistry instance
            verbose: Whether to print progress

        Returns:
            Dictionary of computed results
        """
        if verbose:
            print(f"\n[{self.metadata.id}] Starting {self.metadata.title}...")

        # Validate inputs
        self.validate_inputs(registry)

        # Run computation
        start_time = datetime.now()
        results = self.run(registry)
        end_time = datetime.now()

        if verbose:
            elapsed = (end_time - start_time).total_seconds() * 1000
            print(f"[{self.metadata.id}] Completed in {elapsed:.2f}ms")

        # Inject outputs
        self.inject_outputs(registry, results)

        # Inject section content
        self.inject_section(registry)

        return results

    def execute_with_schema(self, registry: 'PMRegistry', verbose: bool = True) -> 'SimulationResult':
        """
        Execute simulation and return schema-compliant result.

        This method produces a comprehensive SimulationResult that includes:
        - Sections, foundations, references
        - Formulas with full metadata
        - Parameters with validation status
        - Input validation results
        - Type data

        Args:
            registry: PMRegistry instance
            verbose: Whether to print progress

        Returns:
            SimulationResult instance (schema-compliant)
        """
        from .schema import SimulationResult, SchemaCompliantSimulation

        if verbose:
            print(f"\n[{self.metadata.id}] Starting {self.metadata.title} (schema mode)...")

        # Validate inputs
        self.validate_inputs(registry)

        # Run computation with timing
        start_time = datetime.now()
        results = self.run(registry)
        end_time = datetime.now()
        elapsed_ms = (end_time - start_time).total_seconds() * 1000

        if verbose:
            print(f"[{self.metadata.id}] Completed in {elapsed_ms:.2f}ms")

        # Inject outputs into registry
        self.inject_outputs(registry, results)
        self.inject_section(registry)

        # Build schema-compliant result using mixin
        builder = _SchemaBuilder(self)
        return builder.build_result(registry, results, elapsed_ms)

    def get_foundations(self) -> List[Dict[str, Any]]:
        """
        Return foundation physics concepts referenced by this simulation.

        Override in subclasses to specify foundations.

        Returns:
            List of foundation dictionaries
        """
        return []

    def get_references(self) -> List[Dict[str, Any]]:
        """
        Return bibliographic references for this simulation.

        Override in subclasses to specify references.

        Returns:
            List of reference dictionaries
        """
        return []

    def get_visualizations(self) -> List[Dict[str, Any]]:
        """
        Return visualization specifications for this simulation.

        Override in subclasses to specify visualizations (plots, diagrams).
        Each visualization dict should contain:
        - filename: Output filename (e.g., "moduli_evolution.png")
        - title: Plot title
        - type: Visualization type ("line", "scatter", "heatmap", "bar", etc.)
        - generator: Function that generates the plot (optional)

        Returns:
            List of visualization dictionaries
        """
        return []

    def generate_visualizations(self, registry: 'PMRegistry', output_dir: str = "AutoGenerated/plots") -> List[str]:
        """
        Generate all visualizations for this simulation.

        Args:
            registry: PMRegistry with simulation results
            output_dir: Directory to save visualization files

        Returns:
            List of generated file paths
        """
        import os
        from pathlib import Path

        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        generated_files = []
        visualizations = self.get_visualizations()

        for viz_spec in visualizations:
            if 'generator' in viz_spec and callable(viz_spec['generator']):
                try:
                    # Call the generator function with registry and output path
                    filename = viz_spec.get('filename', f"{self.metadata.id}_viz.png")
                    output_path = os.path.join(output_dir, filename)

                    # Generate the visualization
                    viz_spec['generator'](registry, output_path)
                    generated_files.append(output_path)

                    print(f"[OK] Generated {filename}")
                except Exception as e:
                    print(f"[ERROR] Failed to generate {viz_spec.get('filename', 'unknown')}: {e}")

        return generated_files


class _SchemaBuilder:
    """Helper class for building schema-compliant results."""

    def __init__(self, simulation: SimulationBase):
        self.simulation = simulation

    def build_result(
        self,
        registry: 'PMRegistry',
        computed_values: Dict[str, Any],
        execution_time_ms: float = 0.0
    ) -> 'SimulationResult':
        """Build a schema-compliant SimulationResult."""
        from .schema import (
            SimulationResult, SectionEntry, FoundationEntry, ReferenceEntry,
            FormulaEntry, ParameterEntry, InputValidationEntry, TypeDataEntry,
            ValidationStatus
        )
        import math

        sim = self.simulation
        metadata = sim.metadata

        # Build input validation entries
        input_validation = []
        input_parameters = []
        for param_path in sim.required_inputs:
            present = registry.has_param(param_path)
            value = registry.get_param(param_path) if present else None
            entry = registry.get_entry(param_path) if present else None

            input_validation.append(InputValidationEntry(
                path=param_path,
                required=True,
                present=present,
                value=value,
                source=entry.source if entry else "",
                status="OK" if present else "MISSING",
                message="" if present else f"Required parameter {param_path} not found"
            ))

            if present and entry:
                input_parameters.append(ParameterEntry(
                    path=param_path,
                    name=entry.metadata.get("description", param_path) if entry.metadata else param_path,
                    value=value,
                    uncertainty=entry.uncertainty,
                    units=entry.metadata.get("units", "") if entry.metadata else "",
                    status=entry.status,
                    source=entry.source,
                    description=entry.metadata.get("description", "") if entry.metadata else ""
                ))

        # Build output parameter entries with validation
        output_parameters = []
        type_data = []
        for param_def in sim.get_output_param_definitions():
            value = computed_values.get(param_def.path)

            # Determine validation status
            validation_status = ValidationStatus.UNKNOWN.value
            validation_ratio = None
            validation_message = ""

            if param_def.experimental_bound is not None and value is not None:
                if param_def.bound_type == "lower":
                    validation_ratio = value / param_def.experimental_bound
                    if validation_ratio > 1.5:
                        validation_status = ValidationStatus.PASS.value
                        validation_message = f"Value {value:.2e} is {validation_ratio:.2f}x above lower bound"
                    elif validation_ratio > 1.0:
                        validation_status = ValidationStatus.MARGINAL.value
                        validation_message = f"Value {value:.2e} is only {validation_ratio:.2f}x above lower bound"
                    else:
                        validation_status = ValidationStatus.FAIL.value
                        validation_message = f"Value {value:.2e} violates lower bound {param_def.experimental_bound:.2e}"
                elif param_def.bound_type == "upper":
                    validation_ratio = value / param_def.experimental_bound
                    if validation_ratio < 0.5:
                        validation_status = ValidationStatus.PASS.value
                        validation_message = f"Value {value:.2e} is well below upper bound"
                    elif validation_ratio < 1.0:
                        validation_status = ValidationStatus.MARGINAL.value
                        validation_message = f"Value {value:.2e} is close to upper bound"
                    else:
                        validation_status = ValidationStatus.FAIL.value
                        validation_message = f"Value {value:.2e} violates upper bound {param_def.experimental_bound:.2e}"

            output_parameters.append(ParameterEntry(
                path=param_def.path,
                name=param_def.name,
                value=value,
                units=param_def.units,
                status=param_def.status,
                source=metadata.id,
                description=param_def.description,
                derivationFormula=param_def.derivation_formula or "",
                experimentalBound=param_def.experimental_bound,
                boundType=param_def.bound_type or "",
                boundSource=param_def.bound_source or "",
                validationStatus=validation_status,
                validationRatio=validation_ratio,
                validationMessage=validation_message
            ))

            # Type data
            actual_type = type(value).__name__ if value is not None else "null"
            is_numeric = isinstance(value, (int, float))
            is_finite = is_numeric and not (math.isnan(value) or math.isinf(value)) if is_numeric else True

            type_data.append(TypeDataEntry(
                path=param_def.path,
                expectedType="number" if param_def.units != "string" else "string",
                actualType=actual_type,
                isNumeric=is_numeric,
                isFinite=is_finite
            ))

        # Build formula entries
        formula_entries = []
        for formula in sim.get_formulas():
            section_parts = metadata.section_id.split('.')
            formula_entries.append(FormulaEntry(
                id=formula.id,
                label=formula.label,
                section=section_parts[0] if section_parts else "",
                sectionId=metadata.section_id,
                equationNumber=formula.label.strip("()") if formula.label else "",
                latex=formula.latex,
                plainText=formula.plain_text,
                category=formula.category,
                description=formula.description,
                inputParams=formula.input_params,
                outputParams=formula.output_params,
                derivedFrom=formula.derivation.get("parentFormulas", []) if formula.derivation else [],
                derivation=formula.derivation or {},
                terms=formula.terms,
                computedValue=computed_values.get(formula.output_params[0]) if formula.output_params else None,
                units="",
                status="active",
                validated=True
            ))

        # Build section entries
        section_entries = []
        section_content = sim.get_section_content()
        if section_content:
            content_blocks = []
            for block in section_content.content_blocks:
                content_blocks.append({
                    "type": block.type,
                    "content": block.content,
                    "formulaId": block.formula_id or "",
                    "label": block.label or ""
                })

            section_entries.append(SectionEntry(
                sectionId=section_content.subsection_id or section_content.section_id,
                parentSection=section_content.section_id if section_content.subsection_id else "",
                title=section_content.title,
                abstract=section_content.abstract,
                contentBlocks=content_blocks,
                formulaRefs=section_content.formula_refs,
                paramRefs=section_content.param_refs,
                foundationRefs=[],
                referenceRefs=[]
            ))

        # Build foundations and references
        foundations = [FoundationEntry(**f) for f in sim.get_foundations()]
        references = [ReferenceEntry(**r) for r in sim.get_references()]

        # Build result
        return SimulationResult(
            simulationId=metadata.id,
            version=metadata.version,
            domain=metadata.domain,
            title=metadata.title,
            timestamp=datetime.now().isoformat(),
            executionTimeMs=execution_time_ms,
            sections=section_entries,
            foundations=foundations,
            references=references,
            formulas=formula_entries,
            inputParameters=input_parameters,
            outputParameters=output_parameters,
            inputValidation=input_validation,
            outputValidation=[],
            typeData=type_data,
            computedValues=computed_values,
            success=True,
            errors=[],
            warnings=[]
        )
