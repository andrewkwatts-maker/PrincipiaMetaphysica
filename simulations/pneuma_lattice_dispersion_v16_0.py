#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.0 - Lattice Configuration Dispersion Analysis
========================================================================

Analyzes the δ_lat (Lattice Configuration Dispersion) parameter that modulates
the geometric coupling between PM theory and physical microtubule lattices.

CORE CONCEPT:
    The geometric coupling g_geom from PM theory represents an "ideal" coupling
    assuming perfect embedding of G₂ holonomy geometry in matter. Real physical
    systems may deviate due to lattice-level variations:

    g_eff = g_geom × δ_lat

    where δ_lat ∈ [0.7, 1.5] captures the "quality" of geometric realization.

MAIN PAPER STATUS:
    This is a NEUTRAL STRUCTURAL PARAMETER that acknowledges the potential for
    lattice-level modulation WITHOUT making claims about consciousness or
    evolutionary optimization. It simply loosens the over-constrained cascade
    structure identified in the PM parameter hierarchy.

PHYSICAL MOTIVATION:
    1. PM's cascade structure (TCS G₂ #187 → χ_eff → all parameters) is highly
       constrained, with tensions appearing at δ_CP (1.11σ) and θ₂₃ (exact 45°)
    2. δ_lat provides a physical mechanism for "slack" in the cascade
    3. Biological systems implementing G₂ geometry may have imperfect realizations
    4. This allows the theory to make predictions while acknowledging uncertainty

APPENDIX EXTENSION (Speculative):
    Cross-species predictions suggest δ_lat may correlate with tubulin isoform
    diversity, with humans at δ_lat ≈ 1.45 (see evolutionary_orchestration_v16_1.py)

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os
from typing import Dict, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import (
        LatticeDispersionParameters,
        PneumaVielbeinParameters,
        PneumaRacetrackParameters,
        G2SpinorGeometryParameters
    )
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False
    print("[WARNING] config.py not found - using default values")


