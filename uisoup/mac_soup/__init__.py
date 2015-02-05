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

import sys
import re

from Quartz import CoreGraphics as CG

from ..interfaces.i_soup import ISoup
from ..utils.mac_utils import MacUtils
from .element import MacElement
from .mouse import MacMouse
from .keyboard import MacKeyboard
from .. import TooSaltyUISoupException


class MacSoup(ISoup):

    mouse = MacMouse()
    keyboard = MacKeyboard()
    _default_sys_encoding = sys.stdout.encoding or sys.getdefaultencoding()

    def get_object_by_coordinates(self, x, y):
        result = None

        try:
            window_handle = \
                MacUtils.ApplescriptExecutor.get_frontmost_window_name()

            window = self.get_window(window_handle)

            # Sorting by layer from big to small.
            sorted_objects = sorted(window.findall(),
                                    lambda x, y: y._layer_num - x._layer_num)

            cur_x, cur_y = self.mouse.get_position()
            for element in sorted_objects:
                x, y, w, h = element.acc_location
                if x <= cur_x < x + w and y <= cur_y < y + h:
                    result = element
                    break
        except:
            pass

        return result

    def is_window_exists(self, obj_handle):
        try:
            self.get_window(obj_handle)
            return True
        except TooSaltyUISoupException:
            return False

    def get_window(self, obj_handle=None):
        filters = CG.kCGWindowListOptionOnScreenOnly | \
            CG.kCGWindowListExcludeDesktopElements * bool(obj_handle)

        obj_name = obj_handle if obj_handle else u'DesktopWindow Server'
        obj_name = \
            obj_name if type(obj_name) == unicode else obj_name.decode('utf-8')

        regex = MacUtils.convert_wildcard_to_regex(obj_name)

        win_list = CG.CGWindowListCopyWindowInfo(filters, CG.kCGNullWindowID)

        window = filter(lambda x:
                        re.match(MacUtils.replace_inappropriate_symbols(regex),
                                 MacUtils.replace_inappropriate_symbols(
                                     x.get('kCGWindowName', '')) +
                                 x.get('kCGWindowOwnerName', ''),
                                 re.IGNORECASE)
                        if x.get('kCGWindowName', '') else False,
                        win_list)

        window = window[0] if window else window
        if not window:
            obj_name = obj_name.encode(self._default_sys_encoding,
                                       errors='ignore')
            raise TooSaltyUISoupException('Can\'t find window "%s".' %
                                          obj_name)

        process_name = window['kCGWindowOwnerName']
        window_name = window['kCGWindowName']
        process_id = int(window['kCGWindowOwnerPID'])
        # Escape double quotes in window name.
        window_name = window_name.replace('"', '\\"')

        selector = \
            MacUtils.ApplescriptExecutor.get_apple_event_descriptor(
                'window "%s"' % window_name,
                process_name).applescript_specifier
        selector = \
            selector if type(selector) == unicode else selector.decode('utf-8')

        return MacElement(selector, 0, process_name, process_id)

    def get_visible_window_list(self):
        win_list = CG.CGWindowListCopyWindowInfo(
            CG.kCGWindowListOptionOnScreenOnly |
            CG.kCGWindowListExcludeDesktopElements,
            CG.kCGNullWindowID)

        win_names = \
            [w.get('kCGWindowName', '') + w.get('kCGWindowOwnerName', '') for
             w in win_list if w.get('kCGWindowName', '') and 0 not in
             [int(w.get('kCGWindowBounds', 0)['Height']),
              int(w.get('kCGWindowBounds', 0)['Width'])]]

        windows = list()
        for win_name in win_names:
            try:
                windows.append(self.get_window(win_name))
            except TooSaltyUISoupException:
                continue

        return windows

    def get_visible_object_list(self, window_name):
        window = self.get_window(window_name)
        objects = window.findall(
            only_visible=True,
            location=lambda x: 0 not in x[2:])

        return objects
