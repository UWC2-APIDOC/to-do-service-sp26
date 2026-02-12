# Code style guide

<!-- vale off -->

This guide defines coding standards for the documentation testing tools project.

## Python Naming Conventions

### Functions and Variables

Use `snake_case` for all functions, methods, and variables:

```python
# Good
def parse_front_matter(content):
    test_config = get_test_config(metadata)
    server_url = config.get('server_url')

# Bad
def parseFrontMatter(content):
    testConfig = getTestConfig(metadata)
    serverURL = config.get('server_url')
```

### Classes

Use `PascalCase` for class names:

```python
# Good
class DocumentParser:
    pass

# Bad
class document_parser:
    pass
```

### Constants

Use `UPPER_SNAKE_CASE` for constants:

```python
# Good
MAX_FILE_SIZE = 1000000
DEFAULT_TIMEOUT = 30

# Bad
maxFileSize = 1000000
default_timeout = 30
```

### Private/Internal

Use single leading underscore for internal functions/variables:

```python
# Good
def _internal_helper():
    pass

_cache = {}

# Bad
def __internal_helper():  # Double underscore is for name mangling
    pass
```

## File Naming Conventions

### Python Files

- **Utility modules**: `snake_case.py`
    - Example: `doc_test_utils.py`
- **Test files**: `test_*.py` (pytest convention)
    - Example: `test_doc_test_utils.py`, `test_list_linter_exceptions.py`
- **Scripts/tools**: Use hyphens for multi-word names
    - Example: `list-linter-exceptions.py`, `test-api-docs.py`

### Markdown Files

- **Documentation**: Use hyphens for readability
    - Example: `CODE-STYLE-GUIDE.md`, `PHASE-2-SUMMARY.md`
- **Test data**: Use underscores
    - Example: `edge_cases_front_matter.md`, `broken_front_matter.md`

### Why Different Conventions?

- **Python modules** use underscores (standard Python convention)
- **Scripts** use hyphens (more readable in URLs and file listings)
- **Test data** uses underscores (matches Python naming for consistency in code)

## Docstring Format

### Functions

Use Google-style docstrings:

```python
def parse_front_matter(content: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse YAML front matter from markdown content.
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        Dictionary of front matter metadata, or None if not found/invalid
        
    Example:
        >>> content = "---\\nlayout: default\\n---\\n# Heading"
        >>> metadata = parse_front_matter(content)
        >>> metadata['layout']
        'default'
    """
```

Required sections:

- Brief description (one line)
- `Args:` - Parameter descriptions
- `Returns:` - Return value description
- `Example:` (optional but recommended)

### Modules

Include module-level docstring at the top:

```python
#!/usr/bin/env python3
"""
Shared utilities for documentation testing tools.

This module provides common functions for:
- Parsing YAML front matter from markdown files
- Reading markdown files with error handling
- Unified logging with GitHub Actions annotation support
"""
```

## Import Organization

Order imports in three groups, separated by blank lines:

```python
# 1. Standard library imports
import sys
import re
from pathlib import Path
from typing import Optional, Dict, Any

# 2. Third-party imports
import yaml
import pytest

# 3. Local imports
from doc_test_utils import parse_front_matter, log
```

Within each group, sort alphabetically.

## Type Hints

Use type hints for function signatures:

```python
# Good
def log(message: str, 
        level: str = "info",
        file_path: Optional[str] = None,
        line: Optional[int] = None) -> None:
    pass

# Acceptable (for complex types)
from typing import Optional, Dict, Any, Tuple

def get_server_database_key(metadata: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    pass
```

## Error Handling Patterns

### File Operations

Always handle file errors gracefully:

```python
# Good
def read_markdown_file(filepath: Path) -> Optional[str]:
    try:
        return filepath.read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except UnicodeDecodeError as e:
        print(f"Error: Unable to decode file {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None
```

### Don't Suppress Errors Silently

Always log when returning None or empty results:

```python
# Good
if not filepath.exists():
    log(f"File not found: {filepath}", "error")
    return None

# Bad
if not filepath.exists():
    return None  # Silent failure
```

## Function Length and Complexity

### Keep Functions Focused

Each function should do one thing:

```python
# Good - Single responsibility
def parse_front_matter(content: str) -> Optional[Dict[str, Any]]:
    """Extract and parse YAML front matter."""
    # Only parsing logic here

def validate_front_matter(metadata: dict, schema: dict) -> bool:
    """Validate front matter against schema."""
    # Only validation logic here

# Bad - Multiple responsibilities
def parse_and_validate_front_matter(content: str, schema: dict) -> tuple:
    """Parse and validate front matter."""
    # Mixing parsing and validation
```

