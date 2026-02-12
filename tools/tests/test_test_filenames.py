#!/usr/bin/env python3
"""
Tests for test-filenames.py

Covers:
- Filename validation (safe, unsafe characters)
- Environment variable handling
- Empty/missing CHANGED_FILES
- Edge cases (special characters, Unicode)

Run with:
    python3 test_test_filenames.py
    or
    pytest test_test_filenames.py -v
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import the script module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module we're testing
import importlib.util
spec = importlib.util.spec_from_file_location(
    "test_filenames",
    Path(__file__).parent.parent / "test-filenames.py"
)
test_filenames = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_filenames)


def test_get_changed_files():
    """Test extraction of changed files from environment variable."""
    print("\n" + "="*60)
    print("TEST: get_changed_files()")
    print("="*60)
    
    # Save original environment value
    original_value = os.environ.get('CHANGED_FILES')
    
    try:
        # Test 1: Valid comma-separated list
        os.environ['CHANGED_FILES'] = 'file1.py, file2.md, file3.txt'
        files = test_filenames.get_changed_files()
        assert len(files) == 3, f"Expected 3 files, got {len(files)}"
        assert files[0] == 'file1.py', "First file should be file1.py"
        assert files[1] == 'file2.md', "Second file should be file2.md"
        assert files[2] == 'file3.txt', "Third file should be file3.txt"
        print("  SUCCESS: Comma-separated list parsed correctly")
        
        # Test 2: Empty environment variable
        os.environ['CHANGED_FILES'] = ''
        files = test_filenames.get_changed_files()
        assert len(files) == 0, "Empty string should return empty list"
        print("  SUCCESS: Empty string returns empty list")
        
        # Test 3: Missing environment variable
        if 'CHANGED_FILES' in os.environ:
            del os.environ['CHANGED_FILES']
        files = test_filenames.get_changed_files()
        assert len(files) == 0, "Missing env var should return empty list"
        print("  SUCCESS: Missing env var returns empty list")
        
        # Test 4: Extra whitespace
        os.environ['CHANGED_FILES'] = '  file1.py  ,  file2.md  ,  '
        files = test_filenames.get_changed_files()
        assert len(files) == 2, f"Expected 2 files, got {len(files)}"
        assert files[0] == 'file1.py', "Should strip whitespace"
        assert files[1] == 'file2.md', "Should strip whitespace"
        print("  SUCCESS: Whitespace trimmed correctly")
        
        # Test 5: Single file
        os.environ['CHANGED_FILES'] = 'single.py'
        files = test_filenames.get_changed_files()
        assert len(files) == 1, "Should handle single file"
        assert files[0] == 'single.py', "Single file should be correct"
        print("  SUCCESS: Single file handled correctly")
        
    finally:
        # Restore original environment value
        if original_value is not None:
            os.environ['CHANGED_FILES'] = original_value
        elif 'CHANGED_FILES' in os.environ:
            del os.environ['CHANGED_FILES']
    
    print("  ✓ All get_changed_files tests passed")


def test_validate_safe_filenames():
    """Test validation of safe filenames."""
    print("\n" + "="*60)
    print("TEST: validate_filenames() - Safe filenames")
    print("="*60)
    
    # Test 1: All safe filenames
    safe_files = [
        'file.py',
        'test-script.py',
        'doc_utils.py',
        'README.md',
        'file.name.with.dots.txt',
        'file_123.py',
        'CamelCase.py',
        'file-with-hyphens.md'
    ]
    
    unsafe = test_filenames.validate_filenames(safe_files)
    assert len(unsafe) == 0, f"Expected no unsafe files, got {len(unsafe)}: {unsafe}"
    print("  SUCCESS: All safe filenames validated")
    
    # Test 2: Empty list
    unsafe = test_filenames.validate_filenames([])
    assert len(unsafe) == 0, "Empty list should return empty list"
    print("  SUCCESS: Empty list handled correctly")
    
    print("  ✓ All safe filename tests passed")


def test_validate_unsafe_filenames():
    """Test detection of unsafe characters in filenames."""
    print("\n" + "="*60)
    print("TEST: validate_filenames() - Unsafe filenames")
    print("="*60)
    
    # Test 1: Whitespace
    files_with_spaces = ['file name.py', 'test\tfile.md', 'new\nline.txt']
    unsafe = test_filenames.validate_filenames(files_with_spaces)
    assert len(unsafe) == 3, f"Expected 3 unsafe files, got {len(unsafe)}"
    print("  SUCCESS: Whitespace characters detected")
    
    # Test 2: Shell metacharacters
    files_with_meta = [
        'file;rm.py',       # semicolon
        'file|pipe.py',     # pipe
        'file&bg.py',       # ampersand
        'file$var.py',      # dollar sign
        'file`cmd`.py',     # backtick
        'file*.py',         # asterisk
        'file?.py',         # question mark
        'file[].py',        # brackets
        'file().py',        # parentheses
    ]
    unsafe = test_filenames.validate_filenames(files_with_meta)
    assert len(unsafe) == len(files_with_meta), f"Expected {len(files_with_meta)} unsafe files, got {len(unsafe)}"
    print("  SUCCESS: Shell metacharacters detected")
    
    # Test 3: Quote characters
    files_with_quotes = [
        'file"quote.py',    # double quote
        "file'quote.py",    # single quote
    ]
    unsafe = test_filenames.validate_filenames(files_with_quotes)
    assert len(unsafe) == 2, f"Expected 2 unsafe files, got {len(unsafe)}"
    print("  SUCCESS: Quote characters detected")
    
    # Test 4: Path separators
    files_with_separators = [
        'path\\file.py',    # backslash
        'file:name.py',     # colon (Windows drive issues)
    ]
    unsafe = test_filenames.validate_filenames(files_with_separators)
    assert len(unsafe) == 2, f"Expected 2 unsafe files, got {len(unsafe)}"
    print("  SUCCESS: Path separator characters detected")
    
    # Test 5: Angle brackets
    files_with_brackets = ['file<redirect.py', 'file>output.py']
    unsafe = test_filenames.validate_filenames(files_with_brackets)
    assert len(unsafe) == 2, f"Expected 2 unsafe files, got {len(unsafe)}"
    print("  SUCCESS: Angle brackets detected")
    
    # Test 6: Comma (delimiter character)
    files_with_comma = ['file,name.py']
    unsafe = test_filenames.validate_filenames(files_with_comma)
    assert len(unsafe) == 1, f"Expected 1 unsafe file, got {len(unsafe)}"
    print("  SUCCESS: Comma character detected")
    
    print("  ✓ All unsafe filename tests passed")


def test_validate_mixed_filenames():
    """Test validation with mix of safe and unsafe filenames."""
    print("\n" + "="*60)
    print("TEST: validate_filenames() - Mixed safe/unsafe")
    print("="*60)
    
    # Mix of safe and unsafe
    mixed_files = [
        'safe1.py',         # safe
        'file name.py',     # unsafe: space
        'safe2.md',         # safe
        'unsafe;file.py',   # unsafe: semicolon
        'safe_3.txt',       # safe
        'bad$file.py',      # unsafe: dollar sign
        'safe-4.py',        # safe
    ]
    
    unsafe = test_filenames.validate_filenames(mixed_files)
    assert len(unsafe) == 3, f"Expected 3 unsafe files, got {len(unsafe)}"
    assert 'file name.py' in unsafe, "Should detect space"
    assert 'unsafe;file.py' in unsafe, "Should detect semicolon"
    assert 'bad$file.py' in unsafe, "Should detect dollar sign"
    print("  SUCCESS: Mixed safe/unsafe correctly separated")
    
    print("  ✓ All mixed filename tests passed")


def test_edge_cases():
    """Test edge cases and special scenarios."""
    print("\n" + "="*60)
    print("TEST: Edge cases")
    print("="*60)
    
    # Test 1: Very long filename (but safe)
    long_safe = ['a' * 200 + '.py']
    unsafe = test_filenames.validate_filenames(long_safe)
    assert len(unsafe) == 0, "Long but safe filename should pass"
    print("  SUCCESS: Long safe filename validated")
    
    # Test 2: Multiple dots (safe)
    multi_dot = ['file.name.with.many.dots.extension.py']
    unsafe = test_filenames.validate_filenames(multi_dot)
    assert len(unsafe) == 0, "Multiple dots should be safe"
    print("  SUCCESS: Multiple dots validated")
    
    # Test 3: Leading/trailing hyphens and underscores (safe)
    edge_chars = ['-leading.py', 'trailing-.py', '_leading.py', 'trailing_.py']
    unsafe = test_filenames.validate_filenames(edge_chars)
    assert len(unsafe) == 0, "Leading/trailing hyphens and underscores should be safe"
    print("  SUCCESS: Leading/trailing special chars validated")
    
    # Test 4: Numbers only (safe)
    numbers = ['123456.py', '999.md']
    unsafe = test_filenames.validate_filenames(numbers)
    assert len(unsafe) == 0, "Numeric filenames should be safe"
    print("  SUCCESS: Numeric filenames validated")
    
    # Test 5: Unicode characters (safe - not in unsafe pattern)
    # Note: Unicode is technically safe for the regex pattern used
    unicode_files = ['file_中文.py', 'file_émoji.md', 'file_ñ.py']
    unsafe = test_filenames.validate_filenames(unicode_files)
    assert len(unsafe) == 0, "Unicode characters should be safe"
    print("  SUCCESS: Unicode filenames validated")
    
    # Test 6: Just extension (safe)
    just_ext = ['.gitignore', '.env']
    unsafe = test_filenames.validate_filenames(just_ext)
    assert len(unsafe) == 0, "Dotfiles should be safe"
    print("  SUCCESS: Dotfiles validated")
    
    print("  ✓ All edge case tests passed")


def test_environment_variable_handling():
    """Test complete workflow with environment variables."""
    print("\n" + "="*60)
    print("TEST: Environment variable workflow")
    print("="*60)
    
    # Save original environment value
    original_value = os.environ.get('CHANGED_FILES')
    
    try:
        # Test 1: Complete workflow with safe files
        os.environ['CHANGED_FILES'] = 'file1.py, file2.md, test.txt'
        files = test_filenames.get_changed_files()
        unsafe = test_filenames.validate_filenames(files)
        assert len(files) == 3, "Should get 3 files"
        assert len(unsafe) == 0, "All should be safe"
        print("  SUCCESS: Workflow with safe files")
        
        # Test 2: Complete workflow with unsafe files
        os.environ['CHANGED_FILES'] = 'safe.py, un safe.md, bad;file.txt'
        files = test_filenames.get_changed_files()
        unsafe = test_filenames.validate_filenames(files)
        assert len(files) == 3, "Should get 3 files"
        assert len(unsafe) == 2, "Should find 2 unsafe files"
        print("  SUCCESS: Workflow with unsafe files")
        
        # Test 3: Workflow with empty list
        os.environ['CHANGED_FILES'] = ''
        files = test_filenames.get_changed_files()
        unsafe = test_filenames.validate_filenames(files)
        assert len(files) == 0, "Should get empty list"
        assert len(unsafe) == 0, "Should find no unsafe files"
        print("  SUCCESS: Workflow with empty list")
        
    finally:
        # Restore original environment value
        if original_value is not None:
            os.environ['CHANGED_FILES'] = original_value
        elif 'CHANGED_FILES' in os.environ:
            del os.environ['CHANGED_FILES']
    
    print("  ✓ All environment variable workflow tests passed")


def test_comprehensive_unsafe_characters():
    """Test all unsafe characters defined in the pattern."""
    print("\n" + "="*60)
    print("TEST: Comprehensive unsafe character coverage")
    print("="*60)
    
    # Test each unsafe character individually
    unsafe_chars = {
        ' ': 'space',
        '\t': 'tab',
        '\n': 'newline',
        ',': 'comma',
        '*': 'asterisk',
        '?': 'question mark',
        '[': 'left bracket',
        ']': 'right bracket',
        '|': 'pipe',
        '&': 'ampersand',
        ';': 'semicolon',
        '$': 'dollar sign',
        '`': 'backtick',
        '"': 'double quote',
        "'": 'single quote',
        '<': 'less than',
        '>': 'greater than',
        '(': 'left paren',
        ')': 'right paren',
        ':': 'colon',
        '\\': 'backslash'
    }
    
    for char, name in unsafe_chars.items():
        test_file = f'file{char}name.py'
        unsafe = test_filenames.validate_filenames([test_file])
        assert len(unsafe) == 1, f"Should detect {name} as unsafe"
    
    print(f"  SUCCESS: All {len(unsafe_chars)} unsafe characters detected individually")
    print("  ✓ All comprehensive unsafe character tests passed")


def run_all_tests():
    """Run all test functions and report results."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR test-filenames.py")
    print("="*70)
    
    tests = [
        test_get_changed_files,
        test_validate_safe_filenames,
        test_validate_unsafe_filenames,
        test_validate_mixed_filenames,
        test_edge_cases,
        test_environment_variable_handling,
        test_comprehensive_unsafe_characters
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
# End of file tools/tests/test_test_filenames.py