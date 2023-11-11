*** Settings ***
Test Setup        Go To Page "javascript/dynamic_content.html"
Resource          ../resource.robot

*** Test Cases ***
Wait For Expected Conditions One Argument
    Title Should Be    Original
    Click Element    link=delayed change title
    Wait For Expected Condition    title_is    Delayed
    Title Should Be    Delayed
    
