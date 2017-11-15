*** Setting ***
Documentation     Tests Get Browser Capabilities
Resource          ../resource.robot
Library           Collections

*** Test Cases ***
Get Browser Capabilities Using Dictionary
    [Setup]    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}
    ${capabilities}=    Get Browser Capabilities
    Log    Capabilities = ${capabilities}
    [Teardown]    Close Browser

Test Capabilities Browser Name, Platform and Version
    [Documentation]    Using Open Browser
    [Setup]    Set Driver Variables
    Open Browser    about:blank    ${DRIVER_NAME}
    ${capabilities}=    Get Browser Capabilities
    ${browser}=    Normalize Browser Name
    Should Match    ${capabilities['browserName']}    ${browser}
    ${status}    ${platform}=    Run Keyword And Ignore Error    Set Variable    ${capabilities['platform']}
    Run Keyword If    "${status}" == "PASS"    Log    Platform = ${platform}
    ...    ELSE    Log    Platform = ${capabilities['platformName']}
    ${status}    ${version}=    Run Keyword And Ignore Error    Set Variable    ${capabilities['version']}
    Run Keyword If    "${status}" == "PASS"    Log    Browser Version = ${version}
    ...    ELSE    Log    Browser Version = ${capabilities['browserVersion']}
    [Teardown]    Close Browser

Get Browser Capabilities Using Attributes
    [Documentation]    Using Open Browser
    [Tags]    not_on_rf_2.8.7
    [Setup]    Set Driver Variables
    Open Browser    about:blank    ${DRIVER_NAME}
    &{capabilities}=    Get Browser Capabilities
    Log    Capabilities = &{capabilities}
    [Teardown]    Close Browser

Test Capabilities Browser Name, Platform and Version Using Attributes
    [Tags]    not_on_rf_2.8.7
    [Setup]    Set Driver Variables
    Create Webdriver    ${DRIVER_NAME}
    &{capabilities}=    Get Browser Capabilities
    ${browser}=    Normalize Browser Name
    Should Match    ${capabilities.browserName}    ${browser}
    ${status}    ${platform}=    Run Keyword And Ignore Error    Set Variable    ${capabilities.platform}
    Run Keyword If    "${status}" == "PASS"    Log    Platform = ${platform}
    ...    ELSE    Log    Platform = ${capabilities.platformName}
    ${status}    ${version}=    Run Keyword And Ignore Error    Set Variable    ${capabilities.version}
    Run Keyword If    "${status}" == "PASS"    Log    Browser Version = ${version}
    ...    ELSE    Log    Browser Version = ${capabilities.browserVersion}
    Log    Wearable = ${capabilities.get('wearable', 'What were you expecting? To wear a browser?')}
    # [Teardown]    Close Browser

*** Keywords ***
Set Driver Variables
    [Documentation]    Selects proper driver
    ${drivers}=    Create Dictionary    ff=Firefox    firefox=Firefox    ie=Ie    internetexplorer=Ie    googlechrome=Chrome
    ...    gc=Chrome    chrome=Chrome    opera=Opera    phantomjs=PhantomJS    safari=Safari
    ${name}=    Evaluate    "Remote" if "${REMOTE_URL}"!="None" else ${drivers}["${BROWSER.lower().replace(' ', '')}"]
    Set Test Variable    ${DRIVER_NAME}    ${name}
    ${dc names}=    Create Dictionary    ff=FIREFOX    firefox=FIREFOX    ie=INTERNETEXPLORER    internetexplorer=INTERNETEXPLORER    googlechrome=CHROME
    ...    gc=CHROME    chrome=CHROME    opera=OPERA    phantomjs=PHANTOMJS    htmlunit=HTMLUNIT    htmlunitwithjs=HTMLUNITWITHJS
    ...    android=ANDROID    iphone=IPHONE    safari=SAFARI
    ${dc name}=    Get From Dictionary    ${dc names}    ${BROWSER.lower().replace(' ', '')}
    ${caps}=    Evaluate    sys.modules['selenium.webdriver'].DesiredCapabilities.${dc name}    selenium.webdriver,sys
    ${url as str}=    Evaluate    str('${REMOTE_URL}')    # cannot be unicode for versions >= 2.32
    ${kwargs}=    Create Dictionary
    Run Keyword If    "${name}"=="Remote"    Set To Dictionary    ${kwargs}    command_executor    ${url as str}    desired_capabilities
    ...    ${caps}
    Set Test Variable    ${KWARGS}    ${kwargs}

Normalize Browser Name
    [Documentation]    Returns a normalized name for ${DRIVER_NAME} especially for IE
    ${BROWSER}=    Set Variable    ${DRIVER_NAME.lower()}
    ${ret}=    Set Variable If    "${BROWSER}" == "ie"    internet explorer    ${BROWSER}
    [Return]    ${ret}