### Function Length

- Aim for functions under 50 lines
- If longer, consider breaking into helper functions
- Exception: Test functions can be longer for clarity

## Comments

### When to Comment

- **Why, not what**: Explain reasoning, not obvious code
- **Complex logic**: Explain non-obvious algorithms
- **TODO/FIXME**: Mark future work clearly

```python
# Good
# Use regex to avoid issues with multi-byte UTF-8 characters
pattern = r'^---\s*\n(.*?)\n---\s*\n'

# Bad
# Create a pattern
pattern = r'^---\s*\n(.*?)\n---\s*\n'
```

### Comment Style

```python
# Single line comments use hash

"""
Multi-line explanations
use triple-quoted strings
"""
```

## Logging Standards

Use the shared `log()` function with appropriate levels:

```python
from doc_test_utils import log

# Informational output (console only)
log("Processing 10 files...", "info")

# Notices (console + annotation when use_actions=True)
log("No exceptions found", "notice", file_path, None, use_actions, action_level)

# Warnings (console + annotation)
log("Deprecated syntax detected", "warning", file_path, line_num, use_actions, action_level)

# Errors (console + annotation)
log("Invalid YAML syntax", "error", file_path, line_num, use_actions, action_level)

# Success messages (console only)
log("All tests passed", "success")
```

## String Formatting

Use f-strings for string formatting (Python 3.6+):

```python
# Good
message = f"Found {count} exceptions in {filename}"
path = f"{base_dir}/{subdir}/{file}"

# Acceptable for single substitutions
message = "Error: " + error_msg

# Bad
message = "Found %d exceptions in %s" % (count, filename)
message = "Found {} exceptions in {}".format(count, filename)
```

## List Comprehensions

Use list comprehensions for simple transformations:

```python
# Good
valid_files = [f for f in files if f.endswith('.md')]
names = [item.name for item in items]

# Bad (too complex)
result = [process(item) if validate(item) else default(item) 
          for item in items if item.active and item.count > 0]

# Better (break into steps)
active_items = [item for item in items if item.active and item.count > 0]
result = [process(item) if validate(item) else default(item) 
          for item in active_items]
```

## Testing Code Style

### Test Function Names

Start with `test_` and describe what is being tested:

```python
# Good
def test_parse_front_matter():
def test_parse_front_matter_with_invalid_yaml():
def test_log_github_actions_annotations():

# Bad
def front_matter_test():
def test1():
def test_stuff():
```

### Test Structure

Follow Arrange-Act-Assert pattern:

```python
def test_parse_front_matter():
    # Arrange
    content = "---\nlayout: default\n---\n# Test"
    
    # Act
    metadata = parse_front_matter(content)
    
    # Assert
    assert metadata is not None
    assert metadata['layout'] == 'default'
```

### Assertion Messages

Provide helpful failure messages:

```python
# Good
assert count == 5, f"Expected 5 exceptions, got {count}"
assert metadata is not None, "Should parse valid front matter"

# Bad
assert count == 5
assert metadata is not None
```

## Code Organization Within Files

### Order of Elements

1. Shebang and encoding (if script)
2. Module docstring
3. Imports (stdlib, third-party, local)
4. Constants
5. Helper functions (private)
6. Public functions
7. Main execution block

```python
#!/usr/bin/env python3
"""
Module docstring here.
"""

import sys
import re
from pathlib import Path

from doc_test_utils import log

MAX_FILE_SIZE = 1000000

def _internal_helper():
    """Private helper function."""
    pass

def public_function():
    """Public API function."""
    pass

if __name__ == "__main__":
    main()
```

## Avoid

- **Global mutable state**: Use parameters and return values
- **Bare except clauses**: Always specify exception types
- **Magic numbers**: Use named constants
- **Deep nesting**: Refactor if more than 3 levels
- **Long lines**: Keep under 100 characters when practical

## Tools

- **Formatter**: Consider using `black` for automatic formatting
- **Linter**: Use `pylint` or `flake8` for code quality
- **Type checker**: Use `mypy` for type hint validation

## Remember

- **Consistency matters more than perfection**
- **When in doubt, follow PEP 8**
- **Prioritize readability over cleverness**
- **Update this guide as patterns emerge**
