*** Setting ***
Test Setup        Go To Page "forms/html5_input_types.html"
Resource          ../resource.robot

*** Test Cases ***
Input field type color
    Input Text    id:color     \#72da19
    ${value} =    Get Value    id:color
    Log    ${value}    # Get value does not return the changed value

Input field type date
    [Documentation]    Date and time formats are difficult test because format
    ...    depends on the users machine where the test is run. Therefore only
    ...    checking that value is not empty and it should work in most locales.
    Input Text    id:date         11-22-2019
    ${value} =    Get Value       id:date
    Should Not Be Empty           ${value}

Input field type email
    Input Text    id:email        foo@bar.com
    ${value} =    Get Value       id:email
    Should Be Equal As Strings    ${value}    foo@bar.com

Input field type month
    Input Text    id:month     January2019
    ${value} =    Get Value    id:month
    Log    ${value}    # Get value does not return the value

Input field type number
    Input Text    id:number       42
    ${value} =    Get Value       id:number
    Should Be Equal As Strings    ${value}    42

Input field type range
    Input Text    id:range        72
    ${value} =    Get Value       id:range
    Should Be Equal As Strings    ${value}    50    # Default value does not change when input is range

Input field type search
    Input Text    id:search       tidii
    ${value} =    Get Value       id:search
    Should Be Equal As Strings    ${value}    tidii

Input field type tel
    Input Text    id:tel          123 456 567
    ${value} =    Get Value       id:tel
    Should Be Equal As Strings    ${value}    123 456 567

Input field type time
    [Documentation]    Date and time formats are difficult test because format
    ...    depends on the users machine where the test is run. Therefore only
    ...    checking that value is not empty and it should work in most locales.
    Input Text    id:time      02:34PM
    ${value} =    Get Value    id:time
    Should Not Be Empty        ${value}

Input field type url
    Input Text    id:url          https://github.com/robotframework/SeleniumLibrary
    ${value} =    Get Value       id:url
    Should Be Equal As Strings    ${value}    https://github.com/robotframework/SeleniumLibrary

Input field type week
    Input Text    id:week         452019
    ${value} =    Get Value       id:week
    Should Be Equal As Strings    ${value}    2019-W45
