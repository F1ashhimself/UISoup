#!/usr/bin/env python

#    Copyright (c) 2014 Max Beloborodko.
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

__author__ = 'f1ashhimself@gmail.com'

import ctypes
import ctypes.wintypes
from time import sleep

from ..interfaces.i_mouse import IMouse
from ..utils.win_utils import WinUtils


class WinMouse(IMouse):
    _MOUSEEVENTF_MOVE = 0x0001  # mouse move
    _MOUSEEVENTF_LEFTDOWN = 0x0002  # left button down
    _MOUSEEVENTF_LEFTUP = 0x0004  # left button up
    _MOUSEEVENTF_RIGHTDOWN = 0x0008  # right button down
    _MOUSEEVENTF_RIGHTUP = 0x0010  # right button up
    _MOUSEEVENTF_MIDDLEDOWN = 0x0020  # middle button down
    _MOUSEEVENTF_MIDDLEUP = 0x0040  # middle button up
    _MOUSEEVENTF_ABSOLUTE = 0x8000  # absolute move
    _MOUSEEVENTF_XDOWN = 0x0080  # X button down
    _MOUSEEVENTF_XUP = 0x0100  # X button up
    _MOUSEEVENTF_WHEEL = 0x0800  # wheel button is rotated
    _MOUSEEVENTF_HWHEEL = 0x01000  # wheel button is tilted

    _SM_CXSCREEN = 0
    _SM_CYSCREEN = 1

    LEFT_BUTTON = u'b1c'
    RIGHT_BUTTON = u'b3c'
    _SUPPORTED_BUTTON_NAMES = [LEFT_BUTTON, RIGHT_BUTTON]

    def _compose_mouse_event(self, name, press=True, release=False):
        """
        Composes mouse event based on button name and action flags.

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

        mouse_event = 0
        if name == self.LEFT_BUTTON:
            if press:
                mouse_event += self._MOUSEEVENTF_LEFTDOWN
            if release:
                mouse_event += self._MOUSEEVENTF_LEFTUP
        if name == self.RIGHT_BUTTON:
            if press:
                mouse_event += self._MOUSEEVENTF_RIGHTDOWN
            if release:
                mouse_event += self._MOUSEEVENTF_RIGHTUP

        return mouse_event

    def _do_event(self, flags, x, y, data, extra_info):
        """
        Generates mouse event fo a special coordinate.

        Arguments:
            - flags: integer value holding flags that describes mouse events to
            trigger. Can be a combination of:
                _MOUSEEVENTF_MOVE = 0x0001 # mouse move
                _MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down
                _MOUSEEVENTF_LEFTUP = 0x0004 # left button up
                _MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down
                _MOUSEEVENTF_RIGHTUP = 0x0010 # right button up
                _MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down
                _MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up
                _MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move
                _MOUSEEVENTF_XDOWN = 0x0080 # X button down
                _MOUSEEVENTF_XUP = 0x0100 # X button up
                _MOUSEEVENTF_WHEEL = 0x0800 # wheel button is rotated
                _MOUSEEVENTF_HWHEEL = 0x01000 # wheel button is tilted
            - x: integer value with x coordinate.
            - y: integer value with y coordinate.
            - data: integer value holding additional event data, for ex.:
              * If flags contains _MOUSEEVENTF_WHEEL, then data specifies the
                amount of wheel movement. A positive value indicates that the
                wheel was rotated forward, away from the user; a negative
                value indicates that the wheel was rotated backward, toward
                the user. One wheel click is defined as WHEEL_DELTA, which is
                120.
              * If flags contains _MOUSEEVENTF_HWHEEL, then data specifies the
                amount of wheel movement. A positive value indicates that the
                wheel was tilted to the right; a negative value indicates that
                the wheel was tilted to the left.
              * If flags contains _MOUSEEVENTF_XDOWN or _MOUSEEVENTF_XUP, then
                data specifies which X buttons were pressed or released. This
                value may be any combination of the following flags.
              * If flags is not _MOUSEEVENTF_WHEEL, _MOUSEEVENTF_XDOWN, or
                _MOUSEEVENTF_XUP, then data should be zero.
            - extra_info: integer value with additional value associated with
            the mouse event.

        Returns:
            - None
        """

        x_metric = ctypes.windll.user32.GetSystemMetrics(self._SM_CXSCREEN)
        y_metric = ctypes.windll.user32.GetSystemMetrics(self._SM_CYSCREEN)
        x_calc = 65536L * x / x_metric + 1
        y_calc = 65536L * y / y_metric + 1
        ctypes.windll.user32.mouse_event(
            flags, x_calc, y_calc, data, extra_info)

    def move(self, x, y, smooth=True):
        WinUtils.verify_xy_coordinates(x, y)

        old_x, old_y = self.get_position()

        for i in xrange(100):
            intermediate_x = old_x + (x - old_x) * (i + 1) / 100.0
            intermediate_y = old_y + (y - old_y) * (i + 1) / 100.0
            smooth and sleep(.01)

            self._do_event(self._MOUSEEVENTF_MOVE + self._MOUSEEVENTF_ABSOLUTE,
                           int(intermediate_x), int(intermediate_y), 0, 0)

    def drag(self, x1, y1, x2, y2, smooth=True):
        WinUtils.verify_xy_coordinates(x1, y1)
        WinUtils.verify_xy_coordinates(x2, y2)

        self.press_button(x1, y1, self.LEFT_BUTTON)
        self.move(x2, y2, smooth=smooth)
        self.release_button(self.LEFT_BUTTON)

    def press_button(self, x, y, button_name=LEFT_BUTTON):
        WinUtils.verify_xy_coordinates(x, y)
        WinUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        self.move(x, y)
        self._do_event(
            self._compose_mouse_event(button_name, press=True, release=False),
            0, 0, 0, 0)

    def release_button(self, button_name=LEFT_BUTTON):
        WinUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        self._do_event(
            self._compose_mouse_event(button_name, press=False, release=True),
            0, 0, 0, 0)

    def click(self, x, y, button_name=LEFT_BUTTON):
        WinUtils.verify_xy_coordinates(x, y)
        WinUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        self.move(x, y)
        self._do_event(
            self._compose_mouse_event(button_name, press=True, release=True),
            0, 0, 0, 0)

    def double_click(self, x, y, button_name=LEFT_BUTTON):
        WinUtils.verify_xy_coordinates(x, y)
        WinUtils.verify_mouse_button_name(button_name,
                                          self._SUPPORTED_BUTTON_NAMES)

        self.move(x, y)
        self._do_event(
            self._compose_mouse_event(button_name, press=True, release=True),
            0, 0, 0, 0)
        self._do_event(
            self._compose_mouse_event(button_name, press=True, release=True),
            0, 0, 0, 0)

    def get_position(self):
        obj_point = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(obj_point))

        return obj_point.x, obj_point.y
