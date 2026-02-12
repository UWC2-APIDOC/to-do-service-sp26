<!-- vale off -->
# Phase 1: Shared utilities with test suite

## Structure created

```text

tools/
├── doc_test_utils.py              # Shared utility module (clean, no tests)
└── tests/
    ├── README.md                  # Testing documentation
    ├── test_doc_test_utils.py     # Comprehensive test suite
    └── test_data/
        └── sample.md              # Sample Markdown for testing
```

## Changes in phase 1

### 1. Core utilities `doc_test_utils.py`

**Front matter Functions:**

- `parse_frontmatter(content)` - Extract YAML from Markdown
- `get_test_config(metadata)` - Get test configuration
- `get_server_database_key(metadata)` - Get server/db tuple for grouping

**File Operations:**

- `read_markdown_file(filepath)` - Read Markdown with error handling

**Unified Logging:**

- `log(message, level, file_path, line, use_actions, action_level)` - Console + GitHub Actions annotations
    - Levels: `info`, `notice`, `warning`, `error`, `success`
    - Text-only labels (INFO:, WARNING:, ERROR:)
    - Annotation filtering: `all`, `warning`, `error`
    - `info`/`success` never annotate (console only)

### 2. Test suite

Location: `tests/test_doc_test_utils.py`

**Test coverage:**

- Front matter parsing (valid, missing, invalid YAML)
- Test `config` extraction
- Server/database key generation
- Console output formatting
- GitHub Actions annotation filtering
- File reading with error handling

**How to run the tests:**

```bash
# Direct execution
python3 tests/test_doc_test_utils.py

# With pytest
pytest tests/test_doc_test_utils.py -v

# All tests in directory
pytest tests/ -v
```

**Example test output:**

```text
======================================================================
 RUNNING ALL TESTS FOR doc_test_utils.py
======================================================================
TEST SUMMARY: 6 passed, 0 failed
======================================================================
```

## Key design decisions

1. **Text-only labels** - Replaced icons with `INFO:`, `WARNING:`, `ERROR:` for better log file compatibility
2. **Separate test directory** - Keeps utilities clean, supports automated testing
3. **Standard test structure** - pytest/unittest compatible for CI/CD integration
4. **Test data directory** - Organized location for sample files

## Next steps: Phase 2

Migrate existing scripts to use shared utilities:

1. `list-linter-exceptions.py` - Replace `annotate()` with `log()`
2. `markdown-survey.py` - Use shared file reading and logging
3. `test-api-docs.py` - Import  front matter and logging functions

## Test Suites

### test_doc_test_utils.py

Tests for shared utility functions.

**Coverage:**

- Front matter parsing (valid, missing, invalid YAML)
- Test config extraction
- Server/database key generation
- Console output formatting
- GitHub Actions annotation filtering
- File reading with error handling

**Tests:** 6 | **Status:** ✓ All passing

---

### test_list_linter_exception.py

Tests for list-linter-exceptions.py script.

**Coverage:**

- Vale exception parsing (single, multiple, none)
- markdownlint exception parsing (single, multiple, none)
- Mixed exceptions
- Malformed tag rejection
- Empty file handling
- Line number accuracy
- Real test data file usage

**Tests:** 7 | **Status:** ✓ All passing

---

### test_markdown_survey.py

Tests for markdown-survey.py script.

**Coverage:**

- Pattern counting (headings, lists, code blocks, links, images)
- Statistics calculation
- Text-only and formatted output
- File reading error handling
- Empty file handling
- Unicode content handling
- CLI argument processing

**Tests:** 13 | **Status:** ✓ All passing

---

### test_test_api_docs.py

Tests for test-api-docs.py script.

**Coverage:**

- Testable entry parsing
- Curl command extraction
- JSON response extraction
- JSON comparison logic
- Front matter schema validation
- Example execution flow
- Error handling

**Tests:** 8 | **Status:** ✓ All passing

---

### test_get_test_configs.py

Tests for get-test-configs.py utility.

**Coverage:**

- File grouping by identical test configurations
- Different configurations (separate groups)
- Mixed configurations
- Skipping files without front matter
- Skipping files with incomplete config
- Skipping files without test section
- JSON output format
- Shell output format
- Empty file list handling

**Tests:** 9 | **Status:** ✓ All passing

---

## Total Test Coverage

**Test Suites:** 5
**Total Tests:** 43
**Status:** ✓ All passing
