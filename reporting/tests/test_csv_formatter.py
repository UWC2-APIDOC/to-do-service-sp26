#!/usr/bin/env python3
"""
Tests for csv_formatter module.

Covers:
- Schema loading (valid, invalid, missing)
- Nested value extraction
- Value formatting (timestamps, integers, booleans)
- Array expansion (denormalization)
- CSV generation
- File saving

Run with:
    python3 test_csv_formatter.py
    pytest test_csv_formatter.py -v
"""

import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from csv_formatter import (
    load_schema,
    _get_nested_value,
    _format_value,
    _expand_array,
    format_as_csv,
    save_csv
)


def test_load_schema_valid():
    """Test loading a valid schema file."""
    print("\n" + "="*60)
    print("TEST: load_schema() with valid YAML")
    print("="*60)
    
    # Create temporary schema file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
test_schema:
  description: "Test schema"
  mode: denormalized
  format: csv
  fields:
    - source: id
      column: run_id
      type: integer
    - source: name
      column: workflow
      type: string
""")
        temp_path = Path(f.name)
    
    try:
        schema = load_schema(temp_path)
        
        assert schema is not None, "Should load schema"
        assert schema['description'] == "Test schema", "Should parse description"
        assert schema['mode'] == 'denormalized', "Should parse mode"
        assert len(schema['fields']) == 2, "Should have 2 fields"
        assert schema['fields'][0]['source'] == 'id', "Should parse field source"
        
        print("  ✓ Valid schema loaded correctly")
    finally:
        temp_path.unlink()


def test_load_schema_missing():
    """Test loading non-existent schema file."""
    print("\n" + "="*60)
    print("TEST: load_schema() with missing file")
    print("="*60)
    
    schema = load_schema(Path('/nonexistent/schema.yaml'))
    
    assert schema is None, "Should return None for missing file"
    print("  ✓ Returns None for missing file")


def test_load_schema_invalid_yaml():
    """Test loading schema with invalid YAML."""
    print("\n" + "="*60)
    print("TEST: load_schema() with invalid YAML")
    print("="*60)
    
    # Create temporary file with invalid YAML
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: syntax: [unclosed")
        temp_path = Path(f.name)
    
    try:
        schema = load_schema(temp_path)
        
        assert schema is None, "Should return None for invalid YAML"
        print("  ✓ Returns None for invalid YAML")
    finally:
        temp_path.unlink()


def test_get_nested_value():
    """Test nested value extraction."""
    print("\n" + "="*60)
    print("TEST: _get_nested_value()")
    print("="*60)
    
    data = {
        'id': 123,
        'actor': {
            'login': 'user1',
            'profile': {
                'email': 'test@example.com'
            }
        }
    }
    
    # Simple field
    assert _get_nested_value(data, 'id') == 123, "Should get simple field"
    
    # Nested field
    assert _get_nested_value(data, 'actor.login') == 'user1', "Should get nested field"
    
    # Deeply nested
    assert _get_nested_value(data, 'actor.profile.email') == 'test@example.com', \
        "Should get deeply nested field"
    
    # Non-existent field
    assert _get_nested_value(data, 'nonexistent') is None, "Should return None for missing field"
    
    # Non-existent nested field
    assert _get_nested_value(data, 'actor.nonexistent') is None, \
        "Should return None for missing nested field"
    
    print("  ✓ Nested value extraction works correctly")


def test_format_value_types():
    """Test value formatting for different types."""
    print("\n" + "="*60)
    print("TEST: _format_value() type conversion")
    print("="*60)
    
    # Integer
    assert _format_value(123, 'integer') == '123', "Should format integer"
    assert _format_value('456', 'integer') == '456', "Should parse string to integer"
    assert _format_value(None, 'integer') == '', "Should handle None integer"
    assert _format_value('invalid', 'integer') == '', "Should handle invalid integer"
    print("  ✓ Integer formatting works")
    
    # Float
    assert _format_value(123.45, 'float') == '123.45', "Should format float"
    assert _format_value('67.89', 'float') == '67.89', "Should parse string to float"
    assert _format_value(None, 'float') == '', "Should handle None float"
    print("  ✓ Float formatting works")
    
    # Boolean
    assert _format_value(True, 'boolean') == 'true', "Should format True"
    assert _format_value(False, 'boolean') == 'false', "Should format False"
    assert _format_value(None, 'boolean') == '', "Should handle None boolean"
    print("  ✓ Boolean formatting works")
    
    # String
    assert _format_value('test', 'string') == 'test', "Should format string"
    assert _format_value(123, 'string') == '123', "Should convert to string"
    assert _format_value(None, 'string') == '', "Should handle None string"
    print("  ✓ String formatting works")
    
    # URL
    assert _format_value('https://example.com', 'url') == 'https://example.com', \
        "Should format URL"
    assert _format_value(None, 'url') == '', "Should handle None URL"
    print("  ✓ URL formatting works")


def test_format_value_timestamp():
    """Test timestamp formatting."""
    print("\n" + "="*60)
    print("TEST: _format_value() timestamp formatting")
    print("="*60)
    
    # ISO timestamp with Z
    iso_timestamp = '2024-12-16T10:30:00Z'
    formatted = _format_value(iso_timestamp, 'timestamp', '%Y-%m-%d %H:%M:%S')
    assert formatted == '2024-12-16 10:30:00', f"Should format timestamp, got {formatted}"
    print("  ✓ ISO timestamp formatted correctly")
    
    # Timestamp without format (passthrough)
    result = _format_value(iso_timestamp, 'timestamp')
    assert result == iso_timestamp, "Should return original if no format specified"
    print("  ✓ Timestamp passthrough works")
    
    # None timestamp
    assert _format_value(None, 'timestamp') == '', "Should handle None timestamp"
    print("  ✓ None timestamp handled")
    
    # Invalid timestamp
    result = _format_value('not-a-date', 'timestamp', '%Y-%m-%d')
    assert result == 'not-a-date', "Should return original for invalid timestamp"
    print("  ✓ Invalid timestamp handled gracefully")


def test_expand_array():
    """Test array expansion (denormalization)."""
    print("\n" + "="*60)
    print("TEST: _expand_array()")
    print("="*60)
    
    data = {
        'id': 123,
        'name': 'Pull request Validation',
        'jobs': [
            {'id': 456, 'name': 'Lint'},
            {'id': 457, 'name': 'Test'}
        ]
    }
    
    expanded = _expand_array(data, 'jobs')
    
    assert len(expanded) == 2, "Should create 2 rows from 2 jobs"
    assert expanded[0]['id'] == 123, "Should preserve parent data"
    assert expanded[0]['jobs']['id'] == 456, "Should include first job"
    assert expanded[1]['jobs']['id'] == 457, "Should include second job"
    print("  ✓ Array expansion works correctly")
    
    # Test with no array field
    data_no_array = {'id': 123, 'name': 'test'}
    expanded = _expand_array(data_no_array, 'jobs')
    
    assert len(expanded) == 1, "Should return single row if no array"
    assert expanded[0]['id'] == 123, "Should preserve original data"
    print("  ✓ Handles missing array field")


def test_format_as_csv_simple():
    """Test CSV generation with simple schema."""
    print("\n" + "="*60)
    print("TEST: format_as_csv() simple schema")
    print("="*60)
    
    data = {
        'id': 123,
        'name': 'Test Workflow',
        'status': 'completed'
    }
    
    schema = {
        'mode': 'denormalized',
        'fields': [
            {'source': 'id', 'column': 'run_id', 'type': 'integer'},
            {'source': 'name', 'column': 'workflow', 'type': 'string'},
            {'source': 'status', 'column': 'status', 'type': 'string'}
        ]
    }
    
    csv_output = format_as_csv(data, schema)
    
    lines = csv_output.strip().split('\r\n')  # CSV uses \r\n
    assert len(lines) == 2, "Should have header + 1 data row"
    assert lines[0] == 'run_id,workflow,status', "Should have correct header"
    assert lines[1] == '123,Test Workflow,completed', "Should have correct data"
    print("  ✓ Simple CSV generation works")


def test_format_as_csv_with_expansion():
    """Test CSV generation with array expansion."""
    print("\n" + "="*60)
    print("TEST: format_as_csv() with denormalization")
    print("="*60)
    
    data = {
        'id': 123,
        'name': 'Pull request Validation',
        'jobs': [
            {'id': 456, 'name': 'Lint', 'status': 'success'},
            {'id': 457, 'name': 'Test', 'status': 'success'}
        ]
    }
    
    schema = {
        'mode': 'denormalized',
        'expand': 'jobs',
        'fields': [
            {'source': 'id', 'column': 'run_id', 'type': 'integer'},
            {'source': 'jobs.id', 'column': 'job_id', 'type': 'integer'},
            {'source': 'jobs.name', 'column': 'job_name', 'type': 'string'}
        ]
    }
    
    csv_output = format_as_csv(data, schema)
    
    lines = csv_output.strip().split('\r\n')  # CSV uses \r\n
    assert len(lines) == 3, "Should have header + 2 data rows (one per job)"
    assert lines[0] == 'run_id,job_id,job_name', "Should have correct header"
    assert '123' in lines[1], "Should repeat run_id in first row"
    assert '456' in lines[1], "Should have first job ID"
    assert '123' in lines[2], "Should repeat run_id in second row"
    assert '457' in lines[2], "Should have second job ID"
    print("  ✓ Denormalized CSV generation works")


def test_format_as_csv_list_input():
    """Test CSV generation with list of dicts."""
    print("\n" + "="*60)
    print("TEST: format_as_csv() with list input")
    print("="*60)
    
    data = [
        {'id': 123, 'name': 'first'},
        {'id': 456, 'name': 'second'}
    ]
    
    schema = {
        'mode': 'denormalized',
        'fields': [
            {'source': 'id', 'column': 'id', 'type': 'integer'},
            {'source': 'name', 'column': 'name', 'type': 'string'}
        ]
    }
    
    csv_output = format_as_csv(data, schema)
    
    lines = csv_output.strip().split('\r\n')  # CSV uses \r\n
    assert len(lines) == 3, "Should have header + 2 data rows"
    print("  ✓ List input works correctly")


def test_save_csv_new_file():
    """Test saving CSV to new file."""
    print("\n" + "="*60)
    print("TEST: save_csv() new file")
    print("="*60)
    
    csv_content = "id,name\n123,test\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_path = Path(f.name)
    
    # Delete it so we can test creating new
    temp_path.unlink()
    
    try:
        result = save_csv(csv_content, temp_path, append=False)
        
        assert result is True, "Should return True on success"
        assert temp_path.exists(), "Should create file"
        
        content = temp_path.read_text()
        assert content == csv_content, "Should write correct content"
        print("  ✓ New file created correctly")
    finally:
        if temp_path.exists():
            temp_path.unlink()


def test_save_csv_append_mode():
    """Test appending to existing CSV file."""
    print("\n" + "="*60)
    print("TEST: save_csv() append mode")
    print("="*60)
    
    # Create initial file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,name\n123,first\n")
        temp_path = Path(f.name)
    
    try:
        # Append new data (with header that should be skipped)
        new_content = "id,name\n456,second\n"
        result = save_csv(new_content, temp_path, append=True)
        
        assert result is True, "Should return True on success"
        
        content = temp_path.read_text()
        lines = content.strip().split('\n')
        
        assert len(lines) == 3, f"Should have 3 lines (header + 2 data), got {len(lines)}"
        assert lines[0] == 'id,name', "Should keep original header"
        assert lines[1] == '123,first', "Should keep original data"
        assert lines[2] == '456,second', "Should append new data without duplicate header"
        print("  ✓ Append mode works correctly")
    finally:
        temp_path.unlink()


def test_save_csv_error_handling():
    """Test error handling in save_csv."""
    print("\n" + "="*60)
    print("TEST: save_csv() error handling")
    print("="*60)
    
    # Try to write to invalid path
    result = save_csv("test", Path('/nonexistent/directory/file.csv'), append=False)
    
    assert result is False, "Should return False on error"
    print("  ✓ Error handling works")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR csv_formatter.py")
    print("="*70)
    
    tests = [
        test_load_schema_valid,
        test_load_schema_missing,
        test_load_schema_invalid_yaml,
        test_get_nested_value,
        test_format_value_types,
        test_format_value_timestamp,
        test_expand_array,
        test_format_as_csv_simple,
        test_format_as_csv_with_expansion,
        test_format_as_csv_list_input,
        test_save_csv_new_file,
        test_save_csv_append_mode,
        test_save_csv_error_handling,
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
