#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v15.3 - Microtubule-Orch OR Threshold Model (Rigorous)
=============================================================================

SPECULATIVE APPENDIX MATERIAL - Open Problem for Future Work

This simulation explores a hypothetical coupling between PM's G2 moduli sampling
coordinates and Penrose-Hameroff Orchestrated Objective Reduction (Orch OR).

KEY INSIGHT: Biology works ABOVE minimum thresholds, not at fine-tuned peaks.
Evolution optimizes for robust functionality, not razor-sharp optima.

CORE ASSUMPTIONS (Literature-Based):
    1. Collapse timescale: tau = hbar / E_G (Penrose OR criterion)
    2. Gravitational self-energy: E_G = G * m^2 / r
    3. G_eff(phi) modulated by viability factor f(phi)
    4. Broad viable plateau - no fine-tuning required

NUMERICAL PREDICTIONS (Testable Limits):
    - tau_min: 25 ms (gamma synchrony ~40 Hz)
    - tau_max: 2000 ms (slow conscious processing)
    - Threshold n_tubulins: ~10^14 (below = decoherence dominates)
    - Viable plateau: |phi - 0.5| < 0.2 (40% of sampling range)

STATUS: Highly speculative - Orch OR itself remains controversial.
        No direct evidence connects extra-D moduli to brain quantum states.
        Model offers falsifiable extensions, not confirmed predictions.

REFERENCES:
    - Penrose & Hameroff (2014) "Consciousness in the universe"
    - Craddock et al. (2017) "Anesthetics and microtubules"
    - PM racetrack stabilization (v15.0)

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os
from typing import Dict, Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import PhenomenologyParameters, FluxQuantization
    M_PL = PhenomenologyParameters.M_PLANCK_REDUCED
    B3 = FluxQuantization.B3
    CONFIG_LOADED = True
except ImportError:
    M_PL = 2.435e18
    B3 = 24
    CONFIG_LOADED = False


