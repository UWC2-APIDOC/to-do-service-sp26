---
# markdownlint-disable
# vale off
# tags used by just-the-docs theme
layout: default
parent: Contributing
nav_order: 4
has_children: false
has_toc: false
# tags used by AI files
description: "Information about how the pull request automated testing works"
topic_type: reference
tags: 
    - docs
categories: 
    - doc-contributions
ai_relevance: low
importance: 4
prerequisites: []
related_pages: []
examples: []
api_endpoints: []
version: "v1.0"
last_updated: "2026-03-01"
# vale  on
# markdownlint-enable
---
# Pull request validation

<!-- vale write-good.TooWordy = NO -->
<!-- vale write-good.Passive = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale Google.Parens = NO -->

A beginner's guide to how automated quality testing work in this project.

---

## What's pull request validation?

<!-- vale Google.FirstPerson = NO -->

Think of pull request validation as an automated proofreader and quality checker for your work.
When you submit a pull request (PR), which is like saying "I'd like to add my changes
to the project," GitHub automatically runs a series of tests to make sure everything
is correct before anyone reviews your work.

<!-- vale Google.FirstPerson = YES -->

**Why is this helpful?**

- You get instant feedback instead of waiting for a human reviewer
- It catches common mistakes automatically and early in the process
- You learn what needs fixing through clear error messages
- Reviewers can focus on content quality, not formatting issues

---

## How it works: The big picture

When you create or update a pull request, GitHub runs a special workflow file called `pr-validation.yml`.
This file is like a checklist that tells GitHub exactly what to check.

<!-- markdownlint-disable MD013 -->

```text
You submit PR → GitHub runs pr-validation.yml → You see results → Fix issues → Repeat until all checks pass
```
<!-- markdownlint-enable MD013 -->

The workflow runs in **stages**, like checkpoints in a video game.
If you fail an early stage, the later stages don't run until you fix the issue and try again.

---

## The five stages of validation

### Stage 1: Discover what changed

**What happens** GitHub identifies which files you modified

**Why it matters** Different types of files need different checks.
For example, if you only changed documentation, there's no need to test the Python tools.

**What you see**

```text
✓ Discover changed files (15 seconds)
  - Markdown files: 3
  - Docs Markdown: 2
  - Tools files changed: false
```

**What it means** The workflow found 3 Markdown files that changed, 2 of which are in the `/docs` folder.

---

### Stage 2: Test tools

This only runs if you change a tool script, which should be uncommon.
This information is here only to give you a complete picture of the validation process.

**What happens** If you modified any files in the `/tools` directory, GitHub runs tests
to make sure those tools still work

**Why it matters** The validation tools need to work correctly.
If they're broken, they can't check your documentation.

**When this runs** Only if you changed something in `/tools`, which most students won't do.

**What you see**

```text
⊘ Validate testing tools (skipped)
```

**What it means** You didn't change any tools, so validation skips this step. That's normal.

**If you DO see this run**

```text
✓ Validate testing tools (45 seconds)
  All tool tests passed
```

---

### Stage 3: lint and validate content

**What happens** This stage checks your Markdown files for:

- **Filenames** - No spaces or weird characters
- **Linter exceptions** - Counts how many style rules you turned off
- **Markdown structure** - Headings, lists, code blocks
- **MarkdownLint** - Formatting rules, such as heading styles, line length, etc.
- **Vale** - Writing style rules, such as active voice, word choice, etc.

All five of these checks run at the same time.

**Why it matters** These checks ensure your documentation follows the project's style guide
and is properly formatted

**What you see**

```text
✓ Lint Markdown files (2 minutes)
  ✓ Test filenames
  ✓ List linter exceptions  
  ✓ Survey Markdown
  ✓ Run MarkdownLint
  ✓ Run Vale
```

**Common issues you might see**

❌ **Filename error**

```text
✗ Test filenames
  ::error file=My File.md::Filename contains spaces
```

**Fix** Rename file to `my-file.md` to use hyphens instead of spaces

❌ **MarkdownLint error**

```text
✗ Run MarkdownLint
  ::error file=docs/api.md,line=15::MD013 Line too long
```

**Fix** Break the long line into shorter lines.
The repos' style guide requires lines with 100 characters or fewer.

❌ **Vale error**

```text
✗ Run Vale
  ::error file=docs/tutorial.md,line=23::Google.Passive Avoid passive voice
```

