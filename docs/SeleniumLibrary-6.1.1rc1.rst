========================
SeleniumLibrary 6.1.1rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.1.1rc1 is a hotfix release with
one bug fix - the incompatablitilty with Selenium v4.10.0+. More information is given below.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.1.1rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.1.1rc1 was released on Tuesday August 1, 2023. SeleniumLibrary supports
Python 3.7+, Selenium 4.0+ and Robot Framework 4.1.3 or higher.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Update SeleniumLibrary to be compatable with Selenium v4.10.0 (`#1836`_, rc 1)

  Selenium v4.10.0 removed code that was labeled as deprected which we did not catch before the release.
  As such it broke code particular around how the Open Browser keyword calls into selenium. This release is
  a targeted change to resolve that conflict. In particular if one is using a few particular arguments with the
  `Open Browser` keyword then it is recommended you verify you get the same results as before. Some of these
  you *should not* need to make any changes as we make those internally. But others we completely removed and
  you with need to update to get the same functionality. Let me walk through those argument now ..

  If you use the `service_log_path` and/or `executable_path` argument, these are now passed different to the
  webdriver creation. We have strong confidence this was done properly but still want to be transparent a change
  was made there. If you find something amiss please open a support ticket.

  If you use Firefox and the `ff_profile_dir` argument, this is now attached first to the `options` structure and
  passed along to the webdriver creation via options. Again for most users you should not see any issues. If, by
  chance, you are already setting the profile via options (ie ``Open Browser	None	Firefox	options=profile=/path/to/profile/dir``)
  *and* through the `ff_profile_dir` then you will get unexpected operation. I suspect the ff_profile_dir will
  overwride the other; but that is just a guess. Don't try to set it in two places at once. I recognize the change of
  profile into the options strucutre complicates the argumrnt structure here (for example what is you want to pass a
  profile object?). It is not my intention nor do I even attempt to address that here. If you do use firefox profiles
  and have some though on how we can improve this, please reach out.

  If you use `desired_capabilities` they are deprecated and removed completey by Selenium. SeleniumLibrary jsut ignores
  that you passed them in. We will, most likely in the next release jsut remove that argument, but I wanted to ease you
  into this as best as I could. This is not the place for a tutorial on what has been the ay to do this but you can find
  plenty about that on either Selenium Grid documentation or vendors like SauceLabs or BrowserStack.

  Finally if you do do anything beyond the basic ``Open Browser  someUrl  someBrowser`` it would be worthwhile that with
  this release you get similar expected results as with the previos 6.1.0 release. If you see some browser configuration
  settings that are not and can prove this release has something in error please raise a ticket.
  
Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1836`_
      - bug
      - critical
      - Update SeleniumLibrary to be compatable with Selenium v4.10.0
      - rc�1

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.1>`__.

.. _#1836: https://github.com/robotframework/SeleniumLibrary/issues/1836
