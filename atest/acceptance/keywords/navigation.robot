*** Settings ***
Documentation     Tests navigation
Test Setup        Go To Page "links.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Variables ***
${LINKS TITLE}    (root)/links.html
${INDEX TITLE}    (root)/index.html

*** Test Cases ***
Go To
    [Documentation]    Go To
    Verify Location Is "links.html"
    Title Should Be    ${LINKS TITLE}

Go Back
    [Documentation]    Go Back
    [Tags]    Known Issue Safari
    Click Link    Relative
    Title Should Be    ${INDEX TITLE}
    Go Back
    Title Should Be    ${LINKS TITLE}

Click Link
    [Documentation]    LOG 2 Clicking link 'Relative'.
    Click Link    Relative
    Verify Location Is "index.html"
    Title Should Be    ${INDEX TITLE}

Click Link With Whitespace
    [Documentation]    Click Link With Whitespace
    [Tags]    Known Issue Safari
    Click Link    Link with whitespace
    Verify Location Is "target/second.html"

Click Link With Embedded Whitespace
    [Documentation]    Click Link With Embedded Whitespace
    Click Link    Link with whitespace within
    Verify Location Is "target/third.html"

Click Link With Bolded Link Text
    [Documentation]    Click Link With Bolded Link Text
    Click Link    Link with bolded text
    Verify Location Is "target/first.html"

Click Link By Id
    [Documentation]    Click Link By Id
    Click Link    some_id
    Verify Location Is "broken.html"

Click Link By Href
    [Documentation]    Click Link By Href
    Click Link    sub/index.html
    Verify Location Is "sub/index.html"

Click Link With Double Quote
    [Documentation]    Click Link With Double Quote
    Click Link    Link with double " quote
    Verify Location Is "index.html"

Click Link With Special Characters
    [Documentation]    Click Link With Special Characters
    Click Link    Link with < & > \\
    Verify Location Is "index.html"

Click Link With Unicode
    [Documentation]    Click Link With Unicode
    Click Link    Link with Unicode äöüÄÖÜß
    Verify Location Is "index.html"

Click Image
    [Documentation]    LOG 2 Clicking image 'image.jpg'.
    Click Image    image.jpg
    Verify Location Is "index.html"

Click Image By Alt
    [Documentation]    Click Image By Alt
    Click Image    tooltip
    Verify Location Is "index.html"
    Go To Page "links.html"
    Click Image    Image
    Verify Location Is "target/first.html"

Click Image By Id
    [Documentation]    Click Image By Id
    Click Image    image_id
    Verify Location Is "index.html"

Click Image By XPath
    [Documentation]    Click Image By XPath
    Click Image    xpath=//div[@id='second_div']//img
    Verify Location Is "target/second.html"

Click Link With Text And Image
    [Documentation]    Click Link With Text And Image
    Click Link    Text and image
    Verify Location Is "index.html"

Target Opens in New Window
    [Documentation]    Target Opens in New Window
    Cannot Be Executed in IE
    Click Link    Target opens in new window
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    Select Window    ${INDEX TITLE}
    Verify Location Is "index.html"
    [Teardown]    Run Keyword If Test Passed    Run Keywords    Close Window    Select Window

*** Keywords ***
Wait Until Window Is Open
    ${titles} =    Get Window Titles
    ${status} =    Evaluate    len(${titles}) > 1
    Should Be True    ${status}
