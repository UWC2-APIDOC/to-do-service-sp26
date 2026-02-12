# Documentation testing suite

<!-- vale off -->

This directory contains automated tests for the documentation tooling.

## Running tests

### Run all tests

```bash
# Run all test files
python3 -m pytest tests/ -v

# Or run individually
python3 tests/test_doc_test_utils.py
python3 tests/test_list_linter_exceptions.py
```

### With pytest if installed

```bash
pytest tests/test_doc_test_utils.py -v
pytest tests/test_list_linter_exceptions.py -v
pytest tests/ -v  # Run all tests
```

## Test coverage

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
- MarkdownLint exception tag parsing
- Mixed exceptions (both types)
- Malformed exception tags (rejection)
- Empty files
- Line number accuracy
- Test data file processing

## Adding new tests

1. Create a new test file: `test_<module_name>.py`
2. Import the module to test
3. Write test functions (prefix with `test_`)
4. Add test data to `test_data/` if needed
5. Run tests to verify

## Test data

The `test_data/` directory contains sample files used by tests:

- `sample.md` - Complete markdown file with front matter and API examples
- `linter_exceptions.md` - File with Vale and markdownlint exception tags
- `clean.md` - Clean file with no linter exceptions

## Continuous testing

Tests can be run automatically via GitHub Actions on:

- Every push to main
- Pull requests
- Scheduled runs (for example, weekly)

See `.github/workflows/` for CI configuration.

---

## Maintainer guide

### Overview

This directory contains Python scripts that validate student PRs through
the automated `pr-validation.yml` workflow.

### Validation scripts

#### test-filenames.py

**Purpose:** Ensures students only modify allowed directories (`/docs`, `/assignments`)

**Usage:** Called by workflow with `CHANGED_FILES` environment variable

**Fails when:** Files outside allowed directories are modified
(unless user has write permissions)

#### test-front-matter.py

**Purpose:** Validates YAML front matter against schema

**Schema:** `.github/schemas/front-matter-schema.json`

**Fails when:** Missing required fields, invalid field types, schema violations

#### list-linter-exceptions.py

**Purpose:** Counts and reports Vale/markdownlint suppression tags

**Usage:** `python3 list-linter-exceptions.py file.md [--action]`

**Output:** Console summary and GitHub annotations (if `--action`)

#### markdown-survey.py

**Purpose:** Analyzes markdown structure (headings, code blocks, links)

**Usage:** `python3 markdown-survey.py file.md [--action]`

**Output:** Structural statistics

#### test-api-docs.py

**Purpose:** Tests API examples against running json-server

**Requirements:** `json-server@0.17.4`, test database file

**Front matter:** Files must have `test:` section with testable examples

**Fails when:** API calls return unexpected responses

#### Supporting files

- `doc_test_utils.py` - Shared utilities (front matter parsing, logging, file I/O)
- `schema_validator.py` - JSON schema validation
- `help_urls.py` - Centralized help URLs for error messages
- `get-test-configs.py` - Groups files by test configuration
- `get-database-path.py` - Extracts database path from front matter

### Workflow integration

The `pr-validation.yml` workflow runs in 4 stages:

1. **Discover changes** - Identifies modified files
2. **Test tools** - Validates testing infrastructure (if `tools/` changed)
3. **Validate commits** - Checks file locations and commit structure
4. **Lint and test** - Runs all validation in parallel:
    - Filename validation
    - Linter exceptions scan
    - Markdown survey
    - MarkdownLint
    - Vale
    - API documentation tests

**Dependencies:** Each stage depends on previous stages succeeding (fail-fast).

### Maintenance procedures

#### Updating Vale rules

**Steps:**

1. Edit `.vale.ini` or files in `.github/styles/`
2. Test locally:

    ```bash
    vale docs/
    ```

3. Commit changes
4. Vale cache is automatically invalidated on changes

**Note:** Vale version in workflow is 3.12.0.
Keep local version in sync.

#### Updating front matter schema

**Steps:**

1. Edit `.github/schemas/front-matter-schema.json`
2. Test with:

    ```bash
    python3 tools/test-front-matter.py docs/sample.md
    ```

3. Update documentation if adding required fields

#### Updating Python dependencies

Workflow uses `--break-system-packages` flag for pip installs.

**To add dependency:**

1. Add to workflow's pip install step
2. Test locally in clean environment
3. Document in this README

#### Troubleshooting common failures

**Vale fails in CI but passes locally:**

- Check `.vale.ini` config
- Verify Vale version matches workflow (3.12.0)
- Check for environment-specific paths

**API tests fail intermittently:**

- `json-server` may not be ready
- Increase startup wait time in workflow
- Check test database file exists

**Workflow times out:**

- Check for infinite loops in Python scripts
- Review job logs for hanging processes
- May need to increase timeout in workflow

### Testing locally before PR

Simulate the workflow:

```bash
# 1. Check filenames
export CHANGED_FILES="docs/api/sample.md"
python3 tools/test-filenames.py --action

# 2. Check front matter
python3 tools/test-front-matter.py docs/api/sample.md --action

# 3. List linter exceptions
python3 tools/list-linter-exceptions.py docs/api/sample.md --action

# 4. Survey markdown
python3 tools/markdown-survey.py docs/api/sample.md --action

# 5. Run linters
vale docs/
markdownlint docs/

# 6. Test API docs (if applicable)
# Start json-server first
json-server --watch api/to-do-db-source.json --port 3000 &
python3 tools/test-api-docs.py docs/api/sample.md --action
```

### Performance optimization history

- **Batch processing** - Python scripts process multiple files in single invocation
    (eliminates interpreter startup overhead)
- **Vale caching** - Vale binary cached at `~/.vale`
    (eliminates repeated downloads)
- **Workflow consolidation** - Single `pr-validation.yml` replaces 4 separate workflows
    (clearer dependencies, fail-fast)

### Related documentation

- Workflow details: `.github/workflows/pr-validation.yml`
- Front matter schema: `.github/schemas/front-matter-schema.json`
- Code standards: `/.github/.ai/CODE_STYLE_GUIDE.md` (if developing tools)
- Reporting tools: `reporting/_REPORTING_README.md` (workflow analytics)
