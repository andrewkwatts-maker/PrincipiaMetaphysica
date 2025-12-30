# Principia Metaphysica - Computational Physics Package

**Version:** v16.2
**Author:** Andrew Keith Watts
**License:** MIT (code), See LICENSE for theory content
**Created:** December 29, 2025
**DOI:** [TBD - Awaiting Zenodo assignment]

## Overview

This package contains the complete computational implementation of **Principia Metaphysica (PM)**, a geometric unification theory that derives fundamental physics from G2 manifold topology. All Standard Model parameters and cosmological predictions emerge from a single topological invariant: the Betti number **b₃ = 24**.

## What's Included

This Zenodo package is organized into 5 thematic directories containing 24 Python files (15,000+ lines of code) implementing:

- **Geometric foundations** from G2 manifold topology
- **Cosmological predictions** (dark energy, Hubble tension, structure formation)
- **Particle physics** (neutrino mixing, CKM matrix, fermion masses)
- **Quantum biology** (consciousness, decoherence suppression)
- **Verification tools** (cryptographic hashes, validation suite, Wolfram integration)

## Directory Structure

```
zenodo_package/
├── 01_Foundations/          # Core geometric derivations from G2 topology
├── 02_Cosmology/            # Dark energy, S8, Hubble tension
├── 03_Particle_Physics/     # Neutrino mixing, CKM, fermion masses
├── 04_Quantum_Biology/      # Pneuma mechanism, decoherence
├── 05_Verification/         # Discovery hashes, validators, audit trails
├── index.json               # Complete file inventory with descriptions
├── PACKAGE_README.md        # This file
└── LICENSE                  # MIT license
```

### 01_Foundations (5 files)

Core geometric engine deriving all PM parameters from the Betti number b₃=24:

- **geometric_anchors_v16_1.py** - Main class deriving parameters from topology
- **geometric_anchors_derivations.py** - Mathematical derivations
- **g2_geometry_v16_0.py** - Complete G2 manifold implementation (74 KB)
- **g2_geometry_derivations.py** - G2 theory foundations
- **g2_dynamical_flow_v16_2.py** - Ricci flow vacuum selection

**Key Result:** All parameters derived from single number (b₃=24), eliminating tuning.

### 02_Cosmology (5 files)

Cosmological predictions testable by current/near-future experiments:

- **dark_energy_v16_0.py** - Predicts **w₀ = -11/13 ≈ -0.846** (DESI 2025: -0.827 ± 0.063, 1.3σ)
- **s8_suppression_v16_1.py** - S8 tension analysis (PM: 0.837, between Planck 0.832 and KiDS 0.766)
- **multi_sector_v16_0.py** - Shadow sector cosmology
- **cosmology_derivations.py** - Complete derivation chain
- **hubble_tension_resolver_v16_1.py** - H0 tension analysis

**Key Result:** w₀ prediction differs from ΛCDM, testable by DESI/Euclid.

### 03_Particle_Physics (6 files)

Parameter-free predictions for Standard Model and beyond:

- **neutrino_mixing_v16_0.py** - All mixing angles within 1σ of NuFit 6.0
  - θ₁₂ = 33.82° (NuFit: 33.41° ± 0.75°)
  - θ₂₃ = 42.3° (NuFit: 42.1° - 50.0°)
  - θ₁₃ = 8.61° (NuFit: 8.58° ± 0.12°)
  - Δm²₂₁ = 7.53 × 10⁻⁵ eV² (exact match)
  - Δm²₃₁ = 2.453 × 10⁻³ eV² (exact match)

- **ckm_matrix_v16_0.py** - CKM matrix from G2 Froggatt-Nielsen mechanism
  - Jarlskog invariant J = 2.9 × 10⁻⁵ (PDG: 3.0 ± 0.3 × 10⁻⁵, 3% agreement)
  - V_us = 0.223 (Cabibbo angle, PDG: 0.2257 ± 0.0009, 2.9σ)

- **fermion_generations_v16_0.py** - **n_gen = 24/8 = 3** (exact, parameter-free)
- **neutrino_derivations.py** - Type-I seesaw from geometry
- **fermion_derivations.py** - Yukawa hierarchies from G2 curvature
- **neutrino_seesaw_solver.py** - Numerical mass matrix solver

**Key Result:** First topological explanation for exactly 3 generations and CP violation.

### 04_Quantum_Biology (3 files)

Application to quantum effects in biological systems:

