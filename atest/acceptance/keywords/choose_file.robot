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

Running Keyword Is Saved Correctly
    ${keyword_method} =     get_running_keyword
    Should Be Equal    get_running_keyword    ${keyword_method}
    ${keyword_method} =     Get Running Keyword
    Should Be Equal    get_running_keyword    ${keyword_method}
    ${keyword_method} =     Get Running Keyword By Decorator
    Should Be Equal    Get Running Keyword By Decorator    ${keyword_method}
    ${keyword_method} =     get_running_keyword_by_decorator
    Should Be Equal    Get Running Keyword By Decorator    ${keyword_method}

Running Keyword Is Cleared Correctly
    ${sl} =    Get Library Instance    SeleniumLibrary
    Should Be Equal    ${sl._running_keyword}    ${None}
    ${keyword_method} =     Get Running Keyword
    Should Be Equal    get_running_keyword    ${keyword_method}
    ${sl} =    Get Library Instance    SeleniumLibrary
    Should Be Equal    ${sl._running_keyword}    ${None}

Running Keyword Is Cleared Correctly When Error
    ${sl} =    Get Library Instance    SeleniumLibrary
    Should Be Equal    ${sl._running_keyword}    ${None}
    Run Keyword And Expect Error    Page should have contained text 'Is not here' but did not.
    ...    Page Should Contain    Is not here
    ${sl} =    Get Library Instance    SeleniumLibrary
    Should Be Equal    ${sl._running_keyword}    ${None}

*** Keywords ***
Navigate To File Upload Form And Create Temp File To Upload
    Cannot Be Executed in IE
    Go To Page "forms/file_upload_form.html"
    Touch    ${CURDIR}${/}temp.txt
