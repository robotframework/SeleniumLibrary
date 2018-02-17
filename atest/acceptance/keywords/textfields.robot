*** Setting ***
Documentation     Test textfields
Test Setup        Go To Page "forms/prefilled_email_form.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Get Value From Text Field
    ${text} =    Get Value    name
    Should Be Equal    ${text}    Prefilled Name
    Clear Element Text    name
    ${text} =    Get Value    name
    Should Be Equal    ${text}    ${EMPTY}

Input Text and Input Password
    [Documentation]
    ...    LOG 2 Typing text 'username' into text field 'username_field'.
    ...    LOG 3 Typing password into text field 'password_field'.
    [Setup]    Go To Page "forms/login.html"
    Input Text    username_field    username
    Input Password    password_field    password
    Submit Form
    Verify Location Is "forms/submit.html"

Input Non-ASCII Text
    [Documentation]
    ...    LOG 2 Typing text 'Yrjö Ärje' into text field 'name'.
    Input Text    name    Yrjö Ärje
    ${text} =    Get Value    name
    Should Be Equal    ${text}    Yrjö Ärje

Press Key
  [Setup]  Go To Page "forms/login.html"
  Cannot Be Executed in IE
  Press Key    username_field    James Bon
  Press Key    username_field    \\100
  Textfield Value Should Be    username_field    James Bond
  Press Key    password_field    f
  Press Key    login_button    \\10
  Verify Location Is "forms/submit.html"

Attempt Clear Element Text On Non-Editable Field
    [Documentation]    Attempt Clear Element Text On Non-Editable Field
    Run Keyword And Expect Error    *    Clear Element Text    can_send_email
