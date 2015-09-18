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

Get Browser Capabilities Using Dictionary
    [Documentation]    Gets current browser capabilities from WebDriver
    [Setup]    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}
    Go To    ${FRONT PAGE}    # If we don't do this then no version details
    ${capabilities}=    Get Browser Capabilities
    Log    Capabilities = ${capabilities}
    Log    Browser is ${capabilities['browserName']}, version ${capabilities['version']}
    ${browser}=    Normalize Browser Name
    Should Match    ${capabilities['browserName']}    ${browser}
    Run Keyword If    "${browser}" != "internet explorer"    Log    Rotatable = ${capabilities['rotatable']}
    # Disabled next step to PASS in RF pre 2.9
    # Run Keyword If    "${browser}" == "internet explorer"    Run Keyword And Expect Error    *    Log
    #     ...    Rotatable = ${capabilities['rotatable']}
    Log    Platform = ${capabilities['platform']}
    [Teardown]    Close Browser

Get Browser Capabilities Using Attributes
    [Documentation]    Gets current browser capabilities from WebDriver
    [Setup]    Run Keywords    Cannot Run In RF Pre 2.9    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}
    Go To    ${FRONT PAGE}    # If we don't do this then no version details
    &{capabilities}=    Get Browser Capabilities
    Log    Capabilities = &{capabilities}
    Log    Browser is ${capabilities.browserName}, version ${capabilities.version}
    ${browser}=    Normalize Browser Name
    Should Match    ${capabilities.browserName}    ${browser}
    Run Keyword If    "${browser}" != "internet explorer"    Log    Rotatable = ${capabilities.rotatable}
    Run Keyword If    "${browser}" == "internet explorer"    Run Keyword And Expect Error    *    Log
        ...    Rotatable = ${capabilities.rotatable}
    Log    Platform = ${capabilities.platform}
    Log    Wearable = ${capabilities.get('wearable', 'What were you expecting? To wear a browser?')}
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

Cannot Run In RF Pre 2.9
    [Documentation]    Skips the test if running in Robot Framework previous to 2.9.
    Import Library    robot.version    WITH NAME    Version
    ${VERSION}=    Version.Get Version
    Run Keyword If    '${VERSION}' < '2.9.0'    Fail And Set Non-Critical
    ...    This test does not work with Robot Framework ${VERSION}. Please use version 2.9 or newer.

Normalize Browser Name
    [Documentation]    Returns a normalized name for ${DRIVER_NAME} especially for IE
    ${BROWSER}=    Set Variable    ${DRIVER_NAME.lower()}
    ${ret}=    Set Variable If    "${BROWSER}" == "ie"    internet explorer    ${BROWSER}
    [Return]    ${ret}
