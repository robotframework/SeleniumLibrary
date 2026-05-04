*** Settings ***
Documentation     Verifies Input Text and Input Password accept Robot Framework
...               7.4+ Secret type without ValueError. See issue #1966.
Suite Setup       Open Browser To Start Page Disabling Chrome Leaked Password Detection
Test Setup        Go To Page "forms/login.html"
Resource          ../resource.robot
Library           ${CURDIR}/../../resources/secret_helper.py
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Input Password Accepts Secret Type
    [Tags]    require-rf-7.4
    Skip If    not ${SECRET_AVAILABLE}    RF Secret type requires Robot Framework 7.4+
    ${pw}=    Make Secret    s3cret-pass
    Input Text        username_field    yuri
    Input Password    password_field    ${pw}
    ${value}=    Get Value    password_field
    Should Be Equal    ${value}    s3cret-pass

Input Text Accepts Secret Type
    [Tags]    require-rf-7.4
    Skip If    not ${SECRET_AVAILABLE}    RF Secret type requires Robot Framework 7.4+
    ${user}=    Make Secret    yuri
    Input Text    username_field    ${user}
    ${value}=    Get Value    username_field
    Should Be Equal    ${value}    yuri

Input Password With Plain String Still Works
    [Documentation]    Backwards compatibility — plain str must still be accepted.
    Input Text        username_field    yuri
    Input Password    password_field    plain-pass
    ${value}=    Get Value    password_field
    Should Be Equal    ${value}    plain-pass

Input Password Does Not Log Secret Value
    [Tags]    require-rf-7.4    NoGrid
    [Documentation]
    ...    LOG 2:1  INFO    Typing password into text field 'password_field'.
    Skip If    not ${SECRET_AVAILABLE}    RF Secret type requires Robot Framework 7.4+
    ${pw}=    Make Secret    must-not-leak
    Input Password    password_field    ${pw}

*** Keywords ***
Open Browser To Start Page Disabling Chrome Leaked Password Detection
    [Arguments]    ${alias}=${None}
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    options=add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})    alias=${alias}