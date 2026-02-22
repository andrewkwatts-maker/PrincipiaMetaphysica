# Gemini Debate: Sterile Neutrino Portals

**Date:** 2026-02-01T10:12:46.077293
**Priority:** HIGH
**Targets:** simulations/PM/particle/neutrino_mixing.py, simulations/PM/particle/g2_triality_mixing.py, simulations/PM/field_dynamics/orch_or_bridge.py

---

**VERDICT:** MODIFY
**CONFIDENCE:** HIGH
**SCIENTIFIC_SCORE:** 8

**STRENGTHS:**
- Provides a detailed geometric derivation of sterile neutrino portals, linking them to G2 manifold topology and shadow sectors.
- Offers specific formulas for sterile neutrino mass, mixing angle, and portal Lagrangian term.
- Connects the sterile neutrino parameters to hidden-face moduli, providing a potential mass scale prediction (TeV-PeV).
- Suggests experimental observables and detection implications, including LHC monojet searches, DUNE/IceCube/KM3NeT oscillation experiments, and cosmological impact on Delta_N_eff.
- The use of `alpha_leak` from previous sections provides a consistent dark sector coupling.

**WEAKNESSES:**
- The derivation of `n_sterile_eff` relies on an `alpha_leak^(f)` factor, which, while motivated by previous sections, needs more rigorous justification within the G2 framework. It risks being a repackaged fudge factor.
- The mass scale `M_s ~ M_Pl e^{-T_i^(f)/2} ~ 10^2 - 10^4 GeV` is a broad estimate and requires more precise determination from the hidden-face moduli vevs.
- The connection to short-baseline anomalies (MiniBooNE) should be presented cautiously, as these anomalies are still debated within the neutrino physics community.
- The cosmological impact (Delta_N_eff) needs to be checked for consistency with current CMB constraints.

**RECOMMENDATION:**
Adopt the proposal with modifications to strengthen the justification for `alpha_leak` and provide a more precise determination of the sterile neutrino mass scale. Also, temper the claims about short-baseline anomalies and ensure consistency with cosmological constraints.

**SPECIFIC_ACTIONS:**
- **MODIFY:**
    - **Action 1:** Add a subsection that rigorously derives or justifies the `alpha_leak^(f)` factor within the G2 manifold context. Explain the geometric origin of this leakage and its relationship to the bridge flux.
    - **Action 2:** Refine the mass scale prediction for `M_s` by providing a more detailed calculation based on the hidden-face moduli vevs. Include specific values for the moduli `T_i^(f)` and their uncertainties.
    - **Action 3:** Add a disclaimer regarding the short-baseline anomalies, acknowledging the ongoing debate and emphasizing that the sterile neutrino portal provides a potential, but not definitive, explanation.
    - **Action 4:** Verify that the predicted Delta_N_eff value is consistent with current CMB constraints from Planck and other experiments. Adjust the parameters if necessary to ensure consistency.
    - **Action 5:** Add new formulas to the FormulasRegistry for m_nu^eff, sin^2(2*theta), and Delta_N_eff.
    - **Action 6:** Add new parameters to the parameters.json file for y_as and M_s.
