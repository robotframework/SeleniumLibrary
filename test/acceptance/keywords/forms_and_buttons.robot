*** Settings ***
<<<<<<< HEAD:test/acceptance/keywords/forms_and_buttons.robot
Test Setup        Go To Page "forms/named_submit_buttons.html"
Resource          ../resource.robot
Library           OperatingSystem
=======
Test Setup       Go To Page "forms/named_submit_buttons.html"
Resource         ../resource.robot
Library          OperatingSystem

>>>>>>> 5f4628bff964187aa6107f4ab9b85a3dc4e73f79:test/acceptance/keywords/forms_and_buttons.robot

*** Variables ***
${FORM SUBMITTED}  forms/submit.html


*** Test Cases ***
Submit Form
    [Documentation]   LOG 2 Submitting form 'form_name'.
    Submit Form   form_name
    Verify Location Is "${FORM SUBMITTED}"

Submit Form Without Args
    [Setup]   Go To Page "forms/form_without_name.html"
    Submit Form
    Verify Location Is "target/first.html"

Click Ok Button By Name
    [Documentation]   LOG 2 Clicking button 'ok_button'.
    Click Button   ok_button
    Verify Location Is "${FORM SUBMITTED}"

Click Cancel Button By Name
    Click Button   cancel_button
    Value Should Be Cancel

Click Ok Button By Value
    Click Button   Ok
    Verify Location Is "${FORM SUBMITTED}"

Click Cancel Button By Value
    Click Button   Cancel
    Value Should Be Cancel

Click button created with <button> by id
    [Setup]   Go To Page "forms/buttons.html"
    Click Button   button
    Verify Location Is "${FORM SUBMITTED}"

Click button created with <button> by value attribute
    [Setup]   Go To Page "forms/buttons.html"
    Click Button   Get In
    Verify Location Is "${FORM SUBMITTED}"

Click button created with <button> by tag content
    [Setup]   Go To Page "forms/buttons.html"
    Click Button   Sisään
    Verify Location Is "${FORM SUBMITTED}"

Choose File
    [Tags]    file
    [Setup]    Navigate To File Upload Form And Create Temp File To Upload
    ${temp_file}=    Set Variable    ${TEMPDIR}${/}temp.txt
    Choose File    file_to_upload    ${temp_file}
    ${dep_browser}=    Set Variable If    '${BROWSER}'.lower() == 'ff' or '${BROWSER}'.lower() == 'firefox'    temp.txt    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    ${temp_file}    C:\\fakepath\\temp.txt
    ...    #Needs to be checked in Windows and OS X
    Textfield Value Should Be    name= file_to_upload    ${dep_browser}    casesense=${False}
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Run Keyword And Expect Error    *    Textfield Value Should Be    name= file_to_upload    ${dep_browser}
    [Teardown]    Remove File    ${TEMPDIR}${/}temp.txt

Click Image With Submit Type Images
    [Setup]   Go To Page "forms/form_with_image_submit.html"
    Click Image   robot.bmp
    Verify Location Is "${FORM SUBMITTED}"


*** Keywords ***
Value Should Be Cancel
    ${value} =   Get Value   textfield
    Should Be Equal   ${value}   Cancel

Navigate To File Upload Form And Create Temp File To Upload
    #Cannot Be Executed in IE
    Touch    ${TEMPDIR}${/}temp.txt
    Go To Page "forms/file_upload_form.html"
