*** Settings ***
Suite Teardown    Close All Browsers
Resource          resource.robot
Documentation     These tests check the service argument of Open Browser.

*** Test Cases ***
Browser With Selenium Service As String
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    service=port=1234; executable_path='/path/to/driver/executable'
