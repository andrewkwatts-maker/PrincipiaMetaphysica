# Parameters Metadata Audit Report

**Generated:** analyze_parameters_metadata.py
**Source:** theory_output.json
**Date:** 2025-12-26

## Executive Summary

- **Total Top-Level Categories:** 11
- **Total Individual Parameters:** 29
- **Top-Level Keys in Parameters:** 12

## Parameter Categories

1. **dark_energy** (1 parameters)
2. **dimensions** (8 parameters)
3. **gauge** (1 parameters)
4. **kk_spectrum** (1 parameters)
5. **mirror_sector** (4 parameters)
6. **neutrino** (9 parameters)
7. **pmns** (1 parameters)
8. **pneuma** (1 parameters)
9. **proton_decay** (1 parameters)
10. **topology** (1 parameters)
11. **xy_bosons** (1 parameters)

## Top-level Keys in Parameters Section

- `dark_energy` (1 parameters)
- `dimensions` (8 parameters)
- `gauge` (1 parameters)
- `kk_spectrum` (1 parameters)
- `mirror_sector` (4 parameters)
- `neutrino` (9 parameters)
- `pmns` (1 parameters)
- `pneuma` (1 parameters)
- `proton_decay` (1 parameters)
- `topology` (1 parameters)
- `version` (metadata)
- `xy_bosons` (1 parameters)

## 1. Parameters with Missing Values

**Count:** 12 / 29

| Parameter Path | Available Keys |
|----------------|----------------|
| `topology` | CHI_EFF, B2, B3, n_flux, HODGE_H11, HODGE_H21... |
| `dark_energy` | w0, wa, d_eff |
| `gauge` | ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE |
| `proton_decay` | tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound |
| `neutrino.mass_spectrum` | m_nu_1, m_nu_2, m_nu_3, sum_m_nu, units, hierarchy |
| `neutrino.validation` | average_deviation_sigma, source_version |
| `neutrino.seesaw` | m_rh_neutrino, units, description |
| `pmns` | theta_12, theta_23, theta_13, delta_CP |
| `kk_spectrum` | m1_TeV, uncertainty_TeV, LHC_BOUND_TEV |
| `pneuma` | VEV |
| `xy_bosons` | M_X, M_Y |
| `mirror_sector.multi_sector` | n_sectors, gravity_dilution |

## 2. Parameters with Missing Units

**Count:** 21 / 29

| Parameter Path | Available Keys |
|----------------|----------------|
| `dimensions.D_BULK` | value |
| `dimensions.D_AFTER_SP2R` | value |
| `dimensions.D_INTERNAL` | value |
| `dimensions.D_EFFECTIVE` | value |
| `dimensions.D_COMMON` | value |
| `dimensions.D_SHARED_EXTRAS` | value |
| `dimensions.SIGNATURE_INITIAL` | value |
| `dimensions.SIGNATURE_BULK` | value |
| `topology` | CHI_EFF, B2, B3, n_flux, HODGE_H11, HODGE_H21... |
| `dark_energy` | w0, wa, d_eff |
| `gauge` | ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE |
| `proton_decay` | tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound |
| `neutrino.validation` | average_deviation_sigma, source_version |
| `pmns` | theta_12, theta_23, theta_13, delta_CP |
| `kk_spectrum` | m1_TeV, uncertainty_TeV, LHC_BOUND_TEV |
| `pneuma` | VEV |
| `xy_bosons` | M_X, M_Y |
| `mirror_sector.temperature_ratio` | value, description, derivation, source |
| `mirror_sector.dm_baryon_ratio` | predicted, observed, observed_uncertainty, deviation_percent, sigma_agreement, status... |
| `mirror_sector.modulation_width` | value, description |
| ... | 1 more |

## 3. Parameters with Missing Descriptions

**Count:** 20 / 29

Note: Accepts 'description' or 'derivation' fields.

| Parameter Path | Available Keys |
|----------------|----------------|
| `dimensions.D_BULK` | value |
| `dimensions.D_AFTER_SP2R` | value |
| `dimensions.D_INTERNAL` | value |
| `dimensions.D_EFFECTIVE` | value |
| `dimensions.D_COMMON` | value |
| `dimensions.D_SHARED_EXTRAS` | value |
| `dimensions.SIGNATURE_INITIAL` | value |
| `dimensions.SIGNATURE_BULK` | value |
| `topology` | CHI_EFF, B2, B3, n_flux, HODGE_H11, HODGE_H21... |
| `dark_energy` | w0, wa, d_eff |
| `gauge` | ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE |
| `proton_decay` | tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound |
| `neutrino.mass_spectrum` | m_nu_1, m_nu_2, m_nu_3, sum_m_nu, units, hierarchy |
| `neutrino.validation` | average_deviation_sigma, source_version |
| `pmns` | theta_12, theta_23, theta_13, delta_CP |
| `kk_spectrum` | m1_TeV, uncertainty_TeV, LHC_BOUND_TEV |
| `pneuma` | VEV |
| `xy_bosons` | M_X, M_Y |
| `mirror_sector.dm_baryon_ratio` | predicted, observed, observed_uncertainty, deviation_percent, sigma_agreement, status... |
| `mirror_sector.multi_sector` | n_sectors, gravity_dilution |

