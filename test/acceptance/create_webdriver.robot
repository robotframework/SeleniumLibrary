*** Setting ***
Documentation     Tests Webdriver
Resource          resource.robot
Library           Collections

*** Test Cases ***
Create Webdriver Creates Functioning WebDriver
    [Documentation]    LOG 2:1 INFO REGEXP: Creating an instance of the \\w+ WebDriver
    ...    LOG 2:4 DEBUG REGEXP: Created \\w+ WebDriver instance with session id (\\w|-)+
    [Tags]  Known Issue Chrome    Known Issue Internet Explorer    Known Issue Safari
    [Setup]    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}    kwargs=${KWARGS}
    Go To    ${FRONT_PAGE}
    Wait Until Page Contains    needle    5s
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
