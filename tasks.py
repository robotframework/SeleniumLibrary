import os

from invoke import task
from robot.libdoc import libdoc

assert os.getcwd() == os.path.dirname(os.path.abspath(__file__))


@task
def generate_documentation(ctx):
    """Generates the library keyword documentation

    Documentation is generated ny using libdoc
    """
    libdoc(os.path.join(os.path.dirname(__file__), 'src', 'SeleniumLibrary'),
           os.path.join(os.path.dirname(__file__),
                        'docs', 'SeleniumLibrary.html'))
