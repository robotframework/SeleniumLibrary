*** Settings ***
Test Setup        Go To Page "forms/named_submit_buttons.html"
Resource          ../resource.robot

*** Test Cases ***
Choose File
    [Setup]    Navigate To File Upload Form And Create Temp File To Upload
    Choose File    file_to_upload    ${CURDIR}${/}temp.txt
    # Not sure do you get "C:\fakepath\" prefix with all browsers but at least
    # Chrome and Firefox use it regardless the OS.
    Textfield Value Should Be    file_to_upload    C:\\fakepath\\temp.txt
    [Teardown]    Remove File    ${CURDIR}${/}temp.txt

Choose File And File Does Not Exist
    [Setup]    Go To Page "forms/file_upload_form.html"
    Run Keyword And Expect Error
    ...    InvalidArgumentException: Message:*
    ...    Choose File    file_to_upload    ${CURDIR}${/}NotHere.txt

Choose File And Folder
    [Setup]    Go To Page "forms/file_upload_form.html"
    Choose File    file_to_upload    ${CURDIR}
    Textfield Value Should Be    file_to_upload    C:\\fakepath\\keywords

*** Keywords ***
Navigate To File Upload Form And Create Temp File To Upload
    Cannot Be Executed in IE
    Go To Page "forms/file_upload_form.html"
    Touch    ${CURDIR}${/}temp.txt
