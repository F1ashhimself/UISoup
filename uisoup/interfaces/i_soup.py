#!/usr/bin/env python

#    Copyright (c) 2014-2017 Max Beloborodko.
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


class ISoup(object):
    """
    Class to work with UI objects.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def mouse(self):
        """
        Instance of IMouse implementation.
        """

    @abstractproperty
    def keyboard(self):
        """
        Instance of IKeyboard implementation.
        """

    @abstractmethod
    def get_object_by_coordinates(self, x, y):
        """
        Gets object by coordinates.

        :param int x: x coordinate.
        :param int y: y coordinate.
        :rtype: uisoup.interfaces.i_element.IElement
        :return: object that was found by given coordinates.
        """

    @abstractmethod
    def is_window_exists(self, obj_handle):
        """
        Verifies is window exists.

        :param str | int obj_handle: window name (string) or window 
        handler (int) otherwise Desktop Window will be checked.
        :rtype: bool
        :return: True if window exists otherwise False.
        """

    @abstractmethod
    def get_window(self, obj_handle=None):
        """
        Gets window.

        :param str | int obj_handle: window name (string) or window 
        handler (int) otherwise Desktop Window will be checked.
        :rtype: uisoup.interfaces.i_element.IElement
        :return: window object.
        """

    @abstractmethod
    def get_visible_window_list(self):
        """
        Gets list of visible windows.

        :rtype: list[uisoup.interfaces.i_element.IElement]
        :return: list of visible windows.
        """

    @abstractmethod
    def get_visible_object_list(self, window_name):
        """
        Gets list of visible objects for specified window.

        :param str window_name: window name.
        :rtype: list[uisoup.interfaces.i_element.IElement]
        :return: list of visible windows.
        """
