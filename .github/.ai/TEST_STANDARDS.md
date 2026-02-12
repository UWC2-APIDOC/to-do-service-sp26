<!-- vale off -->
# Test Standards

This guide defines testing standards and best practices for the documentation testing tools project.

## Test File Organization

### Directory Structure

```text
tests/
â”œâ”€â”€ README.md                       # Testing overview
â”œâ”€â”€ test_*.py                       # Test suites
â”œâ”€â”€ test_data/                      # Valid test files (should pass)
â”‚   â”œâ”€â”€ README.md
â”‚   â””â”€â”€ *.md                        # Test files
â””â”€â”€ fail_data/                      # Invalid test files (should fail)
    â”œâ”€â”€ README.md
    â””â”€â”€ *.md                        # Test files
```

### File Placement Rules

**test_data/** - Files where tests should **succeed**:

- Valid markdown with proper front matter
- Correctly formatted linter exceptions
- Well-formed data structures
- Files that represent normal, expected input

**fail_data/** - Files where tests should **fail gracefully**:

- Broken YAML syntax
- Missing required elements
- Malformed tags or patterns
- Edge cases that should return None/errors

## Test File Naming

### Test Suites

Follow pytest convention: `test_<module_name>.py`

```text
# Good
test_doc_test_utils.py
test_list_linter_exceptions.py
test_markdown_survey.py

# Bad
doc_test_utils_test.py
test.py
tests_for_utils.py
```

### Test Functions

Start with `test_` and describe what's being tested:

```python
# Good
def test_parse_front_matter():
def test_parse_front_matter_with_invalid_yaml():
def test_log_output_with_github_actions():

# Bad
def parse_front_matter_test():
def test1():
def test_everything():
```

## Test Structure

### Basic Test Pattern

Use Arrange-Act-Assert (AAA) pattern:

```python
def test_parse_front_matter():
    """Test YAML front matter parsing from markdown content."""
    # Arrange - Set up test data
    content = """---
layout: default
description: Test
---
# Heading
"""
    
    # Act - Execute the function being tested
    metadata = parse_front_matter(content)
    
    # Assert - Verify the results
    assert metadata is not None, "Should parse valid front matter"
    assert metadata['layout'] == 'default'
    assert metadata['description'] == 'Test'
```

### Multiple Test Cases in One Function

Group related assertions:

```python
def test_parse_front_matter():
    """Test various front matter scenarios."""
    print("\n" + "="*60)
    print("TEST: parse_front_matter()")
    print("="*60)
    
    # Test 1: Valid front matter
    content_valid = "---\nlayout: default\n---\n# Test"
    metadata = parse_front_matter(content_valid)
    assert metadata is not None, "Should parse valid front matter"
    print("  SUCCESS: Valid front matter parsed")
    
    # Test 2: Missing front matter
    content_missing = "# Test\nNo front matter"
    metadata = parse_front_matter(content_missing)
    assert metadata is None, "Should return None for missing front matter"
    print("  SUCCESS: Missing front matter returns None")
    
    # Test 3: Invalid YAML
    content_invalid = "---\nlayout: [unclosed\n---\n# Test"
    metadata = parse_front_matter(content_invalid)
    assert metadata is None, "Should return None for invalid YAML"
    print("  SUCCESS: Invalid YAML returns None")
    
    print("  âœ“ All parse_front_matter tests passed")
```

## Assertion Standards

### Always Provide Failure Messages

Help debugging with descriptive messages:

```python
# Good
assert count == 5, f"Expected 5 exceptions, got {count}"
assert metadata is not None, "Should parse valid front matter"
assert result['status'] == 'success', f"Expected success, got {result['status']}"

# Bad
assert count == 5
assert metadata is not None
assert result['status'] == 'success'
```

### Check All Important Attributes

Don't just test that something exists:

```python
# Good
assert exceptions is not None
assert len(exceptions['vale']) == 2
assert exceptions['vale'][0]['line'] == 5
assert exceptions['vale'][0]['rule'] == 'Style.Rule'

# Insufficient
assert exceptions is not None
```

### Test Edge Cases Explicitly

```python
# Test empty input
assert parse_front_matter("") is None

# Test whitespace
assert parse_front_matter("   \n  \n  ") is None

# Test None input (if applicable)
with pytest.raises(TypeError):
    parse_front_matter(None)
```

## Test Coverage Requirements

### What to Test

**Core Functionality:**

- Happy path (normal, expected use)
- Edge cases (empty, None, boundary values)
- Error conditions (invalid input, missing data)
- Integration points (multiple functions working together)

**For Each Function:**

1. **Valid input** - Normal expected usage
2. **Invalid input** - Malformed data, wrong types
3. **Empty input** - Empty strings, empty lists, None
4. **Edge cases** - Boundary conditions, special characters
5. **Error handling** - Exceptions raised/caught correctly

### Coverage Goals

- Aim for 80%+ code coverage
- 100% coverage of critical paths
- All error handling paths tested

## Test Data Management

### Creating Test Files

**For test_data/** (valid files):

```python
# Create descriptive, realistic test files
sample.md           # Complete, realistic example
clean.md            # Minimal valid file
unicode_test.md     # Tests Unicode handling
```

**For fail_data/** (invalid files):

```python
# Create files that test error handling
broken_front_matter.md      # Invalid YAML
no_front_matter.md          # Missing front matter
empty.md                    # Zero-length file
malformed_exceptions.md     # Invalid exception tags
```

### Test Data Documentation

Each test data file should:

1. Have a clear purpose
2. Be documented in the directory's README
3. Specify expected behavior
4. Include comments explaining special cases

Example README entry:

```markdown
### broken_front_matter.md
**Purpose:** Test YAML syntax error handling

**Contains:**

- Unclosed strings
- Unclosed lists
- Invalid YAML syntax

**Expected Behavior:**

- `parse_front_matter()` should return `None`
- No crashes or exceptions
- Graceful error handling
```

## Output Standards

### Test Progress Output

Provide clear, informative output:

```python
def test_parse_front_matter():
    print("\n" + "="*60)
    print("TEST: parse_front_matter()")
    print("="*60)
    
    # Test case 1
    content = "..."
    metadata = parse_front_matter(content)
    assert metadata is not None
    print("  SUCCESS: Valid front matter parsed correctly")
    
    # Test case 2
    content_invalid = "..."
    metadata = parse_front_matter(content_invalid)
    assert metadata is None
    print("  SUCCESS: Invalid YAML returns None")
    
    print("  âœ“ All parse_front_matter tests passed")
```

### Final Summary

Provide test suite summary:

```python
def run_all_tests():
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR doc_test_utils.py")
    print("="*70)
    
    tests = [test_parse_front_matter, test_get_test_config, ...]
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n  âœ— FAILED: {test_func.__name__}")
            print(f"    {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0
```

## Running Tests

### Command Line

Tests should be runnable multiple ways:

```bash
# Direct execution
python3 test_doc_test_utils.py

# With pytest
pytest test_doc_test_utils.py -v

# All tests
pytest tests/ -v

# Specific test function
pytest tests/test_doc_test_utils.py::test_parse_front_matter -v
```

### Exit Codes

```python
if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)  # 0 = success, 1 = failure
```

## Test Isolation

### Each Test Should Be Independent

```python
# Good - Self-contained
def test_parse_front_matter():
    content = "---\nlayout: default\n---"
    metadata = parse_front_matter(content)
    assert metadata is not None

# Bad - Depends on global state
global_content = None

def setup_test():
    global global_content
    global_content = "---\nlayout: default\n---"

def test_parse_front_matter():
    metadata = parse_front_matter(global_content)
    assert metadata is not None
```

### Clean Up After Tests

```python
def test_with_file():
    # Create temporary file
    test_file = Path("temp_test.md")
    test_file.write_text("content")
    
    # Run test
    result = process_file(test_file)
    assert result is not None
    
    # Clean up
    test_file.unlink()
```

## Testing External Dependencies

### Mock External Calls When Needed

```python
# When testing file operations
def test_read_markdown_file():
    # Create actual test file
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "sample.md"
    
    # Test with real file
    content = read_markdown_file(test_file)
    assert content is not None
```

### Test Error Conditions

```python
def test_read_nonexistent_file():
    bad_file = Path("nonexistent.md")
    content = read_markdown_file(bad_file)
    assert content is None, "Should return None for missing file"
```

## Regression Testing

### Add Tests for Every Bug

When fixing a bug:

1. Write a test that reproduces the bug
2. Verify the test fails
3. Fix the bug
4. Verify the test passes
5. Commit both fix and test

### Document the Bug in Test

```python
def test_unicode_line_counting():
    """
    Regression test for bug #123.
    
    Previously, line numbers were incorrect when file contained
    multi-byte Unicode characters (emoji, Chinese, etc).
    """
    content = """---
layout: default
---
# Test ä¸­æ–‡
<!-- vale Rule = NO -->
"""
    exceptions = list_vale_exceptions(content)
    assert exceptions['vale'][0]['line'] == 5, "Line number should account for Unicode"
```

## Performance Testing

### Not Required for Every Function

Focus performance tests on:

- Functions processing large datasets
- Functions called repeatedly
- Critical path operations

### Simple Performance Check

```python
import time

def test_parse_performance():
    """Verify parsing doesn't degrade with file size."""
    # Create large content
    content = "---\nlayout: default\n---\n" + ("# Section\n" * 1000)
    
    start = time.time()
    metadata = parse_front_matter(content)
    elapsed = time.time() - start
    
    assert elapsed < 1.0, f"Parsing took {elapsed}s, expected < 1s"
    assert metadata is not None
```

## Continuous Integration

### Tests Should Be CI-Ready

- No manual intervention required
- No interactive prompts
- Clear success/failure indication
- Proper exit codes
- Reasonable execution time

### GitHub Actions Integration

Tests integrate with GitHub Actions:

```yaml
- name: Run tests
  run: |
    python3 -m pytest tests/ -v
```

## Documentation Standards

### Test File Docstrings

```python
#!/usr/bin/env python3
"""
Tests for doc_test_utils module.

Covers:
- Front matter parsing (valid, invalid, edge cases)
- File reading with error handling
- Test configuration extraction
- Logging and GitHub Actions annotations

Run with:
    python3 test_doc_test_utils.py
    pytest test_doc_test_utils.py -v
"""
```

### Test Function Docstrings

```python
def test_parse_front_matter():
    """
    Test YAML front matter parsing from markdown content.
    
    Covers:
    - Valid front matter
    - Missing front matter (returns None)
    - Invalid YAML syntax (returns None)
    """
```

## Common Pitfalls to Avoid

âŒ **Don't test implementation details**

```python
# Bad - Testing internal implementation
assert '_cached_result' in module.__dict__

# Good - Test public behavior
assert parse_front_matter(content) == expected_result
```

âŒ **Don't create brittle tests**

```python
# Bad - Breaks if output format changes slightly
assert output == "Found 5 exceptions in file.md"

# Good - Test the important parts
assert "5 exceptions" in output
assert "file.md" in output
```

âŒ **Don't skip cleanup**

```python
# Bad - Leaves files behind
test_file.write_text("test")
assert process_file(test_file)
# Missing: test_file.unlink()
```

âŒ **Don't test multiple unrelated things**

```python
# Bad - Too much in one test
def test_everything():
    test_parsing()
    test_validation()
    test_output()
    # ... 100 more assertions
```

## Remember

- **Write tests first when possible** (TDD)
- **Test behavior, not implementation**
- **Make failures easy to diagnose**
- **Keep tests fast and independent**
- **Update tests when requirements change**
