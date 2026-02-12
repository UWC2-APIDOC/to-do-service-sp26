---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: Contributing
nav_order: 2
has_children: false
has_toc: false
# tags used by AI files
description: "Information about how to contribute new and updated documentation topics"
topic_type: reference
tags: 
    - docs
categories: 
    - doc-contributions
ai_relevance: low
importance: 4
prerequisites: []
related_pages: 
    - /before-you-start-a-tutorial
examples: []
api_endpoints: []
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---

# Documentation requirements

<!-- vale Google.Colons = NO -->
<!-- vale Google.Parens = NO -->
<!-- vale write-good = NO -->

This document lists all requirements tested in the `pr-validation.yml` GitHub workflow.
These are the rules that documentation must follow to pass automated validation.

## File location requirements

### Allowed directories

- Documentation files: `docs/**/*.md`
- Assignment files: `assignments/**/*.md`

### Restriction

- Students (non-admin, non-write permission users) can only change files in `/docs/` and `/assignments/`
- Changes to other directories require admin or write permissions

**Violation Result:** PR validation fails with error
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/File-Locations`

---

## Filename requirements

### Character restrictions

Filenames must not contain:

- Whitespace characters
- Shell meta-characters: `* ? [ ] | & ; $` `` ` `` `" ' < > ( )`
- Backslashes: `\`
- Colons: `:`

**Validation Tool:** `tools/test-filenames.py`
**Checked via:** `CHANGED_FILES` environment variable
**Violation Result:** Error annotation, PR fails

---

## Commit requirements

### Commit count

- PR must contain exactly 1 commit
- No more, no less

**Violation Result:** Error with message showing actual count
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits`

### Merge commits

- PR must not contain any merge commits
- Use rebase instead

**Violation Result:** Error with message showing merge commit count
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Avoiding-Merge-Commits`

### Branch status

- Warning, if PR branch isn't up to date with base branch
- Recommendation to rebase

**Violation Result:** Warning annotation
**Help Link:** `https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Updating-Your-Branch`

---

## Markdown linting requirements

### MarkdownLint rules

Configured in `.github/config/.MarkdownLint.jsonc`:

#### `MD007: Unordered list indentation`

- Required indent: 4 spaces

#### `MD013: Line length`

- No longer than 100 characters

#### `MD036: Emphasis used instead of heading`

- Disabled

#### `MD049: Emphasis style`

- Required style: underscore (`_italic_`)

#### `MD050: Strong style`

- Required style: asterisk (`**bold**`)

#### `MD060: Link style`

- Required style: compact

**Validation Tool:** `DavidAnson/MarkdownLint-cli2-action@v21`
**Violation Result:** Error annotations on specific lines

---

## Vale requirements

Configured in `.vale.ini`:

### Enabled style packages

- Vale (core rules)
- Google Developer Documentation Style Guide
- write-good (readability checks)
- Readability (readability metrics)

### Specific settings

#### Ignored scopes

- `code` blocks
- `tt` (teletype) elements

#### Skipped scopes

- `script` tags
- `style` tags
- `pre` (pre-formatted) blocks
- `figure` elements
- `text.frontmatter` (YAML front matter)

#### Alert level

- Minimum: `suggestion`
- Reports all suggestions, warnings, and errors

#### Enabled rules

- `Vale.terms`: verifies project terminology
- `Google.*`: All Google style guide rules
- `write-good.*`: All rules except E-Prime
- `Readability.FleschKincaid`: checks reading level (complexity)
- Other readability metrics: NO

#### Disabled rules

- `write-good.E-Prime`: Disabled (allows "to be" verbs)
- `Readability.AutomatedReadability`: Disabled
- `Readability.ColemanLiau`: Disabled
- `Readability.FleschReadingEase`: Disabled
- `Readability.GunningFog`: Disabled
- `Readability.LIX`: Disabled
- `Readability.SMOG`: Disabled

### Custom vocabulary

- Location: `.github/valeStyles/projectTerms/`
- Project-specific approved terms

**Validation Tool:** `errata-ai/vale-action@v2.1.1`
**Version:** 3.12.0
**Violation Result:** Error annotations on specific lines
**Cached:** Yes (Vale binary cached for performance)

---

## Front matter requirements

### Presence

- All files in `/docs/` directory must have YAML front matter
- Front matter must be between `---` delimiters at start of file
- Front matter delimiters must start at the beginning of the line
- Front matter delimiters must be the only characters in the line
- Files with `<!-- front matter not required -->` comment in the first 5 lines of the file:
    - If in `/docs/`: An error, front matter is required
    - If in `/assignments/`: a warning, front matter is recommended
    - If elsewhere: Silently skipped

**Violation Result:** Error, can't test file

### Required fields

As defined in `.github/schemas/front-matter-schema.json`:

- `layout`: string, must be `default`, `page`, or `post`
- `description`: string, 10-200 characters
- `topic_type`: string, must be `reference`, `tutorial`, `guide`, `concept`, or `overview`

### Optional standard fields

#### Navigation and structure

- `parent`: string, exact match to parent page title
- `has_children`: Boolean, indicates if page has child pages
- `has_toc`: Boolean, indicates if page should show table of contents
- `nav_order`: integer, minimum 1 (lower numbers appear first)

#### Content classification

- `tags`: array of strings, unique values
- `categories`: array of strings, unique values
- `ai_relevance`: string, must be `high`, `medium`, or `low`
- `importance`: integer, 1-10

#### Documentation structure

- `prerequisites`: array of strings (page titles or concepts)
- `related_pages`: array of strings (page titles)
- `examples`: array of strings (example names for AI indexing)

#### API-specific

- `api_endpoints`: array of strings matching pattern `^(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)? ?/.+`
- `version`: string matching pattern `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`
- `last_updated`: string, date format

### Test configuration

Optional. Used when file contains testable API examples:

```yaml
test:
  test_apps:          # Array of npm-installable test servers (optional)
    - "json-server@0.17.4"
  server_url:         # URL where test server runs (optional)
    "localhost:3000"
  local_database:     # Path to test database JSON file (optional)
    "/api/to-do-db-source.json"
  testable:           # Array of testable examples (REQUIRED if test exists)
    - "GET example / 200"
    - "POST example / 201,204"
