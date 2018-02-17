*** Settings ***
Documentation     Tests different supported xpath strategies
Test Setup        Go To Page "links.html"
Resource          ../resource.robot

*** Test Cases ***
xpath with prefix should work
    Page Should Contain Element    xpath=//div[@id="div_id"]/a
    Page Should Contain Element    xpath://div[@id="div_id"]/a

xpath with // and without prefix should work
    Page Should Contain Element    //div[@id="div_id"]/a

xpath with (// and without prefix should work
    Page Should Contain Element    (//div[@id="div_id"]/a)[1]

Locator without prefix
    Page Should Contain Element    div_id

Locator with prefix
    Page Should Contain Element    id:div_id
    Page Should Contain Element    id=div_id
    Page Should Contain Element    id:foo:bar
    Page Should Contain Element    id=foo:bar
    Page Should Contain Element    id:bar=foo
    Page Should Contain Element    id=bar=foo

Locator with separator but without matching prefix is not special
    Page Should Contain Element    foo:bar
    Page Should Contain Element    bar=foo

Locator with separator and with matchign prefix cannot be used as-is
    Page Should Contain Element    id:id:problematic
    Page Should Contain Element    id=id:problematic
    Run Keyword And Expect Error
    ...    Page should have contained element 'id:problematic' but did not.
    ...    Page Should Contain Element    id:problematic
