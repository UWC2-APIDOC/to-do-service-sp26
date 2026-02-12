#!/usr/bin/env python3
"""
Test API documentation code examples against a running json-server instance.

Usage:
    test-api-docs.py <markdown_file> [--action [LEVEL]] [--schema SCHEMA_FILE]
    
Arguments:
    markdown_file: Path to the markdown documentation file to test
    --action: Optional flag to output GitHub Actions annotations
              Optional LEVEL: all, warning (default), error
    --schema: Path to JSON schema file for front matter validation
              Default: .github/schemas/front-matter-schema.json
    
Examples:
    test-api-docs.py docs/api/users-get-all-users.md --schema .schemas/front-matter-schema.json
    test-api-docs.py docs/api/users-get-all-users.md --action --schema .schemas/front-matter-schema.json
    test-api-docs.py docs/api/users-get-all-users.md --action all --schema .schemas/front-matter-schema.json
    test-api-docs.py docs/api/users-get-all-users.md --action error --schema .schemas/front-matter-schema.json
"""

import re
import subprocess
import json
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Tuple, List, Any

from doc_test_utils import read_markdown_file, parse_front_matter_with_errors, log, HELP_URLS
from schema_validator import validate_front_matter_schema, DEFAULT_SCHEMA_PATH

# Configuration constants
CURL_TIMEOUT_SECONDS = 10
MAX_DIFFERENCES_SHOWN = 10


def parse_testable_entry(entry: str) -> Tuple[Optional[str], Optional[List[int]]]:
    """
    Parse a testable entry into example name and expected status codes.
    
    Format: "example name / status,codes"
    
    Args:
        entry: Testable entry string from front matter
        
    Returns:
        tuple: (example_name, expected_codes) or (None, None) on error
        
    Example:
        >>> parse_testable_entry("GET example")
        ('GET example', [200])
        >>> parse_testable_entry("POST example / 201")
        ('POST example', [201])
        >>> parse_testable_entry("PUT example / 200,204")
        ('PUT example', [200, 204])
    """
    try:
        parts = entry.split('/')
        example_name = parts[0].strip()
        
        if not example_name:
            return None, None
        
        if len(parts) > 1:
            codes_str = parts[1].strip()
            if not codes_str:
                return None, None
            expected_codes = [int(code.strip()) for code in codes_str.split(',') if code.strip()]
            if not expected_codes:
                return None, None
        else:
            expected_codes = [200]
        
        return example_name, expected_codes
    except (ValueError, IndexError):
        return None, None


def _make_flexible_pattern(example_name: str) -> str:
    """
    Create a flexible regex pattern that matches the example name with optional backticks.
    
    This allows patterns like "GET example" to match:
    - "GET example"
    - "`GET` example" 
    - "GET `example`"
    - "`GET` `example`"
    
    Args:
        example_name: The example name to create a pattern for
        
    Returns:
        str: Regex pattern with flexible backtick matching
        
    Example:
        >>> pattern = _make_flexible_pattern("GET example")
        >>> import re
        >>> bool(re.search(pattern, "### `GET` example request"))
        True
    """
    escaped_name = re.escape(example_name)
    # Split on spaces and wrap each word to allow optional backticks
    words = escaped_name.split(r'\ ')
    flexible_words = [rf'`?{word}`?' for word in words]
    flexible_pattern = r'\s+'.join(flexible_words)
    return flexible_pattern


