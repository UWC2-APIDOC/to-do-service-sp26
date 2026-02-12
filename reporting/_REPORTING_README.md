<!-- markdownlint-disable -->
<!-- vale off -->

# Workflow data collection tools

Utilities for collecting and analyzing GitHub Actions workflow data.

## Overview

This module provides foundational functions for querying GitHub Actions workflow data
via the GitHub CLI (`gh`).
These functions are designed to support future workflow analytics and reporting tools.

## Files

### workflow_data_utils.py

Core data collection utilities.

**Functions:**

- `list_workflow_runs()` - List workflow runs with optional filtering
    by workflow name, date, branch, status
- `get_workflow_run_details()` - Get detailed information for a specific run
- `list_workflow_jobs()` - List all jobs in a workflow run
- `get_workflow_job_details()` - Get detailed job information including steps
- `get_workflow_run_timing()` - Calculate timing metrics for runs and jobs

**Note:** `list_workflow_runs()` uses the general `/actions/runs` endpoint
and filters results in Python.
This is more reliable than the workflow-specific endpoint which requires exact
workflow file names and can return 404 for workflows that exist but have not run recently.

**Query parameters:** All functions properly encode query parameters in the URL
(for example, `created>=2024-12-09` is URL-encoded).
This fixed an issue where `-F` flags were not working for GET requests.

**Error handling:**

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

## Field filtering

All commands support `--fields` to return only specific fields from the response.
This is useful for exploration and reducing output size.

### Syntax

<!-- markdownlint-disable MD013 -->

```bash
--fields "field1,field2,field3"
```

<!-- markdownlint-enable MD013 -->

Fields are comma-separated.
Whitespace is automatically trimmed.

### Nested fields

<!-- vale Google.Colons = NO -->

Use dot notation to access nested fields:

```bash
--fields "id,name,actor.login,head_commit.message"
```

This returns:

```json
[
  {
    "id": 12345,
    "name": "Pull request Validation",
    "actor": {
      "login": "username"
    },
    "head_commit": {
      "message": "Fix bug"
    }
  }
]
```

<!-- vale Google.Colons = YES -->

### Examples

**Minimal output for quick scanning:**

<!-- markdownlint-disable MD013 -->

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

<!-- markdownlint-enable MD013 -->

**Filter array fields (for example, steps in a job):**

<!-- markdownlint-disable MD013 -->

```bash
# Get just step names
python3 workflow-data.py get-job rbwatson to-do-service-sp26 67890 --fields "id,name,steps.name"

# Get multiple fields from each step
python3 workflow-data.py get-job rbwatson to-do-service-sp26 67890 --fields "steps.name,steps.conclusion,steps.number"

# Combine with top-level fields
python3 workflow-data.py get-job rbwatson to-do-service-sp26 67890 --fields "id,name,conclusion,steps.name,steps.conclusion"
```

<!-- markdownlint-enable MD013 -->

<!-- vale Google.Colons = NO -->

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

<!-- vale Google.Colons = YES -->

### Notes

- If a field does not exist, it is omitted from output (no error)
- Field filtering happens after API response, so it does not reduce API quota usage
- Useful for exploration: start with all fields, then narrow down to what you need
- **Array filtering**: Use `array.field` syntax to filter fields within arrays
    (for example, `steps.name`)
- **Multiple array fields**: Can specify multiple fields from the same array
    (for example, `steps.name,steps.conclusion`)
- All items in the array are preserved, only their fields are filtered

## Usage

### Basic examples

<!-- markdownlint-disable MD013 -->

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

<!-- markdownlint-enable MD013 -->

### Programmatic usage

<!-- vale Google.Colons = NO -->

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

<!-- vale Google.Colons = YES -->

## Response formats

### list_workflow_runs()

<!-- vale Google.Colons = NO -->

Returns list of dicts with keys:

- `id` - Workflow run ID
- `name` - Workflow name
- `status` - Current status (completed, in_progress, queued)
- `conclusion` - Final result (success, failure, cancelled, and more)
- `created_at` - ISO timestamp
- `updated_at` - ISO timestamp
- `html_url` - Link to GitHub Actions UI
- Plus additional GitHub API fields

<!-- vale Google.Colons = YES -->

### get_workflow_run_details()

<!-- vale Google.Colons = NO -->

Returns dict with all run information including:

- Run metadata (id, name, status, conclusion)
- Timing information (created_at, updated_at, run_started_at)
- Actor information
- Repository information
- Links (html_url, jobs_url, logs_url)

<!-- vale Google.Colons = YES -->

### list_workflow_jobs()

<!-- vale Google.Colons = NO -->

Returns list of job dicts with:

