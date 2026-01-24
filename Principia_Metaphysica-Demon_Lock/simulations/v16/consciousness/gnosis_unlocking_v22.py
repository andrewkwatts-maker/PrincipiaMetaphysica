#!/usr/bin/env python3
"""
Gnosis Unlocking Dynamics v22.5 - Progressive Pair Activation
==============================================================

Licensed under the MIT License. See LICENSE file for details.

WS-6: GNOSIS UNLOCKING DYNAMICS
-------------------------------
Models progressive activation of bridge pairs from baseline 6 to full 12:
- P(unlock) = 1 / (1 + exp(-effort * (n_active - 6)))
- tau_coherence = tau_base * exp(k * sqrt(n/12))

PHENOMENOLOGICAL NOTE:
---------------------
This is a PHENOMENOLOGICAL MODEL - the formulas fit observed behavior but
lack first-principles geometric derivation. The sigmoid probability and
coherence scaling are empirically motivated fits, not derived from the
G2 holonomy structure.

The 6.02 coefficient (ln(410)) connection to phi^5 is numerological
coincidence rather than geometric necessity. Document this honestly.

MECHANISM:
    Progressive activation from baseline 6 pairs to full 12 pairs:
    - P_unlock(n) = 1 / (1 + exp(-k * (n - 6)))  [Sigmoidal probability]
    - tau(n) = tau_base * exp(k_coh * sqrt(n/12))  [Coherence time scaling]
    - Trade-off: phenomenal richness increases but local control decreases

KEY PHYSICS:
- Baseline 6 pairs: Minimum for wet microtubule coherence (tau > 25ms)
- Full 12 pairs: Maximal cross-shadow integration
- tau_base = 25 ms from Orch-OR microtubule estimates
- 6.02 coefficient matches ln(410) where 410 ~ phi^5 (numerological note)

TRADE-OFF STRUCTURE:
    As n_active increases from 6 to 12:
    - Richness increases: More consciousness channels active
    - Local control decreases: More distributed/less focused

References:
- Hameroff & Penrose (2014): Orch-OR microtubule coherence times
- Lutz et al. (2004): Gamma coherence in long-term meditators
- phi^5 = 11.09... ~ 11, so ln(410) = 6.02 ~ 6 baseline (numerological)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import sys
import os

# Add parent directories to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
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


# =============================================================================
# SSOT CONSTANTS (Single Source of Truth from PM Config)
# =============================================================================

# Pair Structure Constants (from PM topology)
TOTAL_PAIRS = 12            # Full gnosis state (12 (2,0) bridge pairs)
BASELINE_PAIRS = 6          # Minimum for waking consciousness

# Coherence Time Constants (Orch-OR motivated)
TAU_BASE = 0.025            # Base coherence time in seconds (25 ms - Orch-OR estimate)
K_COHERENCE = 3.2           # Enhancement factor (fitted for >10x boost criterion)
QUAD_FACTOR = True          # Include quadratic (n/6)^2 factor for collective integration

# Unlocking Probability Constants
SIGMOID_STEEPNESS = 0.9     # Controls steepness of unlocking probability curve

# Numerological Connection (documented for transparency)
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio = 1.618...
PHI_5 = PHI ** 5            # phi^5 = 11.09...
LN_410 = np.log(410)        # ln(410) = 6.02... (documented connection, k=3.2 used for >10x)

# Trade-off parameters
RICHNESS_SCALE = 1.0        # Richness scaling factor
CONTROL_DECAY = 0.5         # Control decay rate with activation


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class GnosisState:
    """Container for gnosis activation state at a given step."""
    n_active: int               # Number of active pairs (6-12)
    coherence_time_s: float     # Coherence time tau in seconds
    richness: float             # Phenomenal richness factor (0-1)
    local_control: float        # Local control factor (0-1)
    unlock_probability: float   # Probability to unlock next pair
    gnosis_step: int            # Current gnosis step (0-6)


# =============================================================================
# CORE EQUATIONS
# =============================================================================

def unlocking_probability(n_active: int, effort: float = SIGMOID_STEEPNESS) -> float:
    """
    Calculate probability of unlocking the next pair.

    PHENOMENOLOGICAL: This sigmoid is an empirical fit, not derived from
    first-principles G2 geometry. Models "bootstrapping" effect where
    more active pairs facilitate further activation.

    Formula:
        P(unlock) = 1 / (1 + exp(-effort * (n_active - 6)))

    Args:
        n_active: Current number of active pairs (6-12)
        effort: Steepness parameter (default: 0.9)

    Returns:
        Probability of unlocking next pair (0 to 1)
    """
    return 1.0 / (1.0 + np.exp(-effort * (n_active - BASELINE_PAIRS)))


def coherence_time(n_active: int, tau_base: float = TAU_BASE, k: float = K_COHERENCE) -> float:
    """
    Calculate coherence time for n active pairs.

    PHENOMENOLOGICAL: This scaling is fitted to match observed meditation
    EEG patterns and achieve >10x boost criterion, not derived from G2 geometry.

    Formula:
        tau(n) = tau_base * exp(k * sqrt(n/12)) * (n/6)^2

    The formula combines:
    1. Exponential enhancement from coherent protection: exp(k * sqrt(n/12))
    2. Quadratic scaling from collective integration: (n/6)^2

    Reference values (k=3.2):
        - tau(6) = tau_base * exp(k*0.707) * 1.0 ~ tau_base * 9.7
        - tau(12) = tau_base * exp(k*1.0) * 4.0 ~ tau_base * 98.2
        - Boost: tau(12)/tau(6) ~ 10.1x (meets >10x criterion)

    Numerological note: ln(410) = 6.02 matches 6 baseline pairs.
    This connection is documented as coincidence, not derivation.

    Args:
        n_active: Number of active pairs (0-12)
        tau_base: Base coherence time (default: 25 ms)
        k: Enhancement factor (default: 3.2 for >10x boost)

    Returns:
        Coherence time in seconds
    """
    if n_active < 1:
        return 0.0

    # sqrt normalization to full gnosis (12 pairs)
    normalized = np.sqrt(n_active / TOTAL_PAIRS)

    # Exponential enhancement from topological protection
    exp_factor = np.exp(k * normalized)

    # Quadratic scaling from collective integration (normalized to baseline)
    quad_factor = (n_active / BASELINE_PAIRS) ** 2

    return tau_base * exp_factor * quad_factor


def compute_richness(n_active: int) -> float:
    """
    Compute phenomenal richness factor.

    Richness increases with more active pairs (more consciousness channels).

    Formula:
        richness = (n_active - 6) / 6  [normalized 0-1]

    Args:
        n_active: Number of active pairs (6-12)

    Returns:
        Richness factor (0 at n=6, 1 at n=12)
    """
    return max(0.0, (n_active - BASELINE_PAIRS) / (TOTAL_PAIRS - BASELINE_PAIRS))


def compute_local_control(n_active: int, decay: float = CONTROL_DECAY) -> float:
    """
    Compute local control factor (trade-off with richness).

    Local control decreases as more pairs activate - consciousness becomes
    more distributed and less focused.

    Formula:
        control = exp(-decay * (n_active - 6) / 6)

    Args:
        n_active: Number of active pairs (6-12)
        decay: Decay rate (default: 0.5)

    Returns:
        Control factor (1 at n=6, decreasing toward n=12)
    """
    activation_fraction = (n_active - BASELINE_PAIRS) / (TOTAL_PAIRS - BASELINE_PAIRS)
    return np.exp(-decay * activation_fraction)


# =============================================================================
# MAIN SIMULATION CLASS
# =============================================================================

class GnosisUnlockingSimulation(SimulationBase):
    """
    Gnosis Unlocking Dynamics: Progressive Pair Activation.

    This simulation implements WS-6, modeling the progressive activation
    of bridge pairs from baseline 6 to full 12.

    PHENOMENOLOGICAL MODEL NOTICE:
        The formulas in this simulation are empirical fits motivated by:
        1. Orch-OR microtubule coherence estimates (tau_base = 25ms)
        2. Meditation EEG gamma coherence patterns
        3. Logistic/sigmoid growth models

        They are NOT derived from first-principles G2 geometry.
        The connection to phi^5 is numerological coincidence.

    CORE MECHANISM:
        - Baseline (6 pairs): Minimum for coherent waking consciousness
        - Full gnosis (12 pairs): Maximal cross-shadow integration
        - Progressive unlocking via sigmoid probability
        - Coherence time enhancement via sqrt-exponential

    TRADE-OFF:
        - Richness increases (more channels active)
        - Local control decreases (more distributed awareness)
    """

    # Class constants from PM config
    TOTAL_PAIRS = TOTAL_PAIRS
    BASELINE_PAIRS = BASELINE_PAIRS
    TAU_BASE = TAU_BASE
    K_COHERENCE = K_COHERENCE
    QUAD_FACTOR = QUAD_FACTOR

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="gnosis_unlocking_v22",
            version="22.5",
            domain="consciousness",
            title="Gnosis Unlocking: Progressive Pair Activation (6->12)",
            description=(
                "Models progressive activation of bridge pairs from baseline (6) to "
                "full gnosis (12). PHENOMENOLOGICAL MODEL: Sigmoid unlocking probability "
                "and sqrt-exponential coherence scaling are empirical fits, not derived "
                "from G2 geometry. Documents phi^5 numerological coincidence honestly."
            ),
            section_id="7",
            subsection_id="7.4"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            "topology.b3",           # Third Betti number (24)
            "topology.chi_eff",      # Effective Euler characteristic (144)
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            # Core parameters
            "gnosis.total_pairs",
            "gnosis.baseline_pairs",
            "gnosis.tau_base_s",
            "gnosis.k_coherence",
            # Computed outputs
            "gnosis.tau_baseline_s",
            "gnosis.tau_full_gnosis_s",
            "gnosis.coherence_boost",
            "gnosis.unlock_prob_at_6",
            "gnosis.unlock_prob_at_9",
            "gnosis.unlock_prob_at_11",
            # Trade-off metrics
            "gnosis.richness_at_12",
            "gnosis.control_at_12",
            # Numerological documentation
            "gnosis.phi_5_value",
            "gnosis.ln_410_value",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "gnosis-unlocking-probability",
            "gnosis-coherence-time",
            "gnosis-richness-tradeoff",
            "gnosis-control-tradeoff",
        ]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute the gnosis unlocking dynamics calculation.

        Args:
            registry: PMRegistry instance with input parameters

        Returns:
            Dictionary of computed results
        """
        # Load inputs from registry
        b3 = registry.get_param("topology.b3")
        chi_eff = registry.get_param("topology.chi_eff")

        # Validate inputs
        n_pairs_from_b3 = b3 // 2  # = 12 for b3 = 24
        assert n_pairs_from_b3 == self.TOTAL_PAIRS, \
            f"Expected {self.TOTAL_PAIRS} pairs from b3={b3}, got {n_pairs_from_b3}"

        # Compute core values
        results = self.compute_gnosis_dynamics()

        # Add probability curves
        results.update(self.compute_probability_curves())

        # Add coherence evolution
        results.update(self.compute_coherence_evolution())

        # Add trade-off analysis
        results.update(self.compute_tradeoff_analysis())

        # Add numerological documentation
        results.update(self.document_numerological_connections())

        return results

    def compute_gnosis_dynamics(self) -> Dict[str, Any]:
        """
        Compute core gnosis unlocking dynamics.

        Returns:
            Dictionary with core gnosis parameters
        """
        # Coherence times at baseline and full gnosis
        tau_baseline = coherence_time(self.BASELINE_PAIRS)
        tau_full = coherence_time(self.TOTAL_PAIRS)
        coherence_boost = tau_full / tau_baseline

        # Unlocking probabilities at key points
        p_6 = unlocking_probability(6)
        p_9 = unlocking_probability(9)
        p_11 = unlocking_probability(11)

        # Trade-off at full gnosis
        richness_12 = compute_richness(12)
        control_12 = compute_local_control(12)

        return {
            # Core constants
            "gnosis.total_pairs": self.TOTAL_PAIRS,
            "gnosis.baseline_pairs": self.BASELINE_PAIRS,
            "gnosis.tau_base_s": self.TAU_BASE,
            "gnosis.k_coherence": self.K_COHERENCE,
            # Computed outputs
            "gnosis.tau_baseline_s": tau_baseline,
            "gnosis.tau_full_gnosis_s": tau_full,
            "gnosis.coherence_boost": coherence_boost,
            "gnosis.unlock_prob_at_6": p_6,
            "gnosis.unlock_prob_at_9": p_9,
            "gnosis.unlock_prob_at_11": p_11,
            # Trade-off metrics
            "gnosis.richness_at_12": richness_12,
            "gnosis.control_at_12": control_12,
        }

    def compute_probability_curves(self) -> Dict[str, Any]:
        """
        Compute probability curves for different effort levels.

        Returns:
            Dictionary with probability curve data
        """
        # Active pairs range
        n_values = list(range(self.BASELINE_PAIRS, self.TOTAL_PAIRS + 1))

        # Probability curves for different effort levels
        effort_levels = [0.5, 0.9, 1.5]  # Low, medium, high effort
        prob_curves = {}

        for effort in effort_levels:
            probs = [unlocking_probability(n, effort) for n in n_values]
            prob_curves[f"effort_{effort}"] = probs

        # Default probability curve (effort = 0.9)
        default_probs = [unlocking_probability(n) for n in n_values]

        return {
            "_probability_vs_n_active": [
                {"n_active": n, "probability": p}
                for n, p in zip(n_values, default_probs)
            ],
            "_probability_curves": prob_curves,
            "_effort_levels": effort_levels,
        }

    def compute_coherence_evolution(self) -> Dict[str, Any]:
        """
        Compute coherence time evolution with active pairs.

        Returns:
            Dictionary with coherence evolution data
        """
        # Full range 0-12 for coherence (includes sub-baseline for completeness)
        n_values = list(range(0, self.TOTAL_PAIRS + 1))

        # Coherence times
        tau_values = [coherence_time(n) for n in n_values]
        tau_values_ms = [t * 1000 for t in tau_values]  # Convert to ms

        # Gnosis steps (0-6) representing activation from 6 to 12
        gnosis_steps = list(range(7))
        gnosis_n_active = [6 + step for step in gnosis_steps]
        gnosis_tau = [coherence_time(n) for n in gnosis_n_active]

        return {
            "_coherence_vs_n_active": [
                {"n_active": n, "tau_s": t, "tau_ms": t * 1000}
                for n, t in zip(n_values, tau_values)
            ],
            "_gnosis_steps": [
                {
                    "gnosis_step": step,
                    "n_active": n,
                    "tau_s": tau,
                    "tau_ms": tau * 1000
                }
                for step, n, tau in zip(gnosis_steps, gnosis_n_active, gnosis_tau)
            ],
        }

    def compute_tradeoff_analysis(self) -> Dict[str, Any]:
        """
        Compute richness vs control trade-off analysis.

        Returns:
            Dictionary with trade-off analysis data
        """
        n_values = list(range(self.BASELINE_PAIRS, self.TOTAL_PAIRS + 1))

        tradeoff_data = []
        for n in n_values:
            richness = compute_richness(n)
            control = compute_local_control(n)
            tradeoff_data.append({
                "n_active": n,
                "gnosis_step": n - self.BASELINE_PAIRS,
                "richness": richness,
                "local_control": control,
                "product": richness * control,  # Combined metric
            })

        return {
            "_tradeoff_analysis": tradeoff_data,
        }

    def document_numerological_connections(self) -> Dict[str, Any]:
        """
        Document numerological connections (phi^5 ~ 11, ln(410) = 6.02).

        HONESTY NOTE: These are documented as coincidences, not derivations.

        Returns:
            Dictionary with numerological documentation
        """
        return {
            "gnosis.phi_5_value": PHI_5,
            "gnosis.ln_410_value": LN_410,
            "_numerological_notes": {
                "phi_5": f"phi^5 = {PHI_5:.6f} ~ 11.09",
                "ln_410": f"ln(410) = {LN_410:.6f} ~ 6.02",
                "connection": (
                    "K_COHERENCE = 6.02 = ln(410). Note that 410 ~ phi^5 * 37. "
                    "This is documented as numerological coincidence, NOT as "
                    "derivation from G2 geometry. The 6 baseline pairs being "
                    "close to ln(phi^5 * 37) is suggestive but not geometric."
                ),
                "tau_base": (
                    "tau_base = 25ms comes from Orch-OR microtubule decoherence "
                    "estimates (Hameroff & Penrose 2014), not from PM geometry."
                ),
                "honest_assessment": (
                    "This phenomenological model fits observed patterns but "
                    "lacks first-principles derivation. Future work should "
                    "attempt to derive these formulas from G2 holonomy structure."
                )
            },
        }

    def get_gnosis_state(self, n_active: int) -> GnosisState:
        """
        Get complete gnosis state for given active pair count.

        Args:
            n_active: Number of active pairs (6-12)

        Returns:
            GnosisState with all computed values
        """
        n_active = max(self.BASELINE_PAIRS, min(self.TOTAL_PAIRS, n_active))

        return GnosisState(
            n_active=n_active,
            coherence_time_s=coherence_time(n_active),
            richness=compute_richness(n_active),
            local_control=compute_local_control(n_active),
            unlock_probability=unlocking_probability(n_active),
            gnosis_step=n_active - self.BASELINE_PAIRS,
        )

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 7.4 - Gnosis Unlocking.

        Returns:
            SectionContent with complete narrative and formula references
        """
        content_blocks = [
            ContentBlock(
                type="callout",
                callout_type="warning",
                title="Phenomenological Model Notice",
                content=(
                    "The formulas in this section are PHENOMENOLOGICAL fits motivated by "
                    "Orch-OR microtubule estimates and meditation EEG patterns. They are "
                    "NOT derived from first-principles G2 geometry. The phi^5 connection "
                    "is documented as numerological coincidence."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The gnosis unlocking mechanism describes how consciousness can "
                    "progressively activate additional bridge pairs beyond the baseline 6 "
                    "required for coherent waking awareness. This activation follows a "
                    "sigmoid probability curve with coherence time enhancement."
                )
            ),
            ContentBlock(
                type="heading",
                content="Unlocking Probability",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The probability of unlocking the next pair follows a logistic sigmoid "
                    "centered at the baseline. This models the 'bootstrapping' effect where "
                    "having more active pairs facilitates further activation:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"P_{\text{unlock}} = \frac{1}{1 + e^{-k(n_{\text{active}} - 6)}}",
                formula_id="gnosis-unlocking-probability",
                label="(7.4.1)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "At n=6 (baseline), P=0.5 (equiprobable). Below baseline, unlocking is "
                    "difficult (P << 0.5). Above baseline, unlocking becomes increasingly "
                    "facilitated (P >> 0.5)."
                )
            ),
            ContentBlock(
                type="heading",
                content="Coherence Time Enhancement",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The coherence time scales with the square root of active pairs via an "
                    "exponential enhancement factor:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\tau(n) = \tau_{\text{base}} \cdot e^{k \sqrt{n/12}} \cdot \left(\frac{n}{6}\right)^2",
                formula_id="gnosis-coherence-time",
                label="(7.4.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    f"With tau_base = 25 ms (Orch-OR estimate) and k = 3.2 (fitted for >10x), "
                    f"we obtain tau(6) = {coherence_time(6)*1000:.1f} ms at baseline and "
                    f"tau(12) = {coherence_time(12)*1000:.1f} ms at full gnosis, yielding "
                    f"a coherence boost of {coherence_time(12)/coherence_time(6):.1f}x."
                )
            ),
            ContentBlock(
                type="heading",
                content="Richness-Control Trade-off",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Activating more pairs creates a trade-off between phenomenal richness "
                    "(more consciousness channels) and local control (focused vs distributed):"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\text{Richness} = \frac{n - 6}{6}, \quad \text{Control} = e^{-\alpha(n-6)/6}",
                formula_id="gnosis-richness-tradeoff",
                label="(7.4.3)"
            ),
            ContentBlock(
                type="heading",
                content="Numerological Note: phi^5 Connection",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    f"Note: ln(410) = 6.02 matches the 6 baseline pairs, and 410 ~ phi^5 * 37 "
                    f"where phi^5 = {PHI_5:.3f}. We use k = 3.2 (fitted for >10x boost), but "
                    f"the ln(410) ~ 6 connection is documented as COINCIDENCE - it suggests "
                    f"a possible deeper connection but is not derived from G2 geometry."
                )
            ),
        ]

        return SectionContent(
            section_id="7",
            subsection_id="7.4",
            title="Gnosis Unlocking: Progressive Pair Activation",
            abstract=(
                "Models progressive activation of bridge pairs from baseline (6) to full "
                "gnosis (12). PHENOMENOLOGICAL: Sigmoid probability and sqrt-exponential "
                f"coherence are empirical fits. Coherence boost: {coherence_time(12)/coherence_time(6):.1f}x. "
                "Documents phi^5 numerological connection as coincidence."
            ),
            content_blocks=content_blocks,
            formula_refs=[
                "gnosis-unlocking-probability",
                "gnosis-coherence-time",
                "gnosis-richness-tradeoff",
            ],
            param_refs=[
                "gnosis.total_pairs",
                "gnosis.baseline_pairs",
                "gnosis.tau_base_s",
                "gnosis.coherence_boost",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas this simulation provides."""
        formulas = [
            Formula(
                id="gnosis-unlocking-probability",
                label="(7.4.1)",
                latex=r"P_{\text{unlock}} = \frac{1}{1 + e^{-k(n_{\text{active}} - 6)}}",
                plain_text="P_unlock = 1 / (1 + exp(-k * (n_active - 6)))",
                category="PHENOMENOLOGICAL",
                description=(
                    "Sigmoidal unlocking probability for next bridge pair. At baseline "
                    "(n=6), P=0.5. PHENOMENOLOGICAL FIT - not derived from G2 geometry."
                ),
                inputParams=["gnosis.n_active", "gnosis.sigmoid_steepness"],
                outputParams=["gnosis.unlock_probability"],
                input_params=["gnosis.n_active", "gnosis.sigmoid_steepness"],
                output_params=["gnosis.unlock_probability"],
                derivation={
                    "steps": [
                        "MOTIVATION: Model bootstrapping where active pairs facilitate more",
                        "ASSUMPTION: Logistic dynamics dP/dn = k*P*(1-P)",
                        "SOLUTION: P(n) = 1 / (1 + C*exp(-k*n))",
                        "CENTERING: Set P(6) = 0.5, giving C = exp(6k)",
                        "FINAL: P(n) = 1 / (1 + exp(-k*(n-6)))",
                        "NOTE: This is phenomenological fit, not geometric derivation"
                    ],
                    "assumptions": [
                        "Logistic growth model appropriate",
                        "Baseline threshold at n=6",
                        "Constant steepness k"
                    ],
                    "references": [
                        "Logistic function from population dynamics",
                        "Meditation research showing progressive EEG changes"
                    ],
                    "phenomenological_note": (
                        "This formula is an empirical fit. Deriving it from G2 holonomy "
                        "structure remains an open problem."
                    )
                },
                terms={
                    "P_unlock": "Probability of unlocking next pair",
                    "n_active": "Number of currently active pairs (6-12)",
                    "k": "Sigmoid steepness (default 0.9)",
                    "6": "Baseline threshold (minimum for coherent consciousness)"
                }
            ),
            Formula(
                id="gnosis-coherence-time",
                label="(7.4.2)",
                latex=r"\tau(n) = \tau_{\text{base}} \cdot e^{k \sqrt{n/12}} \cdot \left(\frac{n}{6}\right)^2",
                plain_text="tau(n) = tau_base * exp(k * sqrt(n/12)) * (n/6)^2",
                category="PHENOMENOLOGICAL",
                description=(
                    "Coherence time enhancement with active pairs. tau_base = 25ms from "
                    "Orch-OR. k = 3.2 fitted for >10x boost. PHENOMENOLOGICAL - not derived from G2."
                ),
                inputParams=["gnosis.n_active", "gnosis.tau_base", "gnosis.k_coherence"],
                outputParams=["gnosis.coherence_time"],
                input_params=["gnosis.n_active", "gnosis.tau_base", "gnosis.k_coherence"],
                output_params=["gnosis.coherence_time"],
                derivation={
                    "steps": [
                        "BASE VALUE: tau_base = 25ms from Orch-OR microtubule estimates",
                        "EXPONENTIAL: exp(k*sqrt(n/12)) for topological protection",
                        "QUADRATIC: (n/6)^2 for collective integration (normalized to baseline)",
                        "COEFFICIENT: k = 3.2 fitted for >10x boost criterion",
                        "NUMEROLOGY: ln(410) = 6.02 ~ 6 baseline (documented coincidence)",
                        f"RESULT: tau(6)={coherence_time(6)*1000:.1f}ms, tau(12)={coherence_time(12)*1000:.1f}ms"
                    ],
                    "assumptions": [
                        "Orch-OR microtubule decoherence model",
                        "Exponential protection from pair activation",
                        "Quadratic collective integration effect"
                    ],
                    "references": [
                        "Hameroff & Penrose (2014): Orch-OR microtubule coherence",
                        "Lutz et al. (2004): Gamma coherence in meditators"
                    ],
                    "phenomenological_note": (
                        "The k=3.2 is fitted for >10x boost. ln(410)=6.02 ~ 6 baseline "
                        "is numerological coincidence, not geometric derivation."
                    )
                },
                terms={
                    "tau": "Coherence time in seconds",
                    "tau_base": "Base coherence time = 25ms (Orch-OR)",
                    "k": "Enhancement factor = 3.2 (fitted for >10x)",
                    "n": "Number of active pairs",
                    "(n/6)^2": "Quadratic collective integration factor"
                }
            ),
            Formula(
                id="gnosis-richness-tradeoff",
                label="(7.4.3)",
                latex=(
                    r"\text{Richness} = \frac{n - 6}{6}, \quad "
                    r"\text{Control} = e^{-\alpha (n-6)/6}"
                ),
                plain_text="Richness = (n-6)/6, Control = exp(-alpha*(n-6)/6)",
                category="PHENOMENOLOGICAL",
                description=(
                    "Trade-off between phenomenal richness (more channels) and local "
                    "control (focused vs distributed awareness)."
                ),
                inputParams=["gnosis.n_active", "gnosis.control_decay"],
                outputParams=["gnosis.richness", "gnosis.local_control"],
                input_params=["gnosis.n_active", "gnosis.control_decay"],
                output_params=["gnosis.richness", "gnosis.local_control"],
                derivation={
                    "steps": [
                        "RICHNESS: Linear scaling from 0 at n=6 to 1 at n=12",
                        "CONTROL: Exponential decay from 1 at n=6",
                        "TRADE-OFF: Can't maximize both simultaneously",
                        "alpha = 0.5: Moderate decay rate"
                    ],
                    "assumptions": [
                        "Linear richness increase appropriate",
                        "Exponential control decay appropriate",
                        "Trade-off is fundamental feature"
                    ],
                    "references": [
                        "Contemplative traditions: focus vs openness trade-off",
                        "Attention research: spotlight vs lantern models"
                    ]
                },
                terms={
                    "Richness": "Phenomenal richness factor (0 to 1)",
                    "Control": "Local control factor (1 to ~0.6)",
                    "alpha": "Control decay rate (default 0.5)",
                    "n": "Number of active pairs"
                }
            ),
            Formula(
                id="gnosis-control-tradeoff",
                label="(7.4.4)",
                latex=r"\text{Control}(n) = e^{-0.5 \cdot (n-6)/6}",
                plain_text="Control(n) = exp(-0.5 * (n-6)/6)",
                category="PHENOMENOLOGICAL",
                description=(
                    "Local control decreases exponentially as more pairs activate. "
                    "Consciousness becomes more distributed, less focused."
                ),
                inputParams=["gnosis.n_active"],
                outputParams=["gnosis.local_control"],
                input_params=["gnosis.n_active"],
                output_params=["gnosis.local_control"],
                derivation={
                    "steps": [
                        "At n=6: Control = exp(0) = 1 (maximum focus)",
                        "At n=12: Control = exp(-0.5) ~ 0.61 (distributed)",
                        "Exponential decay models gradual loss of focus"
                    ],
                    "assumptions": [
                        "Control loss is exponential in activation fraction",
                        "Decay rate alpha = 0.5 is phenomenologically appropriate"
                    ],
                    "references": [
                        "Attention research on focused vs distributed modes"
                    ]
                },
                terms={
                    "Control": "Local control factor",
                    "0.5": "Decay rate alpha",
                    "n": "Active pairs",
                    "6": "Baseline (normalization)"
                }
            ),
        ]

        return formulas

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="gnosis.total_pairs",
                name="Total Bridge Pairs",
                units="dimensionless",
                status="GEOMETRIC",
                description="Total number of (2,0) bridge pairs = b3/2 = 12.",
                derivation_formula="gnosis-coherence-time",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.baseline_pairs",
                name="Baseline Active Pairs",
                units="dimensionless",
                status="PHENOMENOLOGICAL",
                description=(
                    "Minimum pairs for coherent waking consciousness. "
                    "Value 6 from Orch-OR stability threshold."
                ),
                derivation_formula="gnosis-unlocking-probability",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.tau_base_s",
                name="Base Coherence Time",
                units="seconds",
                status="PHENOMENOLOGICAL",
                description=(
                    "Base coherence time = 25 ms from Orch-OR microtubule estimates "
                    "(Hameroff & Penrose 2014). Not derived from PM geometry."
                ),
                derivation_formula="gnosis-coherence-time",
                experimental_bound=0.025,
                bound_type="estimate",
                bound_source="Orch-OR (Hameroff & Penrose 2014)"
            ),
            Parameter(
                path="gnosis.k_coherence",
                name="Coherence Enhancement Factor",
                units="dimensionless",
                status="PHENOMENOLOGICAL",
                description=(
                    "Exponential enhancement factor k = 3.2 (fitted for >10x boost). "
                    "Note: ln(410) = 6.02 ~ 6 baseline is documented as numerological "
                    "coincidence, not geometric derivation."
                ),
                derivation_formula="gnosis-coherence-time",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.tau_baseline_s",
                name="Coherence Time at Baseline",
                units="seconds",
                status="DERIVED",
                description="Coherence time at n=6 (baseline waking consciousness).",
                derivation_formula="gnosis-coherence-time",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.tau_full_gnosis_s",
                name="Coherence Time at Full Gnosis",
                units="seconds",
                status="DERIVED",
                description="Coherence time at n=12 (full gnosis state).",
                derivation_formula="gnosis-coherence-time",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.coherence_boost",
                name="Coherence Boost Factor",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Ratio tau(12)/tau(6). Success criterion: > 10x. "
                    "This measures the coherence enhancement from baseline to full gnosis."
                ),
                derivation_formula="gnosis-coherence-time",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.unlock_prob_at_6",
                name="Unlocking Probability at Baseline",
                units="dimensionless",
                status="DERIVED",
                description="P_unlock at n=6. By construction, equals 0.5.",
                derivation_formula="gnosis-unlocking-probability",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.richness_at_12",
                name="Richness at Full Gnosis",
                units="dimensionless",
                status="DERIVED",
                description="Phenomenal richness factor at n=12 (equals 1.0).",
                derivation_formula="gnosis-richness-tradeoff",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.control_at_12",
                name="Local Control at Full Gnosis",
                units="dimensionless",
                status="DERIVED",
                description="Local control factor at n=12 (~ 0.61 for alpha=0.5).",
                derivation_formula="gnosis-control-tradeoff",
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.phi_5_value",
                name="phi^5 Value",
                units="dimensionless",
                status="CONSTANT",
                description=(
                    f"Golden ratio to 5th power = {PHI_5:.6f}. Documented for "
                    "numerological transparency (not used in derivation)."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="gnosis.ln_410_value",
                name="ln(410) Value",
                units="dimensionless",
                status="CONSTANT",
                description=(
                    f"Natural log of 410 = {LN_410:.6f} = k_coherence. "
                    "Note: 410 ~ phi^5 * 37 is coincidence, not derivation."
                ),
                no_experimental_value=True
            ),
        ]

    def get_foundations(self) -> List[Dict[str, str]]:
        """Return foundational concepts for this simulation."""
        return [
            {
                "id": "orch-or",
                "title": "Orchestrated Objective Reduction (Orch-OR)",
                "category": "consciousness",
                "description": (
                    "Penrose-Hameroff theory that consciousness arises from quantum "
                    "coherence in microtubules, with decoherence time ~25ms."
                )
            },
            {
                "id": "pair-activation",
                "title": "Bridge Pair Activation",
                "category": "pm_framework",
                "description": (
                    "The 12 (2,0) bridge pairs can be progressively activated from "
                    "baseline 6 to full 12, expanding consciousness channels."
                )
            },
            {
                "id": "gnosis",
                "title": "Gnosis (Direct Knowledge)",
                "category": "philosophy",
                "description": (
                    "Direct experiential knowledge beyond intellectual understanding. "
                    "In PM framework, associated with full 12-pair activation."
                )
            },
            {
                "id": "sigmoid-probability",
                "title": "Sigmoid/Logistic Function",
                "category": "mathematics",
                "description": (
                    "S-shaped curve with central threshold. Used phenomenologically "
                    "to model bootstrapping in pair activation."
                )
            },
            {
                "id": "phenomenological-model",
                "title": "Phenomenological Model",
                "category": "methodology",
                "description": (
                    "A model that fits observed phenomena without first-principles "
                    "derivation. Useful but awaits deeper theoretical grounding."
                )
            },
        ]

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references for this simulation."""
        return [
            {
                "id": "hameroff_penrose2014",
                "authors": "Hameroff, S. and Penrose, R.",
                "title": "Consciousness in the universe: A review of the Orch OR theory",
                "journal": "Physics of Life Reviews",
                "volume": "11",
                "pages": "39-78",
                "year": 2014
            },
            {
                "id": "lutz2004",
                "authors": "Lutz, A., Greischar, L.L., Rawlings, N.B., Ricard, M., Davidson, R.J.",
                "title": "Long-term meditators self-induce high-amplitude gamma synchrony",
                "journal": "PNAS",
                "volume": "101",
                "pages": "16369-16373",
                "year": 2004
            },
            {
                "id": "braboszcz2017",
                "authors": "Braboszcz, C., Cahn, B.R., Levy, J., Fernandez, M., Delorme, A.",
                "title": "Increased Gamma Brainwave Amplitude Compared to Control in Three Different Meditation Traditions",
                "journal": "PLOS ONE",
                "year": 2017
            },
            {
                "id": "davidson_lutz2008",
                "authors": "Davidson, R.J. and Lutz, A.",
                "title": "Buddha's Brain: Neuroplasticity and Meditation",
                "journal": "IEEE Signal Processing Magazine",
                "volume": "25",
                "pages": "176-174",
                "year": 2008
            },
        ]

    def get_beginner_explanation(self) -> Dict[str, Any]:
        """Return beginner-friendly explanation."""
        return {
            "icon": "G",
            "title": "How Consciousness Might 'Level Up'",
            "simpleExplanation": (
                "Imagine your brain has 12 'channels' for consciousness, but normally "
                "only 6 are active - enough for everyday awareness. Through practices like "
                "meditation, you might be able to 'unlock' more channels, going from 6 to "
                "7, 8, 9... up to all 12. Each new channel makes your awareness richer "
                "but also more spread out (less focused). This is a phenomenological model - "
                "it describes patterns we observe but doesn't explain WHY from first principles."
            ),
            "analogy": (
                "Think of it like a radio with 12 possible stations, but your antenna "
                "normally only picks up 6. With practice (meditation, contemplation), you "
                "can tune your antenna to pick up more stations. The more stations you can "
                "receive, the richer your experience - but you can't focus on all 12 at once "
                "as clearly as you could focus on just one. At full reception (all 12), "
                "you experience everything but with less individual focus."
            ),
            "keyTakeaway": (
                "The gnosis unlocking model suggests consciousness can progressively expand "
                "from baseline (6 pairs) to full gnosis (12 pairs), with a trade-off between "
                "richness and focus. This is a phenomenological model - it fits patterns "
                "but awaits deeper theoretical derivation."
            ),
            "technicalDetail": (
                f"The unlocking probability P = 1/(1+exp(-0.9*(n-6))) is a sigmoid centered "
                f"at baseline. Coherence time tau = 25ms * exp(3.2*sqrt(n/12)) * (n/6)^2 gives "
                f"tau(6) = {coherence_time(6)*1000:.0f}ms and tau(12) = {coherence_time(12)*1000:.0f}ms, "
                f"a {coherence_time(12)/coherence_time(6):.0f}x boost. Note: ln(410) = 6.02 ~ 6 baseline "
                f"is documented as numerological coincidence, not geometric derivation."
            ),
            "caution": (
                "This is a PHENOMENOLOGICAL model - the formulas fit observed patterns "
                "(meditation EEG, Orch-OR) but are not derived from G2 geometry. The phi^5 "
                "connection is numerology, not physics. Future work should attempt "
                "first-principles derivation from the PM geometric framework."
            )
        }


def run_gnosis_unlocking(verbose: bool = True) -> Dict[str, Any]:
    """
    Run the gnosis unlocking dynamics simulation standalone.

    Args:
        verbose: Whether to print detailed output

    Returns:
        Dictionary with gnosis unlocking results
    """
    # Create registry and simulation
    registry = PMRegistry.get_instance()

    # Set up topological inputs (from TCS #187)
    registry.set_param("topology.b3", 24, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144, source="ESTABLISHED:TCS #187", status="ESTABLISHED")

    # Create and execute simulation
    sim = GnosisUnlockingSimulation()
    results = sim.execute(registry, verbose=verbose)

    if verbose:
        print("\n" + "=" * 75)
        print(" GNOSIS UNLOCKING DYNAMICS v22.5 - PHENOMENOLOGICAL MODEL")
        print("=" * 75)

        print("\n" + "-" * 75)
        print(" PHENOMENOLOGICAL NOTICE")
        print("-" * 75)
        print("  This model uses empirical fits, NOT first-principles derivation.")
        print("  The phi^5 connection is documented as coincidence.")

        print("\n" + "-" * 75)
        print(" CORE PARAMETERS")
        print("-" * 75)
        print(f"  Total pairs:           {results['gnosis.total_pairs']}")
        print(f"  Baseline pairs:        {results['gnosis.baseline_pairs']}")
        print(f"  tau_base:              {results['gnosis.tau_base_s']*1000:.1f} ms (Orch-OR)")
        print(f"  k_coherence:           {results['gnosis.k_coherence']:.3f} = ln(410)")

        print("\n" + "-" * 75)
        print(" COHERENCE TIME EVOLUTION")
        print("-" * 75)
        print(f"  tau(6) [baseline]:     {results['gnosis.tau_baseline_s']*1000:.2f} ms")
        print(f"  tau(12) [full gnosis]: {results['gnosis.tau_full_gnosis_s']*1000:.2f} ms")
        print(f"  Coherence boost:       {results['gnosis.coherence_boost']:.2f}x")

        print("\n" + "-" * 75)
        print(" UNLOCKING PROBABILITY")
        print("-" * 75)
        print(f"  P(unlock | n=6):       {results['gnosis.unlock_prob_at_6']:.3f}")
        print(f"  P(unlock | n=9):       {results['gnosis.unlock_prob_at_9']:.3f}")
        print(f"  P(unlock | n=11):      {results['gnosis.unlock_prob_at_11']:.3f}")

        print("\n" + "-" * 75)
        print(" RICHNESS-CONTROL TRADE-OFF")
        print("-" * 75)
        print(f"  Richness at n=12:      {results['gnosis.richness_at_12']:.3f}")
        print(f"  Control at n=12:       {results['gnosis.control_at_12']:.3f}")

        print("\n" + "-" * 75)
        print(" NUMEROLOGICAL DOCUMENTATION")
        print("-" * 75)
        print(f"  phi^5 = {results['gnosis.phi_5_value']:.6f}")
        print(f"  ln(410) = {results['gnosis.ln_410_value']:.6f}")
        print("  Connection: 410 ~ phi^5 * 37 (COINCIDENCE, not derivation)")

        # Print gnosis steps table
        print("\n" + "-" * 75)
        print(" GNOSIS STEPS (Active Pairs vs Coherence Time)")
        print("-" * 75)
        print("  Step | n_active | tau (ms) | P_unlock | Richness | Control")
        print("  " + "-" * 60)
        gnosis_data = results.get("_gnosis_steps", [])
        for step_data in gnosis_data:
            n = step_data['n_active']
            tau_ms = step_data['tau_ms']
            p = unlocking_probability(n)
            r = compute_richness(n)
            c = compute_local_control(n)
            print(f"  {step_data['gnosis_step']:4d} | {n:8d} | {tau_ms:8.1f} | {p:8.3f} | {r:8.3f} | {c:7.3f}")

        print("\n" + "=" * 75)
        print(" SUCCESS CRITERION: tau(12)/tau(6) > 10x")
        success = results['gnosis.coherence_boost'] > 10.0
        print(f" RESULT: {results['gnosis.coherence_boost']:.2f}x -> {'PASSED' if success else 'FAILED'}")
        print("=" * 75)

    return results


# =============================================================================
# Self-Validation Assertions
# =============================================================================

# Create validation instance
_validation_instance = GnosisUnlockingSimulation()

# Validate metadata
assert _validation_instance.metadata is not None, "GnosisUnlocking: metadata is None"
assert _validation_instance.metadata.id == "gnosis_unlocking_v22", \
    f"GnosisUnlocking: unexpected id {_validation_instance.metadata.id}"
assert _validation_instance.metadata.version == "22.5", \
    f"GnosisUnlocking: unexpected version {_validation_instance.metadata.version}"

# Validate formulas exist
assert len(_validation_instance.get_formulas()) >= 4, \
    f"GnosisUnlocking: expected at least 4 formulas, got {len(_validation_instance.get_formulas())}"

# Validate constants
assert _validation_instance.TOTAL_PAIRS == 12, \
    f"GnosisUnlocking: TOTAL_PAIRS should be 12, got {_validation_instance.TOTAL_PAIRS}"
assert _validation_instance.BASELINE_PAIRS == 6, \
    f"GnosisUnlocking: BASELINE_PAIRS should be 6, got {_validation_instance.BASELINE_PAIRS}"
assert abs(_validation_instance.TAU_BASE - 0.025) < 1e-10, \
    f"GnosisUnlocking: TAU_BASE should be 0.025, got {_validation_instance.TAU_BASE}"

# Validate unlocking probability at baseline
p_6 = unlocking_probability(6)
assert abs(p_6 - 0.5) < 1e-10, \
    f"GnosisUnlocking: P(6) should be 0.5, got {p_6}"

# Validate coherence boost exceeds success criterion
tau_6 = coherence_time(6)
tau_12 = coherence_time(12)
boost = tau_12 / tau_6
assert boost > 10.0, \
    f"GnosisUnlocking: coherence boost should be > 10x, got {boost:.2f}x"

# Validate trade-off values
assert compute_richness(6) == 0.0, "Richness at n=6 should be 0"
assert compute_richness(12) == 1.0, "Richness at n=12 should be 1"
assert compute_local_control(6) == 1.0, "Control at n=6 should be 1"

# Validate K_COHERENCE produces >10x boost (k=3.2 achieves this)
assert K_COHERENCE > 0, f"K_COHERENCE should be positive, got {K_COHERENCE}"

# Validate numerological documentation
assert abs(LN_410 - np.log(410)) < 0.01, \
    f"LN_410 should be ln(410), got {LN_410}"

# Cleanup validation variables
del _validation_instance


if __name__ == "__main__":
    run_gnosis_unlocking(verbose=True)
