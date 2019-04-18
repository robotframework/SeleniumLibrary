EventFiringWebDriver
====================

This example demonstrates the EventFiringWenDriver support. The MyListener.py
does only log before and after the Selenium API call. But MyListener.py
could make new Selenium API calls or anything else which is possible from the Python.

To run the example, give command::

    robot event_firing_webdriver.robot

From the generated log.html, in the keywords logging, look at logging.
The lines starting "Before " and "After " are from the EventFiringWenDriver.

See `Robot Framework test suite`_  and `EventFiringWebDriver class`_ for further details.

.. _Robot Framework test suite: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/event_firing_webdriver/event_firing_webdriver.robot
.. _EventFiringWebDriver class: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/event_firing_webdriver/MyListener.py
