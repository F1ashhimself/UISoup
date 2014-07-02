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
from .. import TooSaltyUISoupException


class MacMouse(IMouse):

    LEFT_BUTTON = u'b1c'
    RIGHT_BUTTON = u'b3c'
    SUPPORTED_NAMES = [LEFT_BUTTON, RIGHT_BUTTON]

    _LEFT_BUTTON_CODES = [
        CG.kCGEventLeftMouseDown,
        CG.kCGEventLeftMouseDragged,
        CG.kCGEventLeftMouseUp]
    _RIGHT_BUTTON_CODES = [
        CG.kCGEventRightMouseDown,
        CG.kCGEventRightMouseDragged,
        CG.kCGEventRightMouseUp]

    def _verify_xy(self, x, y):
        """
        Verifies that x and y is instance of int otherwise raises exception.

        Arguments:
            - x: x variable.
            - y: y variable.

        Returns:
            - None
        """

        if not isinstance(x, int) or not isinstance(y, int):
            raise TooSaltyUISoupException(
                'x and y arguments should hold int coordinates.')

    def _verify_button_name(self, button_name):
        """
        Verifies that button name is supported otherwise raises exception.

        Arguments:
            - button_name: string, button name.

        Returns:
            - None
        """

        if not button_name in self.SUPPORTED_NAMES:
            raise TooSaltyUISoupException(
                'Button name should be one of supported %s.' %
                repr(self.SUPPORTED_NAMES))

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

    def move(self, x, y):
        self._verify_xy(x, y)

        self._do_event(CG.kCGEventMouseMoved, x, y)

    def drag(self, x1, y1, x2, y2, smooth=True):
        self._verify_xy(x1, y1)
        self._verify_xy(x2, y2)

        for i in xrange(100):
            x = x1 + (x2 - x1) * (i + 1) / 100.0
            y = y1 + (y2 - y1) * (i + 1) / 100.0
            smooth and sleep(.01)
            self._do_event(CG.kCGEventLeftMouseDragged, x, y)

    def press_button(self, x, y, button_name=LEFT_BUTTON):
        self._verify_xy(x, y)
        self._verify_button_name(button_name)

        event_codes = self._compose_mouse_event_chain(
            button_name, press=True, release=False)
        self._do_events(event_codes, x, y)

    def release_button(self, button_name=LEFT_BUTTON):
        self._verify_button_name(button_name)

        event_codes = self._compose_mouse_event_chain(
            button_name, press=False, release=True)
        self._do_events(event_codes, 0, 0)

    def click(self, x, y, button_name=LEFT_BUTTON):
        self._verify_xy(x, y)
        self._verify_button_name(button_name)

        event_codes = self._compose_mouse_event_chain(
            button_name, press=True, release=True)
        self._do_events(event_codes, x, y)

    def double_click(self, x, y, button_name=LEFT_BUTTON):
        self._verify_xy(x, y)
        self._verify_button_name(button_name)

        self.click(x, y, button_name)
        self.click(x, y, button_name)

    def get_position(self):
        position = CG.CGEventGetLocation(CG.CGEventCreate(None))
        return int(position.x), int(position.y)
