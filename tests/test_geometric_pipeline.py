"""
Unit Tests for End-to-End Geometric Pipeline
================================================
Tests the complete derivation chain from E8 → Leech → G2 → Bridges → Physics.
Validates that all stages produce consistent, correct results.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))

from simulations.PM.validation.geometric_pipeline import GeometricPipeline


@pytest.fixture(scope="module")
def pipeline():
    """Run the pipeline once for all tests."""
    p = GeometricPipeline()
    p.run()
    return p


# ------------------------------------------------------------------
# Pipeline execution
# ------------------------------------------------------------------

class TestPipelineExecution:
    """Tests that the pipeline runs end-to-end."""

    def test_pipeline_runs_without_error(self, pipeline):
        assert pipeline._results is not None

    def test_all_stages_present(self, pipeline):
        r = pipeline._results
        for key in ['e8', 'leech', 'lattice_connections', 'g2', 'packing', 'spectral', 'bridges', 'observables']:
            assert key in r, f"Missing pipeline stage: {key}"

    def test_pipeline_valid(self, pipeline):
        assert pipeline._results['pipeline_valid']


# ------------------------------------------------------------------
# E8 stage
# ------------------------------------------------------------------

class TestE8Stage:
    def test_roots_240(self, pipeline):
        assert pipeline._results['e8']['num_roots'] == 240

    def test_dimension_248(self, pipeline):
        assert pipeline._results['e8']['dimension'] == 248

    def test_cartan_det_1(self, pipeline):
        assert pipeline._results['e8']['cartan_det'] == 1

    def test_e8_valid(self, pipeline):
        assert pipeline._results['e8']['all_valid']


# ------------------------------------------------------------------
# Leech stage
# ------------------------------------------------------------------

class TestLeechStage:
    def test_dimension_24(self, pipeline):
        assert pipeline._results['leech']['dimension'] == 24

    def test_kissing_196560(self, pipeline):
        assert pipeline._results['leech']['kissing_number'] == 196_560

    def test_n_gen_3(self, pipeline):
        assert pipeline._results['leech']['n_gen'] == 3

    def test_golay_valid(self, pipeline):
        assert pipeline._results['leech']['golay_valid']


# ------------------------------------------------------------------
# G2 stage
# ------------------------------------------------------------------

class TestG2Stage:
    def test_torsion_free(self, pipeline):
        assert pipeline._results['g2']['torsion_free']

    def test_ricci_flat(self, pipeline):
        assert pipeline._results['g2']['ricci_flat']

    def test_hodge_involution(self, pipeline):
        assert pipeline._results['g2']['hodge_involution']

    def test_lambda2_decomposition(self, pipeline):
        assert pipeline._results['g2']['lambda2_14_plus_7']


# ------------------------------------------------------------------
# Bridges stage
# ------------------------------------------------------------------

class TestBridgesStage:
    def test_12_bridges(self, pipeline):
        assert pipeline._results['bridges']['num_bridges'] == 12

    def test_27d(self, pipeline):
        assert pipeline._results['bridges']['total_dim'] == 27

    def test_signature_26_1(self, pipeline):
        assert pipeline._results['bridges']['signature'] == (26, 1)


# ------------------------------------------------------------------
# Physical observables
# ------------------------------------------------------------------

class TestObservables:
    def test_n_gen_3(self, pipeline):
        assert pipeline._results['observables']['n_gen'] == 3

    def test_alpha_inv_within_20pct(self, pipeline):
        """Geometric α⁻¹ within 20% of 137.036."""
        alpha = pipeline._results['observables']['alpha_inv_geometric']
        error = abs(alpha - 137.036) / 137.036
        assert error < 0.20, f"α⁻¹ = {alpha:.3f}, error = {error*100:.1f}%"

    def test_w0_value(self, pipeline):
        """w₀ = -23/24 ≈ -0.9583."""
        w0 = pipeline._results['observables']['w0']
        assert np.isclose(w0, -23.0 / 24.0)

    def test_chi_eff_144(self, pipeline):
        assert pipeline._results['observables']['chi_eff'] == 144


# ------------------------------------------------------------------
# Monte Carlo stability
# ------------------------------------------------------------------

class TestMonteCarlo:
    def test_n_gen_stable(self, pipeline):
        mc = pipeline.monte_carlo_moduli(num_samples=30, sigma=0.05)
        assert mc['n_gen_stable']

    def test_signature_stable(self, pipeline):
        mc = pipeline.monte_carlo_moduli(num_samples=30, sigma=0.05)
        assert mc['signature_stable']

    def test_kk_mass_reasonable_cv(self, pipeline):
        """KK mass coefficient of variation < 50%."""
        mc = pipeline.monte_carlo_moduli(num_samples=30, sigma=0.05)
        assert mc['kk_mass_cv'] < 0.50


# ------------------------------------------------------------------
# Sensitivity analysis
# ------------------------------------------------------------------

class TestSensitivity:
    def test_jacobian_shape(self, pipeline):
        J = pipeline.sensitivity_jacobian()
        assert J['jacobian_shape'] == (12, 3)

    def test_well_conditioned(self, pipeline):
        J = pipeline.sensitivity_jacobian()
        assert J['well_conditioned']


# ------------------------------------------------------------------
# Full verification
# ------------------------------------------------------------------

class TestFullVerification:
    def test_all_checks_pass(self):
        p = GeometricPipeline()
        checks = p.verify()
        for key, val in checks.items():
            assert val, f"End-to-end verification failed: {key}"
