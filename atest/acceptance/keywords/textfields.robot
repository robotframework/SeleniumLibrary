*** Setting ***
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
    Input Text        username_field    username
    Input Password    password_field    password
    ${username} =    Get Value          username_field
    ${password} =    Get Value          password_field
    Should Be Equal    ${username}      username
    Should Be Equal    ${password}      password
    Submit Form
    Verify Location Is "forms/submit.html"

Input Password Should Not Log Password String
    [Tags]     NoGrid
    [Setup]    Go To Page "forms/login.html"
    [Documentation]
    ...    LOG 2:1  INFO          Typing password into text field 'password_field'.
    ...    LOG 2:2  DEBUG STARTS: POST http
    ...    LOG 2:3  DEBUG STARTS: http
    ...    LOG 2:4  DEBUG         Finished Request
    ...    LOG 2:5  DEBUG STARTS: POST http
    ...    LOG 2:6  DEBUG STARTS: http
    ...    LOG 2:7  DEBUG         Finished Request
    ...    LOG 2:8  INFO          Temporally setting log level to: NONE
    ...    LOG 2:9  INFO          Log level changed from NONE to DEBUG.
    ...    LOG 2:10 NONE
    ...    LOG 3:1  INFO          Typing text 'username' into text field 'username_field'.
    Input Password    password_field    password
    Input Text        username_field    username

Input Text and Input Password No Clear
    [Setup]    Go To Page "forms/login.html"
    Input Text        username_field    user    clear=False
    Input Password    password_field    pass    False
    Input Text        username_field    name    clear=False
    Input Password    password_field    word    False
    ${username} =    Get Value          username_field
    ${password} =    Get Value          password_field
    Should Be Equal    ${username}      username
    Should Be Equal    ${password}      password

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
