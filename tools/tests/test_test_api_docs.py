#!/usr/bin/env python3
"""
Tests for test-api-docs.py

Covers:
- Parse testable entries with status codes
- Extract curl commands from markdown
- Extract expected JSON responses
- JSON object comparison
- Front matter validation (when jsonschema available)

Note: These are unit tests. Integration tests requiring a running
      json-server would be separate.

Run with:
    python3 test_test_api_docs.py
    pytest test_test_api_docs.py -v
"""

import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the script module (uses hyphens, needs importlib)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "test_api_docs",
    Path(__file__).parent.parent / "test-api-docs.py"
)
test_api_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_api_docs)

# Import the functions we're testing
parse_testable_entry = test_api_docs.parse_testable_entry
extract_curl_command = test_api_docs.extract_curl_command
extract_expected_response = test_api_docs.extract_expected_response
compare_json_objects = test_api_docs.compare_json_objects
# Import schema validator directly
import importlib.util
schema_validator_spec = importlib.util.spec_from_file_location("schema_validator", 
                                                   Path(__file__).parent.parent / "schema_validator.py")
if schema_validator_spec and schema_validator_spec.loader:
    schema_validator = importlib.util.module_from_spec(schema_validator_spec)
    schema_validator_spec.loader.exec_module(schema_validator)
    validate_front_matter_schema = schema_validator.validate_front_matter_schema
    JSONSCHEMA_AVAILABLE = schema_validator.JSONSCHEMA_AVAILABLE


def test_parse_testable_entry():
    """Test parsing of testable entries with status codes."""
    print("\n" + "="*60)
    print("TEST: parse_testable_entry()")
    print("="*60)

    test_cases = [
        # (input, expected_output, description)
        ("GET example", ("GET example", [200]), "Simple example, default status"),
        ("POST example / 201", ("POST example", [201]), "Single status code"),
        ("PUT example / 200,204", ("PUT example", [200, 204]), "Multiple status codes"),
        ("DELETE example / 204", ("DELETE example", [204]), "DELETE with 204"),
        ("", (None, None), "Empty string"),
        ("   ", (None, None), "Whitespace only"),
        ("Example / ", (None, None), "Slash but no codes"),
        ("Example / abc", (None, None), "Non-numeric code"),
        ("Example / 200,abc", (None, None), "Mixed valid and invalid codes"),
        ("Example / 200,", (None, None), "Trailing comma"),
        ("Example / ,200", (None, None), "Leading comma"),
        ("/ 200", (None, None), "No example name"),
        ("Example / 200 / 201", ("Example", [200]), "Extra slash (takes first part)"),
        ("PATCH example / 200, 201, 204", ("PATCH example", [200, 201, 204]), "Multiple with spaces"),
    ]
    
    passed = 0
    failed = 0
    
    for input_str, expected, description in test_cases:
        result = parse_testable_entry(input_str)
        
        if result == expected:
            print(f"✓ PASS: {description}")
            print(f"  Input: '{input_str}'")
            print(f"  Result: {result}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Input: '{input_str}'")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
            failed += 1
        print()
    
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All tests passed!")
    else:
        print(f"✗ {failed} test(s) failed")
    # end of test_parse_testable_entry


