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

Multiple Locators with double arrows as separator should work
    Page Should Contain Element    css:div#div_id >> xpath:a[6] >> id:image1_id

Multiple Locators strategy should be case-insensitive
    Page Should Contain Element    cSs=div#div_id >> XpaTh=a[6] >> iD=image1_id

Multiple Locators as a List should work
    ${element} =   Get WebElement    id:foo:bar
    ${locator_list} =    Create List    id:div_id    ${element}    id:bar=foo
    Page Should Contain Element    ${locator_list}

When One Of Locator From Multiple Locators Is Not Found Keyword Fails
    Run Keyword And Expect Error
    ...    Element with locator 'id:not_here' not found.
    ...    Page Should Contain Element    css=div#div_id >> id:not_here >> iD=image1_id

When One Of Locator From Multiple Locators Matches Multiple Elements Keyword Should Not Fail
    Page Should Contain Element    xpath://div >> id=image1_id
