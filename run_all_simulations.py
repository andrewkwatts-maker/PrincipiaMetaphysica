#!/usr/bin/env python3
"""
Principia Metaphysica - Run All Simulations v16.0
===================================================

Unified simulation runner using the v16 infrastructure with:
- PMRegistry for centralized parameter/formula/section management
- EstablishedPhysics for loading experimental constants
- Topological execution order based on simulation dependencies
- Full validation and provenance tracking

ARCHITECTURE:
1. Registry Initialization: Create PMRegistry singleton
2. Load Established Physics: Load PDG/NuFIT/DESI constants
3. Topological Execution: Run simulations in dependency order
4. Validation: Check dependencies before and outputs after each simulation
5. Export: Generate theory_output.json with full provenance

SIMULATION PHASES (Topological Order):

Phase 0 - Introduction (No Dependencies):
  - introduction_v16_0: Theory introduction and overview (Section 1)

Phase 1 - Root Simulations (No Dependencies):
  - g2_geometry_v16_0: G2 manifold topology (b2, b3, chi_eff, K_MATCHING)
  - gauge_unification_v16_0: GUT scale and unified coupling (M_GUT, ALPHA_GUT)

Phase 2 - Core Physics (Depends on Phase 1):
  - fermion_generations_v16_0: Fermion chirality and Yukawa hierarchy
  - chirality_v16_0: Chirality spinor structure from G2 holonomy (Section 4.1)
  - ckm_matrix_v16_0: CKM matrix parameters (Section 4.3)
  - proton_decay_v16_0: Proton lifetime from gauge unification
  - higgs_mass_v16_0: Higgs mass from moduli stabilization

Phase 3 - Precision Observables and Cosmology (Depends on Phase 2):
  - cosmology_intro_v16_0: Cosmological framework introduction (Section 5.1)
  - dark_energy_v16_0: Dark energy from pneuma field (Section 5.2)
  - neutrino_mixing_v16_0: PMNS matrix from G2 associative cycles
  - multi_sector_v16_0: Multi-sector cosmology (dark energy, mirror sectors)

Phase 4 - Field Dynamics (Depends on All):
  - pneuma_mechanism_v16_0: Pneuma field coupling and flow
  - thermal_time_v16_0: Thermal time evolution (depends on Pneuma outputs)

Phase 5 - Discussion, Predictions, and Appendices (Depends on All):
  - discussion_v16_0: Theory discussion and implications (Section 7)
  - predictions_aggregator_v16_0: Testable predictions summary (Section 6)
  - appendix_a_math_v16_0: Mathematical foundations (Appendix A)
  - appendix_b_methods_v16_0: Computational methods (Appendix B)
  - appendix_c_derivations_v16_0: Extended derivations (Appendix C)
  - appendix_d_tables_v16_0: Parameter tables (Appendix D)
  - appendix_m_consciousness_v16_0: Speculative consciousness extensions (Appendix M)
  - appendix_n_g2_landscape_v16_0: G2 topology landscape (Appendix N)

OUTPUT STRUCTURE:
{
  "parameters": {
    "topology.b3": {"value": 24, "source": "g2_geometry_v16_0", ...},
    "gauge.M_GUT": {"value": 2.1e16, "source": "gauge_unification_v16_0", ...},
    ...
  },
  "formulas": {
    "g2-holonomy": {"latex": "...", "category": "THEORY", ...},
    ...
  },
  "sections": {
    "4": {"title": "...", "content_blocks": [...], ...},
    ...
  },
  "provenance": {
    "gauge.M_GUT": ["gauge_unification_v16_0"],
    ...
  },
  "validation": {
    "simulations_run": 8,
    "simulations_passed": 8,
    "simulations_failed": 0,
    "results": [...]
  }
}

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

# Add simulations directory to path
sys.path.insert(0, str(Path(__file__).parent / 'simulations'))
sys.path.insert(0, str(Path(__file__).parent))

# Import base infrastructure
from simulations.base import (
    SimulationBase,
    PMRegistry,
    RegistryValidator,
    ValidationResult,
    SimulationResult as SchemaResult,
    validate_simulation_result,
)

from simulations.base.established import EstablishedPhysics

# Import v16 simulations
# Phase 0 - Introduction (narrative only, no dependencies)
from simulations.v16.introduction.introduction_v16_0 import IntroductionV16

# Phase 1 - Root simulations (no dependencies)
from simulations.v16.geometric.g2_geometry_v16_0 import G2GeometryV16
from simulations.v16.gauge.gauge_unification_v16_0 import GaugeUnificationSimulation

# Phase 2 - Core physics (depends on Phase 1)
from simulations.v16.fermion.fermion_generations_v16_0 import FermionGenerationsV16
from simulations.v16.fermion.chirality_v16_0 import ChiralitySpinorSimulation
from simulations.v16.fermion.ckm_matrix_v16_0 import CKMMatrixSimulation
from simulations.v16.proton.proton_decay_v16_0 import ProtonDecaySimulation
from simulations.v16.higgs.higgs_mass_v16_0 import HiggsMassSimulation

# Phase 3 - Precision observables and cosmology (depends on Phase 2)
from simulations.v16.cosmology.cosmology_intro_v16_0 import CosmologyIntroV16
from simulations.v16.cosmology.dark_energy_v16_0 import DarkEnergyV16
from simulations.v16.thermal.thermal_time_v16_0 import ThermalTimeV16
from simulations.v16.neutrino.neutrino_mixing_v16_0 import NeutrinoMixingSimulation
from simulations.v16.cosmology.multi_sector_v16_0 import MultiSectorV16

# Phase 4 - Field dynamics (depends on all)
from simulations.v16.pneuma.pneuma_mechanism_v16_0 import PneumaMechanismV16

# Phase 5 - Discussion, predictions, and appendices (aggregators and reference material)
from simulations.v16.discussion.discussion_v16_0 import DiscussionV16
from simulations.v16.predictions.predictions_aggregator_v16_0 import PredictionsAggregatorV16
from simulations.v16.appendices.appendix_a_math_v16_0 import AppendixAMathFoundations
from simulations.v16.appendices.appendix_b_methods_v16_0 import AppendixBComputationalMethods
from simulations.v16.appendices.appendix_c_derivations_v16_0 import AppendixCExtendedDerivations
from simulations.v16.appendices.appendix_d_tables_v16_0 import AppendixDParameterTables
from simulations.v16.appendices.appendix_e_proton_v16_0 import AppendixEProtonDecay
from simulations.v16.appendices.appendix_f_v16_0 import AppendixFDimensionalDecomposition
from simulations.v16.appendices.appendix_g_v16_0 import AppendixGEffectiveTorsion
from simulations.v16.appendices.appendix_h_v16_0 import AppendixHProtonBranching
from simulations.v16.appendices.appendix_i_v16_0 import AppendixIGWDispersion
from simulations.v16.appendices.appendix_j_v16_0 import AppendixJMonteCarloError
from simulations.v16.appendices.appendix_k_v16_0 import AppendixKTransparency
from simulations.v16.appendices.appendix_l_v16_0 import AppendixLValuesSummary
from simulations.v16.appendices.appendix_m_v16_0 import AppendixMConsciousnessSpeculation
from simulations.v16.appendices.appendix_n_v16_0 import AppendixNG2Landscape


@dataclass
class SimulationResult:
    """Result of running a single simulation."""
    simulation_id: str
    phase: int
    status: str  # "PASSED", "FAILED", "SKIPPED"
    dependency_check: ValidationResult
    output_check: Optional[ValidationResult] = None
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    outputs_computed: List[str] = field(default_factory=list)


class SimulationRunner:
    """
    Orchestrates execution of all v16 simulations in topological order.
    """

    def __init__(self, verbose: bool = True, schema_mode: bool = False):
        """
        Initialize the simulation runner.

        Args:
            verbose: Whether to print progress messages
            schema_mode: Whether to use schema-compliant execution mode
        """
        self.verbose = verbose
        self.schema_mode = schema_mode
        self.registry = PMRegistry.get_instance()
        self.results: List[SimulationResult] = []
        self.schema_results: List[Dict[str, Any]] = []  # Schema-compliant results

        # Define simulation phases in topological order
        self.phases = {
            0: [
                IntroductionV16(),
            ],
            1: [
                G2GeometryV16(),
                GaugeUnificationSimulation(),
            ],
            2: [
                FermionGenerationsV16(),
                ChiralitySpinorSimulation(),
                CKMMatrixSimulation(),
                ProtonDecaySimulation(),
                HiggsMassSimulation(),
            ],
            3: [
                CosmologyIntroV16(),
                DarkEnergyV16(),
                NeutrinoMixingSimulation(),
                MultiSectorV16(),
            ],
            4: [
                PneumaMechanismV16(),
                ThermalTimeV16(),  # Moved to Phase 4 - depends on Pneuma outputs
            ],
            5: [
                DiscussionV16(),
                PredictionsAggregatorV16(),
                AppendixAMathFoundations(),
                AppendixBComputationalMethods(),
                AppendixCExtendedDerivations(),
                AppendixDParameterTables(),
                AppendixEProtonDecay(),
                AppendixFDimensionalDecomposition(),
                AppendixGEffectiveTorsion(),
                AppendixHProtonBranching(),
                AppendixIGWDispersion(),
                AppendixJMonteCarloError(),
                AppendixKTransparency(),
                AppendixLValuesSummary(),
                AppendixMConsciousnessSpeculation(),
                AppendixNG2Landscape(),
            ],
        }

    def run_all(self) -> Dict[str, Any]:
        """
        Execute all simulations in topological order.

        Returns:
            Dictionary containing validation report and export data
        """
        self._print_header()

        # Step 1: Load established physics
        self._load_established_physics()

        # Step 2: Execute simulations in phases
        for phase_num in sorted(self.phases.keys()):
            self._run_phase(phase_num)

        # Step 3: Generate validation report
        validation_report = self._generate_validation_report()

        # Step 4: Export to theory_output.json
        output_data = self._export_to_json(validation_report)

        # Step 5: Print summary
        self._print_summary(validation_report)

        return output_data

    def _print_header(self) -> None:
        """Print the runner header."""
        if not self.verbose:
            return

        print("=" * 80)
        print("PRINCIPIA METAPHYSICA - Run All Simulations v16.0")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Total simulations: {sum(len(sims) for sims in self.phases.values())}")
        print("=" * 80)

    def _load_established_physics(self) -> None:
        """Load experimental constants into the registry."""
        if self.verbose:
            print("\n[INITIALIZATION] Loading Established Physics")
            print("-" * 80)

        EstablishedPhysics.load_into_registry(self.registry)

        if self.verbose:
            param_count = len(self.registry._parameters)
            print(f"[OK] Loaded {param_count} established parameters")
            print("  - PDG 2024 constants")
            print("  - NuFIT 6.0 neutrino parameters")
            print("  - DESI DR2 cosmological parameters")
            print("  - Experimental bounds (Super-K, LHC, etc.)")

    def _run_phase(self, phase_num: int) -> None:
        """
        Execute all simulations in a given phase.

        Args:
            phase_num: Phase number (1-4)
        """
        simulations = self.phases[phase_num]

        if self.verbose:
            print(f"\n[PHASE {phase_num}] Running {len(simulations)} simulation(s)")
            print("-" * 80)

        for sim in simulations:
            self._run_simulation(sim, phase_num)

    def _run_simulation(self, sim: SimulationBase, phase: int) -> None:
        """
        Execute a single simulation with validation.

        Args:
            sim: SimulationBase instance
            phase: Phase number for tracking
        """
        sim_id = sim.metadata.id

        if self.verbose:
            print(f"\n> {sim_id}: {sim.metadata.title}")

        # Create result entry
        result = SimulationResult(
            simulation_id=sim_id,
            phase=phase,
            status="PENDING",
            dependency_check=ValidationResult(passed=True),
        )

        try:
            # Step 1: Check dependencies
            if self.verbose:
                print(f"  Checking dependencies...")

            result.dependency_check = RegistryValidator.check_dependencies(sim, self.registry)

            if not result.dependency_check.passed:
                result.status = "FAILED"
                result.error_message = "Missing dependencies"
                if self.verbose:
                    print(f"  [X] Dependency check failed:")
                    for error in result.dependency_check.errors:
                        print(f"    - {error}")
                self.results.append(result)
                return

            if self.verbose:
                print(f"  [OK] All dependencies satisfied")

            # Step 2: Execute simulation
            if self.verbose:
                mode_str = " (schema mode)" if self.schema_mode else ""
                print(f"  Running simulation{mode_str}...")

            start_time = datetime.now()

            if self.schema_mode:
                # Execute with schema-compliant output
                schema_result = sim.execute_with_schema(self.registry, verbose=False)
                computed_results = schema_result.computedValues

                # Validate schema compliance
                schema_validation = validate_simulation_result(schema_result.to_dict())
                if not schema_validation["valid"]:
                    if self.verbose:
                        print(f"  [!] Schema validation warnings: {schema_validation['errors']}")

                # Store schema result
                self.schema_results.append(schema_result.to_dict())
            else:
                computed_results = sim.execute(self.registry, verbose=False)

            end_time = datetime.now()

            result.execution_time_ms = (end_time - start_time).total_seconds() * 1000
            result.outputs_computed = list(computed_results.keys())

            if self.verbose:
                print(f"  [OK] Completed in {result.execution_time_ms:.2f}ms")

            # Step 3: Validate outputs
            if self.verbose:
                print(f"  Validating outputs...")

            result.output_check = RegistryValidator.check_outputs(
                sim, computed_results, self.registry
            )

            if not result.output_check.passed:
                result.status = "FAILED"
                result.error_message = "Output validation failed"
                if self.verbose:
                    print(f"  [X] Output validation failed:")
                    for error in result.output_check.errors:
                        print(f"    - {error}")
            else:
                result.status = "PASSED"
                if self.verbose:
                    print(f"  [OK] All outputs validated")
                    print(f"  Computed: {len(result.outputs_computed)} parameters")

        except Exception as e:
            result.status = "FAILED"
            result.error_message = str(e)
            if self.verbose:
                print(f"  [X] Simulation failed with error: {e}")

        self.results.append(result)

    def _generate_validation_report(self) -> Dict[str, Any]:
        """
        Generate validation report from all simulation results.

        Returns:
            Dictionary containing validation statistics and details
        """
        passed = [r for r in self.results if r.status == "PASSED"]
        failed = [r for r in self.results if r.status == "FAILED"]
        skipped = [r for r in self.results if r.status == "SKIPPED"]

        report = {
            "timestamp": datetime.now().isoformat(),
            "simulations_run": len(self.results),
            "simulations_passed": len(passed),
            "simulations_failed": len(failed),
            "simulations_skipped": len(skipped),
            "total_execution_time_ms": sum(r.execution_time_ms for r in self.results),
            "results": []
        }

        # Add detailed results
        for result in self.results:
            result_dict = {
                "simulation_id": result.simulation_id,
                "phase": result.phase,
                "status": result.status,
                "execution_time_ms": result.execution_time_ms,
                "outputs_computed": result.outputs_computed,
            }

            if result.error_message:
                result_dict["error_message"] = result.error_message

            if result.dependency_check and not result.dependency_check.passed:
                result_dict["dependency_errors"] = result.dependency_check.errors

            if result.output_check and not result.output_check.passed:
                result_dict["output_errors"] = result.output_check.errors
                result_dict["output_warnings"] = result.output_check.warnings

            report["results"].append(result_dict)

        return report

    def _collect_beginner_explanations(self) -> Dict[str, Any]:
        """
        Collect beginner explanations from all simulations.

        Returns:
            Dictionary with beginner guide content from all simulations
        """
        explanations = {
            "title": "Beginner's Guide to Principia Metaphysica",
            "description": "Accessible explanations of the key concepts and predictions",
            "topics": []
        }

        # Collect from all phases in order
        for phase_num in sorted(self.phases.keys()):
            for sim in self.phases[phase_num]:
                # Check if simulation has get_beginner_explanation method
                if hasattr(sim, 'get_beginner_explanation'):
                    try:
                        explanation = sim.get_beginner_explanation()
                        explanation["simulation_id"] = sim.metadata.id
                        explanation["domain"] = sim.metadata.domain
                        explanation["section"] = sim.metadata.section_id
                        explanations["topics"].append(explanation)
                    except Exception as e:
                        if self.verbose:
                            print(f"  Warning: Could not get beginner explanation from {sim.metadata.id}: {e}")

        if self.verbose:
            print(f"  [OK] Collected {len(explanations['topics'])} beginner explanations")

        return explanations

    def _export_to_json(self, validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export registry data and validation to JSON.

        Args:
            validation_report: Validation report dictionary

        Returns:
            Complete output data structure
        """
        if self.verbose:
            print("\n[EXPORT] Generating theory_output.json")
            print("-" * 80)

        # Collect beginner explanations from all simulations
        beginner_explanations = self._collect_beginner_explanations()

        output_data = {
            "metadata": {
                "version": "16.0",
                "timestamp": datetime.now().isoformat(),
                "description": "Principia Metaphysica - Complete Theory Output",
                "schemaMode": self.schema_mode,
            },
            "parameters": self.registry.export_parameters(),
            "formulas": self.registry.export_formulas(),
            "sections": self.registry.export_sections(),
            "provenance": self.registry.export_provenance(),
            "validation": validation_report,
            "beginnerGuide": beginner_explanations,
        }

        # Add schema-compliant simulation results if in schema mode
        if self.schema_mode and self.schema_results:
            output_data["simulationResults"] = self.schema_results

            # Aggregate foundations and references from all simulations
            all_foundations = []
            all_references = []
            for result in self.schema_results:
                all_foundations.extend(result.get("foundations", []))
                all_references.extend(result.get("references", []))

            # Deduplicate by id
            seen_foundation_ids = set()
            unique_foundations = []
            for f in all_foundations:
                if f.get("id") not in seen_foundation_ids:
                    seen_foundation_ids.add(f.get("id"))
                    unique_foundations.append(f)

            seen_reference_ids = set()
            unique_references = []
            for r in all_references:
                if r.get("id") not in seen_reference_ids:
                    seen_reference_ids.add(r.get("id"))
                    unique_references.append(r)

            output_data["foundations"] = unique_foundations
            output_data["references"] = unique_references

        # Write to AutoGenerated/theory_output.json
        output_path = Path(__file__).parent / "AutoGenerated" / "theory_output.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        # Also write beginner guide to separate file
        beginner_guide_path = Path(__file__).parent / "AutoGenerated" / "beginner-guide.json"
        with open(beginner_guide_path, 'w', encoding='utf-8') as f:
            json.dump(beginner_explanations, f, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"[OK] Exported to: {output_path}")
            print(f"  - Parameters: {len(output_data['parameters'])}")
            print(f"  - Formulas: {len(output_data['formulas'])}")
            print(f"  - Sections: {len(output_data['sections'])}")
            print(f"  - Provenance entries: {len(output_data['provenance'])}")
            print(f"  - Beginner guide topics: {len(beginner_explanations['topics'])}")
            print(f"[OK] Beginner guide exported to: {beginner_guide_path}")

        # Split theory_output.json into cacheable components
        self._split_theory_output(output_path)

        return output_data

    def _split_theory_output(self, theory_path: Path) -> None:
        """
        Split theory_output.json into smaller cacheable component files.

        Creates: formulas.json, parameters.json, sections.json, metadata.json,
                 statistics.json, index.json
        """
        if self.verbose:
            print("\n[SPLIT] Generating cacheable component files")
            print("-" * 80)

        output_dir = theory_path.parent

        with open(theory_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. Formulas
        if 'formulas' in data:
            formulas_data = {
                'version': data.get('metadata', {}).get('version', '16.0'),
                'count': len(data['formulas']),
                'formulas': data['formulas']
            }
            formulas_path = output_dir / 'formulas.json'
            with open(formulas_path, 'w', encoding='utf-8') as f:
                json.dump(formulas_data, f, indent=2, ensure_ascii=False)
            if self.verbose:
                print(f"  Created: formulas.json ({len(data['formulas'])} formulas)")

        # 2. Parameters
        if 'parameters' in data:
            params_data = {
                'version': data.get('metadata', {}).get('version', '16.0'),
                'parameters': data['parameters']
            }
            params_path = output_dir / 'parameters.json'
            with open(params_path, 'w', encoding='utf-8') as f:
                json.dump(params_data, f, indent=2, ensure_ascii=False)
            if self.verbose:
                print(f"  Created: parameters.json ({len(data['parameters'])} params)")

        # 3. Sections
        if 'sections' in data:
            sections_data = {
                'version': data.get('metadata', {}).get('version', '16.0'),
                'count': len(data['sections']),
                'sections': data['sections']
            }
            sections_path = output_dir / 'sections.json'
            with open(sections_path, 'w', encoding='utf-8') as f:
                json.dump(sections_data, f, indent=2, ensure_ascii=False)
            if self.verbose:
                print(f"  Created: sections.json ({len(data['sections'])} sections)")

        # 4. Metadata
        metadata = {
            'version': data.get('metadata', {}).get('version', '16.0'),
            'timestamp': data.get('metadata', {}).get('timestamp'),
            'validation': data.get('validation', {})
        }
        metadata_path = output_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        if self.verbose:
            print(f"  Created: metadata.json")

        # 5. Statistics
        stats_data = {
            'version': data.get('metadata', {}).get('version', '16.0'),
            'statistics': data.get('statistics', {}),
            'framework_statistics': data.get('framework_statistics', {})
        }
        stats_path = output_dir / 'statistics.json'
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        if self.verbose:
            print(f"  Created: statistics.json")

        # 6. Index file
        index = {
            'version': data.get('metadata', {}).get('version', '16.0'),
            'components': [
                {'name': 'formulas', 'file': 'formulas.json'},
                {'name': 'parameters', 'file': 'parameters.json'},
                {'name': 'sections', 'file': 'sections.json'},
                {'name': 'metadata', 'file': 'metadata.json'},
                {'name': 'statistics', 'file': 'statistics.json'},
                {'name': 'beginner-guide', 'file': 'beginner-guide.json'},
            ]
        }
        index_path = output_dir / 'index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        if self.verbose:
            print(f"  Created: index.json")
            print(f"[OK] Split into {len(index['components'])} component files")

    def _print_summary(self, validation_report: Dict[str, Any]) -> None:
        """
        Print final summary of simulation run.

        Args:
            validation_report: Validation report dictionary
        """
        if not self.verbose:
            return

        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        passed = validation_report["simulations_passed"]
        failed = validation_report["simulations_failed"]
        total = validation_report["simulations_run"]
        total_time = validation_report["total_execution_time_ms"]

        print(f"Simulations Run:    {total}")
        print(f"Passed:             {passed}")
        print(f"Failed:             {failed}")
        print(f"Success Rate:       {100.0 * passed / total:.1f}%")
        print(f"Total Time:         {total_time:.2f}ms")

        if failed > 0:
            print("\nFailed Simulations:")
            for result_dict in validation_report["results"]:
                if result_dict["status"] == "FAILED":
                    sim_id = result_dict["simulation_id"]
                    error = result_dict.get("error_message", "Unknown error")
                    print(f"  [X] {sim_id}: {error}")

        print("\n" + "=" * 80)

        if failed == 0:
            print("[OK] ALL SIMULATIONS PASSED")
        else:
            print(f"[X] {failed} SIMULATION(S) FAILED")

        print("=" * 80)


def main():
    """Main entry point for running all simulations."""
    import argparse

    parser = argparse.ArgumentParser(description="Run all Principia Metaphysica simulations")
    parser.add_argument(
        "--schema", "-s",
        action="store_true",
        help="Enable schema-compliant execution mode (includes full metadata)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress verbose output"
    )

    args = parser.parse_args()

    # Create runner and execute
    runner = SimulationRunner(
        verbose=not args.quiet,
        schema_mode=args.schema
    )
    output_data = runner.run_all()

    # Return exit code based on results
    validation = output_data["validation"]
    exit_code = 0 if validation["simulations_failed"] == 0 else 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
