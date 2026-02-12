---
layout: default
description: File with malformed linter exception tags
---

# Document with Malformed Linter Exceptions

This file contains various incorrectly formatted linter exception tags
that should NOT be matched by the parser.

## Missing Equals Sign

<!-- vale Style.Rule NO -->
This Vale tag is missing the equals sign.

## Missing NO Keyword

<!-- vale Style.Rule = -->
This Vale tag is missing the NO keyword.

## Wrong Format for Markdownlint

<!-- markdownlint MD013 -->
Missing the -disable part.

<!-- markdownlint-disable -->
Missing the rule number.

## Incomplete Rule Number

<!-- markdownlint-disable MD -->
Rule number is incomplete (needs 3 digits).

## Wrong Comment Format

// vale Style.Rule = NO
This uses the wrong comment style for markdown.

/* markdownlint-disable MD013 */
This also uses the wrong comment style.

## Random HTML Comments

<!-- This is just a regular comment -->
<!-- Another comment with vale in it but not a real exception -->
<!-- markdownlint is mentioned here too but not as an exception -->

## These SHOULD Work (for comparison)

<!-- vale Style.Rule = NO -->
This one is correct.

<!-- markdownlint-disable MD013 -->
This one is also correct.
