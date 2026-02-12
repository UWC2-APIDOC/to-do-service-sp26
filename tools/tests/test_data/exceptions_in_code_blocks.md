# Test file: exceptions in code blocks

This file has real exceptions and examples in code blocks.

<!-- vale Google.Parens = NO -->

This is a real exception that should be counted.

Here's how to use Vale exceptions (this should NOT be counted):

```markdown
<!-- vale Google.Parens = NO -->
Your content here
<!-- vale Google.Parens = YES -->
```

Another real exception:

<!-- markdownlint-disable MD013 -->

And here's a MarkdownLint example (should NOT be counted):

````markdown
Example with four backticks:
```bash
curl http://example.com
```

And a linter exception:
<!-- markdownlint-disable MD001 -->
````

Back to real content.

<!-- vale Google.Parens = YES -->

## Summary

Expected counts:
- Vale exceptions: 2 (lines 5 and 25)
- MarkdownLint exceptions: 1 (line 19)
- Total: 3 exceptions

Should NOT count:
- Line 10 (in triple-backtick code block)
- Line 11 (in triple-backtick code block)
- Line 24 (in four-backtick code block)
