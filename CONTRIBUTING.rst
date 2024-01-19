Contribution guidelines
=======================

These guidelines instruct how to submit issues and contribute code to
the `SeleniumLibrary project`_. Other great ways to contribute include
answering questions and participating in discussions within the
#seleniumlibrary channel on the community `Robot Framework Slack`_, the
`Robot Framework Forum`_ and other channels as well as spreading the word
about the framework one way or the other.

Submitting issues
=================

Bugs and enhancements are tracked in the `issue tracker`_.
If you are unsure if something is a bug or is a feature worth
implementing, you can first ask within the `Robot Framework Slack`_. This and
other similar forums, not the issue tracker, are also places where to ask
general questions.

Before submitting a new issue, it is always a good idea to check if the
same bug or enhancement is already reported. If it is, please add your
comments to the existing issue instead of creating a new one.

Reporting bugs
--------------

Explain the bug you have encountered so that others can understand it
and preferably also reproduce it. Key things to have in good bug report:

-  Python version information
-  SeleniumLibrary, Selenium and Robot Framework version
-  Browser type and version.
-  Also the driver version, example ChromeDriver version
-  Steps to reproduce the problem. With more complex problems it is
   often a good idea to create a short, self contained, correct example
   `(SSCCE)`_.
-  Possible error message and traceback.

Notice that all information in the issue tracker is public. Do not
include any confidential information there.

Enhancement requests
====================

Describe the new feature and use cases for it in as much detail as
possible in an issue. Especially with larger enhancements, be prepared to
contribute the code in the form of a pull request as explained below or to
pay someone for the work. Consider also would it be better to implement this
functionality as a separate library outside the SeleniumLibrary. One option
here is to extend SeleniumLibrary using the public API or plug-in api. Please
see `extending documentation`_ for more details.

Code contributions
==================

If you have fixed a bug or implemented an enhancement, you can
contribute your changes via GitHub's pull requests. This is not
restricted to code, on the contrary, fixes and enhancements to
documentation\_ and tests\_ alone are also very valuable.

Code style
----------

You may find a mix of param names for the same thing, for example \`\`error\`\` and
message to indicate a custom error message. Moving forward we are going to
prefer \`\`message\`\` over \`\`error\`\`. We *may* deprecate \`\`error\`\` in the future but for
going forward, please use \`\`message\`\` with your keywords.

Choosing something to work on
-----------------------------

Often you already have a bug or an enhancement you want to work on in
your mind, but you can also look at the `issue tracker`_ to find bugs and
enhancements submitted by others. The issues vary significantly in complexity
and difficulty, so you can try to find something that matches your skill
level and knowledge.

Pull requests
-------------

On GitHub pull requests are the main mechanism to contribute code. They
are easy to use both for the contributor and for person accepting the
contribution, and with more complex contributions it is easy also for
others to join the discussion. Preconditions for creating a pull
requests are having a `GitHub account`_, installing `Git`_ and forking the
`SeleniumLibrary project`_.

GitHub has good articles explaining how to `set up Git`_, `fork a repository`_
and `use pull requests`_ and we do not go through them in more detail.
We do, however, recommend to create dedicated branches for pull requests
instead of creating them based on the master branch. This is especially
important if you plan to work on multiple pull requests at the same time.

This project asks that prior to making an enhancement pull request that you
discuss the enhancement with the team. We wish to avoid having you spend effort on an
ehancement that won't match with the project. We require that a pull request contains
linear history of commits and we do not allow that pull request contains merge commits
or other noise. This helps the review process and makes the maintenance easier for the
project administrators. Generally it is recommended to do `git pull --rebase`  instead
of the `git pull --merge` when there is need pull changes from upstream.

Coding conventions
------------------

The SeleniumLibrary team is currently reviewing, revising, and updating
the coding conventions during Q1 2024. Knowing these coding conventions
are seen as a good practice, we are leaving these here as recommendations
in the mean time but are not forcing this as a requirement for accepting
pull requests.

SeleniumLibrary uses the general Python code conventions defined in
`PEP-8`_. In addition to that, we try to write `idiomatic Python`_ or `"Pythonic" code`_
and follow the `SOLID principles`_. with all new code. An important guideline
is that the code should be clear enough that comments are generally not needed.

Docstrings should be added to public keywords but are not generally
needed in internal code. When docstrings are added, they should follow
`PEP-257`_. See `Documentation`_ section below for more details about
documentation syntax, generating docs, etc.

The code should be formatted with `Black`_ and errors found by `flake8`_
should be fixed. Black and flake8 can be run by using
command::

    inv lint

By default flake8 ignores line length error E501, but it does not ignore
warning W503. In practice Black formats list access like this::

    list[1 : 2]

But flake8 will display an warning about it. This should be manually
fixed to look like::

    list[1:2]

Documentation
-------------

With new features or enhancements adequate documentation is as important
as the actual functionality. Different documentation is needed depending
on the issue.

The main source of documentation should be placed in to the library and
individual keywords.

-  Other keywords and sections in the library introduction can be
   referenced with internal links created with backticks like \`Example
   Keyword\`

-  When referring to arguments, argument names must use in inline code
   style created with double backticks like \`\`argument\`\`.

-  Examples are recommended whenever the new keyword or enhanced
   functionality is not trivial.

-  All new enhancements or changes should have a note telling when the
   change was introduced. Often adding something like
   ``New in SeleniumLibrary 1.8.`` is enough.

Keyword documentation can be easily created using `invoke`_ task::

    inv keyword_documentation

Resulting docs should be verified before the code is committed.

Tests
-----

When submitting a pull request with a new feature or a fix, you should
always include tests for your changes. These tests prove that your
changes work, help prevent bugs in the future, and help document what
your changes do. Depending an the change, you may need ``acceptance tests``,
``unit tests`` or both.

Make sure to run all of the tests before submitting a pull request to be
sure that your changes do not break anything. If you can, test in
multiple browsers and versions (Firefox, Chrome, IE, Edge etc). Pull requests
are also automatically tested on `GitHub Actions`_.

Acceptance tests
~~~~~~~~~~~~~~~~

Most of SeleniumLibrary's testing is done using acceptance tests that
naturally use Robot Framework itself for testing. Every new
functionality or fix should generally get one or more acceptance tests.
For more details on acceptance tests and how to run the acceptance tests,
see `atest/README.rst`_.

Unit tests
~~~~~~~~~~

Unit tests are great for testing internal logic and should be added when
appropriate. For more details on unit tests and running them, see
`utest/README.rst`_.

Continuous integration
----------------------

SeleniumLibrary uses GitHub Actions as it's continuous integration (CI) server.

.. ToDo: re-add when explanation of GitHUb Actions is written
   More details about how `GitHub Actions`_ integration is implemented can be
   found within `<.github/CI/README.rst>.