class LatticeDispersionAnalysis:
    """
    Analyzes the lattice configuration dispersion parameter δ_lat.

    This class provides tools to:
    1. Compute effective couplings for various δ_lat values
    2. Analyze sensitivity of PM predictions to δ_lat
    3. Compute allowed parameter ranges given δ_lat uncertainty
    4. Generate coupling strength profiles across the valid range
    """

    def __init__(self,
                 delta_lat: float = 1.0,
                 g_geom_base: float = None):
        """
        Initialize lattice dispersion analysis.

        Args:
            delta_lat: Lattice dispersion factor (default 1.0 = baseline)
            g_geom_base: Base geometric coupling (from config if None)
        """
        if CONFIG_LOADED:
            self.delta_lat_min = LatticeDispersionParameters.DELTA_LAT_MIN
            self.delta_lat_max = LatticeDispersionParameters.DELTA_LAT_MAX
            self.delta_lat_baseline = LatticeDispersionParameters.DELTA_LAT_BASELINE
            self.g_geom = g_geom_base or LatticeDispersionParameters.G_GEOM_BASE
        else:
            self.delta_lat_min = 0.7
            self.delta_lat_max = 1.5
            self.delta_lat_baseline = 1.0
            self.g_geom = g_geom_base or 0.1

        # Clamp to valid range
        self.delta_lat = np.clip(delta_lat, self.delta_lat_min, self.delta_lat_max)

    def effective_coupling(self, delta_lat: float = None) -> float:
        """
        Compute effective coupling g_eff = g_geom × δ_lat.

        Args:
            delta_lat: Override delta_lat (uses self.delta_lat if None)

        Returns:
            Effective coupling strength
        """
        d = delta_lat if delta_lat is not None else self.delta_lat
        d = np.clip(d, self.delta_lat_min, self.delta_lat_max)
        return self.g_geom * d

    def coupling_range(self) -> Tuple[float, float]:
        """
        Compute the range of effective couplings over valid δ_lat values.

        Returns:
            (g_eff_min, g_eff_max)
        """
        g_min = self.g_geom * self.delta_lat_min
        g_max = self.g_geom * self.delta_lat_max
        return (g_min, g_max)

    def relative_uncertainty(self) -> float:
        """
        Compute relative uncertainty in coupling from δ_lat range.

        Returns:
            Relative uncertainty (dimensionless)
        """
        g_min, g_max = self.coupling_range()
        g_central = self.g_geom * self.delta_lat_baseline
        return (g_max - g_min) / (2 * g_central)

    def scan_delta_lat(self, n_points: int = 51) -> Dict:
        """
        Scan effective coupling over the valid δ_lat range.

        Args:
            n_points: Number of scan points

        Returns:
            Dictionary with delta_lat values and corresponding g_eff
        """
        delta_values = np.linspace(self.delta_lat_min, self.delta_lat_max, n_points)
        g_eff_values = [self.effective_coupling(d) for d in delta_values]

        return {
            'delta_lat': delta_values.tolist(),
            'g_eff': g_eff_values,
            'g_geom_base': self.g_geom,
            'range': (self.delta_lat_min, self.delta_lat_max)
        }

    def cascade_sensitivity(self) -> Dict:
        """
        Analyze how δ_lat uncertainty propagates through the PM cascade.

        The cascade structure is:
        TCS G₂ #187 → χ_eff=144 → N_flux=24 → n_gen=3, coupling constants, etc.

        δ_lat enters at the coupling level and propagates to:
        - Collapse timescale (τ ∝ 1/g_eff²)
        - Coherence threshold (∝ g_eff)
        - Cross-species predictions

        Returns:
            Sensitivity analysis dictionary
        """
        # Baseline values
        g_baseline = self.g_geom * self.delta_lat_baseline
        g_min, g_max = self.coupling_range()

        # Collapse timescale sensitivity (τ ∝ 1/g²)
        tau_factor_min = (g_baseline / g_max) ** 2  # g_max → smaller τ
        tau_factor_max = (g_baseline / g_min) ** 2  # g_min → larger τ

        # Coherence threshold sensitivity (linear in g)
        coherence_factor_min = g_min / g_baseline
        coherence_factor_max = g_max / g_baseline

        return {
            'coupling_range': (g_min, g_max),
            'coupling_relative_uncertainty': self.relative_uncertainty(),
            'collapse_timescale_factor_range': (tau_factor_min, tau_factor_max),
            'coherence_factor_range': (coherence_factor_min, coherence_factor_max),
            'cascade_impact': 'δ_lat loosens the over-constrained spinner',
            'main_tensions_addressed': [
                'δ_CP (1.11σ from PDG): δ_lat provides slack',
                'θ₂₃ (exact 45°): allows small deviations',
                'd_eff (12.576 precision): relaxes to range'
            ]
        }

    def run_analysis(self, verbose: bool = True) -> Dict:
        """
        Run complete lattice dispersion analysis.

        Returns:
            Complete analysis results
        """
        g_eff = self.effective_coupling()
        g_min, g_max = self.coupling_range()
        sensitivity = self.cascade_sensitivity()

        results = {
            'input_parameters': {
                'delta_lat': float(self.delta_lat),
                'g_geom_base': float(self.g_geom),
                'delta_lat_range': [float(self.delta_lat_min), float(self.delta_lat_max)],
                'config_loaded': CONFIG_LOADED
            },
            'effective_coupling': {
                'g_eff': float(g_eff),
                'g_eff_min': float(g_min),
                'g_eff_max': float(g_max),
                'formula': 'g_eff = g_geom × δ_lat'
            },
            'uncertainty_analysis': {
                'relative_uncertainty': float(self.relative_uncertainty()),
                'coupling_range_factor': float(self.delta_lat_max / self.delta_lat_min),
                'degrees_of_freedom_added': 1,
                'over_constraint_relief': 'Allows cascade to "breathe"'
            },
            'cascade_sensitivity': sensitivity,
            'physical_interpretation': {
                'delta_lat_1.0': 'Perfect geometric embedding (baseline)',
                'delta_lat_lt_1.0': 'Degraded lattice coherence',
                'delta_lat_gt_1.0': 'Enhanced/optimized configuration',
                'mechanism': 'Lattice-level variation in G₂ holonomy realization'
            },
            'status': 'MAIN PAPER - Neutral structural parameter',
            'version': 'v16.0'
        }

        if verbose:
            self._print_report(results)

        return results

    def _print_report(self, results: Dict):
        """Print formatted analysis report."""
        print()
        print("=" * 70)
        print(" LATTICE CONFIGURATION DISPERSION ANALYSIS (v16.0)")
        print("=" * 70)
        print()
        print("STATUS: Main paper - neutral structural parameter")
        print()

        print("=" * 70)
        print(" INPUT PARAMETERS")
        print("=" * 70)
        inp = results['input_parameters']
        print(f"  delta_lat: {inp['delta_lat']:.3f}")
        print(f"  g_geom (base): {inp['g_geom_base']:.4f}")
        print(f"  Valid range: [{inp['delta_lat_range'][0]:.1f}, {inp['delta_lat_range'][1]:.1f}]")
        print()

        print("=" * 70)
        print(" EFFECTIVE COUPLING")
        print("=" * 70)
        eff = results['effective_coupling']
        print(f"  Formula: {eff['formula']}")
        print(f"  g_eff = {eff['g_eff']:.4f}")
        print(f"  Range: [{eff['g_eff_min']:.4f}, {eff['g_eff_max']:.4f}]")
        print()

        print("=" * 70)
        print(" UNCERTAINTY ANALYSIS")
        print("=" * 70)
        unc = results['uncertainty_analysis']
        print(f"  Relative uncertainty: {unc['relative_uncertainty']*100:.1f}%")
        print(f"  Coupling range factor: {unc['coupling_range_factor']:.2f}x")
        print(f"  Additional DOF: {unc['degrees_of_freedom_added']}")
        print(f"  Effect: {unc['over_constraint_relief']}")
        print()

        print("=" * 70)
        print(" CASCADE SENSITIVITY")
        print("=" * 70)
        sens = results['cascade_sensitivity']
        tau_min, tau_max = sens['collapse_timescale_factor_range']
        coh_min, coh_max = sens['coherence_factor_range']
        print(f"  Collapse timescale factor: [{tau_min:.2f}, {tau_max:.2f}]x")
        print(f"  Coherence factor: [{coh_min:.2f}, {coh_max:.2f}]x")
        print()
        print("  Tensions addressed:")
        for tension in sens['main_tensions_addressed']:
            print(f"    - {tension}")
        print()

        print("=" * 70)
        print(" PHYSICAL INTERPRETATION")
        print("=" * 70)
        interp = results['physical_interpretation']
        print(f"  delta_lat = 1.0: {interp['delta_lat_1.0']}")
        print(f"  delta_lat < 1.0: {interp['delta_lat_lt_1.0']}")
        print(f"  delta_lat > 1.0: {interp['delta_lat_gt_1.0']}")
        print(f"  Mechanism: {interp['mechanism']}")
        print("=" * 70)


