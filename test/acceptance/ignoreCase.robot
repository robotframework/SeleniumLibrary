*** Settings ***
Library           SeleniumLibrary
Test Teardown     Close All Browsers

*** Variables ***
${ISSUE_URL}      https://github.com/robotframework/SeleniumLibrary/issues/849
${TEXT_XPATH}     //*[@id="issuecomment-315181863"]/div[2]/table/tbody/tr/td

*** Test Cases ***
Element Should Contain with ignore_case support
    [Tags]    test
    Open Browser    ${ISSUE_URL}    gc
    Element Should Contain    xpath=${TEXT_XPATH}    From the API point of view
    Run Keyword And Expect Error    *but its text was*    Element Should Contain    xpath=${TEXT_XPATH}    FROM THE API POINT OF VIEW
    Element Should Contain    xpath=${TEXT_XPATH}    FROM THE API POINT OF VIEW    ignore_case=True
    Run Keyword And Expect Error    *but its text was*    Element Should Contain    xpath=${TEXT_XPATH}    from the api point of view
    Element Should Contain    xpath=${TEXT_XPATH}    from the api point of view    ignore_case=True


