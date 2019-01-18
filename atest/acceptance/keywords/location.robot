*** Settings ***
Test Setup        Go To Front Page
Default Tags      assertions
Resource          ../resource.robot

*** Test Cases ***
Location Should Be
    [Documentation]    LOG 2:4 Current location is '${FRONT PAGE}'.
    Location Should Be    ${FRONT PAGE}
    Location Should Be    ${FRONT PAGE}  message=taco
    Location Should Be    ${FRONT PAGE}  message=None
    Run Keyword And Expect Error
    ...    Location should have been 'non existing' but was '${FRONT PAGE}'.
    ...    Location Should Be    non existing
    Run Keyword And Expect Error
    ...    not a url
    ...    Location Should Be    non existing  message=not a url
    Run Keyword And Expect Error
    ...    Location should have been 'non existing' but was 'http://localhost:7000/html/'.
    ...    Location Should Be    non existing  message=None

Location Should Contain
    [Documentation]    LOG 2:4 Current location contains 'html'.
    Location Should Contain    html
    Location Should Contain    html  message=foobar
    Location Should Contain    html  message=None
    Run Keyword And Expect Error
    ...    Location should have contained 'not a location' but it was '${FRONT PAGE}'.
    ...    Location Should Contain    not a location
    Run Keyword And Expect Error
    ...    did not find it
    ...    Location Should Contain    not a location  message=did not find it
    Run Keyword And Expect Error
    ...    Location should have contained 'not a location' but it was 'http://localhost:7000/html/'.
    ...    Location Should Contain    not a location  message=None