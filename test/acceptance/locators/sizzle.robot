*** Settings ***
Suite Setup       Remote Or Local    # Decides which jQuery to use, in the event of no Internet or Proxy blocking.
Test Setup        Go To Page "${SIZZLE_URL}"
Resource          ../resource.robot

*** Variables ***
${SIZZLE_URL}     ${EMPTY}

*** Test Cases ***
Find By Id
    Cannot Be Executed In Chrome
    Page Should Contain Element    jquery=#div_id
    Element Should Contain    jquery=#foo    Text and image
    Click Link    sizzle=#some_id
    Title Should Be    (root)/broken.html

Find In Table
    Cannot Be Executed In Chrome
    Table Should Contain    jquery=table#simpleTable    simpleTable
    Table Header Should Contain    jquery=table#tableWithTwoHeaders    tableWithTwoHeaders_C2
    Table Footer Should Contain    jquery=table#withHeadAndFoot    withHeadAndFoot_AF1
    Table Row Should Contain    jquery=table#mergedRows    1    mergedRows_D1
    Table Column Should Contain    jquery=table#mergedCols    1    mergedCols_D1
    Table Cell Should Contain    jquery=table#formattedTable    1    1    formattedTable_A1
    Table Cell Should Contain    jquery=table#formattedTable    2    4    äöü€&äöü€&
    Table Cell Should Contain    jquery=h2.someClass ~ table:last-child    2    4    äöü€&äöü€&

Find By Everything Else
    Cannot Be Executed In Chrome
    Page Should Contain Element    jquery=[href="index.html"]
    Element Should Contain    jquery=[target="_blank"]    Target opens in new window
    Click Link    sizzle=:has(img[alt="tooltip"])
    Title Should Be    (root)/index.html

*** Keywords ***
Remote Or Local
    [Documentation]    If there is no access to http://code.jquery.com/jquery-1.11.1.min.js uses locally javascript/jquery-1.11.1.min.js.
    Cannot Be Executed In Chrome    #Even if we use jQuery local we get this error: WebDriverException: Message: u'unknown error: jQuery is not defined\n \ (Session info: chrome=36.0.1985.143)\n \ (Driver info: chromedriver=2.10.267521,platform=Windows NT 6.1 SP1 x86_64)'
    ${oldloglevel}=    BuiltIn.Set Log Level    NONE
    ${oldspeed}=    Set Selenium Speed    0 seconds
    ${oldtimeout}=    Set Selenium Timeout    5 seconds
    ${remote}=    Run Keyword And Return Status    Selenium2Library.Go To    http://code.jquery.com/jquery-1.11.1.min.js
    ${remote}=    Run Keyword And Return Status    Page Should Contain    jQuery v1.11.1
    Set Selenium Timeout    ${oldtimeout}
    Set Selenium Speed    ${oldspeed}
    Run Keyword If    ${remote} and '${BROWSER}'.lower() != 'chrome'    Set Suite Variable    ${SIZZLE_URL}    jquery.html    ELSE    Set Suite Variable
    ...    ${SIZZLE_URL}    jquery-local.html
    BuiltIn.Set Log Level    ${oldloglevel}
    BuiltIn.Pass Execution    Setup done with Remote='${remote}'
