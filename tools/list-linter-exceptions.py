#!/usr/bin/env python3
"""
Scan Markdown files for Vale and markdownlint exception tags.

Usage:
    list-linter-exceptions.py <file1> [file2 ...] [--action LEVEL]

Examples:
    # Single file
    list-linter-exceptions.py README.md
    
    # Multiple files
    list-linter-exceptions.py file1.md file2.md file3.md
    
    # With glob expansion (shell expands)
    list-linter-exceptions.py docs/*.md
    
    # GitHub Actions mode (level required)
    list-linter-exceptions.py docs/*.md --action warning
    list-linter-exceptions.py docs/*.md --action error

Note: Does not test front matter sections.
Note: Ignores exceptions inside fenced code blocks (```, ~~~).
"""

import sys
import re
import argparse
from pathlib import Path

# Import shared utilities
from doc_test_utils import read_markdown_file, log


def list_vale_exceptions(content):
    """
    Scan for Vale and markdownlint exception tags.
    
    Ignores exception comments inside fenced code blocks to prevent
    false positives from documentation examples.
    
    Detects:
    - Vale specific rules: <!-- vale RuleName = NO -->
    - Vale global disable: <!-- vale off -->
    - MarkdownLint specific rules: <!-- markdownlint-disable MD### -->
    - MarkdownLint global disable: <!-- markdownlint-disable -->
    
    Args:
        content: Markdown file content as string
    
    Returns:
        dict: {
            'vale': [{'line': int, 'rule': str, 'full_match': str}, ...],
            'markdownlint': [{'line': int, 'rule': str, 'full_match': str}, ...]
        }
    """
    exceptions = {
        'vale': [],
        'markdownlint': []
    }
    
    # Patterns for linter exceptions
    # Vale: <!-- vale RuleName = NO --> (specific rule)
    vale_specific_pattern = r'<!--\s*vale\s+([A-Za-z0-9.]+)\s*=\s*NO\s*-->'
    
    # Vale: <!-- vale off --> (global disable)
    vale_global_pattern = r'<!--\s*vale\s+off\s*-->'
    
    # MarkdownLint: <!-- markdownlint-disable MD### --> (specific rule)
    markdown_specific_pattern = r'<!--\s*markdownlint-disable\s+(MD\d{3})\s*-->'
    
    # MarkdownLint: <!-- markdownlint-disable --> (global disable)
    markdown_global_pattern = r'<!--\s*markdownlint-disable\s*-->'
    
    # Pattern for fenced code blocks
    # Matches opening: ```lang or ~~~ or ````markdown etc.
    fence_pattern = r'^(`{3,}|~{3,})'
    
    lines = content.split('\n')
    
    # Track code block state
    in_code_block = False
    fence_char = None
    fence_count = 0
    
    for line_num, line in enumerate(lines, start=1):
        # Check for code block fences
        fence_match = re.match(fence_pattern, line)
        
        if fence_match:
            fence = fence_match.group(1)
            current_char = fence[0]  # ` or ~
            current_count = len(fence)
            
            if not in_code_block:
                # Opening fence
                in_code_block = True
                fence_char = current_char
                fence_count = current_count
            elif current_char == fence_char and current_count >= fence_count:
                # Closing fence (same char, equal or more)
                in_code_block = False
                fence_char = None
                fence_count = 0
            # If different char or fewer, it's content inside the block
            
            # Skip exception detection on fence lines
            continue
        
        # Skip exception detection if inside code block
        if in_code_block:
            continue
        
        # Check for Vale specific rule exceptions
        vale_specific_match = re.search(vale_specific_pattern, line)
        if vale_specific_match:
            exceptions['vale'].append({
                'line': line_num,
                'rule': vale_specific_match.group(1),
                'full_match': line.strip()
            })
        
        # Check for Vale global disable
        vale_global_match = re.search(vale_global_pattern, line)
        if vale_global_match:
            exceptions['vale'].append({
                'line': line_num,
                'rule': 'vale-off (global)',
                'full_match': line.strip()
            })
        
        # Check for markdownlint specific rule exceptions
        md_specific_match = re.search(markdown_specific_pattern, line)
        if md_specific_match:
            exceptions['markdownlint'].append({
                'line': line_num,
                'rule': md_specific_match.group(1),
                'full_match': line.strip()
            })
        
        # Check for markdownlint global disable
        md_global_match = re.search(markdown_global_pattern, line)
        if md_global_match:
            exceptions['markdownlint'].append({
                'line': line_num,
                'rule': 'markdownlint-disable (global)',
                'full_match': line.strip()
            })
    
    return exceptions


