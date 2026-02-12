#!/usr/bin/env python3
"""
Tests for list-linter-exceptions.py

Run with:
    python3 test_list_linter_exceptions.py
    or
    pytest test_list_linter_exceptions.py -v
"""

import sys
import io
from pathlib import Path

# Add parent directory to path to import the script module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the functions we're testing
# Note: We need to import list_vale_exceptions as a module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "list_linter_exceptions",
    Path(__file__).parent.parent / "list-linter-exceptions.py"
)
list_linter_exceptions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(list_linter_exceptions)


def test_parse_vale_exceptions():
    """Test parsing of Vale exception tags."""
    print("\n" + "="*60)
    print("TEST: Parse Vale exceptions")
    print("="*60)
    
    # Test single Vale exception
    content = """---
layout: default
---
# Test

<!-- vale Style.Rule = NO -->
Some text here.
<!-- vale Style.Rule = YES -->
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content)
    assert len(exceptions['vale']) == 1, f"Expected 1 Vale exception, got {len(exceptions['vale'])}"
    assert exceptions['vale'][0]['rule'] == 'Style.Rule', "Should match rule name"
    assert exceptions['vale'][0]['line'] == 6, f"Expected line 6, got {exceptions['vale'][0]['line']}"
    print("  SUCCESS: Single Vale exception parsed correctly")
    
    # Test multiple Vale exceptions
    content_multi = """
<!-- vale Rule.One = NO -->
Text
<!-- vale Rule.Two = NO -->
More text
<!-- vale Rule.Three = NO -->
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content_multi)
    assert len(exceptions['vale']) == 3, f"Expected 3 Vale exceptions, got {len(exceptions['vale'])}"
    assert exceptions['vale'][0]['rule'] == 'Rule.One', "First rule should be Rule.One"
    assert exceptions['vale'][1]['rule'] == 'Rule.Two', "Second rule should be Rule.Two"
    assert exceptions['vale'][2]['rule'] == 'Rule.Three', "Third rule should be Rule.Three"
    print("  SUCCESS: Multiple Vale exceptions parsed correctly")
    
    # Test no Vale exceptions
    content_none = """# Just normal markdown
No exceptions here.
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content_none)
    assert len(exceptions['vale']) == 0, "Should find no Vale exceptions"
    print("  SUCCESS: No Vale exceptions in clean content")
    
    print("  ✓ All Vale exception parsing tests passed")


def test_parse_markdownlint_exceptions():
    """Test parsing of markdownlint exception tags."""
    print("\n" + "="*60)
    print("TEST: Parse markdownlint exceptions")
    print("="*60)
    
    # Test single markdownlint exception
    content = """---
layout: default
---
# Test

<!-- markdownlint-disable MD013 -->
This is a very long line that would normally trigger MD013
<!-- markdownlint-enable MD013 -->
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content)
    assert len(exceptions['markdownlint']) == 1, f"Expected 1 markdownlint exception, got {len(exceptions['markdownlint'])}"
    assert exceptions['markdownlint'][0]['rule'] == 'MD013', "Should match rule MD013"
    assert exceptions['markdownlint'][0]['line'] == 6, f"Expected line 6, got {exceptions['markdownlint'][0]['line']}"
    print("  SUCCESS: Single markdownlint exception parsed correctly")
    
    # Test multiple markdownlint exceptions
    content_multi = """
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content_multi)
    assert len(exceptions['markdownlint']) == 3, f"Expected 3 markdownlint exceptions, got {len(exceptions['markdownlint'])}"
    assert exceptions['markdownlint'][0]['rule'] == 'MD001', "First rule should be MD001"
    assert exceptions['markdownlint'][1]['rule'] == 'MD033', "Second rule should be MD033"
    assert exceptions['markdownlint'][2]['rule'] == 'MD041', "Third rule should be MD041"
    print("  SUCCESS: Multiple markdownlint exceptions parsed correctly")
    
    # Test no markdownlint exceptions
    content_none = """# Just normal markdown
