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

Click Element Error
    [Documentation]    FAIL Element with locator 'id:äääääää' not found.
    [Setup]    Go To Page "javascript/click.html"
    Click Element    id:äääääää

Click Element Error 2
    [Documentation]    FAIL Element with locator 'id:鱼鱼鱼鱼' not found.
    [Setup]    Go To Page "javascript/click.html"
    Click Element    id:鱼鱼鱼鱼

Click Element Error 3
    [Documentation]    FAIL Element with locator '鱼在天空中飞翔' not found.
    [Setup]    Go To Page "javascript/click.html"
    Click Element    鱼在天空中飞翔

Double Click Element Error
    [Documentation]    FAIL Element with locator 'id:öööö' not found.
    [Setup]    Go To Page "javascript/click.html"
    Double Click Element    id:öööö

Click Element Action Chain
    [Tags]    NoGrid
    [Documentation]
    ...    LOB 1:1 INFO        Clicking 'singleClickButton' using an action chain.
    ...    LOG 2:6 DEBUG GLOB: *actions {"actions": [{*
    Click Element    singleClickButton      action_chain=True
    Element Text Should Be    output    single clicked

*** Keywords ***
Initialize Page
    [Documentation]    Initialize Page
    Reload Page
    Element Text Should Be    output    initial output
