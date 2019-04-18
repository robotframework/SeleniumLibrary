*** Settings ***
Library           SeleniumLibrary    event_firing_webdriver=${CURDIR}/MyListener.py
Suite Teardown    Close All Browsers

*** Variables ***
${URL}        https://github.com/robotframework/SeleniumLibrary
${ISSUES}     ${URL}/issues
${BROWSER}    Chrome

*** Test Cases ***
Open Browser To Start Page
    Open Browser    ${URL}    ${BROWSER}

Event Firing Webdriver Go To (WebDriver)
    Go To     ${ISSUES}

Event Firing Webdriver Click Element (WebElement)
    Click Element    js-issues-search

Event Firing Webdriver Input Text (WebElement)
    Input Text    js-issues-search    FooBar
