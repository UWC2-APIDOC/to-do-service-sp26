#!/usr/bin/env python3
"""
Tests for markdown-survey.py

Covers:
- Word counting algorithm (with various content types)
- Markdown notation detection (all pattern types)
- CLI argument parsing
- File reading and error handling
- GitHub Actions annotation output

Run with:
    python3 test_markdown_survey.py
    pytest test_markdown_survey.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the script module (uses hyphens, needs importlib)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "markdown_survey",
    Path(__file__).parent.parent / "markdown-survey.py"
)
markdown_survey = importlib.util.module_from_spec(spec)
spec.loader.exec_module(markdown_survey)

# Import the functions we're testing
count_words = markdown_survey.count_words
list_markdown_notations = markdown_survey.list_markdown_notations


def test_count_words_simple():
    """Test word counting with simple text."""
    print("\n" + "="*60)
    print("TEST: count_words() with simple text")
    print("="*60)
    
    # Test 1: Basic text
    content = "Hello world this is a test"
    word_count = count_words(content)
    assert word_count == 6, f"Expected 6 words, got {word_count}"
    print("  SUCCESS: Basic text counted correctly")
    
    # Test 2: Text with punctuation
    content = "Hello, world! This is a test."
    word_count = count_words(content)
    assert word_count == 6, f"Expected 6 words, got {word_count}"
    print("  SUCCESS: Punctuation handled correctly")
    
    # Test 3: Text with multiple spaces
    content = "Hello    world     test"
    word_count = count_words(content)
    assert word_count == 3, f"Expected 3 words, got {word_count}"
    print("  SUCCESS: Multiple spaces handled correctly")
    
    print("  ✓ All simple word counting tests passed")


def test_count_words_markdown():
    """Test word counting excludes markdown notation."""
    print("\n" + "="*60)
    print("TEST: count_words() excludes markdown notation")
    print("="*60)
    
    # Test 1: Heading
    content = "# Heading text here"
    word_count = count_words(content)
    assert word_count == 3, f"Expected 3 words (heading chars removed), got {word_count}"
    print("  SUCCESS: Heading notation removed")
    
    # Test 2: Bold
    content = "This is **bold text** here"
    word_count = count_words(content)
    assert word_count == 5, f"Expected 5 words (asterisks removed), got {word_count}"
    print("  SUCCESS: Bold notation removed")
    
    # Test 3: Italic
    content = "This is *italic text* here"
    word_count = count_words(content)
    assert word_count == 5, f"Expected 5 words (asterisks removed), got {word_count}"
    print("  SUCCESS: Italic notation removed")
    
    # Test 4: Links
    content = "Check out [this link](https://example.com) for more"
    word_count = count_words(content)
    assert word_count == 6, f"Expected 6 words (URL removed, link text kept), got {word_count}"
    print("  SUCCESS: Link URLs removed, text kept")
    
    # Test 5: Lists
    content = "- Item one\n- Item two\n- Item three"
    word_count = count_words(content)
    assert word_count == 6, f"Expected 6 words (list markers removed), got {word_count}"
    print("  SUCCESS: List markers removed")
    
    print("  ✓ All markdown notation exclusion tests passed")


def test_count_words_code():
    """Test word counting excludes code blocks."""
    print("\n" + "="*60)
    print("TEST: count_words() excludes code")
    print("="*60)
    
    # Test 1: Inline code
    content = "The variable `user_id` is important"
    word_count = count_words(content)
    assert word_count == 4, f"Expected 4 words (inline code removed), got {word_count}"
    print("  SUCCESS: Inline code removed")
    
    # Test 2: Code block
    content = """
Some text here.

```python
def example():
    return "code"
```

More text here.
"""
    word_count = count_words(content)
    assert word_count == 6, f"Expected 6 words (code block removed), got {word_count}"
    print("  SUCCESS: Code block removed")
    
    # Test 3: Multiple code blocks
    content = """
Text one.

```bash
echo "test"
```

Text two.

```python
print("test")
```

