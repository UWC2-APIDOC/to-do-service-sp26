<!-- markdownlint-disable -->
<!-- vale off --> 
# Workflow Data Collection Tools

Utilities for collecting and analyzing GitHub Actions workflow data.

## Overview

This module provides foundational functions for querying GitHub Actions workflow data via the GitHub CLI (`gh`). These functions are designed to support future workflow analytics and reporting tools.

## Files

### workflow_data_utils.py

Core data collection utilities.

**Functions:**
- `list_workflow_runs()` - List workflow runs with optional filtering by workflow name, date, branch, status
- `get_workflow_run_details()` - Get detailed information for a specific run
- `list_workflow_jobs()` - List all jobs in a workflow run
- `get_workflow_job_details()` - Get detailed job information including steps
- `get_workflow_run_timing()` - Calculate timing metrics for runs and jobs

**Note:** `list_workflow_runs()` uses the general `/actions/runs` endpoint and filters results in Python. This is more reliable than the workflow-specific endpoint which requires exact workflow file names and can return 404 for workflows that exist but haven't run recently.

**Query parameters:** All functions properly encode query parameters in the URL (e.g., `created>=2024-12-09` is URL-encoded). This fixed an issue where `-F` flags weren't working for GET requests.

**Error Handling:**
- Returns `None` on errors (follows project pattern)
- Logs errors to console
- Does not raise exceptions

### workflow-data.py

CLI tool for querying workflow data.

**Commands:**
- `list-runs` - List recent workflow runs
- `get-run` - Get details for a specific run
- `list-jobs` - List jobs in a run
- `get-job` - Get job details
- `timing` - Get timing information for a run

**Output:** JSON format (pretty-printed by default)

### test_workflow_data_utils.py

Test suite covering error handling, date filtering, and timing calculations.

## Requirements

### GitHub CLI

The tools require the GitHub CLI (`gh`) to be installed and authenticated.

**Install:**
```bash
# macOS
brew install gh

# Linux
# See https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Windows
# See https://github.com/cli/cli#installation
```

**Authenticate:**
```bash
gh auth login
```

## Field Filtering

All commands support `--fields` to return only specific fields from the response. This is useful for exploration and reducing output size.

### Syntax

```bash
--fields "field1,field2,field3"
```

Fields are comma-separated. Whitespace is automatically trimmed.

### Nested Fields

Use dot notation to access nested fields:

```bash
--fields "id,name,actor.login,head_commit.message"
```

This returns:
```json
[
  {
    "id": 12345,
    "name": "PR Validation",
    "actor": {
      "login": "username"
    },
    "head_commit": {
      "message": "Fix bug"
    }
  }
]
```

### Examples

**Minimal output for quick scanning:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --fields "id,name,conclusion"
```

**Include timing information:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --fields "id,name,created_at,updated_at,conclusion"
```

**Include author information:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --fields "id,name,actor.login,conclusion"
```

**Job-level fields:**
```bash
python3 workflow-data.py list-jobs rbwatson to-do-service-sp26 12345 --fields "id,name,conclusion,started_at,completed_at"
```

**Filter array fields (e.g., steps in a job):**
```bash
# Get just step names
python3 workflow-data.py get-job rbwatson to-do-service-sp26 67890 --fields "id,name,steps.name"

# Get multiple fields from each step
python3 workflow-data.py get-job rbwatson to-do-service-sp26 67890 --fields "steps.name,steps.conclusion,steps.number"

# Combine with top-level fields
python3 workflow-data.py get-job rbwatson to-do-service-sp26 67890 --fields "id,name,conclusion,steps.name,steps.conclusion"
```

Output example:
```json
{
  "id": 67890,
  "name": "Lint Markdown Files",
  "conclusion": "success",
  "steps": [
    {"name": "Checkout code", "conclusion": "success"},
    {"name": "Setup Python", "conclusion": "success"},
    {"name": "Run linters", "conclusion": "success"}
  ]
}
```

### Notes

- If a field doesn't exist, it's omitted from output (no error)
- Field filtering happens after API response, so doesn't reduce API quota usage
- Useful for exploration: start with all fields, then narrow down to what you need
- **Array filtering**: Use `array.field` syntax to filter fields within arrays (e.g., `steps.name`)
- **Multiple array fields**: Can specify multiple fields from the same array (e.g., `steps.name,steps.conclusion`)
- All items in the array are preserved, only their fields are filtered

## Usage

### Basic Examples

**List all recent workflow runs:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26
```

**Return only specific fields:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --fields "id,name,conclusion,created_at"
```

**Use nested fields with dot notation:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --fields "id,name,actor.login,head_commit.message"
```

**Filter to specific workflow:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --workflow pr-validation.yml
```

**List runs from last 14 days:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --days 14
```

**Filter by branch:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --branch main
```

**Filter by status:**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --status completed
```

**Get run with specific fields:**
```bash
python3 workflow-data.py get-run rbwatson to-do-service-sp26 12345678 --fields "id,name,conclusion"
```

**List jobs with specific fields:**
```bash
python3 workflow-data.py list-jobs rbwatson to-do-service-sp26 12345678 --fields "id,name,conclusion,started_at"
```

**Get run details:**
```bash
python3 workflow-data.py get-run rbwatson to-do-service-sp26 12345678
```

**List jobs in a run:**
```bash
python3 workflow-data.py list-jobs rbwatson to-do-service-sp26 12345678
```

**Get job details:**
```bash
python3 workflow-data.py get-job rbwatson to-do-service-sp26 98765432
```

