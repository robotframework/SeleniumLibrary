*** Setting ***
Documentation     These tests must open own browser because windows opened by
...               earlier tests would otherwise be visible to Get Window XXX keywords
...               even if those windows were closed.
Suite Setup        Open 3 Browsers with Windows
Suite Teardown     Close All Browsers
Resource          resource.robot

*** Variables ***
@{BrowserA_EXP_TITLES}=    WindowA1    WindowA2    WindowA3
@{BrowserB_EXP_TITLES}=    WindowB1    WindowB2
@{BrowserC_EXP_TITLES}=    WindowC1
@{ALL_BROWSERS_EXP_TITLES}=    @{BrowserA_EXP_TITLES}    @{BrowserB_EXP_TITLES}    @{BrowserC_EXP_TITLES}
@{EXP_ALIASES}=    BrowserA    BrowserB    BrowserC
@{EXP_IDS}=    ${1}    ${2}    ${3}


*** Test Cases ***
Check Titles of Multiple Browser-Windows 
    @{BrowserA_Titles}=    Get Window Titles    browser=BrowserA 
    Should Be Equal        ${BrowserA_Titles}    ${BrowserA_EXP_TITLES}
    @{BrowserB_Titles}=    Get Window Titles    browser=BrowserB
    Should Be Equal        ${BrowserB_Titles}    ${BrowserB_EXP_TITLES}
    @{BrowserC_Titles}=    Get Window Titles    browser=BrowserC
    Should Be Equal        ${BrowserC_Titles}    ${BrowserC_EXP_TITLES}
    @{All_Browsers_Titles}=    Get Window Titles  browser=ALL
    Should Be Equal            ${All_Browsers_Titles}    ${ALL_BROWSERS_EXP_TITLES}

Check Count of Handle
    Check Handle Count    3    BrowserA
    Check Handle Count    2    BrowserB
    Check Handle Count    1    BrowserC
    Check Handle Count    6    ALL

Check Count of Names
    Check Name Count    3    BrowserA
    Check Name Count    2    BrowserB
    Check Name Count    1    BrowserC
    Check Name Count    6    ALL

Check Count of Identifiers
    Check Identifiers Count    3    BrowserA
    Check Identifiers Count    2    BrowserB
    Check Identifiers Count    1    BrowserC
    Check Identifiers Count    6    ALL

Check Locations
    @{Locations}=    Get Locations    browser=ALL
    Should Be Equal As Strings    ${Locations}[0]    ${FRONT_PAGE}javascript/dynamic_content.html?1
    Should Be Equal As Strings    ${Locations}[1]    ${FRONT_PAGE}javascript/dynamic_content.html?2
    Should Be Equal As Strings    ${Locations}[2]    ${FRONT_PAGE}javascript/dynamic_content.html?3
    Should Be Equal As Strings    ${Locations}[3]    ${FRONT_PAGE}javascript/dynamic_content.html?4
    Should Be Equal As Strings    ${Locations}[4]    ${FRONT_PAGE}javascript/dynamic_content.html?5
    Should Be Equal As Strings    ${Locations}[5]    ${FRONT_PAGE}javascript/dynamic_content.html?6
    ${count}    Get Length    ${Locations}
    Should Be Equal As Integers    6    ${count}

Get Browser Ids and Alias
    @{Aliases}=    Get Browser Aliases
    Should Be Equal    ${Aliases}    ${EXP_ALIASES}
    &{Aliases}=    Get Browser Aliases  
    Should Be Equal    ${Aliases.BrowserA}   ${1}
    Should Be Equal    ${Aliases.BrowserB}   ${2}
    Should Be Equal    ${Aliases.BrowserC}   ${3}
    @{IDs}=    Get Browser Ids  
    Should Be Equal    ${IDs}    ${EXP_IDS}

Select Window by Location
    Switch Browser    BrowserA
    Switch Window     WindowA1
    Switch Window By Location    ${FRONT_PAGE}javascript/dynamic_content.html?5
    ${location}    Get Location
    Should Be Equal    ${FRONT_PAGE}javascript/dynamic_content.html?5    ${location}
    Title Should Be    WindowB2

