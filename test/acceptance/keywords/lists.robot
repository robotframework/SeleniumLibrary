*** Settings ***
Documentation     Tests lists
Test Setup        Go To Page "forms/prefilled_email_form.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Get List Items From Single-Select List
    [Documentation]    Get List Items From Single-Select List
    ${items}=    Get List Items    preferred_channel
    ${expected}=    Create List    Email    Telephone    Direct mail
    Should Be Equal    ${items}    ${expected}

Get List Items From Multi-Select List
    [Documentation]    Get List Items From Multi-Select List
    ${items}=    Get List Items    interests
    ${expected}=    Create List    Males    Females    Others
    Should Be Equal    ${items}    ${expected}

Get Selected List Value
    [Documentation]    Get Selected List Value
    ${selected}=    Get Selected List Value    preferred_channel
    Should Be Equal    ${selected}    phone

Get Selected List Values
    [Documentation]    Get Selected List Values
    ${selected}=    Get Selected List Values    preferred_channel
    ${expected}=    Create List    phone
    Should Be Equal    ${selected}    ${expected}

Get Selected List Label
    [Documentation]    Get Selected List Label
    ${selected}=    Get Selected List Label    preferred_channel
    Should Be Equal    ${selected}    Telephone
    Select From List    interests    Males
    ${selected}=    Get Selected List Label    interests
    Should Be Equal    ${selected}    Males

Get Selected List Labels
    [Documentation]    Get Selected List Labels
    ${selected}=    Get Selected List Labels    possible_channels
    ${expected}=    Create List    Email    Telephone
    Should Be Equal    ${selected}    ${expected}

List Selection Should Be
    [Documentation]    LOG 2 Verifying list 'interests' has no options selected.
    ...    LOG 5 Verifying list 'possible_channels' has option(s) [ email | Telephone ] selected.
    List Selection Should Be    interests
    List Selection Should Be    preferred_channel    Telephone
    List Selection Should Be    preferred_channel    phone
    List Selection Should Be    possible_channels    email    Telephone
    Run Keyword And Expect Error
    ...    List 'possible_channels' should have had selection [ email | Telephone | Direct mail ] but it was [ Email | Telephone ]
    ...    List Selection Should Be    possible_channels    email    Telephone    Direct mail

List Selection Should Be When Extraneous Options Are Selected
    [Documentation]    List Selection Should Be When Extraneous Options Are Selected
    Run Keyword And Expect Error
    ...    List 'possible_channels' should have had selection [ email ] but it was [ Email | Telephone ]
    ...    List Selection Should Be    possible_channels    email

List Selection Should Be When List Does Not Exist
    [Documentation]    List Selection Should Be When List Does Not Exist
    Run Keyword And Expect Error    Page should have contained list 'nonexisting' but did not
    ...    List Selection Should Be    nonexisting    whatever

UnSelect Single Value From List
    [Documentation]    LOG 2.1 Unselecting option(s) 'Email' from list 'possible_channels'.
    Unselect and Verify Selection    possible_channels    Email    phone
    Comment    unselecting already unselected option has no effect
    Unselect and Verify Selection    possible_channels    Email    phone
    Unselect And Verify Selection    possible_channels    Telephone
    Run Keyword And Expect Error    Keyword 'Unselect from list' works only for multiselect lists.
    ...    Unselect From List    preferred_channel

UnSelect All From List
    [Documentation]    LOG 2 Unselecting all options from list 'possible_channels'.
    Unselect From List    possible_channels
    List Selection Should Be    possible_channels

Select From Single Selection List
    [Documentation]    LOG 2.1 Selecting option(s) 'Email' from list 'preferred_channel'.
    Select And verify selection    preferred_channel    Email    Email
    Select And verify selection    preferred_channel    Email    Email
    Select And verify selection    preferred_channel    directmail    Direct mail
    Select From List    preferred_channel    Telephone
    # do something else... anything to ensure the list is really set as the next keyword will pass 
    # if list item is highlighted but not selected
    Unselect from List    possible_channels
    List Selection Should Be    preferred_channel    Telephone
    Select From List    preferred_channel
    List Selection Should Be    preferred_channel    Direct mail

