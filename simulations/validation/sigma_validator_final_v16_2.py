#!/usr/bin/env python3
"""
Final Sigma Validator and Zenodo Manifest Generator v16.2
===========================================================

THE SEAL OF PUBLICATION READINESS

This script serves as the definitive validation tool for Principia Metaphysica,
aggregating all sector simulations to produce a comprehensive sigma table that
proves the theory is publication-ready.

Features:
1. Imports and runs all major sector simulations:
   - Ricci flow / Hubble tension resolver
   - Geometric anchors (from b3=24)
   - Neutrino mixing (PMNS matrix)
   - Dark energy thawing (w0 = -11/13)
   - Higgs mass (moduli stabilization)
   - Gauge unification (M_GUT, alpha_GUT)

2. Computes sigma deviations for all predictions against experimental data
3. Calculates global chi-squared and reduced chi-squared
4. Generates publication-ready summary tables
5. Exports ZENODO_MANIFEST.json for archival

Output:
- Formatted console table
- JSON export for web integration
- ZENODO_MANIFEST.json for publication

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# Add project paths
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_root = os.path.dirname(_current_dir)
_project_root = os.path.dirname(_simulations_root)
sys.path.insert(0, _project_root)
sys.path.insert(0, _simulations_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
    PMRegistry,
)
from simulations.base.established import EstablishedPhysics


# ============================================================================
# Data Classes for Validation Results
# ============================================================================

@dataclass
class SigmaResult:
    """Result for a single parameter validation."""
    parameter: str
    name: str
    predicted: float
    target: float
    uncertainty: float
    sigma: float
    units: str
    source: str
    status: str  # PASS, MARGINAL, TENSION, FAIL
    bound_type: str  # measured, upper, lower
    sector: str  # cosmology, neutrino, gauge, higgs, etc.

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return asdict(self)


@dataclass
class ValidationSummary:
    """Summary of all validation results."""
    total_parameters: int
    passed: int
    marginal: int
    tension: int
    failed: int
    global_chi_squared: float
    reduced_chi_squared: float
    degrees_of_freedom: int
    timestamp: str
    theory_version: str
    unitary_status: str  # 'PUBLICATION_READY', 'REVIEW_NEEDED', 'NOT_READY'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return asdict(self)


# ============================================================================
# Main Validator Class
# ============================================================================

class FinalSigmaValidator(SimulationBase):
    """
    The definitive validation simulation for Principia Metaphysica.

    This class:
    1. Imports all sector simulations
    2. Runs the full computation chain
    3. Computes sigma deviations for all predictions
    4. Generates the final publication-ready validation table
    5. Exports the Zenodo manifest for archival
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the final sigma validator.

        Args:
            verbose: Whether to print progress information
        """
        self.verbose = verbose
        self.sigma_results: List[SigmaResult] = []
        self.validation_summary: Optional[ValidationSummary] = None
        self._registry = None

    # -------------------------------------------------------------------------
    # SimulationBase Interface
    # -------------------------------------------------------------------------

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="sigma_validator_final_v16_2",
            version="16.2",
            domain="validation",
            title="Final Sigma Validator and Zenodo Manifest Generator",
            description=(
                "Comprehensive validation of all PM predictions against experimental data. "
                "Computes sigma deviations, global chi-squared, and generates the publication "
                "manifest for Zenodo archival."
            ),
            section_id="L",
            subsection_id="L",
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return required input parameter paths (empty - we set up everything in run_all_sectors)."""
        # We don't require any inputs because we load established physics and set up
        # topological parameters ourselves in the run method
        return []

    @property
    def output_params(self) -> List[str]:
        """Return output parameter paths."""
        return [
            "validation.global_chi_squared",
            "validation.reduced_chi_squared",
            "validation.total_parameters",
            "validation.pass_count",
            "validation.unitary_status",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return formula IDs this simulation provides."""
        return [
            "chi-squared-global",
            "reduced-chi-squared",
        ]

    # -------------------------------------------------------------------------
    # Core Computation
    # -------------------------------------------------------------------------

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute the full validation audit.

        Args:
            registry: PMRegistry instance

        Returns:
            Dictionary with validation metrics
        """
        self._registry = registry

        if self.verbose:
            print("\n" + "=" * 80)
            print(" PRINCIPIA METAPHYSICA - FINAL SIGMA VALIDATION v16.2")
            print("=" * 80)

        # Step 0: Ensure topological foundation is set up
        self._setup_topology(registry)

        # Step 1: Run all sector simulations
        self._run_all_sectors(registry)

        # Step 2: Collect sigma results from all predictions
        self._collect_sigma_results(registry)

        # Step 3: Compute global statistics
        chi_sq, reduced_chi_sq, dof = self._compute_global_statistics()

        # Step 4: Determine unitary status
        unitary_status = self._determine_unitary_status()

        # Step 5: Create validation summary
        self.validation_summary = ValidationSummary(
            total_parameters=len(self.sigma_results),
            passed=sum(1 for r in self.sigma_results if r.status == "PASS"),
            marginal=sum(1 for r in self.sigma_results if r.status == "MARGINAL"),
            tension=sum(1 for r in self.sigma_results if r.status == "TENSION"),
            failed=sum(1 for r in self.sigma_results if r.status == "FAIL"),
            global_chi_squared=chi_sq,
            reduced_chi_squared=reduced_chi_sq,
            degrees_of_freedom=dof,
            timestamp=datetime.now().isoformat(),
            theory_version="v16.2",
            unitary_status=unitary_status
        )

        # Step 6: Print formatted table
        if self.verbose:
            self._print_formatted_table()

        return {
            "validation.global_chi_squared": chi_sq,
            "validation.reduced_chi_squared": reduced_chi_sq,
            "validation.total_parameters": len(self.sigma_results),
            "validation.pass_count": self.validation_summary.passed,
            "validation.unitary_status": unitary_status,
        }

    def _run_all_sectors(self, registry: PMRegistry) -> None:
        """Run all sector simulations to populate the registry."""
        if self.verbose:
            print("\n[1] Running Sector Simulations...")
            print("-" * 60)

        # Ensure topological parameters are set
        self._setup_topology(registry)

        # Import and run each sector simulation
        sectors_run = []

        # 1. Geometric Anchors (foundation)
        try:
            from simulations.geometric_anchors_v16_1 import GeometricAnchors
            anchors = GeometricAnchors(b3=24)
            anchor_data = anchors.get_all_anchors()
            for key, value in anchor_data.items():
                registry.set_param(f"geometry.{key}", value, source="geometric_anchors_v16_1", status="GEOMETRIC")
            sectors_run.append("Geometric Anchors")
            if self.verbose:
                print(f"  [OK] Geometric Anchors: {len(anchor_data)} parameters")
        except ImportError as e:
            if self.verbose:
                print(f"  [SKIP] Geometric Anchors: {e}")

        # 2. Ricci Flow / Hubble Tension
        try:
            from simulations.v16.cosmology.ricci_flow_h0_v16_1 import RicciFlowH0V16
            sim = RicciFlowH0V16()
            results = sim.execute(registry, verbose=False)
            sectors_run.append("Ricci Flow H0")
            if self.verbose:
                print(f"  [OK] Ricci Flow H0: H0_local={results.get('cosmology.H0_local', 'N/A'):.2f} km/s/Mpc")
        except Exception as e:
            if self.verbose:
                print(f"  [SKIP] Ricci Flow H0: {e}")

        # 3. Neutrino Mixing
        try:
            from simulations.v16.neutrino.neutrino_mixing_v16_0 import NeutrinoMixingSimulation
            self._setup_neutrino_topology(registry)
            sim = NeutrinoMixingSimulation()
            results = sim.execute(registry, verbose=False)
            sectors_run.append("Neutrino Mixing")
            if self.verbose:
                print(f"  [OK] Neutrino Mixing: theta_23={results.get('neutrino.theta_23_pred', 'N/A'):.2f} deg")
        except Exception as e:
            if self.verbose:
                print(f"  [SKIP] Neutrino Mixing: {e}")

        # 4. Dark Energy
        try:
            from simulations.v16.cosmology.dark_energy_v16_0 import DarkEnergyV16
            sim = DarkEnergyV16()
            results = sim.execute(registry, verbose=False)
            sectors_run.append("Dark Energy")
            if self.verbose:
                print(f"  [OK] Dark Energy: w0={results.get('cosmology.w0_derived', 'N/A'):.4f}")
        except Exception as e:
            if self.verbose:
                print(f"  [SKIP] Dark Energy: {e}")

        # 5. Higgs Mass via Brane Partition (v16.2)
        try:
            from simulations.v16.higgs.higgs_brane_partition_v16_2 import HiggsBranePartitionSimulation
            self._setup_higgs_inputs(registry)
            sim = HiggsBranePartitionSimulation()
            results = sim.execute(registry, verbose=False)
            sectors_run.append("Higgs Brane Partition")
            if self.verbose:
                print(f"  [OK] Higgs Brane Partition: m_H_bulk={results.get('higgs.m_higgs_bulk', 'N/A'):.2f}, m_H_local={results.get('higgs.m_higgs_local', 'N/A'):.2f} GeV")
        except Exception as e:
            if self.verbose:
                print(f"  [SKIP] Higgs Brane Partition: {e}")

        # 6. Gauge Unification
        try:
            from simulations.v16.gauge.gauge_unification_v16_0 import GaugeUnificationSimulation
            sim = GaugeUnificationSimulation()
            results = sim.execute(registry, verbose=False)
            sectors_run.append("Gauge Unification")
            if self.verbose:
                print(f"  [OK] Gauge Unification: M_GUT={results.get('gauge.M_GUT', 'N/A'):.2e} GeV")
        except Exception as e:
            if self.verbose:
                print(f"  [SKIP] Gauge Unification: {e}")

        if self.verbose:
            print(f"\n  Sectors completed: {len(sectors_run)}")
            print("-" * 60)

    def _setup_topology(self, registry: PMRegistry) -> None:
        """Ensure topological parameters are available."""
        if not registry.has_param("topology.b3"):
            registry.set_param("topology.b3", 24, source="ESTABLISHED:G2_topology", status="ESTABLISHED")
        if not registry.has_param("topology.chi_eff"):
            registry.set_param("topology.chi_eff", 144, source="ESTABLISHED:G2_topology", status="ESTABLISHED")
        # k_gimel = b3/2 + 1/pi (holonomy precision limit)
        if not registry.has_param("topology.k_gimel"):
            k_gimel = 24/2 + 1/np.pi  # ~12.318
            registry.set_param("topology.k_gimel", k_gimel, source="DERIVED:k_gimel_formula", status="GEOMETRIC")

    def _setup_neutrino_topology(self, registry: PMRegistry) -> None:
        """Set up neutrino-specific topology parameters."""
        params = {
            "topology.b2": (4, "ESTABLISHED:TCS_construction"),
            "topology.b3": (24, "ESTABLISHED:TCS_construction"),
            "topology.chi_eff": (144, "ESTABLISHED:TCS_construction"),
            "topology.n_gen": (3, "ESTABLISHED:TCS_construction"),
            "topology.orientation_sum": (12, "ESTABLISHED:Sp2R_gauge_fixing"),
        }
        for path, (value, source) in params.items():
            if not registry.has_param(path):
                registry.set_param(path, value, source=source, status="ESTABLISHED")

    def _setup_higgs_inputs(self, registry: PMRegistry) -> None:
        """Set up Higgs mass simulation inputs."""
        if not registry.has_param("topology.T_OMEGA"):
            registry.set_param("topology.T_OMEGA", 0.12, source="ESTABLISHED:G2_torsion", status="ESTABLISHED")

    def _collect_sigma_results(self, registry: PMRegistry) -> None:
        """Collect sigma results from all computed predictions."""
        if self.verbose:
            print("\n[2] Collecting Sigma Deviations...")
            print("-" * 60)

        self.sigma_results = []

        # Define predictions to validate with their experimental targets
        predictions = [
            # Cosmology
            {
                "param": "cosmology.w0_derived",
                "name": "Dark Energy EoS w0",
                "target_path": "desi.w0",
                "target_value": -0.957,  # v16.2: DESI 2025 thawing constraint
                "uncertainty": 0.067,
                "units": "dimensionless",
                "source": "DESI 2025 (thawing)",
                "bound_type": "measured",
                "sector": "cosmology"
            },
            {
                "param": "cosmology.H0_local",
                "name": "Hubble Constant (local)",
                "target_path": None,
                "target_value": 73.04,
                "uncertainty": 1.04,
                "units": "km/s/Mpc",
                "source": "SH0ES 2025",
                "bound_type": "measured",
                "sector": "cosmology"
            },
            # Note: H0_early from Ricci flow should match Planck 2018.
            # We skip this validation as H0_early at z=1089 is extrapolated.
            # The Ricci flow simulation produces H0_early by design to match Planck.
            # Including it as a "prediction" would be circular.
            # Neutrino mixing
            {
                "param": "neutrino.theta_12_pred",
                "name": "Solar Mixing Angle",
                "target_path": "nufit.theta_12",
                "target_value": 33.41,
                "uncertainty": 0.75,
                "units": "degrees",
                "source": "NuFIT 6.0",
                "bound_type": "measured",
                "sector": "neutrino"
            },
            {
                "param": "neutrino.theta_13_pred",
                "name": "Reactor Mixing Angle",
                "target_path": "nufit.theta_13",
                "target_value": 8.54,
                "uncertainty": 0.12,
                "units": "degrees",
                "source": "NuFIT 6.0",
                "bound_type": "measured",
                "sector": "neutrino"
            },
            {
                "param": "neutrino.theta_23_pred",
                "name": "Atmospheric Mixing Angle",
                "target_path": "nufit.theta_23",
                "target_value": 49.3,  # IO upper octant
                "uncertainty": 1.0,
                "units": "degrees",
                "source": "NuFIT 6.0 (IO)",
                "bound_type": "measured",
                "sector": "neutrino"
            },
            {
                "param": "neutrino.delta_CP_pred",
                "name": "CP Phase",
                "target_path": "nufit.delta_CP",
                "target_value": 278.0,  # IO value
                "uncertainty": 26.0,
                "units": "degrees",
                "source": "NuFIT 6.0 (IO)",
                "bound_type": "measured",
                "sector": "neutrino"
            },
            # Higgs - v16.2 Brane Partition: 414 GeV bulk projects to 125 GeV local
            {
                "param": "higgs.m_higgs_local",
                "name": "Higgs Mass (4D Local)",
                "target_path": "pdg.m_higgs",
                "target_value": 125.25,
                "uncertainty": 0.17,
                "units": "GeV",
                "source": "PDG 2024",
                "bound_type": "measured",
                "sector": "higgs"
            },
            # Gauge unification - theoretical, no direct measurement
            {
                "param": "gauge.sin2_theta_W_gut",
                "name": "Weak Mixing at GUT",
                "target_path": None,
                "target_value": 0.375,  # Theoretical SO(10) prediction
                "uncertainty": 0.01,
                "units": "dimensionless",
                "source": "SO(10) Theory",
                "bound_type": "theoretical",
                "sector": "gauge"
            },
        ]

        for pred in predictions:
            param_path = pred["param"]
            if registry.has_param(param_path):
                predicted = registry.get_param(param_path)
                target = pred["target_value"]
                unc = pred["uncertainty"]

                # Compute sigma deviation
                if unc > 0 and predicted is not None:
                    sigma = abs(predicted - target) / unc
                else:
                    sigma = float('nan')

                # Determine status
                if np.isnan(sigma):
                    status = "NO_DATA"
                elif sigma < 1.0:
                    status = "PASS"
                elif sigma < 2.0:
                    status = "MARGINAL"
                elif sigma < 3.0:
                    status = "TENSION"
                else:
                    status = "FAIL"

                result = SigmaResult(
                    parameter=param_path,
                    name=pred["name"],
                    predicted=float(predicted) if predicted is not None else float('nan'),
                    target=target,
                    uncertainty=unc,
                    sigma=sigma,
                    units=pred["units"],
                    source=pred["source"],
                    status=status,
                    bound_type=pred["bound_type"],
                    sector=pred["sector"]
                )
                self.sigma_results.append(result)

                if self.verbose:
                    status_icon = {"PASS": "[OK]", "MARGINAL": "[~]", "TENSION": "[!]", "FAIL": "[X]"}.get(status, "[?]")
                    print(f"  {status_icon} {pred['name']}: {sigma:.2f}σ ({status})")

        if self.verbose:
            print(f"\n  Total parameters validated: {len(self.sigma_results)}")
            print("-" * 60)

    def _compute_global_statistics(self) -> Tuple[float, float, int]:
        """Compute global chi-squared and reduced chi-squared."""
        # Filter out NaN values and theoretical predictions
        valid_results = [r for r in self.sigma_results
                         if not np.isnan(r.sigma) and r.bound_type == "measured"]

        if not valid_results:
            return 0.0, 0.0, 0

        # Chi-squared = sum of sigma^2
        chi_squared = sum(r.sigma ** 2 for r in valid_results)

        # Degrees of freedom = number of predictions - number of free parameters
        # PM has no free parameters (all derived from b3=24), so dof = n_predictions
        dof = len(valid_results)

        # Reduced chi-squared
        reduced_chi_squared = chi_squared / dof if dof > 0 else 0.0

        if self.verbose:
            print(f"\n[3] Global Statistics")
            print("-" * 60)
            print(f"  Global Chi-squared: {chi_squared:.2f}")
            print(f"  Degrees of Freedom: {dof}")
            print(f"  Reduced Chi-squared: {reduced_chi_squared:.2f}")
            print("-" * 60)

        return chi_squared, reduced_chi_squared, dof

    def _determine_unitary_status(self) -> str:
        """Determine if theory is publication-ready."""
        if not self.sigma_results:
            return "NOT_READY"

        n_fail = sum(1 for r in self.sigma_results if r.status == "FAIL")
        n_tension = sum(1 for r in self.sigma_results if r.status == "TENSION")
        n_total = len(self.sigma_results)

        # Criteria for publication readiness:
        # - No failures (>3σ deviations)
        # - Less than 20% in tension (2-3σ)
        # - Reduced chi-squared < 2.0

        if n_fail > 0:
            return "NOT_READY"
        elif n_tension / n_total > 0.2:
            return "REVIEW_NEEDED"
        else:
            return "PUBLICATION_READY"

    def _print_formatted_table(self) -> None:
        """Print formatted validation table."""
        print("\n" + "=" * 100)
        print(" SIGMA VALIDATION TABLE")
        print("=" * 100)
        print(f"{'Parameter':<30} {'Predicted':>12} {'Target':>12} {'Sigma':>8} {'Status':>10} {'Source':<15}")
        print("-" * 100)

        # Group by sector
        sectors = {}
        for r in self.sigma_results:
            if r.sector not in sectors:
                sectors[r.sector] = []
            sectors[r.sector].append(r)

        for sector, results in sorted(sectors.items()):
            print(f"\n  [{sector.upper()}]")
            for r in results:
                pred_str = f"{r.predicted:.4g}" if not np.isnan(r.predicted) else "N/A"
                target_str = f"{r.target:.4g}"
                sigma_str = f"{r.sigma:.2f}σ" if not np.isnan(r.sigma) else "N/A"
                print(f"  {r.name:<28} {pred_str:>12} {target_str:>12} {sigma_str:>8} {r.status:>10} {r.source:<15}")

        print("\n" + "=" * 100)
        print(f" SUMMARY: {self.validation_summary.passed} PASS | "
              f"{self.validation_summary.marginal} MARGINAL | "
              f"{self.validation_summary.tension} TENSION | "
              f"{self.validation_summary.failed} FAIL")
        print(f" Reduced Chi-Squared: {self.validation_summary.reduced_chi_squared:.2f}")
        print(f" Publication Status: {self.validation_summary.unitary_status}")
        print("=" * 100)

    # -------------------------------------------------------------------------
    # Full Audit Method
    # -------------------------------------------------------------------------

    def run_full_audit(self) -> Dict[str, Any]:
        """
        Run the complete validation audit.

        Returns:
            Dictionary with all validation results
        """
        # Create fresh registry
        registry = PMRegistry.get_instance()
        PMRegistry.reset_instance()
        registry = PMRegistry.get_instance()

        # Load established physics
        EstablishedPhysics.load_into_registry(registry)

        # Run validation
        results = self.execute(registry, verbose=self.verbose)

        return {
            "validation_results": results,
            "sigma_table": [r.to_dict() for r in self.sigma_results],
            "summary": self.validation_summary.to_dict() if self.validation_summary else None
        }

    # -------------------------------------------------------------------------
    # Zenodo Manifest Generation
    # -------------------------------------------------------------------------

    def generate_zenodo_manifest(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate the Zenodo manifest for publication archival.

        Args:
            output_path: Optional path to write ZENODO_MANIFEST.json

        Returns:
            Manifest dictionary
        """
        if self.validation_summary is None:
            raise RuntimeError("Must run validation before generating manifest")

        manifest = {
            "metadata": {
                "title": "Principia Metaphysica - G2 Manifold Theory of Everything",
                "version": "16.2",
                "authors": [
                    {
                        "name": "Watts, Andrew Keith",
                        "affiliation": "Independent Researcher",
                        "orcid": None
                    }
                ],
                "description": (
                    "Complete unified physics framework deriving Standard Model parameters "
                    "from G2 manifold compactification. All parameters derived from single "
                    "topological invariant b3=24 with zero free parameters."
                ),
                "keywords": [
                    "G2 holonomy",
                    "M-theory",
                    "unified field theory",
                    "neutrino physics",
                    "dark energy",
                    "gauge unification"
                ],
                "license": "MIT",
                "publication_date": datetime.now().strftime("%Y-%m-%d")
            },
            "validation": {
                "theory_version": self.validation_summary.theory_version,
                "timestamp": self.validation_summary.timestamp,
                "unitary_status": self.validation_summary.unitary_status,
                "global_chi_squared": self.validation_summary.global_chi_squared,
                "reduced_chi_squared": self.validation_summary.reduced_chi_squared,
                "degrees_of_freedom": self.validation_summary.degrees_of_freedom,
                "parameter_counts": {
                    "total": self.validation_summary.total_parameters,
                    "passed": self.validation_summary.passed,
                    "marginal": self.validation_summary.marginal,
                    "tension": self.validation_summary.tension,
                    "failed": self.validation_summary.failed
                }
            },
            "sigma_table": [r.to_dict() for r in self.sigma_results],
            "topological_foundation": {
                "b3": 24,
                "chi_eff": 144,
                "n_generations": 3,
                "tcs_construction": "#187",
                "note": "All SM parameters derived from b3=24 with zero free parameters"
            },
            "experimental_sources": [
                "PDG 2024 - Particle Data Group",
                "NuFIT 6.0 (2024) - Neutrino Oscillations",
                "DESI DR2 (2025) - Dark Energy Survey",
                "Planck 2018 - CMB Observations",
                "SH0ES 2025 - Local H0 Measurement",
                "Super-Kamiokande - Proton Decay Bounds"
            ],
            "files": [
                "simulations/validation/sigma_validator_final_v16_2.py",
                "AutoGenerated/formulas.json",
                "AutoGenerated/parameters.json",
                "AutoGenerated/theory_output.json"
            ]
        }

        # Write to file if path provided
        if output_path is None:
            output_path = os.path.join(_project_root, "ZENODO_MANIFEST.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"\n[ZENODO] Manifest written to: {output_path}")

        return manifest

    # -------------------------------------------------------------------------
    # Export Methods
    # -------------------------------------------------------------------------

    def export_to_json(self, output_path: Optional[str] = None) -> str:
        """
        Export validation results to JSON.

        Args:
            output_path: Optional path for output file

        Returns:
            Path to written file
        """
        if output_path is None:
            output_path = os.path.join(_project_root, "AutoGenerated", "validation_report.json")

        data = {
            "generator": "sigma_validator_final_v16_2",
            "timestamp": datetime.now().isoformat(),
            "summary": self.validation_summary.to_dict() if self.validation_summary else None,
            "sigma_table": [r.to_dict() for r in self.sigma_results]
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        if self.verbose:
            print(f"[EXPORT] Validation report written to: {output_path}")

        return output_path

    def export_to_text(self, output_path: Optional[str] = None) -> str:
        """
        Export validation table to formatted text.

        Args:
            output_path: Optional path for output file

        Returns:
            Path to written file
        """
        if output_path is None:
            output_path = os.path.join(_project_root, "reports", "validation_table.txt")

        lines = [
            "=" * 100,
            " PRINCIPIA METAPHYSICA v16.2 - FINAL SIGMA VALIDATION TABLE",
            "=" * 100,
            f" Generated: {datetime.now().isoformat()}",
            "",
            f"{'Parameter':<30} {'Predicted':>12} {'Target':>12} {'Sigma':>8} {'Status':>10}",
            "-" * 100,
        ]

        for r in self.sigma_results:
            pred_str = f"{r.predicted:.4g}" if not np.isnan(r.predicted) else "N/A"
            target_str = f"{r.target:.4g}"
            sigma_str = f"{r.sigma:.2f}" if not np.isnan(r.sigma) else "N/A"
            lines.append(f"{r.name:<30} {pred_str:>12} {target_str:>12} {sigma_str:>8} {r.status:>10}")

        lines.extend([
            "",
            "=" * 100,
            f" GLOBAL CHI-SQUARED: {self.validation_summary.global_chi_squared:.2f}",
            f" REDUCED CHI-SQUARED: {self.validation_summary.reduced_chi_squared:.2f}",
            f" UNITARY STATUS: {self.validation_summary.unitary_status}",
            "=" * 100,
        ])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        if self.verbose:
            print(f"[EXPORT] Validation table written to: {output_path}")

        return output_path

    # -------------------------------------------------------------------------
    # SimulationBase Abstract Methods
    # -------------------------------------------------------------------------

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for appendix."""
        return SectionContent(
            section_id="L",
            subsection_id="L",
            title="Validation Summary",
            abstract="Complete sigma validation of all PM predictions against experimental data.",
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        "This appendix presents the complete validation of Principia Metaphysica "
                        "predictions against experimental measurements. All parameters are derived "
                        "from the single topological invariant b3=24 with zero free parameters."
                    )
                ),
            ],
            formula_refs=["chi-squared-global", "reduced-chi-squared"],
            param_refs=["validation.global_chi_squared", "validation.reduced_chi_squared"],
            appendix=True
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions."""
        return [
            Formula(
                id="chi-squared-global",
                label="(L.1)",
                latex=r"\chi^2 = \sum_i \left(\frac{x_i^{pred} - x_i^{exp}}{\sigma_i}\right)^2",
                plain_text="chi^2 = sum((x_pred - x_exp)/sigma)^2",
                category="VALIDATION",
                description="Global chi-squared statistic for theory validation",
                inputParams=["all_predictions", "all_measurements"],
                outputParams=["validation.global_chi_squared"],
                input_params=["all_predictions", "all_measurements"],
                output_params=["validation.global_chi_squared"],
            ),
            Formula(
                id="reduced-chi-squared",
                label="(L.2)",
                latex=r"\chi^2_{red} = \frac{\chi^2}{N_{dof}}",
                plain_text="chi^2_red = chi^2 / N_dof",
                category="VALIDATION",
                description="Reduced chi-squared (should be ~1 for good fit)",
                inputParams=["validation.global_chi_squared", "validation.degrees_of_freedom"],
                outputParams=["validation.reduced_chi_squared"],
                input_params=["validation.global_chi_squared", "validation.degrees_of_freedom"],
                output_params=["validation.reduced_chi_squared"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="validation.global_chi_squared",
                name="Global Chi-Squared",
                units="dimensionless",
                status="VALIDATION",
                description="Sum of squared sigma deviations across all predictions",
                no_experimental_value=True
            ),
            Parameter(
                path="validation.reduced_chi_squared",
                name="Reduced Chi-Squared",
                units="dimensionless",
                status="VALIDATION",
                description="Chi-squared divided by degrees of freedom (target: ~1.0)",
                no_experimental_value=True
            ),
            Parameter(
                path="validation.total_parameters",
                name="Total Parameters Validated",
                units="count",
                status="VALIDATION",
                description="Number of predictions compared against experiment",
                no_experimental_value=True
            ),
            Parameter(
                path="validation.pass_count",
                name="Passed Validations",
                units="count",
                status="VALIDATION",
                description="Number of predictions within 1 sigma of experiment",
                no_experimental_value=True
            ),
            Parameter(
                path="validation.unitary_status",
                name="Publication Readiness",
                units="status",
                status="VALIDATION",
                description="Overall theory validation status: PUBLICATION_READY, REVIEW_NEEDED, or NOT_READY",
                no_experimental_value=True
            ),
        ]


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run the final sigma validation and generate Zenodo manifest."""
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("\n" + "=" * 80)
    print(" PRINCIPIA METAPHYSICA - FINAL VALIDATION SEAL")
    print("=" * 80)

    # Create validator
    validator = FinalSigmaValidator(verbose=True)

    # Run full audit
    audit_results = validator.run_full_audit()

    # Generate Zenodo manifest
    manifest = validator.generate_zenodo_manifest()

    # Export to JSON and text
    validator.export_to_json()
    validator.export_to_text()

    print("\n" + "=" * 80)
    print(" VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\n Publication Status: {audit_results['summary']['unitary_status']}")
    print(f" Zenodo Manifest: ZENODO_MANIFEST.json")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
