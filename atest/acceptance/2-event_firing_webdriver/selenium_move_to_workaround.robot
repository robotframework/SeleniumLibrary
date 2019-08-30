*** Settings ***
Documentation    Can be deleted when minimum Selenium version 4.0
Library          SeleniumLibrary     event_firing_webdriver=${CURDIR}/MyListener.py
Resource         resource_event_firing_webdriver.robot
Force Tags       NoGrid
Suite Setup      Open Browser    ${FRONT PAGE}    ${BROWSER}    alias=event_firing_webdriver
...              remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}

*** Test Cases ***
Selenium move_to workaround Click Element At Coordinates
    [Documentation]    LOG 1:5 DEBUG  Workaround for Selenium 3 bug.
    Click Element At Coordinates    id:some_id    4    4

Selenium move_to workaround Scroll Element Into View
    [Documentation]    LOG 1:4 DEBUG  Workaround for Selenium 3 bug.
    Scroll Element Into View    id:some_id

Selenium move_to workaround Mouse Out
    [Documentation]    LOG 1:8 DEBUG  Workaround for Selenium 3 bug.
    Mouse Out    id:some_id

Selenium move_to workaround Mouse Over
    [Documentation]    LOG 1:5 DEBUG  Workaround for Selenium 3 bug.
    Mouse Over    id:some_id
