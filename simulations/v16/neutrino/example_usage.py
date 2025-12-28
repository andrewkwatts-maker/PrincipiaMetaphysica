#!/usr/bin/env python3
"""
Example Usage: Neutrino Mixing v16 Simulation
==============================================

This script demonstrates various ways to use the NeutrinoMixingSimulation
class in different contexts.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os

# Add parent to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
sys.path.insert(0, _project_root)

from simulations.base import PMRegistry
from simulations.v16.neutrino import NeutrinoMixingSimulation


def example_1_simple_execution():
    """
    Example 1: Simple standalone execution

    This is the easiest way to run the simulation - just call the
    standalone function which handles all setup internally.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 1: Simple Standalone Execution")
    print("=" * 75)

    from simulations.v16.neutrino.neutrino_mixing_v16_0 import run_neutrino_mixing

    results = run_neutrino_mixing(verbose=True)

    print("\nResults dictionary keys:")
    for key in results.keys():
        print(f"  - {key}")


def example_2_manual_registry():
    """
    Example 2: Manual registry setup

    This demonstrates how to manually set up the registry with
    topological parameters before running the simulation.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 2: Manual Registry Setup")
    print("=" * 75)

    # Reset registry for clean state
    PMRegistry.reset_instance()
    registry = PMRegistry.get_instance()

    # Manually set topological parameters
    print("\nSetting topological parameters...")
    registry.set_param("topology.b2", 4,
                      source="ESTABLISHED:TCS #187",
                      status="ESTABLISHED")
    registry.set_param("topology.b3", 24,
                      source="ESTABLISHED:TCS #187",
                      status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144,
                      source="ESTABLISHED:TCS #187",
                      status="ESTABLISHED")
    registry.set_param("topology.n_gen", 3,
                      source="ESTABLISHED:TCS #187",
                      status="ESTABLISHED")
    registry.set_param("topology.orientation_sum", 12,
                      source="ESTABLISHED:Sp(2,R) gauge fixing",
                      status="ESTABLISHED")

    # Create and execute simulation
    print("\nExecuting simulation...")
    sim = NeutrinoMixingSimulation()
    results = sim.execute(registry, verbose=False)

    # Access results from registry
    print("\nResults from registry:")
    print(f"  theta_12 = {registry.get_param('neutrino.theta_12_pred'):.2f} deg")
    print(f"  theta_13 = {registry.get_param('neutrino.theta_13_pred'):.2f} deg")
    print(f"  theta_23 = {registry.get_param('neutrino.theta_23_pred'):.2f} deg")
    print(f"  delta_CP = {registry.get_param('neutrino.delta_CP_pred'):.1f} deg")


def example_3_metadata_inspection():
    """
    Example 3: Inspecting simulation metadata

    Shows how to access metadata, formulas, and section content
    before running the simulation.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 3: Metadata Inspection")
    print("=" * 75)

    sim = NeutrinoMixingSimulation()

    # Inspect metadata
    metadata = sim.metadata
    print("\nSimulation Metadata:")
    print(f"  ID:          {metadata.id}")
    print(f"  Version:     {metadata.version}")
    print(f"  Domain:      {metadata.domain}")
    print(f"  Section:     {metadata.section_id}.{metadata.subsection_id}")
    print(f"  Title:       {metadata.title}")

    # List required inputs
    print("\nRequired Inputs:")
    for inp in sim.required_inputs:
        print(f"  - {inp}")

    # List outputs
    print("\nOutput Parameters:")
    for out in sim.output_params:
        print(f"  - {out}")

    # List formulas
    print("\nFormulas Provided:")
    for formula_id in sim.output_formulas:
        print(f"  - {formula_id}")


