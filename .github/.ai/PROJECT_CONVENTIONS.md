<!-- vale off -->
# Project conventions

This guide defines project-wide conventions for directory structure, CLI patterns,
logging, and GitHub Actions integration.

## Directory dtructure

### Standard layout

```text
project-root/
├── tools/
│   ├── doc_test_utils.py           # Shared utilities
│   ├── list-linter-exceptions.py   # Individual tools
│   ├── markdown-survey.py
│   ├── test-api-docs.py
│   │
│   ├── tests/
│   │   ├── README.md
│   │   ├── test_*.py               # Test suites
│   │   │
│   │   ├── test_data/              # Valid test files
│   │   │   ├── README.md
│   │   │   └── *.md
│   │   │
│   │   └── fail_data/              # Invalid test files
│   │       ├── README.md
│   │       └── *.md
│   │
│   └── [documentation files].md
│
├── .github/
│   └── workflows/
│       └── *.yml                   # GitHub Actions workflows
│
└── [other project directories]
```

### Key principles

**Separation of Concerns:**

- **Tools** live in `tools/`
- **Tests** live in `tools/tests/`
- **Test data** is separated: `test_data/` vs `fail_data/`
- **Documentation** lives with tools or in project root

**Naming:**

- **Utility modules**: `snake_case.py` (e.g., `doc_test_utils.py`)
- **Scripts/tools**: `kebab-case.py` (e.g., `list-linter-exceptions.py`)
- **Test files**: `test_*.py` (pytest standard)
- **Documentation**: `UPPER-CASE.md` or `Title-Case.md`

---

## CLI Argument Patterns

### Standard Arguments

All tools should support these arguments where applicable:

#### --action, -a

**Purpose:** Enable GitHub Actions annotation output

**Format:** `--action [LEVEL]`

**Values:**

- No argument: Use default level (`warning`)
- `all`: Output notice, warning, and error annotations
- `warning`: Output warning and error annotations (default)
- `error`: Output only error annotations

**Examples:**

```bash
# Normal console output
python3 tool.py file.md

# GitHub Actions mode (warnings and errors)
python3 tool.py file.md --action

# GitHub Actions mode (all levels)
python3 tool.py file.md --action all

# GitHub Actions mode (errors only)
python3 tool.py file.md --action error
```

**Implementation:**

```python
parser.add_argument(
    '--action', '-a',
    type=str,
    nargs='?',
    const='warning',
    default=None,
    choices=['all', 'warning', 'error'],
    metavar='LEVEL',
    help='Output GitHub Actions annotations. Optional LEVEL: all, warning (default), error'
)
```

#### File Input

**Purpose:** Specify input file(s)

**Position:** First positional argument

**Examples:**

```bash
python3 tool.py file.md
python3 tool.py docs/*.md
```

**Implementation:**

```python
parser.add_argument(
    'filename',
    type=str,
    help='Path to the markdown file to process'
)
```

#### --help, -h

**Purpose:** Show usage information

**Auto-generated** by argparse

**Must include:**

- Brief description
- Argument documentation
- Usage examples

**Example:**

```python
parser = argparse.ArgumentParser(
    description='Scan markdown files for linter exception tags.',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s README.md                    # Normal output
  %(prog)s --action docs/api.md         # GitHub Actions mode
  %(prog)s --action all docs/api.md     # All annotation levels
    """
)
```

### Future Standard Arguments

As patterns emerge, consider standardizing:

#### --verbose, -v

For detailed output

#### --quiet, -q

For minimal output

#### --output, -o

For specifying output file/directory

---

## Logging Conventions

### Log Levels

Use the shared `log()` function with standard levels:

```python
from doc_test_utils import log

log(message, level, file_path, line, use_actions, action_level)
```

#### Level Definitions

**info** - Informational messages (console only):

```python
log("Processing 10 files...", "info")
log("Found 3 exceptions", "info")
```

**notice** - Notable information (console + annotation if `action_level='all'`):

```python
log("No exceptions found", "notice", file_path, None, use_actions, action_level)
log("Test completed successfully", "notice", file_path, None, use_actions, action_level)
```

**warning** - Problems that don't prevent completion (console + annotation):

```python
log("Deprecated syntax detected", "warning", file_path, line_num, use_actions, action_level)
log("Missing optional field", "warning", file_path, line_num, use_actions, action_level)
```

**error** - Problems that prevent completion (console + annotation):

