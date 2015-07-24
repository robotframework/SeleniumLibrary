*** Settings ***
Resource     ../resource.robot
Suite Setup  Go To Page "links.html"


*** Test Cases ***

Capture page screenshot to default location
  [Documentation]  LOG 2:3  REGEXP: </td></tr><tr><td colspan="3"><a href="selenium-screenshot-\\d.png"><img src="selenium-screenshot-\\d.png" width="800px"></a>
  [Setup]  Remove Files  ${OUTPUTDIR}/selenium-screenshot-*.png
  Capture Page Screenshot
  ${count} =  Count Files In Directory  ${OUTPUTDIR}  selenium-screenshot-*.png
  Should Be Equal As Integers  ${count}  1
  Click Link  Relative
  Wait Until Page Contains Element  tag=body
  Capture Page Screenshot
  ${count} =  Count Files In Directory  ${OUTPUTDIR}  selenium-screenshot-*.png
  Should Be Equal As Integers  ${count}  2

Capture page screenshot to custom file
  [Setup]  Remove Files  ${OUTPUTDIR}/custom-screenshot.png
  Capture Page Screenshot  custom-screenshot.png
  File Should Exist  ${OUTPUTDIR}/custom-screenshot.png

Capture page screenshot to custom directory
  [Setup]  Remove Files  ${TEMPDIR}/seleniumlibrary-screenshot-test.png
  Capture Page Screenshot  ${TEMPDIR}/seleniumlibrary-screenshot-test.png
  File Should Exist  ${TEMPDIR}/seleniumlibrary-screenshot-test.png

Capture page screenshot to non-existing directory
  [Setup]  Remove Directory  ${OUTPUTDIR}/screenshot  recursive
  Capture Page Screenshot  screenshot/test-screenshot.png
  File Should Exist  ${OUTPUTDIR}/screenshot/test-screenshot.png

Capture page screenshot to custom root directory
  [Setup]  Remove Directory  ${OUTPUTDIR}/custom-root  recursive
  Set Screenshot Directory  ${OUTPUTDIR}/custom-root
  Capture Page Screenshot  custom-root-screenshot.png
  File Should Exist  ${OUTPUTDIR}/custom-root/custom-root-screenshot.png

Ensure screenshot captures revert to default root directory
  [Setup]  Remove Files  ${OUTPUTDIR}/default-root-screenshot.png
  Capture Page Screenshot  default-root-screenshot.png
  File Should Exist  ${OUTPUTDIR}/default-root-screenshot.png
