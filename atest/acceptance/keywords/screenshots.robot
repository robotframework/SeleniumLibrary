*** Settings ***
Documentation     Tests screenshots
Suite Setup       Go To Page "links.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Capture page screenshot to default location
    [Documentation]
    ...    LOG 2:4 </td></tr><tr><td colspan="3"><a href="selenium-screenshot-1.png"><img src="selenium-screenshot-1.png" width="800px"></a>
    ...    LOG 8:4 </td></tr><tr><td colspan="3"><a href="selenium-screenshot-2.png"><img src="selenium-screenshot-2.png" width="800px"></a>
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
    [Setup]    Remove Files    ${OUTPUTDIR}/custom-screenshot.png
    Capture Page Screenshot    custom-screenshot.png
    File Should Exist    ${OUTPUTDIR}/custom-screenshot.png

Capture page screenshot to custom directory
    [Setup]    Remove Files    ${TEMPDIR}/seleniumlibrary-screenshot-test.png
    Capture Page Screenshot    ${TEMPDIR}/seleniumlibrary-screenshot-test.png
    File Should Exist    ${TEMPDIR}/seleniumlibrary-screenshot-test.png

Capture page screenshot to non-existing directory
    [Setup]    Remove Directory    ${OUTPUTDIR}/screenshot    recursive
    Capture Page Screenshot    screenshot/test-screenshot.png
    File Should Exist    ${OUTPUTDIR}/screenshot/test-screenshot.png

Set Screenshot Directory
    [Setup]    Remove Directory    ${OUTPUTDIR}/custom-root    recursive
    ${previous} =    Set Screenshot Directory    ${OUTPUTDIR}/custom-root
    ${file} =    Capture Page Screenshot    custom-root-screenshot.png
    File Should Exist    ${OUTPUTDIR}/custom-root/custom-root-screenshot.png
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}custom-root${/}custom-root-screenshot.png
    [Teardown]    Set Screenshot Directory    ${previous}

Set Screenshot Directory set back to previous value
    [Documentation]    The directory is actually set already by previous test.
    [Setup]    Remove Files    ${OUTPUTDIR}/default-root-screenshot.png
    Capture Page Screenshot    default-root-screenshot.png
    File Should Exist    ${OUTPUTDIR}/default-root-screenshot.png

Capture page screenshot with unique index
    [Setup]    Remove Directory    ${OUTPUTDIR}/screenshot-and-index    recursive
    ${file1} =    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/other-{index}-name.png
    ${file2} =    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/some-other-name-{index}.png
    ${file3} =    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/other-{index}-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/other-1-name.png
    Should Be Equal    ${file1}    ${OUTPUTDIR}${/}screenshot-and-index${/}other-1-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/some-other-name-1.png
    Should Be Equal    ${file2}    ${OUTPUTDIR}${/}screenshot-and-index${/}some-other-name-1.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/other-2-name.png
    Should Be Equal    ${file3}    ${OUTPUTDIR}${/}screenshot-and-index${/}other-2-name.png

Capturing a page screenshot with two indexes should not cause an error
    ${file} =    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/two-{index}-in-{index}-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/two-1-in-1-name.png
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}screenshot-and-index${/}two-1-in-1-name.png

Capture page screenshot with index formatting
    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/format-{index:06}-name.png
    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/format-{index:06}-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/format-000001-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/format-000002-name.png

