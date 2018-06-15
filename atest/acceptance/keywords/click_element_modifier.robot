*** Settings ***
Suite Setup       Go To Page "javascript/click_modifier.html"
Test Setup        Initialize Page
Resource          ../resource.robot


*** Test Cases ***
Click Element Modifier CTRL
    Click Element    Button    modifier=CTRL
    Element Text Should Be    output    CTRL click

Click Element Modifier ALT
    Click Element    Button    alt
    Element Text Should Be    output    ALT click

Click Element Modifier Shift
    Click Element    Button    Shift
    Element Text Should Be    output    Shift click

Click Element Modifier CTRL+Shift
    Click Element    Button    modifier=CTRL+Shift
    Element Text Should Be    output    CTRL and Shift click

Click Element No Modifier
    Click Element    Button    modifier=False
    Element Text Should Be    output    Normal click

Click Element Wrong Modifier
    Run Keyword And Expect Error
    ...    ValueError: 'FOOBAR' modifier does not match to Selenium Keys
    ...    Click Element    Button    Foobar

*** Keywords ***
Initialize Page
    Reload Page
    Element Text Should Be    output    initial output
