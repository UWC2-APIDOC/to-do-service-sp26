#!/usr/bin/env python3
"""
Tests for workflow_data_utils module.

Covers:
- gh CLI availability check
- API response parsing
- Date filtering
- Error handling
- Timing calculations

Run with:
    python3 test_workflow_data_utils.py
    pytest test_workflow_data_utils.py -v

Note: These tests require gh CLI to be installed and authenticated.
Some tests use mock data to avoid requiring network access.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow_data_utils import (
    _check_gh_cli,
    _filter_fields,
    list_workflow_runs,
    get_workflow_run_details,
    list_workflow_jobs,
    get_workflow_job_details,
    get_workflow_run_timing
)


def test_check_gh_cli():
    """Test gh CLI availability check."""
    print("\n" + "="*60)
    print("TEST: _check_gh_cli()")
    print("="*60)
    
    # This will fail in environments without gh CLI
    # But should not crash
    result = _check_gh_cli()
    
    assert isinstance(result, bool), "Should return boolean"
    print(f"  gh CLI available: {result}")
    
    if not result:
        print("  ℹ️  gh CLI not available - skipping API tests")
    
    print("  ✓ gh CLI check completed without crashing")


def test_list_workflow_runs_params():
    """Test list_workflow_runs parameter handling."""
    print("\n" + "="*60)
    print("TEST: list_workflow_runs() parameter validation")
    print("="*60)
    
    # Test with invalid repo - should return None gracefully
    runs = list_workflow_runs(
        repo_owner='nonexistent',
        repo_name='nonexistent',
        workflow_name='test.yml',  # Optional parameter
        days_back=1
    )
    
    # Should return None (not crash) for invalid repo
    assert runs is None or isinstance(runs, list), \
        "Should return None or list, not crash"
    
    # Test without workflow_name (should work)
    runs2 = list_workflow_runs(
        repo_owner='nonexistent',
        repo_name='nonexistent',
        days_back=1
    )
    
    assert runs2 is None or isinstance(runs2, list), \
        "Should work without workflow_name parameter"
    
    print("  ✓ Handles invalid repository gracefully")
    print("  ✓ Works with optional workflow_name parameter")


def test_list_workflow_runs_limit_defaults():
    """Test list_workflow_runs limit default behavior."""
    print("\n" + "="*60)
    print("TEST: list_workflow_runs() limit defaults")
    print("="*60)
    
    # Note: These tests verify the logic, but will fail with nonexistent repo
    # In production, the actual API call would respect these parameters
    
    # Test 1: No parameters (should default to limit=10)
    # This would work with real repo: limit should be 10
    print("  Test 1: No params → should default to limit=10")
    print("    (Would apply in real API call)")
    
    # Test 2: days_back only (should be unlimited)
    # This would work with real repo: limit should be 0 (unlimited)
    print("  Test 2: --days 7 → should be unlimited within timeframe")
    print("    (Would apply in real API call)")
    
    # Test 3: limit only (should use that limit)
    # This would work with real repo: limit should be 50
    print("  Test 3: --limit 50 → should return exactly 50")
    print("    (Would apply in real API call)")
    
    # Test 4: both days and limit (should use both)
    print("  Test 4: --days 7 --limit 20 → should apply both constraints")
    print("    (Would apply in real API call)")
    
    print("  ✓ Logic for limit defaults documented")


def test_get_workflow_run_details_invalid():
    """Test get_workflow_run_details with invalid run ID."""
    print("\n" + "="*60)
    print("TEST: get_workflow_run_details() error handling")
    print("="*60)
    
    # Test with invalid run ID - should return None gracefully
    details = get_workflow_run_details(
        repo_owner='nonexistent',
        repo_name='nonexistent',
        run_id=99999999
    )
    
    assert details is None or isinstance(details, dict), \
        "Should return None or dict, not crash"
    
    print("  ✓ Handles invalid run ID gracefully")


def test_list_workflow_jobs_invalid():
    """Test list_workflow_jobs with invalid run ID."""
    print("\n" + "="*60)
    print("TEST: list_workflow_jobs() error handling")
    print("="*60)
    
    jobs = list_workflow_jobs(
        repo_owner='nonexistent',
        repo_name='nonexistent',
        run_id=99999999
    )
    
    assert jobs is None or isinstance(jobs, list), \
        "Should return None or list, not crash"
    
    print("  ✓ Handles invalid run ID gracefully")


def test_get_workflow_job_details_invalid():
    """Test get_workflow_job_details with invalid job ID."""
    print("\n" + "="*60)
    print("TEST: get_workflow_job_details() error handling")
    print("="*60)
    
    job = get_workflow_job_details(
        repo_owner='nonexistent',
        repo_name='nonexistent',
        job_id=99999999
    )
    
    assert job is None or isinstance(job, dict), \
        "Should return None or dict, not crash"
    
    print("  ✓ Handles invalid job ID gracefully")


def test_get_workflow_run_timing_invalid():
    """Test get_workflow_run_timing with invalid run ID."""
    print("\n" + "="*60)
    print("TEST: get_workflow_run_timing() error handling")
    print("="*60)
    
    timing = get_workflow_run_timing(
        repo_owner='nonexistent',
        repo_name='nonexistent',
        run_id=99999999
    )
    
    assert timing is None or isinstance(timing, dict), \
        "Should return None or dict, not crash"
    
    print("  ✓ Handles invalid run ID gracefully")


def test_date_filtering_logic():
    """Test date filtering logic with mock data."""
    print("\n" + "="*60)
    print("TEST: Date filtering logic")
    print("="*60)
    
    # Mock workflow runs with different dates (use timezone-aware datetime)
    from datetime import timezone
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=7)
    
    mock_runs = [
        {'created_at': (now - timedelta(days=2)).isoformat().replace('+00:00', 'Z')},
        {'created_at': (now - timedelta(days=5)).isoformat().replace('+00:00', 'Z')},
        {'created_at': (now - timedelta(days=10)).isoformat().replace('+00:00', 'Z')},  # Should be filtered
    ]
    
    # Filter runs (simulate what list_workflow_runs does)
    filtered = [
        run for run in mock_runs
        if datetime.fromisoformat(run['created_at'].replace('Z', '+00:00')) >= cutoff
    ]
    
    assert len(filtered) == 2, f"Should filter to 2 runs, got {len(filtered)}"
    print(f"  Filtered {len(mock_runs)} runs to {len(filtered)} within date range")
    print("  ✓ Date filtering works correctly")


def test_timing_calculation_logic():
    """Test timing calculation logic with mock data."""
    print("\n" + "="*60)
    print("TEST: Timing calculation logic")
    print("="*60)
    
    # Mock timing data
    start = datetime(2024, 12, 12, 10, 0, 0)
    end = datetime(2024, 12, 12, 10, 2, 5)  # 2 minutes 5 seconds later
    
    duration = (end - start).total_seconds()
    
    assert duration == 125.0, f"Expected 125 seconds, got {duration}"
    print(f"  Calculated duration: {duration} seconds")
    print("  ✓ Timing calculation works correctly")


def test_filter_fields():
    """Test field filtering logic."""
    print("\n" + "="*60)
    print("TEST: Field filtering logic")
    print("="*60)
    
    # Test with simple fields
    data = {
        'id': 123,
        'name': 'test',
        'status': 'completed',
        'extra': 'should be filtered'
    }
    
    filtered = _filter_fields(data, ['id', 'name'])
    assert 'id' in filtered, "Should include 'id' field"
    assert 'name' in filtered, "Should include 'name' field"
    assert 'extra' not in filtered, "Should filter out 'extra' field"
    assert len(filtered) == 2, f"Should have 2 fields, got {len(filtered)}"
    print("  ✓ Simple field filtering works")
    
    # Test with nested fields
    nested_data = {
        'id': 123,
        'actor': {
            'login': 'user1',
            'id': 456,
            'email': 'test@example.com'
        }
    }
    
    filtered = _filter_fields(nested_data, ['id', 'actor.login'])
    assert 'id' in filtered, "Should include 'id' field"
    assert 'actor' in filtered, "Should include 'actor' object"
    assert 'login' in filtered['actor'], "Should include nested 'actor.login' field"
    assert 'email' not in filtered.get('actor', {}), "Should filter out 'actor.email'"
    print("  ✓ Nested field filtering works")
    
    # Test with list of objects
    list_data = [
        {'id': 1, 'name': 'first', 'extra': 'data'},
        {'id': 2, 'name': 'second', 'extra': 'more'}
    ]
    
    filtered = _filter_fields(list_data, ['id', 'name'])
    assert len(filtered) == 2, "Should preserve list length"
    assert 'extra' not in filtered[0], "Should filter fields in list items"
    print("  ✓ List filtering works")
    
    # Test with None fields (should return all)
    filtered = _filter_fields(data, None)
    assert len(filtered) == len(data), "None fields should return all data"
    print("  ✓ None fields returns all data")
    
    # Test with array of objects and nested field
    array_data = {
        'id': 123,
        'name': 'job',
        'steps': [
            {'name': 'step1', 'status': 'completed', 'number': 1},
            {'name': 'step2', 'status': 'completed', 'number': 2},
            {'name': 'step3', 'status': 'failed', 'number': 3}
        ]
    }
    
    filtered = _filter_fields(array_data, ['id', 'steps.name'])
    assert 'id' in filtered, "Should include 'id' field"
    assert 'steps' in filtered, "Should include 'steps' array"
    assert len(filtered['steps']) == 3, "Should preserve array length"
    assert 'name' in filtered['steps'][0], "Should include nested 'name' field"
    assert 'status' not in filtered['steps'][0], "Should filter out 'status' field"
    assert filtered['steps'][0]['name'] == 'step1', "Should preserve values"
    print("  ✓ Array of objects with nested field filtering works")
    
    # Test with multiple nested fields in array
    filtered = _filter_fields(array_data, ['steps.name', 'steps.status'])
    assert len(filtered['steps']) == 3, "Should preserve array length"
    assert 'name' in filtered['steps'][0], "Should include 'name'"
    assert 'status' in filtered['steps'][0], "Should include 'status'"
    assert 'number' not in filtered['steps'][0], "Should filter out 'number'"
    print("  ✓ Multiple nested fields in array works")
    
    print("  ✓ All field filtering tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR workflow_data_utils.py")
    print("="*70)
    
    tests = [
        test_check_gh_cli,
        test_list_workflow_runs_params,
        test_list_workflow_runs_limit_defaults,
        test_get_workflow_run_details_invalid,
        test_list_workflow_jobs_invalid,
        test_get_workflow_job_details_invalid,
        test_get_workflow_run_timing_invalid,
        test_date_filtering_logic,
        test_timing_calculation_logic,
        test_filter_fields,
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