```python
log("Invalid YAML syntax", "error", file_path, line_num, use_actions, action_level)
log("File not found", "error", file_path, None, use_actions, action_level)
```

**success** - Success confirmations (console only):

```python
log("All tests passed", "success")
log("File processed successfully", "success")
```

### Output Format

**Console Format:**

```text
LEVEL: message
```

**Examples:**

```text
INFO: Processing file.md
WARNING: Deprecated syntax on line 10
ERROR: Invalid YAML in front matter
SUCCESS: All tests passed
```

**GitHub Actions Format:**

```text
::level file=path,line=num::message
```

**Examples:**

```text
::notice file=test.md::No exceptions found
::warning file=test.md,line=10::Deprecated syntax
::error file=test.md,line=5::Invalid YAML
```

### When to Use Each Level

| Level | Use When | Creates Annotation? |
| ------- | ---------- | --------------------- |
| `info` | Progress updates, counts, informational | Never |
| `notice` | Notable events, completion messages | If `action_level='all'` |
| `warning` | Fixable issues, deprecations | If `action_level` ≤ `warning` |
| `error` | Blocking issues, failures | Always when `use_actions=True` |
| `success` | Confirmations, final results | Never |

---

## GitHub Actions Integration

### Workflow Structure

Standard workflow for tool testing:

```yaml
name: Tool Test Workflow
on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:

jobs:
  test-tool:
    name: Test Tool Name
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install pyyaml --break-system-packages
      
      - name: Run tool tests
        run: |
          python3 tools/tool-name.py --action error test-file.md
```

### Annotation Best Practices

**Do:**

- ✅ Provide specific file and line numbers
- ✅ Include actionable information
- ✅ Use appropriate severity levels
- ✅ Filter by action level to avoid noise

**Don't:**

- ❌ Create duplicate annotations for the same issue
- ❌ Annotate informational messages
- ❌ Include implementation details
- ❌ Use annotations for progress updates

**Example - Good Annotation:**

```python
log("Vale exception: Style.Rule on line 15", 
    "warning", "docs/api.md", 15, True, "warning")
# Creates: ::warning file=docs/api.md,line=15::Vale exception: Style.Rule
```

**Example - Bad Annotation:**

```python
log("Processing file 3 of 10...", 
    "info", "docs/api.md", None, True, "all")
# Don't annotate progress messages
```

### Exit Codes

Tools should use standard exit codes:

```python
# Success
sys.exit(0)

# General failure
sys.exit(1)

# Specific error codes (optional)
sys.exit(2)  # Invalid arguments
sys.exit(3)  # File not found
```

---

## Error Handling Patterns

### File Operations

Always handle file errors gracefully:

```python
def read_markdown_file(filepath: Path) -> Optional[str]:
    """Read markdown file with error handling."""
    try:
        return filepath.read_text(encoding='utf-8')
    except FileNotFoundError:
        log(f"File not found: {filepath}", "error")
        return None
    except UnicodeDecodeError as e:
        log(f"Unable to decode file {filepath}: {e}", "error")
        return None
    except Exception as e:
        log(f"Error reading file {filepath}: {e}", "error")
        return None
```

**Principles:**