def example_4_formula_details():
    """
    Example 4: Accessing formula details

    Demonstrates how to access the full formula definitions with
    LaTeX, derivations, and parameter mappings.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 4: Formula Details")
    print("=" * 75)

    sim = NeutrinoMixingSimulation()
    formulas = sim.get_formulas()

    # Show details for theta_13 formula
    theta_13_formula = [f for f in formulas if f.id == "pmns-theta-13"][0]

    print("\nFormula: pmns-theta-13")
    print(f"  Label:       {theta_13_formula.label}")
    print(f"  Category:    {theta_13_formula.category}")
    print(f"  Description: {theta_13_formula.description}")
    print(f"\n  LaTeX:       {theta_13_formula.latex}")
    print(f"\n  Plain Text:  {theta_13_formula.plain_text}")
    print(f"\n  Inputs:      {', '.join(theta_13_formula.input_params)}")
    print(f"  Outputs:     {', '.join(theta_13_formula.output_params)}")

    # Show derivation steps
    print("\n  Derivation Steps:")
    for i, step in enumerate(theta_13_formula.derivation['steps'], 1):
        print(f"    {i}. {step['description']}")
        print(f"       {step['formula']}")


def example_5_section_content():
    """
    Example 5: Accessing section content

    Shows how to retrieve the section content for paper generation.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 5: Section Content")
    print("=" * 75)

    sim = NeutrinoMixingSimulation()
    section = sim.get_section_content()

    print(f"\nSection {section.section_id}.{section.subsection_id}: {section.title}")
    print(f"\nAbstract: {section.abstract}")
    print(f"\nContent Blocks: {len(section.content_blocks)}")
    print(f"Formula Refs:   {len(section.formula_refs)}")
    print(f"Param Refs:     {len(section.param_refs)}")

    # Show first few content blocks
    print("\nFirst 3 Content Blocks:")
    for i, block in enumerate(section.content_blocks[:3], 1):
        print(f"\n  Block {i} ({block.type}):")
        if block.type == "paragraph":
            preview = block.content[:80] + "..." if len(block.content) > 80 else block.content
            print(f"    {preview}")
        elif block.type == "formula":
            print(f"    Formula ID: {block.formula_id}")
            print(f"    Label:      {block.label}")


def example_6_parameter_definitions():
    """
    Example 6: Parameter definitions with experimental bounds

    Shows how to access parameter definitions including
    experimental bounds and metadata.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 6: Parameter Definitions")
    print("=" * 75)

    sim = NeutrinoMixingSimulation()
    params = sim.get_output_param_definitions()

    print("\nOutput Parameter Definitions:")
    for param in params:
        print(f"\n  {param.path}")
        print(f"    Name:         {param.name}")
        print(f"    Units:        {param.units}")
        print(f"    Status:       {param.status}")
        print(f"    Description:  {param.description[:60]}...")
        print(f"    Exp. Bound:   {param.experimental_bound} {param.units}")
        print(f"    Bound Type:   {param.bound_type}")
        print(f"    Source:       {param.bound_source}")
        print(f"    Derived From: {param.derivation_formula}")


def example_7_provenance_tracking():
    """
    Example 7: Provenance tracking

    Demonstrates how the registry tracks where each parameter
    came from and when it was computed.
    """
    print("\n" + "=" * 75)
    print("EXAMPLE 7: Provenance Tracking")
    print("=" * 75)

    # Reset and run simulation
    PMRegistry.reset_instance()
    registry = PMRegistry.get_instance()

    # Set inputs
    registry.set_param("topology.b2", 4, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.b3", 24, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.n_gen", 3, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.orientation_sum", 12, source="ESTABLISHED:Sp(2,R)", status="ESTABLISHED")

    # Execute
    sim = NeutrinoMixingSimulation()
    sim.execute(registry, verbose=False)

    # Check provenance
    print("\nProvenance for output parameters:")
    for param_path in sim.output_params:
        entry = registry.get_entry(param_path)
        if entry:
            print(f"\n  {param_path}")
            print(f"    Value:     {entry.value:.2f}")
            print(f"    Source:    {entry.source}")
            print(f"    Status:    {entry.status}")
            print(f"    Timestamp: {entry.timestamp}")


def main():
    """Run all examples."""
    print("\n" + "#" * 75)
    print("# NEUTRINO MIXING V16 - USAGE EXAMPLES")
    print("#" * 75)

    example_1_simple_execution()
    example_2_manual_registry()
    example_3_metadata_inspection()
    example_4_formula_details()
    example_5_section_content()
    example_6_parameter_definitions()
    example_7_provenance_tracking()

    print("\n" + "=" * 75)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
