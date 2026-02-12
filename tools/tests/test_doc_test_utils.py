#!/usr/bin/env python3
"""
Tests for doc_test_utils module.

Run with:
    python3 test_doc_test_utils.py
    or
    pytest test_doc_test_utils.py -v
"""

import sys
import io
from pathlib import Path

# Add parent directory to path to import doc_test_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from doc_test_utils import (
    parse_front_matter,
    read_markdown_file,
    get_test_config,
    get_server_database_key,
    log
)


def test_parse_front_matter():
    """Test YAML front matter parsing from markdown content."""
    print("\n" + "="*60)
    print("TEST: parse_front_matter()")
    print("="*60)
    
    # Test valid front matter
    content = """---
layout: default
description: Test page
test:
  testable:
    - GET example
  server_url: localhost:3000
---
# Test Page
"""
    
    metadata = parse_front_matter(content)
    assert metadata is not None, "Should parse valid front matter"
    assert metadata.get('layout') == 'default', f"Expected 'default', got {metadata.get('layout')}"
    assert metadata.get('description') == 'Test page', f"Expected 'Test page', got {metadata.get('description')}"
    print("  SUCCESS: Valid front matter parsed correctly")
    
    # Test missing front matter
    content_no_fm = "# Test Page\nNo front matter here"
    metadata = parse_front_matter(content_no_fm)
    assert metadata is None, "Should return None for missing front matter"
    print("  SUCCESS: Missing front matter returns None")
    
    # Test invalid YAML
    content_bad_yaml = """---
layout: [unclosed list
---
# Test Page
"""
    metadata = parse_front_matter(content_bad_yaml)
    assert metadata is None, "Should return None for invalid YAML"
    print("  SUCCESS: Invalid YAML returns None")
    
    print("  ✓ All parse_front_matter tests passed")


def test_get_test_config():
    """Test extraction of test configuration from metadata."""
    print("\n" + "="*60)
    print("TEST: get_test_config()")
    print("="*60)
    
    # Test with test config present
    metadata = {
        'layout': 'default',
        'test': {
            'testable': ['GET example'],
            'server_url': 'localhost:3000'
        }
    }
    
    config = get_test_config(metadata)
    assert config == metadata['test'], "Should return test config"
    assert config.get('server_url') == 'localhost:3000', "Should extract server_url"
    print("  SUCCESS: Test config extracted correctly")
    
    # Test with no test config
    metadata_no_test = {'layout': 'default'}
    config = get_test_config(metadata_no_test)
    assert config == {}, "Should return empty dict when no test config"
    print("  SUCCESS: Missing test config returns empty dict")
    
    print("  ✓ All get_test_config tests passed")


def test_get_server_database_key():
    """Test extraction of server/database configuration for grouping."""
    print("\n" + "="*60)
    print("TEST: get_server_database_key()")
    print("="*60)
    
    # Test full configuration
    metadata = {
        'test': {
            'test_apps': ['json-server@0.17.4'],
            'server_url': 'localhost:3000',
            'local_database': '/api/test.json'
        }
    }
    
    apps, url, db = get_server_database_key(metadata)
    assert apps == 'json-server@0.17.4', f"Expected 'json-server@0.17.4', got {apps}"
    assert url == 'localhost:3000', f"Expected 'localhost:3000', got {url}"
    assert db == '/api/test.json', f"Expected '/api/test.json', got {db}"
    print("  SUCCESS: Full configuration extracted correctly")
    
    # Test multiple test_apps (should join with comma)
    metadata_multi = {
        'test': {
            'test_apps': ['json-server@0.17.4', 'other-app@1.0.0'],
            'server_url': 'localhost:3000'
        }
    }
    apps, url, db = get_server_database_key(metadata_multi)
    assert apps == 'json-server@0.17.4,other-app@1.0.0', f"Expected joined apps, got {apps}"
    print("  SUCCESS: Multiple test_apps joined correctly")
    
    # Test missing configuration
    metadata_empty = {}
    apps, url, db = get_server_database_key(metadata_empty)
    assert apps is None, "Should return None for missing test_apps"
    assert url is None, "Should return None for missing server_url"
    assert db is None, "Should return None for missing local_database"
    print("  SUCCESS: Missing configuration returns None values")
    
    print("  ✓ All get_server_database_key tests passed")


