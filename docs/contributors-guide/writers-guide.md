---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: Contributing
nav_order: 1
has_children: false
has_toc: false
# tags used by AI files
description: "Information about how to write new documentation topics"
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

# Writer's guide

<!-- vale Google.Colons = NO -->

This guide helps you create and edit documentation that passes automated validation.

## Getting started

### Where to save files

Save documentation files in these directories:

- API reference: `docs/api/`
- Tutorials and guides: `docs/tutorials/`
- Assignment work: `assignments/`

Students can only add or change files in `docs/` and `assignments/`.
Changes to other directories require `admin` permissions.

### Naming files

Use descriptive, lowercase filenames with hyphens between words:

- Good: `users-get-by-id.md`, `getting-started.md`
- Avoid: `users get by id.md`, `UsersGetById.md`

Don't use these characters in filenames:

<!-- vale Google.Parens = NO -->
- Spaces or special characters: `* ? [ ] | & ; $` `` ` `` `" ' < > ( )`
- Backslashes: `\`
- Colons: `:`
<!-- vale Google.Parens = YES -->

### Creating a new page

Every documentation page needs three parts:

1. Front matter: the metadata between `---` delimiters
2. Page title: the level 1 heading
3. Content

Example:

```markdown
---
layout: default
description: Get a user by ID from the service
topic_type: reference
---

# Get user by ID

Returns the user with the specified ID.

## Parameters

The `id` parameter specifies which user to retrieve.
```

## Front matter reference

Front matter is YAML metadata at the start of each file between `---` delimiters.
All files in `docs/` must have front matter.

### Required fields

Every page needs these three fields:

```yaml
---
layout: default
description: Brief description of the page (10-200 characters)
topic_type: reference
---
```

**`layout`** - Always use `default` for documentation pages

**`description`** - One-sentence summary of the page content.
Used in search results and page metadata.

- Length: at least 10 characters, but no more than 200 characters
- Don't end with a period

**`topic_type`** - Choose the type that best describes your content:

- `reference` - API endpoints, parameters, responses
- `tutorial` - Step-by-step instructions to complete a task
- `guide` - How-to documentation for different use-cases
- `concept` - Explanations of how something works
- `overview` - High-level introductions to a topic

### Navigation fields

Add these fields to control how pages appear in the site navigation:

```yaml
parent: Users
nav_order: 2
has_children: true
has_toc: true
```

**`parent`** - The exact title of the parent page. Used for child pages.

**`nav_order`** - Integer controlling menu order.
Lower numbers appear first. `nav_order`:1 appears ahead of `nav_order`:2.

**`has_children`** - Set to `true` for pages that have child pages.

**`has_toc`** - Set to `true` to show a table of contents for the page.

### Content organization fields

Use these to categorize and relate pages:

```yaml
tags: [api, users, rest]
categories: [api-reference]
prerequisites: [getting-started, authentication]
related_pages: [Create user, Update user, Delete user]
```

**`tags`** - Keywords for categorizing content. Use existing tags when possible.

**`categories`** - Broader groupings than tags.

**`prerequisites`** - Pages or concepts users should understand first. List in recommended reading order.

**`related_pages`** - Other pages covering similar topics.

### Test configuration

Add test configuration to pages with API examples you want validated:

```yaml
test:
  server_url: localhost:3000
  local_database: /api/to-do-db-source.json
  testable:
    - GET example
    - POST example / 201
```

**`server_url`** - Where the test server runs.

**`local_database`** - Path to the JSON file containing test data.

**`testable`** - List of examples to test. Format: `example name` or `example name / status_code`.

If you don't specify a status code, the test assumes `200`.
If more than one success code, separate with commas: `example name / 200,204`.

## Writing API examples

To include API examples that the pull request testing validates,
follow this format exactly.

### Request section

Create a heading with "request" at the end:

````markdown
### GET example request

```bash
curl -X GET {server_url}/users/1
```
````

Requirements:

- Heading level 3 or 4: `###` or `####`
- Heading ends with the word "request"
- Code block uses `bash` or `sh` language
- Contains a `curl` command
- Use `{server_url}` as a placeholder in the example.
  The pull request testing replaces this with the value from the front matter.

### Response section

Create a heading with "response" at the end:

````markdown
### GET example response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

Requirements:

- Heading level 3 or 4: `###` or `####`
- Heading ends with the word "response"
- Code block uses `json` language
- Contains valid JSON
- Shows the expected structure returned by the API

### Complete example structure

````markdown
## Get user by ID

Retrieves a single user record.

### GET example request

```bash
curl -X GET {server_url}/users/1
```

### GET example response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```
````

The example name in your front matter must match the beginning of both headings.
If your front matter says `GET example`, your example headings must start with `GET example`.

You can use code tags to format the heading text, but they don't appear when
matching the heading names with the front matter.
For example, "### \`GET\` object example" in the document
matches a front matter value of `GET object example`.

## Style and formatting

