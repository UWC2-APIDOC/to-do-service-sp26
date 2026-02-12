<!-- markdownlint-disable -->
<!-- vale off --> 
# Timing Commands Implementation

## Summary

Added two new timing commands following the consistent `list-X` / `get-X` pattern:

- **`list-run-timing`** - Get timing for multiple workflow runs
- **`get-run-timing`** - Get timing for a single workflow run (replaces `timing`)

## Changes Made

### 1. workflow_data_utils.py

**New function:** `list_workflow_run_timing()`
- Fetches multiple runs based on filters
- For each run, gets detailed timing data
- Returns nested structure (list of runs, each with jobs array)
- ~130 lines of code

**Enhanced function:** `get_workflow_run_timing()`
- Now returns more context (run_id, run_name, actor, etc.)
- Maintains backward compatibility in structure
- Returns single run with nested jobs array

### 2. workflow-data.py

**Renamed command:**
- `timing` → `get-run-timing`

**New command:**
- `list-run-timing` with filters:
  - `--days N` (default: 7)
  - `--workflow NAME`
  - `--branch NAME`
  - `--status STATUS`

**New command functions:**
- `cmd_list_run_timing()`
- `cmd_get_run_timing()`

### 3. schema_run_timing.yaml

New CSV schema for timing output:
- Expands jobs array into rows
- Denormalizes run context for each job
- Includes all timing fields

## Data Structure

### JSON Output (nested, compact)

```json
[
  {
    "run_id": 12345,
    "run_name": "PR Validation",
    "run_number": 42,
    "run_created_at": "2024-12-16T10:00:00Z",
    "run_updated_at": "2024-12-16T10:03:25Z",
    "run_status": "completed",
    "run_conclusion": "success",
    "run_duration_seconds": 205.0,
    "actor": {
      "login": "rbwatson"
    },
    "jobs": [
      {
        "name": "Validate Testing Tools",
        "status": "completed",
        "conclusion": "success",
        "duration_seconds": 45.2
      },
      {
        "name": "Lint Markdown Files",
        "status": "completed",
        "conclusion": "success",
        "duration_seconds": 89.1
      }
    ],
    "total_job_time_seconds": 134.3
  }
]
```

### CSV Output (denormalized, flat)

```csv
run_id,workflow_name,run_number,run_created_at,run_duration_seconds,actor,job_name,job_status,job_conclusion,job_duration_seconds
12345,PR Validation,42,2024-12-16 10:00:00,205.0,rbwatson,Validate Testing Tools,completed,success,45.2
12345,PR Validation,42,2024-12-16 10:00:00,205.0,rbwatson,Lint Markdown Files,completed,success,89.1
12346,PR Validation,43,2024-12-16 11:30:00,198.5,alice,Validate Testing Tools,completed,success,42.1
12346,PR Validation,43,2024-12-16 11:30:00,198.5,alice,Lint Markdown Files,completed,success,85.3
```

## Usage Examples

### Get timing for last 7 days (JSON)

```bash
workflow-data.py list-run-timing rbwatson to-do-service-sp26
```

### Get timing for last 14 days, specific workflow (JSON)

```bash
workflow-data.py list-run-timing rbwatson to-do-service-sp26 \
  --days 14 \
  --workflow pr-validation.yml
```

### Get timing as CSV

```bash
workflow-data.py list-run-timing rbwatson to-do-service-sp26 \
  --days 7 \
  --format csv \
  --schema schema_run_timing.yaml
```

### Save CSV to file

```bash
workflow-data.py list-run-timing rbwatson to-do-service-sp26 \
  --days 7 \
  --format csv \
  --schema schema_run_timing.yaml \
  --output timing_history.csv
```

### Append to existing CSV (daily collection)

```bash
workflow-data.py list-run-timing rbwatson to-do-service-sp26 \
  --days 1 \
  --format csv \
  --schema schema_run_timing.yaml \
  --output timing_history.csv \
  --append
```

### Get timing for single run

```bash
workflow-data.py get-run-timing rbwatson to-do-service-sp26 12345678
```

### Get single run timing as CSV

```bash
workflow-data.py get-run-timing rbwatson to-do-service-sp26 12345678 \
  --format csv \
  --schema schema_run_timing.yaml
```

## Command Comparison

| Command | Returns | Use Case |
|---------|---------|----------|
| `list-run-timing` | Multiple runs | Analyze timing trends over time |
| `get-run-timing` | Single run | Investigate specific run performance |

Both return the same structure (run with nested jobs array), just different quantities.

## Performance Characteristics

### `list-run-timing` API Calls

For N runs:
- 1 call to `list-runs` (get list of runs)
- N calls to `get-run` (run details)
- N calls to `list-jobs` (jobs for each run)

Total: **1 + 2N calls**

**Example:** 
- 7 days of data = ~50 runs
- API calls = 1 + (2 × 50) = **101 calls**
- Estimated time: **50-100 seconds**

### `get-run-timing` API Calls

For 1 run:
- 1 call to `get-run`
- 1 call to `list-jobs`

Total: **2 calls** (~1-2 seconds)

## CSV Schema Design

The schema uses `expand: jobs` to denormalize:

**Input structure:**
```json
{
  "run_id": 123,
  "jobs": [
    {"name": "Job1"},
    {"name": "Job2"}
  ]
}
```

**Output CSV:**
```
run_id,job_name
123,Job1
123,Job2
```

Run context is repeated for each job, enabling:
- Easy filtering by job name
- Aggregations by run or job
- Time series analysis
- Import to spreadsheets/databases

## Migration Notes

**Breaking change:**
- `timing` command renamed to `get-run-timing`
- Old command no longer exists

**Why no backward compatibility:**
- Only 2 users (you and I)
- Cleaner naming from the start
- Avoids technical debt

**If needed later:**
Add alias in one line:
```python
subparsers.add_parser('timing', help='(alias for get-run-timing)')
```

## Future Enhancements

**Possible additions:**
1. `list-job-timing` - Timing for all jobs across runs
2. `get-job-timing` - Timing for single job (with steps)
3. Time-based aggregations (daily, weekly averages)
4. Built-in filtering (only failed runs, only slow jobs)
5. Comparison mode (run A vs run B)

**Not implemented yet:**
- These would follow the same nested JSON → CSV expansion pattern
- Add only if needed

## Testing

**Manual testing needed:**
```bash
# Test list command (requires valid repo with runs)
workflow-data.py list-run-timing rbwatson to-do-service-sp26 --days 1

# Test get command (requires valid run ID)
workflow-data.py get-run-timing rbwatson to-do-service-sp26 <run-id>

# Test CSV output
workflow-data.py list-run-timing rbwatson to-do-service-sp26 --days 1 \
  --format csv --schema schema_run_timing.yaml

# Verify denormalization (jobs become rows)
# Should see multiple rows per run if run has multiple jobs
```

**Unit tests needed:**
- `test_list_workflow_run_timing()` in test_workflow_data_utils.py
- Mock API responses to avoid network calls
- Verify denormalization logic
- Test error handling

## Files Modified

1. **workflow_data_utils.py**
   - Added `list_workflow_run_timing()` function
   - Enhanced `get_workflow_run_timing()` return value

2. **workflow-data.py**
   - Renamed `timing` → `get-run-timing`
   - Added `list-run-timing` command
   - Updated help text and examples

3. **schema_run_timing.yaml** (new)
   - CSV schema for timing output
   - Expands jobs array
   - All timing fields included

4. **This document** (new)
   - Implementation summary
   - Usage examples
   - Performance notes