- `id` - Job ID
- `name` - Job name
- `status` - Current status
- `conclusion` - Final result
- `started_at` - ISO timestamp
- `completed_at` - ISO timestamp
- `steps` - List of step information

<!-- vale Google.Colons = YES -->

### get_workflow_job_details()

<!-- vale Google.Colons = NO -->

Returns dict with complete job information including:

- Job metadata
- Full step information (name, status, conclusion, started_at, completed_at for each)
- Runner information

<!-- vale Google.Colons = YES -->

### get_workflow_run_timing()

<!-- vale Google.Colons = NO -->

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
    }
  ]
}
```

<!-- vale Google.Colons = YES -->

## Testing

**Run test suite:**

```bash
python3 test_workflow_data_utils.py
```

**With pytest:**

```bash
pytest test_workflow_data_utils.py -v
```

**Note:** Tests will show warnings if `gh` CLI is not available,
but will still test error handling and logic.

## Future enhancements

These foundational functions support future development of:

1. **Aggregation tools** - Collect and summarize data across multiple runs
2. **Reporting tools** - Generate CSV/text reports with statistics
3. **Analysis tools** - Calculate trends, averages, failure rates
4. **Monitoring tools** - Track workflow performance over time
5. **Comparison tools** - Compare workflow performance before/after changes

## Error handling

<!-- vale Google.Colons = NO -->

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

<!-- vale Google.Colons = YES -->

## Dependencies

- Python 3.6+
- GitHub CLI (`gh`) - Must be installed and authenticated
- Standard library only (no pip dependencies for core functionality)

## Integration with project standards

- Follows `CODE_STYLE_GUIDE.md`
- `snake_case` function names
- Type hints throughout
- Google-style docstrings with examples
- Returns `None` on errors (no exceptions)
- Comprehensive error logging

## Troubleshooting

**"gh CLI not found"**

- Install GitHub CLI from https://cli.github.com/
- Verify installation: `gh --version`

**"gh CLI not authenticated"**

- Run: `gh auth login`
- Follow authentication prompts

**"Not Found (HTTP 404)" errors**

<!-- vale Google.Parens = NO -->

- The tool uses `/repos/{owner}/{repo}/actions/runs` endpoint (lists all workflows)
- If you see 404, verify repository name: `gh api repos/{owner}/{repo}`
- Check you have access: `gh repo view {owner}/{repo}`

<!-- vale Google.Parens = YES -->

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

**Results do not match manual gh api calls**

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
6. Follow project standards in `/.github/.ai/`

## References

- GitHub CLI: https://cli.github.com/
- GitHub Actions API: https://docs.github.com/en/rest/actions
- Project standards: `/.github/.ai/STANDARDS_INDEX.md`

---

## Instructor guide

### Purpose

The `reporting/` directory contains tools for collecting workflow data
to support grading and course assessment.

### Understanding Pull request validation

When a student submits a PR, the `pr-validation.yml` workflow runs automatically.
Here is what each stage validates:

#### Stage 1: Discover changes

**What it checks:** Identifies which files were modified

**Student impact:** None - this is informational only

#### Stage 2: Test tools (conditional)

**Runs when:** Student modified files in `tools/` directory

**What it checks:** Tool test suite (`pytest tools/tests/`)

**Student impact:** **BLOCKING** - If tools are broken, workflow stops

**Why it matters:** Ensures validation infrastructure is functional

**Common failures:** Student should not be modifying `tools/`.
Contact if they did.

#### Stage 3: Validate commits

**What it checks:**

- File locations (students can only modify `/docs` and `/assignments`)
- Commit structure (exactly 1 commit, no merge commits)

**Student impact:** **BLOCKING** - If validation fails, workflow stops

**Common failures:**

- Modified files outside `/docs` or `/assignments` → Violated assignment boundaries
- Multiple commits → Needs to squash commits
- Merge commit → Needs to rebase instead

#### Stage 4: Lint and test (parallel jobs)

**Runs when:** Stages 1-3 pass

**Jobs run in parallel:**

1. **lint-markdown**
    - Filename validation
    - Linter exception counting
    - Markdown structure survey
    - MarkdownLint checks
    - Vale style checks

2. **test-api-docs** (if docs modified)
    - Validates API examples execute correctly
    - Tests against mock json-server

**Student impact:** **BLOCKING** - All jobs must pass

### Interpreting workflow results

#### ✅ All checks passed

- Pull request meets all technical requirements
- Ready for content review

#### ❌ File location failure

**Message:** "Only files in /docs/ and /assignments/ can be modified"

**Meaning:** Student modified files outside allowed directories

**Action:**

- Review which files were modified
- Determine if legitimate (instructor may need to grant exception)
- If not legitimate, ask student to remove those changes

#### ❌ Commit structure failure

**Message:** "Pull request must contain exactly one commit"

**Meaning:** Multiple commits or merge commits present

**Action:** Student needs to squash/rebase (see contributor guide)

#### ❌ Vale errors

**Annotations show:** Style violations per file/line

**Meaning:** Writing does not follow style guide

**Action:**

- Review violations in context
- Determine if legitimate suppression needed
- Most violations should be fixed, not suppressed

#### ❌ MarkdownLint errors

**Annotations show:** Markdown syntax violations

**Meaning:** Formatting issues (heading levels, list structure, and more)

**Action:** These are usually straightforward fixes

#### ❌ Front matter schema errors

**Message:** Shows which fields are invalid

**Meaning:** YAML front matter does not match required schema

**Action:** Check schema requirements in `.github/schemas/front-matter-schema.json`

#### ❌ API test failures

**Message:** Shows which API call failed and why

**Meaning:** Code example does not work as documented

**Action:**

- Most serious failure type (code is wrong)
- Review the actual versus expected response
- Student needs to fix code example or update expected response

### Grading considerations

**Workflow results inform but do not determine grades:**

- **Passing workflow** = Minimum technical bar met
    - Still need to evaluate content quality
    - Check for accuracy, completeness, clarity

- **Failing workflow** = Technical issues to resolve first
    - Some failures are severity 1 (API tests, file locations)
    - Some failures are severity 2 (style, formatting)
    - Use annotations to provide specific feedback

**Workflow annotations as feedback:**

- Students see the same annotations you do
- Annotations include file/line references
- Clear, actionable error messages
- Reduces need for manual feedback on technical issues

### Monitoring tools

The `workflow-data.py` script lets you analyze workflow runs:

**List recent Pull request validation runs:**

<!-- markdownlint-disable MD013 -->

```bash
cd reporting
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 \
  --workflow pr-validation.yml \
  --days 7 \
  --fields "id,name,conclusion,actor.login,created_at"
