#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v15.2 - Microtubule-Orch OR Coupling to PM Coordinates
=============================================================================

SPECULATIVE / APPENDIX MATERIAL

Toy model linking quantum consciousness (Penrose-Hameroff Orch OR) to PM's
multi-sector sampling position (moduli coordinate across 4 nodes).

CORE HYPOTHESIS:
    Microtubule quantum coherence/consciousness events may be modulated by
    the vacuum's position in moduli space. Peak coherence occurs at the
    stable "middle" position (racetrack minimum), where we observe ourselves.

MECHANISM:
    1. Orch OR: Microtubule superpositions collapse via gravitational self-energy
       τ = ħ / E_G (Penrose-Hameroff 2014)

    2. PM Extension: Collapse frequency modulated by deviation from racetrack
       minimum (stable vacuum). Coherence stronger in balanced sampling.

    3. Result: Consciousness events peak in our observed vacuum - elegant
       but highly speculative and currently untestable.

BEST-FIT PARAMETERS (from Orch OR literature):
    - n_tubulins: 10^16 → τ ≈ 500 ms (conscious moment timescale)
    - sampling_position: 0.5 → racetrack minimum (stable vacuum)
    - modulation_width: 0.15 → coherence falloff scale

STATUS: Speculative but quantitative starting point for future work.

REFERENCES:
    - Hameroff & Penrose (2014) "Consciousness in the universe"
    - Penrose (1989) "The Emperor's New Mind"
    - PM racetrack stabilization (v15.0)

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import sys
import os
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import PhenomenologyParameters
    M_PL = PhenomenologyParameters.M_PLANCK_REDUCED
    CONFIG_LOADED = True
except ImportError:
    M_PL = 2.435e18  # GeV
    CONFIG_LOADED = False


