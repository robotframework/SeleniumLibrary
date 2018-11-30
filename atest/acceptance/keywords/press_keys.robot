*** Settings ***
Test Setup        Go To Page "forms/input_special_keys.html"
Resource          ../resource.robot

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

Press Keys Normal Keys Many Times With Many Args
    Press Keys    text_field    a+b    C+D
    Click Button    OK
    Wait Until Page Contains    abCD

Press Keys Special Keys SHIFT
    Press Keys    text_field    SHIFT+cc
    Click Button    OK
    Wait Until Page Contains    CC

Press Keys Special Keys SHIFT Many Times
    Press Keys    text_field    SHIFT+cc    SHIFT+dd
    Click Button    OK
    Wait Until Page Contains    CCDD     timeout=3

Press Keys Element Not Found
    run keyword and expect error
    ...    Element with locator 'not_here' not found.
    ...    Press Keys    not_here    YYYY

Press Keys Without Element
    Click Element    text_field
    Press Keys       None    tidii
    Click Button     OK
    Wait Until Page Contains    tidii     timeout=3

Press Keys Multiple Times Without Element
    Click Element    text_field
    Press Keys       None    foo+bar    e+n+d
    Click Button     OK
    Wait Until Page Contains    foobarend     timeout=3

Press Keys Without Element Special Keys
    Click Element    text_field
    Press Keys       None    CTRL+A    CTRL+v
    Click Button     OK
    Wait Until Page Contains    Please input text and click the button. Text will appear in the page.     timeout=3
