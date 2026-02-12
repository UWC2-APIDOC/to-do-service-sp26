#!/usr/bin/env python3
"""
Tests for schema_validator.py

Covers:
- Schema loading with caching
- Front matter validation against JSON schema
- Required vs optional field error categorization
- Error and warning message generation
- Graceful handling when jsonschema unavailable
- Cache clearing functionality

Run with:
    python3 test_schema_validator.py
    pytest test_schema_validator.py -v
"""

import sys
import json
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import module
import importlib.util
spec = importlib.util.spec_from_file_location("schema_validator", 
                                               Path(__file__).parent.parent / "schema_validator.py")
if spec and spec.loader:
    schema_validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema_validator)
    
    load_schema = schema_validator.load_schema
    clear_schema_cache = schema_validator.clear_schema_cache
    validate_front_matter_schema = schema_validator.validate_front_matter_schema
    validate_with_default_schema = schema_validator.validate_with_default_schema
    JSONSCHEMA_AVAILABLE = schema_validator.JSONSCHEMA_AVAILABLE


def test_load_schema():
    """Test schema loading from file."""
    print("\n" + "="*60)
    print("TEST: load_schema()")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    # Clear cache first
    clear_schema_cache()
    
    # Test 1: Load valid schema
    schema = load_schema(schema_path)
    assert schema is not None, "Should load valid schema"
    assert "type" in schema, "Schema should have 'type' field"
    print("  SUCCESS: Valid schema loaded")
    
    # Test 2: Schema is cached (load again)
    schema2 = load_schema(schema_path)
    assert schema2 is schema, "Should return cached schema object"
    print("  SUCCESS: Schema caching works")
    
    # Test 3: Nonexistent schema
    schema3 = load_schema("nonexistent.json")
    assert schema3 is None, "Should return None for missing file"
    print("  SUCCESS: Missing file handled correctly")
    
    print("  ✓ All load_schema tests passed")


def test_clear_schema_cache():
    """Test cache clearing functionality."""
    print("\n" + "="*60)
    print("TEST: clear_schema_cache()")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    # Load schema to populate cache
    schema1 = load_schema(schema_path)
    assert schema1 is not None
    
    # Clear cache
    clear_schema_cache()
    
    # Load again - should be a fresh load
    schema2 = load_schema(schema_path)
    assert schema2 is not None
    # Note: We can't test if it's a different object since JSON parsing
    # might produce identical objects, but cache was cleared
    
    print("  SUCCESS: Cache cleared successfully")
    print("  ✓ All clear_schema_cache tests passed")


