*** Settings ***
Test Setup        Go To Page "forms/input_special_keys.html"
Resource          ../resource.robot
Library           ../../resources/testlibs/ctrl_or_command.py

*** Variables ***
${CTRL_OR_COMMAND}    ${EMPTY}

*** Test Cases ***
Press Keys Normal Keys
    Press Keys    text_field    AAAAA
    Click Button    OK
    Wait Until Page Contains    AAAAA

Press Keys Normal Keys Many Times
    Press Keys    text_field    AAAAA+BBB
    Click Button    OK
    Wait Until Page Contains    AAAAABBB

Press Keys Sends c++
    Press Keys    text_field    c++
    Click Button    OK
    Wait Until Page Contains    c+

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

Press Keys To Multiple Elements
    [Documentation]    The | Press Keys | OK | ENTER | presses OK button two times, because
    ...    Selenium sets the focus to element by clicking the element.
    Press Keys      text_field    tidii
    Press Keys      OK            ENTER
    Press Keys      None          ENTER    ENTER
    Wait Until Page Contains    tidii     timeout=3
    Page Should Contain Element     //p[text()="tidii"]    limit=4

Press Keys ASCII Code Send As Is
    Press Keys    text_field    \\108    \\13
    Click Button    OK
    Wait Until Page Contains    \\108\\13     timeout=3

Press Keys With Scandic Letters
    Press Keys    text_field    ÖÄÖÄÖ    ÅÖÄP
    Click Button    OK
    Wait Until Page Contains    ÖÄÖÄÖÅÖÄP     timeout=3

Press Keys With Asian Text
    Press Keys    text_field    田中さんにあげ+て下    さい
    Click Button    OK
    Wait Until Page Contains    田中さんにあげて下さい     timeout=3

Press Keys Element Not Found
    Run Keyword And Expect Error
    ...    Element with locator 'not_here' not found.
    ...    Press Keys    not_here    YYYY

Press Keys No keys Argument
    Run Keyword And Expect Error
    ...    "keys" argument can not be empty.
    ...    Press Keys    text_field

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
    Press Keys       None    ${CTRL_OR_COMMAND}+A    ${CTRL_OR_COMMAND}+v
    Click Button     OK
    Wait Until Page Contains    Please input text and click the button. Text will appear in the page.     timeout=3

*** Keywords ***
CTRL Or Command Key
    ${CTRL_OR_COMMAND} =    Ctrl Or Command Key
    Set Suite Variable      ${CTRL_OR_COMMAND}
