# To-Do Service

<!-- vale Google.Parens = NO -->
<!-- vale Google.Passive = NO -->
<!-- vale write-good.Passive = NO -->

REST API sample for shared documentation practice

**Published documentation** [To-Do Service API docs](https://uwc2-apidoc.github.io/to-do-service-sp26/)

**Note**

This code is experimental and intended for instructional use only.
Use at your own risk.
No warranty of serviceability is expressed or implied.

---

## Documentation by role

### 📚 Students and contributors

**Getting started:**

1. Fork this repository to your own GitHub account
2. Set up your local environment:
    - Install [Vale](https://vale.sh/)
    - Install VS Code extensions (recommended):
        - MarkdownLint
        <!-- vale Vale.Avoid = NO -->
        <!-- vale Vale.Spelling = NO -->
        - Vale VSCode
        <!-- vale Vale.Spelling = YES -->
        <!-- vale Vale.Avoid = YES -->
3. Read the complete contributor guide:
    - [Documentation requirements](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/documentation-requirements/)
    - [Writers guide](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/writers-guide/)
    - [Validation errors reference](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/validation-errors-table/)

**What you can contribute:**

- API documentation in `/docs`
- Tutorial content
- Code examples
- Bug fixes to existing docs

**Assignment work** Students should place assignment files in `/assignments`

### 👨‍🏫 Instructors

**Course management resources:**

- [Instructor guide](reporting/_REPORTING_README.md#instructor-guide) - Understanding
    Pull request validation workflow
- [Workflow analytics](reporting/_REPORTING_README.md) - Track student submissions
- [Common student issues](reporting/_REPORTING_README.md#common-student-issues-and-solutions) -
    Quick troubleshooting reference

**Key workflows:**

- Pull request validation runs automatically on all student pull requests
- Results inform but don't determine grades
- Workflow annotations provide specific, actionable feedback

### 🔧 Maintainers

**Repository maintenance:**

- [Maintainer guide](tools/_TOOLS_README.md#maintainer-guide) - Validation scripts and workflow maintenance
- [Testing tools](tools/_TOOLS_README.md) - Test suite documentation
- [Project standards](.github/.ai/) - Code style guides and conventions

**Key maintenance tasks:**

- Update Vale rules and styles
- Update front matter schema
- Maintain Python validation scripts
- Update workflow configurations

---

## Quick links

### For everyone

- [Published API documentation](https://uwc2-apidoc.github.io/to-do-service-sp26/)
- [GitHub repository](https://github.com/rbwatson/to-do-service-sp26)
- [Project license](LICENSE)

### Repository structure

```text
to-do-service-sp26/
├── .github/
│   ├── .ai/                    # AI project knowledge
│   ├── schemas/                # Front matter validation schema
│   ├── valeStyles/             # Vale style rules
│   └── workflows/              # GitHub Actions workflows
├── api/                        # Mock API database
├── assignments/                # Student assignment submissions
├── docs/                       # Published documentation
│   ├── api/                    # API reference docs
│   ├── contributors-guide/     # Contributor documentation
│   └── tutorials/              # Tutorial content
├── postman/                    # Postman collections
├── reporting/                  # Workflow analytics tools
└── tools/                      # Validation scripts
```

---

## Contributing

All documentation follows the [writers guide](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/writers-guide/).

### Before submitting a pull request

1. Test locally with Vale and MarkdownLint
2. Ensure your branch has exactly one commit
3. Verify you only modified files in `/docs` or `/assignments`
4. Check that all Pull request validation checks pass

### Pull request validation workflow

Your pull request must pass these automated validation stages before it can be reviewed and merged:

<!-- vale write-good.TooWordy = NO -->
1. **Discover changed files** - Identifies modified files
2. **Test tools** - Validates testing infrastructure (if tools changed)
3. **Lint and validate content** - Runs Vale, MarkdownLint, and API tests
4. **Test API documentation examples** - Tests codes examples in new or changed documentation
5. **Validate commits** - Checks file locations and commit structure
<!-- vale write-good.TooWordy = YES -->

For detailed troubleshooting, see the [validation errors reference](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/validation-errors-table/).

---

## Local testing

### Install dependencies

```bash
# macOS
brew install vale

# Verify installation
vale --version
```

### Run linters locally

```bash
# Vale style checks
vale docs/

# MarkdownLint formatting checks
markdownlint docs/
```

### Test API examples

API examples require json-server:

```bash
# Install json-server
npm install -g json-server@0.17.4

# Start mock API server
json-server --watch api/to-do-db-source.json --port 3000

# In another terminal, test your documentation
python3 tools/test-api-docs.py docs/your-file.md
```

---

## Getting help

### Students

<!-- markdownlint-disable MD013 -->

- Check [validation errors table](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/validation-errors-table/) for specific error messages
- Review [documentation requirements](https://uwc2-apidoc.github.io/to-do-service-sp26/contributors-guide/documentation-requirements/)
- Ask questions in course discussion forum

<!-- markdownlint-enable MD013 -->

### Instructors

- See [instructor guide](reporting/_REPORTING_README.md#instructor-guide) for workflow interpretation
- Review [common student issues](reporting/_REPORTING_README.md#common-student-issues-and-solutions)
- Contact repository maintainers for workflow issues

### Maintainers

- See [maintainer guide](tools/_TOOLS_README.md#maintainer-guide) for detailed procedures
- Review [project standards](.github/.ai/STANDARDS_INDEX.md)
- Check GitHub Actions logs for workflow debugging

---

## License

This project is licensed under the `MIT License` - see [LICENSE](LICENSE) file for details.

---

## About this project

Sample service and documentation project for use in the Spring 2026 term of APIDOC 310 A, API Documentation.

The To-Do Service is a REST API for managing tasks and user information.
It serves as a teaching tool for learning API documentation best practices.
