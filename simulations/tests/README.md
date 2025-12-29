# Principia Metaphysica Test Suite

Comprehensive unit and integration tests for the PM simulation framework.

## Overview

This test suite provides comprehensive coverage for:
- **PMRegistry**: Central parameter registry with provenance tracking
- **ExperimentalDataLoader**: Loading experimental data from DESI, NuFIT, and PDG

## Test Files

### `test_registry.py`
Comprehensive tests for the PMRegistry singleton:

**Coverage Areas:**
1. **Singleton Pattern** (4 tests)
   - Instance uniqueness and persistence
   - Reset functionality

2. **Parameter Management** (8 tests)
   - Get/set parameters with full metadata
   - Provenance tracking
   - Entry retrieval

3. **Status Categories** (4 tests)
   - ESTABLISHED, GEOMETRIC, DERIVED, PREDICTED, CALIBRATED
   - Protection against overwriting ESTABLISHED params

4. **Uncertainty Propagation** (3 tests)
   - Storing and retrieving uncertainties
   - Export functionality

5. **Sigma Deviation Computation** (7 tests)
   - EXCELLENT (< 1σ)
   - GOOD (1-2σ)
   - ACCEPTABLE (2-3σ)
   - TENSION (> 3σ)
   - Edge cases (missing data, no uncertainty)

6. **Prediction Validation** (3 tests)
   - Metadata storage
   - Custom metadata keys
   - Error handling

7. **Accuracy Reports** (2 tests)
   - Categorization by sigma level
   - Filtering by status type

8. **Mismatch Detection** (4 tests)
   - Warning on significant changes
   - Logging mismatches
   - Tolerance handling

9. **Export Methods** (3 tests)
   - Parameter export
   - Provenance export
   - Timestamp validation

10. **Experimental Data Integration** (4 tests)
    - DESI, NuFIT, PDG loading patterns
    - Complete validation workflow

11. **Edge Cases** (9 tests)
    - Empty registry
    - Zero/negative values
    - Very large/small numbers
    - Complex metadata

12. **Parametrized Tests** (11 tests)
    - Sigma boundary testing
    - Status type validation

**Total: 62+ test cases**

### `test_data_loader.py`
Comprehensive tests for ExperimentalDataLoader:

**Coverage Areas:**
1. **Loader Instantiation** (4 tests)
   - Default and custom data directories
   - Missing file warnings

2. **DESI 2025 Loading** (9 tests)
   - w0, wa, H0, Omega_m parameters
   - Data caching
   - Asymmetric uncertainties
   - Error handling

3. **NuFIT 6.0 Loading** (9 tests)
   - Mixing angles (θ₁₂, θ₂₃, θ₁₃)
   - CP violation phase
   - Normal vs inverted ordering
   - Mass ordering preference

4. **PDG 2024 Loading** (11 tests)
   - Gauge boson masses (W, Z, Higgs)
   - Lepton masses (e, μ, τ)
   - Quark masses (top, etc.)
   - Convenience methods

5. **Error Handling** (5 tests)
   - Missing files
   - Malformed JSON
   - Empty files

6. **Registry Integration** (7 tests)
   - Loading into PMRegistry
   - ESTABLISHED status enforcement
   - Mass ordering data

7. **Singleton Pattern** (2 tests)
   - get_loader() functionality

8. **Convenience Functions** (4 tests)
   - Top-level access functions

9. **ExperimentalValue** (2 tests)
   - Dataclass creation and defaults

10. **Integration Tests** (4 tests)
    - Complete workflows for each data source
    - Accuracy report generation

11. **Parametrized Tests** (3 test groups)
    - DESI parameter access
    - NuFIT parameter access
    - PDG parameter access

**Total: 60+ test cases**

## Running Tests

### Run All Tests
```bash
cd h:\Github\PrincipiaMetaphysica\simulations\tests
pytest
```

### Run Specific Test File
```bash
pytest test_registry.py
pytest test_data_loader.py
```

### Run Specific Test Class
```bash
pytest test_registry.py::TestSingletonPattern
pytest test_data_loader.py::TestDESILoading
```

### Run Specific Test
```bash
pytest test_registry.py::TestSigmaDeviation::test_sigma_deviation_excellent
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=simulations --cov-report=html
```

### Run Only Fast Tests (Skip Integration)
```bash
pytest -m "not integration"
```

### Run Only Integration Tests
```bash
pytest -m integration
```

## Test Fixtures

### Registry Fixtures
- `reset_registry`: Automatically resets registry before each test
- `registry`: Provides fresh PMRegistry instance
- `sample_established_params`: Pre-populated with PDG/DESI parameters
- `sample_derived_params`: Pre-populated with derived parameters

