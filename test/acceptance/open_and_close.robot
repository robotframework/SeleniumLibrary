*** Settings ***
Suite Teardown    Close All Browsers
Force Tags        openclose
Resource          resource.robot

*** Test Cases ***
Browser Should Open And Close
    Open Browser To Start Page Without Testing Default Options
    Close Browser

Browser Open With Implicit Wait Should Not Override Default
    Open Browser To Start Page And Test Implicit Wait    10
    Close Browser

There Should Be A Good Error Message If Browser Is Not Opened
    Run Keyword And Expect Error    No browser is open    Title Should Be    foo

Close Browser Does Nothing When No Browser Is Opened
    Close Browser

Browser Open With Not Well-Formed URL Should Close
    [Documentation]    Verify after incomplete 'Open Browser' browser closes
    ...    LOG 1.1:1 REGEXP: Opening browser '\\w+' to base url 'bad.url.bad'
    #If in DEBUG test log with: \\nLOG 1.1 DEBUG STARTS: Opened browser with session id\\nLOG 1.1 DEBUG REGEXP: .*but failed to open url.*\\nLOG 2:1 DEBUG STARTS: DELETE\\nLOG 2:2 DEBUG Finished Request
    Run Keyword And Expect Error    *    Open Browser    bad.url.bad    ${BROWSER}
    Close All Browsers
