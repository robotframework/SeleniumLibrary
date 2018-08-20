Release Notes
=============

3.2.0
-----
- Added message param to keywords `Location Should Be` and `Location Should Contain` to display custom error message [taniabhullar]
- Added `Element Attribute Value Should Be` verifies element identified by locator contains expected attribute value.. [brian-mathews]
- Added `Get Session Id` keyword to get remote webdriver session id [ilfirinpl]
- Fixed example documentation for custom locator [DanielPBak]

3.1.1
-----
- Added `Element Text Should Not Be` to check a element text is not the argument, you can ignore case with `ignore_case=True` [rubygeek]

3.1.0
-----
- Added a message param to `Title Should Be` to display custom error message [rubygeek]
- Compare text regardless of case in: `Element Should Contain`, `Element Should Not Contain` and `Element Text Should Be` by passing `ignore_case=True`. The default is `False` [rubygeek]

3.0.1
-----
- Hotfix release to for issue #1008.

3.0.0
-----
- Added 'Get Locations' keyword [thaffenden]
- Fix getting window information and switching windows on browsers that do not
  support javascript
- Added 'Get Cookie' keyword [wappowers]
- Added 'expiry' as value that can be set with 'Add Cookie' keyword [wappowers]

1.8.0
-----
- Moved keyword documentation to:
  http://robotframework.org/Selenium2Library/Selenium2Library.html
- Library demo project was removed, users shoud use demo from:
  https://bitbucket.org/robotframework/webdemo
- docutils was removed as installation dependency.
- Edge browser support was added to Open Browser keyword [jfx].
- Unselect From List keyword was updated because selenium 2.53.0 or greater
  raised an exception if item can not be unselected.
- Get Element Size keyword was added [SergiuTudos]
- Alert handling was improved to wait alert be present
- Capture Page Screenshot keyword was enhanced to support custom index definition
  in the filename

1.7.4
-------------------
- Reverted 'Press Keys' because of backwards incompatible changes [zephraph]

1.7.3
-------------------
- Added 'Get WebElement' [zephraph][emanlove]

- Added named keys to 'Press Key' [helioguilherme66]

- Fix an import error that caused a dependence on RF >= 2.8.5
  [zephraph]

- Fixed an issue that caused screenshots to be improperly linked in the logs
  [zephraph]

1.7.2
----------------
- Added an argument called screenshot_root_directory that can be passed into S2L's
  constructor to specify where to store screenshots.
- Added new keyword 'set_screenshot_directory' which can be used to set the output
  of screenshots.
  [zephraph]

- Added new keyword Input Text Into Prompt
- Modified 'get_alert_message' to accept a parameter 'dismiss' (defaults to true) which can be
  used to prevent closing the alert message and instead will just return the alerts text.
  Also created new keyword 'dismiss_alert' to dismiss (default) or confirm the alert without
  reading the text of the alert.
  [KingWarin]

- Added new keyword Input Text Into Prompt
  [boakley][ekasteel]

- Fixed issue that caused tests to fail when selenium > 2.26
  [hgarus]

- Fixed an error where regular functions were not able to be used as a custom locator
  [zephraph]

- Changed all test files to have a '.robot' extension
  [zephraph]

1.7.1 (hotfix)
----------------
- Remove references to GLOBAL_VARIABLES for RF 2.9 compatibility

1.7
----------------
- Added keyword 'List Windows' to return a list of all window handles.
  [divfor]

- Enabled 'Select Window' to return window handle as well as accept it as locator, and
  select new popup window by excluding previous window handles (the strict way) or
  by special locator 'new' (the simplified but less strict way).
  [divfor]

- Added new keyword 'Wait Until Page Does Not Contain'.
  [deiga]

- Fixed ‘NoSuchWindowException' issue. Running keyword 'Select Window' after 'Close Window'
  will trigger this issue if locator has prefix 'name=','title=' or 'url='. Also fixed same
  issue for keywords 'Get Window Ids', 'Get Window Titles' and 'Get Window Names'.
  [divfor]

- Corrected error message in new keyword 'Wait Until Element Is Not
  Visible' to reflect element being visible instead of not visible.
  [joepurdy]

- Stop using private browsing with default Firefox profile.
  [ombre42]

- Added new keyword 'Wait Until Element Is Not Visible'.
  [deiga]

- Added new keyword 'Element Should Not Contain'.
  [molsky]

- Added new keyword 'Wait Until Page Does Not Contain Element'.
  [molsky]

- Added new keywords 'Wait Until Element Contains' and 'Wait Until Element Does Not Contain'
  [molsky]

- Added new locator strategy, scLocator, for finding SmartClient and SmartGWT elements.
  [IlfirinPL]

- Edited acceptance test scripts to automatically make known issues for the currently
  known browser and python version noncritical. Also added a noncritical case to the
  travis config for situations where testing is failing on travis for an unknown reason.
- 'Capture Screenshot' now attempts to create its containing directory if the directory
  specified in the filename does not exist.
- 'Choose File' now fails if the file doesn't exist
- Added new keywords 'Add Location Strategy' and 'Remove Location Strategy'
  [zephraph]

- Added 'Get Window Position' and 'Set Window Position' keywords matching the
  Selenium functionality.
  [ktarasz]