def test_log_console_output():
    """Test console output for different log levels."""
    print("\n" + "="*60)
    print("TEST: log() console output")
    print("="*60)
    
    # Capture stdout
    captured_output = io.StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        # Test each level
        log("Info message", "info")
        log("Notice message", "notice")
        log("Warning message", "warning")
        log("Error message", "error")
        log("Success message", "success")
        
        sys.stdout = original_stdout
        output = captured_output.getvalue()
        
        assert "INFO: Info message" in output, "Should output INFO label"
        assert "NOTICE: Notice message" in output, "Should output NOTICE label"
        assert "WARNING: Warning message" in output, "Should output WARNING label"
        assert "ERROR: Error message" in output, "Should output ERROR label"
        assert "SUCCESS: Success message" in output, "Should output SUCCESS label"
        
        print("  SUCCESS: All log levels output correctly")
        
    finally:
        sys.stdout = original_stdout
    
    print("  ✓ Console output tests passed")


def test_log_github_actions():
    """Test GitHub Actions annotation output."""
    print("\n" + "="*60)
    print("TEST: log() GitHub Actions annotations")
    print("="*60)
    
    captured_output = io.StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        # Test with action_level='warning' (should annotate warning and error)
        log("Notice message", "notice", "test.md", 1, True, "warning")
        log("Warning message", "warning", "test.md", 2, True, "warning")
        log("Error message", "error", "test.md", 3, True, "warning")
        
        sys.stdout = original_stdout
        output = captured_output.getvalue()
        
        assert "::warning file=test.md,line=2::Warning message" in output, "Should annotate warning"
        assert "::error file=test.md,line=3::Error message" in output, "Should annotate error"
        assert "::notice" not in output, "Notice should not annotate with action_level='warning'"
        
        print("  SUCCESS: action_level='warning' works correctly")
        
        # Test with action_level='error' (should annotate only error)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        log("Warning message", "warning", "test.md", 2, True, "error")
        log("Error message", "error", "test.md", 3, True, "error")
        
        sys.stdout = original_stdout
        output = captured_output.getvalue()
        
        assert "::warning" not in output, "Warning should not annotate with action_level='error'"
        assert "::error file=test.md,line=3::Error message" in output, "Should annotate error"
        
        print("  SUCCESS: action_level='error' works correctly")
        
        # Test with action_level='all' (should annotate notice, warning, error)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        log("Notice message", "notice", "test.md", 1, True, "all")
        log("Warning message", "warning", "test.md", 2, True, "all")
        
        sys.stdout = original_stdout
        output = captured_output.getvalue()
        
        assert "::notice file=test.md,line=1::Notice message" in output, "Should annotate notice with action_level='all'"
        assert "::warning file=test.md,line=2::Warning message" in output, "Should annotate warning with action_level='all'"
        
        print("  SUCCESS: action_level='all' works correctly")
        
    finally:
        sys.stdout = original_stdout
    
    print("  ✓ GitHub Actions annotation tests passed")


def test_read_markdown_file():
    """Test reading markdown files with error handling."""
    print("\n" + "="*60)
    print("TEST: read_markdown_file()")
    print("="*60)
    
    # Create a temporary test file
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "test_sample.md"
    test_content = """---
layout: default
---
# Test Content
"""
    test_file.write_text(test_content, encoding='utf-8')
    
    # Test reading existing file
    content = read_markdown_file(test_file)
    assert content is not None, "Should read existing file"
    assert "# Test Content" in content, "Should contain expected content"
    print("  SUCCESS: Existing file read correctly")
    
    # Test reading non-existent file
    bad_file = test_dir / "nonexistent.md"
    content = read_markdown_file(bad_file)
    assert content is None, "Should return None for non-existent file"
    print("  SUCCESS: Non-existent file returns None")
    
    # Cleanup
    test_file.unlink()
    
    print("  ✓ All read_markdown_file tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR doc_test_utils.py")
    print("="*70)
    
    tests = [
        test_parse_front_matter,
        test_get_test_config,
        test_get_server_database_key,
        test_log_console_output,
        test_log_github_actions,
        test_read_markdown_file
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
# end of file tools/tests/test_doc_test_utils.py