"""
Principia Metaphysica - QED Simulations v17.2

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

from .compton_wavelength_v17_2 import ComptonWavelengthV17
from .stefan_boltzmann_v17_2 import StefanBoltzmannV17
from .hartree_energy_v17_2 import HartreeEnergyV17
from .magnetic_flux_v17_2 import MagneticFluxV17
from .von_klitzing_v17_2 import VonKlitzingV17
from .avogadro_v17_2 import AvogadroV17
from .faraday_v17_2 import FaradayV17
from .molar_gas_v17_2 import MolarGasV17
from .weak_mixing_v17_2 import WeakMixingV17

# v18 SimulationBase wrapper
from .qed_simulation_v18 import QEDSimulationV18, run_qed_simulation

__all__ = [
    # V17 classes
    'ComptonWavelengthV17',
    'StefanBoltzmannV17',
    'HartreeEnergyV17',
    'MagneticFluxV17',
    'VonKlitzingV17',
    'AvogadroV17',
    'FaradayV17',
    'MolarGasV17',
    'WeakMixingV17',
    # V18 wrapper
    'QEDSimulationV18',
    'run_qed_simulation',
]

__version__ = "19.2"
