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


# TODO: refactor this to take into account the previous number of files
Set Screenshot Directory As EMBED And Not Specifying Filename Whenever Taking Element Screenshots Makes Screenshots To Be Embedded
    ${previous_count} =    Count Files In Directory    ${OUTPUTDIR}    *.png
    ${previous} =    Set Screenshot Directory    EMBED
    ${path} =    Capture Element Screenshot    id:nothing
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    *.png
    Should Be Equal As Integers    ${count}    ${previous_count}
    [Teardown]    Set Screenshot Directory    ${previous}

# TODO: refactor this to take into account the previous number of files
Set Screenshot Directory As EMBED And Specifying Filename Whenever Taking Element Screenshots Makes Screenshots To Be Saved As Files
    ${previous_count} =    Count Files In Directory    ${OUTPUTDIR}    *.png
    ${previous} =    Set Screenshot Directory    EMBED
    ${path} =    Capture Element Screenshot    id:nothing    custom-element-screenshot.png
    File Should Exist    ${OUTPUTDIR}/custom-element-screenshot.png
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    *.png
    Should Be Equal As Integers    ${count}    ${previous_count+1}
    [Teardown]    Set Screenshot Directory    ${previous}

# OK
Capture Element Screenshot And Embed It If Using Specific EMBED As Screenshot Filename, Even If Screenshot Directory Has Been Set
    [Setup]    Remove Directory    ${OUTPUTDIR}/custom-root-elem    recursive
    ${previous} =    Set Screenshot Directory    ${OUTPUTDIR}/custom-root-elem
    ${path} =    Capture Element Screenshot    id:nothing    EMBED
    Should Be Equal    ${path}    EMBED
    Directory Should Not Exist    ${OUTPUTDIR}/custom-root-elem
    [Teardown]    Set Screenshot Directory    ${previous}

# TODO: refactor this to take into account the previous number of files
Capture Element Screenshot And Embed It If Using Specific EMBED As Screenshot Filename, Even If Screenshot Directory Is The Default
    ${previous_count} =    Count Files In Directory    ${OUTPUTDIR}    *.png
    ${previous} =    Set Screenshot Directory    ${OUTPUTDIR}
    ${path} =    Capture Element Screenshot    id:nothing    EMBED
    Should Be Equal    ${path}    EMBED
    ${count} =    Count Files In Directory    ${OUTPUTDIR}    *.png
    Should Be Equal As Integers    ${count}    ${previous_count}
    [Teardown]    Set Screenshot Directory    ${previous}

Capture Element Screenshot When No Browser Is Open
    [Setup]    Close All Browsers
    ${path} =    Capture Element Screenshot    id:nothing
    Should Not Be True    ${path}
    [Teardown]    Open Browser To Start Page