# !/usr/bin/env python
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

import re
import sys
from subprocess import CalledProcessError

from Quartz import CoreGraphics as cg

from ..interfaces.i_soup import ISoup
from ..utils.mac_utils import MacUtils, ApplescriptCommands
from .element import MacElement
from .. import TooSaltyUISoupException


class MacSoup(ISoup):

    mouse = None
    keyboard = None
    _default_sys_encoding = sys.stdout.encoding

    def get_object_by_coordinates(self, x, y):
        pass

    def is_window_exists(self, obj_handle):
        try:
            self.get_window(obj_handle)
            return True
        except TooSaltyUISoupException:
            return False

    def get_window(self, obj_handle=None):
        filters = cg.kCGWindowListOptionOnScreenOnly | \
            cg.kCGWindowListExcludeDesktopElements * bool(obj_handle)

        obj_name = obj_handle if obj_handle else u'DesktopWindow Server'
        obj_name = \
            obj_name if type(obj_name) == unicode else obj_name.decode('utf-8')

        regex = MacUtils.convert_wildcard_to_regex(obj_name)

        win_list = cg.CGWindowListCopyWindowInfo(filters, cg.kCGNullWindowID)

        window = filter(lambda x:
                        re.match(regex,
                                 x.get('kCGWindowName', '') +
                                 x.get('kCGWindowOwnerName', '')),
                        win_list)

        if not window:
            obj_name = obj_name.encode(self._default_sys_encoding,
                                       errors='ignore')
            raise TooSaltyUISoupException('Can\'t find window "%s".' %
                                          obj_name)
        window = window[0]
        process_name = window['kCGWindowOwnerName']
        process_id = window['kCGWindowOwnerPID']
        selector = MacUtils.execute_applescript_command(
            ApplescriptCommands.get_front_window_element(
                process_name)).strip()
        selector = \
            selector if type(selector) == unicode else selector.decode('utf-8')

        template = r'window %s of application process %s'
        match = re.match(template % ('(.+)', '(.+)'), selector)
        window_selector = template % tuple('"%s"' % e for e in match.groups())

        return MacElement(window_selector, process_id)

    def get_visible_window_list(self):
        win_list = cg.CGWindowListCopyWindowInfo(
            cg.kCGWindowListOptionOnScreenOnly |
            cg.kCGWindowListExcludeDesktopElements,
            cg.kCGNullWindowID)

        win_names = \
            [w.get('kCGWindowName', '') + w.get('kCGWindowOwnerName', '') for
             w in win_list if w.get('kCGWindowName', '') and 0 not in
             [int(w.get('kCGWindowBounds', 0)['Height']),
              int(w.get('kCGWindowBounds', 0)['Width'])]]

        windows = list()
        for win_name in win_names:
            try:
                windows.append(self.get_window(win_name))
            except CalledProcessError:
                continue

        return windows

    def get_visible_object_list(self, window_name):
        pass
