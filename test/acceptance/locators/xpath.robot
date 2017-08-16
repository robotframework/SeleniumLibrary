*** Settings ***
Documentation     Tests different supported xpath strategies
Test Setup        Go To Page "links.html"
Resource          ../resource.robot

*** Test Cases ***
xpath with prefix should work
    Page Should Contain Element    xpath=//div[@id="div_id"]/a

xpath with // and without prefix should work
    Page Should Contain Element    //div[@id="div_id"]/a

xpath with (// and without prefix should work
    Page Should Contain Element    (//div[@id="div_id"]/a)[1]
