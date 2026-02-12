---
layout: default
description: Test file with various linter exceptions
---

# Test Document with Linter Exceptions

This document contains various Vale and markdownlint exceptions for testing.

## Vale Exceptions

<!-- vale Style.Rule = NO -->
This paragraph has a Vale exception for Style.Rule.
It should be detected by the scanner.
<!-- vale Style.Rule = YES -->

## Markdownlint Exceptions

<!-- markdownlint-disable MD013 -->
This is a really really really really really really really really really really really really really really really long line that exceeds the line length limit.
<!-- markdownlint-enable MD013 -->

## Mixed Section

<!-- vale Another.Rule = NO -->
This section has both Vale and markdownlint exceptions.

<!-- markdownlint-disable MD033 -->
<div class="custom">
  <p>Some HTML content that would normally trigger markdownlint</p>
</div>
<!-- markdownlint-enable MD033 -->

More text after the exception.

## Additional Exceptions

<!-- vale Spelling.Error = NO -->
This has a sppeling error that would normally be caught.
<!-- vale Spelling.Error = YES -->

<!-- markdownlint-disable MD041 -->
This file doesn't start with a level 1 heading (it starts with front matter).
<!-- markdownlint-enable MD041 -->
