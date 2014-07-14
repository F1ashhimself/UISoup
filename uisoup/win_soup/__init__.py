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

import re
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.automation
import comtypes.client
import sys

from ..utils.win_utils import WinUtils
from .. import TooSaltyUISoupException
from ..interfaces.i_soup import ISoup
from .element import WinElement
from .mouse import WinMouse
from .keyboard import WinKeyboard

comtypes.client.GetModule('oleacc.dll')


class WinSoup(ISoup):

    mouse = WinMouse()
    keyboard = WinKeyboard()
    _default_sys_encoding = sys.stdout.encoding or sys.getdefaultencoding()

    class _EnumWindowsCallback(object):

        last_handle = None

        @classmethod
        def callback(cls, handle, wildcard):
            wildcard = ctypes.cast(wildcard, ctypes.c_wchar_p).value

            wildcard = WinUtils.replace_inappropriate_symbols(wildcard)
            length = ctypes.windll.user32.GetWindowTextLengthW(handle) + 1
            buff = ctypes.create_unicode_buffer(length)
            ctypes.windll.user32.GetWindowTextW(handle, buff, length)
            win_text = WinUtils.replace_inappropriate_symbols(buff.value)

            if re.match(wildcard, win_text):
                cls.last_handle = handle

            return True

    def get_object_by_coordinates(self, x, y):
        obj_point = ctypes.wintypes.POINT()
        obj_point.x = x
        obj_point.y = y
        i_accessible = ctypes.POINTER(comtypes.gen.Accessibility.IAccessible)()
        obj_child_id = comtypes.automation.VARIANT()
        ctypes.oledll.oleacc.AccessibleObjectFromPoint(
            obj_point,
            ctypes.byref(i_accessible),
            ctypes.byref(obj_child_id))

        return WinElement(i_accessible, obj_child_id.value or 0)

    def is_window_exists(self, obj_handle):
        try:
            self.get_window(obj_handle)
            return True
        except TooSaltyUISoupException:
            return False

    def get_window(self, obj_handle=None):
        if obj_handle in (0, None):
            obj_handle = ctypes.windll.user32.GetDesktopWindow()
        elif isinstance(obj_handle, basestring):
            obj_name = unicode(obj_handle)

            regex = WinUtils.convert_wildcard_to_regex(obj_name)

            enum_windows_proc = \
                ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int),
                                   ctypes.POINTER(ctypes.c_int))
            self._EnumWindowsCallback.last_handle = None
            ctypes.windll.user32.EnumWindows(enum_windows_proc(
                self._EnumWindowsCallback.callback),
                ctypes.c_wchar_p(regex))

            obj_handle = self._EnumWindowsCallback.last_handle

            if not obj_handle:
                obj_name = obj_name.encode(self._default_sys_encoding,
                                           errors='ignore')
                raise TooSaltyUISoupException('Can\'t find window "%s".' %
                                              obj_name)

        try:
            return WinElement(obj_handle, 0)
        except:
            raise TooSaltyUISoupException(
                'Error when retrieving window with handle=%r' % obj_handle)

    def get_visible_window_list(self):
        result = self.get_window().findall(
            only_visible=True,
            name=lambda x: x,
            role_name=lambda x: x in ['frm', 'pane'],
            location=lambda x: 0 not in x[2:])

        return result

    def get_visible_object_list(self, window_name):
        window = self.get_window(window_name)
        objects = window.findall(
            only_visible=True,
            role_name=lambda x: x != 'frm',
            location=lambda x: 0 not in x[2:])

        return objects
