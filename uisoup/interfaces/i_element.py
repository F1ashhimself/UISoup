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

import re
from inspect import ismethod
from types import FunctionType
from abc import ABCMeta, abstractmethod, abstractproperty
import xml.dom.minidom

from ..utils import _Utils


class IElement(object):
    """
    Class that describes UI object.
    """

    __metaclass__ = ABCMeta

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
    def acc_name(self):
        """
        Property for element name.
        Also need to specify setter for this property
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
    def acc_description(self):
        """
        Property for element description.
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
    def acc_focused_element(self):
        """
        Property for element in focus.
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
            - description: string or lambda.
            - selection: string or lambda.
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
            - description: string or lambda.
            - selection: string or lambda.
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
            - description: string or lambda.
            - selection: string or lambda.
            - role_name: string or lambda.
            - parent_count: string or lambda.
            - child_count: string or lambda.

        Returns:
            - True if object exists otherwise False.
        """

    def toxml(self):
        """
        Convert Element Tree to XML.

        Arguments:
            - None

        Returns:
            - None
        """

        obj_document = xml.dom.minidom.Document()
        lst_queue = [(self, obj_document)]

        while lst_queue:
            obj_element, obj_tree = lst_queue.pop(0)
            role_name = obj_element.acc_role_name
            obj_name = obj_element.acc_name
            str_name = unicode(obj_name) if obj_name else ''
            str_location = ','.join(str(x) for x in obj_element.acc_location)
            obj_sub_tree = xml.dom.minidom.Element(role_name)
            obj_sub_tree.ownerDocument = obj_document

            try:
                obj_sub_tree.attributes['Name'] = str_name
            except:
                obj_sub_tree.attributes['Name'] = \
                    str_name.encode('unicode-escape')

            obj_sub_tree.attributes['Location'] = str_location
            obj_tree.appendChild(obj_sub_tree)

            if obj_element.acc_child_count:
                for obj_element_child in obj_element:
                    lst_queue.append((obj_element_child, obj_sub_tree))

        return obj_document.toprettyxml()

    def __str__(self):
        result = '[Role: %s(0x%X) | Name: %r | Child count: %d]' % \
                 (self.acc_role_name,
                  self.acc_role,
                  self.acc_name,
                  self.acc_child_count)

        return result

    def _match(self, only_visible, **kwargs):
        """
        Match method.

        Arguments:
            - only_visible: bool, flag that indicates will we search only
            through visible elements.
            - role: string or lambda e.g. lambda x: x == 13
            - name: string or lambda.
            - c_name: string or lambda.
            - location: string or lambda.
            - value: string or lambda.
            - description: string or lambda.
            - parent: string or lambda.
            - selection: string or lambda.
            - role_name: string or lambda.

        Returns:
            - True if element was matched otherwise False.
        """

        try:
            if only_visible and not self.is_visible:
                return False

            for str_property, expected_result in kwargs.items():
                attr = getattr(self, 'acc_' + str_property)
                if ismethod(attr):
                    attr = attr()

                if type(expected_result) is FunctionType:
                    if not expected_result(attr):
                        return False
                else:
                    regex = _Utils.convert_wildcard_to_regex(expected_result)
                    if not re.match(regex, attr):
                        return False
        except:
            return False
        else:
            return True