### Data Loader Fixtures
- `temp_data_dir`: Temporary directory for test data files
- `sample_desi_data`: Sample DESI data structure
- `sample_nufit_data`: Sample NuFIT data structure
- `sample_pdg_data`: Sample PDG data structure
- `temp_loader`: Loader with temporary test data

### Shared Fixtures (conftest.py)
- `test_data_path`: Path to test data directory
- `simulations_path`: Path to simulations directory

## Test Organization

### Unit Tests
Test individual methods and functions in isolation:
- Parameter get/set
- Sigma computation
- Data parsing

### Integration Tests
Test complete workflows:
- Load experimental data → make prediction → validate → report
- Multi-source data integration

### Parametrized Tests
Efficiently test multiple scenarios:
- Sigma deviation boundaries (11 test cases from 1 test)
- Parameter access patterns
- Status categories

## Test Data

### Real Data Files Required
Some tests require actual data files:
- `simulations/data/experimental/desi_2025_constraints.json`
- `simulations/data/experimental/nufit_6_0_parameters.json`
- `simulations/data/experimental/pdg_2024_values.json`

Tests requiring real data are marked with `@pytest.mark.skipif` and will be skipped if files don't exist.

### Temporary Test Data
Most tests use temporary data files created in fixtures to ensure:
- Test isolation
- No dependency on external files
- Predictable test behavior

## Code Coverage

Current coverage targets:
- **PMRegistry**: 100% coverage
- **ExperimentalDataLoader**: 100% coverage

To generate coverage report:
```bash
pytest --cov=base.registry --cov=data.experimental_data_loader --cov-report=html
open htmlcov/index.html
```

## Testing Best Practices

### 1. Test Isolation
- Each test is independent
- Registry is reset before each test
- Temporary files are cleaned up

### 2. Descriptive Names
- Test names clearly describe what is being tested
- Use `test_<method>_<scenario>_<expected_result>` pattern

### 3. Arrange-Act-Assert
```python
def test_example(registry):
    # Arrange
    registry.set_param("test.param", 100, source="test")

    # Act
    value = registry.get_param("test.param")

    # Assert
    assert value == 100
```

### 4. Edge Cases
- Test with zero, negative, very large/small values
- Test missing data scenarios
- Test invalid inputs

### 5. Error Messages
- Use `match` parameter in `pytest.raises` to verify error messages
- Ensures errors are informative

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 5 seconds for full suite)
- No external dependencies (beyond test data files)
- Clear pass/fail criteria

## Adding New Tests

### For New Registry Features
1. Add test class to `test_registry.py`
2. Use existing fixtures
3. Follow naming conventions
4. Add to appropriate category in this README

### For New Data Sources
1. Add test class to `test_data_loader.py`
2. Create sample data fixture
3. Test loading, caching, and registry integration
4. Add parametrized tests for all parameters

### Example Template
```python
class TestNewFeature:
    """Test description of new feature."""

    def test_basic_functionality(self, registry):
        """Test basic usage."""
        # Arrange
        # Act
        # Assert
        pass

    def test_error_handling(self, registry):
        """Test error conditions."""
        with pytest.raises(ValueError):
            # Code that should raise error
            pass

    @pytest.mark.parametrize("input,expected", [
        (1, "one"),
        (2, "two"),
    ])
    def test_multiple_scenarios(self, registry, input, expected):
        """Test multiple scenarios efficiently."""
        pass
```

## Test Statistics

- **Total Test Files**: 2
- **Total Test Classes**: 23
- **Total Test Cases**: 122+
- **Code Coverage**: ~100% for tested modules
- **Execution Time**: < 5 seconds

## Dependencies

Required packages:
```bash
pip install pytest
```

Optional packages for enhanced testing:
```bash
pip install pytest-cov  # Coverage reports
pip install pytest-xdist  # Parallel test execution
pip install pytest-timeout  # Test timeout enforcement
```

## Troubleshooting

### Tests Fail with "Module not found"
- Ensure you're in the `simulations/tests` directory
- Check that `conftest.py` exists and adds parent directory to path

### Tests Skip with "requires actual data files"
- Some tests need real data files
- Either create the files or run with `-m "not requires_data"`

### Tests Fail with "Registry already has param"
- Registry may not be resetting
- Check that `reset_registry` fixture is used with `autouse=True`

### Import Errors
- Ensure all `__init__.py` files exist
- Check Python path configuration in `conftest.py`

## Future Enhancements

Potential additions to test suite:
- [ ] Performance benchmarks
- [ ] Stress tests (large parameter sets)
- [ ] Concurrency tests (thread safety)
- [ ] Mock tests for external dependencies
- [ ] Property-based testing with Hypothesis
- [ ] Snapshot testing for exports

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