Select Non-Existing Item From Single Selection List
    [Documentation]    Select Non-Existing Item From Single Selection List
    [Tags]    OnlyThisOne
    Run Keyword And Expect Error
    ...    ValueError: Option 'Smoke Signals' not in list 'preferred_channel'.
    ...    Select From List    preferred_channel    Tin Can Phone    Smoke Signals
    Select From List    preferred_channel    Tin Can Phone    Smoke Signals    Email
    Run Keyword And Expect Error
    ...    ValueError: Option 'Tin Can Phone' not in list 'preferred_channel'.
    ...    Select From List    preferred_channel    Smoke Signals    Email    Tin Can Phone
    Run Keyword And Expect Error
    ...    NoSuchElementException: Message: Could not locate element with visible text: Tin Can Phone
    ...    Select From List By Label    preferred_channel    Tin Can Phone

Select Non-Existing Item From Multi-Selection List
    [Documentation]    Select Non-Existing Item From Multi-Selection List
    [Tags]    OnlyThisOne
    Run Keyword And Expect Error
    ...    ValueError: Options 'Tin Can Phone, Smoke Signals' not in list 'possible_channels'.
    ...    Select From List    possible_channels    Tin Can Phone    Smoke Signals
    Run Keyword And Expect Error
    ...    ValueError: Options 'Tin Can Phone, Smoke Signals' not in list 'possible_channels'.
    ...    Select From List    possible_channels    Tin Can Phone    Smoke Signals    Email
    Run Keyword And Expect Error
    ...    ValueError: Options 'Tin Can Phone, Smoke Signals' not in list 'possible_channels'.
    ...    Select From List    possible_channels    Tin Can Phone    Email    Smoke Signals

Unselect Non-Existing Item From List
    [Documentation]    LOG 3 Unselecting option(s) 'Tin Can Phone, Smoke Signals, Email' from list 'possible_channels'.
    [Tags]    OnlyThisOne
    Unselect From List    possible_channels    Tin Can Phone    Smoke Signals
    Unselect From List    possible_channels    Tin Can Phone    Smoke Signals    Email

Select From Multiselect List
    [Documentation]    LOG 5 Selecting option(s) 'Direct mail, phone' from list 'possible_channels'.
    Select And verify selection    possible_channels    email    email    Telephone
    Select And verify selection    possible_channels
    ...    Direct mail    Direct mail    email    Telephone
    Unselect from List    possible_channels
    Select From List    possible_channels    Direct mail    phone
    List Selection Should Be    possible_channels    Telephone    directmail

Select All From List
    [Documentation]    LOG 2 Selecting all options from list 'interests'.
    Select All From List    interests
    List Selection Should Be    interests    Males    Females    Others
    Run Keyword And Expect Error    Keyword 'Select all from list' works only for multiselect lists.
    ...    Select All From List    preferred_channel

List Should Have No Selections
    [Documentation]    LOG 2 Verifying list 'interests' has no selection.
    List Should Have No Selections    interests
    Select All From List    interests
    Run Keyword And Expect Error
    ...    List 'interests' should have had no selection (selection was [ Males | Females | Others ])
    ...    List Should Have No Selections    interests

*** Keywords ***
Unselect And Verify Selection
    [Documentation]    Unselect And Verify Selection
    [Arguments]    ${list_id}    ${unselection}    @{exp_selection}
    Unselect From List    ${list_id}    ${unselection}
    List Selection Should Be    ${list_id}    @{exp_selection}

Select And Verify Selection
    [Documentation]    Select And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select From list    ${list_id}    ${selection}
    List Selection Should Be    ${list_id}    @{exp_selection}
