---
layout: default
# This front matter has edge cases
description: "Test file with edge cases in front matter"
empty_field:
null_field: null
number_field: 42
boolean_field: true
array_field:
  - item1
  - item2
nested:
  deep:
    value: "nested value"
special_chars: "Value with 'quotes' and \"double quotes\""
multiline: |
  This is a
  multiline string
  in the front matter
test:
  testable: []  # Empty array
  server_url: ""  # Empty string
---

# Edge Cases Document

This file tests edge cases in front matter parsing:

- Empty fields
- Null values
- Different data types
- Nested structures
- Special characters
- Multiline strings
- Empty arrays and strings

The parser should handle all of these gracefully.