def scan_species_predictions() -> Dict:
    """
    Generate cross-species δ_lat predictions.

    This is APPENDIX/SPECULATIVE material linking δ_lat to biological complexity.
    See evolutionary_orchestration_v16_1.py for full treatment.
    """
    if CONFIG_LOADED:
        return LatticeDispersionParameters.get_species_predictions()
    else:
        # Default values
        species = {
            'Protozoa': 1.0,
            'Cnidaria': 1.05,
            'Insect': 1.15,
            'Fish': 1.20,
            'Reptile': 1.25,
            'Mammal': 1.30,
            'Primate': 1.38,
            'Human': 1.45
        }
        g_base = 0.1
        delta_max = 1.5
        return {
            name: {
                'delta_lat': delta,
                'g_eff': g_base * delta,
                'alpha_evo': (delta - 1.0) / (delta_max - 1.0)
            }
            for name, delta in species.items()
        }


def export_lattice_dispersion_results() -> Dict:
    """Export lattice dispersion results for theory_output.json."""
    analysis = LatticeDispersionAnalysis()
    results = analysis.run_analysis(verbose=False)

    return {
        'DELTA_LAT_BASELINE': results['input_parameters']['delta_lat'],
        'DELTA_LAT_RANGE': results['input_parameters']['delta_lat_range'],
        'G_GEOM_BASE': results['input_parameters']['g_geom_base'],
        'G_EFF': results['effective_coupling']['g_eff'],
        'G_EFF_RANGE': [
            results['effective_coupling']['g_eff_min'],
            results['effective_coupling']['g_eff_max']
        ],
        'RELATIVE_UNCERTAINTY': results['uncertainty_analysis']['relative_uncertainty'],
        'FORMULA': 'g_eff = g_geom × δ_lat',
        'SPECIES_PREDICTIONS': scan_species_predictions(),
        'STATUS': 'MAIN PAPER - Neutral structural parameter',
        'VERSION': 'v16.0'
    }


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("\n" + "=" * 70)
    print("    PRINCIPIA METAPHYSICA v16.0")
    print("    LATTICE CONFIGURATION DISPERSION ANALYSIS")
    print("=" * 70)

    # Run main analysis at baseline
    print("\n[BASELINE ANALYSIS: delta_lat = 1.0]")
    analysis = LatticeDispersionAnalysis(delta_lat=1.0)
    analysis.run_analysis()

    # Run at human value (speculative)
    print("\n[HUMAN VALUE (SPECULATIVE): delta_lat = 1.45]")
    analysis_human = LatticeDispersionAnalysis(delta_lat=1.45)
    analysis_human.run_analysis()

    # Scan over full range
    print("\n" + "=" * 70)
    print(" FULL RANGE SCAN")
    print("=" * 70)
    scan = analysis.scan_delta_lat(n_points=11)
    print(f"\n  {'delta_lat':>10} | {'g_eff':>10}")
    print(f"  {'-'*10} | {'-'*10}")
    for d, g in zip(scan['delta_lat'], scan['g_eff']):
        print(f"  {d:>10.2f} | {g:>10.4f}")

    # Species predictions (appendix)
    print("\n" + "=" * 70)
    print(" CROSS-SPECIES PREDICTIONS (SPECULATIVE/APPENDIX)")
    print("=" * 70)
    species = scan_species_predictions()
    print(f"\n  {'Species':>12} | {'delta_lat':>10} | {'g_eff':>10} | {'alpha_evo':>10}")
    print(f"  {'-'*12} | {'-'*10} | {'-'*10} | {'-'*10}")
    for name, data in species.items():
        print(f"  {name:>12} | {data['delta_lat']:>10.2f} | {data['g_eff']:>10.4f} | {data['alpha_evo']:>10.2f}")

    print("\n" + "=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    print("""
  The δ_lat parameter provides essential flexibility in the PM cascade:

  1. MAIN PAPER: Neutral structural parameter acknowledging potential
     lattice-level modulation of geometric coupling.

  2. LOOSENS CONSTRAINTS: Addresses over-tight cascade structure that
     showed tensions at δ_CP (1.11σ) and exact θ₂₃ = 45°.

  3. PHYSICAL BASIS: G₂ holonomy geometry may be imperfectly realized
     in physical lattice structures (microtubules, crystals, etc.).

  4. APPENDIX (SPECULATIVE): Cross-species predictions suggest δ_lat
     may correlate with tubulin isoform diversity and neural complexity.

  The parameter adds 1 DOF while providing ~40% range in coupling strength.
""")
    print("=" * 70 + "\n")
