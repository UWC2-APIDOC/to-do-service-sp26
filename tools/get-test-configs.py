#!/usr/bin/env python3
"""
Group markdown files by their test configuration.

This script parses front matter from multiple markdown files and groups them
by their test configuration (test_apps, server_url, local_database) for batch
testing. Files without valid test configuration are skipped.

Usage:
    get-test-configs.py --output <format> <file1> [file2 ...]

Examples:
    # JSON output
    python3 get-test-configs.py --output json docs/*.md
    
    # Shell variables output
    python3 get-test-configs.py --output shell docs/*.md
    
    # Use in workflow
    eval "$(python3 tools/get-test-configs.py --output shell docs/*.md)"
    echo $GROUP_1_FILES
    
Exit Codes:
    0: Success (even if no testable files found)
    1: Error occurred
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Any

# Import shared utilities
from doc_test_utils import (
    read_markdown_file,
    parse_front_matter,
    get_server_database_key
)
import help_urls


def group_files_by_config(filepaths: List[Path]) -> Dict[Tuple, List[str]]:
    """
    Group files by their test configuration.
    
    Args:
        filepaths: List of markdown file paths
        
    Returns:
        Dictionary mapping config tuples to file lists
        Config tuple: (test_apps, server_url, local_database)
        
    Example:
        >>> files = [Path('file1.md'), Path('file2.md')]
        >>> groups = group_files_by_config(files)
        >>> len(groups) >= 0
        True
    """
    groups = {}
    skipped_files = []
    
    for filepath in filepaths:
        # Read and parse file
        content = read_markdown_file(filepath)
        if content is None:
            skipped_files.append((str(filepath), "Unable to read file"))
            continue
        
        metadata = parse_front_matter(content)
        if metadata is None:
            skipped_files.append((str(filepath), "No valid front matter"))
            continue
        
        # Get test configuration using shared utility
        test_apps, server_url, local_database = get_server_database_key(metadata)
        
        # Skip files without local_database (required field)
        if local_database is None:
            skipped_files.append((str(filepath), "Missing required field 'local_database'"))
            continue
        
        # Create config tuple for grouping
        config_key = (test_apps, server_url, local_database)
        
        # Add file to group
        if config_key not in groups:
            groups[config_key] = []
        groups[config_key].append(str(filepath))
    
    # Report skipped files to stderr (doesn't interfere with stdout output)
    if skipped_files:
        print(f"\nWarning: Skipped {len(skipped_files)} file(s) without valid test configuration:", file=sys.stderr)
        for filepath, reason in skipped_files:
            print(f"  - {filepath}: {reason}", file=sys.stderr)
        print(f"\nNote: Files need front matter with 'test.local_database' field to be included.", file=sys.stderr)
        print(f"See: {help_urls.HELP_URLS['front_matter']}\n", file=sys.stderr)
    
    return groups


def output_json(groups: Dict[Tuple, List[str]]) -> str:
    """
    Format groups as JSON.
    
    Args:
        groups: Dictionary of config tuples to file lists
        
    Returns:
        JSON string
        
    Example:
        >>> groups = {('app', 'url', 'db'): ['file1.md']}
        >>> output = output_json(groups)
        >>> 'groups' in output
        True
    """
    result = {"groups": []}
    
    for (test_apps, server_url, local_database), files in groups.items():
        group = {
            "test_apps": test_apps,
            "server_url": server_url,
            "local_database": local_database,
            "files": files
        }
        result["groups"].append(group)
    
    return json.dumps(result, indent=2)


def output_shell(groups: Dict[Tuple, List[str]]) -> str:
    """
    Format groups as shell variables.
    
    Args:
        groups: Dictionary of config tuples to file lists
        
    Returns:
        Shell variable assignments
        
    Example:
        >>> groups = {('app', 'url', 'db'): ['file1.md']}
        >>> output = output_shell(groups)
        >>> 'GROUP_1_' in output
        True
    """
    lines = []
    
    for idx, ((test_apps, server_url, local_database), files) in enumerate(groups.items(), 1):
        lines.append(f"# Group {idx}")
        lines.append(f'GROUP_{idx}_TEST_APPS="{test_apps or ""}"')
        lines.append(f'GROUP_{idx}_SERVER_URL="{server_url or ""}"')
        lines.append(f'GROUP_{idx}_LOCAL_DATABASE="{local_database or ""}"')
        lines.append(f'GROUP_{idx}_FILES="{" ".join(files)}"')
        lines.append("")
    
    lines.append(f"# Metadata")
    lines.append(f"GROUP_COUNT={len(groups)}")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Group markdown files by test configuration.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --output json docs/*.md
  %(prog)s --output shell docs/*.md
  
  # Use in workflow with shell output
  eval "$(%(prog)s --output shell docs/*.md)"
  echo $GROUP_1_FILES
        """
    )
    
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        choices=['json', 'shell'],
        help='Output format: json or shell variables'
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=str,
        help='Markdown files to process'
    )
    
    args = parser.parse_args()
    
    # Convert file paths to Path objects
    filepaths = [Path(f) for f in args.files]
    
    # Group files by configuration
    groups = group_files_by_config(filepaths)
    
    # Warn if no files were grouped (helpful for new users)
    if not groups:
        print("\nWarning: No files with valid test configuration found.", file=sys.stderr)
        print("Files must have front matter with 'test.local_database' field.", file=sys.stderr)
        print(f"See: {help_urls.HELP_URLS['front_matter']}\n", file=sys.stderr)
    
    # Output in requested format
    # Note: Data goes to stdout (clean for piping), errors/warnings to stderr
    if args.output == 'json':
        print(output_json(groups))
    elif args.output == 'shell':
        print(output_shell(groups))
    
    sys.exit(0)


if __name__ == "__main__":
    main()
# End of file tools/get-test-configs.py