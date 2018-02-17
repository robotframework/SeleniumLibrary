*** Settings ***
Documentation     Tests JQuery
Test Setup        Go To Page "jquery.html"
Resource          ../resource.robot

*** Test Cases ***
Find By Id
    [Documentation]    Find By Id
    Page Should Contain Element    jquery=#div_id
    Element Should Contain    jquery=#foo    Text and image
    Click Link    sizzle=#some_id
    Title Should Be    (root)/broken.html

Find In Table
    [Documentation]    Find In Table
    Table Should Contain    jquery=table#simpleTable    simpleTable
    Table Header Should Contain    jquery=table#tableWithTwoHeaders    tableWithTwoHeaders_C2
    Table Footer Should Contain    jquery=table#withHeadAndFoot    withHeadAndFoot_AF1
    Table Row Should Contain    jquery=table#mergedRows    1    mergedRows_D1
    Table Column Should Contain    jquery=table#mergedCols    1    mergedCols_D1
    Table Cell Should Contain    jquery=table#formattedTable    1    1    formattedTable_A1
    Table Cell Should Contain    jquery=table#formattedTable    2    4    äöü€&äöü€&
    Table Cell Should Contain    jquery=h2.someClass ~ table:last-child    2    4    äöü€&äöü€&

Find By Everything Else
    [Documentation]    Find By Everything Else
    Page Should Contain Element    jquery=[href="index.html"]
    Element Should Contain    jquery=[target="_blank"]    Target opens in new window
    Click Link    sizzle=:has(img[alt="tooltip"])
    Title Should Be    (root)/index.html