def output_normal(filepath, exceptions):
    """Output in normal format for interactive use."""
    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    log(f"{filepath.name}: {vale_count} Vale exceptions, {md_count} markdownlint exceptions", "info")
    
    # If no exceptions, add a notice
    if vale_count == 0 and md_count == 0:
        log("No Vale or markdownlint exceptions found.", "info")
        return
    
    if vale_count > 0:
        log("Vale exceptions:", "info")
        for exc in exceptions['vale']:
            log(f"  Line {exc['line']}: {exc['rule']}", "info")
    else:
        log("No Vale exceptions found.", "info")
    
    if md_count > 0:
        log("MarkdownLint exceptions:", "info")
        for exc in exceptions['markdownlint']:
            log(f"  Line {exc['line']}: {exc['rule']}", "info")
    else:
        log("No markdownlint exceptions found.", "info")


def output_action(filepath, exceptions, action_level):
    """Output in GitHub Actions format with annotations."""
    vale_count = len(exceptions['vale'])
    md_count = len(exceptions['markdownlint'])
    
    # Summary line to console (always shown)
    log(f"{filepath.name}: {vale_count} Vale exceptions, {md_count} markdownlint exceptions", 
        "info")
    
    # If no exceptions, add a notice
    if vale_count == 0 and md_count == 0:
        log("No Vale or markdownlint exceptions found.",
            "notice",
            str(filepath),
            None,
            True,
            action_level)
        return
    
    if vale_count > 0:
        # Annotate each exception
        for exc in exceptions['vale']:
            log(f"Vale exception: {exc['rule']}",
                "warning",
                str(filepath),
                exc['line'],
                True,
                action_level)
    else:
        log("No Vale exceptions found.",
            "notice",
            str(filepath),
            None,
            True,
            action_level)
    
    if md_count > 0:
        # Annotate each exception
        for exc in exceptions['markdownlint']:
            log(f"MarkdownLint exception: {exc['rule']}",
                "warning",
                str(filepath),
                exc['line'],
                True,
                action_level)
    else:
        log("No markdownlint exceptions found.",
            "notice",
            str(filepath),
            None,
            True,
            action_level)
    
    # Overall summary annotation
    if vale_count + md_count > 0:
        log(f"Found {vale_count} Vale and {md_count} markdownlint exceptions",
            "notice",
            str(filepath),
            None,
            True,
            action_level)


def main():
    parser = argparse.ArgumentParser(
        description='Scan Markdown files for Vale and markdownlint exception tags.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                         # Single file, normal output
  %(prog)s file1.md file2.md file3.md        # Multiple files
  %(prog)s docs/*.md                         # Glob expansion (shell)
  %(prog)s docs/*.md --action warning        # GitHub Actions mode
  %(prog)s docs/*.md --action error          # Only error annotations
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=str,
        help='Path(s) to the Markdown file(s) to scan'
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
    
    # Track overall status
    all_exceptions = {'vale': [], 'markdownlint': []}
    failed_files = []
    total_files = len(args.files)
    
    use_actions = args.action is not None
    action_level = args.action or 'warning'
    
    # Progress message
    if total_files > 1:
        log(f"Scanning {total_files} file(s) for linter exceptions...", "info")
    
    # Process each file
    for idx, filename in enumerate(args.files, 1):
        filepath = Path(filename)
        
        # Progress indicator for multiple files
        if total_files > 1:
            log(f"[{idx}/{total_files}] Processing {filepath.name}", "info")
        
        # Read file using shared utility
        content = read_markdown_file(filepath)
        if content is None:
            failed_files.append(str(filepath))
            log(f"Failed to read {filepath}",
                "error",
                str(filepath),
                None,
                use_actions,
                action_level)
            continue
        
        # Scan for exceptions
        exceptions = list_vale_exceptions(content)
        
        # Output results for this file
        if args.action:
            output_action(filepath, exceptions, action_level)
        else:
            output_normal(filepath, exceptions)
        
        # Aggregate for summary
        all_exceptions['vale'].extend(exceptions['vale'])
        all_exceptions['markdownlint'].extend(exceptions['markdownlint'])
    
    # Final summary for multiple files
    if total_files > 1:
        total_vale = len(all_exceptions['vale'])
        total_md = len(all_exceptions['markdownlint'])
        
        log(f"Summary: {total_vale} Vale, {total_md} markdownlint exceptions across {total_files} files",
            "info")
        
        if use_actions and action_level == 'all':
            log(f"Scanned {total_files} files: {total_vale} Vale, {total_md} markdownlint exceptions total",
                "notice",
                None,
                None,
                True,
                action_level)
    
    # Exit with error if any files failed
    if failed_files:
        log(f"Failed to process {len(failed_files)} file(s)", "error")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
# End of file tools/list-linter-exceptions.py