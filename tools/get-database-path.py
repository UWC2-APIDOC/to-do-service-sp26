#!/usr/bin/env python3
"""
Extract database path from markdown file's front matter.

This script reads a markdown file's front matter and extracts the local_database
path for API testing. If no valid test configuration is found, the script exits
with non-zero status.

Usage:
    get-database-path.py <filename>

Examples:
    # Get database path
    python3 get-database-path.py docs/api.md
    
    # Use in workflow
    DB_PATH=$(python3 tools/get-database-path.py docs/api.md)
    
Exit Codes:
    0: Valid test configuration found, database path printed to stdout
    1: No valid test configuration or error occurred
"""

import sys
from pathlib import Path
from typing import Optional

# Import shared utilities
from doc_test_utils import read_markdown_file, parse_front_matter, get_test_config


def get_database_path(filepath: Path) -> Optional[str]:
    """
    Extract database path from file's front matter.
    
    Args:
        filepath: Path to markdown file
        
    Returns:
        Database path string, or None if not found
        
    Example:
        >>> path = get_database_path(Path('docs/api.md'))
        >>> path
        'api/to-do-db-source.json'
    """
    # Read file
    content = read_markdown_file(filepath)
    if content is None:
        return None
    
    # Parse front matter
    metadata = parse_front_matter(content)
    if metadata is None:
        return None
    
    # Get test config
    test_config = get_test_config(metadata)
    if not test_config:
        return None
    
    # Extract database path (required field)
    db_path = test_config.get('local_database')
    if not db_path:
        return None
    
    # Strip leading slash if present
    if db_path.startswith('/'):
        db_path = db_path[1:]
    
    return db_path


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Error: Exactly one filename required", file=sys.stderr)
        print("Usage: get-database-path.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    db_path = get_database_path(filepath)
    
    if db_path is None:
        # No output, just exit with error code
        sys.exit(1)
    
    # Output database path to stdout
    print(db_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
# End of file tools/get-database-path.py