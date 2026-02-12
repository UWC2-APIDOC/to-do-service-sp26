#!/usr/bin/env python3
"""
Tests for get-test-configs.py

Covers:
- File grouping by configuration
- Configuration matching logic
- JSON and shell output formats
- CLI argument validation
- Integration with shared utilities
- Files without config are skipped

Run with:
    python3 test_get_test_configs.py
    pytest test_get_test_configs.py -v
"""

import sys
import json
import subprocess
import importlib.util
from pathlib import Path

# Get absolute path to parent directory (tools/)
# __file__ = .../tools/tests/test_get_test_configs.py
# parent = .../tools/tests/
# parent.parent = .../tools/
TOOLS_DIR = Path(__file__).resolve().parent.parent

# Add tools directory to path FIRST so imports work
sys.path.insert(0, str(TOOLS_DIR))

# Now import the module with hyphens in filename
SCRIPT_PATH = TOOLS_DIR / "get-test-configs.py"

spec = importlib.util.spec_from_file_location(
    "get_test_configs",
    SCRIPT_PATH
)
get_configs_module = importlib.util.module_from_spec(spec)

# Execute the module (this will now find doc_test_utils)
spec.loader.exec_module(get_configs_module)

# Get the functions we need
group_files_by_config = get_configs_module.group_files_by_config
output_json = get_configs_module.output_json
output_shell = get_configs_module.output_shell


def test_group_single_file():
    """Test grouping a single file."""
    print("\n" + "="*60)
    print("TEST: Group single file")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    files = [test_dir / "valid_complete.md"]
    
    # Act
    groups = group_files_by_config(files)
    
    # Assert
    assert len(groups) == 1, f"Should have 1 group, got {len(groups)}"
    assert sum(len(files) for files in groups.values()) == 1, \
        "Should have 1 file total"
    
    print(f"  ✓ Single file grouped correctly")
    print(f"  ✓ Groups: {len(groups)}")


def test_group_same_config():
    """Test grouping files with identical configuration."""
    print("\n" + "="*60)
    print("TEST: Group files with same configuration")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    files = [
        test_dir / "valid_complete.md",
        test_dir / "valid_same_as_complete.md"
    ]
    
    # Act
    groups = group_files_by_config(files)
    
    # Assert
    assert len(groups) == 1, \
        f"Files with same config should be in 1 group, got {len(groups)}"
    group_files = list(groups.values())[0]
    assert len(group_files) == 2, \
        f"Group should contain 2 files, got {len(group_files)}"
    
    print(f"  ✓ Files with same config grouped together")
    print(f"  ✓ Group size: {len(group_files)}")


def test_group_different_configs():
    """Test grouping files with different configurations."""
    print("\n" + "="*60)
    print("TEST: Group files with different configurations")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    files = [
        test_dir / "valid_complete.md",
        test_dir / "valid_alternate_db.md"
    ]
    
    # Act
    groups = group_files_by_config(files)
    
    # Assert
    assert len(groups) == 2, \
        f"Files with different configs should be in 2 groups, got {len(groups)}"
    
    for group_files in groups.values():
        assert len(group_files) == 1, \
            "Each group should have 1 file"
    
    print(f"  ✓ Files with different configs in separate groups")
    print(f"  ✓ Total groups: {len(groups)}")


def test_group_mixed_valid_invalid():
    """Test grouping mix of valid and invalid files."""
    print("\n" + "="*60)
    print("TEST: Group mix of valid and invalid files")
    print("="*60)
    
    test_dir = Path(__file__).parent
    files = [
        test_dir / "test_data" / "valid_complete.md",
        test_dir / "fail_data" / "no_front_matter.md",
        test_dir / "test_data" / "valid_minimal.md",
        test_dir / "fail_data" / "missing_local_database.md"
    ]
    
    # Act
    groups = group_files_by_config(files)
    
    # Assert
    total_files = sum(len(files) for files in groups.values())
    assert total_files == 2, \
        f"Should only include 2 valid files, got {total_files}"
    
    print(f"  ✓ Only valid files included in groups")
    print(f"  ✓ Total grouped files: {total_files}")
    print(f"  ✓ Invalid files skipped: 2")