No exceptions here.
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content_none)
    assert len(exceptions['markdownlint']) == 0, "Should find no markdownlint exceptions"
    print("  SUCCESS: No markdownlint exceptions in clean content")
    
    print("  ✓ All markdownlint exception parsing tests passed")


def test_mixed_exceptions():
    """Test file with both Vale and markdownlint exceptions."""
    print("\n" + "="*60)
    print("TEST: Mixed Vale and markdownlint exceptions")
    print("="*60)
    
    content = """# Document with Mixed Exceptions

<!-- vale Style.Rule = NO -->
Some text with Vale exception.

<!-- markdownlint-disable MD013 -->
This line is too long for markdownlint.

<!-- vale Another.Rule = NO -->
More text with another Vale exception.

<!-- markdownlint-disable MD033 -->
<div>HTML content</div>
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content)
    
    # Check counts
    assert len(exceptions['vale']) == 2, f"Expected 2 Vale exceptions, got {len(exceptions['vale'])}"
    assert len(exceptions['markdownlint']) == 2, f"Expected 2 markdownlint exceptions, got {len(exceptions['markdownlint'])}"
    print("  SUCCESS: Correct counts for both exception types")
    
    # Check Vale details
    assert exceptions['vale'][0]['rule'] == 'Style.Rule', "First Vale rule should be Style.Rule"
    assert exceptions['vale'][0]['line'] == 3, f"First Vale exception should be on line 3, got {exceptions['vale'][0]['line']}"
    assert exceptions['vale'][1]['rule'] == 'Another.Rule', "Second Vale rule should be Another.Rule"
    assert exceptions['vale'][1]['line'] == 9, f"Second Vale exception should be on line 9, got {exceptions['vale'][1]['line']}"
    print("  SUCCESS: Vale exception details correct")
    
    # Check markdownlint details
    assert exceptions['markdownlint'][0]['rule'] == 'MD013', "First markdownlint rule should be MD013"
    assert exceptions['markdownlint'][0]['line'] == 6, f"First markdownlint exception should be on line 6, got {exceptions['markdownlint'][0]['line']}"
    assert exceptions['markdownlint'][1]['rule'] == 'MD033', "Second markdownlint rule should be MD033"
    assert exceptions['markdownlint'][1]['line'] == 12, f"Second markdownlint exception should be on line 12, got {exceptions['markdownlint'][1]['line']}"
    print("  SUCCESS: Markdownlint exception details correct")
    
    print("  ✓ All mixed exception tests passed")


def test_malformed_exceptions():
    """Test that malformed exception tags are not matched."""
    print("\n" + "="*60)
    print("TEST: Malformed exception tags")
    print("="*60)
    
    content = """# Test Malformed Tags

<!-- vale Style.Rule NO -->
Missing equals sign

<!-- vale Style.Rule = -->
Missing NO

<!--vale Style.Rule = NO-->
No spaces (still valid actually)

<!-- markdownlint MD013 -->
Wrong format