def extract_curl_command(content: str, server_url: str, example_name: str) -> Optional[str]:
    """
    Extract curl command from the specified example section.
    
    Args:
        content: Full markdown file content
        server_url: Base server URL to replace in the curl command if substitution string found
        example_name: Name of the example to find
        
    Returns:
        str: The curl command, or None if not found

    Example:
        >>> content = '''
        ... ### GET example request
        ... ```bash
        ... curl {server_url}/api/users
        ... ```
        ... '''
        >>> cmd = extract_curl_command(content, 'http://localhost:3000', 'GET example')
        >>> print(cmd)
        curl -i http://localhost:3000/api/users
    """
    # Create flexible pattern that allows optional backticks around words
    flexible_pattern = _make_flexible_pattern(example_name)
    
    # Look for heading with "request" (h3 or h4)
    heading_pattern = rf'^###\#?\s+{flexible_pattern}\s+request'
    
    lines = content.split('\n')
    in_example = False
    in_code_block = False
    curl_cmd_elements = []
    curl_cmd_string = ""
    
    for i, line in enumerate(lines):
        # Check if we found the heading
        if re.search(heading_pattern, line, re.IGNORECASE):
            in_example = True
            continue
        
        # If we're in the example section
        if in_example:
            # Look for bash code block
            if line.strip().startswith('```bash') or line.strip().startswith('```sh'):
                in_code_block = True
                continue
            
            # End of code block
            if in_code_block and line.strip() == '```':
                break
            
            # Collect curl command lines
            if in_code_block:
                curl_cmd_elements.append(line)
            
            # Stop if we hit another heading
            if line.startswith('#'):
                break
    
    if curl_cmd_elements:
        curl_cmd_string = '\n'.join(curl_cmd_elements).strip()
        # Add -i flag if not present to get headers
        if '-i' not in curl_cmd_string and '--include' not in curl_cmd_string:
            curl_cmd_string = curl_cmd_string.replace('curl', 'curl -i', 1)
        # Replace server URL if the substitution string found
        if server_url:
            curl_cmd_string = curl_cmd_string.replace('{server_url}', server_url)
        return curl_cmd_string
    
    return None


def extract_expected_response(content: str, example_name: str) -> Optional[Dict[str, Any]]:
    """
    Extract expected JSON response from the specified example section.
    
    Args:
        content: Full markdown file content
        example_name: Name of the example to find
        
    Returns:
        dict: Parsed JSON response, or None if not found

    Example:
        >>> content = '''
        ... ### GET example response
        ... ```json
        ... {"users": [{"id": 1, "name": "Alice"}]}
        ... ```
        ... '''
        >>> response = extract_expected_response(content, 'GET example')
        >>> print(response['users'][0]['name'])
        Alice
    """
    # Create flexible pattern that allows optional backticks around words
    flexible_pattern = _make_flexible_pattern(example_name)
    
    # Look for heading with "response" (h3 or h4)
    heading_pattern = rf'^###\#?\s+{flexible_pattern}\s+response'
    
    lines = content.split('\n')
    in_example = False
    in_code_block = False
    json_lines = []
    
    for i, line in enumerate(lines):
        # Check if we found the heading
        if re.search(heading_pattern, line, re.IGNORECASE):
            in_example = True
            continue
        
        # If we're in the example section
        if in_example:
            # Look for json code block
            if line.strip().startswith('```json'):
                in_code_block = True
                continue
            
            # End of code block
            if in_code_block and line.strip() == '```':
                break
            
            # Collect JSON lines
            if in_code_block:
                json_lines.append(line)
            
            # Stop if we hit another heading
            if line.startswith('#'):
                break
    
    if json_lines:
        try:
            return json.loads('\n'.join(json_lines))
        except json.JSONDecodeError:
            return None
    
    return None