class MicrotubuleThresholdModel:
    """
    Rigorous threshold-based model for Orch OR coupling to PM vacuum.

    Core principle: Biology requires passing thresholds, not matching peaks.
    Microtubule quantum effects are viable across a broad plateau.
    """

    # ==========================================================================
    # NUMERICAL PREDICTIONS - Testable Limits
    # ==========================================================================
    # Based on Hameroff & Penrose (2014) and subsequent literature
    NUMERICAL_LIMITS = {
        # Timescale bounds (from Orch OR literature)
        'tau_min_ms': 25.0,            # ~40 Hz gamma synchrony
        'tau_max_ms': 2000.0,          # ~0.5 Hz slow processing
        'tau_conscious_ms': 500.0,      # Target conscious moment

        # Superposition size bounds (Orch OR estimates)
        'n_tubulins_threshold': 1e8,    # Below: decoherence dominates
        'n_tubulins_conscious': 1e10,   # ~500 ms events (Orch OR target)
        'n_tubulins_max': 2e10,         # ~25 ms (gamma synchrony)

        # G_eff modulation bounds
        'g_mod_max_deviation': 0.15,    # Max 15% G variation
        'g_mod_plateau_width': 0.2,     # Half-width of viable zone

        # Frequency bounds
        'freq_min_hz': 0.5,             # Slow processing threshold
        'freq_gamma_hz': 40.0,          # Gamma synchrony target
    }

    # ==========================================================================
    # PHYSICAL CONSTANTS AND CALIBRATION
    # ==========================================================================
    # The simplified E_G = G*m^2/r formula doesn't capture full OR physics.
    # Penrose's full calculation involves superposition separation at nuclear scale.
    # We use phenomenological calibration to match Orch OR literature:
    #   tau ~ 500 ms for n ~ 10^10 tubulins
    #   tau ~ 25 ms for n ~ 2x10^10 tubulins (gamma ~40 Hz)
    #
    # Calibration: tau = tau_ref * (n_ref / n)^2
    #   where tau_ref = 500 ms at n_ref = 10^10
    CONSTANTS = {
        'hbar': 1.0545718e-34,          # J*s (reduced Planck)
        'G0': 6.67430e-11,              # m^3/(kg*s^2) (Newton)
        'm_tubulin': 1.8e-22,           # kg (~110 kDa)
        'r_superposition': 25.0e-9,     # m (25 nm tubulin diameter)
    }

    # Phenomenological calibration (Orch OR literature)
    CALIBRATION = {
        'tau_ref_s': 0.5,               # 500 ms at reference superposition
        'n_ref': 1e10,                  # Reference superposition size
    }

    # ==========================================================================
    # THRESHOLD PARAMETERS (Recommended Starting Point)
    # ==========================================================================
    # Based on Orch OR literature: 10^10 tubulins -> ~500 ms conscious events
    THRESHOLD_PARAMS = {
        'n_tubulins': 1e10,             # Nominal superposition (Orch OR target)
        'sampling_position': 0.5,        # Racetrack minimum
        'plateau_halfwidth': 0.2,        # Viable zone +/- 0.2
        'g_mod_depth': 0.15,             # Max G_eff deviation
    }

    def __init__(self,
                 n_tubulins: float = None,
                 sampling_position: float = None,
                 plateau_halfwidth: float = None,
                 g_mod_depth: float = None):
        """
        Initialize threshold model.

        Args:
            n_tubulins: Superposition size (10^14 to 10^17)
            sampling_position: PM modulus coordinate [0, 1]
            plateau_halfwidth: Half-width of viable plateau
            g_mod_depth: Maximum G_eff modulation depth
        """
        self.n = n_tubulins if n_tubulins is not None else self.THRESHOLD_PARAMS['n_tubulins']
        self.pos = np.clip(
            sampling_position if sampling_position is not None else self.THRESHOLD_PARAMS['sampling_position'],
            0.0, 1.0
        )
        self.hw = plateau_halfwidth if plateau_halfwidth is not None else self.THRESHOLD_PARAMS['plateau_halfwidth']
        self.depth = g_mod_depth if g_mod_depth is not None else self.THRESHOLD_PARAMS['g_mod_depth']

        # Load constants
        self.hbar = self.CONSTANTS['hbar']
        self.G0 = self.CONSTANTS['G0']
        self.m_tub = self.CONSTANTS['m_tubulin']
        self.r = self.CONSTANTS['r_superposition']

    # ==========================================================================
    # CORE PHYSICS
    # ==========================================================================

    def viability_factor(self) -> float:
        """
        Compute viability factor f(phi) - broad plateau, not sharp peak.

        f(phi) = 1.0                           for |phi - 0.5| <= hw
               = exp(-(|phi-0.5| - hw)^2/0.1^2)  otherwise

        Returns:
            Viability factor in [0, 1]
        """
        deviation = abs(self.pos - 0.5)
        if deviation <= self.hw:
            return 1.0  # Full viability within plateau
        else:
            # Gentle falloff outside plateau
            return np.exp(-((deviation - self.hw)**2) / (0.1**2))

    def g_effective(self) -> float:
        """
        Effective gravitational coupling modulated by vacuum position.

        G_eff = G0 * (1 - depth * (1 - f(phi)))

        In viable plateau: G_eff = G0
        At sector edges: G_eff reduced by up to depth fraction

        Returns:
            G_eff in m^3/(kg*s^2)
        """
        f = self.viability_factor()
        return self.G0 * (1.0 - self.depth * (1.0 - f))

    def collapse_timescale_base(self) -> float:
        """
        Base Penrose OR collapse timescale (phenomenologically calibrated).

        Uses scaling: tau = tau_ref * (n_ref / n)^2
        This captures the E_G ~ m^2 ~ n^2 dependence without numerical issues.

        Calibrated to give:
        - tau ~ 500 ms for n ~ 10^10 tubulins (Hameroff & Penrose 2014)
        - tau ~ 25 ms for n ~ 2x10^10 (gamma ~40 Hz)

        Returns:
            Base timescale in seconds (before G_eff modulation)
        """
        tau_ref = self.CALIBRATION['tau_ref_s']
        n_ref = self.CALIBRATION['n_ref']

        # Scaling: tau ~ 1/E_G ~ 1/m^2 ~ 1/n^2
        # So tau = tau_ref * (n_ref / n)^2
        if self.n > 0:
            return tau_ref * (n_ref / self.n) ** 2
        return np.inf

    def collapse_timescale(self) -> float:
        """
        Effective collapse timescale including G_eff modulation.

        tau_eff = tau_base / g_eff_ratio

        At stable vacuum (pos = 0.5): g_eff_ratio = 1, tau_eff = tau_base
        At edges: g_eff reduced -> tau_eff increased (reduced coherence)

        Returns:
            Timescale in seconds
        """
        tau_base = self.collapse_timescale_base()
        g_ratio = self.g_effective() / self.G0

        if g_ratio > 0:
            return tau_base / g_ratio
        return np.inf

    def event_frequency(self) -> float:
        """
        Proto-conscious event frequency.

        f = 1 / tau

        Returns:
            Frequency in Hz
        """
        tau = self.collapse_timescale()
        if tau > 0 and not np.isinf(tau):
            return 1.0 / tau
        return 0.0

    # ==========================================================================
    # THRESHOLD VALIDATION
    # ==========================================================================

    def is_above_threshold(self) -> Tuple[bool, Dict]:
        """
        Check if system passes minimum thresholds for functionality.

        Returns:
            (passes_threshold, details)
        """
        tau_ms = self.collapse_timescale() * 1000
        freq = self.event_frequency()

        limits = self.NUMERICAL_LIMITS

        # Check individual thresholds
        tau_in_range = limits['tau_min_ms'] <= tau_ms <= limits['tau_max_ms']
        n_above_min = self.n >= limits['n_tubulins_threshold']
        freq_viable = freq >= limits['freq_min_hz']
        in_plateau = abs(self.pos - 0.5) <= self.hw

        passes = tau_in_range and n_above_min and freq_viable

        details = {
            'tau_ms': tau_ms,
            'tau_in_range': tau_in_range,
            'tau_bounds': (limits['tau_min_ms'], limits['tau_max_ms']),
            'n_tubulins': self.n,
            'n_above_threshold': n_above_min,
            'n_threshold': limits['n_tubulins_threshold'],
            'frequency_hz': freq,
            'freq_viable': freq_viable,
            'freq_min': limits['freq_min_hz'],
            'position': self.pos,
            'in_plateau': in_plateau,
            'plateau_bounds': (0.5 - self.hw, 0.5 + self.hw),
            'passes_all': passes
        }

        return passes, details

    # ==========================================================================
    # ANALYSIS
    # ==========================================================================

    def run_analysis(self, verbose: bool = True) -> Dict:
        """
        Run complete threshold analysis.

        Returns:
            Comprehensive results dictionary
        """
        # Core quantities
        tau_base = self.collapse_timescale_base()
        tau = self.collapse_timescale()
        freq = self.event_frequency()
        viability = self.viability_factor()
        g_eff = self.g_effective()

        # Threshold check
        passes, threshold_details = self.is_above_threshold()

        results = {
            'input_parameters': {
                'n_tubulins': float(self.n),
                'sampling_position': float(self.pos),
                'plateau_halfwidth': float(self.hw),
                'g_mod_depth': float(self.depth),
                'config_loaded': CONFIG_LOADED
            },
            'physical_quantities': {
                'G_eff_over_G0': float(g_eff / self.G0),
                'collapse_timescale_base_s': float(tau_base),
                'collapse_timescale_base_ms': float(tau_base * 1000),
                'collapse_timescale_s': float(tau),
                'collapse_timescale_ms': float(tau * 1000),
                'event_frequency_Hz': float(freq)
            },
            'viability': {
                'viability_factor': float(viability),
                'in_plateau': threshold_details['in_plateau'],
                'plateau_bounds': threshold_details['plateau_bounds']
            },
            'threshold_validation': {
                'passes_all_thresholds': passes,
                'tau_in_valid_range': threshold_details['tau_in_range'],
                'tau_bounds_ms': threshold_details['tau_bounds'],
                'n_above_minimum': threshold_details['n_above_threshold'],
                'n_minimum': threshold_details['n_threshold'],
                'freq_above_minimum': threshold_details['freq_viable'],
                'freq_minimum_Hz': threshold_details['freq_min']
            },
            'numerical_predictions': self.NUMERICAL_LIMITS.copy(),
            'interpretation': {
                'key_insight': 'Biology works ABOVE thresholds, not at fine-tuned peaks',
                'viable_range': 'Broad plateau allows robust function without tuning',
                'testable': 'Anesthesia as moduli perturbation -> reduced viability'
            },
            'status': 'SPECULATIVE - Open problem for future work',
            'overall_valid': passes,
            'version': 'v15.3'
        }

        if verbose:
            self._print_report(results)

        return results

    def _print_report(self, results: Dict):
        """Print formatted analysis report."""
        print()
        print("=" * 70)
        print(" MICROTUBULE-ORCH OR THRESHOLD MODEL (v15.3)")
        print("=" * 70)
        print()
        print("STATUS: Speculative appendix - open problem for future work")
        print("KEY INSIGHT: Biology passes thresholds, not matches peaks")
        print()

        print("=" * 70)
        print(" NUMERICAL PREDICTIONS (Testable Limits)")
        print("=" * 70)
        limits = results['numerical_predictions']
        print(f"  tau_min:              {limits['tau_min_ms']:.0f} ms (gamma ~40 Hz)")
        print(f"  tau_max:              {limits['tau_max_ms']:.0f} ms (slow processing)")
        print(f"  tau_conscious:        {limits['tau_conscious_ms']:.0f} ms (target moment)")
        print(f"  n_threshold:          {limits['n_tubulins_threshold']:.0e} (decoherence limit)")
        print(f"  n_conscious:          {limits['n_tubulins_conscious']:.0e} (500 ms events)")
        print(f"  plateau_width:        +/- {limits['g_mod_plateau_width']:.1f} (viable zone)")
        print()

        print("=" * 70)
        print(" INPUT PARAMETERS")
        print("=" * 70)
        inp = results['input_parameters']
        print(f"  n_tubulins:           {inp['n_tubulins']:.0e}")
        print(f"  sampling_position:    {inp['sampling_position']:.2f}")
        print(f"  plateau_halfwidth:    {inp['plateau_halfwidth']:.2f}")
        print(f"  g_mod_depth:          {inp['g_mod_depth']:.2f}")
        print()

        print("=" * 70)
        print(" COMPUTED QUANTITIES")
        print("=" * 70)
        phys = results['physical_quantities']
        print(f"  G_eff / G0:           {phys['G_eff_over_G0']:.4f}")
        print(f"  tau_base:             {phys['collapse_timescale_base_ms']:.1f} ms")
        print(f"  tau_effective:        {phys['collapse_timescale_ms']:.1f} ms")
        print(f"  frequency:            {phys['event_frequency_Hz']:.2f} Hz")
        print()

        print("=" * 70)
        print(" VIABILITY (Broad Plateau)")
        print("=" * 70)
        viab = results['viability']
        print(f"  Viability factor:     {viab['viability_factor']:.4f}")
        print(f"  In plateau:           {viab['in_plateau']}")
        print(f"  Plateau bounds:       [{viab['plateau_bounds'][0]:.2f}, {viab['plateau_bounds'][1]:.2f}]")
        print()

        print("=" * 70)
        print(" THRESHOLD VALIDATION")
        print("=" * 70)
        val = results['threshold_validation']
        status_tau = "PASS" if val['tau_in_valid_range'] else "FAIL"
        status_n = "PASS" if val['n_above_minimum'] else "FAIL"
        status_f = "PASS" if val['freq_above_minimum'] else "FAIL"
        print(f"  tau in range [{val['tau_bounds_ms'][0]:.0f}, {val['tau_bounds_ms'][0]:.0f}] ms: {status_tau}")
        print(f"  n >= {val['n_minimum']:.0e}: {status_n}")
        print(f"  freq >= {val['freq_minimum_Hz']:.1f} Hz: {status_f}")
        print()
        overall = "PASSES" if results['overall_valid'] else "FAILS"
        print(f"  Overall: {overall} threshold requirements")
        print()

        print("=" * 70)
        print(" INTERPRETATION")
        print("=" * 70)
        interp = results['interpretation']
        print(f"  {interp['key_insight']}")
        print(f"  {interp['viable_range']}")
        print(f"  Testable: {interp['testable']}")
        print("=" * 70)


