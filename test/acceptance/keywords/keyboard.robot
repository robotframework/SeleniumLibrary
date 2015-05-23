*** Setting ***
Test Setup        Go To Page "forms/long_page.html"
Force Tags
Default Tags      keyboard
Variables         variables.py
Resource          ../resource.robot

*** Test Cases ***
Press Page-Down
    Element Should Be Visible    block2
    Press Keys    block1    ${NONE}    PAGE_DOWN

Press Home
    Press Keys    block1    ${NONE}    HOME

Press End
    Press Keys    block1    ${NONE}    END
    Capture Page Screenshot    #We should have scrolled down the page

Press Shift-a
    Press Keys    textarea    a    SHIFT
    Press Keys    textarea    b    SHIFT
    Press Keys    textarea    c    SHIFT
    Sleep    5 seconds
    ${value}=    Get Value    textarea
    Capture Page Screenshot

Press Invalid Keys
    Run Keyword And Expect Error    *    Press Keys    textarea    ${NONE}
    Run Keyword And Expect Error    *    Press Keys    textarea    a    WORNG_KEY
