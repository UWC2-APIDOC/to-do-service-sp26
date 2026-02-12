<!-- markdownlint-disable -->
<!-- vale off --> 
# Error Handling: stderr Update

## Changes Made

All user-facing error messages now route to stderr instead of stdout, ensuring clean data output streams for piping and automation.

## Files Updated

### workflow_data_utils.py

**Added:**
- `import sys` for stderr access

**Updated functions:**
- `_check_gh_cli()` - All error messages to stderr:
  - gh CLI not found
  - gh CLI not authenticated
  - gh CLI check timeout
  - General check errors

- `_run_gh_api()` - All error messages to stderr:
  - API call failures
  - Request timeouts
  - JSON parsing errors
  - General API errors

### csv_formatter.py

**Added:**
- `import sys` for stderr access

**Updated functions:**
- `load_schema()` - All error messages to stderr:
  - Schema file not found
  - Invalid YAML syntax
  - General loading errors

- `save_csv()` - All error messages to stderr:
  - File write errors

### workflow-data.py

**Already correct:**
- `output_data()` - Errors already on stderr:
  - No data to output
  - Missing schema for CSV
  - Schema loading failure

**Kept on stdout:**
- `"CSV written to {path}"` - Success message (informational, not error)

## Design Principle

### stderr (error stream):
- CLI tool not found/authenticated
- API failures
- File not found
- Invalid input (schema syntax, etc.)
- Write failures
- Any condition that prevents successful operation

### stdout (data stream):
- JSON output
- CSV output
- Success confirmations
- Informational messages about what succeeded

## Benefits

1. **Clean piping:** `workflow-data.py list-runs ... | jq` works without error messages in output
2. **Automation friendly:** Scripts can capture errors separately from data
3. **Standard practice:** Follows Unix philosophy of separating data and diagnostics
4. **Logging:** Allows separate logging of errors vs. data in production systems

## Example Usage

```bash
# Capture data and errors separately
workflow-data.py list-runs rbwatson repo > data.json 2> errors.log

# Pipe data without errors interfering
workflow-data.py list-runs rbwatson repo --format csv --schema runs.yaml | head -5

# Check for errors without seeing data
workflow-data.py get-run rbwatson repo 12345 2>&1 >/dev/null | grep Error

# Redirect errors to /dev/null when you don't care
workflow-data.py list-runs rbwatson repo 2>/dev/null
```

## Future: Logging Integration

These stderr messages are temporary. Next phase will integrate with the project's shared logging utilities (`doc_test_utils.log()`) which provides:
- Consistent message formatting
- Log levels (info, warning, error)
- GitHub Actions annotation support
- Structured logging

For now, stderr provides clean separation between data and diagnostics.