### Line length

Keep lines under 100 characters. Break long lines at natural points:

```markdown
<!-- Good -->
The API returns user data including the user's name, email address,
and account creation date.

<!-- Too long -->
The API returns user data including the user's name, email address, and account creation date.
```

### Headings

Use sentence-style capitalization. Capitalize only the first word and proper nouns:

```markdown
<!-- Good -->
## Getting started with the API
### What is the user resource?

<!-- Avoid -->
## Getting Started With The API
### What Is The User Resource?
```

Don't end headings with periods or other punctuation:

```markdown
<!-- Good -->
## How to authenticate

<!-- Avoid -->
## How to authenticate.
```

Leave blank lines before and after headings:

```markdown
Text before the heading.

## Heading

Text after the heading.
```

### Lists

Use 4-space indentation for nested lists:

```markdown
- First level
    - Second level
    - Second level
- First level
```

Leave blank lines before and after lists:

```markdown
Here are the steps:

- First step
- Second step
- Third step

The process completes after these steps.
```

For complete sentences, use periods. For fragments, omit periods:

```markdown
<!-- Complete sentences - use periods -->
- This is a complete sentence describing the feature.
- Another complete sentence with proper punctuation.

<!-- Fragments - no periods -->
- Brief point
- Another brief point
```

### Emphasis and strong text

Use underscores for emphasis, or \__italics_\_ and
asterisks for strong \*\***bold**\*\*:

```markdown
Use _emphasis_ for terms you're introducing.
Use **strong** for UI elements and important warnings.
```

### Code

Use backticks for inline code, commands, filenames, and parameters:

```markdown
Set the `timeout` parameter to 30 seconds.
Edit the `config.json` file.
Run the `curl` command.
```

Specify the language for code blocks:

````markdown
```python
def hello_world():
    print("Hello, World!")
```

```bash
npm install package-name
```
````

### Blank lines

Always include blank lines:

- Before and after headings
- Before and after lists
- Before and after code blocks

````markdown
Previous paragraph.

## Heading

First paragraph after heading.

- List item
- List item

Paragraph after list.

```code
example
```

Paragraph after code block.
````

## Writing style

### Readability

Aim for a Flesch-Kincaid grade level of 8 or below when possible:

- Use sentences with 25 words or less.
- Choose simpler words when they work
- Break complex ideas into different sentences

The validation tools check readability and flag overly complex writing.

### Voice and tone

Use active voice and second person:

```markdown
<!-- Good -->
You can create a new user by sending a POST request.

<!-- Avoid -->
A new user can be created by sending a POST request.
Users should send a POST request.
```

### Terminology

Use project-approved terminology:

- `front matter` not `frontmatter` or `front-matter`
- Use the terms defined in the project vocabulary

The Vale linter checks for incorrect terminology and style issues.

### Common style issues

**Avoid exclamation points:**

```markdown
<!-- Good -->
This feature is now available.

<!-- Avoid -->
This feature is amazing!
```

**Avoid ellipses:**

```markdown
<!-- Good -->
The process takes time to complete.

<!-- Avoid -->
The process takes time...
```

**Use gender-neutral pronouns:**

```markdown
<!-- Good -->
When a user logs in, they see their dashboard.

<!-- Avoid -->
When a user logs in, he sees his dashboard.
```

## Using linter exceptions

Sometimes you need to override linting rules. Use exceptions sparingly and only when necessary.

### Vale exceptions

To turn off a Vale rule for a section:

```markdown
<!-- vale Style.Rule = NO -->
Text that violates the rule but is correct for your use case.
<!-- vale Style.Rule = YES -->
```

### MarkdownLint exceptions

To turn off a MarkdownLint rule:

```markdown
<!-- markdownlint-disable MD013 -->
This line can be longer than 100 characters if needed for a specific reason.
<!-- markdownlint-enable MD013 -->
```

### When to use exceptions

Appropriate uses:

- API examples with long URLs or code that you can't break into sections
- Product names or technical terms flagged incorrectly
- Code output or error messages that violate style rules

Don't use exceptions to avoid fixing real style issues.
The validation tools track exceptions and report them in PRs.

## Submitting changes

When you think your changes are ready to submit in a pull request,
you can create a draft pull request to see how your changes fare in
the automated testing.

- If you get some automated testing errors, you can fix them locally
    and the tests are re-run when you push the changes to the feature branch.
- When your pull request passes all test, you can choose that it's `Ready for review`.
    This changes the pull request's status from `Draft` to `Open`.

### Commit requirements

Each pull request must contain exactly one commit:

- If you have more than one commit, squash them into one
- Use `rebase` to update your feature branch. Don't use merge commits.

The validation checks fail if your PR has more than one commit or merge commits.

### Branch updates

Keep your branch up to date with the main branch:

```bash
git fetch origin
git rebase origin/main
```

You'll see a warning, not an error, if your branch is behind the destination branch.

### Understanding validation