Capture page screenshot with escaped braces
    ${file} =    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/brackets-{{index}}-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/brackets-{index}-name.png
    Should Be Equal    ${file}    ${OUTPUTDIR}${/}screenshot-and-index${/}brackets-{index}-name.png
    ${file} =    Capture Page Screenshot    ${OUTPUTDIR}/screenshot-and-index/brackets-{{index-name.png
    File Should Exist    ${OUTPUTDIR}/screenshot-and-index/brackets-{index-name.png

Capture page screenshot computed name is unique
    [Setup]    Run Keywords
    ...  Remove files  ${OUTPUTDIR}/unique-screenshot-*.png
    ...  AND  Touch    ${OUTPUTDIR}/unique-screenshot-1.png
    ...  AND  Touch    ${OUTPUTDIR}/unique-screenshot-2.png
    ...  # unique-screenshot-3 is purposely left out
    ...  AND  Touch    ${OUTPUTDIR}/unique-screenshot-4.png
    # we expect this to be screenshot 3
    ${expected}=    Normalize Path    ${OUTPUTDIR}/unique-screenshot-3.png
    ${actual}=    Capture page screenshot  ${OUTPUTDIR}/unique-screenshot-{index}.png
    Should be equal    ${actual}    ${expected}    values=False
    ...  msg=Expected screenshot to be named '${expected}' but it was '${actual}'
    File Should Exist    ${expected}
    # since screenshot 4 exists, we expect this to be screenshot 5.
    ${expected}=    Normalize Path    ${OUTPUTDIR}/unique-screenshot-5.png
    ${actual}=    Capture page screenshot  ${OUTPUTDIR}/unique-screenshot-{index}.png
    Should be equal  ${actual}  ${expected}  values=False
    ...  msg=Expected screenshot to be named '${expected}' but it was '${actual}'
    File Should Exist    ${expected}

Capture page screenshot advanced formatting name is unique
    [Setup]    Run Keywords
    ...  Remove files  ${OUTPUTDIR}/advanced-screenshot-*.png
    ...  AND  Touch    ${OUTPUTDIR}/advanced-screenshot-002.png
    ...  AND  Touch    ${OUTPUTDIR}/advanced-screenshot-003.png
    ...  # advanced-screenshot-4 is purposely left out
    ...  AND  Touch    ${OUTPUTDIR}/advanced-screenshot-005.png
    # this should be screenshot 1, since it doesn't exist
    ${expected}=    Normalize Path    ${OUTPUTDIR}/advanced-screenshot-001.png
    ${actual}=    Capture page screenshot  ${OUTPUTDIR}/advanced-screenshot-{index:03}.png
    Should be equal  ${actual}  ${expected}  values=False
    ...  msg=Expected screenshot to be named '${expected}' but it was '${actual}'
    File Should Exist    ${expected}
    # since screenshot 1, 2, and 3 exists, the next should be screenshot 4.
    ${expected}=    Normalize Path    ${OUTPUTDIR}/advanced-screenshot-004.png
    ${actual}=    Capture page screenshot  ${OUTPUTDIR}/advanced-screenshot-{index:03}.png
    Should be equal    ${actual}    ${expected}    values=False
    ...  msg=Expected screenshot to be named '${expected}' but it was '${actual}'
    File Should Exist    ${expected}

Capture page screenshot explicit name will overwrite
    [Setup]    Run Keywords
    ...  Remove files  ${OUTPUTDIR}/explicit-screenshot-*.png
    ...  AND  Touch  ${OUTPUTDIR}/explicit-screenshot-1.png
    # make sure we are starting out with a single file in the output directory
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    explicit-screenshot-*.png
    Should be equal as numbers  ${count}  1  values=False
    ...  msg=Expected to find one screenshot file, found ${count}
    # Give an explicit filename that doesn't include the counter placeholder {index}
    Capture page screenshot    ${OUTPUTDIR}/explicit-screenshot-1.png
    # we expect the above to overwrite the existing file
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    explicit-screenshot-*.png
    Should be equal as numbers  ${count}  1  values=False
    ...  msg=Expected to find one screenshot file, found ${count}
    File Should Exist    ${OUTPUTDIR}/explicit-screenshot-1.png

Capture page screenshot with closed browser
    [Documentation]    LOG 2:1 Cannot capture screenshot because no browser is open.
    [Setup]    Close All Browsers
    Capture Page Screenshot
    [Teardown]    Open Browser To Start Page

Set screenshot directory when importing
    [Setup]    Remove Files    ${TEMPDIR}/selenium-screenshot-*.png
    Import Library    SeleniumLibrary    screenshot_root_directory=${TEMPDIR}    WITH NAME    SL2
    Set Library Search Order    SL2
    Open Browser To Start Page
    Capture Page Screenshot
    File Should Exist    ${TEMPDIR}/selenium-screenshot-1.png
    Set Screenshot Directory    ${OUTPUTDIR}/screenshots
    Capture Page Screenshot    custom-name-{index}.png
    File Should Exist    ${OUTPUTDIR}/screenshots/custom-name-1.png
    [Teardown]    Close Browser
