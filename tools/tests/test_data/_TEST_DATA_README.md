<!-- vale off -->
# Test Data Files

This directory contains **valid, well-formed** test files used by the test suites.
All files here should be processed successfully (though they may contain linter exceptions,
those exceptions are correctly formatted).

For files that should **fail** or return errors, see `../fail_data/`.

## Files

### sample.md

Complete, well-formed markdown file with:

- Valid YAML front matter
- API documentation examples
- Test configuration
- Multiple sections

**Used by:** `test_doc_test_utils.py`
**Expected:** Parses successfully

---

### clean.md

Clean markdown file with:

- Valid front matter
- NO linter exceptions
- Normal markdown content
- Multiple sections and formatting

**Used by:** `test_list_linter_exceptions.py`
**Expected:** 0 Vale exceptions, 0 markdownlint exceptions

---

### linter_exceptions.md

Markdown file with:

- Valid front matter
- 3 Vale exception tags (correctly formatted)
- 3 markdownlint exception tags (correctly formatted)
- Mixed content with both types

**Used by:** `test_list_linter_exceptions.py`
**Expected:** 3 Vale exceptions, 3 markdownlint exceptions detected

---

### edge_cases_front_matter.md

**Purpose:** Test front matter parsing edge cases

Contains valid YAML with:

- Empty fields
- Null values
- Different data types (numbers, booleans)
- Nested structures
- Special characters in strings
- Multiline strings
- Empty arrays

**Used by:** Tests for edge case handling
**Expected:** Parses successfully with correct types

---

### unicode_test.md

**Purpose:** Test Unicode and special character handling

Contains valid markdown with:

- Emoji characters (🎉 😀 🚀)
- Multiple language scripts (Chinese, Arabic, Japanese, etc.)
- Special symbols (©, ®, ™, €, etc.)
- Math symbols (∑, ∏, √, ∞)
- Arrows and other Unicode characters
- Linter exceptions with Unicode content

**Used by:** `test_list_linter_exceptions.py`

**Expected:**

- UTF-8 encoding handled correctly
- Line numbers accurate with multi-byte characters
- 1 Vale + 1 markdownlint exception detected

---

### api_doc_config_a.md

**Purpose:** Test file grouping by configuration (Configuration A)

Contains valid markdown with:

- Valid YAML front matter
- Test configuration with test_apps, server_url, local_database
- Configuration A: localhost:3000, /api/users.json

**Used by:** `test_get_test_configs.py`
**Expected:** Groups with other files having identical config

---

### api_doc_config_b.md

**Purpose:** Test file grouping by configuration (Configuration B)

Contains valid markdown with:

- Valid YAML front matter
- Test configuration with test_apps, server_url, local_database
- Configuration B: localhost:4000, /api/tasks.json (different from A)

**Used by:** `test_get_test_configs.py`
**Expected:** Forms separate group from config A

---

### api_doc_same_config_1.md

**Purpose:** Test file grouping - first file with shared config

Contains valid markdown with:

- Valid YAML front matter
- Test configuration matching api_doc_same_config_2.md
- Configuration: localhost:3000, /api/test.json

**Used by:** `test_get_test_configs.py`
**Expected:** Groups together with api_doc_same_config_2.md

---

### api_doc_same_config_2.md

**Purpose:** Test file grouping - second file with shared config

Contains valid markdown with:

- Valid YAML front matter
- Test configuration matching api_doc_same_config_1.md
- Configuration: localhost:3000, /api/test.json

**Used by:** `test_get_test_configs.py`
**Expected:** Groups together with api_doc_same_config_1.md

---

## Invalid/Error Files

Files that should **fail** or return errors are in the `../fail_data/` directory:

See `../fail_data/README.md` for details.

---

## Usage in Tests

Test files should be referenced like:

```python
test_data_dir = Path(__file__).parent / "test_data"
test_file = test_data_dir / "sample.md"

# All files in test_data/ should parse successfully
content = read_markdown_file(test_file)
assert content is not None

metadata = parse_front_matter(content)
assert metadata is not None  # Should succeed for all test_data files
```

## Adding New Test Files

When adding new test files to this directory:

1. Ensure the file is **valid and well-formed**
2. Document the purpose clearly in this README
3. Specify what the file contains
4. Describe expected behavior (what should be detected/parsed)
5. Reference which test files use it
6. Choose a descriptive filename

**If adding a file that should fail**, put it in `../fail_data/` instead.

## Test File Naming Convention

- `*_front_matter.md` - Tests front matter parsing features
- `*_exceptions.md` - Tests linter exception detection
- `clean.md` - No errors/exceptions (baseline)
- `edge_cases_*.md` - Edge case testing (but still valid)
- `unicode_*.md` - Unicode/encoding testing (but still valid)