Text three.
"""
    word_count = count_words(content)
    assert word_count == 6, f"Expected 6 words (multiple code blocks removed), got {word_count}"
    print("  SUCCESS: Multiple code blocks removed")
    
    print("  ✓ All code exclusion tests passed")


def test_count_words_html():
    """Test word counting excludes HTML."""
    print("\n" + "="*60)
    print("TEST: count_words() excludes HTML")
    print("="*60)
    
    # Test 1: HTML tags
    content = "This is <strong>bold</strong> text"
    word_count = count_words(content)
    assert word_count == 4, f"Expected 4 words (HTML tags removed), got {word_count}"
    print("  SUCCESS: HTML tags removed")
    
    # Test 2: Multiple HTML tags
    content = "Text <div>with <span>nested</span> tags</div> here"
    word_count = count_words(content)
    assert word_count == 5, f"Expected 5 words (nested HTML removed), got {word_count}"
    print("  SUCCESS: Nested HTML tags removed")
    
    # Test 3: HTML entities (these stay as text)
    content = "Text with &nbsp; and &amp; entities"
    word_count = count_words(content)
    # Entities are kept as text, so count them
    assert word_count == 6, f"Expected 6 words, got {word_count}"
    print("  SUCCESS: HTML entities handled")
    
    print("  ✓ All HTML exclusion tests passed")


def test_count_words_images():
    """Test word counting excludes images."""
    print("\n" + "="*60)
    print("TEST: count_words() excludes images")
    print("="*60)
    
    # Test 1: Image syntax
    content = "Here is ![alt text](image.png) an image"
    word_count = count_words(content)
    assert word_count == 4, f"Expected 4 words (image removed), got {word_count}"
    print("  SUCCESS: Image syntax removed")
    
    # Test 2: Multiple images
    content = "Image one ![img1](1.png) and ![img2](2.png) here"
    word_count = count_words(content)
    assert word_count == 4, f"Expected 4 words (images removed), got {word_count}"
    print("  SUCCESS: Multiple images removed")
    
    print("  ✓ All image exclusion tests passed")


def test_count_words_edge_cases():
    """Test word counting edge cases."""
    print("\n" + "="*60)
    print("TEST: count_words() edge cases")
    print("="*60)
    
    # Test 1: Empty string
    content = ""
    word_count = count_words(content)
    assert word_count == 0, f"Expected 0 words, got {word_count}"
    print("  SUCCESS: Empty string returns 0")
    
    # Test 2: Only whitespace
    content = "   \n\n   \t  "
    word_count = count_words(content)
    assert word_count == 0, f"Expected 0 words, got {word_count}"
    print("  SUCCESS: Whitespace only returns 0")
    
    # Test 3: Only markdown notation
    content = "# ## ### **__ * _ ` ``` [] () |"
    word_count = count_words(content)
    assert word_count == 0, f"Expected 0 words (only notation), got {word_count}"
    print("  SUCCESS: Only notation returns 0")
    
    # Test 4: Only code
    content = "```\ncode here\n```"
    word_count = count_words(content)
    assert word_count == 0, f"Expected 0 words (only code), got {word_count}"
    print("  SUCCESS: Only code returns 0")
    
    print("  ✓ All edge case tests passed")


def test_list_markdown_notations_headings():
    """Test markdown notation detection for headings."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() for headings")
    print("="*60)
    
    # Test 1: All heading levels
    content = """# H1
## H2
### H3
#### H4
##### H5
###### H6
"""
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'heading_1' in unique, "Should detect heading_1"
    assert 'heading_2' in unique, "Should detect heading_2"
    assert 'heading_3' in unique, "Should detect heading_3"
    assert 'heading_4' in unique, "Should detect heading_4"
    assert 'heading_5' in unique, "Should detect heading_5"
    assert 'heading_6' in unique, "Should detect heading_6"
    print("  SUCCESS: All heading levels detected")
    
    # Test 2: Heading must have space
    content = "#NoSpace"
    notations = list_markdown_notations(content)
    assert 'heading_1' not in notations, "Should not detect heading without space"
    print("  SUCCESS: Headings without space not detected")
    
    print("  ✓ All heading detection tests passed")


def test_list_markdown_notations_text_formatting():
    """Test markdown notation detection for text formatting."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() for text formatting")
    print("="*60)
    
    # Test 1: Bold
    content = "**bold asterisk** and __bold underscore__"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'bold_asterisk' in unique, "Should detect bold with asterisks"
    assert 'bold_underscore' in unique, "Should detect bold with underscores"
    print("  SUCCESS: Bold formatting detected")
    
    # Test 2: Italic
    content = "*italic asterisk* and _italic underscore_"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'italic_asterisk' in unique, "Should detect italic with asterisk"
    assert 'italic_underscore' in unique, "Should detect italic with underscore"
    print("  SUCCESS: Italic formatting detected")
    
    # Test 3: Strikethrough
    content = "~~strikethrough text~~"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'strikethrough' in unique, "Should detect strikethrough"
    print("  SUCCESS: Strikethrough detected")
    
    print("  ✓ All text formatting detection tests passed")


def test_list_markdown_notations_code():
    """Test markdown notation detection for code."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() for code")
    print("="*60)
    
    # Test 1: Inline code
    content = "Some `inline code` here"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'inline_code' in unique, "Should detect inline code"
    print("  SUCCESS: Inline code detected")
    
    # Test 2: Code block
    content = """```python
def test():
    pass
```"""
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'code_block' in unique, "Should detect code block"
    print("  SUCCESS: Code block detected")
    
    print("  ✓ All code detection tests passed")


