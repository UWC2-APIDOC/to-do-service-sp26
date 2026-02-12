<!-- markdownlint-disable -->
<!-- vale off --> 
# Limit Parameter Implementation

## Summary

Added `--limit` parameter to `list-runs` and `list-run-timing` commands to control API usage and provide safer defaults.

## Motivation

**Problem:** 
- `list-run-timing` with `--days 30` could make 400+ API calls
- Easy to accidentally burn through API quota
- No way to get "just the last N runs" without specifying days

**Solution:**
Add `--limit` parameter with smart defaults that balance safety and flexibility.

## Behavior

### Default Behavior (no flags)

```bash
workflow-data.py list-runs <owner> <repo>
workflow-data.py list-run-timing <owner> <repo>
```

**Returns:** 10 most recent runs  
**API calls:** 1 for list-runs, 21 for list-run-timing (2 per run + 1)  
**Safe:** âœ… Yes - minimal API usage

### Using --days Only

```bash
workflow-data.py list-runs <owner> <repo> --days 7
workflow-data.py list-run-timing <owner> <repo> --days 7
```

**Returns:** All runs in last 7 days (unlimited)  
**API calls:** Depends on activity (could be 1-200+)  
**Use when:** You specifically want time-based filtering

### Using --limit Only

```bash
workflow-data.py list-runs <owner> <repo> --limit 50
workflow-data.py list-run-timing <owner> <repo> --limit 50
```

**Returns:** Exactly 50 most recent runs  
**API calls:** 1 for list-runs, 101 for list-run-timing  
**Use when:** You want exact count regardless of time

### Using Both --days and --limit

```bash
workflow-data.py list-runs <owner> <repo> --days 30 --limit 20
workflow-data.py list-run-timing <owner> <repo> --days 30 --limit 20
```

**Returns:** Up to 20 runs within last 30 days (whichever is fewer)  
**API calls:** 1 for list-runs, 41 for list-run-timing  
**Use when:** You want both time and count constraints

### Unlimited (--limit 0)

```bash
workflow-data.py list-runs <owner> <repo> --limit 0
workflow-data.py list-runs <owner> <repo> --days 30 --limit 0
```

**Returns:** All runs (no limit)  
**API calls:** Could be very high  
**Use when:** You really need everything and understand the API cost

## Logic Table

| --days | --limit | Result |
|--------|---------|--------|
| (none) | (none) | 10 most recent runs (default) |
| 7 | (none) | All runs in last 7 days (unlimited) |
| (none) | 50 | 50 most recent runs |
| 7 | 50 | Up to 50 runs within last 7 days |
| 7 | 0 | All runs in last 7 days (explicit unlimited) |
| (none) | 0 | All runs ever (dangerous!) |

## API Call Estimates

### list-runs

| Command | Typical Runs | API Calls |
|---------|-------------|-----------|
| `list-runs <owner> <repo>` | 10 | 1 |
| `list-runs <owner> <repo> --days 7` | 20-50 | 1 |
| `list-runs <owner> <repo> --limit 50` | 50 | 1 |

**Note:** list-runs always makes just 1 API call (GitHub returns up to 100 runs per call).

### list-run-timing

| Command | Typical Runs | API Calls |
|---------|-------------|-----------|
| `list-run-timing <owner> <repo>` | 10 | 21 (1 + 2×10) |
| `list-run-timing <owner> <repo> --days 7` | 20-50 | 41-101 |
| `list-run-timing <owner> <repo> --limit 25` | 25 | 51 (1 + 2×25) |
| `list-run-timing <owner> <repo> --days 30` | 100+ | 200+ ⚠️ |
| `list-run-timing <owner> <repo> --days 30 --limit 20` | 20 | 41 |

**Formula:** API calls = 1 + (2 × number_of_runs)

## Breaking Changes

**From previous version:**
- `list-runs` no longer defaults to `--days 7`
- `list-run-timing` no longer defaults to `--days 7`
- Default behavior changed from "last 7 days" to "last 10 runs"

**Migration:**
```bash
# Old behavior (all runs in last 7 days)
workflow-data.py list-runs <owner> <repo>

# New equivalent
workflow-data.py list-runs <owner> <repo> --days 7

# Or to keep old CLI compatibility, always specify --days
```

