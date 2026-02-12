<!-- vale off -->
# Terminology Guide

This guide defines canonical terms and their correct usage across code, documentation, and comments.

## Core Terms

### Front Matter

**Definition:** Metadata section at the beginning of a markdown file, enclosed in `---` delimiters,
written in YAML format.

**Correct Usage:**

In **text/documentation** (two words):

```markdown
The front matter contains metadata about the document.
This file has valid front matter.
```

In **Python code** (underscore):

```python
# Function names
def parse_front_matter(content):
    pass

# Variable names
front_matter_data = {}
valid_front_matter = True

# Comments
# Extract front matter from the document
```

In **file names**:

- Python files: `front_matter_parser.py` (underscore)
- Scripts: `parse-front-matter.py` (hyphen)
- Test data: `broken_front_matter.md` (underscore)
- Documentation: `front-matter-guide.md` (hyphen)

**Common Mistakes:**

âŒ `frontmatter` (one word)
âŒ `front-matter` in Python code
âŒ `front_matter` in prose

**Reference:** [Merriam-Webster Dictionary](https://www.merriam-webster.com/dictionary/front%20matter)

---

### Linter Exception

**Definition:** An HTML comment tag that tells linting tools (Vale, markdownlint) to ignore
specific rules for a section of text.

**Correct Usage:**

In **text/documentation**:

```markdown
This file contains several linter exceptions.
The linter exception tag is correctly formatted.
```

In **Python code**:

```python
# Function names
def list_linter_exceptions(content):
    pass

# Variable names
linter_exceptions = {'vale': [], 'markdownlint': []}
exception_count = len(linter_exceptions)

# Comments
# Scan for linter exception tags
```

**Types:**

- Vale exception: `<!-- vale Rule.Name = NO -->`
- markdownlint exception: `<!-- markdownlint-disable MD001 -->`

**Alternative Terms:**

- "Exception tag" (acceptable)
- "Lint exception" (acceptable in informal contexts)

âŒ Avoid: "suppression", "ignore", "disable" (unless specifically referring to disable commands)

---

### Test Data vs Fail Data

**Test Data:**
**Definition:** Valid, well-formed files used to test that functions work correctly with proper input.

**Location:** `tests/test_data/`

**Usage:**

```python
# Files in test_data/ should parse successfully
test_file = test_data_dir / "sample.md"
content = read_markdown_file(test_file)
assert content is not None  # Should succeed
```

**Fail Data:**
**Definition:** Invalid or malformed files used to test error handling and edge cases.

**Location:** `tests/fail_data/`

**Usage:**

```python
# Files in fail_data/ should fail gracefully
fail_file = fail_data_dir / "broken_front_matter.md"
metadata = parse_front_matter(content)
assert metadata is None  # Should return None, not crash
```

**Key Difference:**

- test_data/ = "tests should **pass**"
- fail_data/ = "tests should **fail gracefully**"

---

### Annotation vs Log Message

**Annotation:**
**Definition:** A GitHub Actions formatted message that appears in the Actions UI, workflow summary,
and Pull request checks.

**Format:** `::level file=path,line=num::message`

**Usage:**

```python
# Creates both console output and GitHub annotation
log("Invalid YAML", "error", "file.md", 5, use_actions=True, action_level="error")
# Output: ERROR: Invalid YAML
# Output: ::error file=file.md,line=5::Invalid YAML
```

**Log Message:**
**Definition:** Console output for human readers.

**Usage:**

```python
# Console only
log("Processing 10 files...", "info")
# Output: INFO: Processing 10 files...
```

**Levels:**

- `info` - Informational (console only)
- `notice` - Notice (console + annotation if enabled)
- `warning` - Warning (console + annotation if enabled)
- `error` - Error (console + annotation if enabled)
- `success` - Success (console only)

---

### Action Level vs Message Level

**Message Level:**
**Definition:** The severity of a specific log message.

**Values:** `info`, `notice`, `warning`, `error`, `success`

**Action Level:**
**Definition:** The minimum severity required for a message to create a GitHub Actions annotation.

**Values:**

- `all` - Annotate notice, warning, and error
- `warning` - Annotate warning and error (default)
- `error` - Annotate only error

**Example:**

```python
# Message level is "warning"
# Action level is "error"
# Result: Console output only, no annotation
log("Deprecated syntax", "warning", file, line, True, "error")

# Message level is "error"  
# Action level is "error"
# Result: Console output AND annotation
log("Invalid syntax", "error", file, line, True, "error")
```

---

## Style and Format Terms

### snake_case

**Definition:** Words separated by underscores, all lowercase.

**Usage:** Python variables, functions, file names (Python modules)

**Examples:** `parse_front_matter`, `test_data`, `doc_test_utils.py`

### kebab-case (hyphen-case)

**Definition:** Words separated by hyphens, all lowercase.

**Usage:** Scripts, documentation files, CLI tools

**Examples:** `list-linter-exceptions.py`, `CODE-STYLE-GUIDE.md`

### PascalCase

**Definition:** Words concatenated, each word capitalized, no separators.

**Usage:** Python class names

**Examples:** `DocumentParser`, `TestRunner`

### UPPER_SNAKE_CASE

**Definition:** Words separated by underscores, all uppercase.

**Usage:** Constants

**Examples:** `MAX_FILE_SIZE`, `DEFAULT_TIMEOUT`

---

## Project-Specific Terms

### Utility Module

**Definition:** Python module containing shared helper functions.

**Usage:** `doc_test_utils.py`

**Not:** "helper file", "common functions file", "utils"

### Test Suite

**Definition:** A collection of test functions in a single test file.

**Usage:** `test_doc_test_utils.py` is a test suite

**Not:** "test file", "tests", "test script"

### Test Function

**Definition:** A single function testing specific functionality, starting with `test_`.

**Usage:** `test_parse_front_matter()` is a test function

### Test Case

**Definition:** A specific scenario being tested within a test function.

**Usage:**

```python
def test_parse_front_matter():
    # Test case 1: valid front matter
    # Test case 2: missing front matter
    # Test case 3: invalid YAML
```

---

## Documentation Terms

### Reference Documentation

**Definition:** Technical documentation describing APIs, functions, and parameters.

**Examples:** Docstrings, API docs, function signatures

### Guide

**Definition:** Step-by-step instructions for accomplishing a task.

**Examples:** "How to add a new test", "Migration guide"

### Standard

**Definition:** Authoritative rules or conventions to follow.

**Examples:** "Code Style Guide", "Test Standards"

### Summary

**Definition:** High-level overview of changes or status.

**Examples:** "Phase 2 Summary", "Test Results Summary"

---

## Testing Terms

### Unit Test

**Definition:** Tests a single function or small piece of code in isolation.

**Example:** Testing `parse_front_matter()` function alone

### Integration Test

**Definition:** Tests multiple components working together.

**Example:** Testing file reading + parsing + validation

### Regression Test

**Definition:** Test added to prevent a previously fixed bug from recurring.

**Example:** Test for Unicode line counting bug

### Edge Case

**Definition:** Input at the boundary of acceptable values or unusual situations.

**Examples:** Empty string, None, maximum value, Unicode characters

### Happy Path

**Definition:** Expected, normal usage with valid input.

**Example:** Parsing a well-formed markdown file with valid front matter

---

## Common Abbreviations

**Avoid** abbreviations in code unless they're standard industry terms:

âœ… **Acceptable:**

- `url` (Uniform Resource Locator)
- `api` (Application Programming Interface)
- `db` (database)
- `num` (number, when space-constrained)
- `temp` (temporary)

âŒ **Avoid:**

- `fm` for front matter
- `md` for markdown (except file extension)
- `val` for value
- `exc` for exception
- `cfg` for config

**Write out full words:**

```python
# Good
front_matter = parse_front_matter(content)
metadata = extract_metadata(front_matter)

# Bad
fm = parse_fm(content)
meta = extract_meta(fm)
```

---

## Version Control Terms

### Refactor

**Definition:** Restructuring code to improve design without changing behavior.

**Usage:** "Refactor parse_front_matter to use helper functions"

**Not:** "rewrite", "fix", "change"

### Migrate

**Definition:** Moving code from one pattern/system to another.

**Usage:** "Migrate list-linter-exceptions.py to use shared utilities"

**Not:** "convert", "update", "change"

### Phase

**Definition:** A logical grouping of related work.

**Usage:** "Phase 2: Migrate existing scripts"

**Not:** "step", "stage", "iteration"

---

## When in Doubt

1. **Check existing code** - Follow established patterns
2. **Consult this guide** - Use canonical terms
3. **Ask for clarification** - Don't guess
4. **Update this guide** - Add new terms as they're established

---

## Quick Reference

<!-- markdownlint-disable MD013 -->

| Concept | In Prose | In Python | In Files |
| --------- | ---------- | ----------- | ---------- |
| Front matter | "front matter" (2 words) | `front_matter` (underscore) | `front_matter.md` or `front-matter.md` |
| Multiple words | Use spaces | Use underscores | Use hyphens (docs) or underscores (data) |
| Constants | UPPER_SNAKE_CASE | UPPER_SNAKE_CASE | N/A |
| Classes | PascalCase | PascalCase | N/A |
| Functions | snake_case in text | snake_case | N/A |

<!-- markdownlint-enable MD013 -->

---

## Maintaining This Guide

When adding new terms:

1. Define clearly
2. Show correct usage (with examples)
3. Show incorrect usage (what to avoid)
4. Explain why if not obvious
5. Provide context/reference if needed
