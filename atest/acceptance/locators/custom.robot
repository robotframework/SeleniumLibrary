*** Settings ***
Documentation     Test custom locators
Suite Setup       Go To Page "index.html"
Resource          ../resource.robot

*** Test Cases ***
Test Custom Locator
    [Setup]    Setup Custom Locator
    Page Should Contain Element    custom=some_id
    Page Should Not Contain Element    custom=invalid_id

Ensure Locator Auto Unregisters
    [Documentation]    Checks to see if the custom locator registered in the last
    ...    test was automatically unregistered. Setup Custom Locator will fail
    ...    if another locator of the same name is registered.
    Setup Custom Locator

Ensure Attempting to Unregister a Default Locator Fails
    Run Keyword And Expect Error
    ...    Cannot unregister the default strategy 'id'.
    ...    Remove Location Strategy    id

Ensure Unregistering Non-Existent Locator Fails
    Run Keyword And Expect Error
    ...    Cannot unregister the non-registered strategy 'non-existing'.
    ...    Remove Location Strategy    non-existing

Ensure a Custom Locator can be Unregistered
    Setup Custom Locator    persist
    Teardown Custom Locator
    # Test step is used for the next test. It sets up a persistant locator.
    Setup Custom Locator    persist

Ensure Locators Can Persist
    Page Should Contain Element    custom=some_id
    Run Keyword And Expect Error    *    Setup Custom Locator
    [Teardown]    Teardown Custom Locator

*** Keywords ***
Setup Custom Locator
    [Arguments]    ${persist}=${EMPTY}
    Add Location Strategy    custom    Custom Locator Strategy    persist=${persist}

Teardown Custom Locator
    Remove Location Strategy    custom

Custom Locator Strategy
    [Arguments]    ${browser}    ${locator}    ${tag}    ${constraints}
    ${element}=    Execute Javascript    return window.document.getElementById('${locator}') || [];
    [Return]    ${element}
