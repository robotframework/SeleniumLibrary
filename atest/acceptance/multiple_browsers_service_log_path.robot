*** Settings ***
Suite Teardown    Close All Browsers
Resource          resource.robot

*** Test Cases ***
First Browser With Service Log Path
    [Documentation]
    ...    LOG 2:2 INFO STARTS: Browser driver log file created to:
    [Setup]    OperatingSystem.Remove Files    ${OUTPUT DIR}/${BROWSER}.log
    Open Browser    ${FRONT PAGE}  ${BROWSER}    service_log_path=${BROWSER}.log
    OperatingSystem.File Should Not Be Empty     ${OUTPUT DIR}/${BROWSER}.log

Second Browser With Service Log Path And Index
    [Setup]    OperatingSystem.Remove Files    ${OUTPUT DIR}/${BROWSER}-1.log
    Open Browser    ${FRONT PAGE}  ${BROWSER}    service_log_path=${BROWSER}-{index}.log
    OperatingSystem.File Should Not Be Empty     ${OUTPUT DIR}/${BROWSER}-1.log

Third Browser With Service Log Path And Index Should Not Overwrite
    [Setup]    OperatingSystem.Remove Files    ${OUTPUT DIR}/${BROWSER}-2.log
    Open Browser    ${FRONT PAGE}  ${BROWSER}    service_log_path=${BROWSER}-{index}.log
    OperatingSystem.File Should Not Be Empty     ${OUTPUT DIR}/${BROWSER}-2.log

Fourth Browser With Service Log Path In Subfolder
    [Setup]    OperatingSystem.Remove Files    ${OUTPUT DIR}/a_folder/${BROWSER}-1.log
    Open Browser    ${FRONT PAGE}  ${BROWSER}    service_log_path=a_folder/${BROWSER}-{index}.log
    OperatingSystem.File Should Not Be Empty     ${OUTPUT DIR}/a_folder/${BROWSER}-1.log
