---
layout: default
description: "Test with Unicode: émojis 🎉, Chinese 中文, Arabic العربية"
topic_type: reference
tags: ["unicode", "special-chars"]
---

# Unicode and Special Characters Test

This file contains various Unicode characters to test encoding handling.

## Emoji Section 🎉

Testing emoji support: 😀 🚀 ✅ ❌ ⚠️

<!-- vale Unicode.Rule = NO -->
Some text with émojis and spëcial çharacters.
<!-- vale Unicode.Rule = YES -->

## Multiple Languages

- English: Hello World
- Spanish: Hola Mundo
- French: Bonjour le monde
- German: Hallo Welt
- Chinese: 你好世界
- Japanese: こんにちは世界
- Arabic: مرحبا بالعالم
- Russian: Привет мир

<!-- markdownlint-disable MD013 -->
这是一个很长的中文句子，用来测试markdown-linter如何处理Unicode字符和长行。
<!-- markdownlint-enable MD013 -->

## Special Characters

Testing special characters: © ® ™ € £ ¥ § ¶

Math symbols: ∑ ∏ √ ∞ ≈ ≠ ≤ ≥

Arrows: → ← ↑ ↓ ↔ ⇒ ⇐

## Purpose

This file ensures that:
1. UTF-8 encoding is handled correctly
2. Unicode characters don't break parsing
3. Exception tags work with Unicode content
4. Line counting works correctly with multi-byte characters
