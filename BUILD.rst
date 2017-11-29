Creating SeleniumLibrary releases
=================================

These instructions cover steps needed to create new releases of SeleniumLibrary.
Many individual steps are automated, but we don't want to automate
the whole procedure because it would be hard to react if something goes
terribly wrong. When applicable, the steps are listed as commands that can
be copied and executed on the command line.

.. contents::
   :depth: 1

Preconditions
-------------

Operating system and Python requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generating releases has only been tested on Linux, but it ought to work the
same way also on OSX and other unixes. Generating releases on Windows may
work but is not tested, supported, or recommended.

Creating releases is only supported with Python 3.6 or newer. If you are
using Ubuntu or one of its derivatives and don't have Python 3.6 in the
official package repository, you may consider using the
`Dead Snakes PPA <https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa>`_.

The ``pip`` and ``invoke`` commands below are also expected to run on Python
3.6+. Alternatively, it's possible to use the ``python3.6 -m pip`` approach
to run these commands.

Python dependencies
~~~~~~~~~~~~~~~~~~~

Many steps are automated using the generic `Invoke <http://pyinvoke.org>`_
tool with a help by our `rellu <https://github.com/robotframework/rellu>`_
utilities, but also other tools and modules are needed. A pre-condition is
installing all these, and that's easiest done using `pip
<http://pip-installer.org>`_ and the provided `<requirements-build.txt>`_ file::

    pip install -r requirements-build.txt

Using Invoke
~~~~~~~~~~~~

Invoke tasks are defined in the `<tasks.py>`_ file and they are executed from
the command line like::

    inv[oke] task [options]

Run ``invoke`` without arguments for help. All tasks can be listed using
``invoke --list`` and each task's usage with ``invoke --help task``.

Different Git workflows
~~~~~~~~~~~~~~~~~~~~~~~

Git commands used below always expect that ``origin`` is the project main
repository. If that's not the case, and instead ``origin`` is your personal
fork, you probably still want to push to the main repository. In that case
you need to add ``upstream`` or similar to ``git push`` commands before
running them.

Testing
-------

Make sure that adequate tests are executed before releases are created.
See `<test/README.rst>`_ for details.

Preparation
-----------

1. Check that you are on the master branch and have nothing left to commit,
   pull, or push::

      git branch
      git status
      git pull --rebase
      git push

2. Clean up::

      invoke clean

3. Set version information to a shell variable to ease copy-pasting further
   commands. Add ``aN``, ``bN`` or ``rcN`` postfix if creating a pre-release::

      VERSION=<version>

   For example, ``VERSION=3.0.1`` or ``VERSION=3.1a2``.

Release notes
-------------

1. Set GitHub user information into shell variables to ease copy-pasting the
   following command::

      GITHUB_USERNAME=<username>
      GITHUB_PASSWORD=<password>

   Alternatively, supply the credentials when running that command.

2. Generate a template for the release notes::

      invoke release-notes -w -v $VERSION -u $GITHUB_USERNAME -p $GITHUB_PASSWORD

   The ``-v $VERSION`` option can be omitted if `version is already set
   <Set version_>`__. Omit the ``-w`` option if you just want to get release
   notes printed to the console, not written to a file.

   When generating release notes for a preview release like ``3.0.2rc1``,
   the list of issues is only going to contain issues with that label
   (e.g. ``rc1``) or with a label of an earlier preview release (e.g.
   ``alpha1``, ``beta2``).

2. Fill the missing details in the generated release notes template.

3. Make sure that issues have correct information:

   - All issues should have type (bug, enhancement or task) and priority set.
     Notice that issues with the task type are automatically excluded from
     the release notes.
   - Issue priorities should be consistent.
   - Issue titles should be informative. Consistency is good here too, but
     no need to overdo it.

   If information needs to be added or edited, its better to edit it in the
   issue tracker than in the generated release notes. This allows re-generating
   the list of issues later if more issues are added.

4. Add, commit and push::

      git add docs/SeleniumLibrary-$VERSION.rst
      git commit -m "Release notes for $VERSION" docs/SeleniumLibrary-$VERSION.rst
      git push

5. Update later if necessary. Writing release notes is typically the biggest
   task when generating releases, and getting everything done in one go is
   often impossible.

Set version
-----------

1. Set version information in `<src/SeleniumLibrary/__init__.py>`_::

      invoke set-version $VERSION

2. Commit and push changes::

      git commit -m "Updated version to $VERSION" src/SeleniumLibrary/__init__.py
      git push

Documentation
-------------

1. Generate keyword documentation::

      invoke kw-docs
      git commit -m "Generated docs for version $VERSION" docs/SeleniumLibrary.html
      git push

   Note that this *must* be done after`setting version <Set version>`_ above
   or docs will have wrong version number.

2. If README.rst has changed, generate project documentation based on it::

      invoke project-docs
      git commit -m "Regenerated project docs" docs/index.html
      git push

Tagging
-------

1. Create an annotated tag and push it::

      git tag -a v$VERSION -m "Release $VERSION"
      git push --tags

2. Add short release notes to GitHub's `releases page
   <https://github.com/robotframework/SeleniumLibrary/releases>`_
   with a link to the full release notes.

Creating distributions
----------------------

1. Checkout the earlier created tag if necessary::

      git checkout v$VERSION

   This isn't necessary if continuing right after tagging_.

2. Cleanup (again). This removes temporary files as well as ``build`` and
   ``dist`` directories::

      invoke clean

3. Create source distribution and universal (i.e. Python 2 and 3 compatible)
   `wheel <http://pythonwheels.com>`_::

      python setup.py sdist bdist_wheel --universal
      ls -l dist

   Distributions can be tested locally if needed.

4. Upload distributions to PyPI::

      twine upload dist/*

5. Verify that project the page at `PyPI
   <https://pypi.python.org/pypi/robotframework-seleniumlibrary>`_
   looks good.

6. Test installation (add ``--pre`` with pre-releases)::

      pip install --upgrade robotframework-seleniumlibrary

Post actions
------------

1. Back to master if needed::

      git checkout master

2. Set dev version based on the previous version::

      invoke set-version dev
      git commit -m "Back to dev version" src/SeleniumLibrary/__init__.py
      git push

   For example, ``1.2.3`` is changed to ``1.2.4.dev1`` and ``2.0.1a1``
   to ``2.0.1a2.dev1``.

3. Close the `issue tracker milestone
   <https://github.com/robotframework/SeleniumLibrary/milestones>`_.
   Create also new milestone for the next release unless one exists already.

Announcements
-------------

1. `robotframework-users <https://groups.google.com/group/robotframework-users>`_
   and
   `robotframework-announce <https://groups.google.com/group/robotframework-announce>`_
   lists. The latter is not needed with preview releases but should be used
   at least with major updates. Notice that sending to it requires admin rights.

2. Twitter. Either Tweet something yourself and make sure it's re-tweeted
   by `@robotframework <http://twitter.com/robotframework>`_, or send the
   message directly as `@robotframework`. This makes the note appear also
   at http://robotframework.org.

   Should include a link to more information. Possibly a link to the full
   release notes or an email to the aforementioned mailing lists.

3. ``#seleniumlibrary`` channel on the Slack community. Possibly also
   ``#general`` with major releases.

4. `Robot Framework LinkedIn
   <https://www.linkedin.com/groups/Robot-Framework-3710899>`_ group.
   At least with major updates.

5. Consider sending announcements, at least with major releases, also to other
   forums where we want to make the library more well known. This includes
   Selenium forums as well as general testing and test automation forums.

   Need to possibly format the message slightly differently as not all
   recipients are familiar with Robot Framework nor this library.