- **pneuma_mechanism_v16_0.py** - Microtubule coherence for consciousness
  - Coherence time ~10⁻⁴ s (vs 10⁻¹³ s classical)
  - G2 topology enables quantum biology

- **quantum_bio_derivations.py** - Decoherence suppression theory
- **quantum_decoherence_solver.py** - Lindblad equation solver

**Key Result:** Testable predictions for quantum effects in warm, wet biology.

### 05_Verification (5 files)

Tools for reproducibility and intellectual property protection:

- **discovery_hashes.json** - SHA-256 registry of 10 key predictions with timestamps
  - Tamper-evident record of discovery priority
  - Git snapshot: commit 82bdcd14, 2025-12-29
  - Independent verification protocol

- **wolfram_cloud_audit.py** - Automated Wolfram Cloud verification
- **global_validator.py** - Comprehensive validation suite (experimental data comparison)
- **validation_report.json** - Latest validation results
- **wolfram_validator_v16.py** - Symbolic computation verification

**Key Result:** Cryptographic proof of prediction priority, independent verification.

## Key Predictions & Experimental Status

### Strong Experimental Agreements

| Prediction | PM Value | Experimental | Status |
|------------|----------|--------------|--------|
| θ₁₂ (solar angle) | 33.82° | 33.41° ± 0.75° | 0.5σ |
| θ₁₃ (reactor angle) | 8.61° | 8.58° ± 0.12° | 0.3σ |
| Δm²₂₁ | 7.53 × 10⁻⁵ eV² | 7.53 ± 0.18 × 10⁻⁵ eV² | Exact |
| Δm²₃₁ | 2.453 × 10⁻³ eV² | 2.453 ± 0.033 × 10⁻³ eV² | Exact |
| Jarlskog invariant | 2.9 × 10⁻⁵ | (3.0 ± 0.3) × 10⁻⁵ | 3% |
| Fermion generations | 3 | 3 | Exact |

### Good Agreements

| Prediction | PM Value | Experimental | Status |
|------------|----------|--------------|--------|
| w₀ (dark energy) | -0.846 | -0.827 ± 0.063 (DESI) | 1.3σ |
| S8 (structure) | 0.837 | 0.766-0.832 | Between CMB/WL |

### Awaiting Future Data

- **Proton lifetime:** τ_p ≈ 4.8 × 10³⁴ years (Hyper-Kamiokande, 2027+)
- **Quantum biology:** Coherence times (advanced spectroscopy needed)
- **Shadow sector:** Indirect tests via w₀, H₀ measurements

## Installation & Usage

### Prerequisites

```bash
# Install Python dependencies
pip install numpy scipy sympy

# Optional (for Wolfram integration)
pip install wolframclient
```

### Viewing the Website Locally

The HTML documentation requires a local web server due to browser security (CORS) restrictions. Use one of these methods:

**Method 1: Use the included server (Recommended)**
```bash
# Windows
start_server.bat

# Linux/Mac
python serve.py
```
This will start a local server and automatically open the website in your browser.

**Method 2: Python's built-in server**
```bash
python -m http.server 8000
# Then open: http://localhost:8000/index.html
```

**Note:** Opening index.html directly (double-clicking) will NOT work due to browser security restrictions on loading local JSON files.

### Quick Start

```python
# 1. Understand core foundations
from geometric_anchors_v16_1 import GeometricAnchors

anchors = GeometricAnchors(b3=24)
print(f"Warp factor k_gimel: {anchors.k_gimel:.3f}")
print(f"Flux constraint c_kaf: {anchors.c_kaf:.1f}")

# 2. Run cosmology predictions
from dark_energy_v16_0 import DarkEnergySimulation

de_sim = DarkEnergySimulation()
w0, w_a = de_sim.compute_equation_of_state()
print(f"w0 = {w0:.4f}, w_a = {w_a:.3f}")

# 3. Validate neutrino predictions
from neutrino_mixing_v16_0 import NeutrinoMixingSimulation

nu_sim = NeutrinoMixingSimulation()
angles = nu_sim.compute_mixing_angles()
print(f"θ12 = {angles['theta12']:.2f}°")

# 4. Run full validation suite
from global_validator import GlobalValidator

validator = GlobalValidator()
report = validator.validate_all()
print(f"Validation status: {report['overall_status']}")
```

### Reproducing Discovery Hashes