def execute_curl(curl_command: str) -> Tuple[Optional[int], Optional[str], str]:
    """
    Execute a curl command and return the response.
    
    Args:
        curl_command: The curl command to execute
        
    Returns:
        tuple: (status_code, headers, body) or (None, None, error_message)

    Example:
        >>> curl_command = 'curl -i http://localhost:3000/api/users'
        >>> status, headers, body = execute_curl(curl_command)
        >>> if status:
        ...     print(f"Status: {status}")
    """
    try:
        # Run curl with -i to get headers
        result = subprocess.run(
            ['bash', '-c', curl_command],
            capture_output=True,
            text=True,
            timeout=CURL_TIMEOUT_SECONDS
        )
        
        if result.returncode != 0:
            return None, None, result.stderr or "Command failed"
        
        # Parse response
        output = result.stdout
        
        # Split headers and body
        parts = output.split('\n\n', 1)
        if len(parts) < 2:
            # Try with \r\n\r\n
            parts = output.split('\r\n\r\n', 1)
        
        if len(parts) < 2:
            return None, None, "Could not parse response headers/body"
        
        headers = parts[0]
        body = parts[1]
        
        # Extract status code from first line
        status_line = headers.split('\n')[0]
        status_match = re.search(r'HTTP/[\d.]+\s+(\d{3})', status_line)
        
        if not status_match:
            return None, None, "Could not extract status code"
        
        status_code = int(status_match.group(1))
        return status_code, headers, body
        
    except subprocess.TimeoutExpired:
        return None, None, f"Command timed out after {CURL_TIMEOUT_SECONDS} seconds"
    except Exception as e:
        return None, None, str(e)


def compare_json_objects(actual: Any, expected: Any, path: str = "") -> Tuple[bool, List[str]]:
    """
    Recursively compare two JSON objects and return differences.
    
    Args:
        actual: The actual JSON value
        expected: The expected JSON value
        path: Current path in the object hierarchy (for error messages)
        
    Returns:
        tuple: (are_equal, list_of_differences)

    Example:
        >>> actual = {"name": "Alice", "age": 30}
        >>> expected = {"name": "Alice", "age": 25}
        >>> are_equal, diffs = compare_json_objects(actual, expected)
        >>> print(f"Equal: {are_equal}")
        >>> print(f"Differences: {diffs}")
        Equal: False
        Differences: ['Value mismatch at age: expected 25, got 30']
    """
    differences = []
    
    # Compare types
    if type(actual) != type(expected):
        differences.append(f"Type mismatch at {path or 'root'}: expected {type(expected).__name__}, got {type(actual).__name__}")
        return False, differences
    
    # Compare based on type
    if isinstance(expected, dict):
        # Check for missing keys
        for key in expected:
            if key not in actual:
                differences.append(f"Missing key at {path}.{key}" if path else f"Missing key: {key}")
        
        # Check for extra keys
        for key in actual:
            if key not in expected:
                differences.append(f"Extra key at {path}.{key}" if path else f"Extra key: {key}")
        
        # Recursively compare common keys
        for key in expected:
            if key in actual:
                new_path = f"{path}.{key}" if path else key
                are_equal, sub_diffs = compare_json_objects(actual[key], expected[key], new_path)
                differences.extend(sub_diffs)
    
    elif isinstance(expected, list):
        # Compare list lengths
        if len(actual) != len(expected):
            differences.append(f"List length mismatch at {path or 'root'}: expected {len(expected)} items, got {len(actual)}")
            # Still compare what we can
            min_len = min(len(actual), len(expected))
        else:
            min_len = len(expected)
        
        # Compare list items
        for i in range(min_len):
            new_path = f"{path}[{i}]" if path else f"[{i}]"
            are_equal, sub_diffs = compare_json_objects(actual[i], expected[i], new_path)
            differences.extend(sub_diffs)
    
    else:
        # Compare primitive values
        if actual != expected:
            differences.append(f"Value mismatch at {path or 'root'}: expected {expected}, got {actual}")
    
    return len(differences) == 0, differences


