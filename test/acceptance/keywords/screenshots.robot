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

Capture page screenshot to with overwrite false and custom name
  [Setup]  Remove Directory  ${OUTPUTDIR}/screenshot-overwrite  recursive
  Capture Page Screenshot  screenshot-overwrite/some-name.png
  File Should Exist  ${OUTPUTDIR}/screenshot-overwrite/some-name.png
  Capture Page Screenshot  screenshot-overwrite/some-name.png
  File Should Exist  ${OUTPUTDIR}/screenshot-overwrite/some-name-1.png

Capture page screenshot to with overwrite true
  Capture Page Screenshot  overwrite=True
  Capture Page Screenshot  overwrite=True
  File Should Exist  ${OUTPUTDIR}/selenium-screenshot-3.png
  File Should Exist  ${OUTPUTDIR}/selenium-screenshot-4.png
  Capture Page Screenshot  overwrite-filename.png  overwrite=True
  Capture Page Screenshot  overwrite-filename.png  overwrite=True
  File Should Exist  ${OUTPUTDIR}/overwrite-filename.png
  File Should Not Exist  ${OUTPUTDIR}/overwrite-filename-1.png

Capture page screenshot with complex names
  Capture Page Screenshot  many.png.and.dots.png
  Capture Page Screenshot  many.png.and.dots.png
  File Should Exist  ${OUTPUTDIR}/many.png.and.dots.png
  File Should Exist  ${OUTPUTDIR}/many.png.and.dots-1.png
  Capture Page Screenshot  no-png-in-end
  Capture Page Screenshot  no-png-in-end
  File Should Exist  ${OUTPUTDIR}/no-png-in-end
  File Should Exist  ${OUTPUTDIR}/no-png-in-end-1
