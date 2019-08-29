*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/OpenBrowserExample.py

*** Variables ***
${SERVER}=         localhost:7000
${ROOT}=           http://${SERVER}/html
&{EXTRA DICTIONARY}    extra=dictionary    key=value


*** Test Cases ***
Open Browser Coplex Example
    [Documentation]
    ...    LOG 1:2 INFO GLOB: *'key': *'value'*
    ...    LOG 1:2 INFO GLOB: *'extra': *'dictionary'*
    Open Browser    ${ROOT}/forms/prefilled_email_form.html    seleniumwire    extra_dictionary=${EXTRA DICTIONARY}
    [Teardown]    Close All Browsers
