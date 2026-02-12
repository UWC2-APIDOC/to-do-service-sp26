<!-- vale off -->
# Fail Data Files

This directory contains test files that should **fail** or return **None/empty results** when processed.
These files are used to verify error handling and edge case behavior.

## Files

### broken_frontmatter.md

**Purpose:** Test YAML syntax error handling

**Contains:**

- Unclosed string: `local_database: "/api/test.json` (missing closing quote)
- Unclosed list: `broken_list: [unclosed`
- Other YAML syntax errors

**Expected Behavior:**

- `parse_frontmatter()` should return `None`
- No crashes or exceptions
- Graceful error handling

**Test Verification:** ✓ Returns None correctly

---

### no_frontmatter.md

**Purpose:** Test missing frontmatter handling

**Contains:**

- Normal markdown content
- No `---` delimiters
- No YAML frontmatter at all

**Expected Behavior:**

- `parse_frontmatter()` should return `None`
- File should still be readable
- No errors thrown

**Test Verification:** ✓ Returns None correctly

---

### malformed_exceptions.md

**Purpose:** Test rejection of invalid linter exception tags

**Contains:**

- Vale tags missing `=` sign
- Vale tags missing `NO` keyword
- Markdownlint tags with wrong format
- Incomplete rule numbers
- Wrong comment styles (`//`, `/* */`)
- **Also includes 2 valid tags** for comparison

**Expected Behavior:**

- Only the 2 correctly formatted tags should be detected
- Invalid tags should be ignored (not matched by regex)
- Line numbers for valid tags should be accurate

**Test Verification:** ✓ Only 1 Vale + 1 markdownlint detected (correct)

---

### empty.md

**Purpose:** Test zero-length file handling

**Contains:**

- Nothing (0 bytes)

**Expected Behavior:**

- `read_markdown_file()` should return empty string `""`
- `parse_frontmatter("")` should return `None`
- No crashes or errors
- Graceful handling of edge case

**Test Verification:** ✓ Handled correctly

---

### incomplete_test_config.md

**Purpose:** Test handling of incomplete test configurations

**Contains:**

- Valid YAML front matter
- Test section present
- Missing required field: `local_database`
- Has `test_apps` and `server_url` but incomplete

**Expected Behavior:**

- `parse_front_matter()` should succeed
- `get_server_database_key()` returns tuple with None for missing field
- `get-test-configs.py` should skip this file with warning
- Should not crash or cause errors

**Test Verification:** ✓ Skipped with appropriate warning

---

### no_test_config.md

**Purpose:** Test handling of files without test configuration

**Contains:**

- Valid YAML front matter
- Other fields (layout, title, description)
- NO test section at all

**Expected Behavior:**

- `parse_front_matter()` should succeed
- `get_test_config()` returns empty dict `{}`
- `get-test-configs.py` should skip this file with notice
- Should not be grouped with testable files

**Test Verification:** ✓ Skipped correctly

---

## Usage in Tests

These files are used to verify that the tools handle errors gracefully:

```python
# Test error handling
fail_data_dir = Path(__file__).parent / "fail_data"

# Broken YAML should return None
content = read_markdown_file(fail_data_dir / "broken_frontmatter.md")
metadata = parse_frontmatter(content)
assert metadata is None, "Should return None for broken YAML"

# Missing frontmatter should return None
content = read_markdown_file(fail_data_dir / "no_frontmatter.md")
metadata = parse_frontmatter(content)
assert metadata is None, "Should return None for missing frontmatter"

# Invalid exception tags should not match
content = read_markdown_file(fail_data_dir / "malformed_exceptions.md")
exceptions = list_vale_exceptions(content)
# Should find only 2 valid tags, not the ~10+ invalid ones
assert len(exceptions['vale']) == 1
assert len(exceptions['markdownlint']) == 1
```

## Why Separate from test_data/?

**test_data/** contains valid, well-formed files where:

- Tests should **pass**
- Parsing should **succeed**
- Data should be **extracted correctly**

**fail_data/** contains invalid, malformed, or edge case files where:

- Tests should detect **errors**
- Parsing should return **None** or **empty results**
- Tools should handle **gracefully** without crashing

This separation makes test intentions clearer and easier to maintain.

## Adding New Fail Files

When adding new files to this directory:

1. Document what's wrong with the file
2. Specify expected behavior (what should fail/return None)
3. Verify the actual behavior
4. Update this README
5. Update test files to include the new fail case