## 4. Parameters with Missing Source/Derivation Info

**Count:** 23 / 29

| Parameter Path | Has Derivation | Available Keys |
|----------------|----------------|----------------|
| `dimensions.D_BULK` | No | value |
| `dimensions.D_AFTER_SP2R` | No | value |
| `dimensions.D_INTERNAL` | No | value |
| `dimensions.D_EFFECTIVE` | No | value |
| `dimensions.D_COMMON` | No | value |
| `dimensions.D_SHARED_EXTRAS` | No | value |
| `dimensions.SIGNATURE_INITIAL` | No | value |
| `dimensions.SIGNATURE_BULK` | No | value |
| `topology` | No | CHI_EFF, B2, B3, n_flux, HODGE_H11, HODGE_H21... |
| `dark_energy` | No | w0, wa, d_eff |
| `gauge` | No | ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE |
| `proton_decay` | No | tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound |
| `neutrino.mass_splittings.delta_m21_sq` | No | value, units, description, status |
| `neutrino.mass_splittings.delta_m31_sq` | No | value, units, description, status |
| `neutrino.mass_spectrum` | No | m_nu_1, m_nu_2, m_nu_3, sum_m_nu, units, hierarchy |
| `neutrino.validation` | No | average_deviation_sigma, source_version |
| `neutrino.seesaw` | No | m_rh_neutrino, units, description |
| `pmns` | No | theta_12, theta_23, theta_13, delta_CP |
| `kk_spectrum` | No | m1_TeV, uncertainty_TeV, LHC_BOUND_TEV |
| `pneuma` | No | VEV |
| ... | ... | 3 more |

## 5. Parameters with Missing Status

**Count:** 22 / 29

Expected status values: INPUT, DERIVED, GEOMETRIC

| Parameter Path | Available Keys |
|----------------|----------------|
| `dimensions.D_BULK` | value |
| `dimensions.D_AFTER_SP2R` | value |
| `dimensions.D_INTERNAL` | value |
| `dimensions.D_EFFECTIVE` | value |
| `dimensions.D_COMMON` | value |
| `dimensions.D_SHARED_EXTRAS` | value |
| `dimensions.SIGNATURE_INITIAL` | value |
| `dimensions.SIGNATURE_BULK` | value |
| `topology` | CHI_EFF, B2, B3, n_flux, HODGE_H11, HODGE_H21... |
| `dark_energy` | w0, wa, d_eff |
| `gauge` | ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE |
| `proton_decay` | tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound |
| `neutrino.mass_spectrum` | m_nu_1, m_nu_2, m_nu_3, sum_m_nu, units, hierarchy |
| `neutrino.validation` | average_deviation_sigma, source_version |
| `neutrino.seesaw` | m_rh_neutrino, units, description |
| `pmns` | theta_12, theta_23, theta_13, delta_CP |
| `kk_spectrum` | m1_TeV, uncertainty_TeV, LHC_BOUND_TEV |
| `pneuma` | VEV |
| `xy_bosons` | M_X, M_Y |
| `mirror_sector.temperature_ratio` | value, description, derivation, source |
| ... | ... | 2 more |

## 6. Parameters with Missing Uncertainty

**Count:** 25 / 29

Note: Accepts 'uncertainty', 'sigma', 'predicted_error', or 'experimental_error'.