```

#### Test field rules

- If `test` object exists, the test configuration must have a `testable` array
- `test_apps` pattern: `^[a-zA-Z0-9_-]+(@[0-9]+\.[0-9]+\.[0-9]+)?$`
- `server_url` pattern: `^(https?://)?([a-zA-Z0-9.-]+|localhost)(:[0-9]+)?$`
- `local_database` pattern: `^(/)?[a-zA-Z0-9/_.-]+\.json$`
- `testable` item pattern: `^.+( / [0-9,]+)?$`
    - Format: "example name" or "example name / 200,201"
    - Default status code if omitted: 200

**Validation Tool:** `tools/test-api-docs.py` with JSON schema validation
**Violation Result:** Error annotations with specific schema violation details

---

## API documentation testing requirements

### When tests run

- Only runs if files in `docs/` or `assignments/` changed
- Only runs if Markdown linting passed
- Only runs if file has valid front matter with `test` configuration

### Test discovery

1. Check for `<!-- front matter not required -->` comment (see Front Matter requirements)
2. Parse front matter
3. Compare against schema
4. Check for `test` object with `testable` array
5. Skip files without testable examples

### Example format requirements

For each item in `test.testable` array, the Markdown must contain:

#### Request section

- Heading: `### {example_name} request` or `#### {example_name} request`
    - Example name can have words wrapped in backticks: `` `GET` example ``
    - Case-insensitive heading match
- Code block: ` ```bash ` or ` ```sh `
- Must contain: curl command
- URL substitution: `{server_url}` replaced with `test.server_url` value

**Format Help:** <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format>

#### Response section

- Heading: `### {example_name} response` or `#### {example_name} response`
    - Same flexible matching as request section
- Code block: ` ```json `
- Must contain: valid JSON response body
- Used for: comparing actual API response with documented response

**Format Help:** <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format>

### Test execution

#### Database setup

- Test server: json-server@0.17.4 on port 3000
- Database reset: Before testing each file
- Source: `test.local_database` from file's front matter
- Default: `api/to-do-db-source.json` if not specified
- Format: JSON file with REST resources

#### Request execution

1. Extract curl command from request section
2. Add `-i` flag if not present (to get headers)
3. Replace `{server_url}` with actual server URL
4. Execute with 10-second timeout
5. Parse HTTP status code from response headers

#### Response validation

1. Check status code is in expected list
2. Ensure response is valid JSON
3. Compare response structure with documented response
4. Report specific differences if mismatch

### Comparison rules

- Type checking: actual and expected must have same type
- Objects:
    - All expected keys must exist in actual
    - Extra keys in actual generate warnings
- Arrays:
    - Length must match
    - Elements compared by index
- Primitives: Must match exactly
- Differences reported with JSON path

### Test results

- Error if curl command not found or malformed
- Error if response section not found or malformed  
- Error if status code doesn't match expected
- Error if response isn't valid JSON
- Error if response structure doesn't match documentation
- Warning if example sections not formatted correctly

**Validation Tool:** `tools/test-api-docs.py`
**Violation Result:** Error annotations with specific test failure details

---

## Markdown survey

Not required, but provides these statistics:

### Tracked metrics

- Number of files processed
- Heading count per file
- Code block count per file
- Linter exceptions (Vale and MarkdownLint)

**Tool:** `tools/markdown-survey.py`
**Output:** Informational annotations (warnings)

---

## Linter exception tracking

Documents use of linter exception comments:

### Vale exceptions

Format: `<!-- vale RuleName = NO -->`

- Tracked and reported
- Not a validation error

### MarkdownLint exceptions

Format: `<!-- markdownlint-disable MD### -->`

- Tracked and reported
- Not a validation error (but noted)

**Tool:** `tools/list-linter-exceptions.py`
**Output:** Warning annotations showing location and rule

---

## Validation stages and dependencies

### Stage 0: discover changed files

- Identifies all changed Markdown files
- Separates docs from tools
- Flags unauthorized changes

### Stage 1: Test tools

- Runs if any files in `tools/` have changed
- Runs pytest on `tools/tests/`
- **All other stages blocked if this fails**

### Stage 2: Lint and validate content

- Depends on: `Test Tools` passing
- Runs if: Any Markdown files changed
- Sub-checks:
    - Filename validation
    - Linter exception listing
    - Markdown survey
    - MarkdownLint validation
    - Vale validation

### Stage 3: Test API documentation

- Depends on: `Lint and Validate Content` test passing
- Runs if: Files in `docs/` or `assignments/` have changed
- Tests API examples against test server

### Stage 4: Check number of commits

- Depends on: `Lint and Validate Content` and
    the `Test API Documentation` passing
- Always runs as final check
- Sub-checks:
    - Unauthorized file changes
    - Feature branch status compared to original branch
    - Commit count and merge commits

**Failure Behavior:** Fail-fast - if earlier stage fails, dependent stages don't run

---

## Tool locations

### Python scripts

- `tools/test-filenames.py` - Filename validation
- `tools/list-linter-exceptions.py` - Exception tracking
- `tools/markdown-survey.py` - Content statistics
- `tools/test-api-docs.py` - API example testing
- `tools/doc_test_utils.py` - Shared utilities
- `tools/schema_validator.py` - Front matter schema validation
- `tools/get-database-path.py` - Extract database path from front matter

### Configuration files

- `.github/config/.MarkdownLint.jsonc` - MarkdownLint rules
- `.vale.ini` - Vale configuration
- `.github/schemas/front-matter-schema.json` - Front matter schema
- `.github/valeStyles/` - Custom Vale styles and vocabulary

### GitHub actions

- `.github/workflows/pr-validation.yml` - Main validation workflow

---

## Exit codes and results

### Success

- All checks pass
- OK to merge PR

### Failure scenarios

1. **Tool tests fail** - Fix tools before proceeding
2. **Filename invalid** - Rename file to remove special characters
3. **Markdown lint errors** - Fix formatting issues
4. **Vale errors** - Fix writing style issues
5. **Schema validation fails** - Fix front matter structure
6. **API tests fail** - Fix example code or expected responses
7. **Unauthorized files** - Remove changes to restricted directories
8. **Too many commits** - Squash into single commit
9. **Merge commits** - Rebase to remove merge commits

### Help resources

- GitHub Wiki: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/>
- Specific pages linked in error messages
