*** Variables ***
${SERVER}=         localhost:7000
${BROWSER}=        firefox
${REMOTE_URL}=     ${NONE}
${ROOT}=           http://${SERVER}/html
${FRONT_PAGE}=     ${ROOT}/

*** Test Cases ***
Testing Plugin With Arguments
    [Documentation]    When finding plugin fails, the SeleniumLibrary import fails and
    ...    therefore Open Browser keyword is not found.
    Run Keyword And Expect Error
    ...    Initializing test library 'SeleniumLibrary' with arguments *
    ...    Import Library
    ...    SeleniumLibrary
    ...    plugins=${CURDIR}/NotHere.py
    Run Keyword And Expect Error
    ...    No keyword with name 'Open Browser' found.
    ...    Open Browser
    ...    ${FRONT PAGE}
    ...    ${BROWSER}
    ...    remote_url=${REMOTE_URL}
