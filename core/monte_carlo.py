"""
Monte Carlo Configuration Module
================================

Centralized configuration for Monte Carlo simulations.

Single Responsibility: Only handles MC sampling parameters.

v12.7: Increased from 1,000 to 10,000 samples for tighter confidence intervals.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass(frozen=True)
class MonteCarloConfig:
    """
    Monte Carlo simulation configuration.

    Centralized configuration for consistent MC precision across all simulations.
    Increasing samples reduces statistical variance at cost of computation time.

    Performance benchmarks (approximate):
    - 1,000 samples: ~1-2 seconds per simulation
    - 10,000 samples: ~10-20 seconds per simulation
    - 100,000 samples: ~2-3 minutes per simulation

    Statistical precision improvement:
    - Standard error ~ 1/sqrt(N)
    - 10x samples = ~3.16x tighter confidence intervals
    - 100x samples = ~10x tighter confidence intervals
    """
    # Primary sample count for uncertainty propagation
    N_SAMPLES: int = 10_000

    # Quick validation mode (reduced samples for testing)
    N_SAMPLES_QUICK: int = 1_000

    # High precision mode (for final publication runs)
    N_SAMPLES_HIGH: int = 100_000

    # Random seed for reproducibility (None = use system time)
    SEED: Optional[int] = None

    # Convergence thresholds
    CONVERGENCE_RTOL: float = 0.01  # 1% relative tolerance
    MIN_SAMPLES_FOR_CONFIDENCE: int = 100

    # Percentiles for confidence intervals
    CI_68_LOW: float = 16.0   # 68% CI lower bound
    CI_68_HIGH: float = 84.0  # 68% CI upper bound
    CI_95_LOW: float = 2.5    # 95% CI lower bound
    CI_95_HIGH: float = 97.5  # 95% CI upper bound

    def get_samples(self, mode: str = "standard") -> int:
        """
        Get sample count based on mode.

        Args:
            mode: "quick" | "standard" | "high"

        Returns:
            Number of MC samples to use
        """
        modes = {
            "quick": self.N_SAMPLES_QUICK,
            "standard": self.N_SAMPLES,
            "high": self.N_SAMPLES_HIGH,
        }
        return modes.get(mode, self.N_SAMPLES)

    def set_seed(self) -> None:
        """Set numpy random seed if configured"""
        if self.SEED is not None:
            np.random.seed(self.SEED)


# Singleton instance
_mc_config: Optional[MonteCarloConfig] = None


def get_mc_config() -> MonteCarloConfig:
    """Get singleton MonteCarloConfig instance"""
    global _mc_config
    if _mc_config is None:
        _mc_config = MonteCarloConfig()
    return _mc_config


def get_n_samples(mode: str = "standard") -> int:
    """
    Convenience function to get sample count.

    Args:
        mode: "quick" | "standard" | "high"

    Returns:
        Number of MC samples to use
    """
    return get_mc_config().get_samples(mode)


# Export default sample count for backward compatibility
N_SAMPLES_DEFAULT = 10_000
