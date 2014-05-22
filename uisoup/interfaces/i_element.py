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


class IElement(object):
    """
    Class that describes UI object.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, obj_handle, i_object_id):
        """
        Constructor.

        Arguments:
            - obj_handle: instance of i_accessible or window handle.
            - i_object_id: int, object id.
        """

    @abstractmethod
    def click(self, x_offset=None, y_offset=None):
        """
        Clicks by left mouse button on this object.

        Arguments:
            - x_offset: int, x offset, if not defined half of element width
            will be used.
            - y_offset: int, y offset, if not defined half of element height
            will be used.

        Returns:
            - None
        """

    @abstractmethod
    def right_click(self, x_offset=None, y_offset=None):
        """
        Clicks by right mouse button on this object.

        Arguments:
            - x_offset: int, x offset, if not defined half of element width
            will be used.
            - y_offset: int, y offset, if not defined half of element height
            will be used.

        Returns:
            - None
        """

    @abstractmethod
    def double_click(self, x_offset=None, y_offset=None):
        """
        Double clicks by left mouse button on this object.

        Arguments:
            - x_offset: int, x offset, if not defined half of element width
            will be used.
            - y_offset: int, y offset, if not defined half of element height
            will be used.

        Returns:
            - None
        """

    @abstractmethod
    def drag_to(self, x, y, x_offset=None, y_offset=None, smooth=True):
        """
        Drags this object to coordinates.

        Arguments:
            - x: int, x coordinate.
            - y: int, y coordinate.
            - x_offset: int, x offset, if not defined half of element width
            will be used.
            - y_offset: int, y offset, if not defined half of element height
            will be used.
            - smooth: bool, indicates is it needed to simulate smooth movement.

        Returns:
            - None
        """

    @abstractmethod
    def check_state(self, state):
        """
        Checks object state.

        Arguments:
            - state: int, state flag.

        Returns:
            - bool that describes state.
        """

    @abstractproperty
    def hwnd(self):
        """
        Indicates window handle.
        """

    @abstractproperty
    def proc_id(self):
        """
        Indicates process id.
        """

    @abstractproperty
    def is_top_level_window(self):
        """
        Indicates is top level window or not.
        """

    @abstractproperty
    def is_selected(self):
        """
        Indicates selected state.
        """

    @abstractproperty
    def is_pressed(self):
        """
        Indicates pressed state.
        """

    @abstractproperty
    def is_checked(self):
        """
        Indicates checked state.
        """

    @abstractproperty
    def is_visible(self):
        """
        Indicates visible state.
        """

    @abstractproperty
    def is_enabled(self):
        """
        Indicates enabled state.
        """

    @abstractproperty
    def acc_parent_count(self):
        """
        Property for parent child count.
        """

    @abstractproperty
    def acc_child_count(self):
        """
        Property for element child count.
        """

    @abstractproperty
    def acc_role(self):
        """
        Property for element role.
        """

    @abstractproperty
    def acc_name(self):
        """
        Property for element name.
        Also need to specify setter for this property
        """

    @abstractmethod
    def set_name(self, name):
        """
        Sets element name.

        Arguments:
            - name: string, element name.

        Returns:
            - None
        """

    @abstractmethod
    def set_focus(self):
        """
        Sets focus to element.

        Arguments:
            - None

        Returns:
            - None
        """

    @abstractproperty
    def acc_c_name(self):
        """
        Property for combined name (role name + name).
        """

    @abstractproperty
    def acc_location(self):
        """
        Property for element location.
        """

    @abstractproperty
    def acc_value(self):
        """
        Property for element value.
        Also need to specify setter for this property.
        """

    @abstractmethod
    def set_value(self, value):
        """
        Sets element value.

        Arguments:
            - value: string, element value.

        Returns:
            - None
        """

    @abstractproperty
    def acc_default_action(self):
        """
        Property for element default action.
        """

    @abstractproperty
    def acc_description(self):
        """
        Property for element description.
        """

    @abstractproperty
    def acc_help(self):
        """
        Property for element help.
        """

    @abstractproperty
    def acc_help_topic(self):
        """
        Property for element topic.
        """

    @abstractproperty
    def acc_keyboard_shortcut(self):
        """
        Property for element keyboard shortcut.
        """

    @abstractproperty
    def acc_parent(self):
        """
        Property for element parent.
        """

    @abstractproperty
    def acc_selection(self):
        """
        Property for element selection.
        """

    @abstractproperty
    def acc_state(self):
        """
        Property for element state.
        """

    @abstractmethod
    def acc_do_default_action(self):
        """
        Does default action for element.

        Arguments:
            - None

        Returns:
            - None
        """

    @abstractproperty
    def acc_focus(self):
        """
        Property for element in focus.
        """

    @abstractmethod
    def acc_select(self, i_selection):
        """
        Does default action for element.

        Arguments:
            - None

        Returns:
            - None
        """

    @abstractproperty
    def acc_role_name(self):
        """
        Property for element role name.
        """

    @abstractmethod
    def __iter__(self):
        """Iterate all child Element"""

    @abstractmethod
    def find(self, only_visible=True, **kwargs):
        """
        Finds first child element.

        Arguments:
            - only_visible: bool, flag that indicates will we search only
            through visible elements.
            - role: string or lambda e.g. lambda x: x == 13
            - name: string or lambda.
            - c_name: string or lambda.
            - location: string or lambda.
            - value: string or lambda.
            - default_action: string or lambda.
            - description: string or lambda.
            - help: string or lambda.
            - help_topic: string or lambda.
            - keyboard_shortcut: string or lambda.
            - selection: string or lambda.
            - state: string or lambda.
            - focus: string or lambda.
            - role_name: string or lambda.
            - parent_count: string or lambda.
            - child_count: string or lambda.

        Returns:
            - Element that was found otherwise exception will be raised.
        """

    @abstractmethod
    def findall(self, only_visible=True, **kwargs):
        """
        Find all child element.

        Arguments:
            - only_visible: bool, flag that indicates will we search only
            through visible elements.
            - role: string or lambda e.g. lambda x: x == 13
            - name: string or lambda.
            - c_name: string or lambda.
            - location: string or lambda.
            - value: string or lambda.
            - default_action: string or lambda.
            - description: string or lambda.
            - help: string or lambda.
            - help_topic: string or lambda.
            - keyboard_shortcut: string or lambda.
            - selection: string or lambda.
            - state: string or lambda.
            - focus: string or lambda.
            - role_name: string or lambda.
            - parent_count: string or lambda.
            - child_count: string or lambda.

        Returns:
            - List of all elements that was found otherwise None.
        """

    @abstractmethod
    def is_object_exists(self, **kwargs):
        """
        Verifies is object exists.

        Arguments:
            - role: string or lambda e.g. lambda x: x == 13
            - name: string or lambda.
            - c_name: string or lambda.
            - location: string or lambda.
            - value: string or lambda.
            - default_action: string or lambda.
            - description: string or lambda.
            - help: string or lambda.
            - help_topic: string or lambda.
            - keyboard_shortcut: string or lambda.
            - selection: string or lambda.
            - state: string or lambda.
            - focus: string or lambda.
            - role_name: string or lambda.
            - parent_count: string or lambda.
            - child_count: string or lambda.

        Returns:
            - True if object exists otherwise False.
        """

    @abstractmethod
    def toxml(self):
        """
        Convert Element Tree to XML.

        Arguments:
            - None

        Returns:
            - None
        """