def test_example(
    content: str,
    test_config: Dict[str, Any],
    example_name: str,
    expected_codes: List[int],
    file_path: str,
    use_actions: bool,
    action_level: str
) -> bool:
    """
    Test a single example from the documentation.
    
    Args:
        content: Full markdown file content
        test_config: Test metadata taken from file's front matter
        example_name: Name of the example to test
        expected_codes: List of acceptable HTTP status codes
        file_path: Path to the markdown file
        use_actions: Whether to output GitHub Actions annotations
        action_level: Annotation level filter
        
    Returns:
        bool: True if test passed, False otherwise

    Example:
        >>> test_config = {'server_url': 'http://localhost:3000'}
        >>> passed = test_example(
        ...     content=doc_content,
        ...     test_config=test_config,
        ...     example_name='GET example',
        ...     expected_codes=[200],
        ...     file_path='docs/api.md',
        ...     use_actions=False,
        ...     action_level='warning'
        ... )
        >>> print(f"Test {'passed' if passed else 'failed'}")
    """
    log(f"\nTesting example: {example_name}", "info")
    
    # Extract curl command
    server_url = test_config.get('server_url', '')
    curl_cmd = extract_curl_command(content, server_url, example_name)
    if not curl_cmd:
        log(f"Could not find example '{example_name}' or it is not formatted correctly", 
            "warning", file_path, None, use_actions, action_level)
        log(f"Expected format: '### {example_name} request' section with bash code block", "info")
        log(f"-  Help: {HELP_URLS['example_format']}", "info")
        return False
    
    log(f"  Command: {curl_cmd[:80]}...", "info")
    
    # Execute curl command
    status_code, headers, body = execute_curl(curl_cmd)
    
    if status_code is None:
        log(f"Example '{example_name}' failed: {body}", 
            "error", file_path, None, use_actions, action_level)
        return False
    
    log(f"  Status: {status_code}", "info")
    
    # Validate status code
    if status_code not in expected_codes:
        expected_str = ' or '.join(map(str, expected_codes))
        log(f"Example '{example_name}' failed; expected HTTP {expected_str}, got {status_code}", 
            "error", file_path, None, use_actions, action_level)
        return False
    
    log(f"  HTTP {status_code} (success)", "success")
    
    # Parse response body as JSON
    try:
        response_json = json.loads(body)
        log("  Valid JSON response received", "success")
    except json.JSONDecodeError:
        log(f"Example '{example_name}' failed: Response is not valid JSON", 
            "error", file_path, None, use_actions, action_level)
        log(f"  Response: {body[:200]}", "info")
        return False
    
    # Extract expected response
    expected_json = extract_expected_response(content, example_name)
    if expected_json is None:
        log(f"Could not find documented response for '{example_name}' or it is not formatted correctly", 
            "warning", file_path, None, use_actions, action_level)
        log(f"Expected format: '### {example_name} response' section with json code block", "info")
        log(f"-  Help: {HELP_URLS['example_format']}", "info")
        return False
    
    # Compare actual vs expected
    are_equal, differences = compare_json_objects(response_json, expected_json)
    
    if are_equal:
        log("  Response matches documentation exactly", "success")
        log(f"  ✓ Example '{example_name}' PASSED", "success")
        return True
    else:
        log(f"Example '{example_name}' failed: Response does not match documentation", 
            "error", file_path, None, use_actions, action_level)
        log(f"  Differences found: {len(differences)}", "info")
        for diff in differences[:MAX_DIFFERENCES_SHOWN]:
            log(f"    • {diff}", "info")
        if len(differences) > MAX_DIFFERENCES_SHOWN:
            log(f"  ... and {len(differences) - MAX_DIFFERENCES_SHOWN} more differences", "info")
        return False


