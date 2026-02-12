<!-- vale off -->
# Documentation Testing Suite

This directory contains automated tests for the documentation tooling.

## Running Tests

### Run all tests

```bash
# Run all test files
python3 -m pytest tests/ -v

# Or run individually
python3 tests/test_doc_test_utils.py
python3 tests/test_list_linter_exceptions.py
```

### With `pytest` if installed

```bash
pytest tests/test_doc_test_utils.py -v
pytest tests/test_list_linter_exceptions.py -v
pytest tests/ -v  # Run all tests
```

## Test Coverage

### test_doc_test_utils.py

Tests the shared utility functions:

- Front matter parsing (valid, missing, invalid YAML)
- Test config extraction
- Server/database key generation
- Console output formatting
- GitHub Actions annotation filtering
- File reading with error handling

### test_list_linter_exceptions.py

Tests the linter exception scanner:

- Vale exception tag parsing
- Markdownlint exception tag parsing
- Mixed exceptions (both types)
- Malformed exception tags (rejection)
- Empty files
- Line number accuracy
- Test data file processing

## Adding New Tests

1. Create a new test file: `test_<module_name>.py`
2. Import the module to test
3. Write test functions (prefix with `test_`)
4. Add test data to `test_data/` if needed
5. Run tests to verify

## Test Data

The `test_data/` directory contains sample files used by tests:

- `sample.md` - Complete markdown file with front matter and API examples
- `linter_exceptions.md` - File with Vale and markdownlint exception tags
- `clean.md` - Clean file with no linter exceptions

## Continuous Testing

Tests can be run automatically via GitHub Actions on:

- Every push to main
- Pull requests
- Scheduled runs (e.g., weekly)

See `.github/workflows/` for CI configuration.
