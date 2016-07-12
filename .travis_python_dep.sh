#!/bin/bash
set -ev
PYTHON_VERSION=`python -c "import sys; print(sys.version[:3])"`
if [ "${PYTHON_VERSION}" = "2.6" ]; then
    pip install robotframework==2.9.2
    pip install selenium
    pip install decorator
    pip install docutils
    # pip install future
    # pip install mockito
elif [ "${PYTHON_VERSION}" = "2.7" ]; then
    pip install robotframework
    pip install selenium
    pip install decorator
    pip install docutils
    # pip install future
    # pip install mockito
elif [ "${PYTHON_VERSION}" = "3.4" ]; then
    pip install robotframework==3.0b1
    pip install selenium
    pip install decorator
    pip install docutils
    pip install future
fi