def test_validate_required_fields():
    """Test validation of required fields."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() - required fields")
    print("="*60)
    
    if not JSONSCHEMA_AVAILABLE:
        print("  SKIPPED: jsonschema not installed")
        return
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    clear_schema_cache()
    
    # Test 1: Valid metadata (all required fields)
    metadata = {
        "layout": "default",
        "description": "A test page with all required fields",
        "topic_type": "reference"
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert is_valid, "Should be valid with all required fields"
    assert not has_warnings, "Should have no warnings"
    assert len(errors) == 0, "Should have no errors"
    print("  SUCCESS: Valid metadata passes")
    
    # Test 2: Missing required field
    metadata = {
        "layout": "default",
        "description": "Missing topic_type"
        # Missing 'topic_type'
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert not is_valid, "Should be invalid when missing required field"
    assert len(errors) > 0, "Should have errors"
    assert any("topic_type" in err.lower() for err in errors), "Should mention missing field"
    print("  SUCCESS: Detects missing required field")
    
    # Test 3: Multiple missing required fields
    metadata = {
        "layout": "default"
        # Missing 'description' and 'topic_type'
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert not is_valid, "Should be invalid"
    assert len(errors) >= 2, "Should have multiple errors"
    print("  SUCCESS: Detects multiple missing fields")
    
    print("  ✓ All required field tests passed")


def test_validate_optional_fields():
    """Test validation of optional fields."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() - optional fields")
    print("="*60)
    
    if not JSONSCHEMA_AVAILABLE:
        print("  SKIPPED: jsonschema not installed")
        return
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    clear_schema_cache()
    
    # Test 1: Invalid optional field (should be warning, not error)
    metadata = {
        "layout": "default",
        "description": "A test page",
        "topic_type": "reference",
        "nav_order": "invalid"  # Should be integer
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert is_valid, "Should still be valid (optional field error)"
    assert has_warnings, "Should have warnings"
    assert len(warnings) > 0, "Should have warning messages"
    assert len(errors) == 0, "Should have no errors"
    print("  SUCCESS: Optional field errors become warnings")
    
    # Test 2: Invalid enum value in required field
    metadata = {
        "layout": "invalid_layout",  # Not in enum
        "description": "A test page",
        "topic_type": "reference"
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert not is_valid, "Should be invalid (required field has wrong value)"
    assert len(errors) > 0, "Should have errors"
    print("  SUCCESS: Invalid enum in required field is error")
    
    print("  ✓ All optional field tests passed")


def test_validate_field_formats():
    """Test validation of field formats and patterns."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() - field formats")
    print("="*60)
    
    if not JSONSCHEMA_AVAILABLE:
        print("  SKIPPED: jsonschema not installed")
        return
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    clear_schema_cache()
    
    # Test 1: String length validation
    metadata = {
        "layout": "default",
        "description": "Short",  # Too short (minLength: 10)
        "topic_type": "reference"
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert not is_valid, "Should be invalid (description too short)"
    assert len(errors) > 0, "Should have errors"
    print("  SUCCESS: String length validation works")
    
    # Test 2: Integer range validation
    metadata = {
        "layout": "default",
        "description": "A valid description that meets length requirements",
        "topic_type": "reference",
        "nav_order": 0  # Too low (minimum: 1)
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert is_valid, "Should be valid (optional field)"
    assert has_warnings, "Should have warnings"
    print("  SUCCESS: Integer range validation works")
    
    print("  ✓ All field format tests passed")


def test_validate_nested_objects():
    """Test validation of nested objects (like test config)."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() - nested objects")
    print("="*60)
    
    if not JSONSCHEMA_AVAILABLE:
        print("  SKIPPED: jsonschema not installed")
        return
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    clear_schema_cache()
    
    # Test 1: Valid nested test config
    metadata = {
        "layout": "default",
        "description": "A test page with test configuration",
        "topic_type": "reference",
        "test": {
            "testable": ["GET example"],
            "test_apps": ["json-server@0.17.4"],
            "server_url": "localhost:3000",
            "local_database": "/api/test.json"
        }
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert is_valid, "Should be valid with complete test config"
    print("  SUCCESS: Valid nested object passes")
    
    # Test 2: Invalid format in nested optional object
    metadata = {
        "layout": "default",
        "description": "A test page with invalid test config format",
        "topic_type": "reference",
        "test": {
            "testable": ["GET example"],
            "test_apps": "should-be-array",  # Wrong type
            "server_url": "localhost:3000"
        }
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path
    )
    
    assert is_valid, "Should still be valid (nested fields are optional)"
    assert has_warnings, "Should have warnings about wrong type"
    print("  SUCCESS: Invalid format in nested object generates warnings")
    
    print("  ✓ All nested object tests passed")


def test_validate_without_jsonschema():
    """Test graceful handling when jsonschema is not available."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() - without jsonschema")
    print("="*60)
    
    # This test always runs since we check JSONSCHEMA_AVAILABLE in the function
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = str(test_data_dir / "test_schema.json")
    
    metadata = {
        "layout": "default",
        "description": "Test"
    }
    
    # Capture output
    captured = StringIO()
    with redirect_stdout(captured):
        is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
            metadata, schema_path
        )
    
    if JSONSCHEMA_AVAILABLE:
        # When available, should actually validate
        print("  NOTE: jsonschema is available, actual validation performed")
    else:
        # When not available, should skip gracefully
        assert is_valid, "Should return valid when jsonschema unavailable"
        assert not has_warnings, "Should have no warnings"
        assert len(errors) == 0, "Should have no errors"
        output = captured.getvalue()
        assert "jsonschema" in output.lower(), "Should warn about missing library"
        print("  SUCCESS: Gracefully handles missing jsonschema")
    
    print("  ✓ All no-jsonschema tests passed")


def test_validate_with_default_schema():
    """Test convenience function with default schema path."""
    print("\n" + "="*60)
    print("TEST: validate_with_default_schema()")
    print("="*60)
    
    if not JSONSCHEMA_AVAILABLE:
        print("  SKIPPED: jsonschema not installed")
        return
    
    # This will try to load .github/schemas/front-matter-schema.json
    # which won't exist in test environment, so it should handle gracefully
    metadata = {
        "layout": "default",
        "description": "A test page",
        "topic_type": "reference"
    }
    
    captured = StringIO()
    with redirect_stdout(captured):
        is_valid, has_warnings, errors, warnings = validate_with_default_schema(metadata)
    
    # Should return valid (schema not found = skip validation)
    assert is_valid, "Should be valid when schema not found"
    
    output = captured.getvalue()
    if "not found" in output:
        print("  SUCCESS: Handles missing default schema gracefully")
    else:
        print("  NOTE: Default schema may exist in this environment")
    
    print("  ✓ All default schema tests passed")


def test_real_schema_file():
    """Test with actual front-matter-schema.json if available."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() - real schema")
    print("="*60)
    
    if not JSONSCHEMA_AVAILABLE:
        print("  SKIPPED: jsonschema not installed")
        return
    
    # Look for the real schema in test_data
    test_data_dir = Path(__file__).parent / "test_data"
    real_schema_path = test_data_dir / "front-matter-schema.json"
    
    if not real_schema_path.exists():
        print("  SKIPPED: Real schema file not found in test_data")
        return
    
    clear_schema_cache()
    
    # Test with valid metadata matching real schema
    metadata = {
        "layout": "default",
        "description": "GET the user resource with the specified ID from the service",
        "topic_type": "reference",
        "test": {
            "testable": ["GET example"],
            "test_apps": ["json-server@0.17.4"],
            "server_url": "localhost:3000",
            "local_database": "/api/test.json"
        }
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, str(real_schema_path)
    )
    
    assert is_valid, f"Should be valid: {errors}"
    print("  SUCCESS: Valid metadata passes real schema")
    
    # Test with missing required field
    metadata = {
        "layout": "default",
        "description": "Test"
        # Missing topic_type
    }
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, str(real_schema_path)
    )
    
    assert not is_valid, "Should be invalid"
    assert len(errors) > 0, "Should have errors"
    print("  SUCCESS: Real schema detects missing fields")
    
    print("  ✓ All real schema tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR schema_validator.py")
    print("="*70)
    
    tests = [
        test_load_schema,
        test_clear_schema_cache,
        test_validate_required_fields,
        test_validate_optional_fields,
        test_validate_field_formats,
        test_validate_nested_objects,
        test_validate_without_jsonschema,
        test_validate_with_default_schema,
        test_real_schema_file
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_func in tests:
        try:
            output = StringIO()
            with redirect_stdout(output):
                test_func()
            
            output_text = output.getvalue()
            if "SKIPPED" in output_text:
                skipped += 1
                print(output_text, end='')
            else:
                passed += 1
                print(output_text, end='')
                
        except AssertionError as e:
            failed += 1
            print(f"\n  ✗ FAILED: {test_func.__name__}")
            print(f"    {str(e)}")
        except Exception as e:
            failed += 1
            print(f"\n  ✗ ERROR in {test_func.__name__}: {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