def test_files_without_config_skipped():
    """Test that files without test config are skipped."""
    print("\n" + "="*60)
    print("TEST: Files without config are skipped")
    print("="*60)
    
    test_dir = Path(__file__).parent / "fail_data"
    files = [
        test_dir / "no_front_matter.md",
        test_dir / "missing_local_database.md",
        test_dir / "no_test_section.md"
    ]
    
    # Act
    groups = group_files_by_config(files)
    
    # Assert
    assert len(groups) == 0, \
        f"Should have no groups for files without config, got {len(groups)}"
    
    print(f"  ✓ All files without config properly skipped")
    print(f"  ✓ Groups: {len(groups)}")


def test_output_json_format():
    """Test JSON output format."""
    print("\n" + "="*60)
    print("TEST: JSON output format")
    print("="*60)
    
    # Arrange
    groups = {
        ('json-server@0.17.4', 'localhost:3000', 'api/db.json'): ['file1.md', 'file2.md']
    }
    
    # Act
    result = output_json(groups)
    
    # Assert
    data = json.loads(result)  # Should parse without error
    assert 'groups' in data, "JSON should have 'groups' key"
    assert len(data['groups']) == 1, "Should have 1 group"
    assert data['groups'][0]['test_apps'] == 'json-server@0.17.4'
    assert data['groups'][0]['server_url'] == 'localhost:3000'
    assert data['groups'][0]['local_database'] == 'api/db.json'
    assert data['groups'][0]['files'] == ['file1.md', 'file2.md']
    
    print(f"  ✓ Valid JSON output")
    print(f"  ✓ Contains all required fields")


def test_output_json_empty_groups():
    """Test JSON output with no groups."""
    print("\n" + "="*60)
    print("TEST: JSON output with empty groups")
    print("="*60)
    
    # Arrange
    groups = {}
    
    # Act
    result = output_json(groups)
    
    # Assert
    data = json.loads(result)
    assert 'groups' in data, "JSON should have 'groups' key"
    assert len(data['groups']) == 0, "Should have empty groups array"
    
    print(f"  ✓ Valid JSON for empty groups")


def test_output_shell_format():
    """Test shell output format."""
    print("\n" + "="*60)
    print("TEST: Shell output format")
    print("="*60)
    
    # Arrange
    groups = {
        ('json-server@0.17.4', 'localhost:3000', 'api/db.json'): ['file1.md', 'file2.md']
    }
    
    # Act
    result = output_shell(groups)
    
    # Assert
    assert 'GROUP_1_TEST_APPS=' in result, "Should have GROUP_1_TEST_APPS variable"
    assert 'GROUP_1_SERVER_URL=' in result, "Should have GROUP_1_SERVER_URL variable"
    assert 'GROUP_1_LOCAL_DATABASE=' in result, "Should have GROUP_1_LOCAL_DATABASE variable"
    assert 'GROUP_1_FILES=' in result, "Should have GROUP_1_FILES variable"
    assert 'GROUP_COUNT=1' in result, "Should have GROUP_COUNT variable"
    assert 'json-server@0.17.4' in result, "Should contain test_apps value"
    assert 'file1.md file2.md' in result, "Should contain files separated by space"
    
    print(f"  ✓ Valid shell output format")
    print(f"  ✓ All required variables present")


def test_output_shell_multiple_groups():
    """Test shell output with multiple groups."""
    print("\n" + "="*60)
    print("TEST: Shell output with multiple groups")
    print("="*60)
    
    # Arrange
    groups = {
        ('app1', 'url1', 'db1'): ['file1.md'],
        ('app2', 'url2', 'db2'): ['file2.md']
    }
    
    # Act
    result = output_shell(groups)
    
    # Assert
    assert 'GROUP_1_' in result, "Should have GROUP_1_ variables"
    assert 'GROUP_2_' in result, "Should have GROUP_2_ variables"
    assert 'GROUP_COUNT=2' in result, "Should have correct count"
    
    print(f"  ✓ Multiple groups formatted correctly")


def test_output_shell_empty_groups():
    """Test shell output with no groups."""
    print("\n" + "="*60)
    print("TEST: Shell output with empty groups")
    print("="*60)
    
    # Arrange
    groups = {}
    
    # Act
    result = output_shell(groups)
    
    # Assert
    assert 'GROUP_COUNT=0' in result, "Should have GROUP_COUNT=0"
    
    print(f"  ✓ Empty groups handled correctly")


