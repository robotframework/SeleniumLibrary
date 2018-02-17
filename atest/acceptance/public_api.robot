*** Settings ***
Resource          resource.robot
Library           CustomSeleniumKeywords
Suite Setup       Run Keywords
...               Set Library Search Order    CustomSeleniumKeywords    AND
...               Open Browser To Start Page
Suite Teardown    Close Browser

*** Test Cases ***
Find Element
    ${first} =    Use Find Element    first
    Should Be Equal    ${first.text}    This is the haystack and somewhere on this page is a needle.
    ${em} =    Use Find Element    css:em    ${first}
    Should Be Equal    ${em.text}    needle
    Run Keyword And Expect Error
    ...    Element with locator 'nonex' not found.
    ...    Use Find Element    nonex

Find Elements
    ${paras} =    Use Find Elements    //p
    Should Be Equal    ${paras[0].text}    This is the haystack and somewhere on this page is a needle.
    Length Should Be    ${paras}    2
    ${ems} =    Use Find Elements    tag:em    ${paras[0]}
    Should Be Equal    ${ems[0].text}    needle
    Length Should Be    ${ems}    1
    ${nonex} =    Use Find Elements    nonex
    Length Should Be    ${nonex}    0