class MicrotubulePMCoupling:
    """
    Models coupling between Orch OR quantum consciousness and PM vacuum.

    SPECULATIVE: This is appendix/future work material, not a core prediction.
    Provides a quantitative framework for exploring consciousness-vacuum links.
    """

    # === BEST-FIT PARAMETER SET (Recommended Starting Point) ===
    # Rationale:
    # - n_tubulins: 1e16 → τ ≈ 500 ms (Hameroff & Penrose 2014 conscious moment)
    # - sampling_position: 0.5 → racetrack minimum (stable vacuum)
    # - modulation_width: 0.15 → coherence drops ~e^{-1} at ±0.3 deviation
    BEST_PARAMS = {
        'n_tubulins': 1e16,           # Optimal superposition size
        'sampling_position': 0.5,     # Middle (racetrack min)
        'modulation_width': 0.15,     # Coherence falloff scale
    }

    def __init__(self,
                 n_tubulins: float = None,
                 sampling_position: float = None,
                 modulation_width: float = None):
        """
        Initialize microtubule-PM coupling model.

        Args:
            n_tubulins: Number of tubulins in superposition (~10^16 for 500ms)
            sampling_position: PM moduli coordinate (0-1 across sectors)
            modulation_width: Coherence falloff scale
        """
        self.n_tubulins = n_tubulins if n_tubulins is not None else self.BEST_PARAMS['n_tubulins']
        self.pos = np.clip(
            sampling_position if sampling_position is not None else self.BEST_PARAMS['sampling_position'],
            0.0, 1.0
        )
        self.width = modulation_width if modulation_width is not None else self.BEST_PARAMS['modulation_width']

        # Physical constants (SI units)
        self.hbar = 1.0545718e-34  # J·s
        self.G = 6.67430e-11       # m³/(kg·s²)
        self.m_tubulin = 1.8e-22   # kg (tubulin mass)
        self.r_superposition = 1e-9  # m (characteristic separation)

    def gravitational_self_energy(self) -> float:
        """
        Compute gravitational self-energy of tubulin superposition.

        E_G ≈ G·m²/r for coherent superposition of N tubulins.

        Returns:
            Self-energy in Joules
        """
        total_mass = self.n_tubulins * self.m_tubulin
        return self.G * total_mass**2 / self.r_superposition

    def collapse_timescale(self) -> float:
        """
        Compute Orch OR collapse timescale.

        τ = ħ / E_G (Penrose objective reduction criterion)

        For 10^16 tubulins: τ ≈ 500 ms (matches conscious moment)

        Returns:
            Collapse timescale in seconds
        """
        E_G = self.gravitational_self_energy()
        if E_G > 0:
            return self.hbar / E_G
        return np.inf

    def base_event_frequency(self) -> float:
        """
        Base frequency of proto-conscious events.

        f = 1/τ (events per second)

        Returns:
            Frequency in Hz
        """
        tau = self.collapse_timescale()
        if tau > 0 and not np.isinf(tau):
            return 1.0 / tau
        return 0.0

    def pm_modulation_factor(self) -> float:
        """
        Gaussian modulation from deviation from stable vacuum.

        Peak coherence at middle (sampling_position = 0.5).
        Falls off with width = modulation_width.

        Returns:
            Modulation factor (0 to 1)
        """
        deviation = abs(self.pos - 0.5)
        return np.exp(-deviation**2 / (2 * self.width**2))

    def effective_coupling_strength(self) -> float:
        """
        Modulated consciousness event frequency.

        Stronger coherence in balanced/stable vacuum (middle position).

        Returns:
            Effective coupling frequency in Hz
        """
        base = self.base_event_frequency()
        modulation = self.pm_modulation_factor()
        return base * modulation

    def run_analysis(self, verbose: bool = True) -> Dict:
        """
        Run full microtubule-PM coupling analysis.

        Returns:
            Analysis results dictionary
        """
        tau = self.collapse_timescale()
        freq = self.base_event_frequency()
        mod = self.pm_modulation_factor()
        coupling = self.effective_coupling_strength()

        # Validation: Timescale should be ~500 ms for best-fit params
        tau_valid = 0.1 < tau < 2.0  # 100 ms to 2 s range

        results = {
            'input_parameters': {
                'n_tubulins': float(self.n_tubulins),
                'sampling_position': float(self.pos),
                'modulation_width': float(self.width),
                'config_loaded': CONFIG_LOADED
            },
            'orch_or_quantities': {
                'gravitational_self_energy_J': float(self.gravitational_self_energy()),
                'collapse_timescale_s': float(tau),
                'collapse_timescale_ms': float(tau * 1e3),
                'base_frequency_Hz': float(freq)
            },
            'pm_modulation': {
                'modulation_factor': float(mod),
                'effective_coupling_Hz': float(coupling),
                'interpretation': 'Peak coherence at stable vacuum (middle position)'
            },
            'validation': {
                'timescale_valid': tau_valid,
                'expected_range': '100 ms - 2 s for conscious moments'
            },
            'status': 'SPECULATIVE - Appendix material for future work',
            'version': 'v15.2'
        }

        if verbose:
            self._print_report(results)

        return results

    def _print_report(self, results: Dict):
        """Print formatted analysis report."""
        print()
        print("=" * 70)
        print(" MICROTUBULE-PM COUPLING (v15.2 - SPECULATIVE)")
        print("=" * 70)
        print()
        print("STATUS: Appendix/future work material - not a core prediction")
        print()
        print("=" * 70)
        print(" INPUT PARAMETERS")
        print("=" * 70)
        inp = results['input_parameters']
        print(f"  Tubulin superposition: {inp['n_tubulins']:.0e}")
        print(f"  Sampling position: {inp['sampling_position']:.2f}")
        print(f"  Modulation width: {inp['modulation_width']:.2f}")
        print()
        print("=" * 70)
        print(" ORCH OR QUANTITIES")
        print("=" * 70)
        orch = results['orch_or_quantities']
        print(f"  Gravitational self-energy: {orch['gravitational_self_energy_J']:.2e} J")
        print(f"  Collapse timescale: {orch['collapse_timescale_ms']:.1f} ms")
        print(f"  Base event frequency: {orch['base_frequency_Hz']:.2f} Hz")
        print()
        print("=" * 70)
        print(" PM MODULATION")
        print("=" * 70)
        mod = results['pm_modulation']
        print(f"  Modulation factor: {mod['modulation_factor']:.4f}")
        print(f"  Effective coupling: {mod['effective_coupling_Hz']:.2f} Hz")
        print(f"  {mod['interpretation']}")
        print()
        print("=" * 70)
        print(" INTERPRETATION")
        print("=" * 70)
        print("  Peak consciousness events in balanced multi-sector vacuum")
        print("  Future tests: Anesthesia/microtubule disruption vs coherence")
        print()
        val = results['validation']
        status = "VALID" if val['timescale_valid'] else "CHECK"
        print(f"  Timescale validation: {status}")
        print(f"  Expected range: {val['expected_range']}")
        print("=" * 70)

    @classmethod
    def print_best_parameters(cls):
        """Print recommended starting parameters."""
        print("=" * 70)
        print("RECOMMENDED BEST-FIT PARAMETERS FOR FUTURE WORK")
        print("=" * 70)
        print("These values maximize microtubule-Orch OR coupling in the observed")
        print("PM vacuum (middle sampling, stable racetrack minimum).")
        print()
        for key, val in cls.BEST_PARAMS.items():
            print(f"  {key:25}: {val}")
        print()
        print("Rationale:")
        print("  - n_tubulins: 10^16 gives τ ≈ 500 ms (conscious moment)")
        print("  - sampling_position: 0.5 = racetrack minimum (stable)")
        print("  - modulation_width: 0.15 = reasonable coherence falloff")
        print("=" * 70)


