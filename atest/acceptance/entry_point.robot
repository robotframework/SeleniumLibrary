*** Settings ***
Library     Process


*** Test Cases ***
Entry Point Version
    ${process} =    Run Process
    ...    python -m SeleniumLibrary.entry --version
    ...    shell=True
    ...    cwd=${EXECDIR}/src
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Should Be Empty    ${process.stderr}
    Should Contain    ${process.stdout}    Used Python is:
    Should Contain    ${process.stdout}    Installed selenium version is:

Entry Point Translation
    ${process} =    Run Process
    ...    python -m SeleniumLibrary.entry translation ${OUTPUT_DIR}/translation.json
    ...    shell=True
    ...    cwd=${EXECDIR}/src
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Should Be Empty    ${process.stderr}
    Should Be Equal    ${process.stdout}    Translation file created in ${OUTPUT_DIR}/translation.json
    ${process} =    Run Process
    ...    python -m SeleniumLibrary.entry translation --compare ${OUTPUT_DIR}/translation.json
    ...    shell=True
    ...    cwd=${EXECDIR}/src
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    Should Be Empty    ${process.stderr}
    Should Be Equal    ${process.stdout}    Translation is valid, no updated needed.
