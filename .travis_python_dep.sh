#!/bin/bash
set -ev
PYTHON_VERSION=`python -c "import sys; print(sys.version[:3])"`
if [ "${PYTHON_VERSION}" = "2.7" ]; then
    pip install robotframework
    pip install selenium
    pip install decorator
    pip install docutils
    pip install future
    pip install mockito
elif [ "${PYTHON_VERSION}" = "3.4" -o "${PYTHON_VERSION}" = "3.5" ]; then
    pip install robotframework
    pip install selenium
    pip install decorator
    pip install docutils
    pip install future
fi
