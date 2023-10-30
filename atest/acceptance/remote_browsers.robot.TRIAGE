*** Settings ***
Library  SeleniumLibrary
Library    Process

*** Variables ***
${URL}            https://robotframework.org/
${REMOTE_BETA}    http://localhost:7272

*** Test Cases ***
Open Chrome with Remote Webdriver without Options
    # [Setup]   StartDriver  chromedriver
    Open Browser
    ...    url=${URL}
    ...    browser=chrome
    ...    remote_url=${REMOTE_BETA}
    # [Teardown]    Stop Driver

Open Edge with Remote Webdriver without Options
    # [Setup]   StartDriver  msedgedriver
    Open Browser
    ...    url=${URL}
    ...    browser=edge
    ...    remote_url=${REMOTE_BETA}
    # [Teardown]    Stop Driver

*** Keywords ***
Start Driver
    [Arguments]  ${driver_cmd}
    Start Process    ${driver_cmd}    --port:7272
    ${result}=  Wait For Process  timeout=30secs
    Process Should Be Running   error_message=Unable to start driver with command ${driver_cmd}

Stop Driver
    Terminate Process