**Fix** Change "The button is clicked" to "Click the button"

---

### Stage 4: Test API documentation examples

**What happens** If you added or changed documentation that includes API examples
(like curl commands), GitHub runs those examples against a test server to make sure they actually work.

**Why it matters** Nothing is more frustrating than following a tutorial and having the
examples not work. This ensures your code examples are accurate.

**When this runs** Only if you changed files in `/docs` or `/assignments` that contain
testable API examples

**What you see**

```text
✓ Test API documentation examples (1 minute)
  Testing: docs/api/get-user.md
  PASSED: docs/api/get-user.md
  All API examples tested successfully
```

**How it knows what to test** Your Markdown file needs special **_front matter_**,
which is the metadata at the top of a documentation topic and looks like this:

```Markdown
---
test:
  testable:
    - "Get user example / 200"
    - "Create user example / 201"
---
```

**Common issues**

❌ **Missing front matter**

```text
✗ Test API documentation examples
  ::error file=docs/api.md::Front matter is required for files in /docs directory
```

**Fix** Add YAML front matter to the top of your file

❌ **Example doesn't work**

```text
✗ Test API documentation examples
  FAILED: docs/api/get-user.md
  Expected status 200, got 4040
```

**Fix** Check your API endpoint URL or expected response.
Also, check the front matter to make sure your test is configured correctly.

---

### Stage 5: Validate commits

**What happens** GitHub checks that your pull request follows these rules:

- You only changed files in `/docs` or `/assignments`
- Your PR has exactly one commit
- Your commit isn't a "merge commit"

**Why it matters** These rules keep the project organized and make it easier
for reviewers to understand your changes.

**What you see**

```text
✓ Validate commit structure (10 seconds)
  ✓ Check unauthorized file changes
  ✓ Check if branch is up to date
  ✓ Check commit requirements
  Ready to merge - commit structure valid
```

**Common issues**

❌ **Too many commits**

```text
✗ Validate commit structure
  ::error::Pull request must contain exactly one commit; found 3
  Help: [Squashing Commits link]
```

**Fix** Combine the commits in your pull request into one commit by using Git's **_squash_** operation

❌ **Wrong files changed**

```text
✗ Validate commit structure  
  ::error::Only files in /docs/ and /assignments/ can be modified
  Changed: .github/workflows/pr-validation.yml
```

**Fix** Only make changes to files in the allowed directories

---

## Where to see results

### In your pull request

When you open your PR on GitHub, scroll down to see the "Checks" section:

```text
All checks have passed
✓ Discover changed files
✓ Lint Markdown files  
✓ Test API documentation examples
✓ Validate commit structure
```

Or if something failed:

```text
Some checks were not successful
✓ Discover changed files
✗ Lint Markdown files (see details)
✓ Test API documentation examples
✓ Validate commit structure
```

Click "Details" next to any check to see what went wrong.

### In the actions tab

For more detail, click the **Actions** tab at the top of the repository,
then click your workflow run. You'll see:

1. **Summary** - Overview of what passed/failed
2. **Jobs** - Each stage and its steps
3. **Annotations** - Specific errors with file and line numbers

---

## Reading error messages

Error messages follow this pattern:

```text
::error file=path/to/file.md,line=42::Description of the problem
```

Breaking this down:

- `::error` - This is an error. It might also be annotated as a `::warning`.
- `file=path/to/file.md` - The file with the problem
- `line=42` - The specific line number, if applicable
- `Description of the problem` - What's wrong and sometimes how to fix it

**Example**

```text
::error file=docs/api/users.md,line=23::Google.Passive Avoid passive voice
```

This tells you:

- There's a **style error** in `docs/api/users.md`
- It's on **line 23**
- The problem is **passive voice**
- You need to rewrite that sentence in active voice

---

## Common questions

<!-- vale Google.FirstPerson = NO -->

### Why did my check fail even though I didn't change that file?

Sometimes the validation runs on files you didn't directly change. For example:

- If you changed the test tools, all documentation gets re-tested
- If the workflow file itself changed, everything re-runs

### Can I skip a check?

No. All checks must pass before your pull request can be reviewed and merged.

- Add linter exceptions for specific style rules.
    Use this option as a last resort and explain its use in the pull request details.
- Ask an instructor for help if something seems wrong.

