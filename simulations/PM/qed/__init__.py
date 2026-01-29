"""
Principia Metaphysica - QED Simulations v23.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

QED (Quantum Electrodynamics) constants derived from the Decad-Cubic Projection Engine.

ADJUSTMENT REGISTRY:
- Inverse Cubic 1/(1+e): Compton, Avogadro, Faraday, Weak Mixing (contraction/coupling)
- Double-Gate (1+e)(1-e)^2: Rydberg, Bohr Radius (standing wave)
- Inverse Double-Gate: Hartree Energy (binding energy)
- Direct Expansion (1+e): Magnetic Flux, Von Klitzing (propagation)
- Quad-Gate (1+e)^4: Stefan-Boltzmann (4D thermal)
- Neutral (no adjustment): Molar Gas Constant (N_A * k cancellation)
"""

from .compton_wavelength import ComptonWavelengthV17
from .stefan_boltzmann import StefanBoltzmannV17
from .hartree_energy import HartreeEnergyV17
from .magnetic_flux import MagneticFluxV17
from .von_klitzing import VonKlitzingV17
from .avogadro import AvogadroV17
from .faraday import FaradayV17
from .molar_gas import MolarGasV17
from .weak_mixing import WeakMixingV17

__all__ = [
    "ComptonWavelengthV17",
    "StefanBoltzmannV17",
    "HartreeEnergyV17",
    "MagneticFluxV17",
    "VonKlitzingV17",
    "AvogadroV17",
    "FaradayV17",
    "MolarGasV17",
    "WeakMixingV17",
]

__version__ = "23.0"
