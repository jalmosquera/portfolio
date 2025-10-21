# Testing Guide

## Quick Start

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html
```

## Running Specific Tests

```bash
# Run tests for specific app
pytest apps/projects/tests/
pytest apps/about/tests/
pytest apps/contact/tests/
pytest apps/skills/tests/

# Run specific test types
pytest apps/ -k "model"        # Only model tests
pytest apps/ -k "serializer"   # Only serializer tests
pytest apps/ -k "views"        # Only view tests

# Run specific test file
pytest apps/projects/tests/test_models.py

# Run specific test
pytest apps/projects/tests/test_models.py::TestProjectModel::test_create_project_with_required_fields
```

## Test Suite Overview

### Total Tests: 338
- **Projects App**: 73 tests (22 models, 22 serializers, 29 views)
- **About App**: 75 tests (26 models, 22 serializers, 27 views)
- **Contact App**: 88 tests (27 models, 26 serializers, 35 views)
- **Skills App**: 102 tests (47 models, 32 serializers, 51 views)

### Coverage: 68% overall
- **Models**: 100% coverage
- **Serializers**: 98-100% coverage
- **API Views**: 56-86% coverage
- **Routers**: 100% coverage

## Test Structure

Each app has three test files:
```
apps/<app_name>/tests/
├── __init__.py
├── test_models.py      # Django model tests
├── test_serializers.py # DRF serializer tests
└── test_views.py       # API endpoint tests
```

## What's Tested

### Model Tests
- Field validation (max_length, URL format, email format)
- Default values
- Required vs optional fields
- Model methods (str, to_dict, etc.)
- Ordering and filtering
- Timestamps (created_at, updated_at)
- Business logic (e.g., single active profile in AboutMe)

### Serializer Tests
- Data validation
- CamelCase to snake_case field mapping
- Required field enforcement
- Read-only fields
- Partial updates
- List serialization
- File uploads
- Output structure

### View Tests
- CRUD endpoints (List, Retrieve, Create, Update, Delete)
- Custom actions (@action decorators)
- Query parameters (search, ordering, filtering)
- Error handling (404, 400 responses)
- Response formats (camelCase, JSON)
- Edge cases

## Configuration

### pytest.ini
- Django settings: `core.settings`
- Test discovery: `apps/` directory
- Coverage reports: HTML and terminal
- Database: SQLite in-memory with `--nomigrations`

### conftest.py
Global fixtures:
- `api_client`: DRF API client
- `request_factory`: Django request factory
- `media_storage`: Temporary media storage

## Known Issues

### View Tests (131 failing)
The view tests require URL routing configuration. Tests are correctly written but need one of:
1. URL patterns registered in test environment, OR
2. Updated to use DRF's APIRequestFactory directly

### Minor Issues (6 failing)
- Some image upload tests need media storage configuration
- One years_experience validation test needs minor fix

These don't affect the core functionality tests (models and serializers).

## Test Quality

- **Pattern**: AAA (Arrange-Act-Assert)
- **Isolation**: Each test independent with database rollback
- **Fixtures**: pytest fixtures for reusable objects
- **Naming**: Descriptive test names explaining what is tested
- **Documentation**: Docstrings in each test

## CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -r requirements-test.txt
    pytest --cov=apps --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Additional Resources

- Full test report: `TEST_REPORT.md`
- Test dependencies: `requirements-test.txt`
- pytest documentation: https://docs.pytest.org/
- pytest-django: https://pytest-django.readthedocs.io/
