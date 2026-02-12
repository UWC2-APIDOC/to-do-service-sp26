# To-Do Service

<!-- vale Google.Passive = NO -->
<!-- vale Google.Acronyms = NO -->
<!-- vale write-good.Passive = NO -->

REST API Sample for shared documentation practice

For the REST API docs, see [The To-Do Service docs](https://uwc2-apidoc.github.io/to-do-service-sp26/).

**NOTE**:

This code is experimental and is intended for instructional use only.
Use at your own risk. No warranty of serviceability is expressed or implied.

## Contributing documentation

Feel free to contribute new documentation and improve existing the existing docs.

### Configure your system

1. Fork this repository to your own GitHub account.
2. Make sure you can build a local copy of the documentation from your fork.
3. Install [Vale](https://vale.sh/) on your development or editing computer.
   To help you have a successful pull request experience, it's also helpful
   to add these extensions if you edit in VS Code:
    * `Markdownlint` or `Markdown Essentials`, which includes `Markdownlint`.
        * Configure `Markdownlint` in VS Code to use the settings defined
            in [`.github/config/.markdownlint.jsonc`](./.github/config/.markdownlint.jsonc)
    * `Vale VSCode` and configure
        * `Vale > Enable Spellcheck`: checked
        * `Vale > ValeCLI:Config`: `.vale.ini`
        * `Vale > ValeCLI:minAlertLevel`: `inherited`
        * Leave the others as the default

4. Read the detailed [Contributor's guide](https://uwc2-apidoc.github.io/to-do-service-sp26/contributing/)
    for complete information about how to create and edit files for this repo.
5. Build and test your changes locally from your feature branch before you submit a pull request, please.