```

<!-- markdownlint-enable MD013 -->

**Get timing for a specific run:**

```bash
python3 workflow-data.py timing rbwatson to-do-service-sp26 <run-id>
```

**Analyze failure patterns:**

<!-- markdownlint-disable MD013 -->

```bash
# Get all failed runs
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 \
  --workflow pr-validation.yml \
  --status completed \
  --fields "id,conclusion,actor.login" | \
  grep -A1 '"conclusion": "failure"'
```

<!-- markdownlint-enable MD013 -->

### Assignment configuration

**Control what gets validated via front matter schema:**

<!-- vale Google.Colons = NO -->

Edit `.github/schemas/front-matter-schema.json` to:

- Add/remove required fields
- Change validation rules
- Add new test configurations

**Example:** Require specific fields for assignment 2:

```json
{
  "properties": {
    "assignment": {
      "type": "string",
      "enum": ["assignment-1", "assignment-2", "assignment-3"]
    }
  },
  "required": ["layout", "title", "assignment"]
}
```

<!-- vale Google.Colons = YES -->

### Common student issues and solutions

| Issue | Cause | Solution Link |
|-------|-------|---------------|
| "Too many commits" | Did not squash | [Squashing guide](https://github.com/UWC2-APIDOC/to-do-service-sp26/wiki/Squashing-commits) |
| "Merge commit detected" | Used merge instead of rebase | [Updating your branch](https://github.com/UWC2-APIDOC/to-do-service-sp26/wiki/Updating-your-branch) |
| "File location violation" | Modified wrong directory | [File structure](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/documentation-requirements/#file-location-requirements) |
| "Vale errors" | Style violations | [Style guide](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/writers-guide/) |
| "API test failed" | Code example broken | [Testing API examples](https://uwc2-apidoc.github.io/to-do-service-sp26/contributing/#testing-api-examples) |

### Workflow maintenance

**You likely will not need to modify workflows unless:**

- Adding new validation requirements
- Changing assignment structure
- Updating tool versions (Vale, MarkdownLint, json-server)

**If changes needed:**

- Consult maintainer guide in `tools/_TOOLS_README.md`
- Test changes in fork before deploying
- Consider impact on in-flight student PRs

### Getting help

**For workflow/tool issues:**

- See maintainer guide: `tools/_TOOLS_README.md`
- Check workflow logs in GitHub Actions UI
- Review tool documentation in `tools/` directory

**For student support:**

- Reference contributor guide:
    https://uwc2-apidoc.github.io/to-do-service-sp26/contributing/
- Workflow annotations usually provide specific guidance
- Common issues covered in "Common student issues" section above