def test_cli_json_output():
    """Test CLI with JSON output."""
    print("\n" + "="*60)
    print("TEST: CLI with --output json")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    script = Path(__file__).parent.parent / "get-test-configs.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), '--output', 'json', str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, \
        f"Should exit 0, got {result.returncode}"
    
    data = json.loads(result.stdout)  # Should parse
    assert 'groups' in data, "Should have groups in output"
    
    print(f"  ✓ CLI produces valid JSON")
    print(f"  ✓ Exit code: 0")


def test_cli_shell_output():
    """Test CLI with shell output."""
    print("\n" + "="*60)
    print("TEST: CLI with --output shell")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    script = Path(__file__).parent.parent / "get-test-configs.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), '--output', 'shell', str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, \
        f"Should exit 0, got {result.returncode}"
    assert 'GROUP_' in result.stdout, "Should have GROUP_ variables"
    assert 'GROUP_COUNT=' in result.stdout, "Should have GROUP_COUNT"
    
    print(f"  ✓ CLI produces valid shell output")
    print(f"  ✓ Exit code: 0")


def test_cli_missing_output_flag():
    """Test CLI without --output flag shows error."""
    print("\n" + "="*60)
    print("TEST: CLI without --output flag")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    script = Path(__file__).parent.parent / "get-test-configs.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode != 0, "Should exit with error"
    assert 'required' in result.stderr.lower() or 'error' in result.stderr.lower(), \
        "Should show error about missing flag"
    
    print(f"  ✓ Missing --output flag causes error")


def test_cli_invalid_output_format():
    """Test CLI with invalid --output value."""
    print("\n" + "="*60)
    print("TEST: CLI with invalid --output value")
    print("="*60)
    
    test_dir = Path(__file__).parent / "test_data"
    test_file = test_dir / "valid_complete.md"
    script = Path(__file__).parent.parent / "get-test-configs.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), '--output', 'xml', str(test_file)],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode != 0, "Should exit with error"
    assert 'invalid choice' in result.stderr.lower() or 'error' in result.stderr.lower(), \
        "Should show error about invalid choice"
    
    print(f"  ✓ Invalid --output value causes error")


def test_cli_no_files():
    """Test CLI without file arguments."""
    print("\n" + "="*60)
    print("TEST: CLI without file arguments")
    print("="*60)
    
    script = Path(__file__).parent.parent / "get-test-configs.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), '--output', 'json'],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode != 0, "Should exit with error when no files provided"
    
    print(f"  ✓ No files causes error")


def test_cli_help():
    """Test CLI --help flag."""
    print("\n" + "="*60)
    print("TEST: CLI --help flag")
    print("="*60)
    
    script = Path(__file__).parent.parent / "get-test-configs.py"
    
    # Act
    result = subprocess.run(
        [sys.executable, str(script), '--help'],
        capture_output=True,
        text=True
    )
    
    # Assert
    assert result.returncode == 0, "Should exit 0 for --help"
    assert 'usage:' in result.stdout.lower() or 'Usage:' in result.stdout, \
        "Should show usage information"
    assert '--output' in result.stdout, "Should document --output flag"
    
    print(f"  ✓ Help flag works correctly")


def test_shared_utilities_integration():
    """Test that script uses shared utilities correctly."""
    print("\n" + "="*60)
    print("TEST: Shared utilities integration")
    print("="*60)
    
    # Verify the module uses shared utilities
    # Check that functions exist in the module
    assert hasattr(get_configs_module, 'read_markdown_file'), \
        "Module should import read_markdown_file"
    assert hasattr(get_configs_module, 'parse_front_matter'), \
        "Module should import parse_front_matter"
    assert hasattr(get_configs_module, 'get_server_database_key'), \
        "Module should import get_server_database_key"
    
    print(f"  ✓ Uses read_markdown_file from doc_test_utils")
    print(f"  ✓ Uses parse_front_matter from doc_test_utils")
    print(f"  ✓ Uses get_server_database_key from doc_test_utils")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR get-test-configs.py")
    print("="*70)
    
    tests = [
        test_group_single_file,
        test_group_same_config,
        test_group_different_configs,
        test_group_mixed_valid_invalid,
        test_files_without_config_skipped,
        test_output_json_format,
        test_output_json_empty_groups,
        test_output_shell_format,
        test_output_shell_multiple_groups,
        test_output_shell_empty_groups,
        test_cli_json_output,
        test_cli_shell_output,
        test_cli_missing_output_flag,
        test_cli_invalid_output_format,
        test_cli_no_files,
        test_cli_help,
        test_shared_utilities_integration,
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
