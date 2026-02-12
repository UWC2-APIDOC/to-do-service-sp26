#!/usr/bin/env python3
"""
Query GitHub Actions workflow data for analysis and reporting.

Usage:
    workflow-data.py list-runs <owner> <repo> [options]
    workflow-data.py get-run <owner> <repo> <run-id> [options]
    workflow-data.py list-jobs <owner> <repo> <run-id> [options]
    workflow-data.py get-job <owner> <repo> <job-id> [options]
    workflow-data.py list-run-timing <owner> <repo> [options]
    workflow-data.py get-run-timing <owner> <repo> <run-id> [options]

Examples:
    # List recent workflow runs (default: 10 most recent)
    workflow-data.py list-runs <owner> <repo>
    
    # List all runs in last 7 days
    workflow-data.py list-runs <owner> <repo> --days 7
    
    # List exactly 50 most recent runs
    workflow-data.py list-runs <owner> <repo> --limit 50
    
    # List up to 20 runs within last 14 days
    workflow-data.py list-runs <owner> <repo> --days 14 --limit 20
    
    # Filter to specific workflow
    workflow-data.py list-runs <owner> <repo> --workflow pr-validation.yml
    
    # Return only specific fields (JSON output)
    workflow-data.py list-runs <owner> <repo> --fields "id,name,conclusion,created_at"
    
    # Output as CSV with schema
    workflow-data.py list-runs <owner> <repo> \
        --format csv --schema schema_runs_all_fields.yaml
    
    # Save CSV to file
    workflow-data.py list-runs <owner> <repo> \
        --format csv --schema schema_runs_all_fields.yaml \
        --output runs.csv
    
    # Append to existing CSV file
    workflow-data.py list-runs <owner> <repo> --days 1 \
        --format csv --schema schema_runs_all_fields.yaml \
        --output runs.csv --append
    
    # Get run with specific fields (including nested)
    workflow-data.py get-run <owner> <repo> <run-id> --fields "id,name,actor.login"
    
    # List all jobs in a run
    workflow-data.py list-jobs <owner> <repo> <run-id>
    
    # List jobs with specific fields
    workflow-data.py list-jobs <owner> <repo> <run-id> --fields "id,name,conclusion"
    
    # Get detailed job information
    workflow-data.py get-job <owner> <repo> <job-id>
    
    # Get timing for 10 most recent runs (default, safe)
    workflow-data.py list-run-timing <owner> <repo>
    
    # Get timing for all runs in last 7 days
    workflow-data.py list-run-timing <owner> <repo> --days 7
    
    # Get timing for exactly 25 runs as CSV
    workflow-data.py list-run-timing <owner> <repo> --limit 25 \
        --format csv --schema schema_run_timing.yaml
    
    # Get timing for a single run
    workflow-data.py get-run-timing <owner> <repo> <run-id>
"""

import sys
import json
import argparse
import signal
from pathlib import Path

# Handle broken pipe gracefully (e.g., when piping to head)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from workflow_data_utils import (
    list_workflow_runs,
    get_workflow_run_details,
    list_workflow_jobs,
    get_workflow_job_details,
    list_workflow_run_timing,
    get_workflow_run_timing
)
from csv_formatter import load_schema, format_as_csv, save_csv


def parse_fields(fields_str):
    """Parse comma-separated field list, handling whitespace."""
    if not fields_str:
        return None
    return [f.strip() for f in fields_str.split(',') if f.strip()]


def output_data(data, args):
    """Output data in requested format (JSON or CSV)."""
    if data is None:
        print("Error: No data to output", file=sys.stderr)
        sys.exit(1)
    
    # Check for CSV output
    if hasattr(args, 'format') and args.format == 'csv':
        if not hasattr(args, 'schema') or not args.schema:
            print("Error: --schema required for CSV output", file=sys.stderr)
            sys.exit(1)
        
        # Load schema
        schema_path = Path(args.schema)
        if not schema_path.exists():
            # Try in current directory
            schema_path = Path.cwd() / args.schema
        if not schema_path.exists():
            # Try as built-in schema
            schema_path = Path(__file__).parent / f"schema_{args.schema}.yaml"
        
        schema = load_schema(schema_path)
        if not schema:
            sys.exit(1)
        
        # Format as CSV
        csv_output = format_as_csv(data, schema)
        
        # Output or save
        if hasattr(args, 'output') and args.output:
            output_path = Path(args.output)
            append = hasattr(args, 'append') and args.append
            if save_csv(csv_output, output_path, append):
                print(f"CSV written to {output_path}")
            else:
                sys.exit(1)
        else:
            print(csv_output, end='')
    else:
        # JSON output (default)
        pretty = not (hasattr(args, 'compact') and args.compact)
        if pretty:
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps(data))


def cmd_list_runs(args):
    """List workflow runs."""
    fields = parse_fields(args.fields) if hasattr(args, 'fields') else None
    
    runs = list_workflow_runs(
        repo_owner=args.owner,
        repo_name=args.repo,
        workflow_name=args.workflow,
        days_back=args.days if hasattr(args, 'days') else None,
        branch=args.branch,
        status=args.status,
        limit=args.limit if hasattr(args, 'limit') else None,
        fields=fields
    )
    
    if runs is None:
        sys.exit(1)
    
    output_data(runs, args)


def cmd_get_run(args):
    """Get workflow run details."""
    fields = parse_fields(args.fields) if hasattr(args, 'fields') else None
    
    details = get_workflow_run_details(
        repo_owner=args.owner,
        repo_name=args.repo,
        run_id=args.run_id,
        fields=fields
    )
    
    if details is None:
        sys.exit(1)
    
    output_data(details, args)


