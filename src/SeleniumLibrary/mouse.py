#  Copyright 2008-2010 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class Mouse(object):

    def simulate_mouse_over(self, locator):
        """Simulates a user hovering a mouse over the element specified by `locator`.
        
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        
        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Over on element '%s'" % locator)
        self._selenium.mouse_over(locator);

    def simulate_mouse_out(self, locator):
        """Simulates a user moving the mouse pointer away from the 
        element specified by `locator`.
        
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        
        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Out on element '%s'" % locator)
        self._selenium.mouse_out(locator)
    
    def simulate_mouse_down(self, locator):
        """Simulates a user pressing the left mouse button (without releasing it yet) on
        the element specified by `locator`.
        
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        
        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Down on element '%s'" % locator)
        self._selenium.mouse_down(locator)
    
    def simulate_mouse_up(self, locator):
        """Simulates the event that occurs when the user releases the mouse button (i.e., stops
        holding the button down) on the element specified by `locator`.
        
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        
        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Up on element '%s'" % locator)
        self._selenium.mouse_up(locator)
