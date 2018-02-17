*** Settings ***
Documentation     Tests clicking element
Suite Setup       Go To Page "javascript/click.html"
Test Setup        Initialize Page
Resource          ../resource.robot

*** Test Cases ***
Click Element
    [Documentation]    LOG 2 Clicking element 'singleClickButton'.
    Click Element    singleClickButton
    Element Text Should Be    output    single clicked

Double Click Element
    [Documentation]    LOG 2 Double clicking element 'doubleClickButton'.
    [Tags]    Known Issue Safari    Known Issue Firefox
    Double Click Element    doubleClickButton
    Element Text Should Be    output    double clicked

*** Keywords ***
Initialize Page
    [Documentation]    Initialize Page
    Reload Page
    Element Text Should Be    output    initial output
