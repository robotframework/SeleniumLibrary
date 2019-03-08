*** Settings ***
Library           SeleniumLibrary    event_firing_webdriver=${CURDIR}/MyListener.py
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
    [Documentation]
    ...    REGEXP:  .*Wrapping driver to event_firing_webdriver\..*
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}

Event Firing Webdriver Go To (WebDriver)
    [Documentation]
    ...    STARTS 1:2 Before navigate to
    ...    STARTS 1:6 After navigate to
    Go To     ${ROOT}/forms/named_submit_buttons.html

Event Firing Webdriver Input Text (WebElement)
    [Documentation]
    ...    REGEXP:  .*Before send_keys.*
    ...    REGEXP:  .*After send_keys.*
    Input Text    //input[@name="textfield"]    FooBar

Event Firing Webdriver Click Element (WebElement)
    [Documentation]
    ...    REGEXP:  .*Before click.*
    ...    REGEXP:  .*After click.*
    Click Element    //input[@name="ok_button"]
