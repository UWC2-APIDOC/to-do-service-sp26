<!-- vale off -->
# Refactoring Checklist

This checklist ensures consistent, complete refactoring when migrating tools or adding new functionality.

## Before Starting

### 1. Review Existing Standards

- [ ] Read `CODE_STYLE_GUIDE.md`
- [ ] Read `TEST_STANDARDS.md`
- [ ] Read `TERMINOLOGY.md`
- [ ] Read `PROJECT_CONVENTIONS.md`
- [ ] Review similar existing tools

### 2. Understand Current State

- [ ] Identify what needs to be refactored
- [ ] Document current behavior/functionality
- [ ] List dependencies and integrations
- [ ] Check for existing tests
- [ ] Note any special requirements

### 3. Plan the Refactoring

- [ ] Define scope (what will/won't change)
- [ ] Identify shared utilities to use
- [ ] Plan new tests needed
- [ ] List files that need updating
- [ ] Estimate complexity and time

---

## During Refactoring

### Code Changes

#### 1. Import Shared Utilities

- [ ] Add `from doc_test_utils import ...`
- [ ] Import only needed functions
- [ ] Follow import organization (stdlib, third-party, local)
- [ ] Remove duplicate code that's now shared

#### 2. Update Function Names

- [ ] Use `snake_case` for functions
- [ ] Follow terminology guide (e.g., `parse_front_matter`)
- [ ] Update all function calls
- [ ] Update references in comments

#### 3. Update CLI Arguments

- [ ] Use `--action [LEVEL]` pattern
- [ ] Remove redundant argument flags
- [ ] Add help text with examples
- [ ] Test argument parsing

**Standard pattern:**

```python
parser.add_argument(
    '--action', '-a',
    type=str,
    nargs='?',
    const='warning',
    default=None,
    choices=['all', 'warning', 'error'],
    metavar='LEVEL',
    help='Output GitHub Actions annotations'
)
```

#### 4. Replace Custom Logging

- [ ] Replace custom logging with shared `log()` function
- [ ] Use correct levels (info, notice, warning, error, success)
- [ ] Include file_path and line numbers where relevant
- [ ] Pass `use_actions` and `action_level` correctly

**Standard pattern:**

```python
log(message, level, file_path, line, use_actions, action_level)
```

#### 5. Error Handling

- [ ] Use try/except with specific exceptions
- [ ] Return `None` for errors (don't raise in most cases)
- [ ] Log errors with appropriate level
- [ ] Include helpful context in error messages

#### 6. Documentation

- [ ] Update module docstring
- [ ] Update function docstrings
- [ ] Follow Google-style format
- [ ] Include examples where helpful

### File Organization

#### 7. File Names

- [ ] Rename files to match conventions
- [ ] Python modules: `snake_case.py`
- [ ] Scripts: `kebab-case.py`
- [ ] Test files: `test_*.py`
- [ ] Test data: `descriptive_name.md`

#### 8. Directory Structure

- [ ] Place utility modules in `tools/`
- [ ] Place test files in `tools/tests/`
- [ ] Place valid test data in `tools/tests/test_data/`
- [ ] Place invalid test data in `tools/tests/fail_data/`

---

## Testing

### 9. Create Test File

- [ ] Create `test_<module_name>.py`
- [ ] Add module docstring
- [ ] Import functions to test
- [ ] Follow `test_` naming convention

**Template:**

```python
#!/usr/bin/env python3
"""
Tests for <module_name>.

Covers:
- List of functionality tested

Run with:
    python3 test_<module_name>.py
    pytest test_<module_name>.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from module_name import function1, function2

def test_function1():
    """Test function1 behavior."""
    # Arrange
    # Act
    # Assert
    pass

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
```

### 10. Write Tests

For each function, test:

- [ ] Happy path (normal usage)
- [ ] Invalid input
- [ ] Empty/None input
- [ ] Edge cases
- [ ] Error conditions

**Checklist per function:**

```python
def test_function_name():
    # Test 1: Valid input
    assert function(valid_input) == expected_output
    
    # Test 2: Invalid input
    assert function(invalid_input) is None
    
    # Test 3: Empty input
    assert function("") is None
    
    # Test 4: Edge cases
    assert function(edge_case) == expected
```

### 11. Create Test Data

- [ ] Create valid test files in `test_data/`
- [ ] Create invalid test files in `fail_data/`
- [ ] Document each file in README.md
- [ ] Specify expected behavior
- [ ] Include edge cases (Unicode, special chars, etc.)

**Test data checklist:**

- [ ] `test_data/sample.md` - Complete valid example
- [ ] `test_data/clean.md` - Minimal valid file
- [ ] `test_data/edge_cases_*.md` - Edge cases
- [ ] `fail_data/broken_*.md` - Invalid input
- [ ] `fail_data/empty.md` - Zero-length file

### 12. Verify Tests Pass

- [ ] Run tests directly: `python3 test_file.py`
- [ ] Run with pytest: `pytest test_file.py -v`
- [ ] Verify all tests pass
- [ ] Check test output is informative
- [ ] Verify exit codes are correct (0=success, 1=failure)

---

## Documentation

### 13. Update READMEs

**tools/tests/README.md:**

- [ ] Add new test file to list
- [ ] Describe what it tests
- [ ] Update test count
- [ ] Add to test structure diagram

**tools/tests/test_data/README.md:**

- [ ] Document each new test file
- [ ] Specify purpose
- [ ] Describe contents
- [ ] State expected behavior

**tools/tests/fail_data/README.md:**

- [ ] Document each new fail file
- [ ] Specify what should fail
- [ ] Describe expected error handling
- [ ] Include verification status

### 14. Create Summary Document

Create `PHASE_X_SUMMARY.md`:

- [ ] List changes made
- [ ] Document what was refactored
- [ ] Show before/after examples
- [ ] Include test results
- [ ] List files created/modified
- [ ] Note any issues or special considerations

### 15. Update Master Documentation

If patterns change:

- [ ] Update `CODE_STYLE_GUIDE.md`
- [ ] Update `TEST_STANDARDS.md`
- [ ] Update `TERMINOLOGY.md`
- [ ] Update `PROJECT_CONVENTIONS.md`

---

## Verification

### 16. Run All Tests

- [ ] Run complete test suite: `pytest tests/ -v`
- [ ] Verify all tests pass
- [ ] Check for warnings
- [ ] Verify test coverage

### 17. Manual Testing

Test the tool manually:

- [ ] Normal usage: `python3 tool.py file.md`
- [ ] GitHub Actions mode: `python3 tool.py file.md --action`
- [ ] All annotation levels: `--action all`, `--action warning`, `--action error`
- [ ] Error cases: missing files, invalid input
- [ ] Help text: `python3 tool.py --help`

### 18. Integration Testing

If the tool integrates with workflows:

- [ ] Test in GitHub Actions workflow
- [ ] Verify annotations appear correctly
- [ ] Check exit codes in CI
- [ ] Verify error handling in CI

### 19. Code Review

Self-review checklist:

- [ ] Follows code style guide
- [ ] Uses correct terminology
- [ ] Proper error handling
- [ ] No duplicate code
- [ ] Clear, informative comments
- [ ] Complete docstrings
- [ ] Consistent naming

---

## Finalization

### 20. Clean Up

- [ ] Remove old/unused code
- [ ] Remove debug print statements
- [ ] Remove commented-out code
- [ ] Clean up temporary files
- [ ] Organize imports

### 21. Git Operations

- [ ] Stage changes: `git add <files>`
- [ ] Commit with descriptive message
- [ ] Push to feature branch
- [ ] Create pull request
- [ ] Add description and context

**Good commit message:**

```text
Refactor list-linter-exceptions.py to use shared utilities

- Remove custom annotate() function (78 lines)
- Update CLI to use --action \[LEVEL\] pattern
- Add comprehensive test suite (7 tests)
- Create test data files
- Update documentation

Closes #123
```

### 22. Final Verification

Before marking complete:

- [ ] All tests pass locally
- [ ] All tests pass in CI
- [ ] Documentation is complete
- [ ] Code review is done
- [ ] Changes are committed
- [ ] Summary document created

---

## Common Mistakes to Avoid

âŒ **Don't:**

- Skip writing tests ("I'll add them later")
- Copy-paste code instead of using shared utilities
- Use inconsistent naming conventions
- Leave TODOs in production code
- Forget to update documentation
- Mix refactoring with feature additions
- Change behavior without updating tests

âœ… **Do:**

- Write tests first or alongside code changes
- Use shared utilities whenever possible
- Follow naming conventions consistently
- Complete documentation before finishing
- Test thoroughly (unit, integration, manual)
- Refactor first, then add features
- Keep changes focused and scoped

---

## Quick Reference

### Files to Create/Update

**For new tool:**

- [ ] `tools/new-tool.py` - The tool itself
- [ ] `tools/tests/test_new_tool.py` - Test suite
- [ ] `tools/tests/test_data/*.md` - Valid test files
- [ ] `tools/tests/fail_data/*.md` - Invalid test files
- [ ] `tools/tests/test_data/README.md` - Document test files
- [ ] `tools/tests/fail_data/README.md` - Document fail files
- [ ] `tools/tests/README.md` - Update with new tests
- [ ] `tools/PHASE_X_SUMMARY.md` - Document changes

**For refactoring:**

- [ ] Update the tool: `tools/existing-tool.py`
- [ ] Update/create tests: `tools/tests/test_existing_tool.py`
- [ ] Add/update test data as needed
- [ ] Update all relevant READMEs
- [ ] Create summary document

---

## Checklist Usage

### For New Contributors

1. Print this checklist
2. Check off items as you complete them
3. Don't skip items unless you have a good reason
4. Ask questions if anything is unclear

### For Reviewers

Use this checklist to verify:

1. All required items are completed
2. Documentation is thorough
3. Tests are comprehensive
4. Standards are followed

### Continuous Improvement

Update this checklist when:

- New patterns emerge
- Steps are frequently missed
- Better approaches are found
- Tools/processes change

---

## Getting Help

If stuck on any step:

1. Check the relevant guide (CODE_STYLE_GUIDE.md, etc.)
2. Look at similar existing code
3. Review Phase 1 and Phase 2 examples
4. Ask for clarification
5. Document the issue for future reference

Remember: **Consistency and completeness matter more than speed.**