- Return `None` for errors (don't raise)
- Log error with appropriate level
- Include helpful context in message
- Catch specific exceptions first

### Validation

Return early for invalid input:

```python
def parse_front_matter(content: str) -> Optional[Dict[str, Any]]:
    """Parse YAML front matter."""
    # Early return for invalid input
    if not content:
        return None
    
    # Check for front matter delimiters
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return None
    
    # Try to parse YAML
    try:
        return yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError:
        return None  # Return None, don't raise
```

### Exception Hierarchy

**Catch specific exceptions:**

```python
try:
    result = operation()
except FileNotFoundError:
    # Handle missing file
except PermissionError:
    # Handle permission issue
except Exception as e:
    # Catch-all for unexpected errors
```

**Avoid bare except:**

```python
# Bad
try:
    result = operation()
except:  # Catches everything, including KeyboardInterrupt
    pass

# Good
try:
    result = operation()
except Exception as e:  # Catches errors but not system exits
    log(f"Error: {e}", "error")
```

---

## Shared Utilities Usage

### Import Pattern

Import only what you need:

```python
# Good
from doc_test_utils import parse_front_matter, log, read_markdown_file

# Acceptable
import doc_test_utils

# Avoid
from doc_test_utils import *
```

### Common Functions

All tools should use these shared functions where applicable:

**File Operations:**

```python
content = read_markdown_file(filepath)
```

**Front Matter:**

```python
metadata = parse_front_matter(content)
test_config = get_test_config(metadata)
```

**Logging:**

```python
log(message, level, file_path, line, use_actions, action_level)
```

**Don't Duplicate:**

- File reading logic
- Front matter parsing
- Annotation output formatting
- Error message formatting

---

## Testing Conventions

### Test Organization

**One test file per module:**

```text
doc_test_utils.py          → test_doc_test_utils.py
list-linter-exceptions.py  → test_list_linter_exceptions.py
```

**Test data organization:**

- Valid test files → `test_data/`
- Invalid test files → `fail_data/`
- Each directory has README.md

### Test Execution

**Tests must be runnable multiple ways:**

```bash
# Direct execution
python3 tests/test_doc_test_utils.py

# With pytest
pytest tests/test_doc_test_utils.py -v

# All tests
pytest tests/ -v
```

### Test Output

**Provide informative output:**

```python
def test_function():
    print("\n" + "="*60)
    print("TEST: function_name()")
    print("="*60)
    
    # Test cases with output
    assert condition, "Helpful message"
    print("  SUCCESS: Description of what passed")
    
    print("  ✓ All tests passed")
```

---

## Documentation Conventions

### README Files

Every directory with code should have a README:

**Required sections:**

1. Purpose/Overview
2. File descriptions
3. Usage examples
4. Additional context (if needed)

**Example:**

```markdown
# Directory Name

Brief description of what's in this directory.

## Files

### file1.py
Description and purpose.

### file2.py  
Description and purpose.

## Usage

Example commands or patterns.
```

### Code Comments

**When to comment:**

- Complex logic that isn't obvious
- Why something is done a certain way
- Workarounds for bugs or limitations
- TODO/FIXME for future work

**When not to comment:**

- Obvious code
- Repeating what code does
- Outdated information

```python
# Good - Explains why
# Use regex to handle multi-byte UTF-8 correctly
pattern = r'^---\s*\n(.*?)\n---\s*\n'

# Bad - States the obvious
# Create a pattern
pattern = r'^---\s*\n(.*?)\n---\s*\n'
```

### Inline Documentation

Use docstrings for all public functions:

```python
def parse_front_matter(content: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse YAML front matter from markdown content.
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        Dictionary of front matter metadata, or None if not found/invalid
    """
```

---

## Version Control Conventions

### Commit Messages

**Format:**

```text
Brief description (50 chars or less)

Detailed explanation if needed (wrap at 72 chars).
- Bullet points for multiple changes
- Reference issues: Fixes #123
```

**Examples:**

```text
Refactor front matter parsing to use shared utilities

Migrate list-linter-exceptions.py to use doc_test_utils
- Remove custom annotate() function
- Update CLI arguments
- Add comprehensive tests
```

### Branch Naming

**Pattern:** `type/description`

**Types:**

- `feature/` - New functionality
- `bugfix/` - Bug fixes
- `refactor/` - Code restructuring
- `test/` - Test additions/changes
- `docs/` - Documentation updates

**Examples:**

```text
feature/add-markdown-survey-tests
bugfix/fix-unicode-line-counting
refactor/use-shared-logging
```

---

## Performance Considerations

### When to Optimize

**Optimize when:**

- Processing large files (>1MB)
- Processing many files (>100)
- Called repeatedly in loops
- Profiling shows bottleneck

**Don't optimize:**

- Before measuring
- One-time operations
- Rare edge cases
- At cost of readability

### Memory Management

**Be mindful of:**

- Loading entire files into memory
- Caching large datasets
- Creating many temporary objects

**Pattern:**

```python
# Good - Process in chunks for large files
def process_large_file(filepath):
    with open(filepath, 'r') as f:
        for line in f:  # Iterate, don't load all
            process_line(line)

# Bad - Loads entire file
def process_large_file(filepath):
    content = filepath.read_text()  # Whole file in memory
    for line in content.split('\n'):
        process_line(line)
```

---

## Maintaining Conventions

### When to Update

Update these conventions when:

- Patterns emerge across multiple tools
- Better approaches are discovered
- Team agrees on new standards
- External requirements change

### How to Update

1. Propose change with rationale
2. Update relevant documentation
3. Refactor existing code if needed
4. Announce to team
5. Apply to new code immediately

### Consistency Over Perfection

- Follow existing patterns even if not optimal
- Batch refactoring is better than piecemeal
- Document exceptions when necessary
- Update standards, don't work around them