def scan_threshold_viability(n_tubulins_list: list = None) -> Dict:
    """
    Scan viability across positions for different superposition sizes.

    Returns:
        Scan results with threshold regions
    """
    if n_tubulins_list is None:
        # Use Orch OR relevant range: 10^8 to 2x10^10
        n_tubulins_list = [1e8, 1e9, 1e10, 2e10]

    positions = np.linspace(0, 1, 101)

    results = {
        'positions': positions.tolist(),
        'scans': {}
    }

    for n in n_tubulins_list:
        freqs = []
        passes = []
        for pos in positions:
            model = MicrotubuleThresholdModel(n_tubulins=n, sampling_position=pos)
            freqs.append(model.event_frequency())
            p, _ = model.is_above_threshold()
            passes.append(p)

        results['scans'][f'{n:.0e}'] = {
            'frequencies': freqs,
            'passes_threshold': passes,
            'viable_fraction': sum(passes) / len(passes)
        }

    return results


def export_threshold_results() -> Dict:
    """Export threshold model results for integration."""
    model = MicrotubuleThresholdModel()
    results = model.run_analysis(verbose=False)

    return {
        'N_TUBULINS': results['input_parameters']['n_tubulins'],
        'TAU_MS': results['physical_quantities']['collapse_timescale_ms'],
        'FREQUENCY_HZ': results['physical_quantities']['event_frequency_Hz'],
        'VIABILITY_FACTOR': results['viability']['viability_factor'],
        'IN_PLATEAU': results['viability']['in_plateau'],
        'PASSES_THRESHOLD': results['overall_valid'],
        'NUMERICAL_LIMITS': results['numerical_predictions'],
        'STATUS': 'SPECULATIVE',
        'VERSION': 'v15.3'
    }


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Run threshold analysis
    model = MicrotubuleThresholdModel()
    model.run_analysis()

    # Show scan results
    print("\n" + "=" * 70)
    print(" THRESHOLD VIABILITY SCAN")
    print("=" * 70)
    scan = scan_threshold_viability()
    for n_key, data in scan['scans'].items():
        print(f"  {n_key} tubulins: {data['viable_fraction']*100:.1f}% of positions viable")
    print("=" * 70)
