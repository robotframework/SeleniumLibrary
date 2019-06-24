*** Settings ***
Library           SeleniumLibrary    event_firing_webdriver=${CURDIR}/MyListener.py
Suite Setup       Open Browser    ${FRONT PAGE}    ${BROWSER}    alias=event_firing_webdriver
...                   remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}
Suite Teardown    Close All Browsers

*** Variable ***
${SERVER}=                  localhost:7000
${BROWSER}=                 Chrome
${REMOTE_URL}=              ${NONE}
${DESIRED_CAPABILITIES}=    ${NONE}
${ROOT}=                    http://${SERVER}/html
${FRONT_PAGE}=              ${ROOT}/

*** Test Cases ***
Open Browser To Start Page
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:12 DEBUG  Wrapping driver to event_firing_webdriver.
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}

Event Firing Webdriver Go To (WebDriver)
    [Documentation]
    ...    STARTS 1:2 Before navigate to
    ...    STARTS 1:6 After navigate to
    Go To     ${ROOT}/forms/named_submit_buttons.html

Event Firing Webdriver Input Text (WebElement)
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:5 INFO  Before clear and send_keys
    ...    LOG 1:9 INFO  After clear and send_keys
    ...    LOG 1:10 INFO  Before clear and send_keys
    ...    LOG 1:14 INFO  After clear and send_keys
    Input Text    //input[@name="textfield"]    FooBar

Event Firing Webdriver Click Element (WebElement)
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:5 INFO  Before click
    ...    LOG 1:9 INFO  After click
    Click Element    //input[@name="ok_button"]
