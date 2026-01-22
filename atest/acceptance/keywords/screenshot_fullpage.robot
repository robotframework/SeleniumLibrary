*** Settings ***
Documentation     Tests fullpage screenshots
Suite Setup       Go To Page "forms.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Capture fullpage screenshot to default location
    [Tags]    NoGrid
    [Documentation]
    ...    LOG 1:5 </td></tr><tr><td colspan="3"><a href="selenium-fullpage-screenshot-1.png"><img src="selenium-fullpage-screenshot-1.png" width="800px"></a>
    ...    LOG 7:5 </td></tr><tr><td colspan="3"><a href="selenium-fullpage-screenshot-2.png"><img src="selenium-fullpage-screenshot-2.png" width="800px"></a>
    [Setup]    Remove Files    ${OUTPUTDIR}/selenium-fullpage-screenshot-*.png
    ${file} =    Capture Fullpage Screenshot
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    selenium-fullpage-screenshot-*.png
    Should Be Equal As Integers    ${count}    1
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}selenium-fullpage-screenshot-1.png
    Click Link    Relative
    Wait Until Page Contains Element    tag=body
    Capture Fullpage Screenshot
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    selenium-fullpage-screenshot-*.png
    Should Be Equal As Integers    ${count}    2

Capture fullpage screenshot to custom file
    [Setup]    Remove Files    ${OUTPUTDIR}/custom-fullpage-screenshot.png
    Capture Fullpage Screenshot    custom-fullpage-screenshot.png
    File Should Exist    ${OUTPUTDIR}/custom-fullpage-screenshot.png

Capture fullpage screenshot to custom directory
    [Setup]    Remove Files    ${TEMPDIR}/seleniumlibrary-fullpage-screenshot-test.png
    Create Directory    ${TEMPDIR}
    Set Screenshot Directory    ${TEMPDIR}
    Capture Fullpage Screenshot    seleniumlibrary-fullpage-screenshot-test.png
    File Should Exist    ${TEMPDIR}/seleniumlibrary-fullpage-screenshot-test.png

Capture fullpage screenshot with index
    [Setup]    Remove Files    ${OUTPUTDIR}/fullpage-screenshot-*.png
    Capture Fullpage Screenshot    fullpage-screenshot-{index}.png
    Capture Fullpage Screenshot    fullpage-screenshot-{index}.png
    File Should Exist    ${OUTPUTDIR}/fullpage-screenshot-1.png
    File Should Exist    ${OUTPUTDIR}/fullpage-screenshot-2.png

Capture fullpage screenshot with formatted index
    [Setup]    Remove Files    ${OUTPUTDIR}/fullpage-screenshot-*.png
    Capture Fullpage Screenshot    fullpage-screenshot-{index:03}.png
    File Should Exist    ${OUTPUTDIR}/fullpage-screenshot-001.png

Capture fullpage screenshot embedded
    [Setup]    Set Screenshot Directory    EMBED
    ${result} =    Capture Fullpage Screenshot
    Should Be Equal    ${result}    EMBED

Capture fullpage screenshot base64
    [Setup]    Set Screenshot Directory    BASE64
    ${result} =    Capture Fullpage Screenshot
    Should Not Be Empty    ${result}
    Should Match Regexp    ${result}    ^[A-Za-z0-9+/=]+$

Capture fullpage screenshot with EMBED filename
    [Setup]    Set Screenshot Directory    EMBED
    ${result} =    Capture Fullpage Screenshot    EMBED
    Should Be Equal    ${result}    EMBED

Capture fullpage screenshot with BASE64 filename
    [Setup]    Set Screenshot Directory    EMBED
    ${result} =    Capture Fullpage Screenshot    BASE64
    Should Not Be Empty    ${result}
    Should Match Regexp    ${result}    ^[A-Za-z0-9+/=]+$

Capture fullpage screenshot when no browser
    [Setup]    Close All Browsers
    ${result} =    Capture Fullpage Screenshot
    Should Be Equal    ${result}    ${None}