<!-- markdownlint-disable MD -->
Incomplete rule
"""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content)
    
    # The third one (no spaces) should actually match per the regex
    # The others should not match
    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    # We expect 1 Vale match (the no-spaces version is valid)
    assert vale_count == 1, f"Expected 1 Vale exception (no-spaces version), got {vale_count}"
    
    # We expect 0 markdownlint matches (all are invalid)
    assert md_count == 0, f"Expected 0 markdownlint exceptions, got {md_count}"
    
    print("  SUCCESS: Malformed tags correctly rejected")
    print("  ✓ All malformed exception tests passed")


def test_empty_file():
    """Test parsing an empty file."""
    print("\n" + "="*60)
    print("TEST: Empty file")
    print("="*60)
    
    content = ""
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content)
    
    assert len(exceptions['vale']) == 0, "Empty file should have no Vale exceptions"
    assert len(exceptions['markdownlint']) == 0, "Empty file should have no markdownlint exceptions"
    
    print("  SUCCESS: Empty file handled correctly")
    print("  ✓ Empty file test passed")


def test_exception_line_numbers():
    """Test that line numbers are correctly identified."""
    print("\n" + "="*60)
    print("TEST: Line number accuracy")
    print("="*60)
    
    # Create content where we know exactly which lines have exceptions
    lines = [
        "# Title",                                    # Line 1
        "",                                           # Line 2
        "<!-- vale Rule.One = NO -->",                # Line 3
        "Text",                                       # Line 4
        "",                                           # Line 5
        "<!-- markdownlint-disable MD001 -->",       # Line 6
        "",                                           # Line 7
        "More text",                                  # Line 8
        "<!-- vale Rule.Two = NO -->",                # Line 9
        "<!-- markdownlint-disable MD033 -->",       # Line 10
    ]
    content = "\n".join(lines)
    
    exceptions = list_linter_exceptions.list_vale_exceptions(content)
    
    # Check Vale line numbers
    assert exceptions['vale'][0]['line'] == 3, f"First Vale exception should be line 3, got {exceptions['vale'][0]['line']}"
    assert exceptions['vale'][1]['line'] == 9, f"Second Vale exception should be line 9, got {exceptions['vale'][1]['line']}"
    
    # Check markdownlint line numbers
    assert exceptions['markdownlint'][0]['line'] == 6, f"First markdownlint exception should be line 6, got {exceptions['markdownlint'][0]['line']}"
    assert exceptions['markdownlint'][1]['line'] == 10, f"Second markdownlint exception should be line 10, got {exceptions['markdownlint'][1]['line']}"
    
    print("  SUCCESS: All line numbers correctly identified")
    print("  ✓ Line number accuracy test passed")


def test_with_test_data_files():
    """Test with actual test data files."""
    print("\n" + "="*60)
    print("TEST: Test data files")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    # Test file with exceptions
    exceptions_file = test_data_dir / "linter_exceptions.md"
    if exceptions_file.exists():
        content = exceptions_file.read_text(encoding='utf-8')
        exceptions = list_linter_exceptions.list_vale_exceptions(content)
        
        vale_count = len(exceptions['vale'])
        md_count = len(exceptions['markdownlint'])
        
        print(f"  Found {vale_count} Vale exceptions")
        print(f"  Found {md_count} markdownlint exceptions")
        assert vale_count > 0 or md_count > 0, "Test file should have at least one exception"
        print("  SUCCESS: Test file with exceptions processed")
    else:
        print("  SKIPPED: linter_exceptions.md not found")
    
    # Test clean file
    clean_file = test_data_dir / "clean.md"
    if clean_file.exists():
        content = clean_file.read_text(encoding='utf-8')
        exceptions = list_linter_exceptions.list_vale_exceptions(content)
        
        assert len(exceptions['vale']) == 0, "Clean file should have no Vale exceptions"
        assert len(exceptions['markdownlint']) == 0, "Clean file should have no markdownlint exceptions"
        print("  SUCCESS: Clean file has no exceptions")
    else:
        print("  SKIPPED: clean.md not found")
    
    print("  ✓ Test data file tests completed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR list-linter-exceptions.py")
    print("="*70)
    
    tests = [
        test_parse_vale_exceptions,
        test_parse_markdownlint_exceptions,
        test_mixed_exceptions,
        test_malformed_exceptions,
        test_empty_file,
        test_exception_line_numbers,
        test_with_test_data_files
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n  ✗ FAILED: {test_func.__name__}")
            print(f"    {str(e)}")
        except Exception as e:
            failed += 1
            print(f"\n  ✗ ERROR in {test_func.__name__}: {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
# End of file tools/tests/test_list_linter_exception.py 