When you submit a PR, validation runs in four stages:

**Stage 1: Tool tests**

Tests the validation tools themselves.
Only runs if you add or change any files in the `/tools` directory.
Failing this test stage blocks all other test stages.

**Stage 2: Linting**

Checks your Markdown and writing:

- Filename validation - tests filenames for disallowed characters
- MarkdownLint - tests for correct
- Vale
- Linter exception tracking

**Stage 3: API testing**

Tests API examples against a test server. Only runs if you changed files in `docs/` or `assignments/`.

**Stage 4: Commit validation**

Final checks:

- File location permissions
- Single commit pull request
- No merge commits in feature branch

If any stage fails, later stages don't run. Fix the earliest failure first.

## Troubleshooting validation failures

### Filename errors

**Error:** Unsafe filename characters

**Fix:** Rename the file to remove spaces, special characters,
backslashes, or colons. Use hyphens between words.

### MarkdownLint errors

<!-- vale Google.Parens = NO -->

**MD007 (list indentation):** Use 4 spaces for nested list items

**MD013 (line too long):** Break lines over 100 characters

**MD049 (emphasis style):** Use `_underscores_` for emphasis, not asterisks

**MD050 (strong style):** Use `**asterisks**` for strong, not underscores

<!-- vale Google.Parens = YES -->

### Vale errors

Vale catches writing style issues. Common errors:

- Grade level too high, often because a sentence is too complex
- Incorrect terminology
- Passive voice
- Gendered pronouns

Read the error message to see which rule failed and what text triggered it.
The message often suggests a fix.

### Front matter errors

**Error:** Front matter validation failed

**Fix:** Check that you have all required fields (`layout`, `description`, `topic_type`)
and that they contain valid values.

**Error:** Description too short or too long

**Fix:** Make your description 10-200 characters.

**Error:** Invalid topic type

**Fix:** Use one of the five valid types: `reference`, `tutorial`, `guide`, `concept`, or `overview`.

### API test failures

<!-- vale Google.Contractions = NO -->

**Error:** Could not find example

**Fix:** Check that your heading matches the example name in your front matter exactly and
ends with `request` or `response`.

**Error:** Expected HTTP status does not match

**Fix:** Update your front matter to include the actual status code the API returns,
or fix the example to return the expected status.

**Error:** Response does not match documentation

**Fix:** Update your documented response to match what the API actually returns,
or fix the API to return what's documented.

<!-- vale Google.Contractions = YES -->

### Commit errors

**Error:** PR must contain exactly one commit

**Fix:** Squash your commits:

```bash
git rebase -i HEAD~n  # where n is your number of commits
# Mark all except the first as 'squash'
git push --force-with-lease
```

**Error:** PR contains merge commits

**Fix:** Rebase instead of merge:

```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

## Quick reference

### Pre-submission checklist

Before submitting your PR:

- File is in `docs/` or `assignments/`
- Filename uses lowercase and hyphens: no spaces or special characters
- Front matter has `layout`, `description`, and `topic_type`
- Description is 10-200 characters
- Headings use sentence case and has no ending punctuation
- Lists use 4-space indentation
- Lines are under 100 characters
- Blank lines before and after headings, lists, and code blocks
- API examples have both request and response sections
- Front matter `testable` array matches example headings
- Only one commit in your PR
- No merge commits

### Front matter templates

**Basic API reference:**

```yaml
---
layout: default
description: Brief description of the endpoint
topic_type: reference
test:
  server_url: localhost:3000
  local_database: /api/to-do-db-source.json
  testable:
    - GET example
---
```

**Tutorial:**

```yaml
---
layout: default
description: Learn how to complete this task
topic_type: tutorial
prerequisites: [getting-started]
related_pages: [Related topic 1, Related topic 2]
---
```

**Parent page with children:**

```yaml
---
layout: default
description: Overview of this topic area
topic_type: overview
has_children: true
nav_order: 1
---
```

**Child page:**

```yaml
---
layout: default
parent: Parent Page Title
description: Specific aspect of the parent topic
topic_type: reference
nav_order: 2
---
```

### Common fixes

**Line too long:** Break at a natural point, such as after punctuation or before a conjunction

**Wrong emphasis style:** Change `*italic*` to `_italic_`

**Wrong strong style:** Change `__bold__` to `**bold**`

**List indentation:** Use 4 spaces for nested items, not 2

**Missing blank line:** Add blank lines around headings, lists, and code blocks

**Title case heading:** Change `## Getting Started` to `## Getting started`

**Heading punctuation:** Remove periods and question marks from headings

### Help resources

- GitHub Wiki: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/>
- File locations: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/File-Locations>
- Example format: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Example-Format>
- Squashing commits: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Squashing-Commits>
- Avoiding merge commits: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Avoiding-Merge-Commits>
- Updating your branch: <https://github.com/UWC2-APIDOC/to-do-service-auto/wiki/Updating-Your-Branch>
