*** Settings ***
Test Setup      Go To Front Page
Default Tags    assertions
Resource        ../resource.robot


*** Test Cases ***
Location Should Be
    [Documentation]  LOG 2:3 Current location is '${FRONT PAGE}'.
    Location Should Be  ${FRONT PAGE}
    Run Keyword And Expect Error  Location should have been 'non existing' but was '${FRONT PAGE}'  Location Should Be  non existing

Location Should Contain
    [Documentation]  LOG 2:3 Current location contains 'html'.
    Location Should Contain  html
    Run Keyword And Expect Error  Location should have contained 'not a location' but it was '${FRONT PAGE}'.  Location Should Contain  not a location

Title Should Be
    [Documentation]  LOG 2:3 Page title is '(root)/index.html'.
    Title Should Be  (root)/index.html
    Run Keyword And Expect Error  Title should have been 'not a title' but was '(root)/index.html'  Title Should Be  not a title

Page Should Contain
    [Documentation]  LOG 2:5 Current page contains text 'needle'. LOG 4.1:10 REGEXP: (?i)<html .*</html>
    Page Should Contain  needle
    Page Should Contain  This is the haystack
    Run Keyword And Expect Error  Page should have contained text 'non existing text' but did not  Page Should Contain  non existing text

Page Should Contain With Custom Log Level
    [Documentation]  LOG 2.1:10 DEBUG REGEXP: (?i)<html .*</html>
    Run Keyword And Expect Error  Page should have contained text 'non existing text' but did not  Page Should Contain  non existing text  DEBUG

Page Should Contain With Disabling Source Logging
    [Documentation]  LOG 3:2 NONE
    Set Log Level  INFO
    Run Keyword And Expect Error  Page should have contained text 'non existing text' but did not  Page Should Contain  non existing text  loglevel=NONE
    [Teardown]  Set Log Level  DEBUG

Page Should Contain With Frames
    [Setup]  Go To Page "frames/frameset.html"
    Page Should Contain  You're looking at right.

Page Should Not Contain
    [Documentation]  LOG 2:8 Current page does not contain text 'non existing text'. LOG 3.1:7 REGEXP: (?i)<html .*</html>
    Page Should Not Contain  non existing text
    Run Keyword And Expect Error  Page should not have contained text 'needle'  Page Should Not Contain  needle

Page Should Not Contain With Custom Log Level
    [Documentation]  LOG 2.1:7 DEBUG REGEXP: (?i)<html .*</html>
    Run Keyword And Expect Error  Page should not have contained text 'needle'  Page Should Not Contain  needle  DEBUG

Page Should Not Contain With Disabling Source Logging
    [Documentation]  LOG 3:2 NONE
    Set Log Level  INFO
    Run Keyword And Expect Error  Page should not have contained text 'needle'  Page Should Not Contain  needle  loglevel=NONE
    [Teardown]  Set Log Level  DEBUG

Page Should Contain Element
    Page Should Contain Element  some_id
    Run Keyword And Expect Error  Page should have contained element 'non-existent' but did not  Page Should Contain Element  non-existent

Page Should Contain Element With Custom Message
    Run Keyword And Expect Error  Custom error message  Page Should Contain Element  invalid  Custom error message

Page Should Contain Element With Disabling Source Logging
    [Documentation]  LOG 3:2 NONE
    Set Log Level  INFO
    Run Keyword And Expect Error  Page should have contained element 'non-existent' but did not  Page Should Contain Element  non-existent  loglevel=NONE
    [Teardown]  Set Log Level  DEBUG

Page Should Not Contain Element
    Page Should Not Contain Element  non-existent
    Run Keyword And Expect Error  Page should not have contained element 'some_id'  Page Should Not Contain Element  some_id

Page Should Not Contain Element With Disabling Source Logging
    [Documentation]  LOG 3:2 NONE
    Set Log Level  INFO
    Run Keyword And Expect Error  Page should not have contained element 'some_id'  Page Should Not Contain Element  some_id  loglevel=NONE
    [Teardown]  Set Log Level  DEBUG

