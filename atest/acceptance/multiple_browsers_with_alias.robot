*** Settings ***
Documentation     Several instances of browser with same alias
Suite Teardown    Close All Browsers
Resource          resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Multiple Browsers With Same Alias Should Not Open Browser
    [Documentation]       Tests Open Browser keyword to open with existing alias
    [Tags]                alias
    ${browser_1_index}=   Open Browser    ${FRONT PAGE}  ${BROWSER}   index_1
    Location Should Be    ${FRONT PAGE}
    ${browser_2_index}=   Open Browser    ${FRONT PAGE}  ${BROWSER}   index_2
    Should Not Be Equal   ${browser_1_index}    ${browser_2_index}    Second browser should be different than first
    Location Should Be    ${FRONT PAGE}
    ${browser_3_index}=   Open Browser    ${ROOT}/links.html  ${BROWSER}   index_2
    Should Be Equal       ${browser_2_index}    ${browser_3_index}    Third browser should be same as second.
    Location Should Be    ${ROOT}/links.html
    Switch Browser        ${browser_2_index}
    Location Should Be    ${ROOT}/links.html
    Close Browser
    Switch Browser        ${browser_1_index}
    Location Should Be    ${FRONT PAGE}
    Close Browser
