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
