*** Settings ***
Documentation     Tests screenshots
Suite Setup       Go To Page "links.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Capture page screenshot to default location
    [Documentation]    LOG 2:3 REGEXP: </td></tr><tr><td colspan="3"><a href="selenium-screenshot-\\d.png"><img src="selenium-screenshot-\\d.png" width="800px"></a>
    [Setup]    Remove Files    ${OUTPUTDIR}/selenium-screenshot-*.png
    ${file} =    Capture Page Screenshot
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    selenium-screenshot-*.png
    Should Be Equal As Integers    ${count}    1
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}selenium-screenshot-1.png
    Click Link    Relative
    Wait Until Page Contains Element    tag=body
    Capture Page Screenshot
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    selenium-screenshot-*.png
    Should Be Equal As Integers    ${count}    2

Capture page screenshot to custom file
    [Documentation]    Capture page screenshot to custom file
    [Setup]    Remove Files    ${OUTPUTDIR}/custom-screenshot.png
    Capture Page Screenshot    custom-screenshot.png
    File Should Exist    ${OUTPUTDIR}/custom-screenshot.png

Capture page screenshot to custom directory
    [Documentation]    Capture page screenshot to custom directory
    [Setup]    Remove Files    ${TEMPDIR}/seleniumlibrary-screenshot-test.png
    Capture Page Screenshot    ${TEMPDIR}/seleniumlibrary-screenshot-test.png
    File Should Exist    ${TEMPDIR}/seleniumlibrary-screenshot-test.png

Capture page screenshot to non-existing directory
    [Documentation]    Capture page screenshot to non-existing directory
    [Setup]    Remove Directory    ${OUTPUTDIR}/screenshot    recursive
    Capture Page Screenshot    screenshot/test-screenshot.png
    File Should Exist    ${OUTPUTDIR}/screenshot/test-screenshot.png

Capture page screenshot to custom root directory
    [Documentation]    Capture page screenshot to custom root directory
    [Setup]    Remove Directory    ${OUTPUTDIR}/custom-root    recursive
    Set Screenshot Directory    ${OUTPUTDIR}/custom-root
    ${file} =    Capture Page Screenshot    custom-root-screenshot.png
    File Should Exist    ${OUTPUTDIR}/custom-root/custom-root-screenshot.png
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}custom-root${/}custom-root-screenshot.png

Ensure screenshot captures revert to default root directory
    [Documentation]    Ensure screenshot captures revert to default root directory
    [Setup]    Remove Files    ${OUTPUTDIR}/default-root-screenshot.png
    Capture Page Screenshot    default-root-screenshot.png
    File Should Exist    ${OUTPUTDIR}/default-root-screenshot.png

Capture page screenshot with unique index
    [Setup]    Remove Directory    ${OUTPUTDIR}${/}screenshot-and-index    recursive
    ${file1} =    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}other-{index}-name.png
    ${file2} =    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}some-other-name-{index}.png
    ${file3} =    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}other-{index}-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}other-1-name.png
    Should Be Equal    ${file1}    ${OUTPUTDIR}${/}screenshot-and-index${/}other-1-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}some-other-name-1.png
    Should Be Equal    ${file2}    ${OUTPUTDIR}${/}screenshot-and-index${/}some-other-name-1.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}other-2-name.png
    Should Be Equal    ${file3}    ${OUTPUTDIR}${/}screenshot-and-index${/}other-2-name.png

Capturing a page screenshot with two indexes should not cause an error
    ${file} =    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}two-{index}-in-{index}-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}two-1-in-1-name.png
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}screenshot-and-index${/}two-1-in-1-name.png

Capture page screenshot with index formatting
    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}format-{index:06}-name.png
    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}format-{index:06}-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}format-000001-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}format-000002-name.png

Capture page screenshot with escaped braces
    ${file} =    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}brackets-{{index}}-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}brackets-{index}-name.png
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}screenshot-and-index${/}brackets-{index}-name.png
    ${file} =    Capture Page Screenshot    ${OUTPUTDIR}${/}screenshot-and-index${/}brackets-{{index-name.png
    File Should Exist    ${OUTPUTDIR}${/}screenshot-and-index${/}brackets-{index-name.png