Element Should Contain
    Element Should Contain  some_id  This text is inside an identified element
    Run Keyword And Expect Error  Element 'some_id' should have contained text 'non existing text' but its text was 'This text is inside an identified element'.  Element Should Contain  some_id  non existing text
    Run Keyword And Expect Error  ValueError: Element locator 'missing_id' did not match any elements.  Element Should Contain  missing_id  This should report missing element.

Element Should Not Contain
    Element Should Not Contain  some_id  This text is not inside an identified element
    Element Should Not Contain  some_id  elementypo
    Run Keyword And Expect Error  Element 'some_id' should not contain text 'This text is inside an identified element' but it did.  Element Should Not Contain  some_id  This text is inside an identified element
    Run Keyword And Expect Error  ValueError: Element locator 'missing_id' did not match any elements.  Element Should Not Contain  missing_id  This should report missing element.

Element Text Should Be
    Element Text Should Be  some_id  This text is inside an identified element
    Run Keyword And Expect Error  The text of element 'some_id' should have been 'inside' but in fact it was 'This text is inside an identified element'.  Element Text Should Be  some_id  inside

Get Text
    ${str} =  Get Text  some_id
    Should Match  ${str}  This text is inside an identified element
    Run Keyword And Expect Error  ValueError: Element locator 'missing_id' did not match any elements.  Get Text  missing_id

Element Should Be Visible
    [Setup]  Go To Page "visibility.html"
    Element Should Be Visible  i_am_visible
    Run Keyword And Expect Error  The element 'i_am_hidden' should be visible, but it is not.  Element Should Be Visible  i_am_hidden

Element Should Not Be Visible
    [Setup]  Go To Page "visibility.html"
    Element Should Not Be Visible  i_am_hidden
    Run Keyword And Expect Error  The element 'i_am_visible' should not be visible, but it is.  Element Should Not Be Visible  i_am_visible

Page Should Contain Checkbox
    [Documentation]  LOG 2:5 Current page contains checkbox 'can_send_email'.
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Contain Checkbox  can_send_email
    Page Should Contain Checkbox  xpath=//input[@type='checkbox' and @name='can_send_sms']
    Run Keyword And Expect Error  Page should have contained checkbox 'non-existing' but did not  Page Should Contain Checkbox  non-existing

Page Should Not Contain Checkbox
    [Documentation]  LOG 2:5 Current page does not contain checkbox 'non-existing'.
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Not Contain Checkbox  non-existing
    Run Keyword And Expect Error  Page should not have contained checkbox 'can_send_email'  Page Should Not Contain Checkbox  can_send_email

Page Should Contain Radio Button
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Contain Radio Button  sex
    Page Should Contain Radio Button  xpath=//input[@type="radio" and @value="male"]
    Run Keyword And Expect Error  Page should have contained radio button 'non-existing' but did not  Page Should Contain Radio Button  non-existing

Page Should Not Contain Radio Button
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Not Contain Radio Button  non-existing
    Run Keyword And Expect Error  Page should not have contained radio button 'sex'  Page Should Not Contain Radio Button  sex

Page Should Contain Image
    [Setup]  Go To Page "links.html"
    Page Should contain Image  image.jpg
    Run Keyword And Expect Error  Page should have contained image 'non-existent' but did not  Page Should contain Image  non-existent

Page Should Not Contain Image
    [Setup]  Go To Page "links.html"
    Page Should not contain Image  non-existent
    Run Keyword And Expect Error  Page should not have contained image 'image.jpg'  Page Should not contain Image  image.jpg

Page Should Contain Link
    [Setup]  Go To Page "links.html"
    Page Should contain link  Relative
    Page Should contain link  sub/index.html
    Run Keyword And Expect Error  Page should have contained link 'non-existent' but did not  Page Should contain link  non-existent

Page Should Not Contain Link
    [Setup]  Go To Page "links.html"
    Page Should not contain link  non-existent
    Run Keyword And Expect Error  Page should not have contained link 'Relative'  Page Should not contain link  Relative

Page Should Contain List
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page should Contain List  possible_channels
    Run Keyword And Expect Error  Page should have contained list 'non-existing' but did not  Page Should Contain List  non-existing

Page Should Not Contain List
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Not Contain List  non-existing
    Run Keyword And Expect Error  Page should not have contained list 'possible_channels'  Page Should Not Contain List  possible_channels

