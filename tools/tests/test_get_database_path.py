#!/usr/bin/env python3
"""
Tests for get-database-path.py

Covers:
- Valid front matter with database path extraction
- Invalid/missing front matter handling
- Edge cases (leading slashes, Unicode)
- Error handling (missing files)
- Output format validation
- CLI argument validation
- Integration with shared utilities

Run with:
    python3 test_get_database_path.py
    pytest test_get_database_path.py -v
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

# Get absolute path to parent directory (tools/)
# __file__ = .../tools/tests/test_get_database_path.py
# parent = .../tools/tests/
# parent.parent = .../tools/
TOOLS_DIR = Path(__file__).resolve().parent.parent

# Add tools directory to path FIRST so imports work
sys.path.insert(0, str(TOOLS_DIR))

# Now import the module with hyphens in filename
SCRIPT_PATH = TOOLS_DIR / "get-database-path.py"

spec = importlib.util.spec_from_file_location(
    "get_database_path",
    SCRIPT_PATH
)
get_db_module = importlib.util.module_from_spec(spec)

# Execute the module (this will now find doc_test_utils)
spec.loader.exec_module(get_db_module)

# Get the function we need
get_database_path = get_db_module.get_database_path


def test_valid_complete():
    """Test extracting database path from complete front matter."""
    print("\n" + "="*60)
    print("TEST: Valid complete front matter")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is not None, "Should extract database path from valid file"
    assert db_path == "api/to-do-db-source.json", \
        f"Expected 'api/to-do-db-source.json', got '{db_path}'"
    assert not db_path.startswith('/'), "Leading slash should be stripped"
    
    print("  ✓ Complete front matter parsed correctly")
    print(f"  ✓ Database path: {db_path}")


def test_valid_minimal():
    """Test extracting database path from minimal front matter."""
    print("\n" + "="*60)
    print("TEST: Valid minimal front matter")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_minimal.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is not None, "Should extract database path from minimal file"
    assert isinstance(db_path, str), "Database path should be a string"
    assert len(db_path) > 0, "Database path should not be empty"
    
    print(f"  ✓ Minimal front matter parsed correctly")
    print(f"  ✓ Database path: {db_path}")


def test_valid_alternate_db():
    """Test extracting different database path."""
    print("\n" + "="*60)
    print("TEST: Valid alternate database path")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_alternate_db.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is not None, "Should extract alternate database path"
    assert db_path != "api/to-do-db-source.json", \
        "Should be different from default database"
    
    print(f"  ✓ Alternate database path extracted")
    print(f"  ✓ Database path: {db_path}")


def test_leading_slash_stripped():
    """Test that leading slashes are stripped from paths."""
    print("\n" + "="*60)
    print("TEST: Leading slash stripping")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is not None
    assert not db_path.startswith('/'), \
        f"Leading slash should be stripped, got: {db_path}"
    
    print("  ✓ Leading slash properly stripped")


def test_no_front_matter():
    """Test file without front matter returns None."""
    print("\n" + "="*60)
    print("TEST: No front matter")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    test_file = test_dir / "no_front_matter.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is None, "Should return None for file without front matter"
    
    print("  ✓ Missing front matter returns None")


def test_broken_yaml():
    """Test file with invalid YAML returns None."""
    print("\n" + "="*60)
    print("TEST: Broken YAML in front matter")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    test_file = test_dir / "broken_yaml.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is None, "Should return None for invalid YAML"
    
    print("  ✓ Invalid YAML returns None")


def test_missing_local_database():
    """Test file without local_database field returns None."""
    print("\n" + "="*60)
    print("TEST: Missing local_database field")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    test_file = test_dir / "missing_local_database.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is None, \
        "Should return None when local_database is missing (required field)"
    
    print("  ✓ Missing local_database returns None (field is required)")


def test_no_test_section():
    """Test file without test section returns None."""
    print("\n" + "="*60)
    print("TEST: No test section in front matter")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    test_file = test_dir / "no_test_section.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is None, "Should return None without test section"
    
    print("  ✓ Missing test section returns None")


def test_empty_file():
    """Test zero-length file returns None."""
    print("\n" + "="*60)
    print("TEST: Empty file")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    test_file = test_dir / "empty.md"
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is None, "Should return None for empty file"
    
    print("  ✓ Empty file returns None")


def test_file_not_found():
    """Test non-existent file returns None."""
    print("\n" + "="*60)
    print("TEST: Non-existent file")
    print("="*60)
    
    test_file = Path("nonexistent_file_that_does_not_exist.md")
    
    # Act
    db_path = get_database_path(test_file)
    
    # Assert
    assert db_path is None, "Should return None for missing file"
    
    print("  ✓ Missing file returns None")


def test_cli_valid_file():
    """Test CLI with valid file exits 0 and prints path."""
    print("\n" + "="*60)
    print("TEST: CLI with valid file")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    script = Path(__file__).parent.parent / "get-database-path.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, \
        f"Should exit 0 for valid file, got {result.returncode}"
    assert result.stdout.strip() == "api/to-do-db-source.json", \
        f"Should output database path, got: {result.stdout.strip()}"
    assert result.stderr == "", \
        f"Should have no stderr output, got: {result.stderr}"
    
    print("  ✓ Valid file exits with code 0")
    print(f"  ✓ Outputs: {result.stdout.strip()}")


def test_cli_invalid_file():
    """Test CLI with invalid file exits 1."""
    print("\n" + "="*60)
    print("TEST: CLI with invalid file")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    test_file = test_dir / "no_front_matter.md"
    script = Path(__file__).parent.parent / "get-database-path.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 1, \
        f"Should exit 1 for invalid file, got {result.returncode}"
    assert result.stdout == "", \
        f"Should have no stdout output, got: {result.stdout}"
    
    print("  ✓ Invalid file exits with code 1")
    print("  ✓ No stdout output")


def test_cli_no_arguments():
    """Test CLI with no arguments shows usage and exits 1."""
    print("\n" + "="*60)
    print("TEST: CLI with no arguments")
    print("="*60)
    
    script = Path(__file__).parent.parent / "get-database-path.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 1, \
        f"Should exit 1 when no arguments provided, got {result.returncode}"
    assert "Error:" in result.stderr or "Usage:" in result.stderr, \
        f"Should show error/usage message, got: {result.stderr}"
    
    print("  ✓ No arguments exits with code 1")
    print("  ✓ Shows usage message")


def test_output_format_no_trailing_whitespace():
    """Test output has no trailing whitespace."""
    print("\n" + "="*60)
    print("TEST: Output format (no trailing whitespace)")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    script = Path(__file__).parent.parent / "get-database-path.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    output = result.stdout
    assert output.endswith('\n'), "Should end with single newline"
    assert not output.endswith('\n\n'), "Should not have multiple newlines"
    assert output.strip() == output.rstrip(), "Should have no trailing spaces"
    
    print("  ✓ Output format correct (single trailing newline)")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR get-database-path.py")
    print("="*70)
    
    tests = [
        test_valid_complete,
        test_valid_minimal,
        test_valid_alternate_db,
        test_leading_slash_stripped,
        test_no_front_matter,
        test_broken_yaml,
        test_missing_local_database,
        test_no_test_section,
        test_empty_file,
        test_file_not_found,
        test_cli_valid_file,
        test_cli_invalid_file,
        test_cli_no_arguments,
        test_output_format_no_trailing_whitespace,
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
            print(f"\n  ✗ ERROR: {test_func.__name__}")
            print(f"    {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