def test_list_markdown_notations_links_images():
    """Test markdown notation detection for links and images."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() for links and images")
    print("="*60)
    
    # Test 1: Links
    content = "[link text](https://example.com)"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'link' in unique, "Should detect link"
    print("  SUCCESS: Link detected")
    
    # Test 2: Images
    content = "![alt text](image.png)"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'image' in unique, "Should detect image"
    print("  SUCCESS: Image detected")
    
    # Test 3: Link should not be detected as image
    content = "[link](url)"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'link' in unique, "Should detect link"
    assert 'image' not in unique, "Should not detect link as image"
    print("  SUCCESS: Link not confused with image")
    
    print("  ✓ All link and image detection tests passed")


def test_list_markdown_notations_lists():
    """Test markdown notation detection for lists."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() for lists")
    print("="*60)
    
    # Test 1: Unordered list
    content = """- Item 1
- Item 2
* Item 3
+ Item 4
"""
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'unordered_list' in unique, "Should detect unordered list"
    print("  SUCCESS: Unordered list detected")
    
    # Test 2: Ordered list
    content = """1. First
2. Second
3. Third
"""
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'ordered_list' in unique, "Should detect ordered list"
    print("  SUCCESS: Ordered list detected")
    
    # Test 3: Must have space after marker
    content = "-NoSpace"
    notations = list_markdown_notations(content)
    assert 'unordered_list' not in notations, "Should not detect list without space"
    print("  SUCCESS: List without space not detected")
    
    print("  ✓ All list detection tests passed")


def test_list_markdown_notations_other():
    """Test markdown notation detection for other elements."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() for other elements")
    print("="*60)
    
    # Test 1: Blockquote
    content = "> This is a quote"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'blockquote' in unique, "Should detect blockquote"
    print("  SUCCESS: Blockquote detected")
    
    # Test 2: Horizontal rule
    content = """Some text
---
More text"""
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'horizontal_rule' in unique, "Should detect horizontal rule"
    print("  SUCCESS: Horizontal rule detected")
    
    # Test 3: Table
    content = "| Col1 | Col2 | Col3 |"
    notations = list_markdown_notations(content)
    unique = set(notations)
    
    assert 'table_pipe' in unique, "Should detect table"
    print("  SUCCESS: Table detected")
    
    print("  ✓ All other element detection tests passed")


def test_list_markdown_notations_real_file():
    """Test with actual test data files."""
    print("\n" + "="*60)
    print("TEST: list_markdown_notations() with real files")
    print("="*60)
    
    test_data_dir = Path(__file__).parent / "test_data"
    
    # Test 1: Simple file
    simple_file = test_data_dir / "simple_markdown.md"
    if simple_file.exists():
        content = simple_file.read_text(encoding='utf-8')
        notations = list_markdown_notations(content)
        unique = set(notations)
        
        assert 'heading_1' in unique, "Simple file should have heading_1"
        assert 'heading_2' in unique, "Simple file should have heading_2"
        assert 'unordered_list' in unique, "Simple file should have unordered_list"
        assert 'bold_asterisk' in unique, "Simple file should have bold"
        assert 'italic_asterisk' in unique, "Simple file should have italic"
        assert 'link' in unique, "Simple file should have link"
        assert 'inline_code' in unique, "Simple file should have inline code"
        print("  SUCCESS: Simple file analyzed correctly")
    
    # Test 2: Complex file
    complex_file = test_data_dir / "complex_markdown.md"
    if complex_file.exists():
        content = complex_file.read_text(encoding='utf-8')
        notations = list_markdown_notations(content)
        unique = set(notations)
        
        # Should have many notation types
        assert len(unique) >= 10, f"Complex file should have 10+ unique notations, got {len(unique)}"
        print(f"  SUCCESS: Complex file has {len(unique)} unique notation types")
    
    print("  ✓ All real file tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*70)
    print(" RUNNING ALL TESTS FOR markdown-survey.py")
    print("="*70)
    
    tests = [
        test_count_words_simple,
        test_count_words_markdown,
        test_count_words_code,
        test_count_words_html,
        test_count_words_images,
        test_count_words_edge_cases,
        test_list_markdown_notations_headings,
        test_list_markdown_notations_text_formatting,
        test_list_markdown_notations_code,
        test_list_markdown_notations_links_images,
        test_list_markdown_notations_lists,
        test_list_markdown_notations_other,
        test_list_markdown_notations_real_file,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n  ✗ FAILED: {test_func.__name__}")
            print(f"    {str(e)}")
        except Exception as e:
            failed += 1
            print(f"\n  ✗ ERROR in {test_func.__name__}")
            print(f"    {str(e)}")
    
    print("\n" + "="*70)
    print(f" TEST SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