1.6
---
- Added examples to 'Execute Javascript' and 'Execute Async Javascript'
  keyword documentation.
  [ombre42]

- Added instructions to README.rst on how to manually install Selenium2Library.
  [pekkaklarck]

- Fixed issue where the browser failed to properly register if 'Open Browser'
  did not complete.
  [Mika Batsman][elizaleong][emanlove]

- Added support for negative indices for rows and columns in table-related
  keywords.
  [eweitz]

- Added strategy for locating elements by partial link text with locator
  prefix 'partial link'.
  [lina1]

- Added new keyword 'Clear Element Text' for clearing the text of text entry
  elements.
  [emanlove]

- Added new keyword 'Locator Should Match X Times' for validating number of
  times a given locator appears.
  [emanlove]

- Fixed issue where 'Select Window’ with url strategy fails to locate window
  [laulaz]

- Fixed issue where a non-string assigned to window.id caused
  'Select Window' and 'Get Window *' keywords to fail.
  [ombre42]

- Allow using key attributes (default strategy) when the locator contains
  a '=' by using the prefix 'default='. Also make locator prefixes
  space-insensitive.
  [ombre42]

A big thank you to [eweitz] and [HelioGuilherme66] for getting the
continuous integration builds to go green by fixing internal tests.

1.5
---
- Copy Desired Capabilities before modifying to prevent affecting future
  sesions.
  [ombre42]

- Added support for Safari Browser.
  [zmlpjuran]

- Added 'Create Webdriver' to allow greater control of local WebDrivers, such
  as setting a proxy or using Chrome options.
  [ombre42][pekkaklarck][emanlove][j1z0]

- Fixed Mouse Up keyword attempting to click and hold one more time before
  release.
  [myaskevich][emanlove]

- Refixed issue with parsing desired capabilities.
  [cookie314][ymost][emanlove]

- Fixed compatibility with RobotFramework v2.8.1
  [F1ashhimself]

- Modified how internal tests are run and ignore known browser issues.
  [emanlove]

1.4
---
- Added keywords for verifying text entered into textarea elements.
  [stevejefferies][emanlove]

- Fixed bad browser name raising AttributeError.
  [ombre42]

- Raise exception in selecting non-existing item in list. Error handling varies
  between single-select and multi-select lists. See keyword documentation for
  more information.
  [adwu73][emanlove]

- Added 'Get Window Size' and 'Set Window Size' keywords matching the
  Selenium functionality.
  [emanlove][ombre42]

1.3
---
- Updated expected error messages with async javascript tests.
  [emanlove]

- Beautified README.rst.
  [j1z0][emanlove]

- Changed press key test to use Line Feed (\10) instead of
  Carriage Return (\13).
  [emanlove]

- Added new keyword 'Click Element At Coordinates'.
  [aaltat][pierreroth64][ombre42][emanlove]

- Added a "Getting Help" section to README.rst.
  [ombre42][emanlove]

- Added keyword 'Wait Until Element Visible'
  [ombre42]

- Perform check on return value when finding elements. Fixes Issue 65.
  [ombre42]

- Support checking enabled/disabled state of option elements.
  [ekantola]

- Allow desired_capabilities= to be a dictionary.
  [peritus]

- Added Android and iPhone browsers.
  [maddabini]

- Added keyword 'Current Frame Should Not Contain'.
  [adwu73]

1.2
---
- Added PhantomJS as a supported browser type.
  [bmannix]

- Fixed 'Get Selected List Label' under IE7 or IE8.
  [ombre42]

- Added support for jQuery and sizzle selectors.
  [Paul Hicks (tenwit)][peritus][j1z0]

- Added new global variable DEFAULT_HOST to demo server for more easier
  way to bind to other address than 'localhost'.
  [IsNoGood]

- Skip closed browsers when setting Selenium timeout. Fixes #93.
  [ombre42]

1.1
---
- Increased minimum version requirement for Selenium to 2.12.0 within
  setup.py.  This is required due to the change towards using Selenium's
  Select class which was introduced starting in version 2.12.
  [emanlove]

- Use Selenium's Select class within Selenium2Library's "Select *" keywords.
  Optimization of certain "Select *" keywords to increase performance.
  [emanlove] [schminitz]

- Replace maximize current browser window from JS to webdriver.
  [jollychang]

- Verify element is found under 'Get Text' and 'Element Should Contain'
  keywords before returning text or verifing element contains specified text.
  [emanlove]

- Fixed capture page screenshot for RemoteWebDriver.
  [korda]

- Fixed issue with select window under IE. Also addresses issue with Firefox
  when using selenum 2.25.0
  (see https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/4375.
  [adwu73]

- Added iframe support by removing strict filtering for only <frame> elements.
  [emanlove]

- Added the 'get text' keyword to be backwards compatible with the original
  Selenium Library.
  [jouk0]

- Added drag and drop support with two functions `drag and drop  source
  target` and `drag and drop by offset  source  xoffset  yoffset`
  [mamathanag] and [j1z0]

- Added HTMLUnit and HTMLUnitWithJS support.  Just use a line like:
 `Open Browser    [initial page url]    remote_url=[the selenium-server url]    browser=htmlunit`
  [SoCalLongboard]

1.0.1
-----
- Support for Robot Framework 2.7
- Improvements to distribution build script and improved documentation
