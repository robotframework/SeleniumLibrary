*Setting*
Resource  ../resource.robot
Test Setup  Go To Page "frames/frameset.html"
Test Teardown  UnSelect Frame


*Test Cases*

Frame Should Contain
  Frame Should contain  right  You're looking at right.
  Frame Should Contain  left  Links

Frame Should Contain should also work with iframes
  [setup]  Go To Page "frames/iframes.html"
  Frame Should contain  right  You're looking at right.
  Frame Should Contain  left  Links


Page Should Contain Text Within Frames
  Page Should contain  You're looking at right.
  Page Should Contain  Links

Page Should Contain Text Within Frames should also work with iframes
  [setup]  Go To Page "frames/iframes.html"
  Page Should contain  You're looking at right.
  Page Should Contain  Links


Select And Unselect Frame
  [Documentation]  LOG 2 Selecting frame 'left'.
  Select Frame  left
  Click Link  foo
  Unselect Frame
  Select Frame  right
  Current Frame Contains  You're looking at foo.

Select And Unselect Frame should also work with iframes
  [Documentation]   Selecting frame leftiframe
  [setup]  Go To Page "frames/iframes.html"
  Select Frame  left
  Click Link  foo
  Unselect Frame
  Select Frame  right
  Current Frame Contains  You're looking at foo.

Select Frame with non-unique name attribute
  [Documentation]  Descerning frame 'left' from link 'left'.
  [setup]  Go To Page "frames/poorlynamedframe.html"
  Run Keyword And Expect Error  NoSuchFrameException*  Select Frame  left
  Select Frame  xpath=//frame[@name='left']|//iframe[@name='left']
  Click Link  foo
  Unselect Frame
  Select Frame  right
  Current Frame Contains  You're looking at foo.
