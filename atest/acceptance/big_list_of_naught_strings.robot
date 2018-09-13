*** Setting ***
Resource          resource.robot
Library           BigListOfNaughtyStrings.BigListOfNaughtyStrings    WITH NAME    blns

*** Test Cases ***
Big List Of Naughty Strings
    [Documentation]    The  Big List of Naughty Strings is originally copied from:
    ...    https://github.com/minimaxir/big-list-of-naughty-strings
    Open Browser To Start Page
    ${blns} =    blns.Get Blns
    :FOR    ${string}    IN    @{blns}
    \    Check Blns Error Check    ${string}


*** Keywords ***
Check Blns Error Check
    [Arguments]    ${string}
    Run Keyword And Expect Error
    ...    Page should have contained element*
    ...    Page Should Contain Element    ${string}
