*** Variables ***
${SERVER}=                  localhost:7000
${BROWSER}=                 Chrome
${REMOTE_URL}=              ${NONE}
${DESIRED_CAPABILITIES}=    ${NONE}
${ROOT}=                    http://${SERVER}/html
${FRONT_PAGE}=              ${ROOT}/

*** Keyword ***

Go To Page "${relative url}"
    [Documentation]    Goes to page
    Go To    ${ROOT}/${relative url}

