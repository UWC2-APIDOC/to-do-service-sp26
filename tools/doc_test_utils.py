#!/usr/bin/env python3
"""
Shared utilities for documentation testing tools.

This module provides common functions for:
- Parsing YAML front matter from markdown files
- Reading markdown files with error handling
- Extracting test configuration from front matter
- Unified logging with GitHub Actions annotation support
"""

import re
import yaml
from pathlib import Path
from typing import Optional, Dict, Tuple, Any

# Import help URLs from centralized config
from help_urls import HELP_URLS

def parse_front_matter_with_errors(content: str) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[int]]:
    """
    Extract and parse YAML front matter from markdown content with detailed error reporting.
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        Tuple of (metadata_dict, error_message, error_line)
        - metadata_dict: Dictionary if successful, None if failed
        - error_message: Detailed error description if failed, None if successful
        - error_line: Line number where error occurred (for YAML errors), None otherwise
        
    Example:
        >>> content = "---\\nlayout: default\\n---\\n# Heading"
        >>> metadata, error, line = parse_front_matter_with_errors(content)
        >>> metadata['layout']
        'default'
        
        >>> content = "# No front matter"
        >>> metadata, error, line = parse_front_matter_with_errors(content)
        >>> print(error)
        'No front matter found...'
    """
    # Check for front matter delimiters
    # Spec: "---" must be at start of line (no leading whitespace)
    # followed by optional whitespace and required newline
    # Front matter is the text between the two delimiters
    fm_match = re.match(r'^---[ \t]*\n(.*?)\n---[ \t]*\n?', content, re.DOTALL)
    
    if not fm_match:
        # Provide helpful guidance based on what we found
        
        # Check for leading whitespace before ---
        if re.match(r'^\s+---', content):
            return None, (
                "Front matter delimiter has leading whitespace. "
                "The '---' must be at the start of the line with no spaces or tabs before it."
            ), 1
        
        if content.strip().startswith('---'):
            # Has opening delimiter but not closing
            return None, (
                "Front matter opening delimiter found but no closing delimiter could be found. "
                "Ensure front matter ends with '---' on its own line."
            ), 1
        else:
            # No front matter at all
            return None, (
                "No front matter found. Add YAML front matter between --- delimiters at the start of the file.\n"
                "Example:\n"
                "---\n"
                "layout: default\n"
                "description: Your description here\n"
                "---"
            ), 1
    
    # Try to parse YAML
    try:
        metadata = yaml.safe_load(fm_match.group(1))
        return metadata, None, None
    except yaml.YAMLError as e:
        # Extract line number from YAML error if available
        error_line = None
        try:
            if hasattr(e, 'problem_mark') and e.problem_mark is not None:
                # YAML parser provides line/column info
                # problem_mark.line is 0-indexed, +1 for 1-indexed, +1 for opening ---
                error_line = e.problem_mark.line + 2  # type: ignore[attr-defined]
        except (AttributeError, TypeError):
            # If we can't get line number, that's okay, too.
            pass
        
        # Build helpful error message
        error_msg = f"Invalid YAML syntax in front matter: {str(e)}"
        
        if error_line:
            error_msg += f"\nError on or near line {error_line}."
        
        error_msg += (
            "\n\nCommon YAML issues:\n"
            "- Inconsistent indentation (use spaces, not tabs)\n"
            "- Unclosed quotes or brackets\n"
            "- Missing colons after keys"
        )
        
        return None, error_msg, error_line


def parse_front_matter(content: str) -> Optional[Dict[str, Any]]:
    """
    Extract and parse YAML front matter from markdown content.
    
    This is the backward-compatible version that only returns the metadata dict.
    For detailed error reporting, use parse_front_matter_with_errors() instead.
    
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
    metadata, _, _ = parse_front_matter_with_errors(content)
    return metadata


def read_markdown_file(filepath: Path) -> Optional[str]:
    """
    Read a markdown file with proper error handling.
    
    Args:
        filepath: Path to the markdown file
        
    Returns:
        File content as string, or None if error occurred
        
    Example:
        >>> from pathlib import Path
        >>> content = read_markdown_file(Path('README.md'))
        >>> if content:
        ...     print(f"Read {len(content)} characters")

    Note:
        Errors are logged but not raised. Caller should check for None.
    """
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


def get_test_config(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract test configuration from front matter metadata.
    
    Args:
        metadata: Parsed front matter dictionary
        
    Returns:
        Test configuration dictionary, or empty dict if not present
        
    Example:
        >>> metadata = {'test': {'testable': ['GET example'], 'server_url': 'localhost:3000'}}
        >>> config = get_test_config(metadata)
        >>> config['server_url']
        'localhost:3000'
    """
    return metadata.get('test', {})