```python
import json
import hashlib

# Load discovery registry
with open('05_Verification/discovery_hashes.json') as f:
    registry = json.load(f)

# Verify first prediction (w0)
prediction = registry['discoveries'][0]['prediction']
canonical = json.dumps(prediction, sort_keys=True, separators=(',', ':'))
computed_hash = hashlib.sha256(canonical.encode()).hexdigest()

print(f"Expected: {registry['discoveries'][0]['discovery_hash']}")
print(f"Computed: {computed_hash}")
print(f"Match: {computed_hash == registry['discoveries'][0]['discovery_hash']}")
```

## Verification Protocol

To independently verify PM predictions:

1. **Clone repository** at git commit 82bdcd140400506e9378c55c148f88bfe12909ad
2. **Run validation suite:**
   ```bash
   cd 05_Verification
   python global_validator.py
   ```
3. **Verify discovery hashes:**
   ```bash
   python -c "import json, hashlib; ..."  # See code above
   ```
4. **Submit to Wolfram Cloud:**
   ```bash
   python wolfram_cloud_audit.py --all-predictions
   ```

## Scientific Context

### Why G2 Manifolds?

G2 manifolds are 7-dimensional Riemannian manifolds with exceptional holonomy group G2. They provide:

- **Unique topology:** Betti number b₃=24 for TCS (Twisted Connected Sum) construction #187
- **Spinor structure:** Enables fermion description
- **Natural compactification:** 11D M-theory → 4D spacetime
- **Geometric constraints:** Determine all low-energy physics

### Parameter-Free Predictions

Unlike phenomenological models with many free parameters, PM derives:

- 3 fermion generations from 24/8 = 3
- Neutrino angles from geometric seesaw with holonomy phases
- w₀ = -11/13 from dimensional reduction (D_eff = 12.576)
- CP violation from K=4 matching fibres in TCS

This predictive power is testable and falsifiable.

### Comparison to ΛCDM

| Aspect | ΛCDM | PM |
|--------|------|-----|
| Dark energy | w = -1 (cosmological constant) | w₀ = -11/13, w_a ≈ 0.29 |
| Fermion generations | Input (observed = 3) | Derived (b₃/8 = 3) |
| Neutrino mixing | 6+ free parameters | 0 free parameters |
| CP violation | Input (observed J) | Derived (topology) |

PM is **more constrained** and **more predictive** than ΛCDM/SM.

## Citations

### For Code Package

```bibtex
@software{watts2025pm_code,
  author       = {Watts, Andrew Keith},
  title        = {Principia Metaphysica - Computational Physics Package},
  version      = {v16.2},
  date         = {2025-12-29},
  doi          = {TBD},
  url          = {https://github.com/andrewkwatts-maker/PrincipiaMetaphysica},
  note         = {Zenodo archive of computational implementation}
}
```

### For Theory Paper

See `CITATION.cff` in main repository.

### For Specific Predictions

Use discovery hashes from `05_Verification/discovery_hashes.json` with format:

```
PM Prediction [Parameter Name], Discovery Hash: [short_hash],
Predicted: [date], Repository: [github_url], Commit: [git_commit]
```

Example:
```
PM Prediction [w0 = -11/13], Discovery Hash: 918f299f7874ef20,
Predicted: 2025-12-29, Repository: github.com/andrewkwatts-maker/PrincipiaMetaphysica,
Commit: 82bdcd140400506e9378c55c148f88bfe12909ad
```

## License

- **Code:** MIT License (see LICENSE file)
- **Theory content:** See DISCOVERY_PRIORITY.md in main repository for IP terms
- **Discovery hashes:** Public domain (cryptographic verification protocol)

## Contact

**Author:** Andrew Keith Watts
**Email:** AndrewKWatts@gmail.com
**Repository:** https://github.com/andrewkwatts-maker/PrincipiaMetaphysica
**Website:** [TBD]

## Acknowledgments

- NuFit Collaboration for neutrino global fit data (NuFit 6.0, 2024)
- Particle Data Group (PDG 2024)
- DESI Collaboration for BAO and cosmology data (2025)
- Planck Collaboration for CMB data
- Wolfram Research for computational verification infrastructure

## Archive Information

This package was created for permanent archival on Zenodo to ensure:

1. **Long-term preservation** of computational predictions
2. **Citable DOI** for scientific publications
3. **Reproducibility** of all numerical results
4. **Discovery priority** through timestamped hashes
5. **Open science** accessibility for verification

**Recommended for ZIP compression:** Ready for direct upload to Zenodo.

**Total package size:** ~500 KB (uncompressed code + JSON)

**Checksum (SHA-256):** [To be computed after ZIP creation]

---

*Generated: 2025-12-29*
*Package Version: v16.2*
*Theory Version: Principia Metaphysica v16.2*
