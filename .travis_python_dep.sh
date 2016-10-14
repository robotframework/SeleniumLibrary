#!/bin/bash
set -ev
PYTHON_VERSION=`python -c "import sys; print(sys.version[:3])"`
if [ "${PYTHON_VERSION}" = "2.6" ]; then
    pip install robotframework
    pip install selenium==2.53.6
    pip install decorator
    pip install docutils
    pip install future
    pip install mockito
elif [ "${PYTHON_VERSION}" = "2.7" ]; then
    pip install robotframework
    pip install selenium==2.53.6
    pip install decorator
    pip install docutils
    pip install future
    pip install mockito
elif [ "${PYTHON_VERSION}" = "3.4" ]; then
    pip install robotframework
    pip install selenium==2.53.6
    pip install decorator
    pip install docutils
    pip install future
fi