def test_extract_curl_command():
    """Test extraction of curl commands from markdown."""
    print("\n" + "="*60)
    print("TEST: extract_curl_command()")
    print("="*60)
    
    # Use empty string as the default for server URL in tests
    server_url = ""

    # Test 1: Basic curl command
    content = """
# API Doc

### GET example request

```bash
curl http://localhost:3000/users
```
"""
    cmd = extract_curl_command(content, server_url, "GET example")
    assert cmd is not None, "Should find curl command"
    # extract_curl_command inserts -i in commands that don't have it
    assert "curl -i http://localhost:3000/users" in cmd, f"Unexpected command: {cmd}"
    print("  SUCCESS: Basic curl command extracted")
    
    # Test 2: Curl with backticks in heading
    content = """
### `GET` example request

```bash
curl http://localhost:3000/users
```
"""
    cmd = extract_curl_command(content, server_url, "GET example")
    assert cmd is not None, "Should find curl command with backticks in heading"
    print("  SUCCESS: Curl command with backticks extracted")
    
    # Test 3: Multi-line curl command
    content = """
### POST example request

```bash
curl -X POST http://localhost:3000/users \\
  -H "Content-Type: application/json" \\
  -d '{"name":"test"}'
```
"""
    cmd = extract_curl_command(content, server_url, "POST example")
    assert cmd is not None, "Should find multi-line curl command"
    # extract_curl_command inserts -i in commands that don't have it
    assert "curl -i -X POST" in cmd, "Should contain POST method"
    assert "-H" in cmd, "Should contain header flag"
    print("  SUCCESS: Multi-line curl command extracted")
    
    # Test 4: Not found
    content = """
# No curl here
"""
    cmd = extract_curl_command(content, server_url, "Missing example")
    assert cmd is None, "Should return None when not found"
    print("  SUCCESS: Returns None when command not found")
    
    # Test 5: Not in code block
    content = """
## Example request

Just text: curl http://localhost:3000/users

Not in a code block.
"""
    cmd = extract_curl_command(content, server_url, "Example")
    assert cmd is None, "Should return None when curl not in code block"
    print("  SUCCESS: Ignores curl commands outside code blocks")

    # Test 6: Test server_url substitution
    server_url = "localhost:3000"
    content = """
### `GET` example request

```bash
curl http://{server_url}/users
```
"""
    cmd = extract_curl_command(content, server_url, "GET example")
    print(f"Extracted command: {cmd}")
    assert cmd is not None, "Should find curl command"
    # extract_curl_command inserts -i in commands that don't have it
    assert f"curl -i http://{server_url}/users" in cmd, f"Unexpected command: {cmd}"
    assert server_url in cmd, "Should return the command with server_url substituted"
    print("  SUCCESS: {server_url} substitution works correctly.")
    
    print("  ✓ All extract_curl_command tests passed")


def test_extract_expected_response():
    """Test extraction of expected JSON responses."""
    print("\n" + "="*60)
    print("TEST: extract_expected_response()")
    print("="*60)
    
    # Test 1: Simple JSON object
    content = """
### GET example response

```json
{
  "id": 1,
  "name": "Test"
}
```
"""
    response = extract_expected_response(content, "GET example")
    assert response is not None, "Should extract JSON response"
    assert response["id"] == 1, "Should parse JSON correctly"
    assert response["name"] == "Test", "Should parse JSON correctly"
    print("  SUCCESS: Simple JSON object extracted")
    
    # Test 2: JSON array
    content = """
### GET all response

```json
[
  {"id": 1},
  {"id": 2}
]
```
"""
    response = extract_expected_response(content, "GET all")
    assert response is not None, "Should extract JSON array"
    assert isinstance(response, list), "Should be a list"
    assert len(response) == 2, "Should have 2 items"
    print("  SUCCESS: JSON array extracted")
    
    # Test 3: With backticks in heading
    content = """
### `POST` example response

```json
{"created": true}
```
"""
    response = extract_expected_response(content, "POST example")
    assert response is not None, "Should extract with backticks in heading"
    assert response["created"] == True, "Should parse JSON correctly"
    print("  SUCCESS: Response with backticks in heading extracted")
    
    # Test 4: Not found
    content = """
# No response here
"""
    response = extract_expected_response(content, "Missing")
    assert response is None, "Should return None when not found"
    print("  SUCCESS: Returns None when response not found")
    
    # Test 5: Invalid JSON
    content = """
## Bad response

```json
{invalid json}
```
"""
    response = extract_expected_response(content, "Bad")
    assert response is None, "Should return None for invalid JSON"
    print("  SUCCESS: Returns None for invalid JSON")
    
    print("  ✓ All extract_expected_response tests passed")


