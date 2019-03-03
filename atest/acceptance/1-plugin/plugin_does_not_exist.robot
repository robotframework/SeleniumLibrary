*** Variables ***
${SERVER}=         localhost:7000
${BROWSER}=        firefox
${REMOTE_URL}=     ${NONE}
${ROOT}=           http://${SERVER}/html
${FRONT_PAGE}=     ${ROOT}/

*** Test Cases ***
Importing SeleniumLibrary Should Fail If Plugin Is Not Found
    [Documentation]    When finding plugin fails, the SeleniumLibrary import fails and
    ...    therefore Open Browser keyword is not found.
    ...    FAIL STARTS: Initializing test library 'SeleniumLibrary' with arguments
    Import Library
    ...    SeleniumLibrary
    ...    plugins=${CURDIR}/NotHere.py

SeleniumLibrary Open Browser Keyword Should Not Be Found
    [Documentation]    FAIL No keyword with name 'Open Browser' found.
    Open Browser
    ...    ${FRONT PAGE}
    ...    ${BROWSER}
    ...    remote_url=${REMOTE_URL}
