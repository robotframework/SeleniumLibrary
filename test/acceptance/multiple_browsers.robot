*** Settings ***
Documentation     Several instances of browser
Suite Setup       Open Two Browsers And Register Indexes
Suite Teardown    Close All Browsers
Resource          resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Last Opened Browser Should Be Active
    [Documentation]    Tests if browser is active
    Verify Location Is "links.html"

It Should Be Possible To Switch Between Browsers Using Indexes
    [Documentation]    Tests switching browsers
    Switch Browser    ${BROWSER1}
    Verify Location Is ""

It Should Be Give An Alias To New Browser Instance
    [Documentation]    Tests browser alias
    Open Browser    ${ROOT}/forms/prefilled_email_form.html    ${BROWSER}    Third Browser
    ...    remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}
    Verify Location Is "forms/prefilled_email_form.html"
    Switch Browser    ${BROWSER1}
    Verify Location Is ""
    Switch Browser    Third Browser
    Verify Location Is "forms/prefilled_email_form.html"

It Should Be Possible Close A Browser
    [Documentation]    Tests closing browsers
    Open Browser    ${ROOT}/forms/prefilled_email_form.html    ${BROWSER}    Third
    ...    remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}
    Switch Browser    ${BROWSER2}
    Close Browser
    Switch Browser    Third
    Close Browser
    ${BROWSER2} =    Open Browser    ${ROOT}/links.html    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}

Correct Error Message Should Be Given When Trying To Switch To Non-Existing Browser
    [Documentation]    Tests error message
    Run Keyword And Expect Error    No browser with index or alias 'non-existing' found.
    ...    Switch Browser    non-existing

*** Keywords ***
Open Two Browsers And Register Indexes
    [Documentation]    Opens two idexed browsers
    Cannot Be Executed in IE
    ${BROWSER1} =    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}
    ${BROWSER2} =    Open Browser    ${ROOT}/links.html    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}
    Set Suite Variable    $BROWSER1
    Set Suite Variable    $BROWSER2
