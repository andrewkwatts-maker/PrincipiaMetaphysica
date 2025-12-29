# Principia Metaphysica v16.2 - Zenodo Archive

**DOI:** 10.5281/zenodo.18079602
**Date:** 2025-12-29
**Author:** Andrew Keith Watts

## Overview

This archive contains the complete computational framework and data for Principia Metaphysica version v16.2, a theoretical framework unifying gravity, gauge forces, and the origin of time through higher-dimensional geometry.

## Contents

### Data Files (`data/`)
- `theory_output.json` - Complete theory calculations and predictions
- `formulas.json` - All 109 formulas with full metadata
- `parameters.json` - All 58 parameters with values and uncertainties
- `sections.json` - Complete paper content in structured format
- `metadata.json` - Theory metadata and statistics

### Code (`code/`)
- `config.py` - Master configuration file (single source of truth)

### Documentation (`docs/`)
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture
- `FORMAL_ABSTRACT.md` - Formal technical abstract

### Web Interface (`web/`)
- HTML files for interactive paper viewing
- JavaScript renderers for formulas and sections
- CSS styling files

### Metadata (`metadata/`)
- `FILE_MANIFEST.json` - Complete file listing with checksums
- `CHECKSUMS.txt` - SHA-256 checksums for verification
- `zenodo_metadata.json` - Zenodo upload metadata

## Key Features

- **109 Mathematical Formulas** - Fully documented with derivations
- **58 Parameters** - Including 14 testable predictions
- **88% Validation Rate** - 51 of 58 parameters pass consistency checks
- **10 of 14 Predictions** - Within experimental error bars

## Quick Start

1. Extract the archive
2. Open `web/index.html` in a browser for the interactive paper
3. View `data/theory_output.json` for complete calculations
4. Read `docs/README.md` for detailed documentation

## Verification

Verify file integrity using checksums:
```bash
sha256sum -c metadata/CHECKSUMS.txt
```

## Citation

```
Watts, A. K. (2025). Principia Metaphysica: A Unified Theory of Gravity,
Gauge Forces, and Time (Version v16.2). Zenodo. 10.5281/zenodo.18079602
```

Or use `CITATION.cff` for automated citation tools.

## License

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
See LICENSE file for details.

## Links

- **Website:** https://principiametaphysica.com
- **GitHub:** https://github.com/andrewkwatts/PrincipiaMetaphysica
- **DOI:** 10.5281/zenodo.18079602

## Contact

For inquiries: AndrewKWatts@Gmail.com
