*** Settings ***
Library           SeleniumLibrary    event_firing_webdriver=${CURDIR}/../../resources/testlibs/MyListener.py
Resource          resource_event_firing_webdriver.robot
Suite Setup       Open Browser    ${FRONT PAGE}    ${BROWSER}    alias=event_firing_webdriver
...                   remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}
Suite Teardown    Close All Browsers

*** Variables ***
${event_firing_or_none}     ${NONE}

*** Test Cases ***
Open Browser To Start Page
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:12 DEBUG  Wrapping driver to event_firing_webdriver.
    ...    LOG 1:14 INFO  Got driver also from SeleniumLibrary.
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}

Event Firing Webdriver Go To (WebDriver)
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:2 INFO STARTS: Before navigate to
    ...    LOG 1:3 INFO Got driver also from SeleniumLibrary.
    ...    LOG 1:7 INFO STARTS: After navigate to
    Go To     ${ROOT}/forms/named_submit_buttons.html

Event Firing Webdriver Input Text (WebElement)
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:5 INFO  Before clear and send_keys
    ...    LOG 1:9 INFO  After clear and send_keys
    ...    LOG 1:10 INFO  Before clear and send_keys
    ...    LOG 1:14 INFO  After clear and send_keys
    Input Text    //input[@name="textfield"]    FooBar

Event Firing Webdriver With Get WebElement (WebElement)
    [Tags]    NoGrid
    Go To     ${ROOT}/nested_divs.html
    ${link}=        Get WebElement    //a[@id="needleC"]
    Wait Until Element Contains   ${link}   top/c/needle
