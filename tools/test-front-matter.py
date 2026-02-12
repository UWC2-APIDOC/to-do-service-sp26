#!/usr/bin/env python3
"""
Command-line tool to test front matter parsing.

Usage:
    python3 test-front-matter.py <filename>
    python3 test-front-matter.py <filename> --verbose
    
Examples:
    python3 test-front-matter.py docs/api.md
    python3 test-front-matter.py docs/api.md --verbose
"""

import sys
import argparse
from pathlib import Path

# Import from doc_test_utils
sys.path.insert(0, str(Path(__file__).parent))
from doc_test_utils import parse_front_matter_with_errors, read_markdown_file


def main():
    parser = argparse.ArgumentParser(
        description='Test front matter parsing on a markdown file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/api.md
  %(prog)s docs/api.md --verbose
        """
    )
    
    parser.add_argument(
        'filename',
        type=str,
        help='Path to the markdown file to test'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show full front matter content'
    )
    
    args = parser.parse_args()
    
    filepath = Path(args.filename)
    
    # Read file
    print(f"Testing: {filepath}")
    print("=" * 60)
    
    content = read_markdown_file(filepath)
    if content is None:
        print("✗ ERROR: Could not read file")
        sys.exit(1)
    
    # Parse front matter
    metadata, error_msg, error_line = parse_front_matter_with_errors(content)
    
    if metadata is None:
        # Parsing failed
        print("✗ FRONT MATTER PARSING FAILED")
        print()
        if error_line:
            print(f"Error on line {error_line}:")
        print(error_msg)
        sys.exit(1)
    
    # Parsing succeeded
    print("✓ FRONT MATTER PARSED SUCCESSFULLY")
    print()
    
    if args.verbose:
        print("Full front matter content:")
        print("-" * 60)
        import yaml
        print(yaml.dump(metadata, default_flow_style=False, sort_keys=False))
    else:
        print(f"Found {len(metadata)} field(s):")
        for key in metadata.keys():
            value = metadata[key]
            # Truncate long values
            if isinstance(value, str) and len(value) > 50:
                value_display = value[:47] + "..."
            elif isinstance(value, (list, dict)):
                value_display = f"<{type(value).__name__}>"
            else:
                value_display = value
            print(f"  - {key}: {value_display}")
        
        print()
        print("Use --verbose to see full content")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