def test_compare_json_objects_equal():
    """Test JSON comparison for equal objects."""
    print("\n" + "="*60)
    print("TEST: compare_json_objects() - equal objects")
    print("="*60)
    
    # Test 1: Simple equal objects
    actual = {"id": 1, "name": "Test"}
    expected = {"id": 1, "name": "Test"}
    are_equal, diffs = compare_json_objects(actual, expected)
    assert are_equal, "Should be equal"
    assert len(diffs) == 0, "Should have no differences"
    print("  SUCCESS: Simple equal objects")
    
    # Test 2: Equal arrays
    actual = [1, 2, 3]
    expected = [1, 2, 3]
    are_equal, diffs = compare_json_objects(actual, expected)
    assert are_equal, "Should be equal"
    assert len(diffs) == 0, "Should have no differences"
    print("  SUCCESS: Equal arrays")
    
    # Test 3: Nested equal objects
    actual = {"user": {"id": 1, "profile": {"name": "Test"}}}
    expected = {"user": {"id": 1, "profile": {"name": "Test"}}}
    are_equal, diffs = compare_json_objects(actual, expected)
    assert are_equal, "Should be equal"
    assert len(diffs) == 0, "Should have no differences"
    print("  SUCCESS: Nested equal objects")
    
    # Test 4: Equal arrays of objects
    actual = [{"id": 1}, {"id": 2}]
    expected = [{"id": 1}, {"id": 2}]
    are_equal, diffs = compare_json_objects(actual, expected)
    assert are_equal, "Should be equal"
    assert len(diffs) == 0, "Should have no differences"
    print("  SUCCESS: Equal arrays of objects")
    
    print("  ✓ All equality tests passed")


def test_compare_json_objects_different():
    """Test JSON comparison for different objects."""
    print("\n" + "="*60)
    print("TEST: compare_json_objects() - different objects")
    print("="*60)
    
    # Test 1: Different values
    actual = {"id": 1, "name": "Actual"}
    expected = {"id": 1, "name": "Expected"}
    are_equal, diffs = compare_json_objects(actual, expected)
    assert not are_equal, "Should not be equal"
    assert len(diffs) > 0, "Should have differences"
    assert any("name" in d for d in diffs), "Should mention 'name' field"
    print("  SUCCESS: Detected different values")
    
    # Test 2: Missing key
    actual = {"id": 1}
    expected = {"id": 1, "name": "Test"}
    are_equal, diffs = compare_json_objects(actual, expected)
    assert not are_equal, "Should not be equal"
    assert len(diffs) > 0, "Should have differences"
    assert any("Missing" in d for d in diffs), "Should mention missing key"
    print("  SUCCESS: Detected missing key")
    
    # Test 3: Extra key
    actual = {"id": 1, "name": "Test", "extra": "value"}
    expected = {"id": 1, "name": "Test"}
    are_equal, diffs = compare_json_objects(actual, expected)
    assert not are_equal, "Should not be equal"
    assert len(diffs) > 0, "Should have differences"
    assert any("Extra" in d for d in diffs), "Should mention extra key"
    print("  SUCCESS: Detected extra key")
    
    # Test 4: Different types
    actual = {"id": "1"}  # String
    expected = {"id": 1}  # Number
    are_equal, diffs = compare_json_objects(actual, expected)
    assert not are_equal, "Should not be equal"
    assert len(diffs) > 0, "Should have differences"
    print("  SUCCESS: Detected type mismatch")
    
    # Test 5: Different array lengths
    actual = [1, 2, 3]
    expected = [1, 2]
    are_equal, diffs = compare_json_objects(actual, expected)
    assert not are_equal, "Should not be equal"
    assert len(diffs) > 0, "Should have differences"
    assert any("length" in d.lower() for d in diffs), "Should mention array length"
    print("  SUCCESS: Detected array length mismatch")
    
    # Test 6: Nested differences
    actual = {"user": {"id": 1, "name": "Wrong"}}
    expected = {"user": {"id": 1, "name": "Right"}}
    are_equal, diffs = compare_json_objects(actual, expected)
    assert not are_equal, "Should not be equal"
    assert len(diffs) > 0, "Should have differences"
    assert any("user.name" in d for d in diffs), "Should mention nested path"
    print("  SUCCESS: Detected nested differences")
    
    print("  ✓ All difference detection tests passed")


