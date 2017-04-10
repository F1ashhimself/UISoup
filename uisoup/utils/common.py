# !/usr/bin/env python

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

import re
import sys

from .. import TooSaltyUISoupException


class CommonUtils(object):

    @classmethod
    def convert_wildcard_to_regex(cls, wildcard):
        """
        Converts wildcard to regex.

        :param str wildcard: wildcard.
        :rtype: str
        :return: regex pattern.
        """
        regex = re.escape(wildcard)
        regex = regex.replace(r'\?', r'[\s\S]{1}')
        regex = regex.replace(r'\*', r'[\s\S]*')

        return '^%s$' % regex

    @classmethod
    def replace_inappropriate_symbols(cls, text):
        """
        Replaces inappropriate symbols e.g. \xa0 (non-breaking space) to
        normal space.

        :param str text: text in which symbols should be replaced.
        :rtype: str
        :return: processed text.
        """
        replace_pairs = [(u'\xa0', ' '),
                         (u'\u2014', '-')]

        for from_, to_ in replace_pairs:
            text = text.replace(from_, to_)

        return text

    @classmethod
    def verify_xy_coordinates(cls, x, y):
        """
        Verifies that x and y is instance of int otherwise raises exception.

        :param x: x variable.
        :param y: y variable.
        """
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TooSaltyUISoupException(
                'x and y arguments should hold int coordinates.')

    @classmethod
    def verify_mouse_button_name(cls, button_name, supported_names):
        """
        Verifies that button name is supported otherwise raises exception.

        :param str button_name: button name.
        :param list[str] supported_names: supported button names.
        """
        if button_name not in supported_names:
            raise TooSaltyUISoupException(
                'Button name should be one of supported %s.' %
                repr(supported_names))

    @classmethod
    def is_python_3(cls):
        """
        Indicates is currently python 3 used or not.
        
        :rtype: bool
        :return: boolean indicator. 
        """
        return sys.version_info.major == 3
