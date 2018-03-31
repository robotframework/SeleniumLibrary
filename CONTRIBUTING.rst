Contribution guidelines
=======================

These guidelines instruct how to submit issues and contribute code to
the `SeleniumLibrary project`_. Other great ways to contribute include
answering questions and participating discussion on `robotframework-users`_
mailing list and other forums as well as spreading the word about the
framework one way or the other.

Submitting issues
=================

Bugs and enhancements are tracked in the `issue tracker`_.
If you are unsure if something is a bug or is a feature worth
implementing, you can first ask on `robotframework-users`_ list. This and
other similar forums, not the issue tracker, are also places where to ask
general questions.

Before submitting a new issue, it is always a good idea to check is the
same bug or enhancement already reported. If it is, please add your
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
contribute the code in form of a pull request as explained below or to
pay someone for the work. Consider also would it be better to implement this
functionality as a separate library outside the SeleniumLibrary.

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

Coding conventions
------------------

SeleniumLibrary uses the general Python code conventions defined in
`PEP-8`_. In addition to that, we try to write `idiomatic Python`_
and follow the `SOLID principles`_. with all new code. An important guideline
is that the code should be clear enough that comments are generally not needed.

Docstrings should be added to public keywords but are not generally
needed in internal code. When docstrings are added, they should follow
`PEP-257`_. See `Documentation`_ section below for more details about
documentation syntax, generating docs, etc.

We are pretty picky about using whitespace. We use blank lines and
whitespace in expressions as dictated by
`PEP-8`_, but we also follow these rules:

-  Indentation using spaces, not tabs.
-  No trailing spaces.
-  No extra empty lines at the end of the file.
-  Files must end with a newline.

The above rules are good with most other code too. Any good editor or
IDE can be configured to automatically format files according to them.

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
   ``New in SeleniumLibray 1.8.`` is enough.

Keyword documentation can be easily created using `invoke`_ task::

    inv keyword_documentation

Resulting docs should be verified before the code is committed.

Tests
-----

When submitting a pull request with a new feature or a fix, you should
always include tests for your changes. These tests prove that your
changes work, help prevent bugs in the future, and help document what
your changes do. Depending an the change, you may need
``acceptance tests``\ *, ``unit tests``* or both.

Make sure to run all of the tests before submitting a pull request to be
sure that your changes do not break anything. If you can, test in
multiple browsers and versions (Firefox, Chrome, IE, Edge etc). Pull requests
are also automatically tested on `Travis CI`_.

Acceptance tests
~~~~~~~~~~~~~~~~

Most of SeleniumLibrary's testing is done using acceptance tests that
naturally use Robot Framework itself for testing. Every new
functionality or fix should generally get one or more acceptance tests.

Unit tests
~~~~~~~~~~

Unit tests are great for testing internal logic and should be added when
appropriate. For more details see `Unit and acceptance
tests <https://github.com/robotframework/SeleniumLibrary/blob/master/BUILD.rst#unit-and-acceptance-tests%3E>`__.

Continuous integration
----------------------

SeleniumLibrary's continuous integration (CI) servers are visible through
`Travis CI`_. For more details about how to run test and how `Travis CI`_
integration is implemented can be found from the `test/README.rst`_.

Finalizing pull requests
------------------------

Once you have code, documentation and tests ready, it is time to
finalize the pull request.

CHANGES.rst
~~~~~~~~~~~

If you have done any non-trivial change and would like to be credited,
add yourself to `CHANGES.rst`_ file.

Resolving conflicts
~~~~~~~~~~~~~~~~~~~

Conflicts can occur if there are new changes to the master that touch
the same code as your changes. In that case you should
`sync your fork`_ and `resolve conflicts`_ to allow for an easy merge.

The most common conflicting file is the aforementioned
`CHANGES.rst`_, but luckily fixing those conflicts is typically easy.

.. _SeleniumLibrary project: https://github.com/robotframework/SeleniumLibrary
.. _robotframework-users: http://groups.google.com/group/robotframework-users
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues
.. _(SSCCE): http://sscce.org
.. _GitHub account: https://github.com/
.. _Git: https://git-scm.com
.. _set up Git: https://help.github.com/articles/set-up-git/
.. _fork a repository: https://help.github.com/articles/fork-a-repo/
.. _use pull requests: https://help.github.com/articles/using-pull-requests
.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
.. _idiomatic Python: http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
.. _SOLID principles: https://en.wikipedia.org/wiki/SOLID_(object-oriented_design)
.. _PEP-257: https://www.python.org/dev/peps/pep-0257/
.. _invoke: http://www.pyinvoke.org/
.. _Travis CI: https://travis-ci.org/robotframework/SeleniumLibrary
.. _test/README.rst`: https://github.com/robotframework/SeleniumLibrary/blob/master/test/README.rst
.. _CHANGES.rst: https://github.com/robotframework/SeleniumLibrary/blob/master/CHANGES.rst
.. _sync your fork: https://help.github.com/articles/syncing-a-fork/
.. _resolve conflicts: https://help.github.com/articles/resolving-a-merge-conflict-from-the-command-line
