*** Settings ***
Resource        resource.robot
Suite Teardown  Close All Browsers

*** Test Cases ***
Browser Should Open And Close
	Open Browser To Start Page Without Testing Default Options
	Close Browser

Browser Open With Implicit Wait Should Not Override Default
    Open Browser To Start Page And Test Implicit Wait   10
    Close Browser
    

There Should Be A Good Error Message If Browser Is Not Opened
    Run Keyword And Expect Error  No browser is open  Title Should Be  foo

Close Browser Does Nothing When No Browser Is Opened
    Close Browser

Browser Open With Not Well-Formed URL Should Close
   [Documentation]  Verify after incomplete 'Open Browser' browser closes
   ...  LOG 1.1:10   DEBUG STARTS: Opened browser with session id
   ...  LOG 1.1:10   DEBUG REGEXP: .*but failed to open url.*
   ...  LOG 2:2      DEBUG STARTS: DELETE
   ...  LOG 2:3      DEBUG Finished Request
   
   Run Keyword And Expect Error  *
   ...  Open Browser  bad.url.bad  ${BROWSER}
   Close All Browsers
