# Principia Metaphysica - Visualizations

This directory contains visualization scripts for generating publication-quality diagrams for the Principia Metaphysica framework.

## Physics Framework Transition: (24,2) to (24,1)

**Important**: The PM framework underwent a significant revision between v20 and v22+.

### Legacy Framework (v16-v20)
- **Signature**: (24,2) with two timelike dimensions
- **Mechanism**: Sp(2,R) gauge fixing to select physical time
- **Dimensional reduction**: 26D -> 13D -> 4D via gauge constraints

### Current Framework (v22+)
- **Signature**: (24,1) unified single time
- **Mechanism**: 12 Euclidean bridge pairs (2,0) replacing second time
- **Dimensional reduction**: 25D -> 13D -> 4D via Euclidean bridge compactification
- **Reference**: `docs/appendices/appendix_g_euclidean_bridge.md`

---

## Current v23+ Compatible Visualizations

These visualizations are compatible with the v22+ unified (24,1) framework:

| File | Description | Output |
|------|-------------|--------|
| `descent_chain_v21.py` | Dimensional descent chain visualization | descent-chain.png |
| `microtubule_12pair_v22.py` | 12-pair Euclidean bridge microtubule structure | microtubule-12pair.png |
| `gnosis_progression_v22_2.py` | Gnosis progression diagrams | gnosis-progression.png |
| `particle_diagrams.py` | Standard Model particle representations | particle-*.png |
| `gauge_theory_diagrams.py` | Gauge group structures and breaking | gauge-*.png |
| `theory_overview_diagrams.py` | Theory overview and summary | theory-overview.png |
| `brane_gauge_diagrams.py` | Brane-world gauge structure | brane-gauge-*.png |
| `algebra_diagrams.py` | Algebraic structure visualizations | algebra-*.png |
| `dimension_intro_diagrams.py` | Introductory dimension explanations | dimension-intro.png |
| `goldilocks_plot.py` | Parameter space "Goldilocks zone" | goldilocks.png |
| `octonionic_triality.py` | Octonionic triality structure | octonionic-triality.png |
| `falsifiability_dashboard.py` | Experimental predictions dashboard | falsifiability-dashboard.png |
| `ricci_flow_evolution.py` | Ricci flow evolution visualization | ricci-flow.png |
| `cosmology_diagrams.py` | Cosmological predictions | cosmology-*.png |
| `compactification_diagrams.py` | Compactification schemes | compactification-*.png |
| `brane_diagrams.py` | Brane structure diagrams | brane-*.png |

### v16.2 Specific Visualizations
These use v16.2 parameters but are signature-agnostic:

| File | Description |
|------|-------------|
| `torsion_funnel_v16_2.py` | Torsion funnel visualization |
| `four_pattern_orthogonality_v16_2.py` | Four-pattern orthogonality |
| `entropy_basin_terminal_map_v16_2.py` | Entropy basin mapping |
| `stability_heatmap_v16_2.py` | Parameter stability heatmap |
| `certificate_dashboard_v16_2.py` | Validation certificate dashboard |

---

## Archived v16-v20 Visualizations

**WARNING**: These files use deprecated (24,2) two-time physics or Sp(2,R) gauge fixing.
They are retained for historical reference only. DO NOT use for v23+ publication figures.

| File | Deprecated Feature | Status |
|------|-------------------|--------|
| `two_time_structure.py` | (24,2) signature, Sp(2,R) gauge | ARCHIVED |
| `two_time_comparison.py` | (24,2) vs (24,1) comparison | ARCHIVED |
| `g2_geometry_diagrams.py` | (24,2) signature structure | ARCHIVED |
| `gut_diagrams.py` | Sp(2,R) gauge symmetry diagram | ARCHIVED |
| `observer_time_diagrams.py` | (24,2) two-time observer selection | ARCHIVED |
| `dark_energy_diagrams.py` | (24,2) dimensional cascade | ARCHIVED |
| `time_flow_diagrams.py` | Sp(2,R) thermal time framework | ARCHIVED |

All archived files contain a header block indicating their deprecated status:
```python
# =============================================================================
# HISTORICAL ARCHIVE - v16/v20 Physics
# =============================================================================
```

---

## Usage

To generate visualizations:

```bash
# Generate specific diagram
python simulations/visualizations/<filename>.py

# Example: Generate particle diagrams
python simulations/visualizations/particle_diagrams.py
```

Output images are saved to `images/` directory by default.

## Dependencies

- Python 3.8+
- matplotlib
- numpy
- (optional) scipy for some advanced visualizations

---

## Migration Guide

If updating visualizations from v16-v20 to v23+:

1. **Replace (24,2) references** with (24,1)
2. **Remove Sp(2,R) gauge fixing** - replaced by Euclidean bridge mechanism
3. **Update dimensional cascade**: 26D -> 25D starting point
4. **Reference new appendix**: `appendix_g_euclidean_bridge.md`

For questions about the physics transition, see the main documentation in `docs/`.
