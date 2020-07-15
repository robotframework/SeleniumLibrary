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

Choose File With Grid
    [Documentation]
    ...    LOG 2:6 DEBUG GLOB:    POST*/session/*/file*"file": "*
    [Tags]    OnlyGrid
    [Setup]    Touch    ${CURDIR}${/}temp2.txt
    Choose File    file_to_upload    ${CURDIR}${/}temp2.txt
    Textfield Value Should Be    file_to_upload    C:\\fakepath\\temp2.txt
    [Teardown]    Remove File    ${CURDIR}${/}temp2.txt

Choose File With Grid From Library Using SL choose_file method
    [Documentation]
    ...    LOG 4:6 DEBUG GLOB:    POST*/session/*/file*"file": "*
    [Tags]    OnlyGrid
    [Setup]    Go To Page "forms/file_upload_form.html"
    Touch    ${CURDIR}${/}temp42.txt
    Import Library    ${CURDIR}/../../resources/testlibs/ChooseFileLib.py
    ChooseFileLib.my_choose_file    file_to_upload    ${CURDIR}${/}temp42.txt
    Textfield Value Should Be    file_to_upload    C:\\fakepath\\temp42.txt
    [Teardown]    Remove File    ${CURDIR}${/}temp42.txt

Input Text Should Work Same Way When Not Using Grid
    [Documentation]
    ...    LOG 2:5 DEBUG GLOB:    POST*/session/*/clear {"*
    ...    LOG 2:7 DEBUG          Finished Request
    ...    LOG 2:8 DEBUG GLOB:    POST*/session/*/value*"text": "*
    ...    LOG 2:10 DEBUG         Finished Request
    ...    LOG 2:11 DEBUG         NONE
    [Tags]    NoGrid
    [Setup]    Touch    ${CURDIR}${/}temp.txt
    Input Text    file_to_upload    ${CURDIR}${/}temp.txt
    Textfield Value Should Be    file_to_upload    C:\\fakepath\\temp.txt
    [Teardown]    Remove File    ${CURDIR}${/}temp.txt

Input Text Should Work Same Way When Using Grid
    [Tags]    OnlyGrid
    [Setup]    Touch    ${CURDIR}${/}temp3.txt
    Input Text    file_to_upload    ${CURDIR}${/}temp3.txt
    Textfield Value Should Be    file_to_upload    C:\\fakepath\\temp3.txt
    [Teardown]    Remove File    ${CURDIR}${/}temp3.txt

*** Keywords ***
Navigate To File Upload Form And Create Temp File To Upload
    Cannot Be Executed in IE
    Go To Page "forms/file_upload_form.html"
    Touch    ${CURDIR}${/}temp.txt
