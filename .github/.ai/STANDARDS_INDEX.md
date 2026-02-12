<!-- vale off -->
# Documentation Testing Tools - Standards & Guidelines

This is the master index for all project standards, conventions, and guidelines.

## Quick Start

**New to the project?** Read these in order:

1. [TERMINOLOGY.md](./TERMINOLOGY.md#terminology-guide) - Learn the correct terms
2. [CODE_STYLE_GUIDE.md](./CODE_STYLE_GUIDE.md#code-style-guide) - Understand coding standards
3. [PROJECT_CONVENTIONS.md](./PROJECT_CONVENTIONS.md#project-conventions) - See how things are organized
4. [REFACTORING_CHECKLIST.md](./REFACTORING_CHECKLIST.md#refactoring-checklist) - Use this for any changes

**Adding tests?** Read:

1. [TEST_STANDARDS.md](./TEST_STANDARDS.md#test-standards)
2. [REFACTORING_CHECKLIST.md](./REFACTORING_CHECKLIST.md#refactoring-checklist) (Testing section)

---

## Document Summaries

### TERMINOLOGY.md

**What:** Canonical terms and their correct usage

**When to use:** Whenever you're unsure about terminology

**Key topics:**

- Front matter (two words in text, `front_matter` in code)
- Linter exceptions
- Test data vs fail data
- Logging levels and annotations
- Naming conventions (snake_case, kebab-case, etc.)

**Read this when:**

- Writing new code
- Updating documentation
- Naming files or functions
- Unsure about word usage

---

### CODE_STYLE_GUIDE.md

**What:** Python coding standards and best practices

**When to use:** Every time you write code

**Key topics:**

- Naming conventions (functions, variables, classes)
- File naming patterns
- Docstring format (Google-style)
- Import organization
- Error handling patterns
- Function length and complexity
- String formatting (f-strings)
- Code organization

**Read this when:**

- Starting new code
- Reviewing code
- Setting up a new module
- Refactoring existing code

---

### TEST_STANDARDS.md

**What:** Testing standards and best practices

**When to use:** Every time you write or update tests

**Key topics:**

- Test file organization (test_data/ vs fail_data/)
- Test naming conventions
- Test structure (Arrange-Act-Assert)
- Assertion standards
- Test coverage requirements
- Test data management
- Output standards
- Running tests multiple ways

**Read this when:**

- Creating new tests
- Adding test data
- Debugging failing tests
- Reviewing test coverage

---

### PROJECT_CONVENTIONS.md

**What:** Project-wide conventions for structure, CLI, and integration

**When to use:** For architectural decisions and consistency

**Key topics:**

- Directory structure
- CLI argument patterns (--action)
- Logging conventions (levels and usage)
- GitHub Actions integration
- Error handling patterns
- Shared utilities usage
- Documentation conventions
- Version control conventions

**Read this when:**

- Organizing files
- Designing CLI interfaces
- Integrating with GitHub Actions
- Setting up new workflows
- Creating documentation

---

### REFACTORING_CHECKLIST.md

**What:** Step-by-step checklist for refactoring and adding features

**When to use:** Every time you make significant changes

**Key topics:**

- Before starting (review, understand, plan)
- During refactoring (code, files, structure)
- Testing (create tests, test data, verify)
- Documentation (READMEs, summaries)
- Verification (run tests, manual testing, review)
- Finalization (clean up, git, final checks)

**Read this when:**

- Migrating a tool to shared utilities
- Adding new functionality
- Refactoring existing code
- Reviewing someone's work

---

## Usage Patterns

### Pattern 1: Adding a New Tool

```text
1. Read: TERMINOLOGY.md (terms to use)
2. Read: CODE_STYLE_GUIDE.md (how to write it)
3. Read: PROJECT_CONVENTIONS.md (where it goes, CLI pattern)
4. Use: REFACTORING_CHECKLIST.md (follow step by step)
5. Read: TEST_STANDARDS.md (how to test it)
```

### Pattern 2: Refactoring Existing Tool

```text
1. Use: REFACTORING_CHECKLIST.md (complete guide)
2. Reference: CODE_STYLE_GUIDE.md (as you code)
3. Reference: TERMINOLOGY.md (correct terms)
4. Reference: TEST_STANDARDS.md (as you test)
5. Reference: PROJECT_CONVENTIONS.md (for consistency)
```

### Pattern 3: Adding Tests

```text
1. Read: TEST_STANDARDS.md (how to structure)
2. Read: TERMINOLOGY.md (correct terms)
3. Use: REFACTORING_CHECKLIST.md (testing section)
4. Reference: CODE_STYLE_GUIDE.md (code quality)
```

### Pattern 4: Bug Fix

```text
1. Use: REFACTORING_CHECKLIST.md (verification steps)
2. Read: TEST_STANDARDS.md (add regression test)
3. Reference: CODE_STYLE_GUIDE.md (maintain style)
4. Reference: TERMINOLOGY.md (if updating docs)
```

### Pattern 5: Documentation Update

```text
1. Read: TERMINOLOGY.md (correct terms)
2. Read: PROJECT_CONVENTIONS.md (documentation section)
3. Review existing docs for consistency
4. Update as needed
```

---

## For AI Assistants / Future Sessions

### Starting a New Session

Provide this context:

```text
I'm working on the documentation testing tools project. 
Please follow these standards:

- CODE_STYLE_GUIDE.md for coding conventions
- TEST_STANDARDS.md for testing
- TERMINOLOGY.md for correct term usage
- PROJECT_CONVENTIONS.md for structure and patterns
- REFACTORING_CHECKLIST.md for completeness

Key conventions:
- "front matter" (two words in text, front_matter in code)
- Use shared doc_test_utils functions
- CLI pattern: --action [all|warning|error]
- Test organization: test_data/ (pass) vs fail_data/ (fail)
- Logging: log(message, level, file, line, use_actions, action_level)
```

### For Specific Tasks

**Migrating a tool:**

```text
Migrate [tool-name] following REFACTORING_CHECKLIST.md.
Use CODE_STYLE_GUIDE.md and TERMINOLOGY.md for conventions.
```

**Adding tests:**

```text
Add tests for [feature] following TEST_STANDARDS.md.
Place valid files in test_data/, invalid in fail_data/.
```

**Bug fix:**

```text
Fix [bug] and add regression test per TEST_STANDARDS.md.
Verify with REFACTORING_CHECKLIST.md.
```

---

## Document Relationships

```text
TERMINOLOGY.md
    â†“ (defines terms used in)
CODE_STYLE_GUIDE.md
    â†“ (provides patterns for)
PROJECT_CONVENTIONS.md
    â†“ (guides structure for)
REFACTORING_CHECKLIST.md
    â†‘ (references all above)
    â†“ (includes steps for)
TEST_STANDARDS.md
```

**Legend:**

- **TERMINOLOGY.md** is foundational - defines what words mean
- **CODE_STYLE_GUIDE.md** builds on terminology with coding rules
- **PROJECT_CONVENTIONS.md** applies style to project structure
- **REFACTORING_CHECKLIST.md** ties everything together procedurally
- **TEST_STANDARDS.md** is parallel to code standards, for testing

---

## Maintenance

### Updating These Documents

**When to update:**

- New patterns emerge across multiple tools
- Better approaches are discovered
- Standards need clarification
- Team agrees on changes

**How to update:**

1. Propose change with rationale
2. Update affected documents
3. Ensure consistency across documents
4. Update this index if needed
5. Notify team of changes

### Document Owners

All documents are team-owned. Anyone can propose updates via:

- Pull request with explanation
- Discussion in team meetings
- Documentation issues

### Version History

Track major changes:

- 2024-12-04: Initial standards documents created (Phase 2)
- Includes refactoring of "frontmatter" â†’ "front matter"
- Establishes test_data/ vs fail_data/ separation

---

## Examples and References

### Real Examples

**Phase 1 Summary:**

- Example of completing a phase
- Documents utilities created
- Shows test structure

**Phase 2 Summary:**

- Example of migration
- Shows before/after comparisons
- Demonstrates checklist usage

**Front Matter Refactoring:**

- Example of terminology change
- Shows scope of refactoring
- Documents verification

### Reference Implementations

**doc_test_utils.py:**

- Canonical implementation of shared utilities
- Example of proper docstrings
- Error handling patterns

**test_doc_test_utils.py:**

- Canonical test structure
- Example of comprehensive testing
- Shows output formatting

**list-linter-exceptions.py:**

- Example of migrated tool
- Shows CLI argument pattern
- Demonstrates shared utility usage

---

## Getting Help

### Where to Look

1. **This index** - Find the right document
2. **Specific guide** - Get detailed information
3. **Existing code** - See patterns in practice
4. **Phase summaries** - Understand completed work
5. **Ask the team** - When documentation is unclear

### Improving Documentation

If you find:

- Unclear sections
- Missing information
- Contradictions
- Better ways to explain

Please:

1. Note the issue
2. Propose a fix
3. Update the relevant document(s)
4. Share with the team

---

## Quick Reference

| Need to... | Read... |
| ------------ | --------- |
| Know correct term | TERMINOLOGY.md |
| Write Python code | CODE_STYLE_GUIDE.md |
| Organize files | PROJECT_CONVENTIONS.md |
| Write tests | TEST_STANDARDS.md |
| Complete task | REFACTORING_CHECKLIST.md |
| Design CLI | PROJECT_CONVENTIONS.md (CLI section) |
| Handle errors | CODE_STYLE_GUIDE.md (Error Handling) |
| Log messages | PROJECT_CONVENTIONS.md (Logging) |
| Create test data | TEST_STANDARDS.md (Test Data Management) |
| Use shared code | PROJECT_CONVENTIONS.md (Shared Utilities) |

---

## Success Criteria

You're following the standards well if:

âœ… Code follows naming conventions consistently
âœ… Tests exist for all functionality
âœ… Documentation is complete and accurate
âœ… Terms are used correctly
âœ… Files are organized properly
âœ… Error handling is graceful
âœ… Logging uses correct levels
âœ… CLI follows standard patterns
âœ… Checklist items are completed
âœ… Changes are verified before committing

---

## Remember

> **Consistency matters more than perfection.**

It's better to follow an imperfect standard consistently than to have perfect but
inconsistent code. When in doubt, check existing code and follow established patterns.

If you find a better way, great! Update the standards and refactor consistently.
