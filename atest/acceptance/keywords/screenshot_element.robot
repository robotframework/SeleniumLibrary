*** Settings ***
Documentation    Suite description
Suite Setup       Go To Page "links.html"
Resource          ../resource.robot

*** Test Cases ***
Capture Element Screenshot
    [Setup]    Remove Files    ${OUTPUTDIR}/selenium-element-screenshot-1.png
    ${path} =    Capture Element Screenshot    id:nothing
    File Should Exist    ${OUTPUTDIR}/selenium-element-screenshot-1.png
    Should Be Equal    ${path}    ${OUTPUTDIR}${/}selenium-element-screenshot-1.png

Capture Element Screenshot When Element Does Not Exist
    Run Keyword And Expect Error
    ...    Element with locator 'id:not_here' not found.
    ...    Capture Element Screenshot    id:not_here

Capture Element Screenshot When Path Does Not Exist
    [Setup]    Remove Directory    ${OUTPUTDIR}/elements_pictures
    ${path} =    Capture Element Screenshot    id:nothing    ${OUTPUTDIR}${/}elements_pictures${/}selenium-element-screenshot-1.png
    File Should Exist    ${OUTPUTDIR}${/}elements_pictures${/}selenium-element-screenshot-1.png
    Should Be Equal    ${path}    ${OUTPUTDIR}${/}elements_pictures${/}selenium-element-screenshot-1.png

Capture Element Screenshot When No Browser Is Open
    [Setup]    Close All Browsers
    ${path} =    Capture Element Screenshot    id:nothing
    Should Not Be True    ${path}
    [Teardown]  Open Browser To Start Page

