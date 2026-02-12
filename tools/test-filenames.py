#!/usr/bin/env python3
"""
Validate filenames in changed files list for unsafe characters.

This script checks filenames from the CHANGED_FILES environment variable
for characters that could cause security issues or break shell commands.

Usage:
    test-filenames.py [--action LEVEL]

Environment:
    CHANGED_FILES: Comma-separated list of changed filenames
"""

import os
import re
import sys
import argparse
from typing import List

# Import shared utilities
from doc_test_utils import log


def get_changed_files() -> List[str]:
    """
    Get list of changed files from environment variable.
    
    Returns:
        List of filenames from CHANGED_FILES, or empty list if not set
        
    Example:
        >>> os.environ['CHANGED_FILES'] = 'file1.py, file2.md'
        >>> files = get_changed_files()
        >>> len(files)
        2
    """
    changed = os.environ.get('CHANGED_FILES', '')
    if not changed:
        return []
    
    return [f.strip() for f in changed.split(',') if f.strip()]


def validate_filenames(files: List[str]) -> List[str]:
    """
    Check filenames for unsafe characters.
    
    Unsafe characters include:
    - Whitespace
    - Shell metacharacters: , * ? [ ] | & ; $ ` " ' < > ( )
    - Path separators: \\ (backslash)
    - Colon (Windows drive separator issues)
    
    Args:
        files: List of filenames to validate
        
    Returns:
        List of filenames containing unsafe characters
        
    Example:
        >>> validate_filenames(['safe.py', 'un safe.py', 'bad;file.md'])
        ['un safe.py', 'bad;file.md']
    """
    # Pattern matches any unsafe character
    unsafe = re.compile(r"[\s,\*\?\[\]\|\&;\$`\"'<>():\\]")
    
    bad_files = []
    for filename in files:
        if unsafe.search(filename):
            bad_files.append(filename)
    
    return bad_files


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Validate filenames in changed files list for unsafe characters.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Normal output
  %(prog)s --action warning             # GitHub Actions output (warnings)
  %(prog)s --action error               # GitHub Actions output (errors only)

Environment:
  CHANGED_FILES    Comma-separated list of changed filenames
        """
    )
    
    parser.add_argument(
        '--action', '-a',
        type=str,
        nargs='?',
        const='warning',
        default=None,
        choices=['all', 'warning', 'error'],
        help='Output GitHub Actions annotations at specified level (all, warning, error)'
    )
    
    args = parser.parse_args()
    
    use_actions = args.action is not None
    action_level = args.action or 'warning'
    
    # Get changed files from environment
    files = get_changed_files()
    for f in files:
        log(f"Changed file to check: {f}", "info")
    
    if not files:
        log("No changed files reported", "info")
        sys.exit(0)
    
    log(f"Checking {len(files)} changed files for unsafe characters", "info")
    
    # Validate filenames
    unsafe_files = validate_filenames(files)
    
    if unsafe_files:
        # Log each unsafe filename
        log("Unsafe filenames detected:", "error")
        for filename in unsafe_files:
            log(f"  {filename}", "error")
        
        # Create GitHub Actions annotation
        log(f"Found {len(unsafe_files)} unsafe filenames in changed-files list",
            "error",
            None,
            None,
            use_actions,
            action_level)
        
        sys.exit(1)
    
    # Success case
    log("No unsafe filenames found", "success")
    
    if use_actions and action_level == 'all':
        log("All filenames passed validation",
            "notice",
            None,
            None,
            use_actions,
            action_level)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
# End of test_filenames.py