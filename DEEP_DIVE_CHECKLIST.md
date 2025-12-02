# IMPLEMENTATION CHECKLIST FOR PM v7.0

## Phase 1: Config Updates (Priority: HIGH)
- [ ] Add DESI DR2 extended parameters to config.py
- [ ] Add KKSpectrumParameters class to config.py
- [ ] Update proton decay comments
- [ ] Add Planck tension parameters
- [ ] Verify config validation still passes

## Phase 2: Simulation Updates
- [ ] Verify proton_decay_rg_hybrid.py outputs 0.02 OOM
- [ ] Check pmns_full_matrix.py formula corrections
- [ ] Update wz_evolution_desi_dr2.py with Planck tension calc
- [ ] CREATE kk_spectrum_collider.py module
- [ ] Update run_all_simulations.py to include KK spectrum
- [ ] Run full simulation suite and verify output

## Phase 3: Paper Updates
- [ ] Update abstract with refined numbers
- [ ] Section 4 (Cosmology): DESI DR2 + log w(z)
- [ ] Section 5 (Gauge): M_GUT derivation details
- [ ] Section 6 (Fermions): Full PMNS matrix table
- [ ] Section 7 (Predictions): Add KK spectrum subsection
- [ ] Section 9: Convert to "Resolution Status"

## Phase 4: Website Section Updates (Deploy 5 Agents)
- [ ] Agent 1: sections/cosmology.html
- [ ] Agent 2: sections/gauge-unification.html
- [ ] Agent 3: sections/fermion-sector.html
- [ ] Agent 4: sections/predictions.html
- [ ] Agent 5: sections/geometric-framework.html

## Phase 5: Foundation Pages (4 Updates)
- [ ] foundations/g2-manifolds.html - TCS construction
- [ ] foundations/yang-mills.html - 3-loop RG
- [ ] foundations/so10-gut.html - refined M_GUT
- [ ] foundations/kaluza-klein.html - 5 TeV spectrum

## Phase 6: Formula Centralization
- [ ] Scan all HTML for magic numbers (run_magic_finder.py)
- [ ] Replace high-priority formulas with PM.* refs
- [ ] Test all pages load correctly with JS constants
- [ ] Verify no calculation errors

## Phase 7: New Content
- [ ] CREATE sections/outstanding-issues.html
- [ ] Add progress tracker with 9 issues
- [ ] Update beginners-guide.html with v7.0 changes
- [ ] Add "What's New in v7.0?" section to index.html

## Phase 8: Testing & Validation
- [ ] Run build.bat (full pipeline)
- [ ] Verify theory_output.json completeness
- [ ] Check theory-constants.js has 150+ constants
- [ ] Test website: all pages load, formulas display
- [ ] Run config.py validation (all checks pass)
- [ ] Verify grade improvements (B+ -> A-)

## Phase 9: Documentation
- [ ] Update README with v7.0 changes
- [ ] Commit DEEP_DIVE_IMPLEMENTATION_PLAN.md
- [ ] Commit DEEP_DIVE_UPDATE_SUMMARY.json
- [ ] Create v7.0 release notes

## Phase 10: Release
- [ ] Git commit with comprehensive message
- [ ] Git push to repository
- [ ] Update website live version
- [ ] Announce v7.0 release

---

Target completion: 7-12 days
Resources: Solo + 5 parallel agents for website
Expected outcome: Theory grade A-, 95% validated, <1σ tensions
