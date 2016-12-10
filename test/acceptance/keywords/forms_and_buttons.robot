*** Settings ***
Documentation     Tests forms and buttons
Test Setup        Go To Page "forms/named_submit_buttons.html"
Resource          ../resource.robot
Library           OperatingSystem

*** Variables ***
${FORM SUBMITTED}    forms/submit.html

*** Test Cases ***
Submit Form
    [Documentation]    LOG 2 Submitting form 'form_name'.
    Submit Form    form_name
    Verify Location Is "${FORM SUBMITTED}"

Submit Form Without Args
    [Documentation]    Submit Form Without Args
    [Setup]    Go To Page "forms/form_without_name.html"
    Submit Form
    Verify Location Is "target/first.html"

Click Ok Button By Name
    [Documentation]    LOG 2 Clicking button 'ok_button'.
    Click Button    ok_button
    Verify Location Is "${FORM SUBMITTED}"

Click Cancel Button By Name
    [Documentation]    Click Cancel Button By Name
    Click Button    cancel_button
    Value Should Be Cancel

Click Ok Button By Value
    [Documentation]    Click Ok Button By Value
    Click Button    Ok
    Verify Location Is "${FORM SUBMITTED}"

Click Cancel Button By Value
    [Documentation]    Click Cancel Button By Value
    Click Button    Cancel
    Value Should Be Cancel

Click button created with <button> by id
    [Documentation]    Click button created with <button> by id
    [Setup]    Go To Page "forms/buttons.html"
    Click Button    button
    Verify Location Is "${FORM SUBMITTED}"

Click button created with <button> by value attribute
    [Documentation]    Click button created with <button> by value attribute
    [Setup]    Go To Page "forms/buttons.html"
    Click Button    Get In
    Verify Location Is "${FORM SUBMITTED}"

Click button created with <button> by tag content
    [Documentation]    Click button created with <button> by tag content
    [Setup]    Go To Page "forms/buttons.html"
    Click Button    Sisään
    Verify Location Is "${FORM SUBMITTED}"

Choose File
    [Documentation]    Choose File
    [Setup]    Navigate To File Upload Form And Create Temp File To Upload
    [Tags]  Known Issue Internet Explorer    Known Issue Safari
    Choose File    file_to_upload    ${CURDIR}${/}temp.txt
    ${dep_browser}=    Set Variable If
    ...    '${BROWSER}'.lower() == 'ff' or '${BROWSER}'.lower() == 'firefox'
    ...    temp.txt    C:\\fakepath\\temp.txt    #Needs to be checked in Windows and OS X
    Textfield Value Should Be    name= file_to_upload    ${dep_browser}
    [Teardown]    Remove File    ${CURDIR}${/}temp.txt

Click Image With Submit Type Images
    [Documentation]    Click Image With Submit Type Images
    [Setup]    Go To Page "forms/form_with_image_submit.html"
    Click Image    robot.bmp
    Verify Location Is "${FORM SUBMITTED}"

*** Keywords ***
Value Should Be Cancel
    [Documentation]    Value Should Be Cancel
    ${value} =    Get Value    textfield
    Should Be Equal    ${value}    Cancel

Navigate To File Upload Form And Create Temp File To Upload
    [Documentation]    Navigate To File Upload Form And Create Temp File To Upload
    Cannot Be Executed in IE
    Go To Page "forms/file_upload_form.html"
    Touch    ${CURDIR}${/}temp.txt
