*** Settings ***
Test Setup        Go To Page "forms/prefilled_email_form.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Get List Items From Single-Select List
    ${items}=    Get List Items    preferred_channel
    ${expected}=    Create List    Email    Telephone    Direct mail
    Should Be Equal    ${items}    ${expected}

Get List Items From Multi-Select List
    ${items}=    Get List Items    interests
    ${expected}=    Create List    Males    Females    Others
    Should Be Equal    ${items}    ${expected}

Get List Values From Single-Select List
    ${values}=    Get List Items    preferred_channel    value=${True}
    ${expected}=    Create List    email    phone    directmail
    Should Be Equal    ${values}    ${expected}

Get List Values From Multi-Select List
    ${values}=    Get List Items    interests    value=True
    ${expected}=    Create List    males    females    others
    Should Be Equal    ${values}    ${expected}

Get Selected List Value
    ${selected}=    Get Selected List Value    preferred_channel
    Should Be Equal    ${selected}    phone

Get Selected List Values
    ${selected}=    Get Selected List Values    preferred_channel
    ${expected}=    Create List    phone
    Should Be Equal    ${selected}    ${expected}
    ${selected}=    Get Selected List Values    interests
    Should Be Empty    ${selected}

Get Selected List Label
    ${selected}=    Get Selected List Label    preferred_channel
    Should Be Equal    ${selected}    Telephone
    Select From List    interests    Males
    ${selected}=    Get Selected List Label    interests
    Should Be Equal    ${selected}    Males

Get Selected List Labels
    ${selected}=    Get Selected List Labels    possible_channels
    ${expected}=    Create List    Email    Telephone
    Should Be Equal    ${selected}    ${expected}
    ${selected}=    Get Selected List Labels    interests
    Should Be Empty    ${selected}

List Selection Should Be
    [Documentation]
    ...    LOG 2 Verifying list 'interests' has options [${SPACE*2}] selected.
    ...    LOG 5 Verifying list 'possible_channels' has options [ Email | Telephone ] selected.
    List Selection Should Be    interests
    List Selection Should Be    preferred_channel    Telephone
    List Selection Should Be    preferred_channel    phone
    List Selection Should Be    possible_channels    Email    Telephone
    List Selection Should Be    possible_channels    Telephone    Email
    List Selection Should Be    possible_channels    phone    email
    Run Keyword And Expect Error
    ...    List 'possible_channels' should have had selection [ Email | Telephone | Direct mail ] but selection was [ Email (email) | Telephone (phone) ].
    ...    List Selection Should Be    possible_channels    Email    Telephone    Direct mail

List Selection Should Be When Extraneous Options Are Selected
    Run Keyword And Expect Error
    ...    List 'possible_channels' should have had selection [ email ] but selection was [ Email (email) | Telephone (phone) ].
    ...    List Selection Should Be    possible_channels    email

List Selection Should Be When List Does Not Exist
    Run Keyword And Expect Error
    ...    Page should have contained list 'nonexisting' but did not.
    ...    List Selection Should Be    nonexisting    whatever

UnSelect Single Value From List
    Unselect and Verify Selection    possible_channels    Email    phone
    # Unselecting already unselected option has no effect
    Unselect and Verify Selection    possible_channels    Email    phone
    Unselect And Verify Selection    possible_channels    Telephone
    Run Keyword And Expect Error
    ...    Keyword 'Unselect from list' works only for multiselect lists.
    ...    Unselect From List    preferred_channel

Unselect all options using Unselect From List
    Unselect From List    possible_channels
    List Should Have No Selections    possible_channels

Unselect All From List
    [Documentation]    LOG 2 Unselecting all options from list 'possible_channels'.
    Unselect All From List    possible_channels
    List Should Have No Selections    possible_channels
    Unselect All From List    interests
    List Should Have No Selections    interests
    Select All From List    interests
    Unselect All From List    interests
    List Should Have No Selections    interests

Select From Single Selection List
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
    Unselect From List    possible_channels    Tin Can Phone    Smoke Signals
    Unselect From List    possible_channels    Tin Can Phone    Smoke Signals    Email

Select From Multiselect List
    Select And verify selection    possible_channels    Email    Email    Telephone
    Select And verify selection    possible_channels    email    email    phone
    Select And verify selection    possible_channels    Direct mail    Direct mail    Email    Telephone
    Unselect from List    possible_channels
    Select From List    possible_channels    Direct mail    phone
    List Selection Should Be    possible_channels    Telephone    Direct mail

Select All From List
    [Documentation]    LOG 2 Selecting all options from list 'interests'.
    Select All From List    interests
    List Selection Should Be    interests    Males    Females    Others
    Run Keyword And Expect Error
    ...    'Select All From List' works only with multi-selection lists.
    ...    Select All From List    preferred_channel

List Should Have No Selections
    [Documentation]    LOG 2 Verifying list 'interests' has no selections.
    List Should Have No Selections    interests
    Select All From List    interests
    Run Keyword And Expect Error
    ...    List 'interests' should have had no selection but selection was [ Males (males) | Females (females) | Others (others) ].
    ...    List Should Have No Selections    interests

*** Keywords ***
Unselect And Verify Selection
    [Arguments]    ${list_id}    ${unselection}    @{exp_selection}
    Unselect From List    ${list_id}    ${unselection}
    List Selection Should Be    ${list_id}    @{exp_selection}

Select And Verify Selection
    [Arguments]    ${list_id}    ${selection}    @{exp_selection}
    Select From list    ${list_id}    ${selection}
    List Selection Should Be    ${list_id}    @{exp_selection}
