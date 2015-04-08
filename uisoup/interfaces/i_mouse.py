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

from abc import ABCMeta, abstractmethod, abstractproperty


class IMouse(object):
    """
    Class to simulate mouse activities.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def LEFT_BUTTON(self):
        """
        Constant for left mouse button.
        """

    @abstractproperty
    def RIGHT_BUTTON(self):
        """
        Constant for right mouse button.
        """

    @abstractmethod
    def move(self, x, y, smooth=True):
        """
        Move the mouse to the specified coordinates.

        Arguments:
            - x: integer value with x coordinate.
            - y: integer value with y coordinate.
            - smooth: bool, indicates is it needed to simulate smooth movement.

        Returns:
            - None
        """

    @abstractmethod
    def drag(self, x1, y1, x2, y2, smooth=True):
        """
        Drags the mouse to the specified coordinates.

        Arguments:
            - x1: integer value with x start coordinate.
            - y1: integer value with y start coordinate.
            - x1: integer value with x target coordinate.
            - y1: integer value with y target coordinate.
            - smooth: bool, indicates is it needed to simulate smooth movement.

        Returns:
            - None
        """

    @abstractmethod
    def press_button(self, x, y, button_name=LEFT_BUTTON):
        """
        Presses mouse button as dictated by coordinates and button name.

        Arguments:
            - x: integer value with x coordinate to press mouse at.
            - y: integer value with y coordinate to press mouse at.
            - button_name: string value with mouse button name. Should be one
            of: 'b1c' - left button or 'b3c' - right button.

        Returns:
            - None
        """

    @abstractmethod
    def release_button(self, button_name=LEFT_BUTTON):
        """
        Releases mouse button by button name.

        Arguments:
            - button_name: string value with mouse button name. Should be one
            of: 'b1c' - left button or 'b3c' - right button.

        Returns:
            - None
        """

    @abstractmethod
    def click(self, x, y, button_name=LEFT_BUTTON):
        """
        Clicks as dictated by coordinates and button name.

        Arguments:
            - x: integer value with x coordinate to click at.
            - y: integer value with y coordinate to click at.
            - button_name: string value with mouse button name. Should be one
            of: 'b1c' - left button or 'b3c' - right button.

        Returns:
            - None
        """

    @abstractmethod
    def double_click(self, x, y, button_name=LEFT_BUTTON):
        """
        Double-clicks as dictated by coordinates and button name.

        Arguments:
            - x: integer value with x coordinate to double-click at.
            - y: integer value with y coordinate to double-click at.
            - button_name: string value with mouse button name. Should be one
            of: 'b1c' - left button or 'b3c' - right button.

        Returns:
            - None
        """

    @abstractmethod
    def get_position(self):
        """
        Returns current mouse cursor position.

        Arguments:
            - None

        Returns:
            - tuple of two integers, that holds x and y coordinates of current
            mouse cursor position.
        """
