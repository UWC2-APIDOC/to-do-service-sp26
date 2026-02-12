#!/usr/bin/env python3
"""
Utilities for collecting GitHub Actions workflow data.

This module provides functions for:
- Fetching workflow runs and their details
- Retrieving job information and step-level data
- Querying workflow execution history
- Supporting workflow performance analysis

All functions use the GitHub CLI (gh) via bash commands.
"""

import json
import sys
import subprocess
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any
from urllib.parse import urlencode


def _check_gh_cli() -> bool:
    """
    Verify gh CLI is available and authenticated.
    
    Returns:
        True if gh CLI is available and authenticated, False otherwise
    """
    try:
        result = subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            print("Error: gh CLI not found. Install from https://cli.github.com/", file=sys.stderr)
            return False
        
        # Check authentication
        result = subprocess.run(
            ['gh', 'auth', 'status'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            print("Error: gh CLI not authenticated. Run 'gh auth login'", file=sys.stderr)
            return False
            
        return True
    except FileNotFoundError:
        print("Error: gh CLI not found. Install from https://cli.github.com/", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("Error: gh CLI check timed out", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error checking gh CLI: {e}", file=sys.stderr)
        return False


def _run_gh_api(endpoint: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
    """
    Execute a gh api command and return parsed JSON response.
    
    Args:
        endpoint: GitHub API endpoint (e.g., '/repos/owner/repo/actions/runs')
        params: Optional query parameters as key-value pairs
        
    Returns:
        Parsed JSON response as dict, or None on error
        
    Note:
        Errors are logged but not raised. Caller should check for None.
    """
    if not _check_gh_cli():
        return None
    
    # Build URL with query parameters
    url = endpoint
    if params:
        query_string = urlencode(params)
        url = f"{endpoint}?{query_string}"
    
    cmd = ['gh', 'api', url]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error: gh api failed: {result.stderr}", file=sys.stderr)
            print(f"-- Command used: {' '.join(cmd)}", file=sys.stderr)
            return None
        
        return json.loads(result.stdout)
        
    except subprocess.TimeoutExpired:
        print(f"Error: gh api request timed out for {endpoint}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error running gh api: {e}", file=sys.stderr)
        return None


def _filter_fields(data: Any, fields: Optional[List[str]]) -> Any:
    """
    Filter data to include only specified fields.
    
    Args:
        data: Data to filter (dict, list, or primitive)
        fields: List of field names to include, or None for all fields
        
    Returns:
        Filtered data with only specified fields
        
    Note:
        - Supports dot notation for nested fields (e.g., 'actor.login')
        - Supports arrays with dot notation (e.g., 'steps.name' filters each step)
        - If field doesn't exist, it's omitted from output
        - Works recursively on lists and nested structures
        
    Example:
        >>> data = {'id': 1, 'steps': [{'name': 'a', 'status': 'ok'}, {'name': 'b', 'status': 'ok'}]}
        >>> _filter_fields(data, ['id', 'steps.name'])
        {'id': 1, 'steps': [{'name': 'a'}, {'name': 'b'}]}
    """
    if fields is None:
        return data
    
    if isinstance(data, list):
        return [_filter_fields(item, fields) for item in data]
    
    if not isinstance(data, dict):
        return data
    
    # Group fields by their first part (before first dot)
    # This handles multiple nested fields from same parent
    simple_fields = []
    nested_fields = {}
    
    for field in fields:
        if '.' in field:
            parts = field.split('.', 1)
            first, rest = parts[0], parts[1]
            if first not in nested_fields:
                nested_fields[first] = []
            nested_fields[first].append(rest)
        else:
            simple_fields.append(field)
    
    filtered = {}
    
    # Handle simple fields
    for field in simple_fields:
        if field in data:
            filtered[field] = data[field]
    
    # Handle nested fields
    for parent, subfields in nested_fields.items():
        if parent not in data:
            continue
            
        nested_value = data[parent]
        
        if isinstance(nested_value, dict):
            # Nested object - filter it with all subfields
            nested_filtered = _filter_fields(nested_value, subfields)
            # Only include if any subfields matched
            if nested_filtered:
                filtered[parent] = nested_filtered
                
        elif isinstance(nested_value, list):
            # Array of objects - filter each item with all subfields
            filtered_array = []
            for item in nested_value:
                if isinstance(item, dict):
                    item_filtered = _filter_fields(item, subfields)
                    # Only include items where at least one field exists
                    if item_filtered:
                        filtered_array.append(item_filtered)
                else:
                    # Array of primitives - can't filter further
                    filtered_array.append(item)
            
            if filtered_array:
                filtered[parent] = filtered_array
    
    return filtered


def list_workflow_runs(
    repo_owner: str,
    repo_name: str,
    workflow_name: Optional[str] = None,
    days_back: Optional[int] = None,
    branch: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = None,
    fields: Optional[List[str]] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    List workflow runs for a repository.
    
    Args:
        repo_owner: Repository owner (username or organization)
        repo_name: Repository name
        workflow_name: Optional workflow file name to filter results (e.g. 'pr-validation.yml')
                      If None, returns all workflows
        days_back: Number of days of history to retrieve
                  If None and limit not specified, defaults to unlimited with limit=10
        branch: Optional branch name filter
        status: Optional status filter ('completed', 'in_progress', 'queued', etc.)
        limit: Maximum number of runs to return
               If None and days_back not specified, defaults to 10
               If 0, returns all runs (unlimited)
        fields: Optional list of field names to include in results
                Supports dot notation (e.g., ['id', 'name', 'actor.login'])
                If None, returns all fields
        
    Returns:
        List of workflow run dictionaries, or None on error
        Each dict contains: id, name, status, conclusion, created_at, html_url, etc.
        
    Limit Behavior:
        - No args specified: Returns 10 most recent runs
        - --days 7: Returns all runs in last 7 days (unlimited)
        - --limit 50: Returns 50 most recent runs
        - --days 7 --limit 50: Returns up to 50 runs within last 7 days
        - --limit 0: Returns all runs (no limit)
        
    Example:
        >>> # Default: 10 most recent runs
        >>> runs = list_workflow_runs('<owner>', '<repo>')
        >>> len(runs)
        10
        
        >>> # All runs in last 7 days
        >>> runs = list_workflow_runs('<owner>', '<repo>', days_back=7)
        
        >>> # Exactly 50 most recent runs
        >>> runs = list_workflow_runs('<owner>', '<repo>', limit=50)
        
        >>> # Up to 50 runs within last 30 days
        >>> runs = list_workflow_runs('<owner>', '<repo>', days_back=30, limit=50)
        
        >>> # Filter to specific workflow
        >>> runs = list_workflow_runs('<owner>', '<repo>', 
        ...                           workflow_name='pr-validation.yml')
        
        >>> # Return only specific fields
        >>> runs = list_workflow_runs('<owner>', '<repo>',
        ...                           fields=['id', 'name', 'conclusion'])
        >>> runs[0].keys()
        dict_keys(['id', 'name', 'conclusion'])
    """
    # Determine default behavior
    if days_back is None and limit is None:
        # Default: 10 most recent runs
        limit = 10
    elif days_back is not None and limit is None:
        # Days specified but no limit: unlimited
        limit = 0
    
    # Use general actions/runs endpoint (more reliable than workflow-specific)
    endpoint = f'/repos/{repo_owner}/{repo_name}/actions/runs'
    
    params = {'per_page': '100'}
    
    # Add date filter if specified
    if days_back is not None:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        created_filter = cutoff_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        params['created'] = f'>={created_filter}'
    
    if branch:
        params['branch'] = branch
    
    if status:
        params['status'] = status
    
    response = _run_gh_api(endpoint, params)
    if response is None:
        return None
    
    workflow_runs = response.get('workflow_runs', [])
    
    # Filter by date if specified (GitHub's created filter sometimes returns more)
    if days_back is not None:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        filtered_runs = [
            run for run in workflow_runs
            if datetime.fromisoformat(run['created_at'].replace('Z', '+00:00')) >= cutoff_date
        ]
    else:
        filtered_runs = workflow_runs
    
    # Filter by workflow name if specified
    if workflow_name:
        filtered_runs = [
            run for run in filtered_runs
            if run.get('path', '').endswith(workflow_name) or 
               run.get('name', '') == workflow_name
        ]
    
    # Apply limit if specified (0 = unlimited)
    if limit is not None and limit > 0:
        filtered_runs = filtered_runs[:limit]
    
    # Filter fields if specified
    if fields:
        filtered_runs = _filter_fields(filtered_runs, fields)
    
    return filtered_runs


def get_workflow_run_details(
    repo_owner: str,
    repo_name: str,
    run_id: int,
    fields: Optional[List[str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific workflow run.
    
    Args:
        repo_owner: Repository owner (username or organization)
        repo_name: Repository name
        run_id: Workflow run ID
        fields: Optional list of field names to include in results
                Supports dot notation (e.g., ['id', 'name', 'actor.login'])
                If None, returns all fields
        
    Returns:
        Workflow run details dict, or None on error
        Contains: id, name, status, conclusion, created_at, updated_at, 
                  run_started_at, html_url, jobs_url, logs_url, timing_ms, etc.
        
    Example:
        >>> details = get_workflow_run_details('<owner>', '<repo>', <run-id>)
        >>> details['conclusion']
        'success'
        >>> details['run_duration_ms']
        125000
        
        >>> # Return only specific fields
        >>> details = get_workflow_run_details('<owner>', '<repo>', <run-id>,
        ...                                     fields=['id', 'conclusion', 'created_at'])
    """
    endpoint = f'/repos/{repo_owner}/{repo_name}/actions/runs/{run_id}'
    
    response = _run_gh_api(endpoint)
    if response is None:
        return None
    
    # Filter fields if specified
    if fields:
        response = _filter_fields(response, fields)
    
    return response


def list_workflow_jobs(
    repo_owner: str,
    repo_name: str,
    run_id: int,
    fields: Optional[List[str]] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    List all jobs for a specific workflow run.
    
    Args:
        repo_owner: Repository owner (username or organization)
        repo_name: Repository name
        run_id: Workflow run ID
        fields: Optional list of field names to include in results
                Supports dot notation (e.g., ['id', 'name', 'runner.name'])
                If None, returns all fields
        
    Returns:
        List of job dictionaries, or None on error
        Each dict contains: id, name, status, conclusion, started_at, 
                           completed_at, steps, etc.
        
    Example:
        >>> jobs = list_workflow_jobs('<owner>', '<repo>', <run-id>)
        >>> len(jobs)
        4
        >>> jobs[0]['name']
        'Validate Testing Tools'
        
        >>> # Return only specific fields
        >>> jobs = list_workflow_jobs('<owner>', '<repo>', <run-id>,
        ...                           fields=['id', 'name', 'conclusion'])
    """
    endpoint = f'/repos/{repo_owner}/{repo_name}/actions/runs/{run_id}/jobs'
    
    params = {'per_page': '100'}
    
    response = _run_gh_api(endpoint, params)
    if response is None:
        return None
    
    jobs = response.get('jobs', [])
    
    # Filter fields if specified
    if fields:
        jobs = _filter_fields(jobs, fields)
    
    return jobs


def get_workflow_job_details(
    repo_owner: str,
    repo_name: str,
    job_id: int,
    fields: Optional[List[str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific workflow job.
    
    Args:
        repo_owner: Repository owner (username or organization)
        repo_name: Repository name
        job_id: Job ID
        fields: Optional list of field names to include in results
                Supports dot notation (e.g., ['id', 'name', 'steps.name'])
                If None, returns all fields
        
    Returns:
        Job details dict including all steps, or None on error
        Contains: id, name, status, conclusion, started_at, completed_at,
                 steps (with name, status, conclusion, number, started_at, 
                 completed_at for each step)
        
    Example:
        >>> job = get_workflow_job_details('<owner>', '<repo>', 67890)
        >>> job['name']
        'Lint Markdown Files'
        >>> len(job['steps'])
        8
        >>> job['steps'][0]['name']
        'Checkout code'
        
        >>> # Return only specific fields
        >>> job = get_workflow_job_details('<owner>', '<repo>', 67890,
        ...                                 fields=['id', 'name', 'conclusion'])
    """
    endpoint = f'/repos/{repo_owner}/{repo_name}/actions/jobs/{job_id}'
    
    response = _run_gh_api(endpoint)
    if response is None:
        return None
    
    # Filter fields if specified
    if fields:
        response = _filter_fields(response, fields)
    
    return response


def list_workflow_run_timing(
    repo_owner: str,
    repo_name: str,
    workflow_name: Optional[str] = None,
    days_back: Optional[int] = None,
    branch: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Get timing information for multiple workflow runs.
    
    Returns denormalized timing data with run context repeated for each job.
    This enables analysis of timing trends across multiple runs.
    
    Args:
        repo_owner: Repository owner (username or organization)
        repo_name: Repository name
        workflow_name: Optional filter for specific workflow file
        days_back: Number of days to look back
                  If None and limit not specified, defaults to limit=10
        branch: Optional branch filter
        status: Optional status filter (completed, success, failure)
        limit: Maximum number of runs to return
               If None and days_back not specified, defaults to 10
               If 0, returns all runs (unlimited)
        
    Returns:
        List of dicts, one per run, containing:
        - run_id, run_name, run_number, run_created_at, run_updated_at
        - run_status, run_conclusion, run_duration_seconds
        - actor (dict with login)
        - jobs (list with name, status, conclusion, duration_seconds)
        - total_job_time_seconds
        
        Returns None on error.
        
    Limit Behavior:
        - No args specified: Returns timing for 10 most recent runs (20 API calls)
        - --days 7: Returns all runs in last 7 days (potentially 100+ API calls)
        - --limit 50: Returns timing for 50 most recent runs (100 API calls)
        - --days 7 --limit 20: Returns up to 20 runs within last 7 days (40 API calls)
        
    Example:
        >>> # Default: 10 most recent runs (safe)
        >>> timings = list_workflow_run_timing('<owner>', '<repo>')
        >>> len(timings)
        10
        
        >>> # All runs in last 7 days (may be many API calls)
        >>> timings = list_workflow_run_timing('<owner>', '<repo>', days_back=7)
        
        >>> # Exactly 50 runs (100 API calls)
        >>> timings = list_workflow_run_timing('<owner>', '<repo>', limit=50)
        
        >>> timings[0]['run_id']
        <run-id>
        >>> timings[0]['run_name']
        'PR Validation'
        >>> timings[0]['jobs'][0]['name']
        'Validate Testing Tools'
        >>> timings[0]['jobs'][0]['duration_seconds']
        45.2
    """
    # Get list of runs (with limit applied)
    runs = list_workflow_runs(
        repo_owner=repo_owner,
        repo_name=repo_name,
        workflow_name=workflow_name,
        days_back=days_back,
        branch=branch,
        status=status,
        limit=limit,
        fields=None  # Get all fields
    )
    
    if runs is None:
        return None
    
    if not runs:
        print("No runs found matching criteria", file=sys.stderr)
        return []
    
    # Collect timing for each run
    result = []
    
    for run in runs:
        run_id = run.get('id')
        if not run_id:
            continue
        
        # Get run details for accurate timing
        run_details = get_workflow_run_details(repo_owner, repo_name, run_id)
        if run_details is None:
            print(f"Warning: Could not get details for run {run_id}", file=sys.stderr)
            continue
        
        # Get jobs for this run
        jobs = list_workflow_jobs(repo_owner, repo_name, run_id)
        if jobs is None:
            print(f"Warning: Could not get jobs for run {run_id}", file=sys.stderr)
            continue
        
        # Calculate run duration
        run_started = run_details.get('run_started_at')
        run_updated = run_details.get('updated_at')
        
        run_duration = None
        if run_started and run_updated:
            start_time = datetime.fromisoformat(run_started.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(run_updated.replace('Z', '+00:00'))
            run_duration = (end_time - start_time).total_seconds()
        
        # Calculate job durations
        job_timings = []
        total_job_time = 0
        
        for job in jobs:
            started = job.get('started_at')
            completed = job.get('completed_at')
            
            duration = None
            if started and completed:
                start_time = datetime.fromisoformat(started.replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(completed.replace('Z', '+00:00'))
                duration = (end_time - start_time).total_seconds()
                if duration:
                    total_job_time += duration
            
            job_timings.append({
                'name': job.get('name'),
                'status': job.get('status'),
                'conclusion': job.get('conclusion'),
                'duration_seconds': duration
            })
        
        # Build result record
        result.append({
            'run_id': run_details.get('id'),
            'run_name': run_details.get('name'),
            'run_number': run_details.get('run_number'),
            'run_created_at': run_details.get('created_at'),
            'run_updated_at': run_details.get('updated_at'),
            'run_status': run_details.get('status'),
            'run_conclusion': run_details.get('conclusion'),
            'run_duration_seconds': run_duration,
            'actor': run_details.get('actor', {}),
            'jobs': job_timings,
            'total_job_time_seconds': total_job_time
        })
    
    return result


def get_workflow_run_timing(
    repo_owner: str,
    repo_name: str,
    run_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get timing information for a single workflow run and its jobs.
    
    Args:
        repo_owner: Repository owner (username or organization)
        repo_name: Repository name
        run_id: Workflow run ID
        
    Returns:
        Dict with timing information, or None on error
        Contains:
        - run_id, run_name, run_number
        - run_duration_seconds: Total workflow duration
        - actor (dict with login)
        - jobs: List of dicts with job name, duration_seconds, status
        - total_job_time_seconds: Sum of all job durations
        
    Example:
        >>> timing = get_workflow_run_timing('<owner>', '<repo>', <run-id>)
        >>> timing['run_duration_seconds']
        125.5
        >>> timing['jobs'][0]['name']
        'Validate Testing Tools'
        >>> timing['jobs'][0]['duration_seconds']
        45.2
    """
    run_details = get_workflow_run_details(repo_owner, repo_name, run_id)
    if run_details is None:
        return None
    
    jobs = list_workflow_jobs(repo_owner, repo_name, run_id)
    if jobs is None:
        return None
    
    # Calculate run duration
    run_started = run_details.get('run_started_at')
    run_updated = run_details.get('updated_at')
    
    run_duration = None
    if run_started and run_updated:
        start_time = datetime.fromisoformat(run_started.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(run_updated.replace('Z', '+00:00'))
        run_duration = (end_time - start_time).total_seconds()
    
    # Calculate job durations
    job_timings = []
    total_job_time = 0
    
    for job in jobs:
        started = job.get('started_at')
        completed = job.get('completed_at')
        
        duration = None
        if started and completed:
            start_time = datetime.fromisoformat(started.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(completed.replace('Z', '+00:00'))
            duration = (end_time - start_time).total_seconds()
            total_job_time += duration
        
        job_timings.append({
            'name': job.get('name'),
            'status': job.get('status'),
            'conclusion': job.get('conclusion'),
            'duration_seconds': duration
        })
    
    return {
        'run_id': run_details.get('id'),
        'run_name': run_details.get('name'),
        'run_number': run_details.get('run_number'),
        'run_created_at': run_details.get('created_at'),
        'run_updated_at': run_details.get('updated_at'),
        'run_status': run_details.get('status'),
        'run_conclusion': run_details.get('conclusion'),
        'run_duration_seconds': run_duration,
        'actor': run_details.get('actor', {}),
        'jobs': job_timings,
        'total_job_time_seconds': total_job_time
    }
