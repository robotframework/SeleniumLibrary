# Contribution guidelines

These guidelines instruct how to submit issues and contribute code to the
[Selenium2Library project](https://github.com/robotframework/Selenium2Library).
Other great ways to contribute include answering questions and participating
discussion on
[robotframework-users](https://groups.google.com/forum/#!forum/robotframework-users)
mailing list and other forums as well as spreading the word about the framework one way or
the other.


# Submitting issues

Bugs and enhancements are tracked in the
[issue tracker](https://github.com/robotframework/Selenium2Library/issues).
If you are unsure if something is a bug or is a feature worth implementing, you can
first ask on
[robotframework-users](https://groups.google.com/forum/#!forum/robotframework-users)
list. This and other similar forums, not the issue tracker, are also places where to ask
general questions.

Before submitting a new issue, it is always a good idea to check is the
same bug or enhancement already reported. If it is, please add your comments
to the existing issue instead of creating a new one.

## Reporting bugs
Explain the bug you have encountered so that others can understand it
and preferably also reproduce it. Key things to have in good bug report:

- Version information
   - Selenium2Library, Selenium and Robot Framework version
   - Browser type and version.
   - Also the driver version, example ChromeDriver version
- Steps to reproduce the problem. With more complex problems it is often a good idea
  to create a [short, self contained, correct example (SSCCE)](http://sscce.org).
- Possible error message and traceback.

Notice that all information in the issue tracker is public. Do not include
any confidential information there.

# Enhancement requests
Describe the new feature and use cases for it in as much detail as possible.
Especially with larger enhancements, be prepared to contribute the code
in form of a pull request as explained below or to pay someone for the work.
Consider also would it be better to implement this functionality as a separate
tool outside the core framework.

# Code contributions

If you have fixed a bug or implemented an enhancement, you can contribute
your changes via GitHub's pull requests. This is not restricted to code,
on the contrary, fixes and enhancements to documentation_ and tests_ alone
are also very valuable.

## Choosing something to work on
Often you already have a bug or an enhancement you want to work on in your
mind, but you can also look at the
[issue tracker](https://github.com/robotframework/Selenium2Library/issues)
to find bugs and enhancements submitted by others. The issues vary significantly
in complexity and difficulty, so you can try to find something that matches
your skill level and knowledge.

## Pull requests
On GitHub pull requests are the main mechanism to contribute code. They
are easy to use both for the contributor and for person accepting
the contribution, and with more complex contributions it is easy also
for others to join the discussion. Preconditions for creating a pull
requests are having a [GitHub account](https://github.com/),
installing [Git](https://git-scm.com) and forking the
[Selenium2Library project](https://github.com/robotframework/Selenium2Library).

GitHub has good articles explaining how to
[set up Git](https://help.github.com/articles/set-up-git/),
[fork a repository](https://help.github.com/articles/fork-a-repo/) and
[use pull requests](https://help.github.com/articles/using-pull-requests)
and we do not go through them in more detail. We do, however,
recommend to create dedicated branches for pull requests instead of creating
them based on the master branch. This is especially important if you plan to
work on multiple pull requests at the same time.

## Coding conventions
Selenium2Library uses the general Python code conventions defined in
[PEP-8](https://www.python.org/dev/peps/pep-0008/). In addition to that, we try
to write
[idiomatic Python](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html)
and follow the
[SOLID principles](https://en.wikipedia.org/wiki/SOLID_(object-oriented_design))
with all new code. An important guideline is that the code should be clear enough that
comments are generally not needed.

Docstrings should be added to public keywords but are not generally needed in
internal code. When docstrings are added, they should follow
[PEP-257](https://www.python.org/dev/peps/pep-0257/).
See [Documentation](#documentation) section below for more details about
documentation syntax, generating docs, etc.

We are pretty picky about using whitespace. We use blank lines and whitespace
in expressions as dictated by [PEP-8](https://www.python.org/dev/peps/pep-0008/)
, but we also follow these rules:

- Indentation using spaces, not tabs.
- No trailing spaces.
- No extra empty lines at the end of the file.
- Files must end with a newline.

The above rules are good with most other code too. Any good editor or IDE
can be configured to automatically format files according to them.

## Documentation
With new features or enhancements adequate documentation is as important as the
actual functionality. Different documentation is needed depending on the issue.

The main source of documentation should be placed in to the library and
individual keywords. But enhancing the internal
[wiki](https://github.com/robotframework/Selenium2Library/wiki)
or other documentation is equally important.

- Other keywords and sections in the library introduction can be referenced
  with internal links created with backticks like \`Example Keyword\`

- When referring to arguments, argument names must use in inline code style
  created with double backticks like \`\`argument\`\`.

- Examples are recommended whenever the new keyword or enhanced functionality is
  not trivial.

- All new enhancements or changes should have a note telling when the change
  was introduced. Often adding something like ``New in Selenium2Libray 1.8.``
  is enough.

Keyword documentation can be easily created using `<doc/generate.py>`_
script. Resulting docs should be verified before the code is committed.

## Tests
When submitting a pull request with a new feature or a fix, you should
always include tests for your changes. These tests prove that your changes
work, help prevent bugs in the future, and help document what your changes
do. Depending an the change, you may need `acceptance tests`_, `unit tests`_
or both.

Make sure to run all of the tests before submitting a pull request to be sure
that your changes do not break anything. If you can, test in multiple
browsers and versions (Firefox, Chrome, IE, etc). Pull requests are also
automatically tested on `continuous integration`_.

### Acceptance tests
Most of Selenium2Library's testing is done using acceptance tests that
naturally use Robot Framework itself for testing. Every new functionality
or fix should generally get one or more acceptance tests. See
[Unit and acceptance tests](https://github.com/robotframework/Selenium2Library/blob/master/BUILD.rst#unit-and-acceptance-tests>)
for more details about creating and executing them.

### Unit tests


Unit tests are great for testing internal logic and should be added when
appropriate. For more details see
[Unit and acceptance tests](https://github.com/robotframework/Selenium2Library/blob/master/BUILD.rst#unit-and-acceptance-tests>).

## Continuous integration
Selenium2Library's continuous integration (CI) servers are visible through
[travis-ci](https://travis-ci.org/robotframework/Selenium2Library).
They automatically test all new pull request to the repository with Firefox on Python 2.6
and 2.7.

## Finalizing pull requests
Once you have code, documentation and tests ready, it is time to finalize
the pull request.

### AUTHORS.txt
If you have done any non-trivial change and would like to be credited,
add yourself to
[AUTHORS.txt](https://github.com/robotframework/Selenium2Library/blob/master/AUTHORS.txt)
file.

### Resolving conflicts
Conflicts can occur if there are new changes to the master that touch the
same code as your changes. In that case you should
[sync your fork](https://help.github.com/articles/syncing-a-fork>) and
[resolve conflicts](https://help.github.com/articles/resolving-a-merge-conflict-from-the-command-line)
to allow for an easy merge.

The most common conflicting file is the aforementioned
[AUTHORS.txt](https://github.com/robotframework/Selenium2Library/blob/master/AUTHORS.txt)
, but luckily fixing those conflicts is typically easy.

### Squashing commits
If the pull request contains multiple commits, it is recommended that you
squash them into a single commit before the pull request is merged.
See
[Squashing Github pull requests into a single commit](http://eli.thegreenplace.net/2014/02/19/squashing-github-pull-requests-into-a-single-commit)
article for more details about why and how.

Squashing is especially important if the pull request contains lots of
temporary commits and changes that have been later reverted or redone.
Squashing is not needed if the commit history is clean and individual
commits are meaningful alone.