**Get timing information:**
```bash
python3 workflow-data.py timing rbwatson to-do-service-sp26 12345678
```

**Compact output (no pretty-printing):**
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --compact
```

### Programmatic Usage

```python
from workflow_data_utils import (
    list_workflow_runs,
    get_workflow_run_timing
)

# List all recent runs
runs = list_workflow_runs(
    repo_owner='rbwatson',
    repo_name='to-do-service-sp26',
    days_back=7
)

# Or filter to specific workflow
runs = list_workflow_runs(
    repo_owner='rbwatson',
    repo_name='to-do-service-sp26',
    workflow_name='pr-validation.yml',
    days_back=7
)

if runs:
    print(f"Found {len(runs)} runs")
    
    # Get timing for first run
    if runs:
        run_id = runs[0]['id']
        timing = get_workflow_run_timing('rbwatson', 'to-do-service-sp26', run_id)
        
        if timing:
            print(f"Run duration: {timing['run_duration_seconds']} seconds")
            for job in timing['jobs']:
                print(f"  {job['name']}: {job['duration_seconds']} seconds")
```

## Response Formats

### list_workflow_runs()

Returns list of dicts with keys:
- `id` - Workflow run ID
- `name` - Workflow name
- `status` - Current status (completed, in_progress, queued)
- `conclusion` - Final result (success, failure, cancelled, etc.)
- `created_at` - ISO timestamp
- `updated_at` - ISO timestamp
- `html_url` - Link to GitHub Actions UI
- Plus additional GitHub API fields

### get_workflow_run_details()

Returns dict with all run information including:
- Run metadata (id, name, status, conclusion)
- Timing information (created_at, updated_at, run_started_at)
- Actor information
- Repository information
- Links (html_url, jobs_url, logs_url)

### list_workflow_jobs()

Returns list of job dicts with:
- `id` - Job ID
- `name` - Job name
- `status` - Current status
- `conclusion` - Final result
- `started_at` - ISO timestamp
- `completed_at` - ISO timestamp
- `steps` - List of step information

### get_workflow_job_details()

Returns dict with complete job information including:
- Job metadata
- Full step information (name, status, conclusion, started_at, completed_at for each)
- Runner information

### get_workflow_run_timing()

Returns dict with:
```json
{
  "run_duration_seconds": 125.5,
  "total_job_time_seconds": 180.2,
  "jobs": [
    {
      "name": "Validate Testing Tools",
      "status": "completed",
      "conclusion": "success",
      "duration_seconds": 45.2
    },
    // ... more jobs
  ]
}
```

## Testing

**Run test suite:**
```bash
python3 test_workflow_data_utils.py
```

**With pytest:**
```bash
pytest test_workflow_data_utils.py -v
```

**Note:** Tests will show warnings if `gh` CLI is not available, but will still test error handling and logic.

## Future Enhancements

These foundational functions support future development of:

1. **Aggregation tools** - Collect and summarize data across multiple runs
2. **Reporting tools** - Generate CSV/text reports with statistics
3. **Analysis tools** - Calculate trends, averages, failure rates
4. **Monitoring tools** - Track workflow performance over time
5. **Comparison tools** - Compare workflow performance before/after changes

## Error Handling

All functions follow project conventions:
- Return `None` on error
- Log errors with descriptive messages
- Do not raise exceptions
- Caller should check for `None` return

Example:
```python
runs = list_workflow_runs('owner', 'repo')
if runs is None:
    print("Failed to fetch workflow runs")
    sys.exit(1)

# Process runs
for run in runs:
    # ...
```

## Dependencies

- Python 3.6+
- GitHub CLI (`gh`) - Must be installed and authenticated
- Standard library only (no pip dependencies for core functionality)

## Integration with Project Standards

- Follows CODE_STYLE_GUIDE.md
- snake_case function names
- Type hints throughout
- Google-style docstrings with examples
- Returns None on errors (no exceptions)
- Comprehensive error logging

## Troubleshooting

**"gh CLI not found"**
- Install GitHub CLI from https://cli.github.com/
- Verify installation: `gh --version`

**"gh CLI not authenticated"**
- Run: `gh auth login`
- Follow authentication prompts

**"Not Found (HTTP 404)" errors**
- The tool uses `/repos/{owner}/{repo}/actions/runs` endpoint (lists all workflows)
- If you see 404, verify repository name: `gh api repos/{owner}/{repo}`
- Check you have access: `gh repo view {owner}/{repo}`

**Empty results**
- Check repository name and owner are correct
- Verify workflow has run in the specified time period
- Increase date range: `--days 30`
- Try without workflow filter first: omit `--workflow` parameter
- Check workflow names with: `gh api repos/{owner}/{repo}/actions/workflows`

**API rate limiting**
- GitHub API has rate limits
- Use `gh api rate_limit` to check current limit
- Reduce request frequency if hitting limits

**Results don't match manual gh api calls**
- The tool filters results by date in Python after fetching
- Use `--days` parameter to adjust range
- Workflow filtering is case-sensitive and matches file path endings

## Contributing

When adding new functions:
1. Follow existing patterns
2. Add comprehensive docstrings with examples
3. Return `None` on errors
4. Add tests to test suite
5. Update this README
6. Follow project standards in /mnt/project/

## References

- GitHub CLI: https://cli.github.com/
- GitHub Actions API: https://docs.github.com/en/rest/actions
- Project standards: /mnt/project/STANDARDS_INDEX.md