def test_file(
    file_path: str,
    schema_path: str,
    use_actions: bool = False,
    action_level: str = "warning"
) -> Tuple[int, int, int]:
    """
    Test all examples in a documentation file.
    
    Args:
        file_path: Path to the markdown file to test
        schema_path: Path to JSON schema file for validation
        use_actions: Whether to output GitHub Actions annotations
        action_level: Annotation level filter (all, warning, error)
        
    Returns:
        tuple: (total_tests, passed_tests, failed_tests)

    Example:
        >>> total, passed, failed = test_file(
        ...     'docs/api/users.md',
        ...     '.github/schemas/front-matter-schema.json',
        ...     use_actions=False,
        ...     action_level='warning'
        ... )
        >>> print(f"Ran {total} tests: {passed} passed, {failed} failed")
        Ran 3 tests: 3 passed, 0 failed
    """
    log(f"\n{'='*60}", "info")
    log(f"Testing file: {file_path}", "info")
    log(f"{'='*60}", "info")
    
    # Read file content using shared utility
    content = read_markdown_file(Path(file_path))
    if content is None:
        log(f"File not found or unreadable: {file_path}", 
            "error", file_path, None, use_actions, action_level)
        return 0, 0, 0
    
    # Extract and parse front matter
    metadata, error_message, error_line = parse_front_matter_with_errors(content)
    if not metadata:
        log("Front matter is required for all documentation files", 
            "error", file_path, error_line, use_actions, action_level)
        log(f"-  Help: {HELP_URLS['front_matter']}", "info")
        return 0, 0, 0
    
    # Validate front matter against schema
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata, schema_path, file_path, use_actions, action_level
    )
    
    if not is_valid:
        log("Front matter validation failed. Fix errors before testing examples", "error", file_path, None, use_actions, action_level)
        return 0, 0, 0
    
    if has_warnings:
        log("Front matter has warnings but is valid enough to continue", "warning", file_path, None, use_actions, action_level)
    
    # Check if file has testable examples
    test_config = metadata.get('test', {})
    if not test_config:
        log("No test configuration found in front matter", "info")
        return 0, 0, 0
    
    testable = test_config.get('testable', [])
    if not testable:
        log("No testable examples marked in front matter", "info")
        return 0, 0, 0
    
    log(f"Testable examples found: {len(testable)}", "info")
    for item in testable:
        log(f"  - {item}", "info")
    
    # Test each example
    total_tests = len(testable)
    passed_tests = 0
    failed_tests = 0
    
    for testable_entry in testable:
        example_name, expected_codes = parse_testable_entry(testable_entry)
        
        if example_name is None:
            log(f"Invalid testable entry format: {testable_entry}", "error", file_path, None, use_actions, action_level)
            failed_tests += 1
            continue

        if expected_codes is None:
            # assign default expected HTTP status code
            expected_codes = [200]

        if test_example(content, test_config, example_name, expected_codes, file_path, use_actions, action_level):
            passed_tests += 1
        else:
            failed_tests += 1
    
    return total_tests, passed_tests, failed_tests


def main() -> None:
    """Main entry point for the test-api-docs tool."""
    parser = argparse.ArgumentParser(
        description='Test API documentation code examples against a running json-server instance.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/api.md                    # Normal output
  %(prog)s --action docs/api.md           # GitHub Actions output (warnings and errors)
  %(prog)s --action all docs/api.md       # GitHub Actions output (all levels)
  %(prog)s --action error docs/api.md     # GitHub Actions output (errors only)
        """
    )
    
    parser.add_argument(
        'file',
        type=str,
        help='Path to the markdown documentation file to test'
    )
    
    parser.add_argument(
        '--action', '-a',
        type=str,
        nargs='?',
        const='warning',
        default=None,
        choices=['all', 'warning', 'error'],
        metavar='LEVEL',
        help='Output GitHub Actions annotations. Optional LEVEL: all, warning (default), error'
    )
    
    parser.add_argument(
        '--schema',
        default=DEFAULT_SCHEMA_PATH,
        help='Path to JSON schema file for front matter validation'
    )
    
    args = parser.parse_args()
    
    
    # Test the file
    total, passed, failed = test_file(
        args.file, 
        args.schema, 
        args.action is not None, 
        args.action or 'warning'
    )
    
    # Print summary
    log(f"TEST SUMMARY: {args.file}", "info")
    log(f"  Total tests: {total}", "info")
    if passed > 0:
        log(f"  Passed: {passed}", "success")
    if failed > 0:
        log(f"  Failed: {failed}", "error")
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    elif total == 0:
        log("No tests were run", "warning")
        sys.exit(0)
    else:
        log("✓ All tests passed!", "success")
        sys.exit(0)


if __name__ == '__main__':
    main()