Finalizing pull requests
------------------------

Once you have code, documentation and tests ready, it is time to
finalize the pull request.

Acknowledgments
~~~~~~~~~~~~~~~

If you have done any non-trivial change and would like to be credited,
remind us to add ``acknowledge`` tag to the issue. This way we will add
your name to the release notes, when next release is made.

Resolving conflicts
~~~~~~~~~~~~~~~~~~~

Conflicts can occur if there are new changes to the master that touch
the same code as your changes. In that case you should
`sync your fork`_ and `resolve conflicts`_ to allow for an easy merge.

.. _SeleniumLibrary project: https://github.com/robotframework/SeleniumLibrary
.. _Robot Framework Slack: https://rf-invite.herokuapp.com/
.. _Robot Framework Forum: https://forum.robotframework.org/c/libraries/lib-seleniumlibrary/11
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues
.. _(SSCCE): http://sscce.org
.. _extending documentation: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst
.. _GitHub account: https://github.com/
.. _Git: https://git-scm.com
.. _set up Git: https://help.github.com/articles/set-up-git/
.. _fork a repository: https://help.github.com/articles/fork-a-repo/
.. _use pull requests: https://help.github.com/articles/using-pull-requests
.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
.. _idiomatic Python: https://en.wikibooks.org/wiki/Python_Programming/Idioms
.. _"Pythonic" code: https://docs.python-guide.org/writing/style/
.. _SOLID principles: https://en.wikipedia.org/wiki/SOLID_(object-oriented_design)
.. _PEP-257: https://www.python.org/dev/peps/pep-0257/
.. _invoke: http://www.pyinvoke.org/
.. _GitHub Actions: https://github.com/robotframework/SeleniumLibrary/actions
.. _atest/README.rst: https://github.com/robotframework/SeleniumLibrary/tree/master/atest/README.rst
.. _utest/README.rst: https://github.com/robotframework/SeleniumLibrary/blob/master/utest/README.rst
.. _sync your fork: https://help.github.com/articles/syncing-a-fork/
.. _resolve conflicts: https://help.github.com/articles/resolving-a-merge-conflict-from-the-command-line
.. _Black: https://github.com/psf/black
.. _flake8: https://github.com/PyCQA/flake8