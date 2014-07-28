# !/usr/bin/env python

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

from .. import TooSaltyUISoupException


class _Utils(object):

    @classmethod
    def convert_wildcard_to_regex(cls, wildcard):
        """
        Converts wildcard to regex.

        Arguments:
            - wildcard: string, wildcard.

        Returns:
            - String with regex pattern.
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

        Arguments:
            - text: string, text in which symbols should be replaced.
            Should be in unicode.

        Returns:
            - string with processed text.
        """

        replace_pairs = [(u'\xa0', ' '),
                         (u'\u2014', '-')]

        for from_, to_ in replace_pairs:
            text = text.replace(from_, to_)

        return text

    @classmethod
    def verify_xy_coordinates(self, x, y):
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

    @classmethod
    def verify_mouse_button_name(self, button_name, supported_names):
        """
        Verifies that button name is supported otherwise raises exception.

        Arguments:
            - button_name: string, button name.
            - supported_names: list, supported button names.

        Returns:
            - None
        """

        if not button_name in supported_names:
            raise TooSaltyUISoupException(
                'Button name should be one of supported %s.' %
                repr(supported_names))
