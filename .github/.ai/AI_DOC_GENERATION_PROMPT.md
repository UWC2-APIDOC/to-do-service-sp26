# Documentation style for AI

<!-- vale Google.Parens = NO -->
<!-- vale write-good.Passive = NO -->

Add this to the project knowledge when using AI to when helping create repository documentation.

---

## Style guide reference

**All Markdown files** in the repository follow `docs/contributors-guide/writers-guide.md`, including:

- Repository README files
- Maintainer and instructor guides
- Internal documentation
- Published documentation in `/docs`

**Pull request validation lints all `.md` files using Vale and MarkdownLint.**

---

## Context-specific guidelines

### Published docs (`/docs` directory)

**Audience:** students/contributors learning the API

**Style:**

- Tutorial-oriented, step-by-step
- Define technical terms on first use
- Front matter required
- Minimal linter exceptions (fix issues rather than suppress)

**Follow:** `docs/contributors-guide/writers-guide.md` strictly

---

### Repository docs (README files, guides outside `/docs`)

**Audience:** maintainers and instructors (technical)

**Style:**

- Reference-oriented, structured for scanning
- Assume technical knowledge (Git, Python, workflows, schemas)
- Focus on actionable information
- More linter exceptions acceptable (but still minimal)

**Follow:** `docs/contributors-guide/writers-guide.md` with these additions:

#### Tables

- Use for comparing tools, listing parameters, mapping errors to solutions
- Keep simple, left-align text columns
- OK to exceed 100 chars if table requires it

Example:

```markdown
| Tool | Purpose | When it runs |
|------|---------|--------------|
| test-filenames.py | Validates filenames | All PRs |
| test-api-docs.py | Tests API examples | When docs changed |
```

#### Emoji (optional)

- Use sparingly for visual markers in audience routing
- Common usage: 📚 (students) 👨‍🏫 (instructors) 🔧 (maintainers)
- ✅ ❌ for examples of correct/incorrect usage

Example:

```markdown
## Documentation by Role

- 📚 **Students**: See [Contributor Guide](https://...)
- 👨‍🏫 **Instructors**: See [Instructor Guide](reporting/_REPORTING_README.md)
- 🔧 **Maintainers**: See [Maintainer Guide](tools/_TOOLS_README.md)
```

#### Checkboxes

- Use for task lists and checklists

Example:

```markdown
## Pre-deployment checklist

- [ ] Run all tests
- [ ] Update documentation
- [ ] Get team approval
```

#### Link style

- Internal repository links: Use relative paths
    - Good: `[Maintainer Guide](tools/_TOOLS_README.md#section)`
    - Avoid: `/tools/_TOOLS_README.md` or full GitHub URLs
- External links: Use absolute URLs
- Section anchors: Lowercase, hyphens, no punctuation
    - Good: `#instructor-guide`
    - How: GitHub auto-generates from headings

---

## Common linter exceptions for repository docs

Repository docs often need these specific exceptions:

### Vale exceptions

**`Google.Parens`** - Command syntax with explanations

```markdown
<!-- vale Google.Parens = NO -->
Run `git rebase -i HEAD~n` (where n is your commit count).
<!-- vale Google.Parens = YES -->
```

**`Google.Colons`** - YAML/configuration examples

````markdown
<!-- vale Google.Colons = NO -->
```yaml
test:
  server_url: localhost:3000
```
<!-- vale Google.Colons = YES -->
````

**`Vale.Terms`** - Tool/package names not in vocabulary

```markdown
<!-- Vale doesn't recognize tool names -->
<!-- vale Vale.Terms = NO -->
Tools: `pytest`, `json-server`, `markdownlint-cli2`.
<!-- vale Vale.Terms = YES -->
```

### MarkdownLint exceptions

**`MD013`** - Long lines in tables or commands

````markdown
<!-- markdownlint-disable MD013 -->
```bash
python3 workflow-data.py list-runs rbwatson to-do-service-sp26 --workflow pr-validation.yml --days 14
```
<!-- markdownlint-enable MD013 -->
````

### Guidelines for exceptions

1. **Fix first** - Try to resolve the issue before disabling
2. **Be specific** - Disable only the problematic rule, not all linting
3. **Document why** - Add comment explaining the exception
4. **Re-enable immediately** - Don't leave rules turned off any longer than needed
5. **Keep minimal** - Pull request validation records all exceptions

---

## Standard documentation patterns

### Tool/script documentation

````markdown
#### script-name.py

**Purpose:** What it does in one sentence

**Usage:** `python3 tools/script-name.py [args]`

**Arguments:**
- `--flag` - Description

**Output:** What it produces

**Example:**
```bash
python3 tools/script-name.py --action file.md
```
````

### Workflow stage documentation

```markdown
### Stage N: Stage name

**Runs when:** Condition that triggers this stage

**What it checks:**
- Check 1
- Check 2

**Student impact:** BLOCKING or NON-BLOCKING

**Common failures:**
- Failure type → How to fix
```

### Error documentation

```markdown
#### ❌ Error name

**Message:** "Exact error text"

**Meaning:** What went wrong

**Action:**
1. First troubleshooting step
2. Second troubleshooting step
```

### Maintenance procedure

````markdown
### Updating component name

**Steps:**
1. Edit configuration file
2. Test locally
3. Deploy change

**Verification:**

```bash
command to verify
```

**Rollback if needed:**

```bash
command to rollback
```
````

---

## Quick reference

When generating repository documentation:

✅ **Do:**

- Follow `writers-guide.md` for all Markdown basics
- Use tables for structured comparisons
- Use emoji sparingly for visual markers
- Assume technical audience knowledge
- Document linter exceptions when needed
- Use relative links for internal references
- Include blank lines around all headings/lists/code

❌ **Don't:**

- Skip linting (Pull request validation checks all `.md` in the PR)
- Disable entire linters for large sections
- Use linter exceptions without documenting why
- Mix Title Case and sentence case headings
- Forget language tags on code blocks
- Use absolute URLs for internal links

---

## Validation

All repository documentation goes through same Pull request validation as published docs:

- MarkdownLint checks formatting
- Vale checks writing style
- Front matter validation (for files in `/docs` only)
- Pull request validation records all exceptions to the linting rules

Test locally before committing:

```bash
vale README.md
markdownlint README.md
```
