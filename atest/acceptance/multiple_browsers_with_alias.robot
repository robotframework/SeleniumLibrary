*** Settings ***
Suite Teardown    Close All Browsers
Resource          resource.robot

*** Test Cases ***
Open First Browser
    [Documentation]
    ...    LOG 1:1 INFO STARTS: Opening browser '
    ${BROWSER_1_INDEX} =   Open Browser    ${FRONT PAGE}  ${BROWSER}   index_1
    Should Be Equal As Numbers       ${BROWSER_1_INDEX}    1
    Location Should Be    ${FRONT PAGE}
    [Teardown]    Set Suite Variable    ${BROWSER_1_INDEX}

Different Alias Should Open New Browser
    ${BROWSER_2_INDEX} =   Open Browser    ${FRONT PAGE}  ${BROWSER}   index_2
    Should Be Equal As Numbers       ${BROWSER_2_INDEX}    2
    Location Should Be    ${FRONT PAGE}
    [Teardown]    Set Suite Variable    ${BROWSER_2_INDEX}

Same Alias Should Not Open New Browser Same Browser
    [Documentation]
    ...    LOG 1:1 INFO Using existing browser from index 2.
    ...    LOG 1:2 DEBUG STARTS: Switched to browser with Selenium session id
    ...    LOG 1:3 INFO STARTS:  Opening url 'http://
    ${browser_3_index} =   Open Browser    ${ROOT}/links.html  ${BROWSER}   index_2
    Should Be Equal       ${BROWSER_2_INDEX}    ${browser_3_index}
    Location Should Be    ${ROOT}/links.html

Same Alias Should Not Open New Browser Previsous Browser
    [Documentation]
    ...    LOG 1:1 INFO Using existing browser from index 1.
    ...    LOG 1:2 DEBUG STARTS: Switched to browser with Selenium session id
    ...    LOG 1:3 INFO STARTS:  Opening url 'http://
    ${browser_4_index} =   Open Browser    ${ROOT}/links.html  ${BROWSER}   index_1
    Should Be Equal       ${BROWSER_1_INDEX}    ${browser_4_index}
    Location Should Be    ${ROOT}/links.html

Close Browser And Reusing Alias Should Open New Browser
    [Documentation]
    ...    LOG 3:1 INFO STARTS: Opening browser '
    Switch Browser     index_1
    Close Browser
    ${browser_5_index} =   Open Browser    ${FRONT PAGE}  ${BROWSER}   index_1
    Should Be Equal As Numbers       ${browser_5_index}    3
    Location Should Be    ${FRONT PAGE}

Reusing Reused Alias Should Not Open New Browser
    [Documentation]
    ...    LOG 1:1 INFO Using existing browser from index 3.
    ${browser_6_index} =   Open Browser    ${ROOT}/links.html  ${BROWSER}   index_1
    Should Be Equal As Numbers       ${browser_6_index}    3
    Location Should Be    ${ROOT}/links.html
