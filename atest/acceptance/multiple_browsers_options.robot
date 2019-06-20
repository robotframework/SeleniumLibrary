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
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument:--disable-dev-shm-usage

Chrome Browser With Selenium Options List
    [Documentation]
    ...    LOG 4:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 4:2 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    ${argument} =        Create List    --disable-dev-shm-usage
    ${add_argument} =    Create Dictionary    add_argument    ${argument}
    ${options} =         Create List    ${add_argument}
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=${options}

Chrome Browser With Selenium Options Object
    [Documentation]
    ...    LOG 2:2 DEBUG GLOB: *"goog:chromeOptions"*
    ...    LOG 2:2 DEBUG GLOB: *args": ["--disable-dev-shm-usage"?*
    ${options} =    Get Chrome Options
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=${options}


Chrome Browser With Selenium Options Invalid Argument
    Run Keyword And Expect Error     AttributeError: 'Options' object has no attribute 'not_here_method'
    ...    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=not_here_method:arg1:arg2