**Why this is better:**
- Safer default (10 runs = predictable API usage)
- Explicit control when you want time-based filtering
- No accidental API quota burnout

## Use Case Examples

### Daily Timing Collection

```bash
# Collect yesterday's runs (append to CSV)
workflow-data.py list-run-timing <owner> <repo> --days 1 \
  --format csv --schema schema_run_timing.yaml \
  --output daily_timing.csv --append
```

### Weekly Report

```bash
# Get last 50 runs for analysis
workflow-data.py list-runs <owner> <repo> --limit 50 \
  --format csv --schema schema_runs_all_fields.yaml \
  --output weekly_report.csv
```

### Trend Analysis

```bash
# Get timing for last 100 runs (regardless of date)
workflow-data.py list-run-timing <owner> <repo> --limit 100 \
  --format csv --schema schema_run_timing.yaml
```

### Investigating Recent Issues

```bash
# Get failed runs from last 3 days (limited to 20)
workflow-data.py list-runs <owner> <repo> \
  --days 3 --status completed --limit 20 | \
  jq '.[] | select(.conclusion == "failure")'
```

## Implementation Details

### Function Signature Changes

**workflow_data_utils.py:**

```python
# Before
def list_workflow_runs(
    repo_owner: str,
    repo_name: str,
    workflow_name: Optional[str] = None,
    days_back: int = 7,  # Default: 7
    ...
)

# After
def list_workflow_runs(
    repo_owner: str,
    repo_name: str,
    workflow_name: Optional[str] = None,
    days_back: Optional[int] = None,  # No default
    ...
    limit: Optional[int] = None,  # New parameter
)
```

**Logic in function:**

```python
# Determine default behavior
if days_back is None and limit is None:
    limit = 10  # Default: 10 most recent
elif days_back is not None and limit is None:
    limit = 0  # Days specified: unlimited
# else: use provided values
```

### CLI Changes

**workflow-data.py:**

```python
# Before
parser_list.add_argument('--days', type=int, default=7, ...)

# After  
parser_list.add_argument('--days', type=int, ...)  # No default
parser_list.add_argument('--limit', type=int, ...)  # New argument
```

## Testing

**Test matrix:**

- [ ] No args → returns 10 runs
- [ ] --days 7 → returns all runs in 7 days
- [ ] --limit 25 → returns exactly 25 runs
- [ ] --days 7 --limit 25 → returns min(runs_in_7_days, 25)
- [ ] --limit 0 → returns all runs (unlimited)
- [ ] --days 30 --limit 0 → returns all runs in 30 days

**API call verification:**

```bash
# Should make 21 API calls (1 + 2×10)
workflow-data.py list-run-timing <owner> <repo> 2>&1 | grep "gh api" | wc -l
```

## Future Enhancements

**Possible additions:**

1. **Warning for high API usage:**
   ```bash
   workflow-data.py list-run-timing <owner> <repo> --days 30
   # Warning: This may make 200+ API calls. Continue? [y/N]
   ```

2. **Progress indicator:**
   ```bash
   workflow-data.py list-run-timing <owner> <repo> --limit 100
   # Processing run 50/100...
   ```

3. **Built-in pagination:**
   ```bash
   workflow-data.py list-runs <owner> <repo> --limit 100 --page 2
   # Get runs 101-200
   ```

4. **Rate limit checking:**
   ```bash
   workflow-data.py check-rate-limit
   # API calls remaining: 4,234 / 5,000
   ```

## Documentation Updates

Updated files:
- ✅ workflow_data_utils.py - Function signatures and docstrings
- ✅ workflow-data.py - CLI arguments and help text
- ✅ This document - Complete behavior documentation

## Conclusion

The `--limit` parameter provides:
- ✅ Safe defaults (10 runs)
- ✅ Predictable API usage
- ✅ Flexible control (days, limit, or both)
- ✅ Backward compatibility (via --days flag)
- ✅ Protection against accidental quota burnout

Default behavior optimizes for safety while allowing power users to explicitly request more data when needed.