def test_validate_front_matter_with_jsonschema():
    """Test front matter validation when jsonschema is available."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() with jsonschema")
    print("="*60)
    
    # Check if jsonschema is available
    try:
        import jsonschema
        print("  jsonschema is available, running tests")
    except ImportError:
        print("  SKIPPED: jsonschema not installed")
        return
    
    test_data_dir = Path(__file__).parent / "test_data"
    schema_path = test_data_dir / "valid_front_matter_schema.json"
    
    if not schema_path.exists():
        print(f"  SKIPPED: Schema file not found at {schema_path}")
        return
    
    # Test 1: Valid front matter
    metadata = {
        "layout": "api",
        "title": "Test API",
        "test": {
            "testable": ["GET example"],
            "test_apps": ["json-server@0.17.4"]
        }
    }
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, str(schema_path), "test.md", False, "warning"
    )
    assert is_valid, "Should be valid"
    assert not has_warnings, "Should have no warnings"
    print("  SUCCESS: Valid front matter passes")
    
    # Test 2: Missing required field
    metadata = {
        "layout": "api"
        # Missing 'title'
    }
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, str(schema_path), "test.md", False, "warning"
    )
    assert not is_valid, "Should be invalid"
    assert len(errors) > 0, "Should have errors"
    print("  SUCCESS: Detects missing required field")
    
    # Test 3: Invalid enum value
    metadata = {
        "layout": "invalid",  # Not in enum
        "title": "Test"
    }
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, str(schema_path), "test.md", False, "warning"
    )
    assert not is_valid, "Should be invalid"
    assert len(errors) > 0, "Should have errors"
    print("  SUCCESS: Detects invalid enum value")
    
    print("  ✓ All validation tests passed")


def test_validate_front_matter_without_jsonschema():
    """Test front matter validation gracefully handles missing jsonschema."""
    print("\n" + "="*60)
    print("TEST: validate_front_matter_schema() without jsonschema")
    print("="*60)
    
    # Temporarily mock JSONSCHEMA_AVAILABLE as False in schema_validator
    original_value = schema_validator.JSONSCHEMA_AVAILABLE
    schema_validator.JSONSCHEMA_AVAILABLE = False
    
    try:
        metadata = {"layout": "api", "title": "Test"}
        is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
            metadata, "schema.json", "test.md", False, "warning"
        )
        
        # Should return valid even without jsonschema
        assert is_valid, "Should be valid when jsonschema not available"
        assert len(errors) == 0, "Should have no errors"
        print("  SUCCESS: Gracefully handles missing jsonschema")
    finally:
        schema_validator.JSONSCHEMA_AVAILABLE = original_value
    
    print("  ✓ Graceful degradation test passed")



def test_real_test_data_files():
    """Test with actual test data files."""
    print("\n" + "="*60)
    print("TEST: Real test data files")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    # Use empty string for server URL in tests
    # this can be modified for the individual test cases if needed
    server_url = ""  

    # Test 1: Can extract from sample file
    sample_file = test_data_dir / "api_doc_sample.md"
    if sample_file.exists():
        content = sample_file.read_text(encoding='utf-8')
        
        # Test curl extraction
        curl = extract_curl_command(content, server_url, "GET example")
        assert curl is not None, "Should extract curl from sample file"
        assert "curl" in curl.lower(), "Should contain curl command"
        print("  SUCCESS: Extracted curl from api_doc_sample.md")
        
        # Test response extraction
        response = extract_expected_response(content, "GET example")
        assert response is not None, "Should extract response from sample file"
        assert "id" in response, "Should have id field"
        print("  SUCCESS: Extracted response from api_doc_sample.md")
    
    # Test 2: Can extract from GET file
    get_file = test_data_dir / "api_doc_get.md"
    if get_file.exists():
        content = get_file.read_text(encoding='utf-8')
        
        curl = extract_curl_command(content, server_url, "GET all users")
        assert curl is not None, "Should extract curl from GET file"
        print("  SUCCESS: Extracted from api_doc_get.md")
    
    # Test 3: Can extract from POST file with status code
    post_file = test_data_dir / "api_doc_post.md"
    if post_file.exists():
        content = post_file.read_text(encoding='utf-8')
        
        curl = extract_curl_command(content, server_url, "POST example")
        assert curl is not None, "Should extract curl from POST file"
        assert "POST" in curl, "Should be POST request"
        print("  SUCCESS: Extracted from api_doc_post.md")
    
    print("  ✓ All real file tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR test-api-docs.py")
    print("="*70)
    
    tests = [
        test_parse_testable_entry,
        test_extract_curl_command,
        test_extract_expected_response,
        test_compare_json_objects_equal,
        test_compare_json_objects_different,
        test_validate_front_matter_with_jsonschema,
        test_validate_front_matter_without_jsonschema,
        test_real_test_data_files,
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
            print(f"\n  ✗ ERROR in {test_func.__name__}")
            print(f"    {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