def get_server_database_key(metadata: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extract server and database configuration for grouping test files.
    
    Args:
        metadata: Parsed front matter dictionary
        
    Returns:
        Tuple of (test_apps, server_url, local_database)
        Any value may be None if not present in metadata
        
    Example:
        >>> metadata = {
        ...     'test': {
        ...         'test_apps': ['json-server@0.17.4'],
        ...         'server_url': 'localhost:3000',
        ...         'local_database': '/api/test.json'
        ...     }
        ... }
        >>> apps, url, db = get_server_database_key(metadata)
        >>> db
        '/api/test.json'
    """
    test_config = get_test_config(metadata)
    
    # Get test_apps as comma-separated string (for grouping)
    test_apps = test_config.get('test_apps')
    if test_apps and isinstance(test_apps, list):
        test_apps = ','.join(test_apps)
    
    server_url = test_config.get('server_url')
    local_database = test_config.get('local_database')
    
    return test_apps, server_url, local_database


def log(message: str,
        level: str = "info",
        file_path: Optional[str] = None,
        line: Optional[int] = None,
        use_actions: bool = False,
        action_level: str = "warning") -> None:
    """
    Print a message to console and optionally output GitHub Actions annotation.
    
    This function provides unified logging for all documentation test tools.
    It supports console output with labels and optional GitHub Actions annotations
    based on message severity and filtering level.
    
    Args:
        message: The message to log
        level: Message severity level. One of:
            - 'info': Informational message (console only)
            - 'notice': Notice message (console + GitHub notice if use_actions=True)
            - 'warning': Warning message (console + GitHub warning if filtered)
            - 'error': Error message (console + GitHub error if filtered)
            - 'success': Success message (console only)
        file_path: Optional file path for GitHub Actions annotations
        line: Optional line number for GitHub Actions annotations
        use_actions: Whether to output GitHub Actions annotations
        action_level: Minimum severity level to output annotations. One of:
            - 'all': Output notice, warning, and error annotations
            - 'warning': Output warning and error annotations (default)
            - 'error': Output only error annotations
    
    Console output:
        Always outputs to console with appropriate label prefix.
        
    GitHub Actions annotation output:
        Only outputs if use_actions=True AND message level meets threshold:
        - If action_level='all': outputs notice, warning, error
        - If action_level='warning': outputs warning, error
        - If action_level='error': outputs only error
        
    Examples:
        >>> log("Processing file...", "info")
        INFO: Processing file...
        
        >>> log("Missing field", "error", "test.md", 5, True, "error")
        ERROR: Missing field
        ::error file=test.md,line=5::Missing field
        
        >>> log("Deprecated syntax", "warning", "test.md", use_actions=True, action_level="warning")
        WARNING: Deprecated syntax
        ::warning file=test.md::Deprecated syntax
    """
    # Severity label mapping for console output
    labels = {
        'info': 'INFO',
        'notice': 'NOTICE',
        'warning': 'WARNING',
        'error': 'ERROR',
        'success': 'SUCCESS'
    }
    
    # Console output (always)
    label = labels.get(level, '')
    console_msg = f"{label}: {message}" if label else message
    print(console_msg)
    
    # GitHub Actions annotation output (conditional)
    if not use_actions:
        return
    
    # Determine if this level should produce an annotation
    severity_order = {'notice': 0, 'warning': 1, 'error': 2}
    threshold_order = {'all': 0, 'warning': 1, 'error': 2}
    
    # info and success never produce annotations
    if level not in severity_order:
        return
    
    message_severity = severity_order.get(level, 0)
    threshold = threshold_order.get(action_level, 1)
    
    if message_severity < threshold:
        return
    
    # Map our levels to GitHub Actions annotation levels
    action_type = 'notice' if level == 'notice' else level
    
    # Build annotation
    parts = [f"::{action_type}"]
    
    properties = []
    if file_path:
        properties.append(f"file={file_path}")
    if line:
        properties.append(f"line={line}")
    
    if properties:
        parts[0] += " " + ",".join(properties)
    
    parts.append(f"::{message}")
    print("".join(parts))
