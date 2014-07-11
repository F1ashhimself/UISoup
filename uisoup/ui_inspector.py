#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


from os import system
from time import sleep
from inspect import ismethod
from platform import system as platform_system

from . import uisoup


class UIInspector(object):

    @classmethod
    def get_current_element_info(cls, obj_element):
        """
        Gets current element info.

        Arguments:
            - obj_element: object element.

        Returns:
            - String with element attributes.
        """

        dict_info = {}
        lst_attribute_name_list = ['acc_role_name',
                                   'acc_name',
                                   'acc_value',
                                   'acc_location',
                                   'acc_description',
                                   'acc_child_count']

        for attr in lst_attribute_name_list:
            try:
                value = getattr(obj_element, attr)
                if ismethod(value):
                    dict_info[attr] = value()
                else:
                    dict_info[attr] = value
            except:
                dict_info[attr] = None

        return '\n'.join('%s:\t%r' % (attr, dict_info[attr]) for
                         attr in lst_attribute_name_list)


def main():
    """
    Starts UI Inspector.

    Arguments:
        - None

    Returns:
        - None
    """

    try:
        x_old, y_old = None, None
        while True:
            x, y = uisoup.mouse.get_position()
            if (x, y) != (x_old, y_old):
                x_old, y_old = x, y
                obj_element = uisoup.get_object_by_coordinates(x, y)
                clear_command = \
                    'cls' if platform_system() == 'Windows' else 'clear'
                printable_data = \
                    UIInspector.get_current_element_info(obj_element)
                system(clear_command)
                print printable_data
            sleep(0.5)
    except KeyboardInterrupt:
        system('cls')
