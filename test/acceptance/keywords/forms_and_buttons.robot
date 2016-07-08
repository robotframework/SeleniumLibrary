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
    Choose File    file_to_upload    ${CURDIR}${/}temp.txt
    ${dep_browser}=    Set Variable If
    ...    '${BROWSER}'.lower() == 'ff' or '${BROWSER}'.lower() == 'firefox'
    ...    temp.txt    C:\\fakepath\\temp.txt    #Needs to be checked in Windows and OS X
    Textfield Value Should Be    name= file_to_upload    ${dep_browser}
    [Teardown]    Remove File    ${CURDIR}${/}temp.txt

Choose Multiple Files
    [Documentation]    Choose Multiple Files
    [Setup]    Navigate To Multiple File Upload Form And Create 2 Temp Files To Upload
    Choose Multiple Files    id=files_list    ${BROWSER}    ${CURDIR}    temp_1.txt    temp_2.txt
    Click Button  id=check_content
    Check that input element contains the 2 files
    [Teardown]    Remove All Files Generated for Multiple Upload

Click Image With Submit Type ImagesV
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

Navigate To Multiple File Upload Form And Create 2 Temp Files To Upload
    [Documentation]    Navigate To Multiple File Upload Form And Create Necessary files to upload
    Cannot Be Executed in IE
    Go To Page "forms/multiple_file_upload_form.html"
    Touch    ${CURDIR}${/}temp_1.txt
    Touch    ${CURDIR}${/}temp_2.txt

Remove All Files Generated for Multiple Upload
    Remove File    ${CURDIR}${/}temp_1.txt
    Remove File    ${CURDIR}${/}temp_2.txt

Check that input element contains the 2 files
    ${file_listed}    Execute Javascript    return document.getElementById("result").querySelectorAll("li").length
    Should Be Equal As Numbers    ${file_listed}    2
    Page Should Contain    temp_1.txt
    Page Should Contain    temp_2.txt

