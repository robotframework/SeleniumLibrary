*** Settings ***
Test Setup        Go To Page "forms/input_special_keys.html"
# Test Teardown     Test CleanUp
Resource          ../resource.robot
Force Tags       tidii

*** Test Cases ***
Press Keys Normal Keys

    Press Keys    text_field    AAAAA
    Click Button    OK
    Wait Until Page Contains    AAAAA

Press Keys Normal Keys Many Times
    Press Keys    text_field    AAAAA+BBB
    Click Button    OK
    Wait Until Page Contains    AAAAABBB

Press Keys Normal Keys Many Arguments
    Press Keys    text_field    ccc    DDDD
    Click Button    OK
    Wait Until Page Contains    cccDDDD

Press Keys Special Keys SHIFT
    Press Keys    text_field    SHIFT+cc
    Click Button    OK
    Wait Until Page Contains    CC

Press Keys Special Keys SHIFT Many Times
    Press Keys    text_field    SHIFT+cc    SHIFT+dd
    Click Button    OK
    Wait Until Page Contains    CCDD     timeout=3


*** Keywords ***
Test CleanUp
    Input Text    text_field    ${EMPTY}
