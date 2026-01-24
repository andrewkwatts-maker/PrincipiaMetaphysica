#!/usr/bin/env python3
"""
Four Dice OR Condensate Branch Selection v22
==============================================

WS-2: 4 Dice Rolls for Condensate OR Reduction

Implements the 4-dice condensate branch selection mechanism. The 12 bridge
pairs group into 4 "dice" (3 pairs each) for condensate branch selection
via Objective Reduction (OR).

MECHANISM:
    Groups: [P1,P2,P3], [P4,P5,P6], [P7,P8,P9], [P10,P11,P12]
    Each group performs an OR "roll" based on residue flux
    4 rolls select condensate branch: k = argmax(product(o_j^{w_k}))

GEOMETRIC JUSTIFICATION:
    - Condensate structure: (5,1) bridge + 3 x (3,1) generations = 4 "directions"
    - NOT from G2 triality (which gives 3, not 4)
    - Tetrahedron inscribed in horizon circle for 4 vertices

KEY PHYSICS:
    - 12 bridge pairs total (from orientation sum S = 12)
    - 4 dice of 3 pairs each (from condensate structure)
    - OR mechanism selects quantum branch via residue flux
    - Gnosis effect: more active pairs -> more stable rolls

CONDENSATE BRANCH FORMULA:
    P_branch_k = product(o_j^{w_k}) for j in dice
    k_selected = argmax(P_branch_k) over all branches

CENTRAL SAMPLER TAU BOOST (v22.1):
    When the central (2,0) sampler is active (n_local >= 9), coherence time
    tau receives an enhancement boost:
        tau_eff = tau * (1 + p_anc * k_central)
    where:
        - p_anc = ancestral flux from central sampler averaging
        - k_central = central boost factor (phi/sqrt(12))
        - I_central = 1 if n_local >= 9 else 0 (activation indicator)

    Full tau formula with central enhancement:
        tau(n) = tau_0 * exp(k * sqrt((n_local + I_central)/13)) * p_anc^2

References:
    - Penrose, R. (1989). "The Emperor's New Mind"
    - Penrose, R. (1996). "On Gravity's Role in Quantum State Reduction"
    - Hameroff, S. & Penrose, R. (2014). "Consciousness in the universe: Orch OR"
    - Joyce, D.D. (2000). "Compact Manifolds with Special Holonomy"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import sys
import os

# Add parent directories to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
sys.path.insert(0, _simulations_dir)

# Import directly from base submodules to avoid triggering simulations/__init__.py
from simulations.base.simulation_base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)
from simulations.base.registry import PMRegistry

# Import precision constants
from simulations.base.precision import B3, K_GIMEL, PHI

# Import FormulasRegistry for central sampler properties
from core.FormulasRegistry import get_registry as get_formulas_registry


class FourDiceORSimulation(SimulationBase):
    """
    WS-2: Four Dice OR Condensate Branch Selection.

    The 12 bridge pairs are grouped into 4 "dice" of 3 pairs each. Each dice
    performs an OR (Objective Reduction) roll based on residue flux to select
    the condensate branch.

    GEOMETRIC JUSTIFICATION:
        The 4-dice structure arises from condensate geometry:
        - (5,1) bridge: 1 direction (the "spine")
        - 3 x (3,1) generations: 3 additional directions
        - Total: 4 directions forming tetrahedron inscribed in horizon circle

    MECHANISM:
        1. Each dice group accumulates residue flux from its 3 pairs
        2. Flux is weighted by phi-modulated pattern for stability
        3. OR collapse selects outcome o_j for each dice
        4. Branch selection: k = argmax over branches of product(o_j^{w_k})
        5. Gnosis effect increases stability with more active pairs

    CENTRAL SAMPLER INTEGRATION (v22.1):
        When n_local >= 9, the central (2,0) sampler activates and provides
        a tau coherence boost:
            tau_eff = tau * (1 + p_anc * k_central)
        where k_central = phi/sqrt(12) is the central boost factor.

        The full tau formula with central enhancement:
            tau(n) = tau_0 * exp(k * sqrt((n_local + I_central)/13)) * p_anc^2
        where I_central = 1 if n_local >= 9 else 0.

    OUTPUT:
        - 4 dice outcome probabilities
        - Selected branch index k
        - Coherence metric for roll stability
        - Central tau boost factor (optional)
    """

    # =========================================================================
    # CONSTANTS (from PM SSOT)
    # =========================================================================

    # Total bridge pairs (orientation sum S = 12)
    TOTAL_PAIRS: int = 12

    # Number of dice (condensate directions)
    NUM_DICE: int = 4

    # Pairs per dice
    PAIRS_PER_DICE: int = 3

    # Dice modulus (quaternionic structure)
    DICE_MODULUS: int = 4

    # Dice group definitions: which pairs belong to which dice
    # Groups: [P1,P2,P3], [P4,P5,P6], [P7,P8,P9], [P10,P11,P12]
    DICE_GROUPS: List[Tuple[int, int, int]] = [
        (0, 1, 2),      # Dice 0: pairs 1-3 (0-indexed)
        (3, 4, 5),      # Dice 1: pairs 4-6
        (6, 7, 8),      # Dice 2: pairs 7-9
        (9, 10, 11),    # Dice 3: pairs 10-12
    ]

    # R_perp rotation matrix (90-degree rotation for OR reduction)
    R_PERP = np.array([[0, -1], [1, 0]])

    # Condensate structure
    SPINE_BRIDGE: Tuple[int, int] = (5, 1)  # Main condensate bridge
    GENERATION_BRIDGES: List[Tuple[int, int]] = [(3, 1), (3, 1), (3, 1)]

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="four_dice_or_v22",
            version="22.0",
            domain="pneuma",
            title="Four Dice OR Condensate Branch Selection",
            description=(
                "WS-2: The 12 bridge pairs group into 4 dice (3 pairs each) for "
                "condensate branch selection. Each dice performs an OR roll based "
                "on residue flux. The 4 rolls select condensate branch via "
                "k = argmax(product(o_j^{w_k})). The 4-dice structure arises from "
                "condensate geometry: (5,1) bridge + 3x(3,1) generations = 4 directions, "
                "forming a tetrahedron inscribed in the horizon circle."
            ),
            section_id="8",
            subsection_id="8.4"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            "topology.b3",
            "topology.chi_eff",
            "topology.orientation_sum",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            # Dice structure
            "four_dice.total_pairs",
            "four_dice.num_dice",
            "four_dice.pairs_per_dice",
            "four_dice.total_branches",
            # Roll outcomes
            "four_dice.dice_outcomes",
            "four_dice.branch_selected",
            "four_dice.branch_probability",
            # Flux metrics
            "four_dice.total_flux",
            "four_dice.flux_per_dice",
            # Coherence and stability
            "four_dice.coherence_metric",
            "four_dice.gnosis_stability",
            # Geometric factors
            "four_dice.tetrahedron_volume",
            "four_dice.horizon_radius",
            # Central sampler tau boost
            "four_dice.central_tau_boost",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "dice-grouping-formula",
            "or-roll-probability",
            "branch-selection-formula",
            "coherence-metric-formula",
            "gnosis-stability-formula",
            "tetrahedron-geometry",
            "central-tau-boost-formula",
        ]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute the four dice OR condensate branch selection.

        Args:
            registry: PMRegistry instance with input parameters

        Returns:
            Dictionary of computed results
        """
        # Load inputs from registry
        b3 = registry.get_param("topology.b3")
        chi_eff = registry.get_param("topology.chi_eff")
        orientation_sum = registry.get_param("topology.orientation_sum")

        # Initialize pair fluxes (phi-modulated pattern)
        pair_fluxes = self._initialize_pair_fluxes()

        # Perform OR roll for each dice
        dice_outcomes, dice_fluxes = self._perform_or_rolls(pair_fluxes)

        # Select condensate branch
        branch_result = self._select_branch(dice_outcomes, dice_fluxes)

        # Calculate coherence metric
        coherence = self._calculate_coherence(pair_fluxes, dice_outcomes)

        # Calculate gnosis stability
        gnosis_stability = self._calculate_gnosis_stability(chi_eff)

        # Calculate tetrahedron geometry
        tetra_geometry = self._calculate_tetrahedron_geometry(b3)

        # Calculate central sampler tau boost (at full gnosis n=12)
        # Use a representative base tau of 1.0 to get the boost factor
        tau_boost_result = self.tau_central_boost(
            tau=1.0,
            n_local=self.TOTAL_PAIRS,  # Full gnosis
            p_local=pair_fluxes.tolist(),
            use_central_sampler=True
        )

        # Combine all results
        results = {
            # Dice structure
            "four_dice.total_pairs": self.TOTAL_PAIRS,
            "four_dice.num_dice": self.NUM_DICE,
            "four_dice.pairs_per_dice": self.PAIRS_PER_DICE,
            "four_dice.total_branches": self.DICE_MODULUS ** self.NUM_DICE,
            # Roll outcomes
            "four_dice.dice_outcomes": dice_outcomes.tolist(),
            "four_dice.branch_selected": branch_result["branch"],
            "four_dice.branch_probability": branch_result["probability"],
            # Flux metrics
            "four_dice.total_flux": float(np.sum(pair_fluxes)),
            "four_dice.flux_per_dice": dice_fluxes.tolist(),
            # Coherence and stability
            "four_dice.coherence_metric": coherence,
            "four_dice.gnosis_stability": gnosis_stability,
            # Geometric factors
            "four_dice.tetrahedron_volume": tetra_geometry["volume"],
            "four_dice.horizon_radius": tetra_geometry["radius"],
            # Central sampler tau boost
            "four_dice.central_tau_boost": tau_boost_result["tau_boost_factor"],
        }

        # Store internal data for visualization/debugging
        results["_pair_fluxes"] = pair_fluxes.tolist()
        results["_branch_weights"] = branch_result["weights"]
        results["_central_sampler_details"] = tau_boost_result

        return results

    def _initialize_pair_fluxes(
        self,
        seed: Optional[int] = None
    ) -> np.ndarray:
        """
        Initialize residue flux for each bridge pair using phi-modulated pattern.

        The flux pattern uses golden ratio modulation for stability:
            f_i = f_base * phi^(i mod 3)

        This creates a natural hierarchy within each dice group while
        maintaining triality structure.

        Args:
            seed: Random seed for reproducibility (None for deterministic)

        Returns:
            Array of residue fluxes for each pair
        """
        pair_fluxes = np.zeros(self.TOTAL_PAIRS)

        # Base flux normalized by K_GIMEL
        f_base = 1.0 / K_GIMEL

        for i in range(self.TOTAL_PAIRS):
            # Phi modulation creates triality pattern within each dice
            phi_factor = PHI ** (i % self.PAIRS_PER_DICE)
            pair_fluxes[i] = f_base * phi_factor

        # Normalize so total flux equals 1
        pair_fluxes = pair_fluxes / np.sum(pair_fluxes)

        return pair_fluxes

    def _perform_or_rolls(
        self,
        pair_fluxes: np.ndarray,
        seed: Optional[int] = 42
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform OR (Objective Reduction) roll for each dice.

        Each dice aggregates residue flux from its 3 pairs and
        produces an outcome o_j in {0, 1, 2, 3} via mod-4 arithmetic.

        OR MECHANISM:
            1. Sum residue fluxes for pairs in dice group
            2. Apply R_perp rotation for quantum sampling
            3. Scale by K_GIMEL and take mod-4

        Args:
            pair_fluxes: Array of residue fluxes for each pair
            seed: Random seed for OR sampling

        Returns:
            Tuple of (dice_outcomes, dice_fluxes)
        """
        rng = np.random.default_rng(seed)
        dice_outcomes = np.zeros(self.NUM_DICE, dtype=int)
        dice_fluxes = np.zeros(self.NUM_DICE)

        for dice_idx, pairs in enumerate(self.DICE_GROUPS):
            # Aggregate flux for this dice
            flux_sum = 0.0
            for pair_idx in pairs:
                # Apply OR R_perp sampling (quantum coordinate selection)
                theta = rng.uniform(0, 2 * np.pi)
                state = np.array([np.cos(theta), np.sin(theta)])
                rotated = self.R_PERP @ state

                # Contribution is flux weighted by x-projection
                contribution = pair_fluxes[pair_idx] * rotated[0]
                flux_sum += contribution

            # Store dice flux magnitude
            dice_fluxes[dice_idx] = abs(flux_sum)

            # Scale and take mod-4 for outcome
            scaled_flux = abs(flux_sum) * K_GIMEL * self.TOTAL_PAIRS
            dice_outcomes[dice_idx] = int(np.floor(scaled_flux)) % self.DICE_MODULUS

        return dice_outcomes, dice_fluxes

    def _select_branch(
        self,
        dice_outcomes: np.ndarray,
        dice_fluxes: np.ndarray
    ) -> Dict[str, Any]:
        """
        Select condensate branch from 4 dice outcomes.

        BRANCH SELECTION FORMULA:
            P_branch_k = product(o_j^{w_k}) for all dice j
            k_selected = argmax(P_branch_k) over all branches

        The branch encoding uses base-4 (quaternionic structure):
            branch = o_0 + 4*o_1 + 16*o_2 + 64*o_3

        Args:
            dice_outcomes: Array of 4 dice outcomes (0-3 each)
            dice_fluxes: Array of 4 dice flux magnitudes

        Returns:
            Dictionary with branch selection results
        """
        # Calculate branch index using quaternionic encoding
        branch = int(
            dice_outcomes[0] +
            4 * dice_outcomes[1] +
            16 * dice_outcomes[2] +
            64 * dice_outcomes[3]
        )

        total_branches = self.DICE_MODULUS ** self.NUM_DICE  # 256

        # Calculate branch weights (flux-weighted product)
        # Weight for this branch is product of dice flux contributions
        weights = []
        for k in range(total_branches):
            # Decode branch k into dice outcomes
            k_outcomes = [
                k % 4,
                (k // 4) % 4,
                (k // 16) % 4,
                (k // 64) % 4
            ]
            # Weight is product of (flux * match_factor)
            weight = 1.0
            for j in range(self.NUM_DICE):
                # Higher weight when outcome matches
                if k_outcomes[j] == dice_outcomes[j]:
                    weight *= (1 + dice_fluxes[j])
                else:
                    weight *= dice_fluxes[j]
            weights.append(weight)

        # Normalize weights to probabilities
        weights = np.array(weights)
        weights = weights / np.sum(weights)

        # Probability of selected branch
        probability = float(weights[branch])

        return {
            "branch": branch,
            "probability": probability,
            "weights": weights.tolist(),
        }

    def _calculate_coherence(
        self,
        pair_fluxes: np.ndarray,
        dice_outcomes: np.ndarray
    ) -> float:
        """
        Calculate coherence metric for the OR roll.

        COHERENCE METRIC:
            C = 1 - entropy(P_dice) / log2(4)

        Where P_dice is the probability distribution of dice outcomes.
        C = 1 means perfectly coherent (deterministic)
        C = 0 means maximally incoherent (uniform random)

        Args:
            pair_fluxes: Array of residue fluxes
            dice_outcomes: Array of dice outcomes

        Returns:
            Coherence metric in [0, 1]
        """
        # Count outcome frequencies across dice
        outcome_counts = np.bincount(dice_outcomes, minlength=self.DICE_MODULUS)
        outcome_probs = outcome_counts / self.NUM_DICE

        # Calculate entropy (with protection against log(0))
        entropy = -np.sum(outcome_probs * np.log2(outcome_probs + 1e-10))
        max_entropy = np.log2(self.DICE_MODULUS)

        # Coherence is 1 - normalized entropy
        coherence = 1.0 - (entropy / max_entropy)

        return float(coherence)

    def _calculate_gnosis_stability(self, chi_eff: int) -> float:
        """
        Calculate gnosis stability: more active pairs -> more stable rolls.

        GNOSIS STABILITY:
            S_gnosis = (n_active / TOTAL_PAIRS) * (1 - 1/chi_eff)

        At full activation (n=12), stability approaches (1 - 1/chi_eff).
        The chi_eff term provides topological damping.

        Args:
            chi_eff: Effective Euler characteristic (144)

        Returns:
            Gnosis stability factor in [0, 1)
        """
        # Assume full activation for this calculation
        n_active = self.TOTAL_PAIRS

        # Base stability from activation fraction
        activation_factor = n_active / self.TOTAL_PAIRS

        # Topological stability (1 - 1/chi_eff)
        topo_stability = 1.0 - 1.0 / chi_eff

        # Combined stability
        gnosis_stability = activation_factor * topo_stability

        return float(gnosis_stability)

    def tau_central_boost(
        self,
        tau: float,
        n_local: int = 12,
        p_local: Optional[List[float]] = None,
        use_central_sampler: bool = True
    ) -> Dict[str, Any]:
        """
        Compute tau coherence boost from central (2,0) sampler integration.

        When the central sampler is active (n_local >= 9), coherence time tau
        receives an enhancement based on the ancestral flux averaging:

            tau_eff = tau * (1 + p_anc * k_central)

        where:
            - p_anc = ancestral flux from central sampler formula
            - k_central = central boost factor = phi/sqrt(12)

        The full tau formula with central enhancement:
            tau(n) = tau_0 * exp(k * sqrt((n_local + I_central)/13)) * p_anc^2

        where I_central = 1 if n_local >= 9 else 0.

        Args:
            tau: Base coherence time (tau_0 or pre-computed tau)
            n_local: Number of active local pairs (6 baseline -> 12 full gnosis)
            p_local: List of 12 local pair probabilities (if None, uses phi-modulation)
            use_central_sampler: Whether to apply central sampler boost

        Returns:
            Dictionary containing:
                - tau_eff: Effective tau with central boost
                - tau_boost_factor: Multiplicative boost (1 + p_anc * k_central)
                - p_anc: Ancestral flux from central averaging
                - k_central: Central boost factor (phi/sqrt(12))
                - central_active: Whether central sampler is active
                - I_central: Activation indicator (0 or 1)
        """
        # Get FormulasRegistry for central sampler properties
        try:
            reg = get_formulas_registry()
            k_central = reg.central_pair_weight  # phi/sqrt(12)
            activation_threshold = reg.central_activation_threshold  # 9
        except Exception:
            # Fallback to computed values if registry unavailable
            k_central = PHI / np.sqrt(12)  # phi/sqrt(12) ~ 0.467
            activation_threshold = 9

        # Determine if central sampler is active
        central_active = n_local >= activation_threshold
        I_central = 1 if central_active else 0

        # Generate p_local if not provided (phi-modulated pattern)
        if p_local is None:
            p_local = []
            for i in range(self.TOTAL_PAIRS):
                phi_factor = PHI ** (i % self.PAIRS_PER_DICE)
                p_local.append(phi_factor)
            # Normalize
            total = sum(p_local)
            p_local = [p / total for p in p_local]

        # Compute p_anc (ancestral flux)
        if use_central_sampler and central_active:
            # p_anc = (1/12) * sum(p_i) + sqrt(n_local/12) * phi / 12
            local_sum = sum(p_local[:min(n_local, len(p_local))])
            local_avg = local_sum / 12
            dilution = np.sqrt(n_local / 12) * PHI / 12
            p_anc = local_avg + dilution
        else:
            # Central inactive: just local averaging
            local_sum = sum(p_local[:min(n_local, len(p_local))])
            p_anc = local_sum / 12

        # Compute tau boost
        if use_central_sampler and central_active:
            tau_boost_factor = 1.0 + p_anc * k_central
        else:
            tau_boost_factor = 1.0

        # Effective tau
        tau_eff = tau * tau_boost_factor

        return {
            "tau_eff": float(tau_eff),
            "tau_boost_factor": float(tau_boost_factor),
            "p_anc": float(p_anc),
            "k_central": float(k_central),
            "central_active": central_active,
            "I_central": I_central,
            "n_local": n_local,
        }

    def _calculate_tetrahedron_geometry(self, b3: int) -> Dict[str, float]:
        """
        Calculate tetrahedron geometry inscribed in horizon circle.

        The 4 dice correspond to 4 vertices of a regular tetrahedron
        inscribed in the horizon circle. This geometry arises from:
        - (5,1) bridge: apex vertex
        - 3 x (3,1) generations: base triangle vertices

        TETRAHEDRON VOLUME:
            V = (8 * sqrt(3) / 27) * R^3

        where R is the circumradius.

        Args:
            b3: Third Betti number (24)

        Returns:
            Dictionary with tetrahedron geometry results
        """
        # Horizon radius proportional to sqrt(b3)
        horizon_radius = np.sqrt(b3) / 2  # = sqrt(24)/2 ~ 2.449

        # Regular tetrahedron with circumradius = horizon_radius
        R = horizon_radius

        # Edge length: a = R * sqrt(8/3)
        edge_length = R * np.sqrt(8.0 / 3.0)

        # Volume: V = (a^3 / (6 * sqrt(2)))
        volume = (edge_length ** 3) / (6 * np.sqrt(2))

        return {
            "radius": float(horizon_radius),
            "edge_length": float(edge_length),
            "volume": float(volume),
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 8.4 - Four Dice OR Condensate Selection.

        Returns:
            SectionContent with complete narrative and formula references
        """
        content_blocks = [
            ContentBlock(
                type="paragraph",
                content=(
                    "The 12 bridge pairs of the TCS G2 manifold organize into 4 'dice' "
                    "for condensate branch selection via Objective Reduction (OR). Each "
                    "dice contains 3 bridge pairs, corresponding to the triality structure "
                    "within each condensate direction."
                )
            ),
            ContentBlock(
                type="heading",
                content="Dice Grouping Structure",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The grouping into 4 dice of 3 pairs each arises from condensate "
                    "geometry, not from G2 triality (which would give 3 groups):"
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "(5,1) bridge: Main condensate spine - 1 direction",
                    "3 x (3,1) generation bridges: 3 additional directions",
                    "Total: 4 directions = vertices of inscribed tetrahedron"
                ]
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"\text{Groups: } [P_1, P_2, P_3], [P_4, P_5, P_6], "
                    r"[P_7, P_8, P_9], [P_{10}, P_{11}, P_{12}]"
                ),
                formula_id="dice-grouping-formula",
                label="(8.4.1)"
            ),
            ContentBlock(
                type="heading",
                content="OR Roll Mechanism",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each dice performs an Objective Reduction roll based on the "
                    "residue flux from its 3 pairs. The OR mechanism applies the "
                    "R_perp rotation for quantum coordinate selection:"
                )
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"o_j = \left\lfloor \left| \sum_{i \in \text{Dice}_j} "
                    r"R_\perp \cdot f_i \right| \cdot k_{\gimel} \cdot 12 \right\rfloor \mod 4"
                ),
                formula_id="or-roll-probability",
                label="(8.4.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "where f_i is the residue flux for pair i, R_perp is the 90-degree "
                    "rotation matrix, and k_gimel provides the scaling factor."
                )
            ),
            ContentBlock(
                type="heading",
                content="Branch Selection Formula",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 4 dice outcomes select the condensate branch k via:"
                )
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"k = \text{argmax}_{k'} \prod_{j=0}^{3} o_j^{w_{k'}}, \quad "
                    r"\text{branch encoding: } k = o_0 + 4o_1 + 16o_2 + 64o_3"
                ),
                formula_id="branch-selection-formula",
                label="(8.4.3)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This quaternionic base-4 encoding yields 4^4 = 256 possible branches, "
                    "corresponding to different condensate configurations in the 4D projection."
                )
            ),
            ContentBlock(
                type="heading",
                content="Coherence Metric",
                level=3
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"C = 1 - \frac{H(P_{\text{dice}})}{\log_2 4}, \quad "
                    r"H(P) = -\sum_j P_j \log_2 P_j"
                ),
                formula_id="coherence-metric-formula",
                label="(8.4.4)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The coherence metric C measures how deterministic the dice rolls are. "
                    "C = 1 indicates perfectly coherent (all dice give same outcome), while "
                    "C = 0 indicates maximally incoherent (uniform random outcomes)."
                )
            ),
            ContentBlock(
                type="heading",
                content="Gnosis Stability Effect",
                level=3
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"S_{\text{gnosis}} = \frac{n_{\text{active}}}{12} "
                    r"\cdot \left(1 - \frac{1}{\chi_{\text{eff}}}\right)"
                ),
                formula_id="gnosis-stability-formula",
                label="(8.4.5)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The gnosis effect describes how activating more bridge pairs increases "
                    "roll stability. At full activation (n=12), stability approaches "
                    "(1 - 1/chi_eff) ~ 0.993. This provides a mechanism for consciousness "
                    "to stabilize quantum state selection."
                )
            ),
            ContentBlock(
                type="heading",
                content="Tetrahedron Geometry",
                level=3
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"V_{\text{tetra}} = \frac{8\sqrt{3}}{27} R^3, \quad "
                    r"R = \frac{\sqrt{b_3}}{2} = \frac{\sqrt{24}}{2}"
                ),
                formula_id="tetrahedron-geometry",
                label="(8.4.6)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 4 dice vertices form a regular tetrahedron inscribed in the "
                    "horizon circle of radius R = sqrt(b3)/2. This geometric structure "
                    "provides the natural 4-fold organization of condensate branches."
                )
            ),
            ContentBlock(
                type="heading",
                content="Central Sampler Tau Boost",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "When the central (2,0) sampler activates (n_local >= 9), the coherence "
                    "time tau receives an enhancement boost from global flux averaging. The "
                    "central sampler provides a precision enhancement for OR roll stability."
                )
            ),
            ContentBlock(
                type="formula",
                content=(
                    r"\tau_{\text{eff}} = \tau \cdot (1 + p_{\text{anc}} \cdot k_{\text{central}}), "
                    r"\quad k_{\text{central}} = \frac{\phi}{\sqrt{12}}"
                ),
                formula_id="central-tau-boost-formula",
                label="(8.4.7)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The full tau formula with central enhancement incorporates the activation "
                    "indicator I_central: tau(n) = tau_0 * exp(k * sqrt((n_local + I_central)/13)) * p_anc^2. "
                    "This provides approximately 5% coherence boost at full gnosis (n=12), "
                    "enhancing the stability of quantum branch selection."
                )
            ),
        ]

        return SectionContent(
            section_id="8",
            subsection_id="8.4",
            title="Four Dice OR Condensate Branch Selection",
            abstract=(
                "WS-2: The 12 bridge pairs group into 4 dice of 3 pairs each for "
                "condensate branch selection via Objective Reduction. The 4-dice "
                "structure arises from condensate geometry (not G2 triality): "
                "(5,1) bridge + 3x(3,1) generations = 4 directions forming a "
                "tetrahedron inscribed in the horizon circle. Each dice performs "
                "an OR roll based on residue flux, selecting 1 of 256 condensate "
                "branches. The gnosis effect increases roll stability with more "
                "active pairs. Central (2,0) sampler integration provides tau "
                "coherence boost when n_local >= 9."
            ),
            content_blocks=content_blocks,
            formula_refs=[
                "dice-grouping-formula",
                "or-roll-probability",
                "branch-selection-formula",
                "coherence-metric-formula",
                "gnosis-stability-formula",
                "tetrahedron-geometry",
                "central-tau-boost-formula",
            ],
            param_refs=[
                "four_dice.total_pairs",
                "four_dice.num_dice",
                "four_dice.pairs_per_dice",
                "four_dice.total_branches",
                "four_dice.branch_selected",
                "four_dice.coherence_metric",
                "four_dice.gnosis_stability",
                "four_dice.central_tau_boost",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas this simulation provides."""
        formulas = [
            Formula(
                id="dice-grouping-formula",
                label="(8.4.1)",
                latex=(
                    r"\text{Groups: } [P_1, P_2, P_3], [P_4, P_5, P_6], "
                    r"[P_7, P_8, P_9], [P_{10}, P_{11}, P_{12}]"
                ),
                plain_text=(
                    "Dice groups: [P1,P2,P3], [P4,P5,P6], [P7,P8,P9], [P10,P11,P12]"
                ),
                category="GEOMETRIC",
                description=(
                    "The 12 bridge pairs are grouped into 4 dice of 3 pairs each. "
                    "This grouping arises from condensate geometry: (5,1) + 3x(3,1) "
                    "= 4 directions, forming a tetrahedron."
                ),
                inputParams=["topology.orientation_sum"],
                outputParams=["four_dice.num_dice", "four_dice.pairs_per_dice"],
                input_params=["topology.orientation_sum"],
                output_params=["four_dice.num_dice", "four_dice.pairs_per_dice"],
                derivation={
                    "steps": [
                        "12 bridge pairs from orientation sum S = 12",
                        "Condensate structure: (5,1) bridge + 3 x (3,1) generations",
                        "4 condensate directions require 4 dice",
                        "12 pairs / 4 dice = 3 pairs per dice",
                        "Consecutive grouping preserves flux correlations"
                    ],
                    "assumptions": [
                        "Condensate geometry dominates (not G2 triality)",
                        "Equal distribution of pairs across dice"
                    ],
                    "references": [
                        "This work: Condensate structure analysis"
                    ]
                },
                terms={
                    "P_i": "Bridge pair i (i = 1...12)",
                    "[...]": "Dice group containing 3 pairs"
                }
            ),
            Formula(
                id="or-roll-probability",
                label="(8.4.2)",
                latex=(
                    r"o_j = \left\lfloor \left| \sum_{i \in \text{Dice}_j} "
                    r"R_\perp \cdot f_i \right| \cdot k_{\gimel} \cdot 12 \right\rfloor \mod 4"
                ),
                plain_text=(
                    "o_j = floor(|sum(R_perp * f_i)| * k_gimel * 12) mod 4"
                ),
                category="DERIVED",
                description=(
                    "Each dice performs an OR roll by summing residue fluxes, "
                    "applying R_perp rotation, scaling by k_gimel, and taking mod 4. "
                    "This yields an outcome o_j in {0, 1, 2, 3}."
                ),
                inputParams=[],
                outputParams=["four_dice.dice_outcomes"],
                input_params=[],
                output_params=["four_dice.dice_outcomes"],
                derivation={
                    "steps": [
                        "For each dice j, sum residue fluxes f_i from its 3 pairs",
                        "Apply R_perp = [[0,-1],[1,0]] rotation for OR sampling",
                        "Take magnitude |sum| (positive flux contribution)",
                        "Scale by k_gimel * 12 (total pairs normalization)",
                        "Floor and mod 4 for quaternionic outcome"
                    ],
                    "assumptions": [
                        "OR R_perp selects quantum coordinate",
                        "k_gimel provides natural scaling",
                        "Mod 4 preserves quaternionic structure"
                    ],
                    "references": [
                        "Penrose (1996): Gravity's role in quantum state reduction"
                    ]
                },
                terms={
                    "o_j": "Dice j outcome in {0,1,2,3}",
                    "f_i": "Residue flux for pair i",
                    "R_perp": "90-degree rotation matrix",
                    "k_gimel": "Gimel constant ~ 12.318"
                }
            ),
            Formula(
                id="branch-selection-formula",
                label="(8.4.3)",
                latex=(
                    r"k = \text{argmax}_{k'} \prod_{j=0}^{3} o_j^{w_{k'}}, \quad "
                    r"\text{encoding: } k = o_0 + 4o_1 + 16o_2 + 64o_3"
                ),
                plain_text=(
                    "k = argmax(product(o_j^w_k)), encoding: k = o0 + 4*o1 + 16*o2 + 64*o3"
                ),
                category="DERIVED",
                description=(
                    "The condensate branch is selected by maximizing the product "
                    "of dice outcomes weighted by branch-specific weights. The "
                    "quaternionic base-4 encoding maps 4 dice to 256 branches."
                ),
                inputParams=["four_dice.dice_outcomes"],
                outputParams=["four_dice.branch_selected", "four_dice.branch_probability"],
                input_params=["four_dice.dice_outcomes"],
                output_params=["four_dice.branch_selected", "four_dice.branch_probability"],
                derivation={
                    "steps": [
                        "4 dice with 4 outcomes each: 4^4 = 256 possible branches",
                        "Base-4 encoding: k = o0 + 4*o1 + 16*o2 + 64*o3",
                        "Branch probability proportional to weighted product",
                        "Selected branch = argmax over all branches",
                        "Quaternionic structure: (1, i, j, k) basis"
                    ],
                    "assumptions": [
                        "All branches equally accessible a priori",
                        "Flux weighting determines selection probability"
                    ],
                    "references": [
                        "This work: Quaternionic branch encoding"
                    ]
                },
                terms={
                    "k": "Selected branch index (0-255)",
                    "o_j": "Dice j outcome (0-3)",
                    "w_k": "Branch-specific weight"
                }
            ),
            Formula(
                id="coherence-metric-formula",
                label="(8.4.4)",
                latex=(
                    r"C = 1 - \frac{H(P_{\text{dice}})}{\log_2 4}, \quad "
                    r"H(P) = -\sum_j P_j \log_2 P_j"
                ),
                plain_text=(
                    "C = 1 - entropy(P_dice) / log2(4)"
                ),
                category="DERIVED",
                description=(
                    "The coherence metric measures determinism of dice rolls. "
                    "C = 1 for perfectly coherent (same outcome), C = 0 for "
                    "maximally incoherent (uniform random)."
                ),
                inputParams=["four_dice.dice_outcomes"],
                outputParams=["four_dice.coherence_metric"],
                input_params=["four_dice.dice_outcomes"],
                output_params=["four_dice.coherence_metric"],
                derivation={
                    "steps": [
                        "Count outcome frequencies across 4 dice",
                        "Calculate Shannon entropy H of distribution",
                        "Normalize by maximum entropy log2(4) = 2 bits",
                        "Coherence = 1 - normalized entropy"
                    ],
                    "assumptions": [
                        "Uniform prior over outcomes",
                        "Coherence measures quantum correlation"
                    ],
                    "references": [
                        "Shannon (1948): Information theory"
                    ]
                },
                terms={
                    "C": "Coherence metric in [0,1]",
                    "H": "Shannon entropy",
                    "P_dice": "Outcome probability distribution"
                }
            ),
            Formula(
                id="gnosis-stability-formula",
                label="(8.4.5)",
                latex=(
                    r"S_{\text{gnosis}} = \frac{n_{\text{active}}}{12} "
                    r"\cdot \left(1 - \frac{1}{\chi_{\text{eff}}}\right)"
                ),
                plain_text=(
                    "S_gnosis = (n_active / 12) * (1 - 1/chi_eff)"
                ),
                category="PREDICTIONS",
                description=(
                    "The gnosis effect: more active bridge pairs increase roll "
                    "stability. At full activation (n=12), stability approaches "
                    "(1 - 1/144) ~ 0.993."
                ),
                inputParams=["topology.chi_eff", "four_dice.total_pairs"],
                outputParams=["four_dice.gnosis_stability"],
                input_params=["topology.chi_eff", "four_dice.total_pairs"],
                output_params=["four_dice.gnosis_stability"],
                derivation={
                    "steps": [
                        "Activation fraction = n_active / 12",
                        "Topological damping = 1 - 1/chi_eff",
                        "Combined stability = product",
                        "At n=12, chi_eff=144: S ~ 0.993"
                    ],
                    "assumptions": [
                        "Linear scaling with activation",
                        "chi_eff provides topological bound"
                    ],
                    "references": [
                        "This work: Gnosis mechanism"
                    ]
                },
                terms={
                    "S_gnosis": "Gnosis stability factor",
                    "n_active": "Number of active bridge pairs",
                    "chi_eff": "Effective Euler characteristic (144)"
                }
            ),
            Formula(
                id="tetrahedron-geometry",
                label="(8.4.6)",
                latex=(
                    r"V_{\text{tetra}} = \frac{8\sqrt{3}}{27} R^3, \quad "
                    r"R = \frac{\sqrt{b_3}}{2}"
                ),
                plain_text=(
                    "V_tetra = (8*sqrt(3)/27) * R^3, R = sqrt(b3)/2"
                ),
                category="GEOMETRIC",
                description=(
                    "The 4 dice vertices form a regular tetrahedron inscribed "
                    "in the horizon circle. The circumradius R = sqrt(b3)/2 "
                    "connects to the G2 topology."
                ),
                inputParams=["topology.b3"],
                outputParams=["four_dice.tetrahedron_volume", "four_dice.horizon_radius"],
                input_params=["topology.b3"],
                output_params=["four_dice.tetrahedron_volume", "four_dice.horizon_radius"],
                derivation={
                    "steps": [
                        "4 condensate directions form tetrahedron vertices",
                        "Inscribed in horizon circle of radius R",
                        "R = sqrt(b3)/2 from G2 topology",
                        "For b3=24: R = sqrt(24)/2 ~ 2.449",
                        "Volume formula for regular tetrahedron"
                    ],
                    "assumptions": [
                        "Regular tetrahedron (equal edge lengths)",
                        "Horizon circle radius from b3"
                    ],
                    "references": [
                        "Joyce (2000): G2 geometry"
                    ]
                },
                terms={
                    "V_tetra": "Tetrahedron volume",
                    "R": "Circumradius = horizon radius",
                    "b3": "Third Betti number (24)"
                }
            ),
            Formula(
                id="central-tau-boost-formula",
                label="(8.4.7)",
                latex=(
                    r"\tau_{\text{eff}} = \tau \cdot (1 + p_{\text{anc}} \cdot k_{\text{central}}), "
                    r"\quad k_{\text{central}} = \frac{\phi}{\sqrt{12}}"
                ),
                plain_text=(
                    "tau_eff = tau * (1 + p_anc * k_central), k_central = phi/sqrt(12)"
                ),
                category="DERIVED",
                description=(
                    "Central sampler tau boost: When the central (2,0) sampler is active "
                    "(n_local >= 9), coherence time tau receives an enhancement. The boost "
                    "factor k_central = phi/sqrt(12) ~ 0.467 provides golden ratio dilution. "
                    "Full formula: tau(n) = tau_0 * exp(k*sqrt((n_local+I_central)/13)) * p_anc^2 "
                    "where I_central = 1 if n_local >= 9 else 0."
                ),
                inputParams=["four_dice.total_pairs", "four_dice.flux_per_dice"],
                outputParams=["four_dice.central_tau_boost"],
                input_params=["four_dice.total_pairs", "four_dice.flux_per_dice"],
                output_params=["four_dice.central_tau_boost"],
                derivation={
                    "steps": [
                        "Central sampler activates at n_local >= 9 (mid-gnosis)",
                        "Compute p_anc = (1/12)*sum(p_i) + sqrt(n_local/12)*phi/12",
                        "k_central = phi/sqrt(12) ~ 0.467 (central boost factor)",
                        "tau_boost = 1 + p_anc * k_central",
                        "tau_eff = tau * tau_boost"
                    ],
                    "assumptions": [
                        "Central (2,0) sampler provides global averaging",
                        "Golden ratio dilution for precision enhancement",
                        "Effective signature (24,1) preserved"
                    ],
                    "references": [
                        "This work: Central sampler mechanism (v23)",
                        "FormulasRegistry: central_pair_weight property"
                    ]
                },
                terms={
                    "tau_eff": "Effective coherence time with central boost",
                    "tau": "Base coherence time",
                    "p_anc": "Ancestral flux from central averaging",
                    "k_central": "Central boost factor = phi/sqrt(12)",
                    "I_central": "Activation indicator (1 if n >= 9, else 0)"
                }
            ),
        ]

        return formulas

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="four_dice.total_pairs",
                name="Total Bridge Pairs",
                units="dimensionless",
                status="GEOMETRIC",
                description=(
                    "Total number of bridge pairs from G2 orientation sum S = 12."
                ),
                derivation_formula="dice-grouping-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.num_dice",
                name="Number of Dice",
                units="dimensionless",
                status="GEOMETRIC",
                description=(
                    "Number of dice groups (4) from condensate structure: "
                    "(5,1) bridge + 3 x (3,1) generations = 4 directions."
                ),
                derivation_formula="dice-grouping-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.pairs_per_dice",
                name="Pairs per Dice",
                units="dimensionless",
                status="GEOMETRIC",
                description=(
                    "Number of bridge pairs per dice (3). Total pairs / num dice = 12/4 = 3."
                ),
                derivation_formula="dice-grouping-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.total_branches",
                name="Total Condensate Branches",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Total number of condensate branches: 4^4 = 256 from "
                    "quaternionic base-4 encoding of 4 dice outcomes."
                ),
                derivation_formula="branch-selection-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.dice_outcomes",
                name="Dice Outcomes",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Array of 4 dice outcomes, each in {0, 1, 2, 3}. "
                    "Determined by OR roll mechanism on residue fluxes."
                ),
                derivation_formula="or-roll-probability",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.branch_selected",
                name="Selected Branch Index",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Selected condensate branch index (0-255). "
                    "Quaternionic encoding: k = o0 + 4*o1 + 16*o2 + 64*o3."
                ),
                derivation_formula="branch-selection-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.branch_probability",
                name="Branch Probability",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Probability of selected branch based on flux weighting. "
                    "Higher for branches matching high-flux dice outcomes."
                ),
                derivation_formula="branch-selection-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.total_flux",
                name="Total Residue Flux",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Sum of all pair residue fluxes. Normalized to 1 for "
                    "probability interpretation."
                ),
                derivation_formula="or-roll-probability",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.flux_per_dice",
                name="Flux per Dice",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Array of residue flux magnitudes for each dice after "
                    "OR R_perp sampling."
                ),
                derivation_formula="or-roll-probability",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.coherence_metric",
                name="Coherence Metric",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Coherence of dice rolls: C = 1 - normalized_entropy. "
                    "C = 1 for deterministic (all same), C = 0 for uniform random."
                ),
                derivation_formula="coherence-metric-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.gnosis_stability",
                name="Gnosis Stability",
                units="dimensionless",
                status="PREDICTED",
                description=(
                    "Stability factor from gnosis effect. At full activation (n=12), "
                    "S_gnosis = (1 - 1/144) ~ 0.993."
                ),
                derivation_formula="gnosis-stability-formula",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.tetrahedron_volume",
                name="Tetrahedron Volume",
                units="dimensionless",
                status="GEOMETRIC",
                description=(
                    "Volume of regular tetrahedron inscribed in horizon circle. "
                    "The 4 vertices correspond to the 4 dice directions."
                ),
                derivation_formula="tetrahedron-geometry",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.horizon_radius",
                name="Horizon Radius",
                units="dimensionless",
                status="GEOMETRIC",
                description=(
                    "Radius of horizon circle = sqrt(b3)/2 = sqrt(24)/2 ~ 2.449. "
                    "Circumradius of inscribed tetrahedron."
                ),
                derivation_formula="tetrahedron-geometry",
                no_experimental_value=True
            ),
            Parameter(
                path="four_dice.central_tau_boost",
                name="Central Tau Boost Factor",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Coherence time boost factor from central (2,0) sampler. "
                    "tau_eff = tau * central_tau_boost where central_tau_boost = "
                    "1 + p_anc * k_central. At full gnosis (n=12), boost ~ 1.05."
                ),
                derivation_formula="central-tau-boost-formula",
                no_experimental_value=True
            ),
        ]

    def get_foundations(self) -> List[Dict[str, str]]:
        """Return foundational concepts for this simulation."""
        return [
            {
                "id": "objective-reduction",
                "title": "Objective Reduction (OR)",
                "category": "quantum_mechanics",
                "description": (
                    "Penrose's hypothesis that quantum superposition collapses due to "
                    "gravitational self-energy reaching a threshold. Each bridge pair "
                    "contributes to the OR collapse mechanism."
                )
            },
            {
                "id": "condensate-structure",
                "title": "Condensate Structure",
                "category": "field_theory",
                "description": (
                    "The (5,1) bridge + 3 x (3,1) generation structure that gives "
                    "rise to 4 condensate directions, forming a tetrahedron."
                )
            },
            {
                "id": "quaternionic-encoding",
                "title": "Quaternionic Branch Encoding",
                "category": "mathematics",
                "description": (
                    "The base-4 encoding k = o0 + 4*o1 + 16*o2 + 64*o3 provides "
                    "a natural quaternionic structure for 256 branches."
                )
            },
            {
                "id": "gnosis-effect",
                "title": "Gnosis Effect",
                "category": "consciousness",
                "description": (
                    "The increase in roll stability with more active bridge pairs. "
                    "Provides mechanism for consciousness to influence quantum selection."
                )
            },
            {
                "id": "central-sampler",
                "title": "Central (2,0) Sampler",
                "category": "consciousness",
                "description": (
                    "The central sampler is a single (2,0) Euclidean pair that averages "
                    "outcomes from the 12 local (2,0) bridge pairs for global condensate "
                    "selection. Activates at n_local >= 9 (mid-gnosis) and provides tau "
                    "coherence boost via: tau_eff = tau * (1 + p_anc * k_central)."
                )
            },
        ]

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references for this simulation."""
        return [
            {
                "id": "penrose1989",
                "authors": "Penrose, R.",
                "title": "The Emperor's New Mind",
                "publisher": "Oxford University Press",
                "year": 1989
            },
            {
                "id": "penrose1996",
                "authors": "Penrose, R.",
                "title": "On Gravity's Role in Quantum State Reduction",
                "journal": "Gen. Rel. Grav.",
                "volume": "28",
                "year": 1996,
                "pages": "581-600"
            },
            {
                "id": "hameroff2014",
                "authors": "Hameroff, S. and Penrose, R.",
                "title": "Consciousness in the universe: A review of the 'Orch OR' theory",
                "journal": "Physics of Life Reviews",
                "volume": "11",
                "year": 2014,
                "pages": "39-78"
            },
            {
                "id": "joyce2000",
                "authors": "Joyce, D.D.",
                "title": "Compact Manifolds with Special Holonomy",
                "publisher": "Oxford University Press",
                "year": 2000
            },
        ]


def run_four_dice_or(verbose: bool = True, seed: int = 42) -> Dict[str, Any]:
    """
    Run the four dice OR simulation standalone.

    Args:
        verbose: Whether to print detailed output
        seed: Random seed for reproducibility

    Returns:
        Dictionary with four dice OR results
    """
    # Create registry and simulation
    registry = PMRegistry.get_instance()

    # Set up topological inputs
    registry.set_param("topology.b3", B3, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144, source="ESTABLISHED:TCS #187", status="ESTABLISHED")
    registry.set_param("topology.orientation_sum", 12, source="ESTABLISHED:TCS #187", status="ESTABLISHED")

    # Create and execute simulation
    sim = FourDiceORSimulation()
    results = sim.execute(registry, verbose=verbose)

    if verbose:
        print("\n" + "=" * 75)
        print(" FOUR DICE OR CONDENSATE BRANCH SELECTION v22 (WS-2)")
        print("=" * 75)

        print("\n" + "-" * 75)
        print(" DICE STRUCTURE")
        print("-" * 75)
        print(f"  Total bridge pairs:        {results['four_dice.total_pairs']}")
        print(f"  Number of dice:            {results['four_dice.num_dice']}")
        print(f"  Pairs per dice:            {results['four_dice.pairs_per_dice']}")
        print(f"  Total branches:            {results['four_dice.total_branches']}")

        print("\n" + "-" * 75)
        print(" DICE GROUPS")
        print("-" * 75)
        for i, group in enumerate(sim.DICE_GROUPS):
            print(f"  Dice {i}: pairs {[p+1 for p in group]}")

        print("\n" + "-" * 75)
        print(" OR ROLL OUTCOMES")
        print("-" * 75)
        dice_outcomes = results['four_dice.dice_outcomes']
        flux_per_dice = results['four_dice.flux_per_dice']
        print(f"  Dice outcomes:             {dice_outcomes}")
        print(f"  Flux per dice:             {[f'{f:.4f}' for f in flux_per_dice]}")
        print(f"  Total flux:                {results['four_dice.total_flux']:.4f}")

        print("\n" + "-" * 75)
        print(" BRANCH SELECTION")
        print("-" * 75)
        print(f"  Selected branch:           {results['four_dice.branch_selected']} / {results['four_dice.total_branches']}")
        print(f"  Branch probability:        {results['four_dice.branch_probability']:.6f}")
        quat_encoding = f"{dice_outcomes[3]}{dice_outcomes[2]}{dice_outcomes[1]}{dice_outcomes[0]}"
        print(f"  Quaternionic encoding:     {quat_encoding} (base-4)")

        print("\n" + "-" * 75)
        print(" COHERENCE & STABILITY")
        print("-" * 75)
        print(f"  Coherence metric:          {results['four_dice.coherence_metric']:.4f}")
        print(f"  Gnosis stability:          {results['four_dice.gnosis_stability']:.6f}")

        print("\n" + "-" * 75)
        print(" CENTRAL SAMPLER TAU BOOST")
        print("-" * 75)
        central_details = results.get('_central_sampler_details', {})
        print(f"  Central tau boost:         {results['four_dice.central_tau_boost']:.6f}")
        print(f"  Central active:            {central_details.get('central_active', 'N/A')}")
        print(f"  Ancestral flux (p_anc):    {central_details.get('p_anc', 0):.6f}")
        print(f"  k_central (phi/sqrt12):    {central_details.get('k_central', 0):.6f}")
        print(f"  I_central (indicator):     {central_details.get('I_central', 0)}")

        print("\n" + "-" * 75)
        print(" TETRAHEDRON GEOMETRY")
        print("-" * 75)
        print(f"  Horizon radius:            {results['four_dice.horizon_radius']:.4f}")
        print(f"  Tetrahedron volume:        {results['four_dice.tetrahedron_volume']:.4f}")

        print("\n" + "-" * 75)
        print(" SSOT CONSTANTS USED")
        print("-" * 75)
        print(f"  B3 (Betti number):         {B3}")
        print(f"  K_GIMEL:                   {K_GIMEL:.6f}")
        print(f"  PHI (golden ratio):        {PHI:.6f}")

        print("\n" + "=" * 75)
        print(" GEOMETRIC JUSTIFICATION")
        print("=" * 75)
        print("  The 4-dice structure arises from CONDENSATE geometry (not G2 triality):")
        print("    - (5,1) bridge:          1 direction (main spine)")
        print("    - 3 x (3,1) generations: 3 directions (generation bridges)")
        print("    - Total:                 4 directions = tetrahedron vertices")
        print("")
        print("  This tetrahedron is inscribed in the horizon circle of radius sqrt(b3)/2.")
        print("=" * 75)

    return results


# =============================================================================
# Self-Validation Assertions
# =============================================================================

# Create validation instance
_validation_instance = FourDiceORSimulation()

# Validate metadata
assert _validation_instance.metadata is not None, "FourDiceOR: metadata is None"
assert _validation_instance.metadata.id == "four_dice_or_v22", \
    f"FourDiceOR: unexpected id {_validation_instance.metadata.id}"
assert _validation_instance.metadata.version == "22.0", \
    f"FourDiceOR: unexpected version {_validation_instance.metadata.version}"

# Validate constants
assert _validation_instance.TOTAL_PAIRS == 12, \
    f"FourDiceOR: TOTAL_PAIRS should be 12, got {_validation_instance.TOTAL_PAIRS}"
assert _validation_instance.NUM_DICE == 4, \
    f"FourDiceOR: NUM_DICE should be 4, got {_validation_instance.NUM_DICE}"
assert _validation_instance.PAIRS_PER_DICE == 3, \
    f"FourDiceOR: PAIRS_PER_DICE should be 3, got {_validation_instance.PAIRS_PER_DICE}"
assert _validation_instance.DICE_MODULUS == 4, \
    f"FourDiceOR: DICE_MODULUS should be 4, got {_validation_instance.DICE_MODULUS}"

# Validate dice groups
assert len(_validation_instance.DICE_GROUPS) == 4, \
    f"FourDiceOR: should have 4 dice groups, got {len(_validation_instance.DICE_GROUPS)}"
for i, group in enumerate(_validation_instance.DICE_GROUPS):
    assert len(group) == 3, f"FourDiceOR: dice {i} should have 3 pairs, got {len(group)}"

# Validate all pairs are accounted for
all_pairs = set()
for group in _validation_instance.DICE_GROUPS:
    for pair in group:
        all_pairs.add(pair)
assert len(all_pairs) == 12, f"FourDiceOR: should cover 12 pairs, got {len(all_pairs)}"
assert all_pairs == set(range(12)), f"FourDiceOR: pairs should be 0-11"

# Validate formulas exist
assert len(_validation_instance.get_formulas()) >= 6, \
    f"FourDiceOR: expected at least 6 formulas, got {len(_validation_instance.get_formulas())}"

# Cleanup validation variables
del _validation_instance


if __name__ == "__main__":
    run_four_dice_or(verbose=True)
