*** Settings ***
Resource          ../resource.robot

*** Test Cases ***
Capture Page Screenshot Embedded By Screenshot Root Directory
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 3:4 INFO STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64,
    [Setup]    Remove .png Files
    Set Screenshot Directory    Embed
    ${file} =    Capture Page Screenshot
    Should Be Equal    ${file}    EMBED
    Verify That .png Files Do Not Exist

Capture Page Screenshot EMBED As File Name
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 3:4 INFO STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64,
    [Setup]    Remove .png Files
    Set Screenshot Directory                None
    ${file} =    Capture Page Screenshot    EMBED
    Should Be Equal    ${file}    EMBED
    Verify That .png Files Do Not Exist

Capture Element Screenshot EMBED As File Name
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 4:7 INFO STARTS: </td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64,
    [Setup]    Remove .png Files
    Go To Page "links.html"
    Set Screenshot Directory                   None
    ${file} =    Capture Element Screenshot    id:bar=foo    EMBED
    Should Be Equal    ${file}    EMBED
    Verify That .png Files Do Not Exist

Capture Page Screenshot Override EMBED
    [Tags]    NoGrid
    [Setup]    Remove .png Files
    Set Screenshot Directory    EMBED
    ${file}=    Capture Page Screenshot    override-embed-screenshot.png
    Should Be Equal    ${file}    ${OUTPUTDIR}/override-embed-screenshot.png
    File Should Exist    ${OUTPUTDIR}/override-embed-screenshot.png
    File Should Not Exist    ${EXECDIR}/*.png
    File Should Not Exist    ${EXECDIR}/EMBED/*.png

*** Keywords ***
Remove .png Files
    Remove Files     ${OUTPUTDIR}/*.png
    Remove Files     ${EXECDIR}/*.png
    Remove Files     ${EXECDIR}/Embed/*.png

Verify That .png Files Do Not Exist
    File Should Not Exist    ${OUTPUTDIR}/*.png
    File Should Not Exist    ${EXECDIR}/*.png
    File Should Not Exist    ${EXECDIR}/EMBED/*.png