Page Should Contain TextField
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Contain Text Field  name
    Page Should Contain Text Field  xpath=//input[@type='text' and @name='email']
    Run Keyword And Expect Error  Page should have contained text field 'non-existing' but did not  Page Should Contain Text Field  non-existing

Page Should Not Contain Text Field
    [Setup]  Go To Page "forms/prefilled_email_form.html"
    Page Should Not Contain Text Field  non-existing
    Run Keyword And Expect Error  Page should not have contained text field 'name'  Page Should Not Contain Text Field  name

TextField Should Contain
    [Documentation]  LOG 2:7 Text field 'name' contains text ''.
    [Setup]  Go To Page "forms/email_form.html"
    TextField Should contain  name  ${EMPTY}
    Input Text  name  my name
    TextField Should contain  name  my name
    Run Keyword And Expect Error  Text field 'name' should have contained text 'non-existing' but it contained 'my name'  TextField Should contain  name  non-existing

TextField Value Should Be
    [Documentation]  LOG 2:7 Content of text field 'name' is ''.
    [Setup]  Go To Page "forms/email_form.html"
    textfield Value Should Be  name  ${EMPTY}
    Input Text  name  my name
    textfield Value Should Be  name  my name
    Run Keyword And Expect Error  Value of text field 'name' should have been 'non-existing' but was 'my name'  textfield Value Should Be  name  non-existing
    Clear Element Text  name
    Textfield Value Should Be  name  ${EMPTY}

TextArea Should Contain
    [Setup]  Go To Page "forms/email_form.html"
    TextArea Should Contain  comment  ${EMPTY}
    Input Text  comment  This is a comment.
    Run Keyword And Expect Error
    ...  Text field 'comment' should have contained text 'Hello World!' but it contained 'This is a comment.'
    ...  TextArea Should Contain  comment  Hello World!

TextArea Value Should Be
    [Setup]  Go To Page "forms/email_form.html"
    TextArea Value Should Be  comment  ${EMPTY}
    Input Text  comment  This is a comment.
    Run Keyword And Expect Error
    ...  Text field 'comment' should have contained text 'Hello World!' but it contained 'This is a comment.'
    ...  TextArea Value Should Be  comment  Hello World!
    Clear Element Text  comment
    TextArea Value Should Be  comment  ${EMPTY}

Page Should Contain Button
    [Setup]  Go To Page "forms/buttons.html"
    Page Should Contain Button  button
    Page Should Contain Button  Sisään
    Page Should Contain Button  Get In
    Page Should Contain Button  xpath=//button[@type="submit"]
    Page Should Contain Button  Ulos
    Page Should Contain Button  xpath=//input[@type="submit"]
    Page Should Contain Button  Act!
    Page Should Contain Button  xpath=//input[@type="button"]
    Run Keyword And Expect Error  Page should have contained button 'non-existing' but did not  Page Should Contain Button  non-existing

Page Should Not Contain Button In Button Tag
    [Setup]  Go To Page "forms/buttons.html"
    Page Should Not Contain Button  invalid
    Run Keyword And Expect Error  Page should not have contained button 'button'  Page Should Not Contain Button  button

Page Should Not Contain Button In Input Tag
    [Setup]  Go To Page "forms/buttons.html"
    Page Should Not Contain Button  invalid
    Run Keyword And Expect Error  Page should not have contained input 'Act!'  Page Should Not Contain Button  Act!

Get All Links
    [Setup]  Go To Page "links.html"
    ${links}=  Get All Links
    Length Should Be  ${links}  19
    List Should Contain Value  ${links}  bold_id

Xpath Should Match X Times
    [Setup]  Go To Page "forms/login.html"
    Xpath Should Match X Times  //input[@type="text"]  1
    Xpath Should Match X Times  //input[@type="text"]  ${1}
    Run Keyword And Expect Error  Xpath //input[@type="text"] should have matched 2 times but matched 1 times  Xpath Should Match X Times  //input[@type="text"]  2

Locator Should Match X Times
    [Setup]  Go To Page "links.html"
    Locator Should Match X Times  link=Link  2
    Locator Should Match X Times  link=Missing Link  0
