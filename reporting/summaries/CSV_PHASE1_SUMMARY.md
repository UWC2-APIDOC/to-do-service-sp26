<!-- markdownlint-disable -->
<!-- vale off --> 
# Phase 1: CSV Output - Implementation Summary

## Files Created

### 1. Schema Files (Default/Comprehensive)

**schema_runs_all_fields.yaml**
- All workflow run fields
- ~80+ fields including actor, repository, head_commit, etc.
- Use as starting template - copy and delete unneeded fields

**schema_jobs_all_fields.yaml** 
- Job fields with run context
- Denormalized: repeats run info for each job
- Includes runner information

**schema_steps_all_fields.yaml**
- Step fields with job context  
- Denormalized: repeats job info for each step
- Minimal fields (steps have less data)

### 2. CSV Formatter Module

**csv_formatter.py**
- `load_schema()` - Load YAML schema files
- `format_as_csv()` - Convert JSON to CSV per schema
- `_expand_array()` - Handle denormalization
- `_format_value()` - Type conversion (timestamp, boolean, etc.)
- `save_csv()` - Save with append mode support

## Usage

### Basic CSV Output

```bash
# List runs as CSV
workflow-data.py list-runs rbwatson repo \
  --format csv \
  --schema schema_runs_all_fields.yaml

# Get single run as CSV  
workflow-data.py get-run rbwatson repo 12345 \
  --format csv \
  --schema schema_runs_all_fields.yaml

# Jobs with run context (denormalized)
workflow-data.py list-jobs rbwatson repo 12345 \
  --format csv \
  --schema schema_jobs_all_fields.yaml

# Steps with job context (denormalized)
workflow-data.py get-job rbwatson repo 67890 \
  --format csv \
  --schema schema_steps_all_fields.yaml
```

### Save to File

```bash
# Write to file
workflow-data.py list-runs rbwatson repo \
  --format csv \
  --schema schema_runs_all_fields.yaml \
  --output runs.csv

# Append mode (for collecting history)
workflow-data.py list-runs rbwatson repo --days 1 \
  --format csv \
  --schema schema_runs_all_fields.yaml \
  --output runs.csv \
  --append
```

### Create Custom Schemas

Copy a default schema and edit:

```bash
cp schema_runs_all_fields.yaml my_runs_schema.yaml
# Edit: Remove fields you don't need
# Edit: Rename columns as desired
workflow-data.py list-runs rbwatson repo \
  --format csv \
  --schema my_runs_schema.yaml
```

## Schema Structure

```yaml
schema_name:
  description: "Human-readable description"
  mode: denormalized  # Phase 1 only supports this
  expand: jobs        # Optional: array field to expand into rows
  format: csv
  
  fields:
    - source: id                    # JSON path (dot notation)
      column: run_id                # CSV column name
      type: integer                 # Data type
    
    - source: created_at
      column: created
      type: timestamp
      format: "%Y-%m-%d %H:%M:%S"   # Optional format string
    
    - source: jobs.id              # From expanded array
      column: job_id
      type: integer
```

## Supported Types

- `string` - No conversion
- `integer` - Parse to int
- `float` - Parse to float  
- `boolean` - Convert to true/false
- `timestamp` - Parse ISO, format with strftime
- `url` - String (validates URL format)

## How Denormalization Works

When `expand: jobs` is specified:

**Input JSON:**
```json
{
  "id": 123,
  "name": "Pull request Validation",
  "jobs": [
    {"id": 456, "name": "Lint"},
    {"id": 457, "name": "Test"}
  ]
}
```

**Output CSV:**
```csv
run_id,run_name,job_id,job_name
123,Pull request Validation,456,Lint
123,Pull request Validation,457,Test
```

Run data is repeated for each job (denormalized).

## Next Steps (Phase 2)

- Normalized mode: Multiple CSV files with foreign keys
- Auto-detect schema from command
- Built-in schemas shipped with tool
- Schema validation

## Testing

```bash
# Test with real data
workflow-data.py list-runs rbwatson to-do-service-sp26 --days 1 \
  --format csv \
  --schema schema_runs_all_fields.yaml \
  | head -20

# Should output CSV with all run fields
```

## Notes

- Default output is still JSON (no breaking changes)
- CSV requires `--format csv` and `--schema`
- Schemas are user-editable YAML files
- Type conversion handles ISO timestamps, booleans, etc.
- Append mode skips CSV header on subsequent writes