### How long does validation take?

Typically 2-4 minutes total. Breakdown:

- Stage 1 (Discover): 10-15 seconds
- Stage 2 (Test tools): Normally skipped (or ~45 seconds)
- Stage 3 (Lint): 1-2 minutes
- Stage 4 (API tests): 30 seconds - 1 minute (if applicable)
- Stage 5 (Commits): 10 seconds

Note, the testing might not start immediately after you create or update your pull request.

### What if the checks keep running forever?

If a check runs for more than 10 minutes, something is wrong:

1. Refresh the page to see if it completed
2. Cancel the workflow and try again
3. Ask an instructor for help

<!-- vale Google.FirstPerson = YES -->

---

## Tips for success

The best case scenario is when you submit your pull request and it passes
all the validation the first time.
Here are some ways to make that more likely to occur.

### Before you submit your pull request

- [Add the runtime tools to your IDE](https://github.com/UWC2-APIDOC/to-do-service-sp26#-students-and-contributors)
and use them while you're editing.

- Add the runtime tools to your system and run these checks locally on your computer
    with each file that you've changed before creating the PR:

    ```bash
    # Check with Vale (style guide)
    vale docs/your-file.md

    # Check with MarkdownLint (formatting)
    Markdownlint docs/your-file.md
    ```

    This catches most issues before GitHub does.

- Create a draft pull request from your feature branch and the tests run
each time you add a commit and push the update to your branch.

### After the GitHub tests run

1. **Don't panic if you see red X's** - Everyone gets errors sometimes
2. **Read the error messages carefully** - They tell you exactly where the problem is
3. **Fix one thing at a time** - Don't try to fix everything at once
4. **Push changes to your branch** - GitHub automatically re-run the checks when you update the branch

### Making changes after a failed test

1. Fix the issues in your files
2. Stage your changes

    ```bash
    git add docs/your-file.md
    ```

3. Amend your existing commit

    ```bash
    git commit --amend --no-edit
    git push --force
    ```

    You can also create new commit with your change as long as you
    remember to squash all the new commits in your feature branch
    before you push the changes to your branch.

Remember, GitHub automatically re-runs validation when you push.

---

## The workflow in Action: A real example

<!-- vale Google.We = NO -->

Let's walk through what happens when you submit a PR:

<!-- vale Google.We = YES -->

**You submit a PR with**

- Added file: `docs/api/get-task.md`
- Modified file: `docs/tutorials/quickstart.md`

**GitHub runs**

1. **Discover changed files** ✓

   ```text
   Found:
   - 2 Markdown files
   - 2 docs Markdown files
   - No tools changed
   ```

2. **Test tools** ⊘ (skipped - you didn't change tools)

3. **Lint Markdown files** ✓

   ```test
   Testing: docs/api/get-task.md, docs/tutorials/quickstart.md
   - Filenames: OK
   - MarkdownLint: OK
   - Vale: 2 warnings about passive voice
   ```

   **Result** Passed (warnings don't fail the check)

4. **Test API examples** ✓

   ```text
   Testing: docs/api/get-task.md
   - Testing "Get task example / 200"
   - Status: 200 ✓
   - Response matches: ✓
   PASSED
   ```

5. **Validate commits** ✓

   ```text
   - Files in allowed directories: ✓
   - Exactly 1 commit: ✓
   - No merge commits: ✓
   ```

**Result** All checks passed. Your PR is ready for human review.

---

## Summary

Pull request validation is your friend, not your enemy. It:

- Runs automatically when you submit or update a PR
- Checks your work in stages: **discover → test tools → lint → test API → validate commits**
- Gives you specific, actionable feedback
- Ensures quality before human reviewers look at your work
- Saves time for everyone

**Remember** The goal isn't to make your life harder.
It's there to help you submit high-quality work and learn best practices for documentation.

---

## Getting help

If validation keeps failing and you're not sure why:

1. **Read the error messages carefully** - They often include links to more information
2. **Check the common issues** - section in this guide
3. **Look at the contributor guide** - for examples of correct formatting
4. **Ask in your course discussion forum** - Others might have the same question
5. **Contact your instructor** - They can help diagnose tricky issues

**Helpful resources**

- [Validation errors reference](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/validation-errors-table/)
- [Writers guide](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/writers-guide/)
- [Documentation requirements](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/documentation-requirements/)