def cmd_list_jobs(args):
    """List jobs for a workflow run."""
    fields = parse_fields(args.fields) if hasattr(args, 'fields') else None
    
    jobs = list_workflow_jobs(
        repo_owner=args.owner,
        repo_name=args.repo,
        run_id=args.run_id,
        fields=fields
    )
    
    if jobs is None:
        sys.exit(1)
    
    output_data(jobs, args)


def cmd_get_job(args):
    """Get job details."""
    fields = parse_fields(args.fields) if hasattr(args, 'fields') else None
    
    job = get_workflow_job_details(
        repo_owner=args.owner,
        repo_name=args.repo,
        job_id=args.job_id,
        fields=fields
    )
    
    if job is None:
        sys.exit(1)
    
    output_data(job, args)


def cmd_list_run_timing(args):
    """Get timing information for multiple workflow runs."""
    timing_data = list_workflow_run_timing(
        repo_owner=args.owner,
        repo_name=args.repo,
        workflow_name=args.workflow if hasattr(args, 'workflow') else None,
        days_back=args.days if hasattr(args, 'days') else None,
        branch=args.branch if hasattr(args, 'branch') else None,
        status=args.status if hasattr(args, 'status') else None,
        limit=args.limit if hasattr(args, 'limit') else None
    )
    
    if timing_data is None:
        sys.exit(1)
    
    output_data(timing_data, args)


def cmd_get_run_timing(args):
    """Get timing information for a single workflow run."""
    timing = get_workflow_run_timing(
        repo_owner=args.owner,
        repo_name=args.repo,
        run_id=args.run_id
    )
    
    if timing is None:
        sys.exit(1)
    
    output_data(timing, args)


def main():
    parser = argparse.ArgumentParser(
        description='Query GitHub Actions workflow data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    subparsers.required = True
    
    # Common arguments
    def add_common_args(subparser):
        subparser.add_argument('owner', help='Repository owner')
        subparser.add_argument('repo', help='Repository name')
        subparser.add_argument('--compact', action='store_true',
                             help='Output compact JSON (no pretty-printing)')
        subparser.add_argument('--fields',
                             help='Comma-separated list of fields to return (e.g., "id,name,conclusion")')
        subparser.add_argument('--format', choices=['json', 'csv'], default='json',
                             help='Output format (default: json)')
        subparser.add_argument('--schema',
                             help='Schema file for CSV output (required when --format=csv)')
        subparser.add_argument('--output',
                             help='Output file path (default: stdout)')
        subparser.add_argument('--append', action='store_true',
                             help='Append to output file instead of overwriting (CSV only)')
    
    # list-runs command
    parser_list = subparsers.add_parser('list-runs',
                                        help='List workflow runs')
    add_common_args(parser_list)
    parser_list.add_argument('--workflow',
                           help='Filter by workflow file name (e.g., pr-validation.yml)')
    parser_list.add_argument('--days', type=int,
                           help='Days of history to retrieve (default: unlimited with limit=10)')
    parser_list.add_argument('--limit', type=int,
                           help='Maximum number of runs to return (default: 10, use 0 for unlimited)')
    parser_list.add_argument('--branch',
                           help='Filter by branch name')
    parser_list.add_argument('--status',
                           choices=['completed', 'in_progress', 'queued'],
                           help='Filter by status')
    parser_list.set_defaults(func=cmd_list_runs)
    
    # get-run command
    parser_get = subparsers.add_parser('get-run',
                                       help='Get workflow run details')
    add_common_args(parser_get)
    parser_get.add_argument('run_id', type=int, help='Workflow run ID')
    parser_get.set_defaults(func=cmd_get_run)
    
    # list-jobs command
    parser_jobs = subparsers.add_parser('list-jobs',
                                        help='List jobs for a workflow run')
    add_common_args(parser_jobs)
    parser_jobs.add_argument('run_id', type=int, help='Workflow run ID')
    parser_jobs.set_defaults(func=cmd_list_jobs)
    
    # get-job command
    parser_job = subparsers.add_parser('get-job',
                                       help='Get job details')
    add_common_args(parser_job)
    parser_job.add_argument('job_id', type=int, help='Job ID')
    parser_job.set_defaults(func=cmd_get_job)
    
    # list-run-timing command
    parser_list_timing = subparsers.add_parser('list-run-timing',
                                               help='Get timing for multiple workflow runs')
    add_common_args(parser_list_timing)
    parser_list_timing.add_argument('--workflow',
                                   help='Filter to specific workflow file')
    parser_list_timing.add_argument('--days', type=int,
                                   help='Number of days to look back (default: unlimited with limit=10)')
    parser_list_timing.add_argument('--limit', type=int,
                                   help='Maximum number of runs to return (default: 10, use 0 for unlimited)')
    parser_list_timing.add_argument('--branch',
                                   help='Filter to specific branch')
    parser_list_timing.add_argument('--status',
                                   help='Filter by status (completed, success, failure)')
    parser_list_timing.set_defaults(func=cmd_list_run_timing)
    
    # get-run-timing command
    parser_get_timing = subparsers.add_parser('get-run-timing',
                                             help='Get timing for a single workflow run')
    add_common_args(parser_get_timing)
    parser_get_timing.add_argument('run_id', type=int, help='Workflow run ID')
    parser_get_timing.set_defaults(func=cmd_get_run_timing)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