Switch Window to Different Browser
    Switch Browser      BrowserC
    Switch Window       WindowC1
    Location Should Be      ${FRONT_PAGE}javascript/dynamic_content.html?6
    Switch Window       title:WindowA1    browser=BrowserA
    Location Should Be      ${FRONT_PAGE}javascript/dynamic_content.html?1
    Switch Window       url:${FRONT_PAGE}javascript/dynamic_content.html?4    browser=BrowserB
    Title Should Be     WindowB1

Get Specific Locations and Title
    Switch Browser    BrowserA
    Switch Window     title:WindowA1
    Location Should Be    ${FRONT_PAGE}javascript/dynamic_content.html?1
    @{Locations}=    Get Locations    browser=BrowserB
    Should Be Equal    ${Locations}[0]    ${FRONT_PAGE}javascript/dynamic_content.html?4
    Should Be Equal    ${Locations}[1]    ${FRONT_PAGE}javascript/dynamic_content.html?5
    ${count}=    Get Length    ${Locations}
    Should Be Equal As Integers    ${count}    2
    @{Titles}=    Get Window Titles    browser=BrowserC
    Should Be Equal    ${Titles}[0]    WindowC1
    ${count}=    Get Length    ${Titles}
    Should Be Equal As Integers    ${count}    1
    

Fail Switching Window and Locations From Different Browser
    Switch Browser    BrowserA
    Switch Window     WindowA1
    ${Error_Msg}=    Run Keyword And Expect Error    *    Switch Window    WindowB1
    Should Be Equal As Strings    ${Error_Msg}    No window matching handle, name, title or URL 'WindowB1' found.
    ${Error_Msg}=    Run Keyword And Expect Error    *    Get Locations    browser=UnknownBrowser
    Should Be Equal As Strings    ${Error_Msg}    Non-existing index or alias 'UnknownBrowser'.
    ${Error_Msg}=    Run Keyword And Expect Error    *    Get Window Handles    browser=${4}
    Should Be Equal As Strings    ${Error_Msg}    Non-existing index or alias '4'.



*** Keywords ***
Open 3 Browsers with Windows
    Close All Browsers
    Open Browser With Alias And Title    BrowserA    WindowA1    1
    Open New Window and set Title                    WindowA2    2
    Open New Window And Set Title                    WindowA3    3
    Open Browser With Alias And Title    BrowserB    WindowB1    4
    Open New Window And Set Title                    WindowB2    5
    Open Browser With Alias And Title    BrowserC    WindowC1    6

Open New Window And Set Title
    [Arguments]    ${title}    ${id}
    Execute Javascript    window.open("dynamic_content.html?${id}")
    Switch Window    locator=NEW
    Set Window Title    ${title}

Open Browser With Alias And Title
    [Arguments]    ${alias}    ${title}    ${id}
    Open Browser    ${FRONT_PAGE}javascript/dynamic_content.html?${id}    ${BROWSER}    alias=${alias}
    Set Window Title    ${title}

Set Window Title
    [Arguments]    ${title}
    Input Text    id:titleChangeTxt    ${title}
    Click Button    id:titleChangeBtn
    Title Should Be    ${title}

Check Handle Count
    [Arguments]    ${length}    ${browser_alias}=${None}
    @{WinCountBrowser}=    Get Window Handles    ${browser_alias}
    ${len}=    Get Length     ${WinCountBrowser}
    Should Be Equal As Integers    ${len}   ${length}

Check Name Count
    [Arguments]    ${length}    ${browser_alias}=${None}
    @{WinCountBrowser}=    Get Window Names    ${browser_alias}
    ${len}=    Get Length     ${WinCountBrowser}
    Should Be Equal As Integers    ${len}   ${length}
    
Check Identifiers Count
    [Arguments]    ${length}    ${browser_alias}=${None}
    @{WinCountBrowser}=    Get Window Identifiers    ${browser_alias}
    ${len}=    Get Length     ${WinCountBrowser}
    Should Be Equal As Integers    ${len}   ${length}

Switch Window By Location
    [Arguments]    ${selected_location}
    @{IDs}=    Get Browser Ids
    FOR     ${id}    IN    @{IDs}
        @{locations}=    Get Locations    browser=${id}
        Run Keyword If    '${selected_location}' in $locations
        ...    Switch Window    url:${selected_location}    browser=${id}
    END
