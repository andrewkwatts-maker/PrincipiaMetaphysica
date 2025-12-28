# Deprecated Simulation Files

## Overview

This directory contains **legacy simulation files from versions 12.x through 15.x** that have been superseded by the v16 simulation framework. These files are preserved for historical reference and reproducibility purposes only.

## Important Notes

### DO NOT USE FOR PRODUCTION

- These simulation files are **deprecated** and should not be used for new analysis or production calculations
- They may contain outdated assumptions, incomplete implementations, or bugs that have been fixed in v16
- The v16 framework provides improved accuracy, better error handling, and more comprehensive physical models

### Superseded by v16

All functionality in these deprecated files has been reimplemented, refined, and enhanced in the v16 simulation framework located at:
- `h:\Github\PrincipiaMetaphysica\simulations\v16\`

The v16 framework includes:
- **Unified architecture**: Consistent interfaces across all simulation modules
- **Enhanced numerical methods**: Improved convergence and stability
- **Comprehensive validation**: Extensive test coverage and physical consistency checks
- **Modern foundations**: Built on the latest Foundation schema and Constants system
- **Better documentation**: Clear API documentation and usage examples

### Purpose of This Archive

These files are preserved for:
1. **Reproducibility**: Ability to reproduce historical results and calculations from earlier research phases
2. **Reference**: Understanding the evolution of the theoretical framework and computational methods
3. **Comparison**: Benchmarking v16 improvements against previous implementations
4. **Archival**: Complete historical record of the project's development

### Migration to v16

If you need functionality from any deprecated simulation:

1. **Check v16 first**: The feature likely exists in improved form in `simulations/v16/`
2. **Consult documentation**: See `simulations/v16/*/README.md` files for migration guides
3. **Review DEPRECATED_FILES.md**: Understand which v16 module replaces each deprecated file
4. **Do not import**: Never import from deprecated files in new code

## Directory Structure

The deprecated files are organized to mirror their original structure in `simulations/core/`:

```
deprecated/
└── core/
    ├── cosmology/       # Cosmological simulation files (v12-v15)
    ├── fermion/         # Fermion generation and chirality simulations (v13-v14)
    ├── gauge/           # Gauge unification and symmetry breaking (v12-v14)
    ├── geometric/       # G2 geometry and torsion calculations (v12-v15)
    ├── higgs/           # Higgs mass and Yukawa coupling simulations (v12-v14)
    ├── misc/            # Miscellaneous calculations and utilities (v12-v14)
    ├── moduli/          # Moduli stabilization simulations (v12-v15)
    ├── neutrino/        # Neutrino mass and mixing simulations (v12-v14)
    ├── pneuma/          # Pneuma field mechanism simulations (v12-v15)
    ├── proton/          # Proton decay calculations (v12-v13)
    └── quantum_bio/     # Quantum biology threshold simulations (v15)
```

## Version History

- **v12.x**: Initial comprehensive simulation framework with G2 geometry integration
- **v13.x**: Enhanced geometric validations and moduli stabilization
- **v14.x**: Advanced gauge unification and topological phase calculations
- **v15.x**: Quantum biology extensions and final pre-v16 refinements
- **v16.0+**: Complete framework redesign with Foundation schema integration (CURRENT)

## For Developers

### Do Not Modify

Files in this directory should be considered **read-only**. Any bug fixes or improvements should be:
1. Implemented in the v16 framework
2. Documented in v16 release notes
3. Cross-referenced but not backported

### Import Warnings

If you accidentally import from deprecated modules, you may encounter:
- Missing dependencies (older Constants or Foundation versions)
- API incompatibilities with v16 code
- Inconsistent results compared to v16 calculations

Always use:
```python
from simulations.v16.geometric import g2_geometry_v16_0  # CORRECT
```

Not:
```python
from simulations.deprecated.core.geometric import g2_torsion_m_gut_v12_4  # WRONG
```

## Questions or Issues

If you believe you need to reference deprecated code:
1. Document your reason in detail
2. Verify the functionality doesn't exist in v16
3. Consult the project maintainer
4. Consider whether the v16 implementation is actually more appropriate

## See Also

- **DEPRECATED_FILES.md**: Complete inventory of all deprecated files with original paths
- **simulations/v16/**: Current production simulation framework
- **SYSTEM_ARCHITECTURE.md**: Overview of the v16 simulation architecture
- **FOUNDATION_SCHEMA_README.md**: Foundation schema documentation used by v16
