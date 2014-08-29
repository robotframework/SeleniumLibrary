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
    Capture Page Screenshot

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
    Capture Page Screenshot

Press Invalid Keys
    Run Keyword And Expect Error    *    Press Keys    textarea    ${NONE}
    Run Keyword And Expect Error    *    Press Keys    textarea    a    WORNG_KEY
