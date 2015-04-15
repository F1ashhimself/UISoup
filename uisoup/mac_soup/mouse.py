#!/usr/bin/env python
#
#    Copyright (c) 2014 Oleksandr Iakovenko.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__author__ = 'alex.jakovenko@gmail.com'


from Quartz import CoreGraphics as CG

from time import sleep

from ..interfaces.i_mouse import IMouse
from ..utils.mac_utils import MacUtils


class MacMouse(IMouse):

    LEFT_BUTTON = u'b1c'
    RIGHT_BUTTON = u'b3c'
    _SUPPORTED_BUTTON_NAMES = [LEFT_BUTTON, RIGHT_BUTTON]

    _LEFT_BUTTON_CODES = [
        CG.kCGEventLeftMouseDown,
        CG.kCGEventLeftMouseDragged,
        CG.kCGEventLeftMouseUp]
    _RIGHT_BUTTON_CODES = [
        CG.kCGEventRightMouseDown,
        CG.kCGEventRightMouseDragged,
        CG.kCGEventRightMouseUp]

    def _compose_mouse_event_chain(self, name, press=True, release=False):
        """
        Composes chain of mouse events based on button name and action flags.

        Arguments:
            - name: string value holding mouse button name. Should be one of:
            'b1c' - left button or 'b3c' - right button.
            - press: boolean flag indicating whether event should indicate
            button press.
            - release: boolean flag indicating whether event should indicate
            button release.

        Returns:
            - None
        """

        mouse_event_chain = []
        if name == self.LEFT_BUTTON:
            if press:
                mouse_event_chain.append(CG.kCGEventLeftMouseDown)
            if release:
                mouse_event_chain.append(CG.kCGEventLeftMouseUp)
        if name == self.RIGHT_BUTTON:
            if press:
                mouse_event_chain.append(CG.kCGEventRightMouseDown)
            if release:
                mouse_event_chain.append(CG.kCGEventRightMouseUp)

        return mouse_event_chain

    def _do_event(self, code, x, y):
        """
        Generates mouse event for a special coordinate.

        Arguments:
            - code: integer value holding mouse event code.
            - x: integer value with x coordinate.
            - y: integer value with y coordinate.
        Returns:
            - None
        """

        if code in self._LEFT_BUTTON_CODES:
            button = CG.kCGMouseButtonLeft
        elif code in self._RIGHT_BUTTON_CODES:
            button = CG.kCGMouseButtonRight
        else:
            button = CG.kCGMouseButtonCenter

        CG.CGEventPost(
            CG.kCGHIDEventTap,
            CG.CGEventCreateMouseEvent(None, code, (x, y), button)
        )

    def _do_events(self, codes, x, y):
        """
        Generates a sequence of mouse events for a special coordinate.

        Arguments:
            - codes: list of integer values holding mouse event codes.
            - x: integer value with x coordinate.
            - y: integer value with y coordinate.
        Returns:
            - None
        """

        for code in codes:
            self._do_event(code, x, y)

    def move(self, x, y, smooth=True):
        MacUtils.verify_xy_coordinates(x, y)

        old_x, old_y = self.get_position()

        for i in xrange(100):
            intermediate_x = old_x + (x - old_x) * (i + 1) / 100.0
            intermediate_y = old_y + (y - old_y) * (i + 1) / 100.0
            smooth and sleep(.01)

            self._do_event(CG.kCGEventMouseMoved, int(intermediate_x),
                           int(intermediate_y))

    def drag(self, x1, y1, x2, y2, smooth=True):
        MacUtils.verify_xy_coordinates(x1, y1)
        MacUtils.verify_xy_coordinates(x2, y2)

        self.press_button(x1, y1, self.LEFT_BUTTON)

        for i in xrange(100):
            x = x1 + (x2 - x1) * (i + 1) / 100.0
            y = y1 + (y2 - y1) * (i + 1) / 100.0
            smooth and sleep(.01)
            self._do_event(CG.kCGEventLeftMouseDragged, x, y)

        self.release_button(self.LEFT_BUTTON)

    def press_button(self, x, y, button_name=LEFT_BUTTON):
        MacUtils.verify_xy_coordinates(x, y)
        MacUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        event_codes = self._compose_mouse_event_chain(
            button_name, press=True, release=False)
        self._do_events(event_codes, x, y)

    def release_button(self, button_name=LEFT_BUTTON):
        MacUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        event_codes = self._compose_mouse_event_chain(
            button_name, press=False, release=True)
        self._do_events(event_codes, 0, 0)

    def click(self, x, y, button_name=LEFT_BUTTON):
        MacUtils.verify_xy_coordinates(x, y)
        MacUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        event_codes = self._compose_mouse_event_chain(
            button_name, press=True, release=True)
        self._do_events(event_codes, x, y)

    def double_click(self, x, y, button_name=LEFT_BUTTON):
        MacUtils.verify_xy_coordinates(x, y)
        MacUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        if button_name == self.LEFT_BUTTON:
            button = CG.kCGMouseButtonLeft
            down = CG.kCGEventLeftMouseDown
            up = CG.kCGEventLeftMouseUp
        if button_name == self.RIGHT_BUTTON:
            button = CG.kCGMouseButtonRight
            down = CG.kCGEventRightMouseDown
            up = CG.kCGEventRightMouseUp

        # http://www.codeitive.com/0iJqgkejVj/performing-a-double-click-using-cgeventcreatemouseevent.html
        event = CG.CGEventCreateMouseEvent(None, down, (x, y), button)
        CG.CGEventPost(CG.kCGHIDEventTap, event)
        CG.CGEventSetType(event, up)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

        CG.CGEventSetIntegerValueField(event, CG.kCGMouseEventClickState, 2)

        CG.CGEventSetType(event, down)
        CG.CGEventPost(CG.kCGHIDEventTap, event)
        CG.CGEventSetType(event, up)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

    def get_position(self):
        position = CG.CGEventGetLocation(CG.CGEventCreate(None))
        return int(position.x), int(position.y)
