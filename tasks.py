import sys
from pathlib import Path

import bs4
from docutils.core import publish_cmdline
from invoke import task
from rellu import initialize_labels, ReleaseNotesGenerator, Version
from rellu.tasks import clean  # noqa
from robot.libdoc import libdoc


assert Path.cwd() == Path(__file__).parent

VERSION_PATTERN = '__version__ = "(.*)"'
REPOSITORY = "robotframework/SeleniumLibrary"
VERSION_PATH = Path("src/SeleniumLibrary/__init__.py")
RELEASE_NOTES_PATH = Path("docs/SeleniumLibrary-{version}.rst")
RELEASE_NOTES_TITLE = "SeleniumLibrary {version}"
RELEASE_NOTES_INTRO = """
SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary {version} is a new release with
**UPDATE** enhancements and bug fixes. **ADD more intro stuff...**

**REMOVE this section with final releases or otherwise if release notes contain
all issues.**
All issues targeted for SeleniumLibrary {version.milestone} can be found
from the `issue tracker`_.

**REMOVE ``--pre`` from the next command with final releases.**
If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary=={version}

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary {version} was released on {date}. SeleniumLibrary supports
Python **ADD VERSIONS**, Selenium **ADD VERSIONS** and
Robot Framework **ADD VERSIONS**.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3A{version.milestone}
"""


@task
def kw_docs(ctx, version=None):
    """Generates the library keyword documentation.
    Args:
        version:  Appends version to the end of the filename.
                  Used for alpha and beta release.

    Documentation is generated by using the Libdoc tool.
    """
    if version:
        out = Path(f"docs/SeleniumLibrary-{version}.html")
    else:
        out = Path("docs/SeleniumLibrary.html")
    libdoc(str(Path("src/SeleniumLibrary")), str(out))
    with out.open("r") as file:
        data = file.read()
    soup = bs4.BeautifulSoup(data, "html.parser")
    script_async = soup.new_tag(
        "script", src="https://www.googletagmanager.com/gtag/js?id=UA-106835747-4"
    )
    script_async.attrs["async"] = None
    soup.head.append(script_async)
    script_data = soup.new_tag("script")
    script_data.string = """
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-106835747-4', {
    'anonymize_ip': true,
    'page_path': location.pathname+location.search+location.hash });
window.onhashchange = function() { 
    gtag('event', 'HashChange', {
    'event_category': 'Subsection',
    'event_label': window.location.hash
     });
}    
"""
    soup.head.append(script_data)
    with out.open("w") as file:
        file.write(str(soup))


@task
def project_docs(ctx):
    """Generate project documentation.

    These docs are visible at http://robotframework.org/SeleniumLibrary/.
    """
    args = [
        "--stylesheet=style.css,extra.css",
        "--link-stylesheet",
        "README.rst",
        "docs/index.html",
    ]
    publish_cmdline(writer_name="html5", argv=args)
    print(Path(args[-1]).absolute())


@task
def set_version(ctx, version):
    """Set project version in `src/SeleniumLibrary/__init__.py`` file.

    Args:
        version: Project version to set or ``dev`` to set development version.

    Following PEP-440 compatible version numbers are supported:
    - Final version like 3.0 or 3.1.2.
    - Alpha, beta or release candidate with ``a``, ``b`` or ``rc`` postfix,
      respectively, and an incremented number like 3.0a1 or 3.0.1rc1.
    - Development version with ``.dev`` postfix and an incremented number like
      3.0.dev1 or 3.1a1.dev2.

    When the given version is ``dev``, the existing version number is updated
    to the next suitable development version. For example, 3.0 -> 3.0.1.dev1,
    3.1.1 -> 3.1.2.dev1, 3.2a1 -> 3.2a2.dev1, 3.2.dev1 -> 3.2.dev2.
    """
    version = Version(version, VERSION_PATH, VERSION_PATTERN)
    version.write()
    print(version)


@task
def print_version(ctx):
    """Print the current project version."""
    print(Version(path=VERSION_PATH))


@task
def release_notes(ctx, version=None, username=None, password=None, write=False):
    """Generates release notes based on issues in the issue tracker.

    Args:
        version:  Generate release notes for this version. If not given,
                  generated them for the current version.
        username: GitHub username.
        password: GitHub password.
        write:    When set to True, write release notes to a file overwriting
                  possible existing file. Otherwise just print them to the
                  terminal.

    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively. If they aren't
    specified at all, communication with GitHub is anonymous and typically
    pretty slow.
    """
    version = Version(version, VERSION_PATH, VERSION_PATTERN)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    generator = ReleaseNotesGenerator(
        REPOSITORY, RELEASE_NOTES_TITLE, RELEASE_NOTES_INTRO
    )
    generator.generate(version, username, password, file)


@task
def init_labels(ctx, username=None, password=None):
    """Initialize project by setting labels in the issue tracker.

    Args:
        username: GitHub username.
        password: GitHub password.

    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively.

    Should only be executed once when taking ``rellu`` tooling to use or
    when labels it uses have changed.
    """
    initialize_labels(REPOSITORY, username, password)


@task
def lint(ctx):
    """Runs black and flake8 for project Python code."""
    ctx.run("black --config pyproject.toml src/ utest/ atest/")
    ctx.run("flake8 --config .flake8 src/ utest/ atest/")


@task
def gen_stub(ctx):
    """Generate stub/.pyi file for SeleniumLibrary/__init__.py.

    Stub files improves the IDE integration for Python usage.
    """
    ctx.run("python gen_stub.py")


@task
def atest(ctx, suite=None):
    """Runs atest/run.py with headlesschrome.

    Args:
        suite: Select which suite to run.
    """
    commad = "python atest/run.py headlesschrome"
    if suite:
        commad = f"{commad} --suite {suite}"
    ctx.run(commad)
