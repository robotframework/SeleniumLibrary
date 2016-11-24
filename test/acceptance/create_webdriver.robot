*** Setting ***
Documentation     Tests Webdriver
Resource          resource.robot
Library           Collections

*** Test Cases ***
Create Webdriver Creates Functioning WebDriver
    [Documentation]    LOG 2:1 INFO REGEXP: Creating an instance of the \\w+ WebDriver
    ...    LOG 2:4 DEBUG REGEXP: Created \\w+ WebDriver instance with session id (\\w|-)+
    [Setup]    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}    kwargs=${KWARGS}
    Go To    ${FRONT PAGE}
    Page Should Contain    needle
    [Teardown]    Close Browser

Create Webdriver With Bad Driver Name
    [Documentation]    Invalid browser name
    Run Keyword And Expect Error    'Fireox' is not a valid WebDriver name
    ...    Create Webdriver    Fireox

Create Webdriver With Duplicate Arguments
    [Documentation]    Invalid values in arguments
    ${kwargs}=    Create Dictionary    arg=1
    Run Keyword And Expect Error    Got multiple values for argument 'arg'.
    ...    Create Webdriver    Firefox    kwargs=${kwargs}    arg=2

Create Webdriver With Bad Keyword Argument Dictionary
    [Documentation]    Invalid arguments types
    Run Keyword And Expect Error    kwargs must be a dictionary.
    ...    Create Webdriver    Firefox    kwargs={'spam': 'eggs'}

Create Reusable Webdriver with alias
    [Documentation]    Reconnect to an existing browser session
    [Setup]    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}  alias=dummy     kwargs=${KWARGS}
    ${file}=    Save Webdriver
    Restore Webdriver   alias=dummy
    ${file}=    Save Webdriver
    Restore Webdriver   alias=dummy     delete_file=${False}
    Restore Webdriver   alias=dummy
    ${file}=    Save Webdriver          dummy.tmp
    Restore Webdriver   alias=dummy     file=${file}     
    ${file}=    Save Webdriver          ${CURDIR}/dummy.tmp
    Restore Webdriver   alias=dummy     file=${file}     
    ${file}=    Save Webdriver
    Restore Webdriver   alias=dummy2    file=session_dummy.tmp     
    ${sid}  ${url} =    Save Webdriver  ${None}
    Restore Webdriver   alias=dummy     session_id=${sid}  session_url=${url}     
    Go To    ${FRONT PAGE}
    Page Should Contain    needle
    [Teardown]    Close Browser

Create Reusable Webdriver without alias
    [Documentation]    Reconnect to an existing browser session
    [Setup]    Set Driver Variables
    ${i1} =     Create Webdriver    ${DRIVER_NAME}       kwargs=${KWARGS}
    ${file}=    Save Webdriver
    ${i2} =     Restore Webdriver           file=${file}
    log to console    \n${i1}-${i2}
    ${file}=    Save Webdriver
    Restore Webdriver           file=${file}   delete_file=${False}
    Restore Webdriver           file=${file}   delete_file=${False}
    Restore Webdriver           alias=dummy    file=${file}
    ${file}=    Save Webdriver  dummy.tmp
    Restore Webdriver           file=${file}     
    ${file}=    Save Webdriver  ${CURDIR}/dummy.tmp
    Restore Webdriver           file=${file}     
    ${sid}  ${url} =    Save Webdriver  ${None}
    Restore Webdriver   session_id=${sid}  session_url=${url}     
    Go To    ${FRONT PAGE}
    Page Should Contain    needle
    [Teardown]    Close Browser

Create Reusable Webdriver with Invalid Arguments
    [Documentation]    Invalid arguments & run-time errors
    run keyword and expect error  *both alias and file*     Restore Webdriver
    run keyword and expect error  *IOError*No such file*    Restore Webdriver   alias=foo
    run keyword and expect error  *IOError*No such file*    Restore Webdriver   file=foo.tmp

Create Reusable Webdriver with runtime errors
    [Documentation]    run-time errors
    [Setup]    Set Driver Variables
    run keyword and expect error  *No browser is open*      Save Webdriver
    run keyword and expect error  *URLError*refused*        Restore Webdriver   session_id=foo   session_url=http://127.0.0.1:52470/foo
    Create Webdriver    ${DRIVER_NAME}       kwargs=${KWARGS}
    ${sid}  ${url} =    Save Webdriver  ${None}
    run keyword and expect error  **    Restore Webdriver   session_id=bogus  session_url=${url}     
    [Teardown]    Close Browser

*** Keywords ***
Set Driver Variables
    [Documentation]    Selects proper driver
    ${drivers}=    Create Dictionary    ff=Firefox    firefox=Firefox    ie=Ie
    ...    internetexplorer=Ie    googlechrome=Chrome    gc=Chrome
    ...    chrome=Chrome    opera=Opera    phantomjs=PhantomJS    safari=Safari
    ${name}=    Evaluate    "Remote" if "${REMOTE_URL}"!="None" else ${drivers}["${BROWSER.lower().replace(' ', '')}"]
    Set Test Variable    ${DRIVER_NAME}    ${name}
    ${dc names}=    Create Dictionary    ff=FIREFOX    firefox=FIREFOX    ie=INTERNETEXPLORER
    ...    internetexplorer=INTERNETEXPLORER    googlechrome=CHROME    gc=CHROME
    ...    chrome=CHROME    opera=OPERA    phantomjs=PHANTOMJS    htmlunit=HTMLUNIT
    ...    htmlunitwithjs=HTMLUNITWITHJS    android=ANDROID    iphone=IPHONE
    ...    safari=SAFARI
    ${dc name}=    Get From Dictionary    ${dc names}    ${BROWSER.lower().replace(' ', '')}
    ${caps}=    Evaluate    sys.modules['selenium.webdriver'].DesiredCapabilities.${dc name}
    ...    selenium.webdriver,sys
    ${url as str}=    Evaluate    str('${REMOTE_URL}')    # cannot be unicode for versions >= 2.32
    ${kwargs}=    Create Dictionary
    Run Keyword If    "${name}"=="Remote"    Set To Dictionary    ${kwargs}    command_executor
    ...    ${url as str}    desired_capabilities    ${caps}
    Set Test Variable    ${KWARGS}    ${kwargs}
