# Scripts Directory

Utility scripts for Principia Metaphysica development and validation.

## Available Scripts

### `validate_config_usage.py`

**Purpose:** Enforce Single Source of Truth principle by detecting hardcoded parameter values that should be imported from `config.py`.

**Usage:**
```bash
# Basic validation
python scripts/validate_config_usage.py

# Verbose output with fix suggestions inline
python scripts/validate_config_usage.py --verbose

# Generate detailed fix suggestions
python scripts/validate_config_usage.py --fix
```

**What it checks:**
- M_GUT hardcoding (should use `GaugeUnificationParameters.M_GUT`)
- M_PLANCK hardcoding (should use `PhenomenologyParameters.M_PLANCK_REDUCED`)
- SHADOW_KUF/SHADOW_CHET hardcoding (should use `SharedDimensionsParameters`)
- THETA_23 hardcoding (should use `NeutrinoParameters.THETA_23`)
- ALPHA_GUT hardcoding (should use `GaugeUnificationParameters.ALPHA_GUT`)

**Exit codes:**
- `0`: All files properly import from config.py
- `1`: Violations found

**Example output:**
```
Files checked: 64
Files with violations: 13
Total violations: 37

By Parameter Type:
  M_GUT: 26 instances
  THETA_23: 3 instances
  ALPHA_GUT: 3 instances
  SHADOW_KUF: 2 instances
  SHADOW_CHET: 2 instances
  M_PLANCK: 1 instances
```

**CI/CD Integration:**
Add to your continuous integration pipeline:
```yaml
- name: Validate config usage
  run: python scripts/validate_config_usage.py
```

## Related Documentation

- **Audit Report:** `reports/SINGLE_SOURCE_TRUTH_AUDIT.md`
- **Config Reference:** `config.py`
- **Usage Guide:** See Section 7 of audit report for best practices

## Development Workflow

1. Make changes to simulation files
2. Run validation: `python scripts/validate_config_usage.py`
3. Fix any violations reported
4. Commit changes

## Contributing

When adding new parameters:
1. Define in appropriate class in `config.py`
2. Import in simulation files using `from config import ClassName`
3. Use `ClassName.PARAMETER_NAME` to access
4. Run validation script to verify

**DO NOT:**
- Hardcode phenomenological parameters (M_GUT, M_Planck, etc.)
- Duplicate parameter definitions across files
- Use magic numbers for critical physics values

**ACCEPTABLE:**
- Geometry-derived constants (intersection numbers, Betti numbers)
- Local computational variables (loop counters, array sizes)
- Temporary exploratory parameters (mark with TODO comment)

---

**Last Updated:** 2025-12-17
