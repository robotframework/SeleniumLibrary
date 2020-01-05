*** Settings ***
Suite Teardown    Close All Browsers
Library           ../resources/testlibs/get_selenium_options.py
Resource          resource.robot
Documentation     Creating test which would work on all browser is not possible. When testing with other
...    browser than Chrome it is OK that these test will fail. SeleniumLibrary CI is run with Chrome only
...    and therefore there is tests for Chrome only.

*** Test Cases ***
Chrome Browser With Selenium Options As String
    [Documentation]
    ...    LOG 1:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:2 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("--disable-dev-shm-usage")

Chrome Browser With Selenium Options As String With Attirbute As True
    [Documentation]
    ...    LOG 1:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:2 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    ...    LOG 1:2 DEBUG GLOB: *"--headless"*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument ( "--disable-dev-shm-usage" ) ; headless = True

Chrome Browser With Selenium Options With Complex Object
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:2 DEBUG GLOB: *"mobileEmulation": {"deviceName": "Galaxy S5"*
    ...    LOG 1:2 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument ( "--disable-dev-shm-usage" ) ; add_experimental_option( "mobileEmulation" , { 'deviceName' : 'Galaxy S5'})

Chrome Browser With Selenium Options Object
    [Documentation]
    ...    LOG 2:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 2:2 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    ${options} =    Get Chrome Options
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=${options}

Chrome Browser With Selenium Options Invalid Method
    Run Keyword And Expect Error     AttributeError: 'Options' object has no attribute 'not_here_method'
    ...    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=not_here_method("arg1")


Chrome Browser With Selenium Options Argument With Semicolon
    [Documentation]
    ...    LOG 1:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 1:2 DEBUG GLOB: *["has;semicolon"*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("has;semicolon")
