*** Setting ***
Test Setup        Go To Page "forms/long_page.html"
Force Tags
Default Tags      keyboard    inprogress
Variables         variables.py
Resource          ../resource.robot

*** Test Cases ***
Press Page-Down
    #Focus    english_input
    Press Keys    english_input    ${NONE}    PAGE_DOWN

Press Home
    #Focus    english_input
    Press Keys    english_input    ${NONE}    HOME

Press End
    #Focus    english_input
    Press Keys    english_input    ${NONE}    END
    Capture Page Screenshot    #We should have scrolled down the page

Press Shift-a
    [Documentation]    This test fails with Opera, because it types "abc" ignoring SHIFT key.
    Press Keys    textarea    a    SHIFT
    Press Keys    textarea    b    SHIFT
    Press Keys    textarea    c    SHIFT
    Sleep    2 seconds
    ${value}=    Get Value    textarea
    Should Be Equal    ${value}    ABC
    #Capture Page Screenshot

Press Shift-def at Once
    Press Keys    textarea    def    SHIFT
    ${value}=    Get Value    textarea
    Should Be Equal    ${value}    DEF
    #Capture Page Screenshot

Press Home, End, Arrows, Backspace and Delete
    Input Text    textarea    ABC
    Press Keys    textarea    ${NONE}    END
    Press Keys    textarea    ${NONE}    LEFT
    Press Keys    textarea    ${NONE}    BACKSPACE
    Press Keys    textarea    ${NONE}    HOME
    Press Keys    textarea    ${NONE}    RIGHT
    Press Keys    textarea    ${NONE}    DELETE
    ${value}=    Get Value    textarea
    Should Be Equal    ${value}    A
    #Capture Page Screenshot

Press Control, Shift, Arrow, Control C, Control V, Control Z
    [Documentation]    Use directional keys to select text, copy and paste. (using double-click to attempt to select element text).
    ...    Strange actions happens with Firefox if we use "block1" instead of "inside_text".
    Double Click Element    inside_text
    Press Keys    inside_text    \\\\CONTROL    SHIFT    RIGHT
    Press Keys    inside_text    \\\\CONTROL    SHIFT    RIGHT
    Press Keys    inside_text    \\\\CONTROL    SHIFT    RIGHT
    Press Keys    inside_text    \\\\CONTROL    SHIFT    RIGHT
    Press Keys    inside_text    C    CONTROL
    Press Keys    textarea    V    CONTROL
    ${value}=    Get Value    textarea
    Double Click Element    english_input
    #This block with Control+Shift+End makes firefox Navigation test fail by not reusing Tabbed windows
    #Control-A shows plugins page
    #Press Keys    english_input    A    CONTROL
    Press Keys    english_input    ${None}    HOME
    Press Keys    english_input    \\\\CONTROL    SHIFT    END
    Press Keys    english_input    C    CONTROL
    Press Keys    textarea    V    CONTROL
    #Press Keys    textarea    Z    CONTROL
    Press Keys    textarea    Text is :
    Press Keys    textarea    ${None}    END
    Press Keys    textarea    V    CONTROL
    ${value2}=    Get Value    textarea
    Log    Value1 is "${value}" Value2 is "${value2}"    INFO
    #Should Be Equal    ${value}    A
    Capture Page Screenshot

Press Invalid Keys
    Run Keyword And Expect Error    *    Press Keys    textarea    ${NONE}
    Run Keyword And Expect Error    *    Press Keys    textarea    a    WORNG_KEY