| Parameter Path | Status | Available Keys |
|----------------|--------|----------------|
| `dimensions.D_BULK` | N/A | value |
| `dimensions.D_AFTER_SP2R` | N/A | value |
| `dimensions.D_INTERNAL` | N/A | value |
| `dimensions.D_EFFECTIVE` | N/A | value |
| `dimensions.D_COMMON` | N/A | value |
| `dimensions.D_SHARED_EXTRAS` | N/A | value |
| `dimensions.SIGNATURE_INITIAL` | N/A | value |
| `dimensions.SIGNATURE_BULK` | N/A | value |
| `topology` | N/A | CHI_EFF, B2, B3, n_flux, HODGE_H11, HODGE_H21... |
| `dark_energy` | N/A | w0, wa, d_eff |
| `gauge` | N/A | ALPHA_GUT, ALPHA_GUT_INV, M_GUT, WEAK_MIXING_ANGLE |
| `proton_decay` | N/A | tau_p_years, SUPER_K_BOUND, BR_epi0, ratio_to_bound |
| `neutrino.mass_splittings.delta_m21_sq` | INPUT | value, units, description, status |
| `neutrino.mass_splittings.delta_m31_sq` | INPUT | value, units, description, status |
| `neutrino.mass_spectrum` | N/A | m_nu_1, m_nu_2, m_nu_3, sum_m_nu, units, hierarchy |
| `neutrino.validation` | N/A | average_deviation_sigma, source_version |
| `neutrino.seesaw` | N/A | m_rh_neutrino, units, description |
| `pmns` | N/A | theta_12, theta_23, theta_13, delta_CP |
| `kk_spectrum` | N/A | m1_TeV, uncertainty_TeV, LHC_BOUND_TEV |
| `pneuma` | N/A | VEV |
| ... | ... | 5 more |

## Metadata Completeness by Category

| Category | Parameters | Missing Units | Missing Desc | Missing Source | Missing Status | Missing Uncertainty |
|----------|------------|---------------|--------------|----------------|----------------|---------------------|
| dark_energy | 1 | 1 | 1 | 1 | 1 | 1 |
| dimensions | 8 | 8 | 8 | 8 | 8 | 8 |
| gauge | 1 | 1 | 1 | 1 | 1 | 1 |
| kk_spectrum | 1 | 1 | 1 | 1 | 1 | 1 |
| mirror_sector | 4 | 4 | 2 | 2 | 3 | 4 |
| neutrino | 9 | 1 | 2 | 5 | 3 | 5 |
| pmns | 1 | 1 | 1 | 1 | 1 | 1 |
| pneuma | 1 | 1 | 1 | 1 | 1 | 1 |
| proton_decay | 1 | 1 | 1 | 1 | 1 | 1 |
| topology | 1 | 1 | 1 | 1 | 1 | 1 |
| xy_bosons | 1 | 1 | 1 | 1 | 1 | 1 |

## Overall Completeness Metrics

- **Values present:** 58.6% (17/29)
- **Units present:** 27.6% (8/29)
- **Descriptions present:** 31.0% (9/29)
- **Source info present:** 20.7% (6/29)
- **Status present:** 24.1% (7/29)
- **Uncertainty present:** 13.8% (4/29)

## Recommendations

### High Priority

1. **Add source** to 23 parameters (79.3% of total)
   - Should specify: experimental reference or theoretical basis
   - Critical for understanding data flow and provenance

2. **Add status** to 22 parameters (75.9% of total)
   - Should specify: INPUT, DERIVED, or GEOMETRIC
   - Critical for understanding data flow and provenance

3. **Add description/derivation** to 20 parameters (69.0% of total)
   - Should specify: physical meaning
   - Critical for understanding data flow and provenance

### Medium Priority

1. **Add units** to 21 parameters (72.4% of total)
   - Use SI or natural units (GeV, eV^2, degrees, dimensionless, etc.)

2. **Add uncertainty** to 25 parameters (86.2% of total)
   - Express as experimental error, predicted error, sigma, or uncertainty

### Standard Metadata Schema

Recommended fields for each parameter:
```json
{
  "value": <number or array>,          // or "predicted", "experimental", "observed"
  "units": "GeV" | "degrees" | ...,    // Physical units
  "description": "...",                 // Physical meaning (or "derivation")
  "status": "INPUT|DERIVED|GEOMETRIC", // Origin type
  "source": "...",                      // Experimental ref or calculation method
  "uncertainty": <number>,              // or "sigma", "predicted_error", etc.
}
```

## Examples of Well-Documented Parameters

Found 4 parameters with complete metadata (13.8%):

- `neutrino.pmns_angles.theta_12`
- `neutrino.pmns_angles.theta_23`
- `neutrino.pmns_angles.theta_13`
- `neutrino.pmns_angles.delta_cp`

## Sample Parameter Details

### `neutrino.pmns_angles.theta_12`

```json
{
  "predicted": 33.59,
  "predicted_error": 1.18,
  "experimental": 33.41,
  "experimental_error": 0.75,
  "units": "degrees",
  "derivation": "From tri-bimaximal + G\u2082 perturbation",
  "source": "NuFIT 6.0 (2024)",
  "status": "DERIVED"
}
```

**Metadata Present:**
- ✓ value
- ✓ units
- ✓ description
- ✓ source
- ✓ status
- ✓ uncertainty
