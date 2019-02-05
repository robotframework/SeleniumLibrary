*** Settings ***
Library     SeleniumLibrary    plugins=${CURDIR}/NotHere.py

*** Variables ***
${SERVER}=         localhost:7000
${BROWSER}=        firefox
${REMOTE_URL}=     ${NONE}
${ROOT}=           http://${SERVER}/html
${FRONT_PAGE}=     ${ROOT}/

*** Test Cases ***
Testing Plugin With Arguments
    [Documentation]    When import fails, Open Browser keyword is not found.
    ...    FAIL No keyword with name 'Open Browser' found.
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
