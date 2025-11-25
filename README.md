copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this material, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com

# PrincipiaMetaphysica
Philosophiæ Metaphysicæ Principia Mathematica

This report presents a rigorous formulation of the Principia Metaphysica framework,
positing a (12,1) dimensional bulk spacetime where the single time dimension is an
emergent thermodynamic phenomenon. We introduce the Thermal Time Hypothesis
(TTH), linking the flow of time to the entropy gradient of a fundamental fermionic
"Pneuma" consciousness field. The framework is constructed as a non-renormalizable
Effective Field Theory (EFT), with the observable (3,1) universe realized as a brane
embedded in the 13D bulk. Through Kaluza-Klein compactification of the nine extra
spatial dimensions, we derive an effective 4D Myrzakulov-type F(R,T) gravity. A
dynamical systems analysis of this theory reveals a late-time cosmological attractor,
driven by a scalar modulus (the "Mashiach" field), which naturally explains the
observed cosmic acceleration. The model's mathematical consistency is established
through the constraints of Clifford algebra representations for fermions in 13D, gauge
anomaly cancellation, and holographic principles enforced by the Quantum Focusing
Conjecture (QFC). Crucially, the theory yields falsifiable predictions in the form of
specific Lorentz-violating operators within the Standard-Model Extension (SME),
leading to a modified dispersion relation for gravitational waves testable by current
and future observatories.

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
- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) - Complete automation workflow guide
- [CONFIG_README.md](CONFIG_README.md) - All about config.py
- [SimulateTheory_README.md](SimulateTheory_README.md) - Calculation engine details

---
