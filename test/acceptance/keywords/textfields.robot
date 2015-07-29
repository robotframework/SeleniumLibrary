*** Setting ***
Test Setup        Go To Page "forms/prefilled_email_form.html"
Variables         variables.py
Resource          ../resource.robot

*** Test Cases ***
Get Value From Text Field
    ${text} =    Get Value    name
    Should Be Equal    ${text}    Prefilled Name
    Clear Element Text    name
    ${text} =    Get Value    name
    Should Be Equal    ${text}    ${EMPTY}


Input Unicode In Text Field
    Input Text    name    ${unic_text}
    ${text} =    Get Value    name
    Should Be Equal    ${text}    ${unic_text}

Input Password
    [Documentation]    LOG 3 Typing password into text field 'password_field'
    [Setup]    Go To Page "forms/login.html"
    Input Text    username_field    username
    Input Password    password_field    password
    Submit Form
    Verify Location Is "forms/submit.html"

Press Key
    [Setup]    Go To Page "forms/login.html"
    #Cannot Be Executed in IE
    Input Text    username_field    James Bond
    Press Key    username_field    HOME
    Press Key    username_field    END
    Press Key    username_field    ARROW_LEFT
    Press Key    username_field    ARROW_LEFT
    Press Key    username_field    ARROW_LEFT
    Press Key    username_field    DELETE
    Press Key    username_field    ARROW_LEFT
    Press Key    username_field    ARROW_RIGHT
    Press Key    username_field    \\108    #This is the 'l' char
    Press Key    username_field    o
    ${text} =    Get Value    username_field
    Should Be Equal    ${text}    James Blond
    Press Key    password_field    f
    Press Key    password_field    9
    Press Key    login_button    ENTER
    Verify Location Is "forms/submit.html"

Attempt Clear Element Text On Non-Editable Field
    Run Keyword And Expect Error    *    Clear Element Text    can_send_email
