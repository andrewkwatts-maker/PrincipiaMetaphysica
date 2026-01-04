# Test Suite Quick Start

## Installation

```bash
# Install test dependencies
pip install pytest

# Optional: Install additional testing tools
pip install pytest-cov pytest-xdist
```

## Running Tests

### Run All Tests (158 tests)
```bash
cd h:\Github\PrincipiaMetaphysica\simulations\tests
pytest
```

**Expected Output:**
```
============================= 158 passed in 0.46s ==============================
```

### Run Specific Test File

**Registry Tests (70 tests):**
```bash
pytest test_registry.py
```

**Data Loader Tests (88 tests):**
```bash
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
pytest --cov=base.registry --cov=data.experimental_data_loader --cov-report=html
```

Then open `htmlcov/index.html` to view coverage report.

## Test Structure

### test_registry.py (70 tests)
Tests for PMRegistry singleton:
- Singleton pattern (4 tests)
- Parameter management (8 tests)
- Status categories (8 tests)
- Uncertainty propagation (3 tests)
- Sigma deviation (7 tests)
- Prediction validation (3 tests)
- Accuracy reports (2 tests)
- Mismatch detection (4 tests)
- Export methods (3 tests)
- Experimental data integration (4 tests)
- Edge cases (9 tests)
- Parametrized tests (16 tests)

### test_data_loader.py (88 tests)
Tests for ExperimentalDataLoader:
- Loader instantiation (4 tests)
- DESI 2025 loading (9 tests)
- NuFIT 6.0 loading (9 tests)
- PDG 2024 loading (12 tests)
- Error handling (5 tests)
- Registry integration (6 tests)
- Singleton pattern (2 tests)
- Convenience functions (4 tests)
- ExperimentalValue (2 tests)
- Integration scenarios (4 tests)
- Parametrized data access (13 tests)

## Test Categories

### Unit Tests
Test individual methods in isolation:
```bash
pytest test_registry.py::TestParameterManagement
```

### Integration Tests
Test complete workflows:
```bash
pytest test_data_loader.py::TestIntegrationScenarios
```

### Parametrized Tests
Efficiently test multiple scenarios:
```bash
pytest test_registry.py::TestParametrizedScenarios
```

## Quick Verification

**1. Check if all tests pass:**
```bash
pytest --tb=short
```

**2. Run only fast tests:**
```bash
pytest -m "not integration"
```

**3. Show test coverage:**
```bash
pytest --cov=base.registry --cov=data.experimental_data_loader --cov-report=term
```

## Common Issues

### Module not found
- Ensure you're in `simulations/tests` directory
- Check that `conftest.py` exists

### Tests fail with import errors
- Verify Python path in `conftest.py`
- Ensure `__init__.py` files exist

### Some tests skipped
- Tests requiring actual data files will skip if files don't exist
- This is expected behavior

## Expected Test Results

**All tests should pass:**
- test_registry.py: 70 passed
- test_data_loader.py: 88 passed
- **Total: 158 passed in ~0.5 seconds**

## Next Steps

After running tests successfully:
1. Review coverage report to identify untested code
2. Add new tests for any new features
3. Run tests before committing changes
4. Consider adding tests to CI/CD pipeline

## Support

For issues or questions:
- See full documentation in `README.md`
- Check pytest documentation: https://docs.pytest.org/
- Review test code for examples