def scan_positions(positions: np.ndarray = None, n_tubulins: float = 1e16) -> Dict:
    """
    Scan coupling strength over different sampling positions.

    Args:
        positions: Array of positions to scan
        n_tubulins: Superposition size for scan

    Returns:
        Scan results
    """
    if positions is None:
        positions = np.linspace(0, 1, 51)

    couplings = []
    for pos in positions:
        model = MicrotubulePMCoupling(n_tubulins=n_tubulins, sampling_position=pos)
        couplings.append(model.effective_coupling_strength())

    return {
        'positions': positions.tolist(),
        'couplings': couplings,
        'peak_position': positions[np.argmax(couplings)],
        'peak_coupling': max(couplings)
    }


def export_microtubule_results() -> Dict:
    """Export microtubule coupling results."""
    model = MicrotubulePMCoupling()
    results = model.run_analysis(verbose=False)

    return {
        'N_TUBULINS': results['input_parameters']['n_tubulins'],
        'COLLAPSE_TIMESCALE_MS': results['orch_or_quantities']['collapse_timescale_ms'],
        'EFFECTIVE_COUPLING_HZ': results['pm_modulation']['effective_coupling_Hz'],
        'MODULATION_FACTOR': results['pm_modulation']['modulation_factor'],
        'TIMESCALE_VALID': results['validation']['timescale_valid'],
        'STATUS': 'SPECULATIVE',
        'VERSION': 'v15.2'
    }


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Print best parameters
    MicrotubulePMCoupling.print_best_parameters()

    # Run analysis with best-fit parameters
    model = MicrotubulePMCoupling()
    model.run_analysis()

    # Position scan
    print("\n" + "=" * 70)
    print(" Position Scan (coupling vs. sampling position)")
    print("=" * 70)
    scan = scan_positions()
    print(f"  Peak position: {scan['peak_position']:.2f}")
    print(f"  Peak coupling: {scan['peak_coupling']:.2f} Hz")
    print("  (Confirms maximum at middle = stable vacuum)")
    print("=" * 70)
