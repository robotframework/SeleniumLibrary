*** Settings ***
Suite Teardown    Close All Browsers
Library           ../resources/testlibs/get_selenium_options.py
Resource          resource.robot
Force Tags        Known Issue Firefox    Known Issue Safari    Known Issue Internet Explorer
Documentation     Creating test which would work on all browser is not possible.
...    These tests are for Chrome only.

*** Test Cases ***
Chrome Browser With Selenium Options As String
    [Documentation]
    ...    LOG 1:14 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:14 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("--disable-dev-shm-usage")
 
Chrome Browser With Selenium Options As String With Attribute As True
    [Documentation]
    ...    LOG 1:14 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:14 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    ...    LOG 1:14 DEBUG GLOB: *"--headless=new"*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument ( "--disable-dev-shm-usage" ) ; add_argument ( "--headless=new" )
 
Chrome Browser With Selenium Options With Complex Object
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:14 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:14 DEBUG GLOB: *"mobileEmulation": {"deviceName": "Galaxy S5"*
    ...    LOG 1:14 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument ( "--disable-dev-shm-usage" ) ; add_experimental_option( "mobileEmulation" , { 'deviceName' : 'Galaxy S5'})
 
Chrome Browser With Selenium Options Object
    [Documentation]
    ...    LOG 2:14 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 2:14 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    ${options} =    Get Chrome Options
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=${options}
 
Chrome Browser With Selenium Options Invalid Method
    Run Keyword And Expect Error     AttributeError: 'Options' object has no attribute 'not_here_method'
    ...    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=not_here_method("arg1")


Chrome Browser With Selenium Options Argument With Semicolon
    [Documentation]
    ...    LOG 1:14 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:14 DEBUG GLOB: *["has;semicolon"*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("has;semicolon")

Chrome Browser with Selenium Options Ending With Semicolon
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("--disable-dev-shm-usage") ;

Chrome Browser with Selenium Options Ending With A Few Semicolons
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("--disable-dev-shm-usage") ; ; ;

Chrome Browser with Selenium Options Containing Empty Option
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument ( "--disable-dev-shm-usage" ) ; ; add_argument ( "--headless=new" )

Chrome Browser with Selenium Options With A Missing Semicolon
    Run Keyword And Expect Error    ValueError: Unable to parse option: "add_argument ( "--disable-dev-shm-usage" ) add_argument ( "--headless=new" )"
    ...    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument ( "--disable-dev-shm-usage" ) add_argument ( "--headless=new" )
