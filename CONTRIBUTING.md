# Contributing to Collab Coursebook

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to Collab Coursebook. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.


#### Table Of Contents

[Code of Conduct](#code-of-conduct)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [First Contribution](#first-contributions)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Documentation Styleguide](#documentation-styleguide)
  * [Python Styleguide](#python-styleguide)

[Labels within the Repository](#labels-within-the-repository)


## Code of Conduct

This project has a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the current maintainers.


## How Can I Contribute?


### Reporting Bugs

Bug reports should help to understand the issue, reproduce the behavior, and find related reports.

Before creating bug reports, please check open issues as you might find out that you don't need to create a new one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). Fill out any applicable template to help us resolve issues faster.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.


#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as GitLab issues.
Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use Markdown code blocks.
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots** which show you following the steps and demonstrate the problem.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version?** What's the most recent version in which the problem doesn't happen?
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version (commit)) are you using?**
* **What's the OS you're using**?

### Suggesting Enhancements

This section describes submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

Before creating enhancement suggestions, please check the software does not provide this functionality already or there is already an open issue suggesting it, as you might find out that you don't need to create a new one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion). Fill in any applicable templates, including the steps that you imagine you would take if the feature you're requesting existed.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as GitLab issues. Create an issue on that repository and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as Markdown code blocks.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots** which help you demonstrate the steps or point out the part of the software which the suggestion is related to.
* **Explain why this enhancement would be useful** to users.

### First Contributions

Contributions to Collab Coursebook are wanted! They may consist of code, documentation, testing, reporting etc.
Unsure where to begin? You can start by looking through `beginner` and `help-wanted` issues:

* Beginner issues - issues which should only require a few lines of code, and a test or two.
* Help wanted issues - issues which should be a bit more involved than `beginner` issues.

Do not hesitate to contact the current maintainers if you have any questions. We will be glad to help you get started.

### Pull Requests

Please follow these steps with your contributions:

1. Follow all instructions in any template we provide.
1. Follow the [styleguides](#styleguides)

While the prerequisites above must be satisfied prior to having your pull request reviewed, reviewers may ask you to complete additional design work, tests, or other changes before your pull request can be accepted.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line


### Documentation Styleguide

* Please use [GitLab Flavored Markdown (GFM)](https://docs.gitlab.com/ee/user/markdown.html).


### Python Styleguide

* Follow [PEP8](https://www.python.org/dev/peps/pep-0008/).
* If you use PyCharm, you can use its standard auto formatting settings.


## Labels within the Repository

This section lists the labels used to track and manage issues or pull requests.

GitLab's search functions makes it easy to use labels for finding groups of issues or pull requests.
The labels are loosely grouped by their purpose, but it's not required that every issue have a label from every group or that an issue can't have more than one label from the same group.

Please open an issue if you have suggestions for new labels.

### Issue Lables (Types and States)

| Label name | Description |
| --- | --- |
| `feature` | Feature requests. |
| `bug` | Confirmed bugs or reports that are very likely bugs. |
| `question` | Questions more than bug reports or feature requests. |
| `feedback` | General feedback more than bug reports or feature requests. |
| `meta` | Issues or tasks related to documentation or repository matters. |
| `help-wanted` | Maintainers explicitly appreciate help in resolving this issue. |
| `beginner` | Less complex issues which would be good first issues to work on for users who want to contribute. |
| `more-information-needed` | More information needs to be collected about these problems or feature requests. |
| `blocked` | Issues blocked on other issues. |
| `duplicate` | Issues which are duplicates of other issues, i.e. they have been reported before. |
| `wontfix` | Issues that cannot or will not be fixed for now, either because they're working as intended or for some other reason. |
| `low-priority` | Issues that are meant to be remembered, but are low priority i.e. do not need to be fixed to maintain functionality or enable users to perform intended actions. These might take a while to resolve. |
| `high-priority` | Issues that should be resolved as soon as possible. |


### Pull Request Labels

| Label name | Description |
| --- | --- |
| `work-in-progress` | Pull requests which are still being worked on, more changes will follow. |
| `needs-review` | Pull requests which need code review, and approval from maintainers. |
| `under-review` | Pull requests being reviewed by maintainers. |
| `requires-changes` | Pull requests which need to be updated based on review comments and then reviewed again. |
| `needs-testing` | Pull requests which need manual testing. |
