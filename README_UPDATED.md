copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this material, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com

# Principia Metaphysica
Philosophiæ Metaphysicæ Principia Mathematica

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18079602.svg)](https://doi.org/10.5281/zenodo.18079602)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v16.2-blue.svg)](https://github.com/andrewkwatts/PrincipiaMetaphysica/releases)

## Abstract

This paper presents Principia Metaphysica, a theoretical framework unifying gravity, gauge forces, and the origin of time through higher-dimensional geometry. The framework begins with 26-dimensional spacetime with signature (24,2)—24 spatial dimensions and 2 timelike dimensions. An Sp(2,R) gauge symmetry removes unphysical ghost states, projecting to an effective 13-dimensional shadow manifold with signature (12,1). This 13D space then compactifies on a 7-dimensional G₂ manifold, yielding a 6-dimensional bulk with signature (5,1).

The framework features four branes: one 6D observable universe (5,1) and three 4D shadow universes (3,1), all sharing a common 4D spacetime base. The topology of the flux-dressed G₂ manifold yields an effective Euler characteristic χ_eff = 144, which through the relation n_gen = χ_eff/48 predicts exactly 3 fermion generations. The fundamental field is an 8192-component spinor in 26D (Clifford algebra Cl(24,2)), which gauge-reduces to 64 effective components in the 13D shadow.

Time emerges from thermal entropy via the Two-Time Thermal Hypothesis: observable thermal time couples to an orthogonal hidden time dimension. The framework predicts dark energy equation of state w₀ = -11/13 ≈ -0.846 and w_a ≈ -0.75, matching DESI 2024 observations within 1σ. SO(10) grand unification emerges naturally from the G₂ compactification. Shared extra dimensions produce Kaluza-Klein graviton resonances at approximately 5 TeV, testable at the High-Luminosity LHC.

Six critical mathematical issues have been resolved: (1) Generation count correctly derived from flux-dressed topology rather than bare Euler characteristic; (2) Dark energy attractor to w = -1.0 at late times via Mashiach minimum; (3) Spinor dimensions validated via Clifford algebra; (4) Dimensional reduction pathway clarified (gauge projection followed by compactification); (5) Previously undefined parameters now derived from geometry; (6) Gauge coupling unification achieved with 3% precision. Framework validation shows 51 of 58 parameters (88%) passing consistency checks, with 10 of 14 predictions within experimental error bars.

---

## Quick Start

### Making Parameter Changes

**All parameter values live in ONE place:** `config.py`

```bash
# 1. Edit config.py (change any parameter value)
# 2. Update JavaScript for HTML webpages
python generate_js_constants.py

# 3. (Optional) Update analysis CSV
python SimulateTheory.py
```

That's it! Your HTML webpages automatically use the new values.

### Project Structure

```
config.py                      ← EDIT THIS (single source of truth)
    ↓
generate_js_constants.py       ← RUN THIS (auto-generates JavaScript)
    ↓
js/theory-constants.js         ← AUTO-GENERATED (don't edit!)
    ↓
HTML webpages                  ← AUTO-UPDATED (load the JS)
```

**Documentation:**
- [ARCHITECTURE.md](ARCHITECTURE.md) - How files relate to each other
- [CONFIG_README.md](CONFIG_README.md) - All about config.py
- [SimulateTheory_README.md](SimulateTheory_README.md) - Calculation engine details

---

## Citation

### Zenodo Archive

This work is archived on Zenodo with DOI: [10.5281/zenodo.18079602](https://doi.org/10.5281/zenodo.18079602)

### BibTeX

```bibtex
@article{watts2025principia,
  title={Principia Metaphysica: A Unified Theory of Gravity, Gauge Forces, and Time},
  author={Watts, Andrew Keith},
  year={2025},
  version={v16.2},
  doi={10.5281/zenodo.18079602},
  url={https://doi.org/10.5281/zenodo.18079602},
  publisher={Zenodo}
}
```

### APA Style

```
Watts, A. K. (2025). Principia Metaphysica: A Unified Theory of Gravity,
Gauge Forces, and Time (Version v16.2). Zenodo.
https://doi.org/10.5281/zenodo.18079602
```

### Chicago Style

```
Watts, Andrew Keith. 2025. "Principia Metaphysica: A Unified Theory of
Gravity, Gauge Forces, and Time." Version v16.2. Zenodo.
https://doi.org/10.5281/zenodo.18079602.
```

### Plain Text

```
Watts, A. K. (2025). Principia Metaphysica: A Unified Theory of Gravity,
Gauge Forces, and Time (v16.2). Zenodo. DOI: 10.5281/zenodo.18079602
```

---

## Known Open Problems

The framework has several unresolved theoretical challenges documented in [sections/conclusion.html](sections/conclusion.html):

1. **Asymptotic Safety Extent**: If UV fixed points exist in GUT sector (not just gravity), operator enhancement could affect proton decay predictions. Current assumption: AS confined to gravity sector only.

2. **LQG Time Scale**: Connection between t_ortho ~ 10^-18 s and Loop Quantum Gravity's t_Planck ~ 10^-44 s unclear (26 orders of magnitude difference). May represent complementary regimes.

3. **Landscape Size**: Predicted vacua (~10^(10^8)) vastly exceed anthropic bound (~10^120), requiring dynamical selection mechanism beyond anthropic reasoning.

4. **Mirror DM Quantification**: Z_2 dark matter candidate from two-time structure needs quantitative predictions: relic abundance, direct detection cross-sections, self-interaction constraints.

5. **Gauge-Higgs Calculation**: Higgs potential from Wilson line breaking requires explicit geometric derivation including quantum corrections.

See the [full paper](principia-metaphysica-paper.html) for detailed analysis of the framework and validation results.

---

## Links

- **Interactive Paper:** [https://principiametaphysica.com](https://principiametaphysica.com)
- **GitHub Repository:** [https://github.com/andrewkwatts/PrincipiaMetaphysica](https://github.com/andrewkwatts/PrincipiaMetaphysica)
- **Zenodo Archive:** [https://doi.org/10.5281/zenodo.18079602](https://doi.org/10.5281/zenodo.18079602)

## Contact

For inquiries, please contact: AndrewKWatts@Gmail.com
