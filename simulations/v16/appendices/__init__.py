"""
Principia Metaphysica v16 - Appendices Module
==============================================

Section 8: Appendices (A-D)

This module contains four comprehensive appendices documenting the
mathematical foundations, computational methods, extended derivations,
and parameter tables for Principia Metaphysica.

Appendices:
-----------
- Appendix A: Mathematical Foundations
  * G2 holonomy and exceptional geometry
  * Spinor structures and Clifford algebras
  * Differential geometry on 7-manifolds
  * Fiber bundles and K3 surfaces
  * Cohomology and characteristic classes

- Appendix B: Computational Methods
  * Renormalization group equations (3-loop)
  * Numerical integration techniques
  * Threshold corrections (KK towers)
  * Asymptotic safety corrections
  * Optimization algorithms

- Appendix C: Extended Derivations
  * G2 holonomy from parallel spinor
  * Gauge coupling unification
  * Fermion mass hierarchies
  * Neutrino mixing from A₄ symmetry
  * Higgs mass from moduli stabilization
  * Proton lifetime from cycle separation

- Appendix D: Parameter Tables
  * Physical constants (M_Planck, α_em, etc.)
  * PDG experimental values
  * Geometric/topological parameters
  * Gauge coupling evolution
  * Theory predictions and experimental status

Usage:
------
    from simulations.v16.appendices import (
        AppendixAMathFoundations,
        AppendixBComputationalMethods,
        AppendixCExtendedDerivations,
        AppendixDParameterTables,
    )

    # Create appendix instances
    appendix_a = AppendixAMathFoundations()
    appendix_b = AppendixBComputationalMethods()
    appendix_c = AppendixCExtendedDerivations()
    appendix_d = AppendixDParameterTables()

    # Execute with registry
    results_a = appendix_a.execute(registry, verbose=True)
    results_b = appendix_b.execute(registry, verbose=True)
    results_c = appendix_c.execute(registry, verbose=True)
    results_d = appendix_d.execute(registry, verbose=True)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .appendix_a_math_v16_0 import AppendixAMathFoundations
from .appendix_b_methods_v16_0 import AppendixBComputationalMethods
from .appendix_c_derivations_v16_0 import AppendixCExtendedDerivations
from .appendix_d_tables_v16_0 import AppendixDParameterTables

__all__ = [
    'AppendixAMathFoundations',
    'AppendixBComputationalMethods',
    'AppendixCExtendedDerivations',
    'AppendixDParameterTables',
]

__version__ = "16.0"
