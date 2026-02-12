#!/usr/bin/env python3
"""
Count unique markdown notation patterns in files.

Usage:
    markdown-survey.py <file1> [file2 ...] [--action LEVEL]

This tool analyzes markdown files to count:
- Words (excluding code, HTML, and markdown notation)
- Markdown notation patterns (headings, lists, links, etc.)
- Unique notation types used

Examples:
    # Single file
    markdown-survey.py README.md
    
    # Multiple files
    markdown-survey.py file1.md file2.md file3.md
    
    # With glob expansion
    markdown-survey.py docs/*.md
    
    # GitHub Actions mode (level required)
    markdown-survey.py docs/*.md --action warning
    markdown-survey.py docs/*.md --action all
"""

import sys
import re
import argparse
from pathlib import Path

from doc_test_utils import read_markdown_file, log


def count_words(content: str) -> int:
    """
    Count words in markdown content, excluding code blocks and HTML.
    
    Algorithm:
    1. Remove fenced code blocks (```...```)
    2. Remove inline code (`...`)
    3. Remove HTML tags
    4. Remove markdown notation characters
    5. Split on whitespace and count non-empty tokens
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        Number of prose words in the content
        
    Example:
        >>> content = "# Heading\\n\\nThis is **bold** text with `code`."
        >>> count_words(content)
        5
    """
    # Remove fenced code blocks
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove image syntax entirely (must be before link removal)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    
    # Remove URLs from links but keep link text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove markdown notation characters
    text = re.sub(r'[#*_~`\[\]()>|+-]', ' ', text)
    
    # Split and count non-empty words
    words = [w for w in text.split() if w.strip()]
    
    return len(words)


def list_markdown_notations(content: str) -> list:
    """
    Extract and count markdown notation patterns.
    
    Patterns assume markdownlint compliance:
    - Headings have space after #
    - Lists have proper spacing
    - Horizontal rules are on their own lines
    
    Args:
        content: Full markdown file content as string
        
    Returns:
        List of notation names found (may contain duplicates)
        
    Example:
        >>> content = "# Heading\\n\\n**bold** and `code`"
        >>> notations = list_markdown_notations(content)
        >>> 'heading_1' in notations
        True
        >>> 'bold_asterisk' in notations
        True
    """
    patterns = {
        # Headings (1-6 levels) - must have space after
        r'^#\s': 'heading_1',
        r'^##\s': 'heading_2',
        r'^###\s': 'heading_3',
        r'^####\s': 'heading_4',
        r'^#####\s': 'heading_5',
        r'^######\s': 'heading_6',
        
        # Bold
        r'\*\*': 'bold_asterisk',
        r'__': 'bold_underscore',
        
        # Italic
        r'(?<!\*)\*(?!\*)': 'italic_asterisk',
        r'(?<!_)_(?!_)': 'italic_underscore',
        
        # Code
        r'```': 'code_block',
        r'`': 'inline_code',
        
        # Links and images
        r'!\[.*?\]\(.*?\)': 'image',
        r'(?<!!)\[.*?\]\(.*?\)': 'link',
        
        # Blockquote - must have space after >
        r'^>\s': 'blockquote',
        
        # Lists - markdownlint requires space after marker
        r'^\s*[-*+]\s': 'unordered_list',
        r'^\s*\d+\.\s': 'ordered_list',
        
        # Horizontal rule - must be on own line
        r'^(\*{3,}|-{3,}|_{3,})$': 'horizontal_rule',
        
        # Strikethrough
        r'~~': 'strikethrough',
        
        # Tables
        r'\|': 'table_pipe',
    }
    
    found_notations = []
    
    for line in content.split('\n'):
        for pattern, notation_name in patterns.items():
            if re.search(pattern, line, re.MULTILINE):
                found_notations.append(notation_name)
    
    return found_notations


def main():
    """Main entry point for the markdown survey tool."""
    parser = argparse.ArgumentParser(
        description='Count markdown notation patterns and words in a file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                         # Single file, normal output
  %(prog)s file1.md file2.md file3.md        # Multiple files
  %(prog)s docs/*.md                         # Glob expansion (shell)
  %(prog)s docs/*.md --action warning        # GitHub Actions mode
  %(prog)s docs/*.md --action all            # All annotations
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=str,
        help='Path(s) to the markdown file(s) to analyze'
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
    
    # Track overall status and aggregates
    failed_files = []
    total_files = len(args.files)
    
    # Aggregates across all files
    total_words = 0
    total_notations = 0
    all_unique_notations = set()
    
    use_actions = args.action is not None
    action_level = args.action or 'warning'
    
    # Progress message for multiple files
    if total_files > 1:
        log(f"Analyzing {total_files} markdown file(s)...", "info")
    
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
        
        # Count words and notations for this file
        word_count = count_words(content)
        markdown_notations = list_markdown_notations(content)
        markdown_notation_count = len(markdown_notations)
        unique_notations = set(markdown_notations)
        unique_notation_count = len(unique_notations)
        unique_notation_list = ', '.join(sorted(unique_notations))
        
        # Format output message for this file
        message = (f"{filepath.name}: {word_count} words, "
                   f"{markdown_notation_count} markdown_symbols, "
                   f"{unique_notation_count} unique_codes: {unique_notation_list}")
        
        # Output results for this file
        if use_actions:
            log(message, "notice", str(filepath), None, True, action_level)
        else:
            log(message, "info")
        
        # Aggregate for summary
        total_words += word_count
        total_notations += markdown_notation_count
        all_unique_notations.update(unique_notations)
    
    # Final summary for multiple files
    if total_files > 1:
        files_processed = total_files - len(failed_files)
        all_unique_count = len(all_unique_notations)
        all_unique_list = ', '.join(sorted(all_unique_notations))
        
        summary = (f"Summary: {files_processed} files, {total_words} total words, "
                   f"{total_notations} total markdown_symbols, "
                   f"{all_unique_count} unique_codes across all files: {all_unique_list}")
        
        log(summary, "info")
        
        if use_actions and action_level == 'all':
            log(f"Analyzed {files_processed} files: {total_words} words, {total_notations} symbols",
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


"""
Word count algorithm rationale:

The algorithm excludes content that isn't "document words":
1. **Code blocks removed** - not prose
2. **Inline code removed** - typically technical identifiers, not words
3. **HTML tags removed** - markup, not content
4. **Link URLs removed** - keep link text (those are words), discard URLs
5. **Images removed entirely** - alt text is often filenames/technical
6. **Markdown notation stripped** - removes #, *, _, etc.

This gives a count of actual prose words in the document.

Alternative algorithms to consider:

- **More inclusive**: Keep inline code, alt text → higher counts, includes all visible text
- **More strict**: Remove headings, emphasis entirely → lower counts, only body text
- **Simple split**: Just `len(content.split())` → fastest but counts everything including URLs

The current approach balances "words a human reader would read as prose" while being 
deterministic and fast.

Example output:

README.md: 1247 words, 342 markdown_symbols, 8 unique_codes: bold_asterisk, code_block, 
heading_1, heading_2, inline_code, link, ordered_list, table_pipe, unordered_list
"""
# end of markdown-survey.py