*** Settings ***
Documentation     Tests asynchronous javascript
Suite Teardown    Set Selenium Timeout    5 seconds
Test Setup        Go To Page "javascript/dynamic_content.html"
Resource          ../resource.robot

*** Test Cases ***
Should Not Timeout If Callback Invoked Immediately
    [Documentation]     Should Not Timeout If Callback Invoked Immediately
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1](123);
    Should Be Equal    ${result}    ${123}

Should Be Able To Return Javascript Primitives From Async Scripts Neither None Nor Undefined
    [Documentation]     Should Be Able To Return Javascript Primitives From Async Scripts
    ...    Neither None Nor Undefined
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1](123);
    Should Be Equal    ${result}    ${123}
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1]('abc');
    Should Be Equal    ${result}    abc
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1](false);
    Should Be Equal    ${result}    ${false}
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1](true);
    Should Be Equal    ${result}    ${true}

Should Be Able To Return Javascript Primitives From Async Scripts Null And Undefined
    [Documentation]     Should Be Able To Return Javascript Primitives From Async Scripts
    ...    Null And Undefined
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1](null);
    Should Be Equal    ${result}    ${None}
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1]();
    Should Be Equal    ${result}    ${None}

Should Be Able To Return An Array Literal From An Async Script
    [Documentation]     Should Be Able To Return An Array Literal From An Async Script
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1]([]);
    Should Not Be Equal    ${result}    ${None}
    Length Should Be    ${result}    0

Should Be Able To Return An Array Object From An Async Script
    [Documentation]     Should Be Able To Return An Array Object From An Async Script
    ${result} =    Execute Async Javascript    arguments[arguments.length - 1](new Array());
    Should Not Be Equal    ${result}    ${None}
    Length Should Be    ${result}    0

Should Be Able To Return Arrays Of Primitives From Async Scripts
    [Documentation]     Should Be Able To Return Arrays Of Primitives From Async Scripts
    ${result} =    Execute Async Javascript
    ...    arguments[arguments.length - 1]([null, 123, 'abc', true, false]);
    Should Not Be Equal    ${result}    ${None}
    Length Should Be    ${result}    5
    ${value} =    Remove From List    ${result}    -1
    Should Be Equal    ${value}    ${false}
    ${value} =    Remove From List    ${result}    -1
    Should Be Equal    ${value}    ${true}
    ${value} =    Remove From List    ${result}    -1
    Should Be Equal    ${value}    abc
    ${value} =    Remove From List    ${result}    -1
    Should Be Equal    ${value}    ${123}
    ${value} =    Remove From List    ${result}    -1
    Should Be Equal    ${value}    ${None}
    Length Should Be    ${result}    0

Should Timeout If Script Does Not Invoke Callback
    [Documentation]    Should Timeout If Script Does Not Invoke Callback
    Run Keyword And Expect Error    TimeoutException:*    Execute Async Javascript    return 1 + 2;

Should Timeout If Script Does Not Invoke Callback With A Zero Timeout
    [Documentation]    Should Timeout If Script Does Not Invoke Callback With A Zero Timeout
    Run Keyword And Expect Error    TimeoutException:*    Execute Async Javascript
    ...    window.setTimeout(function() {}, 0);

Should Not Timeout If Script Callsback Inside A Zero Timeout
    [Documentation]     Should Not Timeout If Script Callsback Inside A Zero Timeout
    ${result} =    Execute Async Javascript
    ...    var callback = arguments[arguments.length - 1];
    ...    window.setTimeout(function() { callback(123); }, 0)

Should Timeout If Script Does Not Invoke Callback With Long Timeout
    [Documentation]    Should Timeout If Script Does Not Invoke Callback With Long Timeout
    Set Selenium Timeout    0.5 seconds
    Run Keyword And Expect Error    TimeoutException:*    Execute Async Javascript
    ...    var callback = arguments[arguments.length - 1]; window.setTimeout(callback, 1500);

Should Detect Page Loads While Waiting On An Async Script And Return An Error
    [Documentation]     Should Detect Page Loads While Waiting On An Async Script
    ...    And Return An Error
    Set Selenium Timeout    0.5 seconds
    Run Keyword And Expect Error    WebDriverException:*    Execute Async Javascript
    ...    window.location = 'javascript/dynamic';

Should Catch Errors When Executing Initial Script
    [Documentation]    Should Catch Errors When Executing Initial Script
    Run Keyword And Expect Error    WebDriverException:*    Execute Async Javascript
    ...    throw Error('you should catch this!');
    #TODO Implement Selenium asynchronous javascript test
    #Should Be Able To Execute Asynchronous Scripts
    #    # To Do
    #TODO    EdManlove    Add support for arguement passing to selenium javascript calls
    #Should Be Able To Pass Multiple Arguments To Async Scripts
    #    ${result} =    Execute Async Javascript
    #...    arguments[arguments.length - 1](arguments[0] + arguments[1]);    1    2
    #    Should Be Equal    ${result}    ${3}
