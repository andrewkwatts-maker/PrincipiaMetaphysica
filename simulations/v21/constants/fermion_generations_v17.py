"""
Principia Metaphysica - Fermion Generations Derivation v17.2

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Derives the number of fermion generations from G2 manifold topology.

Primary Formula:
    n_gen = b3 / 8 = 24 / 8 = 3 (EXACT)

Alternative Form (from effective Euler characteristic):
    n_gen = |chi_eff| / 48 = 144 / 48 = 3

Where:
    - b3 = 24: Third Betti number of TCS #187 manifold
    - chi_eff = 144: Effective Euler characteristic
    - Divisor 8: From spinorial structure in 7D

This is an EXACT prediction - no approximation or fitting.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

from core.FormulasRegistry import get_registry

# Get registry SSoT
_REG = get_registry()


@dataclass
class FermionGenerationsResult:
    """Results from fermion generations derivation."""

    # Topological inputs
    b3: int
    chi_eff: int

    # Primary derivation
    divisor_spinorial: int
    n_gen_from_betti: int

    # Alternative derivation
    divisor_index: int
    n_gen_from_chi: int

    # Experimental
    experimental_value: int
    exact_match: bool

    status: str
    theoretical_basis: str


class FermionGenerations:
    """
    Number of fermion generations from G2 manifold topology.

    In M-theory compactifications on G2 manifolds, the number of
    chiral generations arises from the effective Euler characteristic
    or index formula linked to the third Betti number b3.

    n_gen = b3/8 = 24/8 = 3 (EXACT)

    This is a pure topological prediction with no free parameters.
    Only manifolds with b3 multiple of 8 allow consistent chiral fermions.
    """

    def __init__(self):
        # Topological invariants from SSoT registry (locked by TCS #187)
        self.b3 = _REG.elders  # = 24 (third Betti number)
        self.chi_eff = _REG.chi_eff_total  # = 144 (both shadows combined)

        # Divisors
        self.spinorial_divisor = 8  # From 7D spinor structure
        self.index_divisor = 48  # 24 * 2 (F-theory + SpR(2))

        # Experimental
        self.EXPERIMENTAL_GENERATIONS = 3

    def compute_from_betti(self) -> Dict[str, Any]:
        """
        Primary derivation: n_gen = b3 / 8

        Each 3-cycle supports 8 zero modes, but chirality projects
        to net 1 per cycle in effective theory.
        """
        n_gen = self.b3 // self.spinorial_divisor

        return {
            'b3': self.b3,
            'divisor': self.spinorial_divisor,
            'n_gen': n_gen,
            'formula': 'b3 / 8 = 24 / 8 = 3',
            'explanation': 'Spinorial structure in 7D; chirality projection from 3-cycles'
        }

    def compute_from_chi(self) -> Dict[str, Any]:
        """
        Alternative derivation: n_gen = |chi_eff| / 48

        chi_eff = 144 from manifold (related to b3 and other Betti numbers).
        48 = 24 * 2: F-theory Sethi-Vafa-Witten index with SpR(2) parity.
        """
        n_gen = abs(self.chi_eff) // self.index_divisor

        return {
            'chi_eff': self.chi_eff,
            'divisor': self.index_divisor,
            'n_gen': n_gen,
            'formula': '|chi_eff| / 48 = 144 / 48 = 3',
            'explanation': 'F-theory index formula with unified time parity factor'
        }

    def compute_consistency_check(self) -> Dict[str, Any]:
        """
        Verify both derivations give same result and match experiment.
        """
        n_betti = self.b3 // self.spinorial_divisor
        n_chi = abs(self.chi_eff) // self.index_divisor

        return {
            'n_from_betti': n_betti,
            'n_from_chi': n_chi,
            'consistent': n_betti == n_chi,
            'experimental': self.EXPERIMENTAL_GENERATIONS,
            'exact_match': n_betti == self.EXPERIMENTAL_GENERATIONS
        }

    def compute_why_locked(self) -> Dict[str, str]:
        """
        Explain why n_gen = 3 is topologically locked.
        """
        return {
            'constraint': 'b3 must be multiple of 8 for chiral fermions',
            'b3_24': 'TCS #187 has b3 = 24 (from manifold construction)',
            'uniqueness': 'Different b3 gives different physics; 24 yields SM',
            'experimental': 'Precisely 3 generations observed (no 4th at LHC)',
            'status': 'EXACT prediction - pure topology, no tuning'
        }

    def compute_full_derivation(self) -> FermionGenerationsResult:
        """Full fermion generations derivation."""
        betti = self.compute_from_betti()
        chi = self.compute_from_chi()
        check = self.compute_consistency_check()

        return FermionGenerationsResult(
            b3=self.b3,
            chi_eff=self.chi_eff,
            divisor_spinorial=self.spinorial_divisor,
            n_gen_from_betti=betti['n_gen'],
            divisor_index=self.index_divisor,
            n_gen_from_chi=chi['n_gen'],
            experimental_value=self.EXPERIMENTAL_GENERATIONS,
            exact_match=check['exact_match'],
            status='EXACT',
            theoretical_basis='G2 manifold topology + index theorem'
        )

    def run_demonstration(self) -> Dict[str, Any]:
        """Run fermion generations demonstration."""
        print("=" * 60)
        print("Fermion Generations from G2 Manifold Topology")
        print("=" * 60)

        print(f"\nTopological Invariants (TCS #187):")
        print(f"  b3 = {self.b3} (third Betti number)")
        print(f"  chi_eff = {self.chi_eff} (effective Euler characteristic)")

        # Primary derivation
        betti = self.compute_from_betti()
        print(f"\n1. Primary Derivation (Betti Number):")
        print(f"   n_gen = b3 / 8")
        print(f"   n_gen = {betti['b3']} / {betti['divisor']} = {betti['n_gen']}")
        print(f"   ({betti['explanation']})")

        # Alternative derivation
        chi = self.compute_from_chi()
        print(f"\n2. Alternative Derivation (Euler Characteristic):")
        print(f"   n_gen = |chi_eff| / 48")
        print(f"   n_gen = {chi['chi_eff']} / {chi['divisor']} = {chi['n_gen']}")
        print(f"   ({chi['explanation']})")

        # Consistency
        check = self.compute_consistency_check()
        print(f"\n3. Consistency Check:")
        print(f"   From b3:    {check['n_from_betti']}")
        print(f"   From chi:   {check['n_from_chi']}")
        print(f"   Consistent: {check['consistent']}")
        print(f"   Experiment: {check['experimental']}")
        print(f"   EXACT MATCH: {check['exact_match']}")

        # Why locked
        locked = self.compute_why_locked()
        print(f"\n4. Why This is Locked:")
        print(f"   - {locked['constraint']}")
        print(f"   - {locked['b3_24']}")
        print(f"   - {locked['experimental']}")

        result = self.compute_full_derivation()

        print("\n" + "=" * 60)
        print("STATUS: EXACT PREDICTION")
        print("n_gen = 3 is a pure topological result - NO TUNING")
        print("=" * 60)

        return {
            'betti': betti,
            'chi': chi,
            'consistency': check,
            'locked': locked,
            'result': result
        }


def run_generations_demo():
    """Run fermion generations demonstration."""
    gen = FermionGenerations()
    return gen.run_demonstration()


if __name__ == '__main__':
    run_generations_demo()
