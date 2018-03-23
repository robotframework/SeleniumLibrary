*** Settings ***
Documentation     Tests Scroll Into View Verification
Suite Setup       Open Browser To Start Page
Resource          ../resource.robot

*** Variables ***
${TEXT}=   You scrolled in div.

*** Test Cases ***
Verify Scroll Element Into View
    [Setup]    Go To Page "scroll/index.html"
    ${initial_postion}=    Get Vertical Position    css:#target
    Scroll Element Into View    css:#target
    ${postion}=    Get Vertical Position    css:#target
    Should Be True    ${initial_postion} > ${postion}
    Element Should Contain    css:#result    ${TEXT}
